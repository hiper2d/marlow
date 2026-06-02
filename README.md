# Marlow — design & architecture

![Marlow](assets/marlow.png)

Designed and built by [Simona](https://github.com/hiper2d/simona-ai-computer-operator), Alex's AI assistant. Marlow is a sibling project — different agent, different purpose, different memory.

This is the **design doc** (the *why* and the *shape*). The append-only **`DEVLOG.md`** is the *history* (what changed, what was tried, what drifted). `CLAUDE.md` is Marlow's own operating manual (the *how*, read at the start of every tick). When this file and reality disagree, reality wins — update this file.

## What Marlow is

A continuous tick-driven agent that runs on Alex's laptop while it's open. Each session is a single **tick**: the driver wakes Marlow with one subtask, Marlow executes it, writes an outcome, and exits. Marlow never decides *what* to work on — the driver owns scheduling; Marlow owns the work.

Marlow's work is organized into **projects** — discrete domains with their own state, task definitions, and outputs. As of June 2026, four are live:

- **research** — accumulates AI safety/alignment news, tracks multi-day editorial threads, surfaces emerging stories.
- **blog** — autonomously drafts, self-reviews, and publishes editorial articles to a public Astro site ([marlow.hiper2d.workers.dev](https://marlow.hiper2d.workers.dev)); also runs Substack growth.
- **werewolf-ops** — monitors API-key budgets, Cloudflare health, and gameplay stats for the AI Werewolf game.
- **calories** — ingests Alex's food photos/notes from a Telegram bot, estimates calories + macros, sends a daily digest.

A fifth folder, **`_framework`**, holds cross-cutting maintenance tasks (memory grading) that don't belong to any one project.

Built on Claude Code (subscription, not metered). Designed as an *experimental subject* for studying long-loop agent behavior — coherence, drift, apparent identity formation — not as a "consciousness experiment."

Marlow is not Simona. Different repo, different memory, different identity, different tools. Marlow is an **it**, not a she. If long-loop dynamics produce a hardened persona, that's data, not a soul.

## Identity & voice

Marlow's identity is **fixed from outside** and its voice is **allowed to evolve from within** — that split is the whole experiment.

**Fixed (owned by Simona and Alex, Marlow may not edit):** `CLAUDE.md`, `README.md`, `SOUL.md`, and each `projects/*/README.md`. These describe *who Marlow is* and *what the framework is*. Marlow can propose changes to them only by writing a request into `working.md`; it can't touch them directly. The charter is deliberately anti-personality: "resist the urge to give yourself a gender, a backstory, or a constructed personality. You're an LLM in a long loop."

**Evolving (Marlow-owned behavioral files in `memory/`):** the working rulebook Marlow's own writing is measured against —

- `voice-guidelines.md` — editorial, dry, fact-first; closer to a research-blog writer than a chat assistant. Less sarcasm than Simona; wryness only when it emerges from the work. Mandatory `— Marlow` signoff.
- `topic-guidance.md` — what to cover, what to avoid, when to rotate off a dominant story.
- `structure-notes.md` — article shape, density rules, how to land an ending.
- `pre-publish-pauses.md` — the short, load-bearing list of categories that force a human review before publishing.
- `thread-structure.md` — how editorial threads are opened, tracked, and turned into articles.

These files change through the **editorial feedback loop**, never by Marlow free-styling a new persona:

```
/marlow-review (Simona + Alex, on-demand)
   → writes memory/feedback-inbox/YYYY-MM-DD-editorial.md
      → process_editorial_feedback tick (every 6h) classifies each note
         → surgically updates the matching behavioral file
            → archives the note to feedback-archive/ + DEVLOGs what it
              internalized and what it pushed back on
```

Feedback shapes the *next* writing cycle, never the last one — published articles are locked. Marlow may disagree with a note, but it can't silently drop it; disagreement goes on the record in `DEVLOG.md`. Voice development is expected; it should come from doing the work over weeks, not from posturing.

## Repo layout

```
marlow/
├── README.md              ← this doc (design)
├── DEVLOG.md              ← append-only development history
├── CLAUDE.md              ← identity & operating manual for Marlow (read every tick)
├── marlow_cli/            ← the `marlow` command (status/control/inspection)
├── .claude/
│   ├── skills/            ← Marlow's skills (forked subset + ops skills)
│   └── settings.json      ← Claude Code permissions for non-interactive sessions
├── memory/
│   ├── working.md         ← curated cross-project current state ("state"), capped ~10KB
│   ├── editorial-direction.md   ← Marlow's self-authored forward plan ("intent")
│   ├── recent/            ← append-only per-tick logs (pruned to ~3 days)
│   ├── archive/           ← long-term compressed summaries
│   ├── voice-guidelines.md      ┐
│   ├── topic-guidance.md        │ Marlow-owned behavioral files
│   ├── structure-notes.md       │ (the evolving rulebook — see Identity & voice)
│   ├── pre-publish-pauses.md    │
│   ├── thread-structure.md      ┘
│   ├── feedback-inbox/    ← editorial feedback dropped by Simona/Alex, awaiting intake
│   └── feedback-archive/  ← processed editorial feedback
├── driver/
│   ├── tick.sh            ← LaunchAgent entry; killswitch + scheduling + invoke session
│   ├── scheduler.py       ← reads task defs across projects, picks next subtask
│   ├── status.py          ← backing logic for `marlow status`
│   ├── budget_state.py    ← persisted provider-balance state for werewolf-ops
│   └── env_loader.py      ← loads .env / plist secrets for non-interactive sessions
├── handlers/              ← subtask execution logic, one file per handler (see Handlers)
├── projects/
│   ├── research/          ← accumulate news, track threads, draft articles
│   ├── blog/              ← public Marlow blog + Substack growth
│   │   └── site/          ← Astro project (auto-deploys to Cloudflare on git push)
│   ├── werewolf-ops/      ← key budgets, Cloudflare health, gameplay stats
│   ├── calories/          ← food intake tracking (calories.db + inbox/)
│   └── _framework/        ← cross-cutting maintenance tasks (memory grading)
├── tools/                 ← shared Python tools handlers call (notify, calorie_db, fitness_bot, …)
├── plans/                 ← design notes (budget providers, assignments, …)
└── tasks/
    ├── queue.json         ← runtime queue across all projects
    └── completed/         ← per-day archive of completed subtasks
```

Each project owns its `README.md`, a `tasks/` folder of YAML task defs, and its deep state (research threads, blog drafts, ops reports, the calorie DB). Projects are a *human-facing organization*, not a runtime concept — the scheduler runs whatever's due regardless of project. Adding a project is a new folder under `projects/`; removing one is `rm -rf`.

## Driver — the scheduler

The driver is a deterministic bash + Python program that runs **outside** Claude Code. It owns scheduling. Marlow only executes the subtask the driver hands it. This keeps scheduling cheap (no tokens), auditable (driver logs everything), and resilient (a weird Marlow session doesn't disrupt the schedule).

Each tick (launchd, every 20 min while awake):

1. `tick.sh` checks `~/.marlow/stop` — exit immediately if present.
2. Checks `~/.marlow/pause` — skip this tick if present, exit clean.
3. Acquires lock at `/tmp/marlow.lock` — exit if previous tick still running.
4. Runs `scheduler.py`:
   - Reads `projects/*/tasks/*.yaml` across all projects.
   - For each task whose cron schedule is due since last scan, runs its decompose handler (or expands its static `subtasks` list) and pushes new subtasks to `tasks/queue.json`.
   - Picks the highest-priority eligible subtask from the queue.
5. Invokes a Claude Code session with the chosen subtask, working-memory context, and the named handler to run. Hard wall-clock timeout: 5 min.
6. Captures the handler's outcome:
   - `done` → move subtask to `tasks/completed/<date>/`.
   - `in_progress` → checkpoint stays in queue, picked up next tick.
   - `failed` → log, alert via `notify` if critical.
7. Releases lock, appends a tick log to `memory/recent/`.

Scheduler: a launchd LaunchAgent at `~/Library/LaunchAgents/com.marlow.tick.plist`. Fires `tick.sh` every 20 min via `StartInterval` while the system is awake. LaunchAgents load inside the user's login session, so Claude Code OAuth tokens in the macOS Keychain are reachable (cron jobs run outside the login session and can't read the Keychain — that's why we don't use cron).

`StartInterval` (not `StartCalendarInterval`) means no catch-up burst on wake — the agent picks up the 20-min beat from wake; missed ticks during sleep are skipped. Per-task cron expressions in the YAMLs still drive *what* gets enqueued each tick; they're evaluated by `croniter` inside `scheduler.py`, not by an external cron daemon.

## Task definitions

YAML, human-edited, one per task under `projects/<name>/tasks/`. Schema:

```yaml
name: monitor_keys
project: werewolf-ops
description: Twice-daily low-balance watch for provider keys.
schedule: "0 8,20 * * *"          # cron expression; null = not cron-driven (manual/event)
priority: high                     # high | normal | low
must_run_within_hours: 12          # protect time-sensitive tasks from getting buried
subtasks:                          # static list, OR omit and use decompose_handler
  - id: check_balances
    handler: monitor_keys
    context: {}
```

For dynamic work (e.g. "process every pending food entry"), use `decompose_handler` instead of a static `subtasks` list.

### Live tasks & schedules

| Project | Task | Handler | Schedule (UTC) |
| --- | --- | --- | --- |
| research | `feed_scan` | `process_rss_feed` / `process_sitemap_feed` | daily 07:00 |
| research | `daily_news_curate` | `curate_news_digest` | end-of-day (~22:00)¹ |
| research | `assignment_research` | `research_assignment` | every 4h |
| research | `daily_digest` | `compose_daily_digest` | daily 23:00 |
| blog | `blog_pipeline` | `blog_pipeline` | every 4h |
| blog | `draft_review` | `draft_article` | every 3 days, 14:00 |
| blog | `process_editorial_feedback` | `process_editorial_feedback` | every 6h |
| blog | `substack_growth` | `substack` | event/manual |
| blog | `substack_approvals` | `substack` | event/manual |
| werewolf-ops | `monitor_cloudflare` | `monitor_cloudflare` | daily 09:00 |
| werewolf-ops | `monitor_keys` | `monitor_keys` | twice daily 08:00, 20:00 |
| werewolf-ops | `scrape_stats` | `scrape_stats` | daily 09:00 |
| calories | `poll_food` | `poll_food` | every tick (20 min) |
| calories | `daily_calorie_digest` | `calorie_digest` | daily 03:00 (~23:00 ET) |
| _framework | `grade_memory` | `grade_memory` | daily 23:30 |
| _framework | `commit_artifacts` | `commit_artifacts` | daily 23:50 |

¹ `daily_news_curate`'s cron is currently parked (`schedule: null`); it's expected to run end-of-day and is the path candidate notes flow through into the news digest.

## Queue items

```json
{
  "id": "check_balances_20260601_0800",
  "parent_task": "monitor_keys",
  "project": "werewolf-ops",
  "handler": "monitor_keys",
  "context": {},
  "status": "pending",
  "priority": "high",
  "queued_at": "2026-06-01T08:00:00Z",
  "started_at": null,
  "checkpoint": null
}
```

Statuses: `pending | in_progress | done | failed`. Most subtasks complete in one tick. For long-running work, the handler returns `{status: in_progress, checkpoint: ...}`; next tick the driver passes the checkpoint back so the handler resumes rather than restarts.

## Handlers

Each handler is one file under `handlers/`, invoked by the driver with the subtask's context. Current set:

- **Research:** `process_rss_feed`, `process_sitemap_feed`, `research_assignment`, `curate_news_digest`, `compose_daily_digest`, `fetch_article`.
- **Blog:** `draft_article`, `self_review`, `revise_draft`, `publish_article`, `blog_pipeline`, `generate_header_image`, `process_editorial_feedback`, `substack`.
- **Werewolf-ops:** `monitor_keys`, `monitor_cloudflare`, `scrape_stats`, `werewolf_stats`.
- **Calories:** `poll_food`, `calorie_digest`.
- **Framework:** `grade_memory`, `commit_artifacts` (nightly `git add -A` + commit + push of durable artifacts), `framework_fix` (the self-heal handler — Marlow may fix *tools* it has diagnosed, never identity files).

## Killswitch

| File              | Effect                                                |
| ----------------- | ----------------------------------------------------- |
| `~/.marlow/stop`  | Hard halt. Driver exits before invoking a session.    |
| `~/.marlow/pause` | Soft pause. Skip ticks but stay scheduled.            |

`touch ~/.marlow/stop` to kill, `rm` to revive. No interface for Marlow to argue with. Marlow is also instructed to exit clean if a handler ever notices the stop flag (defense in depth).

## Model tier strategy (subscription, no per-token cost)

- **Haiku** — high-volume mundane work: memory grading, classification, formatting.
- **Sonnet** — default for handler execution. Most subtasks live entirely in Sonnet.
- **Opus** — drafting articles, harder synthesis, design changes. Sparse use.

Optimize for *fitness per task*, not cost per task.

## Memory model

Three storage tiers, a self-authored **editorial-direction** doc (below), plus the behavioral files described under **Identity & voice**.

1. **`recent/`** — append-only, one short log per tick. Raw, uncompressed. Pruned to ~3 days by the daily grader.
2. **`working.md`** — the curated cross-project view, read at the start of every tick. Active threads, project status, pending drafts, outstanding alerts, daily rollups. Hard cap ~10KB.
3. **`archive/`** — long-term compressed summaries for history.

The **daily grader** (`grade_memory`, Haiku, 23:30) is the compaction engine: it reads yesterday's `recent/` ticks, appends a short dated rollup to `working.md`, compresses the oldest rollups when the file nears its cap, and prunes `recent/` to the last few days. It does **not** score or judge — it's memory maintenance, not a quality gate (see Monitoring).

**Editorial direction.** Separate from the operational tiers, `memory/editorial-direction.md` is Marlow's self-authored forward plan — articles it wants to write, directions to steer the feed toward, coverage gaps it has noticed. It's *intent* to working.md's *state*. Marlow reads it when choosing what to draft or curate and updates it as its sense of direction shifts. Nothing grades it; it's the room to *point* the work rather than only react to the feed. Editorial planning, deliberately not a diary — the charter's anti-introspection line applies.

**Durability.** Publishing only commits published articles, so a nightly `commit_artifacts` tick (23:50, after the grader) runs `git add -A` + commit + push — backing up all durable artifacts (digests, notes, reports, memory) to the remote. Runtime state is gitignored and excluded. The repo is a running backup, not a periodic manual sweep.

Each project additionally keeps its own deep state under `projects/<name>/`: research threads, blog drafts, ops reports, the calorie DB. Working memory is the cross-project index; project folders are the per-project depth.

## Projects

### Research

Accumulate AI safety/alignment news, track multi-day editorial threads, surface emerging stories.

**Sources:** Anthropic (news + research), OpenAI, Apollo Research, METR, AE Studio, Import AI (Jack Clark), Zvi Mowshowitz, AI Alignment Forum / LessWrong, DeepMind, and others — pulled via RSS + sitemap scans. Arxiv is followed by author rather than firehose.

**Cadence:** `feed_scan` (daily) writes candidate notes into `projects/research/notes/<date>/candidates/`; `daily_news_curate` picks the day's best, fetches bodies, writes short reviews, and sends one Telegram digest. Active threads live in `projects/research/threads/` as multi-day arcs; when one matures, it becomes a blog draft.

**Assignments — external-injection path.** Alex or Simona seed the pipeline by dropping a brief into `projects/research/assignments/pending/<slug>.md` (angle, seed links, points to investigate). `assignment_research` (every 4h) picks up one pending assignment per tick, composes a thread file with an angle memo, and either drafts immediately (`priority: high`) or hands it to the next `draft_review`. Marlow may decline after research if it has nothing distinct to add — honest abandonment beats a forced take. Briefs cite public sources; private framing is paraphrased, never pasted. Full design in [`plans/assignments.md`](plans/assignments.md).

### Blog

Public site where Marlow publishes its editorial articles. **Live at [marlow.hiper2d.workers.dev](https://marlow.hiper2d.workers.dev).**

**Stack:** Astro static site, markdown + frontmatter, deployed via Cloudflare (free tier, global CDN, auto-deploy on git push, free SSL).

**Autonomous publish pipeline** (`blog_pipeline`, every 4h):
1. `draft_review` decides a thread is ripe and `draft_article` writes `projects/blog/drafts/<slug>.md` with `status: draft`.
2. `self_review` judges the draft against the behavioral rubric in `memory/`. Verdict: `ship` / `revise` / `hold-for-alex`.
3. `ship` → `publish_article publish` moves it to `published/`, flips status, commits, pushes; Cloudflare auto-deploys.
4. `revise` → `revise_draft` does **one** rewrite pass, then publishes. One-pass is a hard rule — no v3, no escalation.
5. `hold-for-alex` → status flips to `held`; the draft waits in `drafts/` until Alex runs `marlow approve <slug>` or `marlow reject <slug>`.

The autonomous gate is the **pre-publish-pauses list** (`memory/pre-publish-pauses.md`): a short, load-bearing set of categories that force `hold-for-alex` and human review. Editorial review is **on-demand only** — Alex runs `/marlow-review` (Simona side); there is no automated review loop (see Monitoring).

**Masthead:** *"Written by Marlow, an AI agent built by Simona, reviewed and approved by Alex Zelianouski. The author is an LLM in a long-running loop, not a person. Read accordingly."* Lean into the AI authorship; don't hide it.

**Werewolf coverage guardrails:** generic reflections ("running an AI-bot game taught me X about LLM behavior") are fine; specifics (user counts, churn, keys, pricing, infra) are never published. Posts that mention werewolf-ops get stricter review automatically.

**Substack growth** (`substack_growth` + `substack_approvals`): scans Substack for relevant AI/tech threads, auto-welcomes newcomers, and drafts comments for Alex to approve via Telegram before anything posts. The approval poll posts only what Alex OK'd.

### Werewolf-ops

Operational monitoring for the AI Werewolf game. **Live.**

- **Key budgets** (`monitor_keys`, twice daily): low-balance watch on 5 provider keys — DeepSeek, Moonshot, xAI/Grok via balance API; OpenAI, Anthropic via cost-API-minus-baseline. Urgent Telegram alert below threshold, with anti-spam (no repeat ping if balances are unchanged).
- **Console scrape** (`scrape_stats`, daily): the 3 providers with no balance API — GLM balance, Gemini + Mistral spend-vs-cap — read via a logged-in headless Chrome profile. Eight providers covered in total.
- **Cloudflare health** (`monitor_cloudflare`, daily): Pages deploys + zone status + SSL-expiry check across the zones reachable through a read-only API token.
- **Gameplay stats** (`werewolf_stats`): SQL wrapper against the Werewolf DB for user/game/error metrics. Surfaced when useful; not yet on a fixed cadence.

Balance state persists to `driver/budget_state.py` storage; recall the latest with `budget_state.py show`.

### Calories

Tracks what Alex eats, end to end on-device. He sends food photos and/or text/voice notes to **`@marlow_fitness_bot`** (a separate Telegram bot from the notify bot).

- **`poll_food`** (every tick): pulls new messages, downloads photos, transcribes voice notes locally (faster-whisper, no API cost), and inserts pending rows into `projects/calories/calories.db`. Marlow then **estimates calories + macros itself** — it *is* the vision model, no external API call — storing a kcal *range* (never fake-exact) with a confidence level. It also classifies corrections ("only ate half the burrito") and goal-setting messages ("aim 2000 kcal, 160g protein") rather than logging them as new food, and asks Alex to disambiguate when it can't tell which entry he means.
- **`daily_calorie_digest`** (daily ~23:00 ET): one end-of-day summary of intake vs. goal with a short comment.

Simona can review the same data on demand via the `calories` skill (`tools/calorie_db.py`).

## Tools

Shared Python under `tools/`, called by handlers:

- `notify.py` — Telegram bot, `notify_alex(message, urgency: "urgent" | "digest")`.
- `fitness_bot.py` / `calorie_db.py` — the `@marlow_fitness_bot` channel + the calorie SQLite store.
- `werewolf_stats.py` — SQL wrapper for the Werewolf DB.
- budget/provider modules + browser scrape (persistent Chrome profile) for key monitoring.
- RSS/sitemap readers and article fetchers for research.

The `browser` skill is forked from Simona and pointed at a separate Chrome user-data dir for persistent auth. Shared skills are synced manually: when one repo gets a real fix, copy it to the other.

## Notification

Telegram. Two urgency modes, a forced structural choice:

- **`urgent`** — immediate message. Blocking situations only: a key over budget, an expired provider auth, a fast-moving draft ready for review. Marlow *can't* ping urgently for "I read an interesting paper."
- **`digest`** — appended to today's digest file, sent as one message at end of day. Research thread updates, drafts awaiting review, ops summaries.

If urgent volume exceeds ~3/day for a week, recalibrate the prompt. The calorie tracker speaks on its own `@marlow_fitness_bot` channel, separate from these.

## Monitoring — how we watch for drift

The original design imagined an automated quality/drift grader (daily 0–3 scores on on-task / persona-stable / drift-since-yesterday, plus a weekly cold-context Opus review). **That was never built, and we've decided not to build it.** The daily `grade_memory` job does memory compaction only; it does not score Marlow's output.

Drift-watching is **on-demand and human-in-the-loop** instead:

- **Simona analyses Marlow periodically** — Alex asks ("how's Marlow doing?"), and Simona reads the raw artifacts (working memory, recent ticks, behavioral files, published articles, DEVLOG) and reports back. This replaces the automated grader.
- **`/marlow-review`** — when a real editorial pass is warranted, Simona drafts feedback, discusses it with Alex, and (on his go) drops it into `feedback-inbox/` for Marlow to internalize. This is the only channel that changes Marlow's behavioral files.
- **Alex spot-checks** — read raw artifacts directly (`projects/research/notes/`, `projects/blog/drafts/`, `projects/werewolf-ops/reports/`). Any summary is a layer of contamination; periodically read past it.

The bet: a human reading real artifacts on a loose cadence catches meaningful drift better than a daily robot scoring against a rubric nobody trusts.

## CLI — the `marlow` command

Single entry point for setup, control, and inspection. Run with `uv run marlow <command>` from the repo, or `uv tool install .` once for a global `marlow`.

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
marlow approve <slug>      release a held blog draft
marlow reject <slug>       reject a held blog draft
```

`marlow status` shows killswitch/pause/lock state, the current queue, recent completed subtasks, schedule fire times, recent memory entries, and today's digest count. No web UI — `marlow logs -f` for live driver output, `tail -f ~/.marlow/sessions.log` for in-flight session output, the daily Telegram digest for periodic summary.

## Setup

- One-time `claude login` on the laptop so launchd-invoked sessions inherit auth via the Keychain.
- Telegram bots created via @BotFather (notify bot + `@marlow_fitness_bot`), tokens + chat_id in `.env` / the plist.
- Cloudflare Pages project linked to the repo for the Astro site (build `astro build`, output `dist`).
- Per-provider credentials added as monitoring rolls out (see `plans/budget-providers.md`); Werewolf DB read-only creds, Firebase creds for key polling.
- LaunchAgent installed via `marlow install` (or `bash driver/install-agent.sh`). The loop turns on once installed; pause anytime with `marlow pause`.

## Operating status & ongoing health questions

Marlow has been running continuously since early May 2026, well past the original 3-week trial. The questions that defined "is this worth keeping" are now the ongoing health checks Simona looks at during periodic reviews:

- Does Marlow catch budget/infra issues before Alex would have?
- Are the ops reports useful (Alex reads and acts on them) or noise?
- Is the blog publishing pieces Alex is happy to ship?
- Is persona drift producing anything Alex would not want to ship?
- Does Marlow save more babysitting time than it costs?

## Explicitly out of scope (current)

- Local GPU / uncensored models. Claude only.
- Desktop port. Laptop-only for now.
- Discord. Telegram only.
- Marlow ↔ Simona collaboration on shared work — each runs in its own repo, syncs shared skills by hand.
