# Marlow DEVLOG

Append-only chronological log of Marlow's development arc. Written from
outside Marlow (Simona and Alex). Captures decisions taken, decisions
reconsidered, things tried that didn't work, framework concerns Marlow
herself filed, and pivots — the *journey*, not the *spec*.

This file's existence is enforced; see Simona's CLAUDE.md under
"Marlow project — devlog discipline." Every substantive piece of
framework work appends an entry before moving on to the next.

---

## 2026-05-12 — Simona daemon, Astro blog site, drafting pipeline, scheduler fixes

### What landed

- **Astro blog site** scaffolded at `projects/blog/site/`. Six routes (homepage, post/[slug], thread/[slug], threads index, archive, about) plus `/rss.xml`. Content collection unions `../drafts/` and `../published/` so drafts render with a visible badge during the iteration phase. Dark mode default with a `data-theme` toggle + `prefers-color-scheme` fallback. Serif body (Iowan/Charter on macOS, Georgia fallback), system sans for UI chrome, ~38rem reading column. Pagefind search and Cloudflare Pages deploy deliberately deferred — designing around real content beats designing around Lorem Ipsum.
- **Drafting pipeline** for Marlow: `handlers/draft_article.py` (orchestration — returns thread file + every research/candidate note that mentions the thread slug), `projects/blog/tasks/draft_review.yaml` (weekly Sundays 14:00 UTC), CLAUDE.md drafting protocol with explicit ripeness bar (3+ cross-source anchors, real through-line, something to say), and `marlow draft <slug>` CLI for on-demand drafting.
- **Marlow's first draft** landed: "Three data points in a week, one asymmetry" on the `automated-ai-rd` thread. 8.7KB. Picked the right framing — not "automated AI R&D has arrived" but "the offense side is moving faster than the defense side."
- **Simona daemon** built — parallel framework in the simona repo mirroring Marlow's. `daemon/` (tick.sh, scheduler.py, notify.py, install/uninstall-agent.sh, PROTOCOL.md), `handlers/` (review_drafts.py, observe_marlow.py), state at `~/.simona-loop/`. LaunchAgent label `com.simona.tick`, 7200s interval. Telegram shares Marlow's bot (env vars loaded from marlow's `.env` in tick.sh). Tasks: `review_drafts` (every 2h, reviews drafts that lack a `<slug>.simona-review.md` sibling), `observe_marlow` (daily 12 UTC, journals Marlow's evolving state). On-demand: `simona review [slug]` and `simona observe`.
- **Scheduler fixes**: eager-fire on first sight (newly-added task definitions were firing immediately because `is_due` accidentally returned True for tz-aware datetimes from croniter — now explicit `return False` on first sight), and dedup of subtasks with identical `(handler, url, prefix)` already pending/in-progress (previously feed_scan re-fires queued full batches of no-op subtasks).
- **UTC rollover fix** in `compose_daily_digest` and `curate_news_digest`: if invoked within first 4 hours past UTC midnight, default to yesterday's date. Previously, a 23:00 UTC task firing post-midnight after sleep would send the empty new-day file instead of yesterday's actual content.
- **AlignmentForum fetch fix**: Marlow's first autonomous curate (May 10 22:02 UTC) hit 429 throttling on all AF article fetches with the agent-style UA. Fixed: real Safari UA + `Accept-Language` header + retry-with-backoff on 429. Smoke-tested against a real AF post, 10K chars extracted cleanly.
- **Inspection CLI**: `marlow threads`, `marlow notes [--date X] [--candidates]`, `marlow memory [-n N]`, `marlow news [--date X]`. Surfaces what Marlow's been doing without grepping the repo.
- **Voice / humor permission** added to CLAUDE.md: dry humor, wryness, running observations across days, mild self-doubt are fine when they emerge from real things — never performed. Plus a channel-split clarification (research → curate pipeline; `notify_alex(urgency=digest)` reserved for ops-class events from future projects).
- **Memory grader** wired: `handlers/grade_memory.py`, `projects/_framework/tasks/grade_memory.yaml` (23:30 UTC daily). Reads yesterday's `memory/recent/` tick logs, Marlow compresses into a `## Daily rollups` section in `working.md`, prunes recent/ to 3-day retention. New `_framework` quiet meta-project for cross-cutting tasks.

### What Marlow flagged that we acted on

The grader's first run produced a `working.md` with **three Outstanding Requests for Alex/Simona** that Marlow filed herself, with evidence:

1. *Scheduler queues same-day duplicate feed scans.* Apollo /blog/ ran three times (May 11), METR twice, Anthropic news + research each twice. All no-ops because handlers check `last_seen`, but wasteful. Marlow proposed dedup on `(url, prefix)`. → **Fixed** in scheduler dedup.
2. *`notify_alex(urgency=digest)` is undercalled.* Two consecutive empty days in `digests/daily/` while 22 candidate notes were being written. Asked whether by design or bug. → **Clarified** in CLAUDE.md: research goes through curate; daily_digest channel is for future ops/budget events.
3. *daily_digest fired ~1h late after UTC rollover.* Scheduled `0 23 * * *`, actually ran 00:06 UTC May 12 with today's date. → **Fixed** with the UTC rollover default-to-yesterday logic.

