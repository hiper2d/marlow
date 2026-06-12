"""
reactions_store — Alex's gut reactions to published articles (Simona's review surface).

When Marlow publishes, `publish_article` pings Alex on Telegram for a one-line
gut reaction and registers the ping's message_id here. The single inbound poller
(`crosspost.poll`) matches Alex's reply by reply_to_message_id and records the
reaction text here.

SIMONA-SIDE ON PURPOSE: no drafting handler reads this file. Marlow never sees
the raw reactions — reading "Alex was bored by this" would turn the blog into
people-pleasing, the exact drift the sandboxed voice-journal design avoids. The
signal reaches Marlow's writing only after Simona distills it into a rubric edit
(voice-guidelines.md via the feedback inbox) or a craft-framed journal note.
Simona reads this file at editorial-review time.

Append-only JSONL at projects/blog/reactions.jsonl. Two record types:
    {"type":"request",  "ts":..., "msg_id":N, "slug":..., "title":..., "url":...}
    {"type":"reaction", "ts":..., "msg_id":N, "slug":..., "title":..., "text":...}
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parent.parent
STORE_PATH = REPO_ROOT / "projects" / "blog" / "reactions.jsonl"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _append(rec: dict) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with STORE_PATH.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _read_all() -> list[dict]:
    try:
        lines = STORE_PATH.read_text().splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def request(msg_id: int, slug: str, title: str, url: str) -> dict:
    rec = {
        "type": "request", "ts": _now_iso(), "msg_id": int(msg_id),
        "slug": slug, "title": title, "url": url,
    }
    _append(rec)
    return rec


def find_request(reply_to_msg_id) -> dict | None:
    """Return the publish-reaction request a reply targets, if any."""
    if reply_to_msg_id is None:
        return None
    try:
        rid = int(reply_to_msg_id)
    except (TypeError, ValueError):
        return None
    for rec in _read_all():
        if rec.get("type") == "request" and rec.get("msg_id") == rid:
            return rec
    return None


def record(msg_id: int, slug: str, title: str, text: str) -> dict:
    rec = {
        "type": "reaction", "ts": _now_iso(), "msg_id": int(msg_id),
        "slug": slug, "title": title, "text": (text or "").strip(),
    }
    _append(rec)
    return rec


def list_reactions() -> list[dict]:
    return [r for r in _read_all() if r.get("type") == "reaction"]
