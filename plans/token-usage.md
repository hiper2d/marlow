# Token usage: where it goes and how to cut it

Written 2026-10-29. Data: `~/.marlow/cost-log.jsonl` (one record per tick) for the 14 days 10-15 to 10-28, Claude Code session transcripts for per-turn context, and test sessions run on 10-29 to measure the starting context.

## 1. Summary

- Marlow reads about **49M input tokens a day** and writes about **210K**. Writer (Opus): 20M. Ops (Sonnet): 29M.
- About **70% of those tokens are spent in ticks that found nothing to do**: no new Telegram message, no new feed entry, all sites up.
- Every turn of every tick starts with **45K tokens** of context before Marlow reads a single file of her own. Most of it is Claude Code's own setup, not Marlow's memory.
- No tick is near the context limit. The biggest single turn in 1,500 sessions held 137K tokens. The large per-tick numbers (500K+) are sums over many turns, not one context.
- Plan: cut the starting context (steps 1-3), skip ticks that have nothing to do (step 4), then take fewer turns (step 5). Estimated result: **about 8-12M tokens a day, down from 49M.**

## 2. How to read the numbers

- **Tick:** one Claude session that runs one task, then exits.
- **Turn:** one model call inside a tick. Each tool call (run a script, read a file) costs one turn.
- **Context per turn:** everything the model sees on that call: system prompt, tools, instructions, and the conversation so far.
- **Input tokens per tick** = the sum of the context over all its turns. A tick with 10 turns at about 55K each reads about 550K. That is why the number looks huge while the context stays small.
- **So tokens per tick ≈ turns × context per turn.** The three ways to cut it: fewer ticks, fewer turns, smaller context.
- **Cache:** almost all input is re-read from the prompt cache (about 211K of the median writer tick's 237K). Cached tokens are cheaper, but they still count toward the subscription's usage limits.
- **Dollars:** `cost_usd` in the log is what the tokens would cost at API list prices. We are on a subscription, so nothing is billed. It is shown below only as a way to compare usage, and it is labeled "list price".

All numbers below are **per day**, averaged over the 14 days.

## 3. Totals per profile

| Profile | Model | Ticks/day | Turns/day | Input tokens/day | Output tokens/day | List price/day |
|---|---|---|---|---|---|---|
| writer | Opus 4.8 | 52 | 387 | 20.0M | 100K | $24.39 |
| ops | Sonnet 5 | 49 | 512 | 29.4M | 110K | $12.09 |
| **total** | | **101** | **899** | **49.4M** | **210K** | **$36.48** |

Per tick (median): writer 5 turns and 237K input; ops 10 turns and 548K input.

## 4. Per task

Sorted by input tokens per day. "Nothing to do" is the share of the task's ticks whose result said there was nothing new (estimated by matching phrases like "0 new", "quiet scan" or "no actionable drafts" in the result text).

| Task | Profile | Ticks/day | Turns (median) | Tokens per tick (median) | Tokens/day | Nothing to do |
|---|---|---|---|---|---|---|
| monitor_betterstack | ops | 15.6 | 12 | 744K | 12.6M | 66% |
| monitor_uptime | ops | 18.6 | 7 | 367K | 7.0M | 100% |
| process_rss_feed | writer | 10.6 | 10 | 495K | 6.1M | 66% |
| crosspost (Telegram poll) | writer | 17.4 | 4 | 202K | 3.7M | 94% |
| process_sitemap_feed | writer | 6.0 | 9 | 464K | 3.2M | 75% |
| monitor_health | ops | 3.7 | 12 | 691K | 2.6M | 88% |
| monitor_discord | ops | 3.9 | 11 | 610K | 2.4M | 93% |
| blog_pipeline | writer | 5.5 | 5 | 209K | 1.4M | 92% |
| curate_news_digest | writer | 1.0 | 22 | 1,246K | 1.4M | 14% |
| grade_memory | writer | 0.9 | 18 | 1,318K | 1.3M | 38% |
| monitor_keys | ops | 2.0 | 10 | 535K | 1.2M | 64% |
| research_assignment | writer | 5.2 | 5 | 220K | 1.2M | 100% |
| scrape_stats | ops | 1.0 | 14 | 841K | 1.0M | 0% |
| tampa_luma | ops | 1.6 | 9 | 447K | 0.8M | 68% |
| process_editorial_feedback | writer | 3.8 | 4 | 201K | 0.8M | 100% |
| monitor_cloudflare | ops | 1.0 | 12.5 | 721K | 0.7M | 100% |
| werewolf_stats | ops | 1.0 | 11 | 675K | 0.7M | 29% |
| self_reflect | writer | 0.5 | 12 | 650K | 0.4M | 0% |
| draft_article | writer | 0.1 | 28.5 | 2,577K | 0.4M | 0% |
| compose_daily_digest | writer | 0.9 | 7 | 348K | 0.3M | 31% |
| commit_artifacts | ops | 1.0 | 5 | 249K | 0.3M | 0% |

Tokens in ticks with nothing to do: writer 13.9M/day (69%), ops 22.2M/day (75%).

The work Marlow exists for is cheap. Drafting, self-reflection and the daily news curation together are about 2M tokens a day. The big spenders are hourly checks that find nothing: the betterstack scan, the uptime check and the Telegram poll.

## 5. Where one turn's context goes

Measured on 10-29 with a one-word test session started in the Marlow repo:

| Piece | Tokens | Needed? |
|---|---|---|
| Claude Code core system prompt + the 6 tools Marlow uses (Bash, Read, Write, Edit, Glob, Grep) | ~14.5K | Yes |
| The other built-in tool definitions (agents, web, notebook, tasks, ...) | ~14.9K | No. 600 recent sessions called only Bash, Write, Read and Edit (plus ToolSearch 4 times). |
| Claude Code auto-memory (its own memory system for this repo) | ~11.9K | No. **Switched off 10-29**, see step 1. |
| `CLAUDE.md` (shared rules) | ~3.9K | Yes |
| **Start of every session, before any profile** | **45.2K** | |
| + writer `IDENTITY.md` | +17.9K | Partly. Most of it is per-task instructions a feed scan never uses. |
| + ops `IDENTITY.md` | +6.7K | Partly. |

Then the task reads its own files: `working.md` (8.0K), `lessons.md` (3.5K), the task YAML and the handler output. The first turn of a real tick is about 49K at the median.

Peak context in any single turn (1,500 recent sessions): median 56K, 90th percentile 73K, 99th percentile 95K, maximum 137K.

## 6. The plan

Ordered by savings per unit of work. Each step lists what it saves on its own, measured against today's 49.4M/day.

### Step 1. Turn off Claude Code auto-memory - DONE 10-29

- **What:** `"autoMemoryEnabled": false` in `.claude/settings.json`. Marlow has her own memory system; this one was a fifth memory layer nobody designed.
- **Found:** ops ticks had been writing to it since July: 815 files in `~/.claude/projects/-Users-hiper2d-projects-marlow/memory/recent/`, plus a 16.5KB index loaded into every tick of both profiles. About 295 tool calls in 600 recent sessions read or wrote it, which also cost turns. Its one useful note (append to daily report files, never overwrite them) moved to `profiles/ops/IDENTITY.md`.
- **Saves:** 11.9K × 899 turns/day ≈ **10.7M/day (22%)**, plus the turns spent writing memory.
- **Verified:** test session base context dropped from 45.2K to 33.3K.
- **Left over:** the old memory folder is no longer loaded. Delete it whenever you like.

### Step 2. Load only the 6 tools Marlow uses

- **What:** add `--tools Bash,Read,Write,Edit,Glob,Grep` to the `claude -p` call in `driver/tick.sh`.
- **Saves:** 14.9K × 899 ≈ **13.4M/day (27%)**.
- **Measured:** with steps 1 and 2 together, base context is 18.4K instead of 45.2K.
- **Risk:** low. If a task needs web fetch, its handler script already does it in Python. Run one tick of each task after the change.

### Step 3. Make the identity files short

- **What:** the writer `IDENTITY.md` (17.9K) holds detailed instructions for every task: drafting, crossposting, reflection, curation. Every tick loads all of it. Move each task's instructions into its task YAML, which the tick already reads. Keep only who she is, the shared rules and pointers in IDENTITY. Same for ops.
- **Target:** writer about 6K, ops about 3K.
- **Saves:** writer 11.9K × 387 ≈ 4.6M; ops 3.7K × 512 ≈ 1.9M. **About 6.5M/day (13%).**
- **Note:** this also makes her "who you are" section a larger share of what she reads. Today it's a few paragraphs inside 18K of procedures.

### Step 4. Don't start a session when there is nothing to do

- **What:** the biggest lever. Before `tick.sh` launches Claude, it runs a cheap deterministic check for the task: any new Telegram message? any new feed entries? any new Betterstack incident? any pending assignment or inbox file? If the answer is no, the driver writes the result ("nothing new") and the report line itself and exits. No model call.
- **Where:** a `precheck` command per handler, returning `{"work": true|false, "summary": "..."}`. Start with the tasks that are almost always empty: `monitor_uptime` (100%), `research_assignment` (100%), `process_editorial_feedback` (100%), `crosspost` (94%), `monitor_discord` (93%), `blog_pipeline` (92%), `monitor_health` (88%). Then the feeds and betterstack.
- **Saves:** up to the 36M/day spent in empty ticks today. After steps 1-3 make each tick smaller, the realistic figure is **about 60-70% of what is left**.
- **Bonus:** `monitor_uptime` is a pure HTTP check. It needs Marlow only when a site is down.
- **Risk:** a precheck that wrongly says "nothing" hides real work. Each precheck must be the same function the handler already uses (for example `fetch_new` for feeds), not a second copy of the logic.

### Step 5. Fewer turns per tick

- **Give the YAML in the prompt.** Today a tick spends a turn finding and reading its task YAML. The driver can paste the subtask and its YAML into the first prompt.
- **Batch the feed scans.** About 16 feed-scan ticks a day each pay the full base context and 9-10 turns. One tick that runs `fetch_new` on all feeds and judges only the new entries would cost a fraction of that.
- **Compact handler output.** Handlers should return short JSON. Long output stays in the context for every later turn.
- **Saves:** hard to estimate before trying. If ops goes from 10 turns to 6, ops tokens drop by about 40%.

### Step 6. Housekeeping (no token effect)

- Session transcripts: 2,928 files, 1.2GB in `~/.claude/projects/-Users-hiper2d-projects-marlow/`. Add `--no-session-persistence` to the tick call, or prune old files.
- `tools/cost.py` header says `claude -p` usage moved to a $100/month API credit on 2026-06-15. At about $36/day of list-price usage that credit would have run out in 3 days, so the comment is stale. Fix it, and rename the field in reports to "list price".

## 7. Expected result

| | Base context per turn | Input tokens/day |
|---|---|---|
| Before (10-15 to 10-28) | 45.2K (+17.9K writer / +6.7K ops) | 49.4M |
| After step 1 (done) | 33.3K | ~38.7M |
| After steps 1-2 | 18.4K | ~25.3M |
| After steps 1-3 | 18.4K (+6K writer / +3K ops) | ~18.8M |
| After steps 1-4 | same | ~7-9M |
| After step 5 | same | lower still |

These are estimates: each step is computed from today's turns per day, and the steps overlap a little.

## 8. How to check

After each step, recompute the per-profile and per-task tables from `~/.marlow/cost-log.jsonl` for the days since the change and compare them with sections 3 and 4. A small `tools/usage_report.py` that prints these two tables would make it a one-command check; it is worth writing as part of step 2.
