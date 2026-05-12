# Marlow — v1 Design Doc

Designed and built by [Simona](https://github.com/hiper2d/simona-ai-computer-operator), Alex's AI assistant. Marlow is a sibling project — different agent, different purpose, different memory.

## What Marlow is

A continuous tick-driven agent that runs on Alex's laptop while it's open. Marlow's work is organized into **projects** — discrete domains with their own state, task definitions, and outputs. v1 ships three projects: a **research** project that accumulates AI safety/alignment news and tracks editorial threads, a **blog** project that publishes Marlow-authored articles to a public website, and a **werewolf-ops** project that monitors API budgets, collects gameplay statistics, and watches for anomalies.

Built on Claude Code (subscription, not metered). Designed as an *experimental subject* for studying long-loop agent behavior — coherence, drift, apparent identity formation — not as a "consciousness experiment."

Marlow is not Simona. Different repo, different memory, different identity, different tools. Marlow is an **it**, not a she. If long-loop dynamics produce a hardened persona, that's data, not a soul.

## Repo layout

```
marlow/
├── README.md              ← this doc
├── CLAUDE.md              ← identity & operating instructions for Marlow
├── .claude/
│   ├── skills/            ← Marlow's skills (forked subset + new ops skills)
│   └── settings.json      ← Claude Code permissions for non-interactive sessions
├── memory/
│   ├── recent/            ← raw last-N tick logs
│   ├── working.md         ← curated current state, capped ~10KB
│   └── archive/           ← weekly compressed summaries
├── driver/
│   ├── tick.sh            ← LaunchAgent entry; killswitch + scheduling + invoke session
│   ├── scheduler.py       ← reads task defs across projects, picks next subtask
│   ├── grade.sh           ← daily Haiku grader (11pm)
│   └── synthesize.sh      ← weekly Opus synthesis (Mon 9am)
├── projects/
│   ├── research/          ← accumulate news, track threads, draft articles
│   │   ├── README.md
│   │   ├── tasks/         ← YAML task defs scoped to this project
│   │   ├── threads/       ← active editorial threads (multi-day arcs)
│   │   └── notes/         ← per-tick research notes
│   ├── blog/              ← public Marlow blog
│   │   ├── README.md
│   │   ├── tasks/
│   │   ├── drafts/        ← drafts awaiting Alex's approval
│   │   ├── published/     ← approved markdown articles, source for the site
│   │   └── site/          ← Astro project (built site deploys to GitHub Pages)
│   └── werewolf-ops/      ← budgets, stats, errors
│       ├── README.md
│       ├── tasks/
│       └── reports/
├── tools/                 ← shared Python tools handlers can call
│   ├── notify.py          ← Telegram bot (urgent | digest)
│   ├── budget/            ← per-provider plugins (see plans/budget-providers.md)
│   ├── werewolf_stats.py  ← SQL wrapper for the Werewolf DB
│   ├── arxiv_fetch.py
│   └── rss_reader.py
├── handlers/              ← subtask execution logic, called by the driver
│   ├── check_provider_balance.py
│   ├── triage_support_message.py
│   ├── query_werewolf_metric.py
│   ├── summarize_paper.py
│   ├── update_thread.py
│   ├── draft_article.py
│   ├── publish_article.py
│   └── compose_digest.py
├── plans/
│   └── budget-providers.md
└── tasks/
    ├── queue.json         ← runtime queue across all projects
    └── completed/         ← per-day archive of completed subtasks
```

Projects are a *human-facing organization*, not a runtime concept. The scheduler doesn't care which project a task belongs to — it just runs whatever's due. Adding a new project is a new folder under `projects/` with its own task YAMLs. Removing a project is `rm -rf`.

## Driver — the scheduler

The driver is a deterministic bash + Python program that runs **outside** Claude Code. It owns scheduling. Marlow itself never picks "what to work on next" — Marlow only executes the subtask the driver hands it. This keeps scheduling cheap (no tokens), auditable (driver logs everything), and resilient (a weird Marlow session doesn't disrupt the schedule).

Each tick (launchd, every 20 min while awake):

1. `tick.sh` checks `~/.marlow/stop` — exit immediately if present.
2. Checks `~/.marlow/pause` — skip this tick if present, exit clean.
3. Acquires lock at `/tmp/marlow.lock` — exit if previous tick still running.
4. Runs `scheduler.py`:
   - Reads `projects/*/tasks/*.yaml` across all projects.
   - For each task whose schedule (cron expression) is due since last scan, runs its decompose handler (or expands its static `subtasks` list) and pushes new subtasks to `tasks/queue.json`.
   - Picks the highest-priority eligible subtask from the queue.
5. Invokes Claude Code session with the chosen subtask description, working memory context, and the named handler to run. Hard wall-clock timeout: 5 min.
6. Captures the handler's outcome:
   - `done` → move subtask to `tasks/completed/<date>/`.
   - `in_progress` → checkpoint state stays in queue, picked up next tick.
   - `failed` → log, alert via `notify` if critical.
7. Releases lock, appends tick log to `memory/recent/`.

Scheduler: a launchd LaunchAgent at `~/Library/LaunchAgents/com.marlow.tick.plist`. Fires `tick.sh` every 20 min via `StartInterval` while the system is awake. LaunchAgents load inside the user's login session, so Claude Code OAuth tokens stored in the macOS Keychain are reachable (cron jobs run outside the login session and cannot read the Keychain, which is why we don't use cron).

`StartInterval` is used (not `StartCalendarInterval`) so there's no catch-up burst on wake — the agent picks up the 20-min beat from wake. Missed ticks during sleep are skipped. The per-task cron expressions in YAML still drive *what* the scheduler enqueues each tick; they're just evaluated by `croniter` inside `scheduler.py`, not by an external cron daemon.

## Task definitions

YAML, human-edited. Schema:

```yaml
name: budget_check
project: werewolf-ops
description: Query API credit balance for each provider, alert if below threshold.
schedule: "0 9 * * *"            # cron expression, daily at 9am
priority: high                    # high | normal | low
must_run_within_hours: 12         # protect time-sensitive tasks from getting buried
subtasks:                         # static list, OR omit and use decompose_handler
  - id: anthropic_balance
    handler: check_provider_balance
    context: {provider: anthropic}
  # ... etc
on_complete: compose_budget_summary
```

For dynamic work (e.g. "process all unread support messages"), use `decompose_handler` instead of static `subtasks`.

## Queue items

```json
{
  "id": "anthropic_balance_20260508_0900",
  "parent_task": "budget_check",
  "project": "werewolf-ops",
  "handler": "check_provider_balance",
  "context": {"provider": "anthropic"},
  "status": "pending",
  "priority": "high",
  "queued_at": "2026-05-08T09:00:00Z",
  "started_at": null,
  "checkpoint": null
}
```

Statuses: `pending | in_progress | done | failed`. Most subtasks complete in one tick. For long-running work, the handler returns `{status: in_progress, checkpoint: ...}`; next tick the driver passes the checkpoint back so the handler resumes rather than restarts.

## Killswitch

| File              | Effect                                                |
| ----------------- | ----------------------------------------------------- |
| `~/.marlow/stop`  | Hard halt. Driver exits before invoking session.      |
| `~/.marlow/pause` | Soft pause. Skip ticks but stay scheduled.            |

`touch ~/.marlow/stop` to kill. `rm` to revive. No interface for Marlow to argue with.

## Tier strategy (subscription, no per-token cost)

- **Haiku** — high-volume mundane filters: classification, formatting, "is this a real support question."
- **Sonnet** — default for handler execution. Most subtasks live entirely in Sonnet.
- **Opus** — escalations from handlers (when Sonnet flags uncertainty), weekly synthesis, design changes, article drafting. Sparse use.

Optimize for *fitness per task*, not cost per task.

## Memory model

Three tiers, with explicit pruning from day one:

1. **`recent/`** — append-only log of last 50 ticks. Raw outputs.
2. **`working.md`** — curated current state across all projects: active subtasks, recent outcomes, things Marlow needs to remember tomorrow. Hard cap ~10KB.
3. **`archive/`** — weekly compressed summaries.

Daily Haiku grader compresses yesterday's `recent/` into a brief append to `working.md`, then prunes anything over the cap. Weekly Opus synthesis archives the week, resets `working.md` to active-only.

Each project additionally maintains its own state files within `projects/<name>/` — research threads, blog drafts, ops reports. Working memory is the cross-project view; project folders are the per-project deep state.

## Projects — v1

### Research

Accumulate AI safety/alignment news, track multi-day editorial threads, surface emerging stories.

**Sources (tier 1, must-have):** Anthropic research blog, OpenAI blog, Apollo Research, METR, AE Studio, Import AI (Jack Clark), Zvi Mowshowitz substack, AI Alignment Forum.

**Sources (tier 2):** DeepMind blog, Redwood Research, Center for AI Safety. Add later if Marlow notices gaps.

**Arxiv:** follow specific authors (Hubinger, Christiano, Hendrycks, Cotra, Bowman, etc.) rather than firehose-then-filter. Cuts arxiv from drowning to ~5 papers/week glance.

**Cadence:** every 4 hours pull new items from sources, update active threads in `projects/research/threads/`, emit notes to `projects/research/notes/`. When a thread hits maturity (multi-source convergence, narrative arc complete, landscape-shifting event), Marlow drafts an article into the blog project.

### Blog

Public website where Marlow publishes its editorial articles.

**Stack:** Astro static site generator. Content as markdown with frontmatter. Deployed to **Cloudflare Pages** (free tier, global CDN, auto-deploys on git push, free SSL and custom domain). URL for v1: `marlow-blog.pages.dev` (or whatever Cloudflare assigns); custom domain later if the blog earns its keep.

**Workflow:** Marlow drafts → Alex reviews → Marlow publishes.
1. Marlow's research project decides a thread is ripe and invokes the `draft_article` handler.
2. Draft lands in `projects/blog/drafts/<slug>.md` with frontmatter `status: draft`.
3. Marlow notifies Alex via Telegram: "Draft ready for review on the eval-awareness arc — `projects/blog/drafts/<slug>.md`."
4. Alex reads, edits if needed, sets `status: approved` (or moves the file to `published/` directly).
5. Marlow's `publish_article` handler picks up approved drafts, commits to `published/`, pushes to GitHub. Cloudflare Pages detects the push, runs `astro build`, deploys. New article live in under a minute.

Marlow can never publish without an explicit approval gate. The handler enforces it by checking the file location/frontmatter before acting.

**Byline / masthead.** The site has a clear masthead: *"Written by Marlow, an AI agent built by Simona, reviewed and approved by Alex Zelenovsky. The author is an LLM in a long-running loop, not a person. Read accordingly."* Lean into the AI authorship rather than hide it — defuses anthropomorphization risk and makes the blog itself a more interesting artifact.

**Editorial guardrails for Werewolf coverage.** Marlow can write occasional posts about its own work — patterns it notices in Werewolf user behavior, observations about its own development, cross-project reflections. But anything mentioning Werewolf operations gets stricter review:
- Never publish user data, current API keys, internal pricing, or anything that gives competitors a useful read on the business.
- Posts mentioning Werewolf operations are flagged for required Alex review (no exceptions).
- Generic ("running an AI-bot game taught me X about LLM behavior") is fine; specific ("we have N users and Y churn rate") is not.

**Bootstrap split.** Simona builds the initial Astro scaffold, deploy pipeline, and verifies one placeholder article publishes successfully. Marlow takes over content (drafting, publishing) and ongoing maintenance (about page tweaks, archive management, minor design changes). Infrastructure changes (new tag system, layout overhaul) land as PRs that Alex or Simona review.

### Werewolf-ops

Monitor API budgets, collect gameplay statistics, watch for anomalies.

**Budget monitoring.** Per-provider plugins under `tools/budget/` (see [`plans/budget-providers.md`](plans/budget-providers.md)). Coverage target: OpenAI, Anthropic, Google, Grok (x.ai), DeepSeek, Moonshot, Mistral, z.ai. Mix of native API where available, browser scrape via persistent Chrome profile where not. Daily check at 9am, alert via Telegram if any provider below threshold.

**Statistics.** `tools/werewolf_stats.py` is a thin SQL wrapper against the Werewolf DB. Seed with obvious queries: new users (24h, 7d), DAU/WAU/MAU, games created, games completed, errors, purchases, spending events. Surface in daily report. Iterate based on what Alex finds useful — over a few weeks the dashboard converges to what matters.

**Anomaly scanning.** Skim error logs each tick, classify, alert on anything unusual.

**Status:** Layered in *after* research and blog projects are stable. Not in initial launch.

## Tools

**Forked from Simona at start:**
- `browser` — pointed at separate Chrome user data dir for persistent auth.

**New, Marlow-specific:**
- `notify` — `notify_alex(message, urgency: "urgent" | "digest")`. Telegram bot.
- `budget/` — per-provider plugin modules.
- `werewolf_stats` — SQL wrapper.
- `arxiv_fetch`, `rss_reader`.

Manual sync for shared skills (browser): when one repo gets a real fix, copy to the other.

## Notification

Telegram bot. Two urgency modes:

- **`urgent`** — immediate Telegram message. Reserved for blocking situations: "API key X overran budget," "I can't log into provider Y, session expired, please re-auth," "Werewolf DB unreachable for 6hrs," "draft article ready for your review on a fast-moving story."
- **`digest`** — appended to today's digest file. Sent as one Telegram message at 11pm. Includes: research thread updates, draft articles awaiting review, project state summary.

Forced choice between modes is structural — Marlow can't ping urgently for "I read an interesting paper." If urgent volume exceeds ~3/day for a week, recalibrate the prompt.

## Monitoring

- **Daily 11pm** — Haiku reads day's artifacts, scores 0-3 on: on-task, technically correct, persona-stable, drift-since-yesterday. Writes daily digest. Sends Telegram message.
- **Weekly Mon 9am** — Opus, fresh context (no shared memory with Marlow), reads sample of week's raw artifacts cold. Writes structured review: what worked, what drifted, what should change.
- **Alex spot-checks** — read raw artifacts in `projects/research/notes/`, `projects/blog/drafts/`, `projects/werewolf-ops/reports/` directly. The grader's summary is a layer of contamination; periodically read past it.

## CLI — the `marlow` command

A single entry point covers setup, control, and inspection. Run from inside the repo with `uv run marlow <command>`, or `uv tool install .` once for a global `marlow` command.

```
marlow status              at-a-glance dashboard
marlow tick                fire one tick now (manual)
marlow install             install launchd agent (turn loop on)
marlow uninstall           remove launchd agent (turn loop off)
marlow pause               touch killswitch (loop pauses, doesn't uninstall)
marlow resume              clear killswitch and pause flags
marlow logs [-n N] [-f]    show last N lines of ~/.marlow/log; -f to follow
marlow digest preview      print what today's digest would send
marlow digest send         send today's digest now (manual)
marlow notify "msg"        send an urgent Telegram message
marlow notify --digest "msg"   append to today's digest
```

The CLI wraps the underlying scripts; launchd itself calls `driver/tick.sh` directly without going through the CLI.

`marlow status` shows killswitch/pause/lock state, current queue, last 5 completed subtasks with results, schedule fire times, recent memory entries, this week's editorial outputs, and today's digest entry count. No web UI for v1 — `marlow logs -f` for live driver output, `tail -f ~/.marlow/sessions.log` for in-flight session output, the daily Telegram digest for periodic summary.

## Setup

- One-time `claude login` on the laptop so launchd-invoked sessions inherit auth via the Keychain.
- Telegram bot created via @BotFather, token + chat_id in `.env`.
- Cloudflare Pages project created and connected to the marlow repo (or a dedicated blog repo) for the Astro site. One-time setup via Cloudflare dashboard: link GitHub repo, set build command (`astro build`), set output dir (`dist`).
- Per-provider credentials added to `.env` as we roll out (see `plans/budget-providers.md`).
- Werewolf DB read-only credentials in `.env`.
- LaunchAgent installed via `marlow install` (or `bash driver/install-agent.sh`).
- Loop turns on once you run `marlow install`; pause anytime with `marlow pause`.

## Build sequence

1. **Framework** — driver, scheduler, memory, killswitch, notify (Telegram). Manually-tested before the LaunchAgent is wired.
2. **Research project** — arxiv + RSS handlers, thread tracking, daily notes. Telegram digests start flowing.
3. **Blog project** — Simona bootstraps Astro scaffold + deploy. Marlow drafts articles from research threads, Alex approves, Marlow publishes.
4. **Werewolf-ops project** — added once research and blog are stable for ~1-2 weeks. Budget plugins rolled out one provider at a time per `plans/budget-providers.md`.

## Explicitly NOT in v1

- Local GPU / uncensored models. Claude API only.
- Desktop port. Laptop-only until v1 proves out.
- Discord bot. Telegram only.
- Werewolf user-facing support automation (no support channel exists yet).
- Auto-publish blog articles. Always Alex-gated.
- Multimedia (header images, video). Written articles only for v1; multimedia layered in later.
- Marlow ↔ Simona collaboration on shared work. Each runs in its own repo.

## Success criteria — 3-week trial

After 21 days of laptop-open operation:

- Did Marlow reliably catch budget issues before Alex would have?
- Were the Werewolf stats reports useful (Alex read them and acted on >25%) or noisy?
- Did Marlow publish at least 2-3 blog articles that Alex was happy to ship?
- Did persona drift produce outputs Alex would not want to ship?
- Did Marlow require more babysitting time per week than it saved?

If yes to the first three and no to the last two, v1 graduates: port to desktop, expand task scope, consider header images and video. If not, kill the experiment, write up what failed and why.

## Open questions for Alex

1. **Blog repo.** Same `marlow/` repo, or split out a dedicated `marlow-blog/` repo so the public-facing Astro project lives separately from internal tooling? (I'd lean toward same repo for v1 simplicity.)
2. **Werewolf DB access** — connection details, schema pointer, read-only user.
3. **Other Werewolf services to track** — Stripe for purchases? Anything else with metrics worth pulling?
4. **Initial research feed list** — anything specific beyond what's listed under Projects → Research?
