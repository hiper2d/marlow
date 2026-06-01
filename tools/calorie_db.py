"""
calorie_db — SQLite store for the calorie-tracking project.

One row per food/drink entry. Entries arrive as Telegram messages (photo
and/or text note) via the `poll_food` handler, which inserts them as
*pending* rows (no estimate yet). Marlow's tick session then reads each
pending entry (vision on the photo + the text note) and fills in the
estimate via `estimate`. The nightly `calorie_digest` handler rolls up a
local day and stores the summary in `digests`.

Design choices:
  - kcal is stored as a LOW/HIGH range, not a single fake-precise number.
    Portion size is the dominant error source; a range is honest.
  - Entries are grouped by LOCAL date (America/New_York by default,
    override with CALORIE_TZ) so "a day" matches Alex's day, not UTC.
  - `update_id` is UNIQUE — the Telegram update id is the dedupe key, so
    re-running a fetch never double-counts a meal.

Importable:
    from tools.calorie_db import add_pending, fill_estimate, get_day

CLI (handlers call these; Simona uses them to pull data for discussion):
    uv run python tools/calorie_db.py init
    uv run python tools/calorie_db.py pending
    uv run python tools/calorie_db.py estimate --id 12 --description "..." \
        --kcal-low 600 --kcal-high 850 --protein 35 --carbs 70 --fat 25 \
        --source both --confidence medium --comment "big portion of rice"
    uv run python tools/calorie_db.py day [--date YYYY-MM-DD]
    uv run python tools/calorie_db.py range --start YYYY-MM-DD --end YYYY-MM-DD
    uv run python tools/calorie_db.py recent [--days 7]
    uv run python tools/calorie_db.py save-digest --date YYYY-MM-DD \
        --comment "..." [--sent]
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "projects" / "calories" / "calories.db"

# Local "day" boundary for grouping entries. Alex is Eastern; override via
# CALORIE_TZ if that ever changes.
LOCAL_TZ = ZoneInfo(os.environ.get("CALORIE_TZ", "America/New_York"))

VALID_SOURCES = ("photo", "text", "both", "voice")
VALID_CONFIDENCE = ("low", "medium", "high")


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _local_date(ts_utc: datetime) -> str:
    """Map a UTC timestamp to its YYYY-MM-DD in Alex's local timezone."""
    return ts_utc.astimezone(LOCAL_TZ).date().isoformat()


def _today_local() -> str:
    return _local_date(_now_utc())


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS entries (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                update_id   INTEGER UNIQUE,           -- Telegram dedupe key
                ts_utc      TEXT NOT NULL,            -- ISO8601 UTC of the message
                local_date  TEXT NOT NULL,            -- YYYY-MM-DD in LOCAL_TZ
                raw_text    TEXT,                     -- Alex's note / voice transcript
                photo_path  TEXT,                     -- relative path to saved photo
                audio_path  TEXT,                     -- relative path to saved voice note
                description TEXT,                     -- Marlow's food identification
                kcal_low    INTEGER,
                kcal_high   INTEGER,
                protein_g   REAL,
                carbs_g     REAL,
                fat_g       REAL,
                source      TEXT,                     -- photo | text | both
                confidence  TEXT,                     -- low | medium | high
                comment     TEXT,                     -- Marlow's per-entry note
                status      TEXT NOT NULL DEFAULT 'pending',  -- pending | estimated
                created_at  TEXT NOT NULL,
                estimated_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_entries_local_date
                ON entries(local_date);
            CREATE INDEX IF NOT EXISTS idx_entries_status
                ON entries(status);

            CREATE TABLE IF NOT EXISTS digests (
                local_date  TEXT PRIMARY KEY,
                entry_count INTEGER,
                kcal_low    INTEGER,
                kcal_high   INTEGER,
                protein_g   REAL,
                carbs_g     REAL,
                fat_g       REAL,
                comment     TEXT,
                created_at  TEXT NOT NULL,
                sent_at     TEXT
            );
            """
        )
        # Migration: add columns introduced after the first DB was created.
        cols = {r[1] for r in conn.execute("PRAGMA table_info(entries)")}
        if "audio_path" not in cols:
            conn.execute("ALTER TABLE entries ADD COLUMN audio_path TEXT")
        if "amendments" not in cols:
            # JSON array of prior states, appended each time an already-
            # estimated entry is corrected. Keeps history honest.
            conn.execute("ALTER TABLE entries ADD COLUMN amendments TEXT")


def add_pending(
    *,
    update_id: int | None,
    ts_utc: datetime,
    raw_text: str | None,
    photo_path: str | None,
    source: str,
    audio_path: str | None = None,
) -> int | None:
    """Insert a pending entry (no estimate yet). Returns the row id, or
    None if this update_id was already ingested (dedupe)."""
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO entries
                (update_id, ts_utc, local_date, raw_text, photo_path,
                 audio_path, source, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
            """,
            (
                update_id,
                ts_utc.isoformat(timespec="seconds"),
                _local_date(ts_utc),
                raw_text,
                photo_path,
                audio_path,
                source,
                _now_utc().isoformat(timespec="seconds"),
            ),
        )
        return cur.lastrowid if cur.rowcount else None


