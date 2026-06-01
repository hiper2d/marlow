"""
calorie_digest — nightly roll-up of a local day's food log.

Two steps, split so Marlow writes the human comment in its own voice:

  1. `summary` returns the day's totals + every estimated entry as JSON.
     Marlow reads it and composes a short, honest digest message (totals
     as a range, macros, meal-timing observations, one useful comment —
     not cheerleading).
  2. `send --text "<message>"` delivers that message to the fitness chat
     and records the digest in the DB (marked sent).

If the day has unestimated `pending` entries, `summary` flags them so
Marlow estimates them first (via calorie_db) before sending — otherwise
the totals undercount.

CLI:
    uv run python handlers/calorie_digest.py summary [--date YYYY-MM-DD]
    uv run python handlers/calorie_digest.py send --text "..." [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from driver.env_loader import import_plist_env  # noqa: E402

import_plist_env()

from tools import calorie_db, fitness_bot  # noqa: E402


def due() -> dict:
    """Dates with food logged but no digest sent yet (today + any missed)."""
    calorie_db.init_db()
    return {"dates": calorie_db.undelivered_digests()}


def summary(date: str | None) -> dict:
    calorie_db.init_db()
    day = calorie_db.get_day(date)
    t = day["totals"]
    day["has_pending"] = t["pending_count"] > 0
    day["empty"] = t["estimated_count"] == 0 and t["pending_count"] == 0
    return day


def send(*, date: str | None, text: str) -> dict:
    resp = fitness_bot.send_message(text)
    saved = calorie_db.save_digest(
        date=date or calorie_db._today_local(), comment=text, sent=True
    )
    return {"ok": resp.get("ok", False), "saved": saved}


def main() -> int:
    p = argparse.ArgumentParser(description="Nightly calorie digest.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("due", help="Dates with food logged but no digest sent yet.")

    ps = sub.add_parser("summary", help="Day totals + entries for Marlow to comment on.")
    ps.add_argument("--date", default=None)

    pd = sub.add_parser("send", help="Send the composed digest and record it.")
    pd.add_argument("--text", required=True)
    pd.add_argument("--date", default=None)

    args = p.parse_args()
    if args.cmd == "due":
        print(json.dumps(due(), indent=2, ensure_ascii=False))
    elif args.cmd == "summary":
        print(json.dumps(summary(args.date), indent=2, ensure_ascii=False))
    elif args.cmd == "send":
        print(json.dumps(send(date=args.date, text=args.text), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
