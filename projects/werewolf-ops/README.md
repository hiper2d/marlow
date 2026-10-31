# Werewolf-Ops Project

Monitor API budgets across providers, collect gameplay statistics from the Werewolf DB, watch for anomalies. Layered in **after** research and blog projects are stable for ~1-2 weeks.

## State

- **`tasks/`** — YAML task definitions for this project.
- **`reports/`** — daily/weekly reports and aggregated metrics.

## Workstreams

### Budget monitoring

Per-provider plugins under `tools/budget/`. Each plugin implements a common `get_balance()` interface. Some use the provider's native API, some use Marlow's persistent Chrome profile to scrape the dashboard.

Coverage target: OpenAI, Anthropic, Google, Grok (x.ai), DeepSeek, Moonshot, Mistral, z.ai.

Rollout tracked in [`plans/budget-providers.md`](../../plans/budget-providers.md).

Daily check at 9am. Alert via Telegram (`urgency: urgent`) if any provider falls below its configured threshold.

### Statistics — LIVE (v1, since 2026-06-02)

The Werewolf game stores everything in **Firestore** (not SQL — the earlier
"SQL wrapper / read-only SQL user" plan was wrong). `handlers/werewolf_stats.py`
reads the `users` and `games` collections via the **same** read-only service
account `monitor_keys` already uses (`MARLOW_FIREBASE_CREDS`) — no new access
was needed; it was a schema-knowledge gap, not a permissions gap.

Task: [`tasks/werewolf_stats.yaml`](tasks/werewolf_stats.yaml) — daily 09:00 UTC,
digest-only (activity is a trend, not an alarm; the budget watch owns alerts).

v1 query set (`werewolf_stats.py report`, rendered by `show`):

- **New users** — today / 7d / 30d, total, tier split (free/api/paid)
- **Games created** — today / 7d / 30d, total, + how many today were by users
  who signed up today
- **Money spent (AI burn)** — `created_cost_usd` (Σ `totalGameCost` of games
  created per window; a lower bound, grows as games are played) and
  `live_cost_usd` + `daily_burn` (Σ cost across all live ≤30d games; its
  day-over-day delta is the true daily spend). Secondary `user_spend_mtd_usd`
  from `users.spendings` — NOT revenue: `free` is our cost, `api` is users' own
  keys, only `paid` is actual income (~$0 today).

Snapshots persist to `state/stats_latest.json` + `state/stats_history.jsonl`.
**This matters**: games carry a 30-day Firestore TTL (`expireAt`), so without a
daily snapshot history any trend older than a month — and the burn series — is
gone. The history is the long memory.

**Content screen (since 2026-09-19).** The game judges every piece of human
text (chat messages, new-game name/theme/instructions) with Jev before it
reaches an AI provider and writes one row per call to `jevScreenCalls`
(werewolf `app/api/jev-screen.ts`; verdicts `ok` / `grey` / `would_block` /
`error`, a 0–3 risk score, a reason flag). It runs in `monitor` mode first,
recording and rejecting nothing. `werewolf_stats` reads the day's rows with
the same read-only account, prints the counts, every would-block row with an
excerpt, and the day's provider refusals (`games.providerBlocks`) joined with
that game's screened messages. The digest carries one status line every day
(so a screen that stopped running shows as "not instrumented", not as a quiet
day) plus the flagged rows. Those rows are what Alex reads before flipping
`jevScreenMode` in Firestore `config/limits` to `enforce`.

Deferred (the "add more" backlog): DAU/WAU/MAU (only a single
`last_login_timestamp` exists per user — no event log, so these must be
accumulated from daily snapshots, not backfilled), game-completion rate (parse
`gameState == GAME_OVER`/`AFTER_GAME_DISCUSSION`), model/theme popularity,
errors/anomalies, Stripe.

### Anomaly scanning — LIVE (broken-game watch, since 2026-06-02)

