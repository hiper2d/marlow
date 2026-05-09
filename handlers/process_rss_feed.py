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
    return new


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
