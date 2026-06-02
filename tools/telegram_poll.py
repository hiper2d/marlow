"""
Marlow telegram_poll — read Alex's replies back from Telegram (the inbound half
of the bot; tools/notify.py is the outbound half).

The bot is otherwise send-only. This adds a minimal getUpdates poller so Marlow
can pick up Alex's replies (e.g. approving queued Substack comment drafts) on a
tick. It is deliberately dumb transport: it fetches new text messages from Alex's
chat and advances the read offset. It does NOT interpret commands — that judgment
("post 1,3", "skip the second one", "yes do them all") is left to Marlow's
session reading the messages against the outbox, which is far more robust than
brittle command parsing.

Offset semantics (Telegram getUpdates): passing offset=N confirms all updates
< N and returns updates >= N. We persist the last seen update_id and next call
with last+1, so each message is delivered exactly once.

Importable:
    from tools.telegram_poll import fetch_new_messages
    msgs = fetch_new_messages()          # [{update_id, date, text}], advances offset
    msgs = fetch_new_messages(advance=False)   # peek without consuming

CLI for manual testing:
    python tools/telegram_poll.py fetch         # consume + print new messages
    python tools/telegram_poll.py peek          # print without advancing offset
    python tools/telegram_poll.py reset         # forget offset (re-read backlog next time)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
OFFSET_PATH = REPO_ROOT / "tasks" / "telegram_offset.json"

TELEGRAM_GET_UPDATES = "https://api.telegram.org/bot{token}/getUpdates"
TELEGRAM_TIMEOUT = 15  # seconds


def _env() -> tuple[str | None, str | None]:
    load_dotenv(REPO_ROOT / ".env")
    return os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")


def _load_offset() -> int | None:
    try:
        return int(json.loads(OFFSET_PATH.read_text())["last_update_id"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _save_offset(update_id: int) -> None:
    OFFSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    OFFSET_PATH.write_text(json.dumps(
        {"last_update_id": int(update_id),
         "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")},
    ))


def fetch_new_messages(advance: bool = True) -> list[dict]:
    """Return new inbound text messages from Alex's chat since the last offset.

    Each item: {update_id, date (unix), text}. Only messages whose chat id matches
    TELEGRAM_CHAT_ID are returned (ignores anything from other chats). When
    advance=True the read offset is moved past the highest update_id seen, so the
    same message is never returned twice.
    """
    token, chat_id = _env()
    if not token or not chat_id:
        raise RuntimeError("missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")

    last = _load_offset()
    params: dict = {"timeout": 0}
    if last is not None:
        params["offset"] = last + 1

    resp = requests.get(TELEGRAM_GET_UPDATES.format(token=token), params=params, timeout=TELEGRAM_TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("ok"):
        raise RuntimeError(f"telegram getUpdates not ok: {str(payload)[:200]}")

    updates = payload.get("result", [])
    messages: list[dict] = []
    max_update_id = last
    for upd in updates:
        uid = upd.get("update_id")
        if uid is not None and (max_update_id is None or uid > max_update_id):
            max_update_id = uid
        msg = upd.get("message") or upd.get("edited_message")
        if not msg:
            continue
        if str(msg.get("chat", {}).get("id")) != str(chat_id):
            continue  # not Alex — ignore
        text = msg.get("text")
        if not text:
            continue
        messages.append({"update_id": uid, "date": msg.get("date"), "text": text})

    if advance and max_update_id is not None:
        _save_offset(max_update_id)
    return messages


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch", help="consume + print new messages (advances offset)")
    sub.add_parser("peek", help="print new messages without advancing offset")
    sub.add_parser("reset", help="forget the stored offset")
    args = ap.parse_args()

    if args.cmd == "reset":
        try:
            OFFSET_PATH.unlink()
            print(json.dumps({"ok": True, "reset": True}))
        except FileNotFoundError:
            print(json.dumps({"ok": True, "reset": False, "note": "no offset file"}))
        return

    try:
        msgs = fetch_new_messages(advance=(args.cmd == "fetch"))
    except (RuntimeError, requests.RequestException) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        sys.exit(1)
    print(json.dumps({"ok": True, "count": len(msgs), "messages": msgs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
