"""
process_sitemap_feed — sibling of process_rss_feed for sites without RSS.

Reads a sitemap (optionally with a URL prefix filter), returns entries
newer than this feed's last_seen timestamp. Shares the same per-feed
state file as the RSS handler — keyed by sitemap URL + prefix, so two
different prefixes against the same sitemap don't collide.

CLI:
    python handlers/process_sitemap_feed.py fetch --url URL [--prefix PFX] [--limit N]
    python handlers/process_sitemap_feed.py mark-seen --url URL [--prefix PFX] --latest ISO --entry-id ID
    python handlers/process_sitemap_feed.py state
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = REPO_ROOT / "projects" / "research" / "threads" / "_feed_state.json"

sys.path.insert(0, str(REPO_ROOT))
from tools import sitemap_reader  # noqa: E402


def _state_key(url: str, prefix: str | None) -> str:
    return f"{url}|{prefix or ''}"


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text())


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True))


def fetch_new(url: str, prefix: str | None = None, limit: int | None = None) -> list[dict]:
    state = load_state()
    key = _state_key(url, prefix)
    last_seen = (state.get(key) or {}).get("last_seen")
    last_id = (state.get(key) or {}).get("last_entry_id")
    entries = sitemap_reader.fetch(url, prefix=prefix, limit=limit)
    if last_seen is None and last_id is None:
        # First scan — return everything (capped) so Marlow can decide.
        return entries
    new = []
    for e in entries:
        if e.get("id") == last_id:
            break
        if e.get("published") and last_seen and e["published"] <= last_seen:
            continue
        new.append(e)
    return new


def mark_seen(url: str, prefix: str | None, latest_iso: str, entry_id: str) -> None:
    state = load_state()
    state[_state_key(url, prefix)] = {"last_seen": latest_iso, "last_entry_id": entry_id}
    save_state(state)


def cmd_fetch(args):
    print(json.dumps(fetch_new(args.url, prefix=args.prefix, limit=args.limit), indent=2))


def cmd_mark_seen(args):
    mark_seen(args.url, args.prefix, args.latest, args.entry_id)
    print(f"marked {args.url} (prefix={args.prefix}) → {args.latest}")


def cmd_state(args):
    print(json.dumps(load_state(), indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fetch = sub.add_parser("fetch")
    p_fetch.add_argument("--url", required=True)
    p_fetch.add_argument("--prefix", default=None)
    p_fetch.add_argument("--limit", type=int, default=None)

    p_mark = sub.add_parser("mark-seen")
    p_mark.add_argument("--url", required=True)
    p_mark.add_argument("--prefix", default=None)
    p_mark.add_argument("--latest", required=True)
    p_mark.add_argument("--entry-id", required=True)

    sub.add_parser("state")

    args = parser.parse_args()
    if args.cmd == "fetch":
        cmd_fetch(args)
    elif args.cmd == "mark-seen":
        cmd_mark_seen(args)
    elif args.cmd == "state":
        cmd_state(args)


if __name__ == "__main__":
    main()
