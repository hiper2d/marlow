"""
Marlow RSS reader — pure fetching, no opinions.

Wraps feedparser to give a uniform JSON shape across feeds. Used by
handlers/process_rss_feed.py and any other handler that needs feed data.

CLI for manual testing:
    python tools/rss_reader.py <feed_url>
    python tools/rss_reader.py <feed_url> --limit 5
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

import feedparser


def _entry_published(entry) -> str | None:
    """Best-effort ISO8601 timestamp for an entry."""
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc).isoformat()
            except (TypeError, ValueError):
                continue
    return None


def fetch(url: str, limit: int | None = None) -> list[dict]:
    """Fetch a feed, return entries as a list of plain dicts."""
    parsed = feedparser.parse(url)
    if parsed.bozo and not parsed.entries:
        raise RuntimeError(f"feed parse failed: {parsed.bozo_exception}")
    entries = []
    for e in parsed.entries[: limit or len(parsed.entries)]:
        entries.append(
            {
                "id": getattr(e, "id", None) or getattr(e, "link", None),
                "title": getattr(e, "title", "").strip(),
                "link": getattr(e, "link", None),
                "published": _entry_published(e),
                "summary": getattr(e, "summary", "").strip(),
            }
        )
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    try:
        entries = fetch(args.url, args.limit)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(entries, indent=2))


if __name__ == "__main__":
    main()
