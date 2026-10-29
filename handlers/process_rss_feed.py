"""
process_rss_feed — first real handler.

Given a feed URL, returns the entries that are new since Marlow last
checked it. Marlow then decides what (if anything) to write up as a note.

State per-feed lives at projects/research/threads/_feed_state.json:
    {"<feed_url>": {"last_seen": "<iso8601>", "last_entry_id": "..."}}

CLI:
    python handlers/process_rss_feed.py fetch --url URL [--limit N]
        → JSON list of entries newer than last_seen for this URL
    python handlers/process_rss_feed.py mark-seen --url URL --latest ISO --entry-id ID
        → updates state so next fetch only sees newer entries
    python handlers/process_rss_feed.py state
        → prints the full feed state file
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = REPO_ROOT / "projects" / "research" / "threads" / "_feed_state.json"

# Make tools/ importable
sys.path.insert(0, str(REPO_ROOT))
from tools import rss_reader  # noqa: E402

import re  # noqa: E402
from datetime import datetime, timedelta, timezone  # noqa: E402

NOTES_ROOT = REPO_ROOT / "projects" / "research" / "notes"
# LessWrong and the Alignment Forum serve the same post under the same id
# (lesswrong.com/posts/<id>/... == alignmentforum.org/posts/<id>/...).
_LW_POST_ID = re.compile(r"(?:lesswrong\.com|alignmentforum\.org)/posts/([A-Za-z0-9]{10,})")


def _dedup_keys(url: str | None) -> set[str]:
    if not url:
        return set()
    keys = {url.split("?")[0].split("#")[0].rstrip("/").lower()}
    m = _LW_POST_ID.search(url)
    if m:
        keys.add("lw:" + m.group(1))
    return keys


def _captured_keys(days: int = 3) -> set[str]:
    """Dedup keys of candidate notes written in the last `days` days, any source."""
    keys: set[str] = set()
    today = datetime.now(timezone.utc).date()
    for i in range(days):
        d = NOTES_ROOT / (today - timedelta(days=i)).isoformat() / "candidates"
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            try:
                head = f.read_text()[:1500]
            except OSError:
                continue
            m = re.search(r'^url:\s*"?([^"\n]+)"?', head, re.M)
            if m:
                keys |= _dedup_keys(m.group(1).strip())
    return keys


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text())


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True))


def fetch_new(url: str, limit: int | None = None) -> list[dict]:
    """Return entries newer than this feed's last_seen timestamp."""
    state = load_state()
    last_seen = (state.get(url) or {}).get("last_seen")
    last_id = (state.get(url) or {}).get("last_entry_id")
    entries = rss_reader.fetch(url, limit=limit)
    if last_seen is None and last_id is None:
        # First time we see this feed — return everything (capped) so Marlow
        # can decide which entries are worth noting.
        return entries
    new = []
    for e in entries:
        if e.get("id") == last_id:
            break  # we've caught up to where we left off
        if e.get("published") and last_seen and e["published"] <= last_seen:
            continue  # older than last_seen
        new.append(e)
    # Cross-source dedup: drop entries already captured as a candidate from
    # another feed (e.g. an AF post that the LessWrong scan already noted).
    captured = _captured_keys()
    return [e for e in new if not (_dedup_keys(e.get("link")) & captured)]


def mark_seen(url: str, latest_iso: str, entry_id: str) -> None:
    state = load_state()
    state[url] = {"last_seen": latest_iso, "last_entry_id": entry_id}
    save_state(state)


def cmd_fetch(args):
    entries = fetch_new(args.url, args.limit)
    print(json.dumps(entries, indent=2))


def cmd_mark_seen(args):
    mark_seen(args.url, args.latest, args.entry_id)
    print(f"marked {args.url} → {args.latest}")


def cmd_state(args):
    print(json.dumps(load_state(), indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fetch = sub.add_parser("fetch", help="Fetch entries newer than last_seen")
    p_fetch.add_argument("--url", required=True)
    p_fetch.add_argument("--limit", type=int, default=None)

    p_mark = sub.add_parser("mark-seen", help="Update last_seen for a feed")
    p_mark.add_argument("--url", required=True)
    p_mark.add_argument("--latest", required=True, help="ISO8601 timestamp of newest seen entry")
    p_mark.add_argument("--entry-id", required=True)

    sub.add_parser("state", help="Print the feed state file")

    args = parser.parse_args()
    if args.cmd == "fetch":
        cmd_fetch(args)
    elif args.cmd == "mark-seen":
        cmd_mark_seen(args)
    elif args.cmd == "state":
        cmd_state(args)


if __name__ == "__main__":
    main()
