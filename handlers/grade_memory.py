"""
grade_memory — daily memory grader.

Orchestration handler for the daily memory grading tick. The handler
itself is deterministic — it lists tick logs in memory/recent/ within
a time window, returns them as JSON, and on request prunes anything
older than a cutoff. The editorial compression (reading the day's
ticks, writing a one-paragraph rollup to working.md) happens inside
Marlow's session.

The default retention is 3 days: anything older than that has either
been compressed into working.md by yesterday's grader, or is stale.

CLI:
    python handlers/grade_memory.py list-recent [--since YYYY-MM-DD]
        → JSON of tick log entries newer than `since` (default: 1 day ago)
    python handlers/grade_memory.py prune-recent [--keep-days N]
        → delete recent/ files older than now() - keep_days; default keep=3
        → prints {"deleted": [...], "kept": N}
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RECENT_DIR = REPO_ROOT / "memory" / "recent"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _file_mtime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def list_recent(since: datetime) -> list[dict]:
    """Return all recent/ tick logs with mtime >= since."""
    if not RECENT_DIR.exists():
        return []
    out = []
    for f in sorted(RECENT_DIR.glob("*.md")):
        try:
            mtime = _file_mtime(f)
            if mtime < since:
                continue
            text = f.read_text()
        except OSError:
            continue
        out.append({
            "name": f.name,
            "mtime": mtime.isoformat(),
            "size": len(text),
            "body": text,
        })
    return out


def prune_recent(keep_days: int) -> dict:
    """Delete recent/ files older than now() - keep_days."""
    if not RECENT_DIR.exists():
        return {"deleted": [], "kept": 0}
    cutoff = _now() - timedelta(days=keep_days)
    deleted, kept = [], 0
    for f in RECENT_DIR.glob("*.md"):
        try:
            mtime = _file_mtime(f)
        except OSError:
            continue
        if mtime < cutoff:
            try:
                f.unlink()
                deleted.append(f.name)
            except OSError as e:
                deleted.append(f"{f.name} (error: {e})")
        else:
            kept += 1
    return {"deleted": sorted(deleted), "kept": kept, "cutoff": cutoff.isoformat()}


# ─── CLI ───────────────────────────────────────────────────────────────────


def cmd_list(args):
    if args.since:
        since = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
    else:
        since = _now() - timedelta(days=1)
    items = list_recent(since)
    print(json.dumps({"since": since.isoformat(), "count": len(items), "items": items}, indent=2, ensure_ascii=False))


def cmd_prune(args):
    result = prune_recent(args.keep_days)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list-recent", help="List recent/ tick logs newer than --since")
    p_list.add_argument("--since", help="YYYY-MM-DD (UTC); defaults to 1 day ago")

    p_prune = sub.add_parser("prune-recent", help="Delete recent/ files older than --keep-days")
    p_prune.add_argument("--keep-days", type=int, default=3)

    args = parser.parse_args()
    if args.cmd == "list-recent":
        cmd_list(args)
    elif args.cmd == "prune-recent":
        cmd_prune(args)


if __name__ == "__main__":
    main()
