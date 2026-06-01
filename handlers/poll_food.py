"""
poll_food — pull new food messages from the fitness bot into the DB.

Runs every tick. Fetches new Telegram updates (photos + text notes Alex
sent to @marlow_fitness_bot), downloads any photos, and inserts each as a
*pending* entry in calorie_db. It does NOT estimate calories — that's
Marlow's job in the tick session, working from the pending rows.

Why pending rows instead of returning raw data for Marlow to hold in
context: durability. The Telegram offset is advanced as soon as messages
are fetched, so if a tick dies after fetching, those messages are gone
from Telegram's queue. Writing them to the DB first means a crash loses
nothing — the next tick just sees them still `pending` and estimates them.

Offset state lives in projects/calories/state/offset.json. Photos are
saved under projects/calories/inbox/<YYYY-MM-DD>/.

CLI:
    uv run python handlers/poll_food.py fetch
        → JSON: {fetched, new_pending, skipped_duplicates, pending_ids}
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from driver.env_loader import import_plist_env  # noqa: E402

import_plist_env()

from tools import calorie_db, fitness_bot  # noqa: E402

PROJECT_DIR = REPO_ROOT / "projects" / "calories"
STATE_PATH = PROJECT_DIR / "state" / "offset.json"
INBOX_DIR = PROJECT_DIR / "inbox"


def _load_offset() -> int | None:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text()).get("offset")
        except (json.JSONDecodeError, OSError):
            return None
    return None


def _save_offset(offset: int) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"offset": offset}))


def _extract(message: dict) -> tuple[str | None, str | None, str | None]:
    """Return (raw_text, photo_file_id, voice_file_id) for a message."""
    note = message.get("caption") or message.get("text")
    photo_file_id = None
    if message.get("photo"):
        # `photo` is an array of sizes; the last is the largest.
        photo_file_id = message["photo"][-1]["file_id"]
    voice_file_id = None
    # `voice` = recorded note (OGG/Opus); `audio` = an uploaded audio file.
    if message.get("voice"):
        voice_file_id = message["voice"]["file_id"]
    elif message.get("audio"):
        voice_file_id = message["audio"]["file_id"]
    return note, photo_file_id, voice_file_id


def fetch() -> dict:
    calorie_db.init_db()
    offset = _load_offset()
    updates = fitness_bot.get_updates(offset=offset)

    new_pending: list[int] = []
    skipped = 0
    max_update_id = offset - 1 if offset is not None else None

    for upd in updates:
        update_id = upd["update_id"]
        if max_update_id is None or update_id > max_update_id:
            max_update_id = update_id

        message = upd.get("message") or upd.get("edited_message")
        if not message:
            continue  # ignore non-message updates (e.g. callback queries)

        note, photo_file_id, voice_file_id = _extract(message)
        if not note and not photo_file_id and not voice_file_id:
            continue  # nothing edible here (sticker, etc.)

        ts_utc = datetime.fromtimestamp(message["date"], tz=timezone.utc)
        day_dir = INBOX_DIR / ts_utc.astimezone(calorie_db.LOCAL_TZ).date().isoformat()

        photo_rel = None
        if photo_file_id:
            dest = day_dir / f"{update_id}.jpg"
            try:
                fitness_bot.download_file(photo_file_id, dest)
                photo_rel = str(dest.relative_to(REPO_ROOT))
            except Exception as e:  # noqa: BLE001 — keep the entry, flag the miss
                note = (note or "") + f" [photo download failed: {e}]"

        # Voice note: download the OGG, transcribe locally, use the
        # transcript as the note. Marlow can't hear audio, so this is the
        # only way the content reaches the estimate step.
        audio_rel = None
        transcript = None
        if voice_file_id:
            dest = day_dir / f"{update_id}.ogg"
            try:
                fitness_bot.download_file(voice_file_id, dest)
                audio_rel = str(dest.relative_to(REPO_ROOT))
                from tools.transcribe import transcribe_audio

                result = transcribe_audio(dest)
                transcript = result.get("text") or None
            except Exception as e:  # noqa: BLE001 — keep the entry, flag the miss
                note = (note or "") + f" [voice transcription failed: {e}]"

        # Merge a typed caption with a transcript if both somehow present.
        note = " | ".join(p for p in (note, transcript) if p) or None

        if photo_rel and (note or audio_rel):
            source = "both"
        elif photo_rel:
            source = "photo"
        elif audio_rel:
            source = "voice"
        else:
            source = "text"

        entry_id = calorie_db.add_pending(
            update_id=update_id,
            ts_utc=ts_utc,
            raw_text=note,
            photo_path=photo_rel,
            audio_path=audio_rel,
            source=source,
        )
        if entry_id is not None:
            new_pending.append(entry_id)
        else:
            skipped += 1

    # Advance + persist the offset so consumed updates aren't re-fetched.
    if max_update_id is not None and updates:
        _save_offset(max_update_id + 1)

    return {
        "ok": True,
        "fetched": len(updates),
        "new_pending": len(new_pending),
        "skipped_duplicates": skipped,
        "pending_ids": new_pending,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Poll the fitness bot for food messages.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch", help="Fetch new messages and insert pending entries.")
    args = p.parse_args()

    if args.cmd == "fetch":
        print(json.dumps(fetch(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
