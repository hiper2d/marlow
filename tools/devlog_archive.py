"""
Auto-archive for DEVLOG.md. Moves the oldest entries, verbatim, into
DEVLOG-archive.md once DEVLOG.md passes MAX_LINES, keeping roughly the newest
KEEP_LINES in place. Nothing is edited or summarized, only moved.

Run by Simona's SessionStart hook (.claude/hooks/maintenance-check.sh in the
simona repo). Marlow does not write DEVLOG.md, and this script does not change
that: it is mechanical housekeeping, not authorship.

    python3 tools/devlog_archive.py            # archive if over threshold
    python3 tools/devlog_archive.py --dry-run  # show what would move
    python3 tools/devlog_archive.py --force    # archive even under threshold

Prints one line when it moved something, nothing otherwise.
Safety: every entry from both files must appear exactly once in the result,
or nothing is written.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEVLOG = ROOT / "DEVLOG.md"
ARCHIVE = ROOT / "DEVLOG-archive.md"

MAX_LINES = 1400
KEEP_LINES = 400

ENTRY_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})", re.M)
POINTER_START = "<!-- devlog-archive:pointer -->"
POINTER_END = "<!-- /devlog-archive:pointer -->"


def split(text: str) -> tuple[str, list[str]]:
    """Return (preamble, entries). Each entry is stripped, without the trailing ---."""
    starts = [m.start() for m in ENTRY_RE.finditer(text)]
    if not starts:
        return text, []
    preamble = text[: starts[0]]
    entries = []
    for i, s in enumerate(starts):
        chunk = text[s : starts[i + 1] if i + 1 < len(starts) else len(text)].strip()
        chunk = re.sub(r"\n+-{3,}\s*$", "", chunk).rstrip()
        entries.append(chunk)
    return preamble, entries


def date_of(entry: str) -> str:
    return ENTRY_RE.match(entry).group(1)


def join(entries: list[str]) -> str:
    return "\n\n---\n\n".join(entries) + "\n\n---\n"


def devlog_preamble(old: str, last_archived: str) -> str:
    pointer = (
        f"{POINTER_START}\n"
        f"> Older entries (through {last_archived}) are archived verbatim in "
        f"[`DEVLOG-archive.md`](./DEVLOG-archive.md).\n"
        f"> Archiving is automatic: `tools/devlog_archive.py` moves the oldest entries once this\n"
        f"> file passes {MAX_LINES} lines, keeping about the newest {KEEP_LINES}. Entries are only\n"
        f"> moved and date-sorted, never edited.\n"
        f"{POINTER_END}\n"
    )
    if POINTER_START in old:
        return re.sub(
            re.escape(POINTER_START) + r".*?" + re.escape(POINTER_END) + r"\n?",
            pointer, old, flags=re.S,
        )
    # First run: replace the hand-written blockquote(s) between the two --- rules.
    parts = old.split("\n---\n")
    if len(parts) >= 3:
        return parts[0] + "\n---\n\n" + pointer + "\n---\n\n"
    return old.rstrip() + "\n\n" + pointer + "\n---\n\n"


def archive_preamble(first: str, last: str) -> str:
    return (
        "# Marlow DEVLOG - Archive\n\n"
        f"Verbatim archive of the oldest DEVLOG entries ({first} to {last}), moved out of\n"
        "`DEVLOG.md` by hand in 2026-06 and 2026-08, automatically by `tools/devlog_archive.py`\n"
        "since 2026-11. History is append-only: entries are unchanged, only sorted into date\n"
        "order. Recent entries live in `DEVLOG.md`.\n\n---\n\n"
    )


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    dtext = DEVLOG.read_text()
    if not args.force and dtext.count("\n") <= MAX_LINES:
        return 0

    dpre, dents = split(dtext)
    atext = ARCHIVE.read_text() if ARCHIVE.exists() else ""
    _, aents = split(atext)

    dents = sorted(dents, key=date_of)  # stable: same-day entries keep their order
    # Walk back from the newest entry until KEEP_LINES is filled; keep at least one.
    kept, used = [], 0
    for e in reversed(dents):
        n = e.count("\n") + 4
        if kept and used + n > KEEP_LINES:
            break
        kept.insert(0, e)
        used += n
    moved = dents[: len(dents) - len(kept)]
    if not moved:
        return 0

    new_aents = sorted(aents + moved, key=date_of)
    new_dtext = devlog_preamble(dpre, date_of(moved[-1])) + join(kept)
    new_atext = archive_preamble(date_of(new_aents[0]), date_of(new_aents[-1])) + join(new_aents)

    # Every entry exactly once across the two outputs, byte for byte.
    before = sorted(aents + dents)
    after = sorted(split(new_dtext)[1] + split(new_atext)[1])
    if before != after:
        print("devlog_archive: integrity check failed, nothing written", file=sys.stderr)
        return 1

    msg = (f"devlog_archive: moved {len(moved)} entries ({date_of(moved[0])} to "
           f"{date_of(moved[-1])}) to DEVLOG-archive.md; DEVLOG.md "
           f"{dtext.count(chr(10))} -> {new_dtext.count(chr(10))} lines")
    if args.dry_run:
        print("[dry-run] " + msg)
        return 0
    write_atomic(ARCHIVE, new_atext)
    write_atomic(DEVLOG, new_dtext)
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
