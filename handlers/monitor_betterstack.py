"""
monitor_betterstack — app-level error watch for the Werewolf game via Betterstack.

The FOURTH werewolf-ops workstream, and the companion to monitor_health.
monitor_keys watches what the free tier COSTS, werewolf_stats what it PRODUCES,
monitor_health whether a *game* WORKS (its `errorState` in Firestore). This
watches whether the *app* is throwing — the failures that never reach a game
doc: unhandled exceptions, provider 5xx, Next.js server errors, dead requests.

The game already ships structured logs to Betterstack via `@logtail/node`
(werewolf-client/app/utils/logger.ts). We read them back through Betterstack's
ClickHouse HTTP query API (the app's source token is ingest-only; this needs a
separate query credential — a ClickHouse connection, created under Telemetry →
Integrations → SQL API).

── Storage, and why an S3 table shows up ────────────────────────────────────
Betterstack Telemetry is ClickHouse with tiered storage. Recent rows sit in a
fast hot table — `remote(<source>_logs)`; older rows are flushed to cheap S3 —
`s3Cluster(primary, <source>_s3)`. The Live-tail UI stitches both together so a
human never sees the seam. The raw SQL API does not: you address a table.
For THIS source the flush to S3 is aggressive and the volume is tiny, so the
hot table is almost always empty and S3 holds effectively everything, including
near-real-time rows. So we query S3. (The cost: the freshest ~couple minutes may
still be unflushed in the hot tier — caught on the next tick, since the window
overlaps. Fine for an hourly error watch. Union the two if we ever want lower
latency.)

── Schema ───────────────────────────────────────────────────────────────────
There is no flat `level` column. Each row's `raw` is the full JSON log line;
level + message come out with `JSONExtractString(raw, 'level' | 'message')`.
Levels seen in practice: info, debug (and warn/error when they happen).

── Alert model: presence, not rate-spike ───────────────────────────────────
At this volume the error baseline is ZERO — errors essentially never appear. So
"did the rate spike above normal?" is the wrong question; "did ANY error/warn
appear?" is both simpler and strictly more sensitive. We alert on error/warn
rows NOT seen on a previous scan (fingerprint dedup, same noise discipline as
monitor_health diffing the errored-game set):
  - First run with no prior state → BASELINE the current error/warn rows, emit
    one digest summary, no urgent ping (don't alarm on a pre-existing pile).
  - Later runs → any error-level row that's new is urgent; any new warn is
    digest. Old rows already fingerprinted are never re-pinged.

Credentials (in the launchd plist, mirrored to os.environ by env_loader):
  BETTERSTACK_CH_HOST, BETTERSTACK_CH_USER, BETTERSTACK_CH_PASS.
Fails clean (ok: false) if unset — same failure contract as monitor_keys/health.

CLI:
    python handlers/monitor_betterstack.py report   → scan + persist, JSON
    python handlers/monitor_betterstack.py show      → last scan, human-readable
    python handlers/monitor_betterstack.py digest    → digest block for notify
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

from driver.budget_state import STATE_DIR  # noqa: E402

# The durable store for this source. Hot tier is remote(t507167_ai_werewolf_2_logs);
# we query S3 (see module docstring). Override via env if the source/cluster moves.
TABLE = os.environ.get("BETTERSTACK_CH_TABLE", "s3Cluster(primary, t507167_ai_werewolf_2_s3)")
WINDOW_MIN = int(os.environ.get("BETTERSTACK_WINDOW_MIN", "90"))
ALERT_LEVELS = ("error", "warn")
HTTP_TIMEOUT = 30
ROW_LIMIT = 500          # plenty at this volume; caps a runaway error storm
SEEN_CAP = 2000          # fingerprints retained for dedup (errors are rare → never hit)

BS_LATEST = STATE_DIR / "betterstack_latest.json"
BS_HISTORY = STATE_DIR / "betterstack_history.jsonl"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _creds() -> dict | None:
    host = os.environ.get("BETTERSTACK_CH_HOST")
    user = os.environ.get("BETTERSTACK_CH_USER")
    pw = os.environ.get("BETTERSTACK_CH_PASS")
    if not (host and user and pw):
        return None
    return {"host": host, "user": user, "pw": pw}


def _query(creds: dict, sql: str) -> str:
    """POST a SQL statement to the ClickHouse HTTP endpoint, return raw text body.
    Raises requests.RequestException / RuntimeError on transport or query error."""
    resp = requests.post(
        f"{creds['host']}?output_format_pretty_row_numbers=0",
        auth=(creds["user"], creds["pw"]),
        headers={"Content-type": "plain/text"},
        data=sql,
        timeout=HTTP_TIMEOUT,
    )
    if resp.status_code != 200:
        # Betterstack returns a ClickHouse exception JSON or an auth error body.
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200].strip()}")
    return resp.text


def _fetch_rows(creds: dict) -> list[dict]:
    """The error/warn rows in the window, newest first. Each: {dt, level, msg}."""
    levels = ", ".join(f"'{l}'" for l in ALERT_LEVELS)
    sql = (
        "SELECT dt, JSONExtractString(raw,'level') AS lvl, "
        "substring(JSONExtractString(raw,'message'),1,200) AS msg "
        f"FROM {TABLE} "
        f"WHERE dt > now() - INTERVAL {WINDOW_MIN} MINUTE "
        f"AND JSONExtractString(raw,'level') IN ({levels}) "
        f"ORDER BY dt DESC LIMIT {ROW_LIMIT} FORMAT JSONEachRow"
    )
    body = _query(creds, sql)
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        rows.append({"dt": o.get("dt"), "level": o.get("lvl"), "msg": (o.get("msg") or "").strip()})
    return rows


def _fingerprint(row: dict) -> str:
    key = f"{row.get('dt')}|{row.get('level')}|{row.get('msg')}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]


def _prior_seen() -> list[str] | None:
    """Fingerprints from the last run. None → never scanned (→ baseline)."""
    try:
        with BS_LATEST.open() as f:
            prev = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    return list(prev.get("seen", []))


def _derive_issues(rows: list[dict], prior: list[str] | None) -> tuple[list[dict], bool]:
    """Issues for error/warn rows new since last scan. Returns (issues, baselined).

    First run (prior is None) sets a baseline: one digest line, no urgent — we
    don't alarm on the pre-existing pile we just discovered."""
    if prior is None:
        if rows:
            errs = sum(1 for r in rows if r["level"] == "error")
            return ([{
                "severity": "digest",
                "kind": "betterstack_baseline",
                "target": "logs",
                "detail": f"baseline: {len(rows)} error/warn log line(s) in the last "
                          f"{WINDOW_MIN}m on first scan ({errs} error, {len(rows)-errs} warn) "
                          f"— not alerting (pre-existing). New lines alert from here.",
            }], True)
        return ([], True)

    seen = set(prior)
    issues = []
    for r in rows:
        if _fingerprint(r) in seen:
            continue  # already known — don't re-ping
        is_err = r["level"] == "error"
        issues.append({
            "severity": "urgent" if is_err else "digest",
            "kind": "app_error" if is_err else "app_warn",
            "target": r["dt"] or "?",
            "detail": f"[{r['level']}] {r['msg'][:140] or '(no message)'}",
        })
    return (issues, False)


