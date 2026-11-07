"""
self_reflect - surfaces Marlow's two notebooks (personal + work) + context, and is
the one tick that condenses them.

Writer loop only, every 2 days on its own cron, regardless of publishing.
Every writer tick may append to either notebook; this tick is where she sits
down with them: a real personal entry if there is one, and the condensing
pass for both files (the only place that happens, so two ticks never
compact the same file).

The handler only gathers materials; the session edits the files directly
(see the writer IDENTITY, "Your notebooks" and "Self-reflection").

CLI:
    self_reflect.py materials     -> JSON: both notebooks + splits + context
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _memory_compact  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
MEMORY = REPO_ROOT / "memory"
PERSONAL = MEMORY / "notebook-personal.md"
WORK = MEMORY / "notebook-work.md"
RECENT_DIR = MEMORY / "recent"
LESSONS = MEMORY / "lessons.md"
WORKING = MEMORY / "working.md"
INBOX = MEMORY / "inbox-from-alex.md"
INBOX_ARCHIVE = MEMORY / "inbox-archive.md"
PUBLISHED_DIR = REPO_ROOT / "projects" / "blog" / "published"

# Fold older dated entries into a distilled "Standing reflections" section once
# the COMPACTABLE region passes this size. Measured on the older entries only,
# never the whole file - otherwise a long protected tail trips the flag and she
# gets woken to compact with nothing she's allowed to touch.
COMPACT_THRESHOLD_BYTES = 5_000
# Never offer the newest N entries for compaction. They are what the next tick
# reads for steering; distilling them is the one edit that defeats the file.
PROTECT_ENTRIES = 3
# The distilled section is re-synthesized rarely and deliberately (see the
# ratchet note in _memory_compact) - not on every pass.
STANDING_THRESHOLD_BYTES = 10_000
# Both notebooks are read by EVERY writer tick (2026-11-07), so they are bounded
# tighter than the old diary/journal were (8KB/20KB): ~10-12KB each at rest.
STANDING_HEADING = "## Standing reflections"      # notebook-personal.md
WORK_STANDING_HEADING = "## Standing notes"        # notebook-work.md


def _read(path: Path) -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""


def _title_of(md_path: Path) -> str:
    """Pull `title:` from frontmatter, else the file stem."""
    text = _read(md_path)
    if text.startswith("---"):
        for line in text.splitlines()[1:]:
            if line.strip() == "---":
                break
            if line.startswith("title:"):
                return line.split(":", 1)[1].strip().strip('"')
    return md_path.stem


def _recent_published(n: int = 6) -> list[dict]:
    if not PUBLISHED_DIR.exists():
        return []
    files = sorted(PUBLISHED_DIR.glob("*.md"), reverse=True)[:n]
    return [{"slug": f.stem, "title": _title_of(f)} for f in files]


def _latest_article() -> dict:
    if not PUBLISHED_DIR.exists():
        return {}
    files = sorted(PUBLISHED_DIR.glob("*.md"), reverse=True)
    if not files:
        return {}
    return {"slug": files[0].stem, "text": _read(files[0])}


def _recent_activity(n: int = 8) -> list[str]:
    """First non-empty line of the most recent tick logs — a light sense of what
    she's actually been doing, to reflect against rather than reflect in a vacuum."""
    if not RECENT_DIR.exists():
        return []
    out = []
    for f in sorted(RECENT_DIR.glob("*.md"), reverse=True)[:n]:
        for line in _read(f).splitlines():
            if line.strip():
                out.append(f"{f.stem}: {line.strip()[:160]}")
                break
    return out


def _split(path: Path, heading: str) -> dict:
    return _memory_compact.analyze(
        path,
        standing_heading=heading,
        protect=PROTECT_ENTRIES,
        threshold=COMPACT_THRESHOLD_BYTES,
        standing_threshold=STANDING_THRESHOLD_BYTES,
    )


def materials() -> dict:
    personal = _split(PERSONAL, STANDING_HEADING)
    work = _split(WORK, WORK_STANDING_HEADING)
    return {
        # The two notebooks. This tick is the ONLY one that condenses them.
        # Each split is pre-separated: `protected` (newest entries) is verbatim
        # and off-limits; only `compactable` is folded into the standing section.
        "notebook_personal": _read(PERSONAL),
        "notebook_personal_path": str(PERSONAL.relative_to(REPO_ROOT)),
        "personal_split": personal,
        "notebook_work": _read(WORK),
        "notebook_work_path": str(WORK.relative_to(REPO_ROOT)),
        "work_split": work,
        "needs_compaction": personal["needs_compaction"] or work["needs_compaction"],
        # Everything else she has: her state, her conversation with Alex, the
        # last piece she actually wrote.
        "inbox_from_alex": _read(INBOX),
        "inbox_archive_tail": _read(INBOX_ARCHIVE)[-6000:],
        "lessons": _read(LESSONS),
        "working": _read(WORKING),
        "latest_article": _latest_article(),
        "recent_published": _recent_published(),
        "recent_activity": _recent_activity(n=60),
    }


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("materials", help="Gather the diary + context for a reflection tick")
    args = parser.parse_args()
    if args.cmd == "materials":
        print(json.dumps(materials(), indent=2))


if __name__ == "__main__":
    main()
