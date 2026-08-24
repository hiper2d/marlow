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
    python handlers/grade_memory.py bound-working [--cap N] [--check]
        → FIFO-truncate working.md's daily-rollup region to a hard byte cap
        → prints {"dropped": [...], "kept": N, "oversized": [...], "head_bytes": N}
    python handlers/grade_memory.py lessons-status
        → pre-split view of memory/lessons.md for the compaction pass

Bounding contract (added 2026-08-24, after working.md reached 149KB against a
documented 10KB cap - the cap was a line in a prompt and Opus declined to act
on it every night for two months):

  - `## Current state` / `## Outstanding requests` are EXEMPT from truncation.
    Their facts expire when they stop being true, not on a schedule; a FIFO
    would drop a true fact for being old. Bounded by a warn flag instead.
  - `## Daily rollups` is a fixed-size FIFO. Oldest dated sections drop whole
    once the region exceeds ROLLUP_CAP_BYTES; their dates fold into a trailing
    `### Earlier` line that is never dropped.
  - Per-entry size is REPORTED, not enforced. The FIFO bounds the file either
    way; entry size only decides how many days of history fit in it (at 5KB a
    rollup that is 2 days, at 1.5KB it is 8). Auto-trimming prose to hit a byte
    count makes the record worse, so the pressure is surfaced to monitor_self.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _memory_compact  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
RECENT_DIR = REPO_ROOT / "memory" / "recent"
WORKING = REPO_ROOT / "memory" / "working.md"
LESSONS = REPO_ROOT / "memory" / "lessons.md"

# Hard cap on the daily-rollup FIFO region. Sized so ~8 days of history fit at
# the instructed rollup size (one paragraph plus a short bullet list, ~1.5KB).
ROLLUP_CAP_BYTES = 12_000
ROLLUP_HEADING = "## Daily rollups"
# Per-rollup budget. Reported only - see the bounding contract above.
ROLLUP_ENTRY_MAX_BYTES = 1_500
# `## Current state` is exempt from the FIFO but not from scrutiny: past this
# it has stopped being a state summary and become a log.
HEAD_WARN_BYTES = 6_000

# lessons.md - the only genuinely long-term memory. Replaces the never-built
# weekly `memory/archive/` synthesis. Bar for an entry is high (a failure
# signature, a workaround, a "this looks broken but isn't" that will still be
# true in six months), so it stays small on its own; most days add nothing.
LESSONS_STANDING_HEADING = "## Standing lessons"
LESSONS_PROTECT = 3
LESSONS_COMPACT_THRESHOLD_BYTES = 6_000
LESSONS_STANDING_THRESHOLD_BYTES = 12_000


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


def bound_working(cap: int, check_only: bool = False) -> dict:
    """FIFO the rollup region to `cap`; report the exempt head and fat entries."""
    text = _memory_compact.read(WORKING)
    if not text:
        return {"ok": False, "reason": "no working.md"}

    head, _ = _memory_compact.split_sections(text, ROLLUP_HEADING)
    oversized = _memory_compact.oversized_sections(
        text, region_heading=ROLLUP_HEADING, max_bytes=ROLLUP_ENTRY_MAX_BYTES
    )
    new_text, report = _memory_compact.truncate_fifo(
        text, region_heading=ROLLUP_HEADING, cap_bytes=cap
    )
    report.update({
        "head_bytes": len(head.encode()),
        "head_over_warn": len(head.encode()) > HEAD_WARN_BYTES,
        "head_warn_bytes": HEAD_WARN_BYTES,
        "entry_max_bytes": ROLLUP_ENTRY_MAX_BYTES,
        "oversized": oversized,
        "size_before": len(text.encode()),
        "size_after": len(new_text.encode()),
        "applied": False,
    })
    if report.get("ok") and not check_only and new_text != text:
        WORKING.write_text(new_text)
        report["applied"] = True
    return report


def lessons_status() -> dict:
    return _memory_compact.analyze(
        LESSONS,
        standing_heading=LESSONS_STANDING_HEADING,
        protect=LESSONS_PROTECT,
        threshold=LESSONS_COMPACT_THRESHOLD_BYTES,
        standing_threshold=LESSONS_STANDING_THRESHOLD_BYTES,
    )


def cmd_bound(args):
    print(json.dumps(bound_working(args.cap, check_only=args.check), indent=2))


def cmd_lessons(args):
    print(json.dumps(lessons_status(), indent=2))


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

    p_bound = sub.add_parser("bound-working", help="FIFO-truncate working.md's rollup region")
    p_bound.add_argument("--cap", type=int, default=ROLLUP_CAP_BYTES)
    p_bound.add_argument("--check", action="store_true", help="Report only, write nothing")
    p_bound.set_defaults(func=cmd_bound)

    p_lessons = sub.add_parser("lessons-status", help="Pre-split view of memory/lessons.md")
    p_lessons.set_defaults(func=cmd_lessons)

    args = parser.parse_args()
    if args.cmd == "list-recent":
        cmd_list(args)
    elif args.cmd == "prune-recent":
        cmd_prune(args)
    elif args.cmd == "bound-working":
        cmd_bound(args)
    elif args.cmd == "lessons-status":
        cmd_lessons(args)


if __name__ == "__main__":
    main()