def _next_seen(rows: list[dict], prior: list[str] | None) -> list[str]:
    """Updated fingerprint list: current window's fps first, then prior, capped."""
    cur = [_fingerprint(r) for r in rows]
    merged, out = set(), []
    for fp in cur + (prior or []):
        if fp not in merged:
            merged.add(fp)
            out.append(fp)
        if len(out) >= SEEN_CAP:
            break
    return out


def _compact(report: dict) -> dict:
    return {
        "checked_at": report.get("checked_at"),
        "window_min": report.get("window_min"),
        "counts": report.get("counts"),
        "new_issues": len([i for i in report.get("issues", [])
                           if i["kind"] in ("app_error", "app_warn")]),
        "any_urgent": report.get("any_urgent"),
        "issues": [f"{i['severity']}:{i['target']}" for i in report.get("issues", [])],
    }


def _save(report: dict) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = BS_LATEST.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(BS_LATEST)
        with BS_HISTORY.open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


def report() -> dict:
    now = _now_utc()
    creds = _creds()
    if not creds:
        return {"ok": False, "checked_at": _checked_at(now),
                "error": "BETTERSTACK_CH_HOST/USER/PASS not set (ClickHouse query creds)"}
    try:
        rows = _fetch_rows(creds)
    except (requests.RequestException, RuntimeError) as e:
        return {"ok": False, "checked_at": _checked_at(now), "error": str(e)[:200]}

    prior = _prior_seen()                       # read BEFORE we overwrite latest
    issues, baselined = _derive_issues(rows, prior)
    counts = {lvl: sum(1 for r in rows if r["level"] == lvl) for lvl in ALERT_LEVELS}
    result = {
        "ok": True,
        "checked_at": _checked_at(now),
        "window_min": WINDOW_MIN,
        "counts": counts,
        "rows": rows[:50],                      # a sample for `show`; not the dedup state
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
        "baselined": baselined,
        "seen": _next_seen(rows, prior),        # dedup state for the next run
    }
    _save(result)
    return result


