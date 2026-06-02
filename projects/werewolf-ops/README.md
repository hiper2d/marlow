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

### Anomaly scanning

Skim error logs each tick, classify, alert on anything unusual.

## Status

Not yet active. Build order: budget plugins (one provider at a time, starting with DeepSeek), then stats, then anomaly scanning.
