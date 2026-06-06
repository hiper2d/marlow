"""
crosspost_store — state for the news-crosspost flow.

The daily news curate tick sends each interesting pick to Alex as its own
Telegram message and registers it here. Alex replies *to a message* when he
wants it crossposted (`substack`, `x`, or `both`, optionally with an angle).
Marlow drafts the post in Alex's voice, sends the draft back for review, and on
his `go` posts it. No reply = nothing happens (the item just sits; the research
pipeline still uses it for the blog regardless).

One store, under projects/blog/crosspost/state.json:

    {"items": {
        "<news_msg_id>": {
            "msg_id":      <telegram message_id of the news message we sent>,
            "url":         "<article url>",
            "title":       "<article title>",
            "source":      "<feed name>",
            "take":        "<Marlow's 2-line take that went out>",
            "sent_at":     "...Z",
            "status":      "sent" | "awaiting_approval" | "posted"
                           | "partial" | "skipped",
            "platforms":   ["substack", "x"],     # what Alex asked for
            "instructions":["punchier", "cut the last line"],  # accrued edits
            "drafts":      {"substack": "<note text>", "x": ["<hook>", "<...url>"]},
            "draft_msg_id":<telegram message_id of the draft we sent back>,
            "posted":      {"substack": "<note url>", "x": "<tweet url>"}
        }}}

Matching a reply: store the news message_id when we send the item, and the draft
message_id when we send a draft back. A reply's reply_to_message_id matches one
of those, so we know whether Alex is routing a fresh item ("post on both") or
reacting to a draft ("go" / an edit). find_by_reply() resolves both.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parent.parent
CROSSPOST_DIR = REPO_ROOT / "projects" / "blog" / "crosspost"
STATE_PATH = CROSSPOST_DIR / "state.json"

PLATFORMS = ("substack", "x")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_state() -> dict:
    try:
        s = json.loads(STATE_PATH.read_text())
    except (OSError, ValueError):
        s = {}
    s.setdefault("items", {})
    return s


def save_state(state: dict) -> None:
    CROSSPOST_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def add_item(msg_id: int, url: str, title: str, source: str, take: str) -> dict:
    """Register a news item we just sent to Telegram (keyed by its message_id)."""
    s = load_state()
    item = {
        "msg_id": int(msg_id),
        "url": url,
        "title": title,
        "source": source,
        "take": take,
        "sent_at": _now_iso(),
        "status": "sent",
        "platforms": list(PLATFORMS),   # always both — Alex crossposts to Substack + X together
        "instructions": [],
        "drafts": {},
        "draft_msg_id": None,
        "posted": {},
    }
    s["items"][str(msg_id)] = item
    save_state(s)
    return item


def get(msg_id: int | str) -> dict | None:
    return load_state()["items"].get(str(msg_id))


def find_by_reply(reply_to_msg_id: int | str) -> tuple[dict | None, str | None]:
    """Resolve a reply's target. Returns (item, which) where which is:
        "news"  — Alex replied to the original news message (routing a crosspost)
        "draft" — Alex replied to a draft we sent back (go / edit / voice)
        None    — no match (reply to something unrelated)."""
    if reply_to_msg_id is None:
        return None, None
    rid = str(reply_to_msg_id)
    items = load_state()["items"]
    if rid in items:
        return items[rid], "news"
    for it in items.values():
        if it.get("draft_msg_id") is not None and str(it["draft_msg_id"]) == rid:
            return it, "draft"
    return None, None


def _mutate(msg_id: int | str, fn) -> dict | None:
    s = load_state()
    it = s["items"].get(str(msg_id))
    if it is None:
        return None
    fn(it)
    save_state(s)
    return it


def set_platforms(msg_id: int | str, platforms: list[str]) -> dict | None:
    clean = [p for p in platforms if p in PLATFORMS]
    return _mutate(msg_id, lambda it: it.__setitem__("platforms", clean))


def add_instruction(msg_id: int | str, text: str) -> dict | None:
    return _mutate(msg_id, lambda it: it["instructions"].append(text.strip()))


def set_draft(msg_id: int | str, platform: str, draft) -> dict | None:
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}")
    return _mutate(msg_id, lambda it: it["drafts"].__setitem__(platform, draft))


def set_draft_msg_id(msg_id: int | str, draft_msg_id: int) -> dict | None:
    return _mutate(msg_id, lambda it: it.__setitem__("draft_msg_id", int(draft_msg_id)))


def set_status(msg_id: int | str, status: str) -> dict | None:
    return _mutate(msg_id, lambda it: it.__setitem__("status", status))


def set_posted(msg_id: int | str, platform: str, url: str | None) -> dict | None:
    return _mutate(msg_id, lambda it: it["posted"].__setitem__(platform, url))


def list_items(status: str | None = None) -> list[dict]:
    items = list(load_state()["items"].values())
    if status:
        items = [it for it in items if it.get("status") == status]
    return sorted(items, key=lambda it: it.get("sent_at", ""))
