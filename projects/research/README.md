# Research Project

Marlow reads her sources, explores the open web, and sends Alex the news she finds worth his time. What she reads and follows is her call (2026-11-07): the source list is hers, and so is the daily exploration. Her findings are one place her weekly blog piece can come from, never a requirement.

## State

- **`tasks/`** - YAML task definitions (`feed_scan`, `explore`, `daily_news_curate`, `daily_digest`, `monitor_models`).
- **`feeds/`** - her source list and its machinery:
  - `sources.yaml` - the list `feed_scan` expands, one scan per source. Hers to change, only through `tools/sources.py`.
  - `proposals.yaml` - changes the `explore` tick (no shell) wants; `tick.sh` runs `sources.py apply` once a day.
  - `sources-log.md` - every add/remove, applied or refused, with the reason.
  - `state.json` - per-feed last-seen state (runtime, gitignored).
- **`notes/`** - per-tick notes. Feed scans and `explore` both write candidates into `notes/<date>/candidates/`.
- **`explorations/`** - what the `explore` tick learned: the question, what she found (with links), what she now thinks.
- **`article-ideas/`** - news picks Alex flagged (via `crosspost` reply-matching) that he wants to write about himself. Simona reads this folder when Alex asks "anything from Marlow's findings?".
- **`archive/`** - retired 2026-11-07: the old research threads, `thread-structure.md`, and the assignment briefs. Kept for reference; nothing reads them.

## Sources

`feed_scan` reads `feeds/sources.yaml`. It started (May 2026) with Anthropic (news + research), Apollo Research (science + blog), METR, AE Studio, Import AI, Zvi Mowshowitz, the AI Alignment Forum and LessWrong. From 2026-11-07 Marlow adds and drops sources herself (cap 15, each costs a tick a day). `tools/sources.py` refuses anything that isn't a public http(s) host or doesn't parse as a feed.

Model releases come from the providers' own APIs, not from feeds: `monitor_models` (ops profile) diffs the model lists of the 12 providers Alex uses and sends new releases to the news chat.

## Web access

Only the `explore` tick has `WebSearch` / `WebFetch`, and it runs sandboxed (`context.web: true` -> `driver/tick.sh`): no Bash, project settings not loaded, reads limited to her own areas with the repo's secrets denied, writes limited to notes, explorations, her notebooks and `proposals.yaml`. Every web call, including refused ones from any other tick, is logged by `driver/log_web_access.py` to `~/.marlow/writer/web-access.jsonl`; `monitor_self` flags any attempt outside the sandbox.

## Cadence

| Task | Schedule (UTC) | What it does |
| --- | --- | --- |
| `feed_scan` | daily 07:00 | One scan per source in `feeds/sources.yaml`; candidate notes into `notes/<date>/candidates/`. |
| `explore` | daily 15:00 | Open-web exploration (sandboxed): a curiosity, news beyond the list, primary sources. Writes candidates, explorations, notebook entries, source proposals. |
| `daily_news_curate` | daily 22:00 | Pick the day's best 3-5 candidates (feed + explore), fetch bodies, write short takes, send **each pick as its own Telegram message**. |
| `monitor_models` | every 2h at :15 | Ops profile. Diff the provider model lists; send real new models to the news chat. |
| `daily_digest` | daily 23:00 | Assemble today's digest file and send it to Alex via Telegram. |
