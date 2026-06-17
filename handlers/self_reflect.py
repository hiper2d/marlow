"""
self_reflect — surfaces Marlow's self-reflection diary + light context.

This is the DECOUPLED self-reflection path (writer loop only). Unlike the
voice-journal — which is about the *prose* and only fires when a draft is
reviewed — this fires on its own cron (every 2 days) regardless of whether
anything published, and it's about *her*: what she wants, what she finds
interesting, where she's heading.

The handler only gathers materials; the tick session writes the entry by
editing the file directly (see the writer IDENTITY, "Self-reflection").

CLI:
    self_reflect.py materials     → JSON: diary + recent context + needs_compaction
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MEMORY = REPO_ROOT / "memory"
SELF_REFLECTION = MEMORY / "self-reflection.md"
EDITORIAL_DIRECTION = MEMORY / "editorial-direction.md"
RECENT_DIR = MEMORY / "recent"
PUBLISHED_DIR = REPO_ROOT / "projects" / "blog" / "published"

# Fold older dated entries into a distilled "Standing reflections" section once
# the file passes this size. Keeps a frequently-written diary from rotting.
COMPACT_THRESHOLD_BYTES = 8_000


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


def materials() -> dict:
    body = _read(SELF_REFLECTION)
    return {
        "self_reflection": body,
        "self_reflection_path": str(SELF_REFLECTION.relative_to(REPO_ROOT)),
        "exists": SELF_REFLECTION.exists(),
        "size_bytes": len(body.encode()),
        "needs_compaction": len(body.encode()) > COMPACT_THRESHOLD_BYTES,
        "editorial_direction": _read(EDITORIAL_DIRECTION),
        "recent_published": _recent_published(),
        "recent_activity": _recent_activity(),
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