`handlers/monitor_health.py` scans the `games` collection for the game's own
`errorState` field (written by `setGameErrorState` when a system error hits a
game). Broken games are thus readable straight from Firestore — no log pipeline.

Task: [`tasks/monitor_health.yaml`](tasks/monitor_health.yaml) — every 6h.
Alerts on games errored **since the last scan** (never the standing pile, which
it baselines on first run): urgent if `recoverable: false`, digest if
recoverable. State in `state/health_latest.json` (+ history). In practice the
errors seen so far are LLM-provider response-parse failures (DeepSeek/Grok JSON,
Mistral/OpenAI schema validation) — a game-reliability signal, not infra.

### Poker with AI watch — LIVE (lane errors + activity pulse, since 2026-10-31)

`handlers/monitor_poker.py` is the same discipline for the second game,
pokerwithai.net, which lives on the SAME Firebase project under `poker_`-prefixed
collections (`poker_games`, `poker_users`) — same read-only service account, no
new cred. Poker keeps one error slot PER LANE on the game doc (`gameError` for
cards/betting/compaction, `chatError` for table talk), so a game-lane error is a
frozen hand (urgent) and a chat-lane error a quiet table (digest). Errors are
keyed `gameId:lane:timestamp`: retry-then-fail-again is new, a cleared error
drops out, the first scan baselines the pile.

Task: [`tasks/monitor_poker.yaml`](tasks/monitor_poker.yaml) — every 6h, offset
3h from monitor_health. Because Poker sees a few tables a MONTH (2026-10-31: 14
live games, 16 users, nobody has played twice), the scan also puts every new
table and signup since the last scan into the digest — the only place Alex sees
a stranger trying it. State in `state/poker_latest.json` (+ history).

App-level logs: `monitor_betterstack.py --app poker` runs the Werewolf
Betterstack scan against Poker's own source — same incident folding and
classes, Poker's field names mapped onto the common shape, a Poker-shaped game
snapshot (two error lanes), its own state (`state/betterstack_poker_*`). Task:
[`tasks/monitor_betterstack_poker.yaml`](tasks/monitor_betterstack_poker.yaml),
every 3h offset 90 min from the Werewolf scan. Poker's tables live in
[`config/betterstack_sources.json`](config/betterstack_sources.json) and are
EMPTY until the source exists (Poker's Vercel deploy had no log token as of
2026-10-31); while empty the scan is a quiet `configured: false` no-op.

### App-level error watch — LIVE (Betterstack logs, since 2026-06-03)

`handlers/monitor_betterstack.py` reads the app's logs back from Betterstack and
catches what `errorState` can't: unhandled exceptions, provider 5xx, Next.js
server errors — failures where the request died before writing a game doc. The
game already ships structured logs to Betterstack via `@logtail/node`
(`BETTER_STACK_SOURCE_TOKEN`, ingest-only; see
`werewolf-client/app/utils/logger.ts`).

Task: [`tasks/monitor_betterstack.yaml`](tasks/monitor_betterstack.yaml) —
every 3 hours with a 4-hour window (hourly / 90 min until 2026-10-23). State in
`state/betterstack_latest.json` (+ history).

