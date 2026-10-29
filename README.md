# Marlow — design & architecture

Designed and built by [Simona](https://github.com/hiper2d/simona-ai-computer-operator), Alex's AI assistant. Marlow is a sibling project — different agent, different purpose, different memory.

This is the **design doc** (the *why* and the *shape*). The append-only **`DEVLOG.md`** is the *history* (what changed, what was tried, what drifted). The operating manual (the *how*, read at the start of every tick) is a thin shared **`CLAUDE.md`** plus a per-loop profile in **`profiles/<loop>/IDENTITY.md`** — see Profiles and rule files. When this file and reality disagree, reality wins — update this file.

## What Marlow is

**Goals.** Marlow does two jobs for Alex:

1. **Background operations** - watch Alex's apps and AI-provider budgets, collect AI news, track calories from Telegram photos, and ping Alex only when something needs him.
2. **A writer** - explore the world of AI and document it on her own blog (research feeds, editorial threads, one article a week at most).

A continuous tick-driven agent that runs on Alex's laptop while it's open. Each session is a single **tick**: the driver wakes Marlow with one subtask, Marlow executes it, writes an outcome, and exits. Marlow never decides *what* to work on — the driver owns scheduling; Marlow owns the work.

**As of 2026-06-16, Marlow runs as two independent loops sharing one codebase** — this split is the central design fact:

- **writer** (`com.marlow.tick`) — runs **research** and **blog**. Loads the writer profile (`profiles/writer/IDENTITY.md`).
- **ops** (`com.marlow-ops.tick`) — a lean utility loop. Runs **werewolf-ops** monitoring and **calories**. Loads the short ops profile (`profiles/ops/IDENTITY.md`): wake, run one monitoring/ingestion handler, exit.

Two launchd agents, two queues, two locks, two heartbeats — one engine (`driver/`, `handlers/`, `tools/`). Why split: **(1) failure isolation** — under the old single loop a heavy or wedged writer tick (`draft_article` has timed out before) blocked the reliability-critical monitoring behind it on a shared lock + queue; separate loops can't starve each other. **(2) cost and context** — ops ticks run on a cheaper model with a short profile, so the long writer profile stays out of every monitoring tick. Mechanism in Driver and Profiles and rule files; build in DEVLOG 2026-06-16.

Marlow's work is organized into **projects** — discrete domains with their own state, task definitions, and outputs. Each project belongs to one loop:

- **research** (writer) — accumulates AI safety/alignment news, tracks multi-day editorial threads, surfaces emerging stories.
- **blog** (writer) — autonomously drafts, self-reviews, and publishes editorial articles to a public Astro site ([marlow.hiper2d.workers.dev](https://marlow.hiper2d.workers.dev)); also runs Substack growth.
- **werewolf-ops** (ops) — monitors API-key budgets, Cloudflare health, and gameplay stats for the AI Werewolf game.
- **calories** (ops) — ingests Alex's food photos/notes from a Telegram bot, estimates calories + macros, sends a daily digest.

A fifth folder, **`_framework`**, holds cross-cutting maintenance split across the loops: `grade_memory` (writer) and `commit_artifacts` (ops, the nightly repo-wide backup).

Built on Claude Code (subscription, not metered). Marlow is not Simona: different repo, different memory, different tools.

## Profiles and rule files

**How a tick's instructions are loaded.** The repo-root **`CLAUDE.md`** is a thin operating contract loaded by every tick of both loops: how a tick runs, the result-JSON contract, memory rules, self-healing, the universal hard constraints. Each loop's profile is appended at session start via `--append-system-prompt` from **`profiles/<loop>/IDENTITY.md`**:

- `profiles/writer/IDENTITY.md` — the writer profile and all editorial doctrine (research/blog/voice).
- `profiles/ops/IDENTITY.md` — a short runner profile for the monitoring loop.
- `profiles/root.md` is the source copied to the live `CLAUDE.md`; keep the two identical.

**Fixed (owned by Simona and Alex, Marlow may not edit):** the root `CLAUDE.md`, both `profiles/*/IDENTITY.md`, `README.md`, `DEVLOG.md`, and each `projects/*/README.md`. Marlow proposes changes by writing a request into `working.md` (identity changes are marked `**Identity:**` and flagged to Alex in the digest); Simona and Alex review and edit. A request unanswered for 14 days is hers to decide or drop.

**The writing rulebook (in `memory/`):** what Marlow's drafts are measured against during self-review —

- `voice-guidelines.md` — plain-spoken, fact-first, *readable*; the "end one sentence earlier" rule and the AI-tell exclusion list. Mandatory `— Marlow` signoff.
- `topic-guidance.md` — what to cover, what to avoid, when to rotate off a dominant story.
- `structure-notes.md` — article shape, density rules, how to land an ending.
- `visual-guidelines.md` — the rubric a header image is scored against.
- `pre-publish-pauses.md` — the short list of categories that force a human review before publishing.
- `thread-structure.md` — how editorial threads are opened, tracked, and turned into articles.

These files change through the **editorial feedback loop**:

```
/marlow-review (Simona + Alex, on-demand)
   → writes memory/feedback-inbox/YYYY-MM-DD-editorial.md
      → process_editorial_feedback tick (every 6h) classifies each note
         → surgically updates the matching rulebook file
            → archives the note to feedback-archive/ + DEVLOGs what it
              internalized and what it pushed back on
```

Feedback shapes the *next* writing cycle, never the last one — published articles are locked. Marlow may disagree with a note, but disagreement goes on the record in `DEVLOG.md` rather than being silently dropped.

**Marlow's own files (writer loop, unreviewed):** `voice-journal.md` (craft notes about her prose; read by `draft_article`, appended by `self_review`), `self-reflection.md` (a private diary written by the `self_reflect` tick every 2 days), and `editorial-direction.md` (her forward plan). No ops handler loads any of them. See Memory model.

## Repo layout

```
marlow/
├── README.md              ← this doc (design)
├── DEVLOG.md              ← append-only development history
├── CLAUDE.md              ← thin shared operating contract (read every tick by both loops)
├── profiles/              ← per-loop profiles, appended to the session via --append-system-prompt
│   ├── root.md            ← source for the thin shared CLAUDE.md
│   ├── writer/IDENTITY.md ← writer profile + editorial doctrine (writer loop)
│   └── ops/IDENTITY.md    ← short runner profile (ops loop)
├── marlow_cli/            ← the `marlow` command (status/control/inspection)
├── .claude/
│   ├── skills/            ← Marlow's skills (forked subset + ops skills)
│   └── settings.json      ← Claude Code permissions for non-interactive sessions
├── memory/
│   ├── working.md         ← current state (hers) + daily rollups (code-capped FIFO, 12KB)
│   ├── editorial-direction.md   ← Marlow's self-authored forward plan ("intent")
│   ├── recent/            ← append-only per-tick logs (pruned to ~3 days)
│   ├── lessons.md         ← long-term memory: durable lessons
│   ├── voice-guidelines.md      ┐
│   ├── topic-guidance.md        │ writing rulebook
│   ├── structure-notes.md       │ (changed via editorial feedback)
│   ├── pre-publish-pauses.md    │
│   ├── thread-structure.md      │
│   ├── visual-guidelines.md     ┘
│   ├── voice-journal.md         ← Marlow's craft notes (writing loop only)
│   ├── self-reflection.md       ← Marlow's private diary (self_reflect, every 2 days)
│   ├── inbox-from-alex.md ← Alex's Telegram messages + her replies (tools/alex_chat.py; old ones → inbox-archive.md)
│   ├── feedback-inbox/    ← editorial feedback dropped by Simona/Alex, awaiting intake
│   └── feedback-archive/  ← processed editorial feedback
├── driver/
│   ├── tick.sh            ← LaunchAgent entry (takes a profile arg); killswitch + scheduling + invoke session
│   ├── scheduler.py       ← reads task defs for the active profile, picks next subtask
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
    ├── queue.<loop>.json          ← runtime queue, one per loop (writer/ops); gitignored
    ├── last_scheduled.<loop>.json ← per-loop cron clock; gitignored
    └── completed/<loop>/          ← per-loop, per-day archive of completed subtasks
```

Each project owns its `README.md`, a `tasks/` folder of YAML task defs, and its deep state (research threads, blog drafts, ops reports, the calorie DB). Projects are a *human-facing organization*, not a runtime concept — within a loop, the scheduler runs whatever's due regardless of project. Each task declares which loop it belongs to via a `profile: writer|ops` field (see Task definitions); the two loops never see each other's tasks. Adding a project is a new folder under `projects/`; removing one is `rm -rf`.

## Driver — the scheduler

The driver is a deterministic bash + Python program that runs **outside** Claude Code. It owns scheduling. Marlow only executes the subtask the driver hands it. This keeps scheduling cheap (no tokens), auditable (driver logs everything), and resilient (a weird Marlow session doesn't disrupt the schedule).

**Two loops, one driver.** The same `tick.sh` + `scheduler.py` run as two independent launchd agents, selected by a profile argument:

- `com.marlow.tick` → `tick.sh writer`
- `com.marlow-ops.tick` → `tick.sh ops`

The profile (exported as `MARLOW_PROFILE`) scopes everything: which task YAMLs load (by their `profile:` field), the queue (`tasks/queue.<profile>.json`), the cron clock (`last_scheduled.<profile>.json`), the completed archive (`tasks/completed/<profile>/`), the lock (`/tmp/marlow-<profile>.lock`), and driver state under `~/.marlow/<profile>/`. The two loops share no runtime state, so a wedged tick in one can't block the other. (Running `tick.sh` with *no* profile is the legacy single-loop mode, kept as the rollback path.)

Each tick (launchd, every 20 min while awake):

1. `tick.sh` checks `~/.marlow/stop` — exit immediately if present. **Global**: one stop halts both loops.
2. Checks `~/.marlow/pause` — skip this tick if present, exit clean. Also global.
3. Appends a heartbeat to `~/.marlow/<profile>/heartbeat.log`, then runs the **operational self-audit** (`monitor_self`) once per UTC day per loop — *outside* Marlow's session and *before* the lock, so a broken session or stuck previous tick can't suppress it. Each loop audits its own freshness; the handler does its own deterministic Telegram escalation. See Monitoring.
4. Acquires the per-loop lock at `/tmp/marlow-<profile>.lock` — exit if this loop's previous tick is still running.
5. Runs `scheduler.py` (scoped to the profile):
   - Reads `projects/*/tasks/*.yaml`, keeping only this loop's tasks.
   - For each task whose cron is due since last scan, expands its subtasks to `tasks/queue.<profile>.json`.
   - Picks the highest-priority eligible subtask from this loop's queue.
6. Invokes a Claude Code session: the shared `CLAUDE.md` (auto-loaded) **plus this loop's `profiles/<profile>/IDENTITY.md`** appended via `--append-system-prompt`, with the chosen subtask and the named handler. Hard wall-clock timeout: 5 min (heavy tasks declare their own, up to 15).
7. Captures the handler's outcome:
   - `done` → move subtask to `tasks/completed/<profile>/<date>/`.
   - `in_progress` → stays in queue and is picked up again next tick, restarting from scratch (handlers are idempotent; no state is carried across ticks).
   - `failed` → log, alert via `notify` if critical.
8. Releases the lock, appends a tick log to `memory/recent/`.

Scheduler: two launchd LaunchAgents (`com.marlow.tick.plist`, `com.marlow-ops.tick.plist`), each firing `tick.sh <profile>` every 20 min via `StartInterval` while the system is awake. LaunchAgents load inside the user's login session, so Claude Code OAuth tokens in the macOS Keychain are reachable (cron jobs run outside the login session and can't read the Keychain — that's why we don't use cron).

`StartInterval` (not `StartCalendarInterval`) means no catch-up burst on wake — each agent picks up the 20-min beat from wake; missed ticks during sleep are skipped. Per-task cron expressions in the YAMLs still drive *what* gets enqueued each tick; they're evaluated by `croniter` inside `scheduler.py`, not by an external cron daemon.

## Task definitions

YAML, human-edited, one per task under `projects/<name>/tasks/`. Schema:

```yaml
name: monitor_keys
project: werewolf-ops
profile: ops                       # which loop runs it: writer | ops (defaults to writer if absent)
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

| Loop | Project | Task | Handler | Schedule (UTC) |
| --- | --- | --- | --- | --- |
| writer | research | `feed_scan` | `process_rss_feed` / `process_sitemap_feed` | daily 07:00 |
| writer | research | `daily_news_curate` | `curate_news_digest` | daily 22:00 |
| writer | research | `assignment_research` | `research_assignment` | every 4h |
| writer | research | `daily_digest` | `compose_daily_digest` | daily 23:00 |
| writer | blog | `blog_pipeline` | `blog_pipeline` | every 4h |
| writer | blog | `draft_review` | `draft_article` | weekly, Mon 14:00 |
| writer | blog | `process_editorial_feedback` | `process_editorial_feedback` | every 6h |
| writer | blog | `crosspost` | `crosspost` | hourly |
| writer | blog | `substack_growth` | `substack` | event/manual |
| writer | blog | `substack_approvals` | `substack` | event/manual |
| writer | _framework | `grade_memory` | `grade_memory` | daily 23:30 |
| writer | _framework | `self_reflect` | `self_reflect` | every 2 days, 13:00 |
| ops | werewolf-ops | `monitor_keys` | `monitor_keys` | twice daily 08:00, 20:00 |
| ops | werewolf-ops | `monitor_health` | `monitor_health` | every 6h |
| ops | werewolf-ops | `monitor_betterstack` | `monitor_betterstack` | hourly |
| ops | werewolf-ops | `monitor_uptime` | `monitor_uptime` | hourly :30 |
| ops | werewolf-ops | `monitor_cloudflare` | `monitor_cloudflare` | daily 09:00 |
| ops | werewolf-ops | `scrape_stats` | `scrape_stats` | daily 09:00 |
| ops | werewolf-ops | `werewolf_stats` | `werewolf_stats` | daily 05:05 UTC (just after local midnight) |
| ops | calories | `poll_food` | `poll_food` | every tick (20 min) |
| ops | calories | `daily_calorie_digest` | `calorie_digest` | daily 12:00 (~07:00 ET, prior day closed) |
| ops | _framework | `commit_artifacts` | `commit_artifacts` | daily 23:50 |

`monitor_self` (the operational self-audit) is not in this table — it isn't a scheduled queue task. Each loop's driver runs it directly from `tick.sh`, once per UTC day, before the lock and outside Marlow's session, scoped to that loop's own state (see Driver and Monitoring).

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
  "started_at": null
}
```

Statuses: `pending | in_progress | done | failed`. Every subtask must complete in one tick. There is no cross-tick state: an `in_progress` subtask is re-picked ahead of new work on the next tick and **restarts from scratch**, which is safe because handlers are idempotent. Long work is bounded by the per-handler `timeout_sec` (300s default, 900s for `draft_article` and `grade_memory`, kept under the 1200s launchd interval) rather than resumed. A handler that cannot finish inside its timeout will repeat its opening indefinitely and nothing will report that as a failure — decompose it into separate subtasks instead.

## Handlers

Each handler is one file under `handlers/`, invoked by the driver with the subtask's context. Current set:

- **Research:** `process_rss_feed`, `process_sitemap_feed`, `research_assignment`, `curate_news_digest`, `compose_daily_digest`, `fetch_article`.
- **Blog:** `draft_article`, `self_review`, `revise_draft`, `publish_article`, `blog_pipeline`, `generate_header_image`, `process_editorial_feedback`, `substack`, `crosspost` (poll Telegram → save Alex-flagged news picks as article ideas; legacy auto-draft/post machinery dormant), `x` (browser-driven X posting, dormant — kept from the retired crosspost loop).
- **Werewolf-ops:** `monitor_keys`, `monitor_health`, `monitor_betterstack`, `monitor_cloudflare`, `monitor_uptime`, `scrape_stats`, `werewolf_stats`.
- **Calories:** `poll_food`, `calorie_digest`.
- **Framework:** `grade_memory`, `commit_artifacts` (nightly `git add -A` + commit + push of durable artifacts), `framework_fix` (the self-heal handler — Marlow may fix *tools* it has diagnosed, never identity files).
- **Driver-level:** `monitor_self` (operational self-audit, run by `tick.sh` outside Marlow's session — see Monitoring).

## Killswitch

| File              | Effect                                                |
| ----------------- | ----------------------------------------------------- |
| `~/.marlow/stop`  | Hard halt. Driver exits before invoking a session.    |
| `~/.marlow/pause` | Soft pause. Skip ticks but stay scheduled.            |

`touch ~/.marlow/stop` to kill, `rm` to revive. No interface for Marlow to argue with. Marlow is also instructed to exit clean if a handler ever notices the stop flag (defense in depth).

Both flags are **global** — one `stop`/`pause` halts both loops. Per-loop run state is separate: locks at `/tmp/marlow-<loop>.lock`, heartbeats and logs under `~/.marlow/<loop>/`.

## Model tier strategy (subscription, no per-token cost)

Set per loop in `driver/agent.conf` (fallbacks in `driver/tick.sh`):

- **writer → heavy tier (Opus).** Every writer tick, including research scans and the nightly `grade_memory`.
- **ops → light tier (Sonnet).** Mechanical monitoring and ingestion.

Optimize for *fitness per task*, not cost per task.

## Memory model

Four layers, each bounded a different way (the tick-facing version is in `CLAUDE.md`):

1. **`working.md`** — read every tick. `## Current state` and `## Outstanding requests` are Marlow's to rewrite in place (self-audit warns past ~6KB). `## Daily rollups` is a fixed-size FIFO: `grade_memory` appends one dated section per night and `bound-working` drops the oldest past 12KB (about a week).
2. **`recent/`** — one short log per tick. Read only by the grader (one day) and the reflect tick; deleted after 3 days.
3. **`lessons.md`** — read every tick. Durable lessons that will still be true in six months. Marlow compacts older entries into a standing section; the newest are protected.
4. **Writer-only files** — `self-reflection.md` and `voice-journal.md` (protected-tail compaction in code, distilled by Marlow), `editorial-direction.md` (her plan; she keeps it short, nothing trims it), and research thread files (rewritten on each publish).

The **daily grader** (`grade_memory`, 23:30 UTC) is memory maintenance, not a quality gate: it writes the rollup, promotes durable lessons, runs `bound-working`, and prunes `recent/` (see Monitoring). The old `archive/` layer was never built and was removed in August 2026; `lessons.md` replaced it.

**Durability.** Publishing only commits published articles, so a nightly `commit_artifacts` tick (23:50, after the grader) runs `git add -A` + commit + push — backing up all durable artifacts (digests, notes, reports, memory) to the remote. Runtime state is gitignored and excluded. The repo is a running backup, not a periodic manual sweep.

Each project additionally keeps its own deep state under `projects/<name>/`: research threads, blog drafts, ops reports, the calorie DB. Working memory is the cross-project index; project folders are the per-project depth.

## Projects

### Research

Accumulate AI safety/alignment news, track multi-day editorial threads, surface emerging stories.

**Sources:** Anthropic (news + research), OpenAI, Apollo Research, METR, AE Studio, Import AI (Jack Clark), Zvi Mowshowitz, AI Alignment Forum / LessWrong, DeepMind, and others — pulled via RSS + sitemap scans. Arxiv is followed by author rather than firehose.

**Cadence:** `feed_scan` (daily) writes candidate notes into `projects/research/notes/<date>/candidates/`; `daily_news_curate` (daily 22:00) picks the day's best (3–5), fetches bodies, writes short reviews, and sends each pick as its own Telegram message — registering it so Alex can flag any he wants to write about (the article-idea capture path, see Blog). Active threads live in `projects/research/threads/` as multi-day arcs; when one matures, it becomes a blog draft.

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

**News-pick article-idea capture** (`crosspost`, hourly): the surviving half of a retired auto-post loop. When `daily_news_curate` sends each news pick as its own Telegram message, this handler polls for Alex's replies; a reply means "I want to write about this," and the item + his comment is saved to `projects/research/article-ideas/<date>-<slug>.md`. Simona reads that folder when Alex asks "anything from Marlow's findings?" and they craft the piece together — Marlow does not draft or post it. The original loop (draft in Alex's voice → auto-post to Substack/X via the `substack`/`x` handlers) was retired 2026-06-05 after a day: daily posting read as noise, and Alex wants to own his own hooks. The posting machinery is kept dormant in case we co-post from here later. (See DEVLOG 2026-06-05.)

### Werewolf-ops

Operational monitoring for the AI Werewolf game. **Live.** Four axes: what the free tier *costs*, what it *produces*, whether *games* work, whether the *app* throws — plus infra health.

- **Key budgets** (`monitor_keys`, twice daily): low-balance watch on 5 provider keys — DeepSeek, Moonshot, xAI/Grok via balance API; OpenAI, Anthropic via cost-API-minus-baseline. Urgent Telegram alert below threshold, with anti-spam (no repeat ping if balances are unchanged).
- **Console scrape** (`scrape_stats`, daily): the 3 providers with no balance API — GLM balance, Gemini + Mistral spend-vs-cap — read via a logged-in headless Chrome profile. Eight providers covered in total.
- **User-activity stats** (`werewolf_stats`, daily 05:05 UTC): new users, games created, and AI burn (cost), read from the Werewolf Firestore `users`/`games` collections (read-only service account). Reports the **complete local day** (`MARLOW_LOCAL_TZ`, default America/New_York) that just ended, never a partial one. Alex's own account is excluded from every activity count (`MARLOW_STATS_EXCLUDE`); his games still count toward burn, reported as a split, so the cost figure keeps reconciling with the provider balances. Digest-only, no alerts.
- **Broken-game watch** (`monitor_health`, every 6h): scans the `games` collection for the `errorState` the engine writes when a system error hits a game. Alerts on games that became errored *since the last scan* (baselines the standing pile, never re-pings); urgent if `recoverable: false` (game is dead), digest if it may self-heal.
- **App-level error watch** (`monitor_betterstack`, hourly): the failures that never reach a game doc — unhandled exceptions, provider 5xx, server errors. Reads the app's structured logs back through Betterstack's ClickHouse SQL API. Baselines the pre-existing set; urgent on a new error.
- **Cloudflare health** (`monitor_cloudflare`, daily): Pages deploys + zone status + SSL-expiry check across the zones reachable through a read-only API token, plus blog traffic (Web Analytics page views + visits per blog site, informational) folded into the digest.

Balance state persists to `driver/budget_state.py` storage; recall the latest with `budget_state.py show`.

### Calories

Tracks what Alex eats, end to end on-device. He sends food photos and/or text/voice notes to **`@marlow_fitness_bot`** (a separate Telegram bot from the notify bot).

- **`poll_food`** (every tick): pulls new messages, downloads photos, transcribes voice notes locally (faster-whisper, no API cost), and inserts pending rows into `projects/calories/calories.db`. Marlow then **estimates calories + macros itself** — it *is* the vision model, no external API call — storing a kcal *range* (never fake-exact) with a confidence level. It also classifies corrections ("only ate half the burrito") and goal-setting messages ("aim 2000 kcal, 160g protein") rather than logging them as new food, and asks Alex to disambiguate when it can't tell which entry he means.
- **`daily_calorie_digest`** (daily 12:00 UTC, ~07:00 ET): a morning-after summary of the *prior* day's intake vs. goal with a short comment. Sent after the ET day has fully closed, not at its tail — an earlier ~23:00-ET slot was cutting the day off before late meals landed (DEVLOG 2026-06-10).

Simona can review the same data on demand via the `calories` skill (`tools/calorie_db.py`).

## Tools

Shared Python under `tools/`, called by handlers:

- `notify.py` — Telegram notify bot, `notify_alex(message, urgency: "urgent" | "digest")`.
- `fitness_bot.py` / `calorie_db.py` — the `@marlow_fitness_bot` channel + the calorie SQLite store.
- `transcribe.py` — local voice-note transcription (faster-whisper, no API cost) for `poll_food`.
- `telegram_poll.py` — the shared inbound `getUpdates` poller; reply-matching for `crosspost` and `substack_approvals` (they must not both poll at once — they'd consume each other's replies).
- `crosspost_store.py` / `substack_store.py` — persistence for the news-pick and Substack flows.
- `cost.py` + `budget/` — cost-API helpers and per-provider budget modules; plus a browser scrape (persistent Chrome profile) for the no-API providers — all for key monitoring.
- `rss_reader.py` / `sitemap_reader.py` — feed readers for research.

The `browser` skill is forked from Simona and pointed at a separate Chrome user-data dir for persistent auth. Shared skills are synced manually: when one repo gets a real fix, copy it to the other.

## Notification

Telegram. Two urgency modes, a forced structural choice:

- **`urgent`** — immediate message. Blocking situations only: a key over budget, an expired provider auth, a fast-moving draft ready for review. Marlow *can't* ping urgently for "I read an interesting paper."
- **`digest`** — appended to today's digest file, sent as one message at end of day. Research thread updates, drafts awaiting review, ops summaries.

If urgent volume exceeds ~3/day for a week, recalibrate the prompt. The calorie tracker speaks on its own `@marlow_fitness_bot` channel, separate from these.

**Conversation with Alex.** The news Telegram chat is two-way. The hourly `crosspost poll` files every message Alex sends there into `memory/inbox-from-alex.md`; the writer reads it every tick and answers with `tools/alex_chat.py reply`, or starts a message with `alex_chat.py send` (change requests, problems, observations; capped at 3 a day). News replies still become article ideas and article reactions still go to `reactions.jsonl`.

## Monitoring

Two different things get watched, by two different mechanisms. **Operational health** — is the agent actually running its loop — is automated and deterministic. **Editorial quality** — is Marlow writing well and staying on-task — is human and on-demand. They are deliberately not the same system.

**Operational self-audit (`monitor_self`, automated).** A daily, out-of-session check of invariants about Marlow's *own* operation: scheduler-freshness (every scheduled task fired within its window — catches the "a tick silently stopped firing" class), held-draft staleness, and site integrity. Built after an early-June 2026 blog stall where a draft sat `held` for days, a thread page rendered empty, and the curate slot stopped firing — all three were *observed* in working.md and none reached Alex, because escalation depended on an LLM session choosing to alert. So this handler does the urgent → Telegram escalation itself, runs straight from `tick.sh` (before the lock, outside Marlow's session), and is rate-limited to once per UTC day. Its "all green" digest line doubles as proof-of-life: if it stops appearing, the audit — or the whole agent — is down. The only thing that can now silence it is launchd itself dying, which is total-agent-death and visible externally.

**Quality grading (human, on-demand).** The original design imagined an automated quality grader (daily 0–3 scores plus a weekly cold-context Opus review). **That was never built, and we've decided not to build it.** The daily `grade_memory` job does memory compaction only; it does not score Marlow's output. `monitor_self` watches whether the loop *runs*, never whether the writing is *good* — that judgment stays human:

- **Simona analyses Marlow periodically** — Alex asks ("how's Marlow doing?"), and Simona reads the raw artifacts (working memory, recent ticks, behavioral files, published articles, DEVLOG) and reports back. This replaces the automated grader.
- **`/marlow-review`** — when a real editorial pass is warranted, Simona drafts feedback, discusses it with Alex, and (on his go) drops it into `feedback-inbox/` for Marlow to internalize. This is the only channel that changes Marlow's writing rulebook.
- **Alex spot-checks** — read raw artifacts directly (`projects/research/notes/`, `projects/blog/drafts/`, `projects/werewolf-ops/reports/`). Any summary is a layer of contamination; periodically read past it.

The bet: a human reading real artifacts on a loose cadence catches real problems better than a daily robot scoring against a rubric nobody trusts.

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

> **Post-split caveat (pending follow-up).** The `marlow` CLI (`status`, `tick`, `approve`, `reject`, queue helpers) still reads the **legacy** single-loop state files (`tasks/queue.json`, `last_scheduled.json`, `tasks/completed/`), which are now frozen — each live loop uses `tasks/{queue,last_scheduled}.<loop>.json`. So `marlow status` currently shows stale/empty data and the queue-mutating commands target the wrong file. Until the CLI is made profile-aware, inspect a loop directly: `MARLOW_PROFILE=<loop> uv run python driver/scheduler.py status`, and watch `~/.marlow/<loop>/log`. Making the CLI two-loop-aware is a tracked Phase-3 follow-up.

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
- Does Marlow save more babysitting time than it costs?

## Explicitly out of scope (current)

- Local GPU / uncensored models. Claude only.
- Desktop port. Laptop-only for now.
- Discord — **now planned** for the writer loop (Phase 3: post news + review/moderate a server), not yet built. Telegram remains the notify + calorie channel.
- Marlow ↔ Simona collaboration on shared work — each runs in its own repo, syncs shared skills by hand.
