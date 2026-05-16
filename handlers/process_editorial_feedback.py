"""
process_editorial_feedback — read Simona/Alex editorial feedback and internalize it.

Marlow's writing sessions start with this handler. It's a deterministic I/O
primitive: list inbox, read one file, archive one file. The actual editorial
work — classifying feedback, updating behavioral files in memory/, writing the
DEVLOG entry, deciding to apply or push back — happens in Marlow's session
around the handler output.

Inbox: memory/feedback-inbox/<name>.md  (written by Simona's marlow-review skill)
Archive: memory/feedback-archive/<name>.md  (moved here after processing)

Behavioral files (Marlow edits in-session, not via this handler):
  - memory/voice-guidelines.md
  - memory/topic-guidance.md
  - memory/structure-notes.md
  - memory/pre-publish-pauses.md

CLI:
    python handlers/process_editorial_feedback.py list
        → JSON list of inbox files with metadata
    python handlers/process_editorial_feedback.py has-pending
        → JSON {"pending": bool, "count": int}
    python handlers/process_editorial_feedback.py read --name <filename>
        → JSON {ok, name, path, body}
    python handlers/process_editorial_feedback.py archive --name <filename>
        → JSON {ok, name, archived_to}
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INBOX = REPO_ROOT / "memory" / "feedback-inbox"
ARCHIVE = REPO_ROOT / "memory" / "feedback-archive"


def _inbox_files() -> list[Path]:
    if not INBOX.exists():
        return []
    return sorted(f for f in INBOX.glob("*.md") if f.is_file())


def list_inbox() -> dict:
    files = _inbox_files()
    return {
        "count": len(files),
        "files": [
            {
                "name": f.name,
                "path": str(f.relative_to(REPO_ROOT)),
                "size": f.stat().st_size,
                "mtime": f.stat().st_mtime,
            }
            for f in files
        ],
    }


def has_pending() -> dict:
    files = _inbox_files()
    return {"pending": len(files) > 0, "count": len(files)}


def read_feedback(name: str) -> dict:
    path = INBOX / name
    if not path.exists() or not path.is_file():
        return {"ok": False, "error": f"no inbox file at {path}"}
    return {
        "ok": True,
        "name": name,
        "path": str(path.relative_to(REPO_ROOT)),
        "body": path.read_text(),
    }


def archive_feedback(name: str) -> dict:
    src = INBOX / name
    if not src.exists() or not src.is_file():
        return {"ok": False, "error": f"no inbox file at {src}"}
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    target = ARCHIVE / name
    n = 2
    while target.exists():
        target = ARCHIVE / f"{src.stem}-{n}{src.suffix}"
        n += 1
    shutil.move(str(src), str(target))
    return {
        "ok": True,
        "name": name,
        "archived_to": str(target.relative_to(REPO_ROOT)),
    }


def cmd_list(args):
    print(json.dumps(list_inbox(), indent=2, ensure_ascii=False))


def cmd_has_pending(args):
    result = has_pending()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["pending"] else 1)


def cmd_read(args):
    result = read_feedback(args.name)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_archive(args):
    result = archive_feedback(args.name)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List all inbox files with metadata")
    sub.add_parser("has-pending", help="Exit 0 if inbox has files, 1 if empty")

    p_read = sub.add_parser("read", help="Read one inbox file's body")
    p_read.add_argument("--name", required=True)

    p_archive = sub.add_parser("archive", help="Move an inbox file to feedback-archive/")
    p_archive.add_argument("--name", required=True)

    args = parser.parse_args()
    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "has-pending":
        cmd_has_pending(args)
    elif args.cmd == "read":
        cmd_read(args)
    elif args.cmd == "archive":
        cmd_archive(args)


if __name__ == "__main__":
    main()
