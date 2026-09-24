"""
Marlow notify — Telegram bots for sending messages to Alex.

Two bots, split 2026-09-22 so alerts don't drown in the news feed:
- channel="monitor" (default): urgents, the 23:00 ops digest, tick notifies.
  Creds TELEGRAM_MONITOR_BOT_TOKEN / TELEGRAM_MONITOR_CHAT_ID (the old
  fitness bot, renamed "Monitoring"). Falls back to the news bot if unset.
- channel="news": news picks, publish reaction pings, crosspost replies.
  Creds TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID. This is also the bot
  tools/telegram_poll.py reads replies from, so anything Alex is expected to
  reply to MUST go out on "news".

Two urgency modes:
- urgent: send immediately as a Telegram message
- digest: append to today's digest file; the daily digest handler sends
  the assembled file as one message at 11pm

Failures (missing credentials, Telegram API errors) fall back to a local
log file so notifications are never silently lost.

Importable:
    from tools.notify import notify_alex
    notify_alex("API key X is below threshold", urgency="urgent")
    notify_alex("New paper: ...", urgency="digest")

CLI for manual testing:
    python tools/notify.py "test message"             # urgent
    python tools/notify.py "test message" --digest    # append to digest
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import requests
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
DIGEST_DIR = REPO_ROOT / "digests" / "daily"
FALLBACK_LOG = REPO_ROOT / "digests" / "_notify_fallback.log"
# Urgents Telegram refused, waiting to ride along in the next 23:00 digest
# (compose_daily_digest reads + clears it). The fallback log alone was a dead end:
# the 2026-09-22 20:21Z alert died there during a TLS block and nothing read it.
UNDELIVERED = REPO_ROOT / "digests" / "_undelivered.jsonl"

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
TELEGRAM_TIMEOUT = 10  # seconds

Urgency = Literal["urgent", "digest"]
Channel = Literal["monitor", "news"]


def _env(channel: Channel = "monitor") -> tuple[str | None, str | None]:
    load_dotenv(REPO_ROOT / ".env")
    news = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if channel == "news":
        return news
    mon = os.getenv("TELEGRAM_MONITOR_BOT_TOKEN"), os.getenv("TELEGRAM_MONITOR_CHAT_ID")
    return mon if all(mon) else news


# requests puts the full URL, bot token included, into its exception text.
_TOKEN_RE = re.compile(r"bot\d+:[A-Za-z0-9_-]+")


def _redact(text: str) -> str:
    return _TOKEN_RE.sub("bot<redacted>", text)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _log_fallback(message: str, reason: str) -> None:
    """Write to a local log when Telegram delivery fails — never lose a message."""
    FALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{_now().isoformat(timespec='seconds')}] [{_redact(reason)}] {message}\n"
    with open(FALLBACK_LOG, "a") as f:
        f.write(line)


def send_telegram_message(message: str, channel: Channel = "monitor") -> dict:
    """Send one Telegram message. Returns {ok, message_id, detail}.

    Unlike send_telegram (which returns just (ok, detail)), this surfaces the
    sent message_id. The crosspost flow needs it: each news item is sent as its
    own message, and Alex replies *to that message* to ask for a crosspost — we
    match his threaded reply (reply_to_message.message_id) back to the item by
    this id.
    """
    token, chat_id = _env(channel)
    if not token or not chat_id:
        return {"ok": False, "message_id": None, "detail": f"missing Telegram creds for channel {channel!r} in .env"}
    try:
        resp = requests.post(
            TELEGRAM_API.format(token=token),
            json={"chat_id": chat_id, "text": message},
            timeout=TELEGRAM_TIMEOUT,
        )
        if resp.status_code != 200:
            return {"ok": False, "message_id": None, "detail": _redact(f"telegram returned {resp.status_code}: {resp.text[:200]}")}
        mid = (resp.json().get("result") or {}).get("message_id")
        return {"ok": True, "message_id": mid, "detail": "sent"}
    except (requests.RequestException, ValueError) as e:
        return {"ok": False, "message_id": None, "detail": _redact(f"telegram request failed: {e}")}


def _queue_undelivered(message: str, detail: str) -> None:
    try:
        UNDELIVERED.parent.mkdir(parents=True, exist_ok=True)
        with open(UNDELIVERED, "a") as f:
            f.write(json.dumps({"ts": _now().isoformat(timespec="seconds"),
                                "message": message, "detail": _redact(detail)[:200]},
                               ensure_ascii=False) + "\n")
    except OSError:
        pass  # the fallback log still has it


def read_undelivered() -> list[dict]:
    """Urgents still waiting for a delivery, oldest first."""
    try:
        lines = UNDELIVERED.read_text().splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def clear_undelivered(delivered: list[dict]) -> None:
    """Drop entries that went out in a digest. Anything queued meanwhile stays."""
    keep = [e for e in read_undelivered() if e not in delivered]
    try:
        if keep:
            UNDELIVERED.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in keep))
        else:
            UNDELIVERED.unlink(missing_ok=True)
    except OSError:
        pass


def send_telegram(message: str, channel: Channel = "monitor") -> tuple[bool, str]:
    """Send a single message via Telegram. Returns (ok, detail).

    Thin back-compat wrapper over send_telegram_message for callers that don't
    need the message_id (the digest sender, urgent notifies, etc.)."""
    r = send_telegram_message(message, channel)
    return r["ok"], r["detail"]


def append_to_digest(message: str) -> Path:
    """Append a timestamped entry to today's digest file. Returns the file path.

    Format is plain-text-friendly so the assembled digest reads well in
    Telegram without markdown rendering. URL auto-linking still works as
    long as URLs include their https:// prefix.
    """
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    today = _now().strftime("%Y-%m-%d")
    path = DIGEST_DIR / f"{today}.md"
    if not path.exists():
        path.write_text(f"Marlow daily digest — {today}\n\n")
    timestamp = _now().strftime("%H:%M UTC")
    with open(path, "a") as f:
        f.write(f"━━━ {timestamp} ━━━\n\n{message}\n\n")
    return path


def notify_alex(message: str, urgency: Urgency = "digest") -> dict:
    """Send a notification. Returns a result dict for the caller to log."""
    if urgency == "urgent":
        ok, detail = send_telegram(message)
        if not ok:
            _log_fallback(message, f"urgent telegram failed: {detail}")
            _queue_undelivered(message, detail)
        return {"urgency": "urgent", "delivered": ok, "detail": detail}
    if urgency == "digest":
        try:
            path = append_to_digest(message)
            return {"urgency": "digest", "delivered": True, "path": str(path)}
        except OSError as e:
            _log_fallback(message, f"digest append failed: {e}")
            return {"urgency": "digest", "delivered": False, "detail": str(e)}
    raise ValueError(f"unknown urgency: {urgency!r}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="Message text to send")
    parser.add_argument(
        "--digest",
        action="store_true",
        help="Append to today's digest file instead of sending immediately",
    )
    args = parser.parse_args()
    urgency: Urgency = "digest" if args.digest else "urgent"
    result = notify_alex(args.message, urgency=urgency)
    print(result)
    sys.exit(0 if result["delivered"] else 1)


if __name__ == "__main__":
    main()
