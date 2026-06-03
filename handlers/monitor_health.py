"""
monitor_health — broken-game watch for the Werewolf game (anomaly scanning).

The third werewolf-ops workstream. monitor_keys watches what the free tier
COSTS, werewolf_stats watches what it PRODUCES; this watches whether games are
actually WORKING. Same Firestore, same read-only service account — no new creds.

Signal: the game persists a `errorState` object on a game doc when a system
error hits it (`setGameErrorState` in the game's game-actions.ts). Shape:
    {recoverable: bool,
     context: {gameId, timestamp: ISO8601, function},
     details: "Error: ...\n  <stack>"}
So a broken game is readable straight from the `games` collection — no log
pipeline needed. (App-level exceptions that never reach a game doc — provider
5xx, dead requests — are Betterstack's job; deferred, see werewolf-ops README.)

Noise control — the crux: at any moment a pile of old errored games sits in the
30-day TTL window (abandoned mid-bug weeks ago). Re-alerting on those every scan
is noise. So we alert on games that became errored SINCE THE LAST SCAN, not the
standing set — exactly how monitor_keys avoids re-pinging an unchanged balance.
  - First run with no prior state → BASELINE the current errored set, emit a
    single digest summary, no urgent ping.
  - Later runs → diff against the prior set. A newly-errored game is urgent if
    `recoverable: false` (engine gave up — game is dead), digest if recoverable
    (may self-heal on retry). A game that clears its error drops from the set;
    if it re-errors later it counts as new again.

Credentials: MARLOW_FIREBASE_CREDS (read-only service account) — same wiring as
monitor_keys/werewolf_stats. Fails clean (`ok: false`) if unset.

CLI:
    python handlers/monitor_health.py report   → scan + persist, JSON + issues
    python handlers/monitor_health.py show      → last snapshot, human-readable
    python handlers/monitor_health.py digest    → digest block for notify
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

from handlers.monitor_keys import _firestore_db  # noqa: E402
from driver.budget_state import STATE_DIR  # noqa: E402

GAMES = "games"

HEALTH_LATEST = STATE_DIR / "health_latest.json"
HEALTH_HISTORY = STATE_DIR / "health_history.jsonl"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _age_hours(iso: str | None, now: datetime) -> float | None:
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return round((now - dt).total_seconds() / 3600, 1)


def _summarize(err: dict, game_id: str, theme, owner, state, now: datetime) -> dict:
    """Flatten a game's errorState into a compact, reportable row."""
    ctx = err.get("context") or {}
    details = (err.get("details") or "")
    first_line = details.splitlines()[0].strip() if details else "(no details)"
    return {
        "id": game_id,
        "theme": theme or "(untitled)",
        "owner": owner,
        "state": state,
        "recoverable": bool(err.get("recoverable")),
        "error_at": ctx.get("timestamp"),
        "age_hours": _age_hours(ctx.get("timestamp"), now),
        "function": ctx.get("function"),
        "summary": first_line[:160],
    }


def _scan_errored(db, now: datetime) -> list[dict]:
    rows = []
    for snap in db.collection(GAMES).stream():
        g = snap.to_dict() or {}
        err = g.get("errorState")
        if not err:
            continue
        rows.append(_summarize(err, snap.id, g.get("theme"), g.get("ownerEmail"),
                               g.get("gameState"), now))
    rows.sort(key=lambda r: (r["error_at"] or ""), reverse=True)
    return rows


def _prior_ids() -> set[str] | None:
    """Errored game ids from the last run. None → never scanned (→ baseline)."""
    try:
        with HEALTH_LATEST.open() as f:
            prev = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    return {r["id"] for r in prev.get("errored", [])}


def _derive_issues(errored: list[dict], prior: set[str] | None) -> tuple[list[dict], bool]:
    """Issues for games errored SINCE last scan. Returns (issues, baselined).

    First run (prior is None) sets a baseline: one digest summary, no urgent —
    we don't alarm on the pre-existing pile we just discovered.
    """
    if prior is None:
        if errored:
            return ([{
                "severity": "digest",
                "kind": "health_baseline",
                "target": "games",
                "detail": f"baseline: {len(errored)} game(s) carrying errors on first scan "
                          f"(not alerting — pre-existing). Newly-broken games alert from here.",
            }], True)
        return ([], True)

    issues = []
    for r in errored:
        if r["id"] in prior:
            continue  # already known — don't re-ping
        sev = "urgent" if not r["recoverable"] else "digest"
        kind = "game_broken" if not r["recoverable"] else "game_error_recoverable"
        rec = "unrecoverable" if not r["recoverable"] else "recoverable"
        issues.append({
            "severity": sev,
            "kind": kind,
            "target": r["id"],
            "detail": f"{r['theme']} ({r['owner']}) hit a {rec} error in {r['state']}: "
                      f"{r['summary']}",
        })
    return (issues, False)


