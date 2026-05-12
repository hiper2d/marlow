"""
compose_daily_digest — assemble today's accumulated digest entries and
send them to Alex via Telegram.

`tools/notify.py` accumulates `urgency=digest` entries into
`digests/daily/<date>.md` throughout the day. This handler is the
end-of-day delivery: read that file, chunk if needed, send via the
notify tool's send_telegram (bypassing the digest-append path).

If the day's file is empty or missing, send a short "quiet day"
message instead — confirms the loop is alive without filler.

CLI:
    python handlers/compose_daily_digest.py send
    python handlers/compose_daily_digest.py send --date 2026-05-09
    python handlers/compose_daily_digest.py preview [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIGEST_DIR = REPO_ROOT / "digests" / "daily"

sys.path.insert(0, str(REPO_ROOT))
from tools import notify  # noqa: E402

TG_MAX_LEN = 4000  # Telegram caps at 4096; leave headroom for continuation markers


def _today() -> str:
    """Return the date this digest should cover.

    The task is scheduled at 23:00 UTC. If the agent was asleep at 23:00
    and the tick fires after UTC rollover, defaulting to `now().date()`
    sends an empty file for the new day and skips the actual day's
    accumulated entries. So: within the first 4 hours after UTC midnight,
    default to yesterday — that's the day the schedule intended.
    """
    now = datetime.now(timezone.utc)
    if now.hour < 4:
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    return now.strftime("%Y-%m-%d")


def _chunk(text: str, max_len: int = TG_MAX_LEN) -> list[str]:
    """Split text into chunks of <= max_len, breaking on paragraph boundaries."""
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
    current = ""
    for paragraph in text.split("\n\n"):
        if not paragraph:
            continue
        candidate = (current + "\n\n" + paragraph) if current else paragraph
        if len(candidate) > max_len:
            if current:
                chunks.append(current)
                current = paragraph
            else:
                # Single paragraph alone exceeds max_len — hard split.
                while len(paragraph) > max_len:
                    chunks.append(paragraph[:max_len])
                    paragraph = paragraph[max_len:]
                current = paragraph
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def _quiet_day_message(date: str) -> str:
    return f"Marlow — {date}\n\nQuiet day. Nothing worth flagging."


def assemble(date: str) -> tuple[str, int]:
    """Read today's digest file, return (message_to_send, entry_count)."""
    path = DIGEST_DIR / f"{date}.md"
    if not path.exists():
        return _quiet_day_message(date), 0
    body = path.read_text().strip()
    if not body:
        return _quiet_day_message(date), 0
    # Each entry is delimited by an "━━━ HH:MM UTC ━━━" line (notify.py format)
    entry_count = body.count("━━━ ")
    if entry_count == 0:
        # File exists but no entries — only the date header. Treat as quiet.
        return _quiet_day_message(date), 0
    return body, entry_count


def send_digest(date: str) -> dict:
    """Assemble and send today's digest. Returns a result dict."""
    message, entry_count = assemble(date)
    chunks = _chunk(message)
    sent = []
    failed = []
    total = len(chunks)
    for i, chunk in enumerate(chunks, 1):
        prefix = f"[{i}/{total}] " if total > 1 else ""
        ok, detail = notify.send_telegram(prefix + chunk)
        (sent if ok else failed).append({"chunk": i, "detail": detail})
    return {
        "date": date,
        "entry_count": entry_count,
        "chunks_sent": len(sent),
        "chunks_failed": len(failed),
        "details": {"sent": sent, "failed": failed},
    }


# ─── CLI ───────────────────────────────────────────────────────────────────


def cmd_send(args):
    date = args.date or _today()
    result = send_digest(date)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["chunks_failed"] == 0 else 1)


def cmd_preview(args):
    date = args.date or _today()
    message, entry_count = assemble(date)
    chunks = _chunk(message)
    print(f"Date:        {date}")
    print(f"Entries:     {entry_count}")
    print(f"Chunks:      {len(chunks)}")
    print(f"Total chars: {sum(len(c) for c in chunks)}")
    print("─" * 56)
    for i, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            print(f"--- chunk {i}/{len(chunks)} ({len(chunk)} chars) ---")
        print(chunk)
        print()


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_send = sub.add_parser("send", help="Assemble and send today's digest to Telegram")
    p_send.add_argument("--date", help="Override date (YYYY-MM-DD); defaults to today UTC")

    p_preview = sub.add_parser("preview", help="Show what would be sent without sending")
    p_preview.add_argument("--date", help="Override date; defaults to today UTC")

    args = parser.parse_args()
    if args.cmd == "send":
        cmd_send(args)
    elif args.cmd == "preview":
        cmd_preview(args)


if __name__ == "__main__":
    main()
