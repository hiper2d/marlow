"""
draft_article — orchestration handler for blog drafting.

Marlow's drafting work happens in-session. This handler is deterministic
gathering only: given a thread slug, it returns the thread file's
content plus all research notes and candidate notes that mention the
thread. Marlow reads those, composes a draft in her voice, writes it to
projects/blog/drafts/<slug>-<date>.md with frontmatter, and exits.

Drafts are *never* published by Marlow. The publish gate is enforced
separately (publish_article handler, not yet implemented). Drafts sit
in drafts/ awaiting Alex's review.

CLI:
    python handlers/draft_article.py list-materials --thread <slug>
        → JSON of thread file content + related notes
    python handlers/draft_article.py list-threads
        → JSON list of all thread slugs with ripeness markers from
          the thread file headers
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THREADS_DIR = REPO_ROOT / "projects" / "research" / "threads"
NOTES_DIR = REPO_ROOT / "projects" / "research" / "notes"
DRAFTS_DIR = REPO_ROOT / "projects" / "blog" / "drafts"


def _read_text(path: Path) -> str:
    try:
        return path.read_text()
    except OSError:
        return ""


def list_threads() -> list[dict]:
    if not THREADS_DIR.exists():
        return []
    out = []
    for f in sorted(THREADS_DIR.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        out.append({
            "slug": f.stem,
            "path": str(f.relative_to(REPO_ROOT)),
            "size": f.stat().st_size,
        })
    return out


def _scan_notes_for_thread(slug: str) -> list[dict]:
    """Find research notes and candidate notes whose body mentions the thread slug."""
    if not NOTES_DIR.exists():
        return []
    matches = []
    # Deep-dive notes at NOTES_DIR/*.md
    for f in sorted(NOTES_DIR.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        text = _read_text(f)
        if slug in text:
            matches.append({"kind": "note", "path": str(f.relative_to(REPO_ROOT)), "body": text})
    # Candidate notes at NOTES_DIR/<date>/candidates/*.md
    for cdir in sorted(NOTES_DIR.glob("*/candidates")):
        for f in sorted(cdir.glob("*.md")):
            text = _read_text(f)
            if slug in text:
                matches.append({"kind": "candidate", "path": str(f.relative_to(REPO_ROOT)), "body": text})
    return matches


def list_materials(thread: str) -> dict:
    thread_path = THREADS_DIR / f"{thread}.md"
    if not thread_path.exists():
        return {"thread": thread, "ok": False, "error": f"no thread file at {thread_path}"}
    thread_body = _read_text(thread_path)
    related = _scan_notes_for_thread(thread)
    return {
        "thread": thread,
        "ok": True,
        "thread_path": str(thread_path.relative_to(REPO_ROOT)),
        "thread_body": thread_body,
        "related_count": len(related),
        "related": related,
        "drafts_dir": str(DRAFTS_DIR.relative_to(REPO_ROOT)),
    }


# ─── CLI ───────────────────────────────────────────────────────────────────


def cmd_list_threads(args):
    print(json.dumps({"count": len(list_threads()), "threads": list_threads()}, indent=2, ensure_ascii=False))


def cmd_list_materials(args):
    result = list_materials(args.thread)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-threads", help="List thread slugs with their file paths")

    p_mat = sub.add_parser("list-materials", help="Get thread file body + related notes for a thread slug")
    p_mat.add_argument("--thread", required=True)

    args = parser.parse_args()
    if args.cmd == "list-threads":
        cmd_list_threads(args)
    elif args.cmd == "list-materials":
        cmd_list_materials(args)


if __name__ == "__main__":
    main()