def _compact(report: dict) -> dict:
    return {
        "checked_at": report.get("checked_at"),
        "errored_total": len(report.get("errored", [])),
        "new_errors": sum(1 for i in report.get("issues", [])
                          if i["kind"] in ("game_broken", "game_error_recoverable")),
        "any_urgent": report.get("any_urgent"),
        "issues": [f"{i['severity']}:{i['target']}" for i in report.get("issues", [])],
    }


def _save(report: dict) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = HEALTH_LATEST.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(HEALTH_LATEST)
        with HEALTH_HISTORY.open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


def report() -> dict:
    now = _now_utc()
    try:
        db = _firestore_db()
    except RuntimeError as e:
        return {"ok": False, "checked_at": _checked_at(now), "error": str(e)}

    prior = _prior_ids()                 # read BEFORE we overwrite latest
    errored = _scan_errored(db, now)
    issues, baselined = _derive_issues(errored, prior)
    result = {
        "ok": True,
        "checked_at": _checked_at(now),
        "errored": errored,
        "errored_count": len(errored),
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
        "baselined": baselined,
    }
    _save(result)
    return result


# ─── Renders ─────────────────────────────────────────────────────────────────


def render(report: dict) -> str:
    if not report.get("ok"):
        return f"monitor_health failed: {report.get('error', 'unknown')}"
    out = [f"Werewolf health — {report['checked_at']}", ""]
    errored = report.get("errored", [])
    out.append(f"  {len(errored)} game(s) currently carrying an error "
               f"(of the live ≤30d set)")
    for r in errored[:10]:
        rec = "recoverable" if r["recoverable"] else "UNRECOVERABLE"
        age = f"{r['age_hours']}h ago" if r["age_hours"] is not None else "age ?"
        out.append(f"    · {r['theme']} ({r['owner']}) — {rec}, {age}, {r['state']}")
        out.append(f"        {r['summary']}")
    if len(errored) > 10:
        out.append(f"    … +{len(errored) - 10} more")
    issues = report.get("issues", [])
    out.append("")
    if issues:
        out.append("  Issues this scan:")
        for i in issues:
            mark = "🔴" if i["severity"] == "urgent" else "⚠️"
            out.append(f"    {mark} [{i['severity']}] {i['detail']}")
    else:
        out.append("  No new errors since last scan.")
    return "\n".join(out)


def render_digest(report: dict) -> str | None:
    """Digest block — only when there's something new. Returns None if nothing to
    say (no new errors), so a quiet scan adds no line to the daily digest."""
    if not report.get("ok"):
        return f"Werewolf health: scan failed ({report.get('error', 'unknown')})."
    issues = report.get("issues", [])
    if not issues:
        return None
    date = (report.get("checked_at") or "")[:10]
    head = f"Werewolf health — {date}: {len(issues)} new" \
           + (" (urgent)" if report.get("any_urgent") else "")
    lines = [head] + [f"  · {i['detail']}" for i in issues]
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Scan for errored games + persist (JSON)")
    sub.add_parser("show", help="Render the last persisted scan, human-readable")
    sub.add_parser("digest", help="Digest block from the last scan (empty if no new errors)")
    args = ap.parse_args()
    if args.cmd == "report":
        res = report()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    elif args.cmd == "show":
        try:
            with HEALTH_LATEST.open() as f:
                print(render(json.load(f)))
        except (OSError, json.JSONDecodeError):
            print("No scan yet — run `report` first.")
    elif args.cmd == "digest":
        try:
            with HEALTH_LATEST.open() as f:
                d = render_digest(json.load(f))
            print(d if d else "")
        except (OSError, json.JSONDecodeError):
            print("")


if __name__ == "__main__":
    main()