def fill_estimate(
    *,
    entry_id: int,
    description: str,
    kcal_low: int,
    kcal_high: int,
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    source: str,
    confidence: str,
    comment: str | None,
    reason: str | None = None,
) -> bool:
    """Fill in (or correct) Marlow's estimate for an entry. The same call
    handles the first estimate and later corrections: if the entry was
    already `estimated`, its prior values are snapshotted into
    `amendments` (with `reason`) before being overwritten, so history is
    never silently lost. Returns False if no such row."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM entries WHERE id = ?", (entry_id,)).fetchone()
        if row is None:
            return False

        amendments = json.loads(row["amendments"]) if row["amendments"] else []
        if row["status"] == "estimated":
            amendments.append(
                {
                    "at": _now_utc().isoformat(timespec="seconds"),
                    "reason": reason,
                    "was": {
                        "description": row["description"],
                        "kcal_low": row["kcal_low"], "kcal_high": row["kcal_high"],
                        "protein_g": row["protein_g"], "carbs_g": row["carbs_g"],
                        "fat_g": row["fat_g"], "confidence": row["confidence"],
                    },
                }
            )

        conn.execute(
            """
            UPDATE entries SET
                description = ?, kcal_low = ?, kcal_high = ?,
                protein_g = ?, carbs_g = ?, fat_g = ?,
                source = ?, confidence = ?, comment = ?,
                status = 'estimated', estimated_at = ?, amendments = ?
            WHERE id = ?
            """,
            (
                description, kcal_low, kcal_high,
                protein_g, carbs_g, fat_g,
                source, confidence, comment,
                _now_utc().isoformat(timespec="seconds"),
                json.dumps(amendments) if amendments else None,
                entry_id,
            ),
        )
        return True


def void(entry_id: int, reason: str | None = None) -> bool:
    """Mark an entry as not-eaten (logged then retracted — "scratch the
    pizza"). Excluded from totals like a dismissal, but semantically "this
    was food Alex decided not to count," distinct from non-food chatter."""
    with _connect() as conn:
        cur = conn.execute(
            "UPDATE entries SET status = 'voided', comment = ?, estimated_at = ? WHERE id = ?",
            (reason, _now_utc().isoformat(timespec="seconds"), entry_id),
        )
        return cur.rowcount > 0


def get_entry(entry_id: int) -> dict | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM entries WHERE id = ?", (entry_id,)).fetchone()
    return _row_to_dict(row) if row else None


def dismiss(entry_id: int, reason: str | None = None) -> bool:
    """Mark a pending entry as not-food (greeting, chatter, etc.) so it
    leaves the pending queue and never counts toward totals."""
    with _connect() as conn:
        cur = conn.execute(
            """
            UPDATE entries
               SET status = 'dismissed', comment = ?,
                   estimated_at = ?
             WHERE id = ?
            """,
            (reason, _now_utc().isoformat(timespec="seconds"), entry_id),
        )
        return cur.rowcount > 0


def _row_to_dict(row: sqlite3.Row) -> dict:
    return {k: row[k] for k in row.keys()}


def get_pending() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM entries WHERE status = 'pending' ORDER BY ts_utc"
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def _totals(entries: list[dict]) -> dict:
    est = [e for e in entries if e["status"] == "estimated"]
    pending = [e for e in entries if e["status"] == "pending"]
    return {
        "kcal_low": sum(e["kcal_low"] or 0 for e in est),
        "kcal_high": sum(e["kcal_high"] or 0 for e in est),
        "protein_g": round(sum(e["protein_g"] or 0 for e in est), 1),
        "carbs_g": round(sum(e["carbs_g"] or 0 for e in est), 1),
        "fat_g": round(sum(e["fat_g"] or 0 for e in est), 1),
        "estimated_count": len(est),
        "pending_count": len(pending),
    }


def get_day(date: str | None = None) -> dict:
    date = date or _today_local()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM entries WHERE local_date = ? ORDER BY ts_utc",
            (date,),
        ).fetchall()
    entries = [_row_to_dict(r) for r in rows]
    return {"date": date, "totals": _totals(entries), "entries": entries}