# ─── Renders ─────────────────────────────────────────────────────────────────


def render(report: dict) -> str:
    if not report.get("ok"):
        return f"monitor_betterstack failed: {report.get('error', 'unknown')}"
    c = report.get("counts", {})
    out = [f"Werewolf app logs (Betterstack) — {report['checked_at']}",
           f"  window: last {report.get('window_min')}m   "
           f"error={c.get('error', 0)} warn={c.get('warn', 0)}", ""]
    rows = report.get("rows", [])
    if rows:
        out.append("  Recent error/warn lines:")
        for r in rows[:10]:
            out.append(f"    · {r['dt']}  [{r['level']}] {r['msg'][:120]}")
        if len(rows) > 10:
            out.append(f"    … +{len(rows) - 10} more")
    else:
        out.append("  No error/warn lines in the window.")
    issues = report.get("issues", [])
    out.append("")
    if issues:
        out.append("  Issues this scan:")
        for i in issues:
            mark = "🔴" if i["severity"] == "urgent" else "⚠️"
            out.append(f"    {mark} [{i['severity']}] {i['detail']}")
    else:
        out.append("  No new error/warn lines since last scan.")
    return "\n".join(out)


def render_digest(report: dict) -> str | None:
    """Digest block — only when there's something new. Returns None on a quiet
    scan so it adds no line to the daily digest."""
    if not report.get("ok"):
        return f"Werewolf app logs: scan failed ({report.get('error', 'unknown')})."
    issues = report.get("issues", [])
    if not issues:
        return None
    date = (report.get("checked_at") or "")[:10]
    head = f"Werewolf app logs — {date}: {len(issues)} new" \
           + (" (urgent)" if report.get("any_urgent") else "")
    lines = [head] + [f"  · {i['detail']}" for i in issues]
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Scan Betterstack for new error/warn lines + persist (JSON)")
    sub.add_parser("show", help="Render the last persisted scan, human-readable")
    sub.add_parser("digest", help="Digest block from the last scan (empty if nothing new)")
    args = ap.parse_args()
    if args.cmd == "report":
        res = report()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    elif args.cmd == "show":
        try:
            with BS_LATEST.open() as f:
                print(render(json.load(f)))
        except (OSError, json.JSONDecodeError):
            print("No scan yet — run `report` first.")
    elif args.cmd == "digest":
        try:
            with BS_LATEST.open() as f:
                d = render_digest(json.load(f))
            print(d if d else "")
        except (OSError, json.JSONDecodeError):
            print("")


if __name__ == "__main__":
    main()
