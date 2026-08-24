"""
_memory_compact - shared bounding primitives for Marlow's memory files.

Not a tick handler. A library imported by `grade_memory`, `self_reflect` and
`self_review` so every memory file is bounded by the same two mechanisms
instead of four hand-rolled ones.

Two mechanisms, deliberately different:

1. **FIFO truncation** (`truncate_fifo`) - deterministic, code-enforced, no
   model in the loop. Used for `working.md`'s daily-rollup region: oldest
   dated sections are dropped whole once the region exceeds its cap, and
   their dates are folded into a trailing `### Earlier` line. This is for
   the file that is prepended to EVERY tick of BOTH loops, where "the model
   was asked nicely to compress and didn't" is not an acceptable failure
   mode. It was 149KB against a documented 10KB cap for months.

2. **Protected-tail analysis** (`analyze`) - for files Marlow compacts with
   judgment (the journals, the lessons file). The handler splits the file
   and hands the session a pre-split view so the recent entries are
   structurally out of reach rather than merely off-limits by instruction.
   The session distills `compactable` into the standing section and never
   touches `protected`.

Why a protected tail at all: the newest entries are the ones the next tick
actually reads for steering. Distilling them is the one edit that destroys
the file's purpose, so the code makes it hard rather than the prompt asking
for it.

Why `standing` has its OWN, much higher threshold: re-paraphrasing an
already-distilled section on every pass is a ratchet - six months of
compressing the compression and the voice journal reads like it was written
by nobody, which for a file whose entire purpose is developing a voice is
the worst available outcome. Standing sections are re-synthesized rarely and
deliberately, not weekly.

File shape assumed by `analyze` (both journals already match it):

    # Title
    ... preamble / form notes ...
    ## <standing_heading>          <- distilled, long-lived
    ...
    ## Entries                     <- newest first
    ### 2026-08-22
    ...
    ### 2026-08-20
    ...
"""

from __future__ import annotations

import re
from pathlib import Path

# --- knobs -------------------------------------------------------------------
# Entries newer than this many are never offered for compaction.
DEFAULT_PROTECT = 3
# Compaction is flagged on the size of the COMPACTABLE region only, never the
# whole file. Measuring the whole file wakes her up to compact when the only
# thing over the line is the protected tail she isn't allowed to touch.
DEFAULT_COMPACT_THRESHOLD = 8_000
# The distilled section gets a far looser bound - see the ratchet note above.
DEFAULT_STANDING_THRESHOLD = 20_000

ENTRIES_HEADING = "## Entries"
_ENTRY_RE = re.compile(r"^### ", re.MULTILINE)
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
# The Earlier line is re-parsed on every pass, so its own day COUNT has to
# survive the round trip. Rendering "first .. last (N days)" and then counting
# dates on re-read finds only the two boundary dates, silently resetting N to 2
# and losing the record of how much history has aged out.
_SPAN_RE = re.compile(r"(\d{4}-\d{2}-\d{2})\s*\.\.\s*(\d{4}-\d{2}-\d{2})\s*\((\d+) days\)")


def read(path: Path) -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""


def _nbytes(s: str) -> int:
    return len(s.encode())


def split_sections(text: str, heading: str) -> tuple[str, str]:
    """Split `text` at a `## ` heading. Returns (before, from-heading-onward).

    The heading line itself stays with the second half so callers can
    reassemble by plain concatenation.
    """
    idx = text.find(heading)
    if idx == -1:
        return text, ""
    return text[:idx], text[idx:]


def split_entries(entries_block: str) -> tuple[str, list[str]]:
    """Split a `## Entries` block into (heading_line, [entry, entry, ...]).

    Entries are returned in file order, which in both journals is
    newest-first - so `entries[:protect]` is the recent tail to protect.
    Each entry string retains its own `### ` heading and trailing newlines,
    so `heading + "".join(entries)` round-trips exactly.
    """
    if not entries_block:
        return "", []
    parts = _ENTRY_RE.split(entries_block)
    head = parts[0]
    entries = ["### " + p for p in parts[1:]]
    return head, entries


def entry_title(entry: str) -> str:
    return entry.splitlines()[0].lstrip("# ").strip() if entry.strip() else ""


def analyze(
    path: Path,
    *,
    standing_heading: str,
    protect: int = DEFAULT_PROTECT,
    threshold: int = DEFAULT_COMPACT_THRESHOLD,
    standing_threshold: int = DEFAULT_STANDING_THRESHOLD,
) -> dict:
    """Pre-split a judgment-compacted memory file for a tick session.

    The returned dict is what the session works from. `protected` is
    verbatim and off-limits; `compactable` is the only region the session
    rewrites, folding it into the standing section.
    """
    body = read(path)
    preamble, rest = split_sections(body, standing_heading)
    standing_block, entries_block = split_sections(rest, ENTRIES_HEADING)
    entries_head, entries = split_entries(entries_block)

    protected = entries[:protect]
    compactable = entries[protect:]
    compactable_text = "".join(compactable)
    standing_bytes = _nbytes(standing_block)

    return {
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": _nbytes(body),
        # Regions, so the session never has to parse the file itself.
        "preamble": preamble,
        "standing_heading": standing_heading,
        "standing": standing_block,
        "standing_bytes": standing_bytes,
        "entries_heading": entries_head,
        "protected": protected,
        "protected_titles": [entry_title(e) for e in protected],
        "protected_count": len(protected),
        "compactable": compactable,
        "compactable_titles": [entry_title(e) for e in compactable],
        "compactable_count": len(compactable),
        "compactable_bytes": _nbytes(compactable_text),
        # Flags.
        "needs_compaction": _nbytes(compactable_text) > threshold,
        "needs_standing_resynthesis": standing_bytes > standing_threshold,
        "thresholds": {
            "protect": protect,
            "compact_bytes": threshold,
            "standing_bytes": standing_threshold,
        },
    }


