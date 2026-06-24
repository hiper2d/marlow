# calories — Alex's calorie tracker

A Marlow project. Alex sends photos, text notes, and/or **voice notes** of what he eats and
drinks to the Telegram bot **@marlow_fitness_bot** throughout the day.
Voice notes are transcribed locally (faster-whisper) at ingest, so they
flow through the same path as a typed note.
Marlow pulls them every tick, estimates calories + macros (protein /
carbs / fat), stores each entry, and sends a morning-after digest of the
prior day back to the same chat. Simona queries the same DB when Alex wants to talk through
the numbers.

This is **not** a food scale. Calorie estimates from a photo are noisy —
portion size is the dominant error, not food identification. So estimates
are stored as a **low/high kcal range**, and a text note ("chicken ~200g,
cup of rice") is treated as stronger evidence than the photo alone. The
tool is for *trends* — is the weekly average drifting up? — not clinical
accuracy.

## Pieces

| File | Role |
|------|------|
| `tools/fitness_bot.py` | Telegram client for @marlow_fitness_bot (receive + send). Sole `getUpdates` consumer for this bot. |
| `tools/transcribe.py`  | Local speech-to-text (faster-whisper) for voice notes. No API cost. Model via `CALORIE_WHISPER_MODEL` (default `small`, multilingual). |
| `tools/calorie_db.py`  | SQLite store (`calories.db`). One row per entry, grouped by Alex's local day (Eastern). Also Simona's query surface. |
| `handlers/poll_food.py` | Every tick: fetch new messages, download photos + voice notes, transcribe voice, insert **pending** rows, advance the Telegram offset. Photos of one multi-photo send (shared Telegram `media_group_id`) fold into a single entry (`extra_photos`) so an album of one meal isn't counted twice. |
| `handlers/calorie_digest.py` | Morning after (12:00 UTC ≈ 07:00 ET): roll up the prior fully-closed day, Marlow comments, send to the chat. |

## Data flow

```
Alex → @marlow_fitness_bot (photo / text / voice)
   │
   ▼  every tick
poll_food fetch ──► pending rows in calories.db  (+ photo/voice in inbox/)
   │                 (voice notes transcribed locally → raw_text)
   │
   ▼  same tick, Marlow's session
read photo(s) + note → estimate → calorie_db estimate (or dismiss if not food)
   (photo_path + every path in extra_photos = the one meal, all angles)
   │
   ▼  morning after (≈7am ET, prior day closed)
calorie_digest due → summary → Marlow writes comment → send → digests row
```

## Storage notes

- `entries.status`: `pending` (ingested, not yet estimated) → `estimated`
  (counts toward totals), `dismissed` (not food — greeting, chatter, or a
  correction instruction once applied), or `voided` (logged then retracted —
  "scratch the pizza"). Only `estimated` counts.
- **Corrections**: Alex just messages the bot in plain language ("that coffee
  was small", "only ate half", "scratch the pizza", "forgot — oatmeal this
  morning"). Marlow matches it to the target entry and re-runs `estimate` with
  `--reason` (or `void`), confirming first if it's ambiguous. The prior values
  are snapshotted into the `amendments` JSON column — corrections never
  silently overwrite history. Works for today and past days; a correction to an
  already-digested day triggers a short follow-up message.
- **Goals**: Alex sets a target by messaging the bot in plain language
  ("I'm 185, cutting to 175, aim 2000 kcal and 160g protein"). Marlow
  classifies it as goal-setting, extracts the structured fields, and stores
  it via `set-goal` (inferring kcal/protein if Alex gave only weight +
  intent, and noting what was inferred). Goals live in their own `goals`
  table, append-only: each `set-goal` supersedes the prior active row, so
  the latest `active` row is "the goal now" and history is kept. Weight is a
  **snapshot** taken when the goal was set — there's no weigh-in time series.
  The nightly digest comments the day against the active goal (kcal range vs
  `kcal_target`, protein vs `protein_target_g`); with no goal set it's the
  plain digest. "Drop the goal" → `clear-goal`.
- kcal stored as `kcal_low` / `kcal_high`. Totals sum the ranges.
- `update_id` is UNIQUE — re-running a fetch never double-counts.
- Days are grouped by `local_date` (America/New_York; override `CALORIE_TZ`).
- `calories.db`, `inbox/` (photos), and `state/` (poll offset) are
  gitignored — personal + regenerable, not source.

## Querying (Simona, or Alex via Simona)

```
uv run python tools/calorie_db.py day [--date YYYY-MM-DD]   # includes active goal
uv run python tools/calorie_db.py recent --days 7
uv run python tools/calorie_db.py range --start YYYY-MM-DD --end YYYY-MM-DD
uv run python tools/calorie_db.py goal                      # current goal (or null)
```

## Credentials

`.env` (gitignored): `MARLOW_FITNESS_BOT_TOKEN`, `MARLOW_FITNESS_CHAT_ID`.
Distinct from the ops/notify bot so food traffic stays off the alert channel.
