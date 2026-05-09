"""
Marlow notify — Telegram bot for sending messages to Alex.

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
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import requests
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
DIGEST_DIR = REPO_ROOT / "digests" / "daily"
FALLBACK_LOG = REPO_ROOT / "digests" / "_notify_fallback.log"

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
TELEGRAM_TIMEOUT = 10  # seconds

Urgency = Literal["urgent", "digest"]


def _env() -> tuple[str | None, str | None]:
    load_dotenv(REPO_ROOT / ".env")
    return os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _log_fallback(message: str, reason: str) -> None:
    """Write to a local log when Telegram delivery fails — never lose a message."""
    FALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{_now().isoformat(timespec='seconds')}] [{reason}] {message}\n"
    with open(FALLBACK_LOG, "a") as f:
        f.write(line)


def send_telegram(message: str) -> tuple[bool, str]:
    """Send a single message via Telegram. Returns (ok, detail)."""
    token, chat_id = _env()
    if not token or not chat_id:
        return False, "missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env"
    try:
        resp = requests.post(
            TELEGRAM_API.format(token=token),
            json={"chat_id": chat_id, "text": message},
            timeout=TELEGRAM_TIMEOUT,
        )
        if resp.status_code != 200:
            return False, f"telegram returned {resp.status_code}: {resp.text[:200]}"
        return True, "sent"
    except requests.RequestException as e:
        return False, f"telegram request failed: {e}"


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