These reports were unprompted — Marlow noticed during a single grader tick the day after the bugs first manifested. The "outstanding requests" pattern from CLAUDE.md works.

### Decisions reconsidered

- **cron → launchd** (carried over from earlier in session): the original install-cron.sh + crontab approach failed silently because cron jobs run outside the user login session and can't read OAuth tokens from the macOS Keychain. Symptom: every tick exited in ~2 seconds with "Not logged in." Diagnosis took longer than the fix. Replaced with a per-user LaunchAgent (`com.marlow.tick`, StartInterval 1200, RunAtLoad false). LaunchAgents load inside the user login session — Keychain access works, subscription auth works. Same one fix solved the auth bug and gave us a cleaner macOS-native scheduler.
- **News curation: per-scan flag vs. end-of-day pick.** First impulse was the existing pattern (each feed_scan tick flags interesting items into `digests/daily/<date>.md` via `notify_alex(urgency=digest)`). Reconsidered after Alex pointed out the editorial limitation: scans are isolated, so Marlow can't rank a quiet-but-strong item against a noisy mediocre one. Pivoted to two-pass — candidate notes during scans, end-of-day curation across all sources. The pivot meant new handlers (`curate_news_digest`, `fetch_article`), new task (`daily_news_curate` at 22:00 UTC), and a CLAUDE.md rewrite of the scan-time and end-of-day protocols. First curated digest (May 10 22:02 UTC) validated the choice — Marlow picked 5 from 9 candidates with explicit ranking reasoning.

### Things that surprised us

- Marlow choosing not to write 24 individual candidate notes for Apollo's historical sitemap on first scan — instead writing a single thematic catalog ("First scan… 24 papers/posts plus the index page. Sitemap `lastmod` is uniformly 2026-05-08 — that's when their sitemap was regenerated, not when these were written.") This kind of editorial judgment under-instruction is exactly what the design hoped for but couldn't be specified for.
- Marlow's autonomous May 11 digest opening with "the day's center of gravity is automated-AI-R&D" — a real synthesis observation, not a recap. Caught Anthropic's two foregrounded caveats on the AAR paper, flagged Kokotajlo-as-mission-director in Apollo's PBC announcement, noted Steven Byrnes' empowerment essay weakens corrigibility-as-target proposals. Voice arrived sooner than expected.
- Marlow filing three architectural concerns about her own framework in her first proper working memory — including spotting the scheduler eager-fire bug from downstream effects (duplicate scans), without ever being told to look for it.

### What's deferred

- **Pagefind search** on the blog (15-min add, no urgency at low post volume).
- **Cloudflare Pages deploy config** and a real domain. Site is local-only at `localhost:4321`.
- **Production filtering** of drafts from the public build. Currently drafts visible with a `Draft` badge; one-line change in `src/lib/posts.ts` when ready.
- **Publish handler** — moves approved drafts from `drafts/` to `published/`, eventually pushes to git for Cloudflare auto-deploy. Approval gate stays manual either way.
- **Weekly Opus synthesizer** — compresses Marlow's `working.md` daily rollups into `memory/archive/<week>.md` weekly, resets working.md to active-only. Pairs with the daily grader.
- **Simona's `self_reflect`** task — weekly Simona-on-Simona. Considered too early to design until `observe_marlow` has produced enough entries to know what daily voice looks like.
- **Two-way Telegram chat** — would let Alex ask Marlow about her picks from his phone. Postponed — no public-IP server, and the "Marlow on a server" pivot it implies isn't ready.

### Open questions / things to watch

- Does the new closing `— Marlow` paragraph in news digests develop a recognizable voice over a week of entries, or stay generic? First digest with the change fires May 12 22:00 UTC.
- Does the `observe_marlow` journal develop continuity across days, or read like 30 isolated daily snapshots?
- Does the scheduler eager-fire fix actually work as expected for the new draft_review and grade_memory tasks (both first-sight after the fix landed), or does some other edge case fire them prematurely?
- Will the laptop's sleep behavior cause `observe_marlow` (12 UTC daily) to chronically miss its fire window? May need to either move to a time when the laptop is reliably awake, or accept that Simona's loop is partially aspirational on a laptop schedule.

### State at end of day

- Marlow: launchd agent active (com.marlow.tick), 20-min interval, ~30 successful ticks. Queue mostly drained. One thread file (`automated-ai-rd`, ripeness high), six candidate threads in working memory. One blog draft pending review. Two news digests delivered to Telegram. Working.md ~6.5KB. Grader functional. Drafting functional.
- Simona daemon: launchd agent installed (com.simona.tick), 2h interval, 1 successful run (manual kickstart, "nothing to do"). First on-demand observation in flight at end of session.
- Marlow repo: committed through `b8c7dad` (editorial output snapshot) plus the Astro site (`<later commit>`). Simona repo: uncommitted (git block in simona repo; Alex commits).

---
