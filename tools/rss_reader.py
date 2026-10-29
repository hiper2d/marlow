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
import json as _json
import re
import time
import urllib.request
from datetime import datetime, timedelta, timezone

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


_YT_FEED = re.compile(r"youtube\.com/feeds/videos\.xml\?channel_id=([\w-]+)")
_AGO = re.compile(r"(\d+)\s*(second|minute|hour|day|week|month|year)s?\s+ago")
_AGO_UNIT = {"second": 1, "minute": 60, "hour": 3600, "day": 86400,
             "week": 7 * 86400, "month": 30 * 86400, "year": 365 * 86400}


def _youtube_channel_page(channel_id: str, limit: int | None) -> list[dict]:
    """Fallback for YouTube: read the channel's /videos page instead of the feed.

    The anonymous videos.xml endpoint returns 404/500 for most channels from
    this host (seen 2026-10). The channel page still works. Entry ids use the
    feed's `yt:video:<id>` form so last_entry_id dedup carries over. Publish
    times are approximate (from "2 days ago"); no description.
    """
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/130 Safari/537.36",
        "Accept-Language": "en-US,en",
    })
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    if not m:
        raise RuntimeError("youtube channel page: no ytInitialData")
    lockups: list[dict] = []

    def walk(o):
        if isinstance(o, dict):
            if "lockupViewModel" in o:
                lockups.append(o["lockupViewModel"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(_json.loads(m.group(1)))
    now = datetime.now(timezone.utc)
    entries = []
    for lv in lockups:
        if lv.get("contentType") != "LOCKUP_CONTENT_TYPE_VIDEO" or not lv.get("contentId"):
            continue
        md = lv.get("metadata", {}).get("lockupMetadataViewModel", {})
        published = None
        for row in md.get("metadata", {}).get("contentMetadataViewModel", {}).get("metadataRows", []):
            for part in row.get("metadataParts", []):
                a = _AGO.search(part.get("accessibilityLabel") or "")
                if a:
                    published = (now - timedelta(seconds=int(a.group(1)) * _AGO_UNIT[a.group(2)])).isoformat()
        vid = lv["contentId"]
        entries.append({
            "id": f"yt:video:{vid}",
            "title": (md.get("title", {}).get("content") or "").strip(),
            "link": f"https://www.youtube.com/watch?v={vid}",
            "published": published,
            "summary": "",
        })
    if not entries:
        raise RuntimeError("youtube channel page: no videos found")
    return entries[: limit or len(entries)]


def fetch(url: str, limit: int | None = None, attempts: int = 3) -> list[dict]:
    """Fetch a feed, return entries as a list of plain dicts.

    Retries a failed fetch (HTTP error or unparseable body with no entries) up
    to `attempts` times with a short backoff. YouTube's anonymous feed endpoint
    serves intermittent 404s / garbled bodies from this host; one or two retries
    absorb most of them.
    """
    for attempt in range(1, attempts + 1):
        parsed = feedparser.parse(url)
        status = getattr(parsed, "status", 200)
        failed = (parsed.bozo and not parsed.entries) or (status >= 400 and not parsed.entries)
        if not failed:
            break
        if attempt < attempts:
            time.sleep(2 * attempt)
    else:
        yt = _YT_FEED.search(url)
        if yt:
            return _youtube_channel_page(yt.group(1), limit)
        reason = parsed.bozo_exception if parsed.bozo else f"HTTP {status}"
        raise RuntimeError(f"feed fetch failed after {attempts} attempts: {reason}")
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
