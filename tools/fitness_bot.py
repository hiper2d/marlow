"""
fitness_bot — Telegram client for @marlow_fitness_bot (the calorie bot).

Separate bot from the ops/notify bot (`notify.py`). This one both
RECEIVES (food photos + text notes from Alex) and SENDS (the nightly
calorie digest back to the same chat). Keeping food traffic on its own
bot keeps it out of Marlow's alert channel.

Credentials (in the gitignored .env, mirrored from the launchd plist):
    MARLOW_FITNESS_BOT_TOKEN
    MARLOW_FITNESS_CHAT_ID

Only ONE consumer may long-poll a bot's getUpdates at a time. The
`poll_food` handler is that sole consumer; nothing else should call
get_updates() on this token.

Importable:
    from tools.fitness_bot import get_updates, download_file, send_message

CLI for manual testing:
    uv run python tools/fitness_bot.py whoami
    uv run python tools/fitness_bot.py send "test from Marlow"
    uv run python tools/fitness_bot.py peek          # getUpdates, no offset commit
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

# Mirror the launchd plist env so standalone invocations see the same
# secrets a tick-fired run would.
sys.path.insert(0, str(REPO_ROOT))
try:
    from driver.env_loader import import_plist_env  # noqa: E402

    import_plist_env()
except Exception:
    pass

API = "https://api.telegram.org/bot{token}"
TIMEOUT = 30


def _creds() -> tuple[str | None, str | None]:
    load_dotenv(REPO_ROOT / ".env")
    return (
        os.getenv("MARLOW_FITNESS_BOT_TOKEN"),
        os.getenv("MARLOW_FITNESS_CHAT_ID"),
    )


def _token() -> str:
    token, _ = _creds()
    if not token:
        raise RuntimeError("MARLOW_FITNESS_BOT_TOKEN not in environment")
    return token


def get_updates(offset: int | None = None, *, timeout: int = 0) -> list[dict]:
    """Fetch new updates. Passing `offset` confirms (consumes) all updates
    with a lower id — Telegram won't return them again. Omit offset to
    peek without consuming."""
    params: dict = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    resp = requests.get(
        API.format(token=_token()) + "/getUpdates", params=params, timeout=TIMEOUT
    )
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram getUpdates failed: {payload}")
    return payload.get("result", [])


def download_file(file_id: str, dest: Path) -> Path:
    """Download a Telegram file (e.g. a photo) to `dest`."""
    token = _token()
    info = requests.get(
        API.format(token=token) + "/getFile",
        params={"file_id": file_id},
        timeout=TIMEOUT,
    )
    info.raise_for_status()
    file_path = info.json()["result"]["file_path"]
    url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    blob = requests.get(url, timeout=TIMEOUT)
    blob.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(blob.content)
    return dest


def send_message(text: str) -> dict:
    """Send a message to Alex's fitness-bot chat."""
    token, chat_id = _creds()
    if not token or not chat_id:
        raise RuntimeError("MARLOW_FITNESS_BOT_TOKEN / _CHAT_ID not in environment")
    resp = requests.post(
        API.format(token=token) + "/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    p = argparse.ArgumentParser(description="Fitness Telegram bot client.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami", help="getMe — confirm the bot identity.")
    sub.add_parser("peek", help="getUpdates without committing an offset.")
    ps = sub.add_parser("send", help="Send a message to the fitness chat.")
    ps.add_argument("text")
    args = p.parse_args()

    if args.cmd == "whoami":
        resp = requests.get(API.format(token=_token()) + "/getMe", timeout=TIMEOUT)
        print(json.dumps(resp.json(), indent=2))
    elif args.cmd == "peek":
        print(json.dumps(get_updates(), indent=2, ensure_ascii=False))
    elif args.cmd == "send":
        print(json.dumps(send_message(args.text), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
