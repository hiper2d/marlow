"""
alex_chat — Marlow's conversation with Alex in the news Telegram chat.

Every message Alex sends in the news chat lands in memory/inbox-from-alex.md
(the hourly `crosspost poll` files it there, whatever it is: a reply to a news
pick, a reaction to an article, or just a message). Marlow reads the inbox on
every writer tick and answers when she has something to say. She can also
start a conversation: change requests, problems, observations.

Inbox format: one section per Alex message, newest at the bottom.

    ## 2026-10-28 14:02 UTC · msg 990 · new
    > re: first 150 chars of the message he replied to
    Alex: his text
    Marlow (14:31 UTC): her reply

Status is `new` (unread), `answered` or `read`. Marlow's own openers are
logged as `## ... · msg N · from-marlow` sections.

CLI:
    python tools/alex_chat.py list-new
    python tools/alex_chat.py reply --to MSG_ID --text "..."   # threaded reply, marks answered
    python tools/alex_chat.py mark-read --id MSG_ID            # read, no reply needed
    python tools/alex_chat.py send --text "..."                # Marlow starts a message (capped per day)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from tools import notify  # noqa: E402

INBOX = REPO_ROOT / "memory" / "inbox-from-alex.md"
ARCHIVE = REPO_ROOT / "memory" / "inbox-archive.md"
STATE = REPO_ROOT / "projects" / "blog" / "crosspost" / "alex_chat_state.json"

# Marlow-initiated messages per UTC day. Replies to Alex don't count.
DAILY_SEND_CAP = 3
# Past this size, the oldest non-new sections move to the archive.
INBOX_CAP_BYTES = 10_000

HEADER = (
    "# Inbox from Alex\n\n"
    "Alex's messages from the news Telegram chat, oldest first, with your replies.\n"
    "Read it every writer tick. Answer with `tools/alex_chat.py reply`, or `mark-read`\n"
    "when no reply is needed. Code moves old handled messages to inbox-archive.md.\n\n"
)
_SECTION = re.compile(r"^## (.+?) · msg (\d+) · (new|answered|read|from-marlow)\s*$", re.M)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _read() -> str:
    return INBOX.read_text() if INBOX.exists() else HEADER


def _write(text: str) -> None:
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    INBOX.write_text(_bound(text))


def _sections(text: str) -> list[tuple[int, int, re.Match]]:
    ms = list(_SECTION.finditer(text))
    return [(m.start(), ms[i + 1].start() if i + 1 < len(ms) else len(text), m) for i, m in enumerate(ms)]


def _bound(text: str) -> str:
    """Move the oldest handled sections to the archive until under the cap."""
    moved = []
    while len(text.encode()) > INBOX_CAP_BYTES:
        old = next(((a, b) for a, b, m in _sections(text) if m.group(3) != "new"), None)
        if old is None:
            break
        moved.append(text[old[0]:old[1]])
        text = text[:old[0]] + text[old[1]:]
    if moved:
        with open(ARCHIVE, "a") as f:
            f.write("".join(moved))
    return text


def append_from_alex(msg_id: int, text: str, reply_to_text: str | None = None,
                     context: str | None = None) -> None:
    """File one incoming Alex message as a `new` section. Called by crosspost poll."""
    body = _read()
    if re.search(rf"· msg {int(msg_id)} ·", body):
        return  # already filed
    stamp = _now().strftime("%Y-%m-%d %H:%M UTC")
    sec = f"## {stamp} · msg {int(msg_id)} · new\n"
    if context:
        sec += f"> {context}\n"
    if reply_to_text:
        snippet = " ".join(reply_to_text.split())[:150]
        sec += f'> re: "{snippet}"\n'
    sec += f"Alex: {(text or '').strip() or '(no text)'}\n\n"
    _write(body.rstrip("\n") + "\n\n" + sec)


def list_new() -> list[dict]:
    text = _read()
    out = []
    for a, b, m in _sections(text):
        if m.group(3) == "new":
            out.append({"msg_id": int(m.group(2)), "received": m.group(1), "section": text[a:b].strip()})
    return out


def _set_status(msg_id: int, status: str, add_line: str | None = None) -> bool:
    text = _read()
    for a, b, m in _sections(text):
        if int(m.group(2)) == int(msg_id) and m.group(3) != "from-marlow":
            sec = text[a:b].rstrip("\n")
            sec = sec.replace(f"· msg {int(msg_id)} · {m.group(3)}", f"· msg {int(msg_id)} · {status}", 1)
            if add_line:
                sec += "\n" + add_line
            _write(text[:a] + sec + "\n\n" + text[b:].lstrip("\n"))
            return True
    return False


def reply(msg_id: int, text: str) -> dict:
    if not text.strip():
        return {"ok": False, "detail": "empty reply"}
    res = notify.send_telegram_message(text, channel="news", reply_to=int(msg_id))
    if not res.get("ok"):
        return {"ok": False, "detail": res.get("detail")}
    stamp = _now().strftime("%H:%M UTC")
    flat = text.strip().replace("\n", "\n  ")
    found = _set_status(msg_id, "answered", f"Marlow ({stamp}): {flat}")
    return {"ok": True, "sent_msg_id": res.get("message_id"), "filed": found}


def mark_read(msg_id: int) -> dict:
    return {"ok": _set_status(msg_id, "read")}


def _load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def send(text: str) -> dict:
    """Marlow starts a message to Alex. Capped at DAILY_SEND_CAP per UTC day."""
    if not text.strip():
        return {"ok": False, "detail": "empty message"}
    today = _now().strftime("%Y-%m-%d")
    st = _load_state()
    sent_today = st.get("sent", {}).get(today, 0)
    if sent_today >= DAILY_SEND_CAP:
        return {"ok": False, "detail": f"daily cap reached ({DAILY_SEND_CAP}); send it tomorrow or fold it into a reply"}
    res = notify.send_telegram_message(text, channel="news")
    if not res.get("ok"):
        return {"ok": False, "detail": res.get("detail")}
    st["sent"] = {today: sent_today + 1}
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st))
    stamp = _now().strftime("%Y-%m-%d %H:%M UTC")
    flat = text.strip().replace("\n", "\n  ")
    body = _read()
    _write(body.rstrip("\n") + f"\n\n## {stamp} · msg {res.get('message_id')} · from-marlow\nMarlow: {flat}\n\n")
    return {"ok": True, "sent_msg_id": res.get("message_id"), "sent_today": sent_today + 1, "cap": DAILY_SEND_CAP}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list-new")
    r = sub.add_parser("reply"); r.add_argument("--to", type=int, required=True); r.add_argument("--text", required=True)
    m = sub.add_parser("mark-read"); m.add_argument("--id", type=int, required=True)
    s = sub.add_parser("send"); s.add_argument("--text", required=True)
    a = ap.parse_args()
    if a.cmd == "list-new":
        out = {"ok": True, "new": list_new()}
    elif a.cmd == "reply":
        out = reply(a.to, a.text)
    elif a.cmd == "mark-read":
        out = mark_read(a.id)
    else:
        out = send(a.text)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0 if out.get("ok") else 1)


if __name__ == "__main__":
    main()