**Incidents + analysis (2026-10-23).** The handler folds error/warn lines into
*incidents* (one game, one failure class — `timeout`, `provider_busy`,
`model_refusal`, `free_cap`, … see `CLASSES`), reads the structured fields the
game logs (`gameId`, `model`, `botName`, `function`, the real `error` text and
the stack head), and attaches a read-only Firestore snapshot of the game to every
NEW incident (state, day, error state, last message, owner, tier, models at the
table). The session then does the judgment the YAML's playbook spells out — what
happened, what the player saw, whether it needs Alex — and that text is the
alert. Before this the alert was a dump of raw `message` fields ("Game action
failed: U x2"), and one incident straddling two hourly scans paged twice.

**How we read it.** The app's source token is ingest-only, so reading needs a
separate **ClickHouse query connection** (Telemetry → Integrations → SQL API; the
password shows once on creation). Credentials live in the launchd plist:
`BETTERSTACK_CH_HOST`, `BETTERSTACK_CH_USER`, `BETTERSTACK_CH_PASS`.

**Why an S3 table.** Betterstack Telemetry is ClickHouse with tiered storage:
recent rows in a hot table `remote(<source>_logs)`, older rows flushed to S3
`s3Cluster(primary, <source>_s3)`. The Live-tail UI hides the seam; the raw SQL
API doesn't. For this source the flush is aggressive and the volume tiny, so the
hot table is almost always empty and S3 holds effectively everything — so the
handler queries S3. There's no flat `level` column: each row's `raw` is the full
JSON log line, and level/message come out via `JSONExtractString(raw, …)`.

**Alert model — presence, not rate-spike.** Measured volume is ~tens of lines a
day and the error baseline is *zero*, so statistical spike-vs-baseline is the
wrong tool. We alert on the **presence** of incidents NEW since the last scan
(incident fingerprint = target + failure class; a known incident is forgotten
24h after its last line), never the standing set — same discipline as
monitor_health. First scan baselines (one digest line, no urgent); thereafter a
new incident whose worst line is error-level is urgent, a warn-only one is digest.

**Multi-account clusters in the stats digest (2026-10-23).** `werewolf_stats`
now diffs the device/IP clusters against the previous snapshot and the digest
prints only clusters that *appeared* or *grew* (a new account on a known shared
browser or connection). The standing list is still in the saved report and in
`show`. Alex: "I'm only interested when an attempt is detected, not the full
list all the time." The strongest signal — a free-cap refusal with a device
scope — reaches Betterstack since the same day (the game moved that line from
`console.warn` to its logger), so the log watch sees it as class `free_cap`.

### Community watch - LIVE (Discord activity + behavior, since 2026-06-28)

`handlers/monitor_discord.py` watches the Discord community server "AI Werewolf
and other projects" - the first ops monitor aimed at PEOPLE rather than infra. It
polls the conversational channels (general, general-discussion, ai-news) for
messages new since the last scan (per-channel id cursor), computes activity stats
(server/online counts, per-channel + per-author volume), and applies deterministic
heuristics for the obvious bad-behavior shapes: someone posting too much, repeating
the same message, link floods, mass mentions. The handler is the deterministic half
only; the SESSION reads the returned `sample` of new messages and judges tone
(rude/hostile/pestering) - the part rules can't do. Same handler-gathers /
session-interprets split as the other monitors.

Task: [`tasks/monitor_discord.yaml`](tasks/monitor_discord.yaml) - every 6h
(00/06/12/18 UTC). Bad behavior (heuristic-urgent or the session's tone judgment)
pings Alex urgent; routine activity rolls into the daily digest; a quiet window is
silent. State in `state/discord_latest.json` (+ history); reports to
`reports/discord/<YYYY-MM-DD>.md`.

**Alert model - cursor diff, not rate-spike.** Only messages NEW since the last
scan are examined (per-channel `last_message_ids`). First sight of a channel
baselines it (records the latest id, gathers no history, one digest line) - same
discipline as monitor_health / monitor_betterstack.

**Message Content intent.** Reading other users' message content over REST needs
the privileged Message Content intent (Developer Portal -> Bot -> Privileged
Gateway Intents). If off, non-bot messages come back empty; the handler emits a
`content_intent_off` issue so Marlow tells Alex. Volume/mention floods are still
caught while blind to tone.

## Status

All six workstreams live: **budget** (monitor_keys + scrape_stats, 8
providers), **statistics** (werewolf_stats, daily), **anomaly scanning**
(monitor_health, broken-game watch every 6h), **app-level errors**
(monitor_betterstack, hourly Betterstack log watch), **community watch**
(monitor_discord, Discord activity + behavior every 6h), **Poker with AI**
(monitor_poker, lane errors + new tables every 6h, since 2026-10-31). Next: the
stats "add more" backlog (DAU/WAU/MAU, completion rate, model/theme popularity).
