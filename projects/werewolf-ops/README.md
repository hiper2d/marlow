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
  day-over-day delta is the true daily spend). Secondary `revenue_mtd_usd` from
  `users.spendings`.

Snapshots persist to `state/stats_latest.json` + `state/stats_history.jsonl`.
**This matters**: games carry a 30-day Firestore TTL (`expireAt`), so without a
daily snapshot history any trend older than a month — and the burn series — is
gone. The history is the long memory.

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

### App-level error watch — LIVE (Betterstack logs, since 2026-06-03)

`handlers/monitor_betterstack.py` reads the app's logs back from Betterstack and
catches what `errorState` can't: unhandled exceptions, provider 5xx, Next.js
server errors — failures where the request died before writing a game doc. The
game already ships structured logs to Betterstack via `@logtail/node`
(`BETTER_STACK_SOURCE_TOKEN`, ingest-only; see
`werewolf-client/app/utils/logger.ts`).

Task: [`tasks/monitor_betterstack.yaml`](tasks/monitor_betterstack.yaml) —
hourly. State in `state/betterstack_latest.json` (+ history).

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
wrong tool. We alert on the **presence** of error/warn lines NEW since the last
scan (fingerprint dedup), never the standing set — same discipline as
monitor_health. First scan baselines (one digest line, no urgent); thereafter a
new error line is urgent, a new warn is digest.

## Status

All four workstreams live: **budget** (monitor_keys + scrape_stats, 8
providers), **statistics** (werewolf_stats, daily), **anomaly scanning**
(monitor_health, broken-game watch every 6h), **app-level errors**
(monitor_betterstack, hourly Betterstack log watch). Next: the stats "add more"
backlog (DAU/WAU/MAU, completion rate, model/theme popularity).