def get_range(start: str, end: str) -> dict:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT local_date,
                   COUNT(*) AS entry_count,
                   SUM(CASE WHEN status='estimated' THEN kcal_low ELSE 0 END) AS kcal_low,
                   SUM(CASE WHEN status='estimated' THEN kcal_high ELSE 0 END) AS kcal_high,
                   ROUND(SUM(CASE WHEN status='estimated' THEN protein_g ELSE 0 END), 1) AS protein_g,
                   ROUND(SUM(CASE WHEN status='estimated' THEN carbs_g ELSE 0 END), 1) AS carbs_g,
                   ROUND(SUM(CASE WHEN status='estimated' THEN fat_g ELSE 0 END), 1) AS fat_g
            FROM entries
            WHERE local_date BETWEEN ? AND ?
            GROUP BY local_date ORDER BY local_date
            """,
            (start, end),
        ).fetchall()
    days = [_row_to_dict(r) for r in rows]
    n = len(days) or 1
    avg = {
        "kcal_low": round(sum(d["kcal_low"] or 0 for d in days) / n),
        "kcal_high": round(sum(d["kcal_high"] or 0 for d in days) / n),
        "protein_g": round(sum(d["protein_g"] or 0 for d in days) / n, 1),
        "carbs_g": round(sum(d["carbs_g"] or 0 for d in days) / n, 1),
        "fat_g": round(sum(d["fat_g"] or 0 for d in days) / n, 1),
    }
    return {"start": start, "end": end, "days": days, "daily_average": avg}


def undelivered_digests() -> list[str]:
    """Local dates that have at least one estimated entry but no digest
    marked sent. Lets the nightly task catch up across missed ticks
    (laptop asleep at digest time) instead of summarizing the wrong day."""
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT DISTINCT e.local_date
            FROM entries e
            LEFT JOIN digests d ON d.local_date = e.local_date
            WHERE e.status = 'estimated'
              AND (d.local_date IS NULL OR d.sent_at IS NULL)
            ORDER BY e.local_date
            """
        ).fetchall()
    return [r["local_date"] for r in rows]


