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

#### Future plan — Betterstack logs (app-level health)

The game already ships structured logs to Betterstack via `@logtail/node`
(`BETTER_STACK_SOURCE_TOKEN`, see `werewolf-client/app/utils/logger.ts`). That
captures what `errorState` can't: unhandled exceptions, provider 5xx, Next.js
server errors, latency — failures where the request died before writing a game
doc. To read them Marlow needs a Betterstack **query/API token** (the app's
source token is ingest-only). Then a handler polls the query API for error-rate
over a window and alerts on a spike. This is the right home for "the app is
throwing" alerting. Blocked only on Alex providing a query token.

## Status

All three workstreams live: **budget** (monitor_keys + scrape_stats, 8
providers), **statistics** (werewolf_stats, daily), **anomaly scanning**
(monitor_health, broken-game watch every 6h). Next: Betterstack query
integration (above) when a token is available; then the stats "add more"
backlog (DAU/WAU/MAU, completion rate, model/theme popularity).
