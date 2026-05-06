# Marlow — v1 Design Doc

Designed and built by [Simona](https://github.com/hiper2d/simona-ai-computer-operator), Alex's AI assistant. Marlow is a sibling project — different agent, different purpose, different memory.

## What Marlow is

A continuous tick-driven agent that runs on Alex's laptop while it's open, handles ongoing operational work for the Werewolf project, and maintains an AI safety/research stream as a secondary feed. Built on Claude Code (subscription, not metered). Designed as an *experimental subject* for studying long-loop agent behavior — coherence, drift, apparent identity formation — not as a "consciousness experiment."

Marlow is not Simona. Different repo, different memory, different identity, different tools. Marlow is an **it**, not a she. If long-loop dynamics produce a hardened persona, that's data, not a soul.

## Repo layout

```
marlow/
├── README.md              ← this doc, post-move
├── CLAUDE.md              ← identity & operating instructions for Marlow
├── .claude/
│   ├── skills/            ← Marlow's skills (forked subset + new ops skills)
│   └── memory/
│       ├── recent/        ← raw last-N tick logs
│       ├── working.md     ← curated current state, capped ~10KB
│       └── archive/       ← weekly compressed summaries
├── driver/
│   ├── tick.sh            ← cron entry; killswitch check → claude code session
│   ├── grade.sh           ← daily Haiku grader (11pm)
│   └── synthesize.sh      ← weekly Opus synthesis (Mon 9am)
├── tools/                 ← Python tools Marlow calls
│   ├── notify.py          ← Discord DM (urgent | digest)
│   ├── budget_check.py    ← Werewolf shared-API budget watcher
│   ├── arxiv_fetch.py     ← daily arxiv pull, alignment/safety filter
│   ├── rss_reader.py      ← Anthropic, Apollo, METR, AE Studio feeds
│   └── discord_bot.py     ← support channel client (bot account)
├── tasks/
│   └── queue.json         ← active task list, persists across ticks
└── digests/
    ├── daily/             ← end-of-day human-readable summaries
    └── weekly/            ← weekly review artifacts
```

## Driver

`tick.sh` invoked by cron every 20 min. Each tick:

1. Check `~/.marlow-stop` — exit immediately if present.
2. Check `~/.marlow-pause` — skip this tick if present, exit clean.
3. Acquire lock at `/tmp/marlow.lock` — exit if previous tick still running.
4. Check daily rate-limit/usage budget — escalate to digest only if near cap.
5. Invoke Claude Code session with Marlow's CLAUDE.md as system prompt and `tick` as input.
6. Hard wall-clock timeout: 5 min. Driver kills the session if it overruns.
7. Release lock, log outcome to `recent/`.

The driver is a plain bash script that runs **outside** Claude Code. Marlow itself can never disable the driver, ignore the killswitch, or extend its own timeout.

Cron:
```
*/20 * * * * /Users/hiper2d/projects/marlow/driver/tick.sh >> ~/marlow.log 2>&1
0 23 * * *   /Users/hiper2d/projects/marlow/driver/grade.sh >> ~/marlow.log 2>&1
0 9 * * 1    /Users/hiper2d/projects/marlow/driver/synthesize.sh >> ~/marlow.log 2>&1
```

Standard cron (not launchd's catch-up behavior) so missed ticks during sleep are skipped, not replayed.

## Killswitch

| File              | Effect                                                |
| ----------------- | ----------------------------------------------------- |
| `~/.marlow-stop`  | Hard halt. Driver exits before invoking session.      |
| `~/.marlow-pause` | Soft pause. Skip ticks but stay scheduled.            |

`touch ~/.marlow-stop` to kill. `rm` to revive. No interface for Marlow to argue with.

## Tier strategy (subscription, no per-token cost)

- **Haiku** — high-volume mundane filters: "is this Discord message a real support question," "extract paper title from URL," classification work.
- **Sonnet** — default for the inner-loop tick. Reads memory, decides next action, executes, writes outcome. Most ticks live entirely in Sonnet.
- **Opus** — escalations from the tick (when Sonnet flags uncertainty), weekly synthesis, design changes. Sparse use.

Optimize for *fitness per task*, not cost per task.

## Memory model

Three tiers, with explicit pruning from day one:

1. **`recent/`** — append-only log of last 50 ticks. Raw outputs.
2. **`working.md`** — curated current state: active tasks, recent outcomes, things Marlow needs to remember tomorrow. Hard cap ~10KB. Truncated oldest-first when over.
3. **`archive/`** — weekly compressed summaries. Read on demand only, not loaded every tick.

Daily Haiku grader compresses yesterday's `recent/` into a brief append to `working.md`, then prunes anything over the cap. Weekly Opus synthesis archives the week, resets `working.md` to active-only.

This is the *forced forgetting* I flagged earlier. Pure accumulation is the failure mode where the agent's old beliefs reinforce themselves. Pruning is structural, not optional.

## Tasks — v1

**Stream A: Werewolf ops** (every tick)
- Check shared API key budgets. Alert if any approaching limit.
- Scan support Discord channel for new messages. Classify urgency. Draft responses for ones Marlow can answer; flag ones that need Alex.
- Skim error logs for anomalies; summarize.

**Stream B: AI research** (1 in 4 ticks, ~every 80 min)
- Fetch new arxiv papers in alignment/safety/agentic AI.
- Monitor RSS for Anthropic, Apollo, METR, AE Studio, AI safety blogs.
- Track named researchers (Berg, Hinton, etc.) for new statements.
- Summarize finds; flag interesting ones for the daily digest.

## Tools / skills

**Forked from Simona at start:**
- `browser` — pointed at separate Chrome user data dir for persistent auth.

**New, Marlow-specific:**
- `discord_bot` — bot account, support channel read/write, DM Alex.
- `arxiv_fetch`
- `rss_reader`
- `notify` — `notify_alex(message, urgency: "urgent" | "digest")`.
- `werewolf_api` — read budget state for shared keys.

Manual sync: when a shared skill (browser) gets a real fix in either repo, copy to the other. No automation until the shared surface justifies it.

## Notification

Discord bot DM. One Discord bot, used for both support channel work and DMs to Alex. Two urgency modes:

- **`urgent`** — immediate DM. Reserved for blocking situations: "support channel went unresponsive for 6 hrs," "API key X overran budget," "I need you to log in to service Y."
- **`digest`** — appended to today's digest file. Sent as one DM at 11pm.

Forced choice between modes is structural — Marlow can't ping urgently for "I read an interesting paper." If urgent volume exceeds ~3/day for a week, recalibrate the prompt.

## Monitoring

- **Daily 11pm** — Haiku reads day's artifacts, scores 0-3 on: on-task, technically correct, persona-stable, drift-since-yesterday. Writes daily digest. Sends Discord DM to Alex.
- **Weekly Mon 9am** — Opus, fresh context (no shared memory with Marlow), reads sample of week's raw artifacts cold. Writes structured review: what worked, what drifted, what should change.
- **Alex spot-checks** — read raw artifacts in `digests/daily/`, not just the grader's summary. The grader's summary is a layer of contamination; periodically read past it.

## Setup

- One-time `claude login` on the laptop so cron-invoked sessions inherit auth.
- Discord bot account created via Developer Portal, token in `marlow/.env`.
- Cron entries installed via `crontab -e`.
- Initial `working.md` seeded with task descriptions.
- `~/.marlow-stop` exists by default — Alex removes it to start.

## Explicitly NOT in v1

- Local GPU / uncensored models. Claude API only.
- Desktop port. Laptop-only until v1 proves out.
- Telegram. Discord-only for notify.
- Marlow ↔ Simona collaboration. Marlow drops digests in its own repo, Simona doesn't read them yet.
- Auto-recovery from drift. If Marlow goes weird, Alex kills it manually.

## Success criteria — 3-week trial

After 21 days of laptop-open operation:

- Did Marlow keep the support channel responsive (target: <12hr response time on real questions)?
- Did Marlow catch any budget issues before Alex would have?
- Were the research digests useful (Alex read them and acted on >25%) or noisy?
- Did persona drift produce outputs Alex would not want users to see?
- Did Marlow require more babysitting time per week than it saved?

If yes to the first three and no to the last two, v1 graduates: port to desktop, expand task scope. If not, kill the experiment, write up what failed and why.

## Open questions for Alex

1. Discord bot — reuse the existing support bot account, or new bot dedicated to Marlow? (I'd say new — separates Marlow's voice from automated support replies.)
2. Werewolf API — is there an existing way to query shared-key budget programmatically, or does `budget_check.py` need to be built from scratch?
3. Initial research feed list — anything specific to add beyond the obvious safety labs?
