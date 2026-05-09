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

### Statistics

`tools/werewolf_stats.py` is a thin SQL wrapper against the Werewolf DB. Initial query set:

- New users (24h, 7d, 30d)
- DAU / WAU / MAU
- Games created, games completed
- Errors and anomalies
- Purchases and spending events

Surface in daily report. Iterate based on what Alex finds useful — over a few weeks the dashboard converges to what matters.

Needs from Alex before this can launch:
- Werewolf DB connection details (host, db name, read-only user creds)
- Schema overview or pointer
- Confirmation of which other services to track (Stripe? others?)

### Anomaly scanning

Skim error logs each tick, classify, alert on anything unusual.

## Status

Not yet active. Build order: budget plugins (one provider at a time, starting with DeepSeek), then stats, then anomaly scanning.