def save_digest(*, date: str, comment: str, sent: bool) -> dict:
    day = get_day(date)
    t = day["totals"]
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO digests
                (local_date, entry_count, kcal_low, kcal_high,
                 protein_g, carbs_g, fat_g, comment, created_at, sent_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(local_date) DO UPDATE SET
                entry_count=excluded.entry_count,
                kcal_low=excluded.kcal_low, kcal_high=excluded.kcal_high,
                protein_g=excluded.protein_g, carbs_g=excluded.carbs_g,
                fat_g=excluded.fat_g, comment=excluded.comment,
                sent_at=COALESCE(excluded.sent_at, digests.sent_at)
            """,
            (
                date, t["estimated_count"], t["kcal_low"], t["kcal_high"],
                t["protein_g"], t["carbs_g"], t["fat_g"], comment,
                _now_utc().isoformat(timespec="seconds"),
                _now_utc().isoformat(timespec="seconds") if sent else None,
            ),
        )
    return {"date": date, "totals": t, "comment": comment, "sent": sent}


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _print(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def main() -> int:
    p = argparse.ArgumentParser(description="Calorie tracking SQLite store.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Create tables.")
    sub.add_parser("pending", help="List entries awaiting an estimate.")

    pe = sub.add_parser(
        "estimate",
        help="Estimate a pending entry, or correct an estimated one (pass --reason).",
    )
    pe.add_argument("--id", type=int, required=True)
    pe.add_argument("--description", required=True)
    pe.add_argument("--kcal-low", type=int, required=True)
    pe.add_argument("--kcal-high", type=int, required=True)
    pe.add_argument("--protein", type=float, default=0.0)
    pe.add_argument("--carbs", type=float, default=0.0)
    pe.add_argument("--fat", type=float, default=0.0)
    pe.add_argument("--source", choices=VALID_SOURCES, required=True)
    pe.add_argument("--confidence", choices=VALID_CONFIDENCE, required=True)
    pe.add_argument("--comment", default=None)
    pe.add_argument("--reason", default=None,
                    help="Why this corrects a prior estimate (snapshots the old values).")

    pdm = sub.add_parser("dismiss", help="Mark a pending entry as not-food.")
    pdm.add_argument("--id", type=int, required=True)
    pdm.add_argument("--reason", default=None)

    pv = sub.add_parser("void", help="Retract a logged entry Alex didn't actually eat.")
    pv.add_argument("--id", type=int, required=True)
    pv.add_argument("--reason", default=None)

    pg = sub.add_parser("get", help="Fetch one entry by id (with amendment history).")
    pg.add_argument("--id", type=int, required=True)

    pd = sub.add_parser("day", help="One local day's entries + totals.")
    pd.add_argument("--date", default=None, help="YYYY-MM-DD (default: today local).")

    pr = sub.add_parser("range", help="Per-day totals + daily average over a range.")
    pr.add_argument("--start", required=True)
    pr.add_argument("--end", required=True)

    prc = sub.add_parser("recent", help="Last N days (shorthand for range).")
    prc.add_argument("--days", type=int, default=7)

    psd = sub.add_parser("save-digest", help="Store the daily digest summary.")
    psd.add_argument("--date", default=None)
    psd.add_argument("--comment", required=True)
    psd.add_argument("--sent", action="store_true", help="Mark as already sent.")

    args = p.parse_args()

    if args.cmd == "init":
        init_db()
        _print({"ok": True, "db": str(DB_PATH)})
    elif args.cmd == "pending":
        _print(get_pending())
    elif args.cmd == "estimate":
        ok = fill_estimate(
            entry_id=args.id, description=args.description,
            kcal_low=args.kcal_low, kcal_high=args.kcal_high,
            protein_g=args.protein, carbs_g=args.carbs, fat_g=args.fat,
            source=args.source, confidence=args.confidence, comment=args.comment,
            reason=args.reason,
        )
        _print({"ok": ok, "id": args.id})
    elif args.cmd == "dismiss":
        _print({"ok": dismiss(args.id, args.reason), "id": args.id})
    elif args.cmd == "void":
        _print({"ok": void(args.id, args.reason), "id": args.id})
    elif args.cmd == "get":
        _print(get_entry(args.id))
    elif args.cmd == "day":
        _print(get_day(args.date))
    elif args.cmd == "range":
        _print(get_range(args.start, args.end))
    elif args.cmd == "recent":
        from datetime import timedelta
        end = _now_utc().astimezone(LOCAL_TZ).date()
        start = end - timedelta(days=args.days - 1)
        _print(get_range(start.isoformat(), end.isoformat()))
    elif args.cmd == "save-digest":
        date = args.date or _today_local()
        _print(save_digest(date=date, comment=args.comment, sent=args.sent))

    return 0


if __name__ == "__main__":
    sys.exit(main())