def _parse_earlier(block: str) -> tuple[str | None, str | None, int]:
    """Recover (first_date, last_date, count) from an existing Earlier line."""
    if not block:
        return None, None, 0
    m = _SPAN_RE.search(block)
    if m:
        return m.group(1), m.group(2), int(m.group(3))
    dates = sorted(set(_DATE_RE.findall(block)))
    if not dates:
        return None, None, 0
    return dates[0], dates[-1], len(dates)


def _earlier_line(heading: str, first: str | None, last: str | None, count: int) -> str:
    """The bounded bookkeeping line. A span, a count, a pointer. Never prose."""
    if not first or count <= 0:
        return ""
    span = f"{first} .. {last} ({count} days)" if count > 1 else first
    return (
        f"{heading}\n\n"
        f"- Rollups dropped from the FIFO window: {span}. "
        f"Recoverable from the repo history; anything durable should already be "
        f"in `memory/lessons.md`.\n"
    )


def truncate_fifo(
    text: str,
    *,
    region_heading: str,
    cap_bytes: int,
    earlier_heading: str = "### Earlier",
) -> tuple[str, dict]:
    """Bound a dated-section region as a fixed-size FIFO queue.

    Everything before `region_heading` is exempt and never touched - in
    `working.md` that is `## Current state`, whose facts expire when they
    stop being true, not on a schedule. FIFO'ing them would drop a true
    fact for being old.

    Within the region, dated `### ` sections run newest-first, so the queue
    drains from the END. Dropped sections are folded into a trailing
    `### Earlier` line, which is never dropped: it is the record that history
    existed. That line is DATES ONLY, deliberately - the first version of this
    accumulated dropped prose and reached 7.4KB, which, being exempt from the
    queue, starved the cap down to a single day of retained history. A
    bookkeeping line that grows is not bookkeeping. Anything durable in a rollup
    must be promoted to `lessons.md` before its day falls out of the window; the
    Earlier line only records that the day existed. Returns (new_text, report).
    """
    head, region = split_sections(text, region_heading)
    if not region:
        return text, {"ok": False, "reason": f"no '{region_heading}' region", "dropped": []}

    region_head, sections = split_entries(region)

    # The Earlier line is bookkeeping, not a queue slot. Pull it aside so it
    # can't be dropped and can be rewritten with whatever we drop this pass.
    earlier_idx = next(
        (i for i, s in enumerate(sections) if s.startswith(earlier_heading)), None
    )
    earlier = sections.pop(earlier_idx) if earlier_idx is not None else ""
    # Dates only - never carry prior prose forward (see the docstring).
    prior_first, prior_last, prior_count = _parse_earlier(earlier)
    # Collapse it to its bounded form BEFORE measuring. Measuring the stale
    # block instead makes the queue over-drop: a 7.4KB Earlier that is about to
    # become a 200-byte line otherwise counts against the cap on every
    # iteration and evicts days that would have fit.
    if earlier:
        earlier = _earlier_line(earlier_heading, prior_first, prior_last, prior_count)

    def region_bytes(secs: list[str]) -> int:
        return _nbytes(region_head + "".join(secs) + earlier)

    dropped: list[str] = []
    # Drain oldest-first (end of list) until the region fits. Always keep at
    # least one dated section, so a single oversized entry can't empty the
    # queue - it surfaces as an oversized-entry flag instead.
    while len(sections) > 1 and region_bytes(sections) > cap_bytes:
        dropped.append(entry_title(sections.pop()))

    if dropped:
        dropped_dates = sorted({d for title in dropped for d in _DATE_RE.findall(title)[:1]})
        bounds = [x for x in (prior_first, prior_last, *dropped_dates) if x]
        earlier = _earlier_line(
            earlier_heading,
            min(bounds), max(bounds),
            prior_count + len(dropped_dates),
        )

    new_region = region_head + "".join(sections) + earlier
    new_text = head + new_region

    return new_text, {
        "ok": True,
        "dropped": dropped,
        "kept": len(sections),
        "region_bytes_before": _nbytes(region),
        "region_bytes_after": _nbytes(new_region),
        "cap_bytes": cap_bytes,
    }


def oversized_sections(text: str, *, region_heading: str, max_bytes: int) -> list[dict]:
    """Dated sections in a region that blow the per-entry budget.

    The FIFO caps the file; this catches the reason a capped file holds only
    two days of history instead of eight. Surfaced to monitor_self rather
    than auto-trimmed - cutting prose mid-sentence to hit a byte count makes
    the record worse, so the pressure is visible instead of silent.
    """
    _, region = split_sections(text, region_heading)
    if not region:
        return []
    _, sections = split_entries(region)
    return [
        {"title": entry_title(s), "bytes": _nbytes(s)}
        for s in sections
        if _nbytes(s) > max_bytes
    ]
