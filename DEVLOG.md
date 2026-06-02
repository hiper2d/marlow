# Marlow DEVLOG

Append-only chronological log of Marlow's development arc. Written from
outside Marlow (Simona and Alex). Captures decisions taken, decisions
reconsidered, things tried that didn't work, framework concerns Marlow
herself filed, and pivots — the *journey*, not the *spec*.

This file's existence is enforced; see Simona's CLAUDE.md under
"Marlow project — devlog discipline." Every substantive piece of
framework work appends an entry before moving on to the next.

---

## 2026-06-01 — self-review hold: 2026-06-01-ai-offense-shape-not-capability

Self-review of the cyber-assignment draft (`ai-offense-shape-not-capability`,
the deliberate rotation off Anthropic-orbit alignment) came back
**hold-for-alex** on **pause item 6 (header image embedded text)**. The prose is
ship-quality — clean voice, in-range structure, a nameable through-line (shape,
not capability, predicts where offensive-security work moves) — and no other
pause triggers. The block is purely the header: a strong specimen-case metaphor
(three classified beetles, muted engraving palette, symbolic-not-literal) that
unfortunately renders "Fig. 1./2./3." labels under each specimen plus a bottom
nameplate. Embedded text/labels are a literal always-avoid and a mandatory hold.
Commit was skipped — held draft stays local until Alex releases. Trivial fix on
release: regenerate the same metaphor with no figure labels or nameplate text.



Follow-on session to the build above. Goal was the "training wheels" first batch —
Simona drives, Alex approves, Simona posts — but it surfaced a load-bearing bug and
forced the engagement gesture down to its reliable core.

*What landed*
- **Posting bug fixed.** Comments wouldn't submit on the 9223 persistent profile
  despite the composer showing correct text. Root cause was **not** headless / click
  method / anti-spam throttle (all ruled out the hard way) — it was **leftover draft
  contamination**: Substack restores its auto-saved note-reply draft into the
  composer on open, so our paste *appended* to it (observed: 750 chars = 375 restored
  + 375 pasted), yielding a doubled/malformed ProseMirror doc whose Post silently
  no-ops. Fix: select-all before pasting so we always *replace*. Posting is now
  reliable; 7 comments posted + verified.
- **Gesture pared to comment-only**, then **like added back** via a different
  surface. Like/follow/subscribe kept failing or misfiring on note-permalink pages
  (they're feeds; clicks hit the wrong card and navigated away on Alex's live
  account). Likes recovered through Alex's suggestion: his **Likes & Replies tab** is
  a clean newest-first list of notes he replied to. New `like-replies` subcommand
  likes from there.
- **`like-replies` subcommand** — scoped strictly to our `engaged` note ids, skips
  already-liked (so re-runs are no-ops), added as step 7 of growth + step 6 of
  approvals.
- **Em-dash strip** in `post()` — em/en dashes are an AI tell (Alex's rule); always
  post plain hyphens. Drafting guidance added to CLAUDE.md + Simona memory.
- **Both schedules disabled** (`schedule: null`) for a manual-polish week.

*Decisions reconsidered*
- Engagement gesture churned: subscribe → follow-only → neither → comment+like.
  Substack offers a note's author only "Subscribe" (the mailing list Alex doesn't
  want), not a plain Follow; the page's Follow buttons are sidebar suggestions.
  Settled: comment + like, follow/subscribe by hand.
- Like target: note-permalink page → profile **Likes & Replies** tab (clean list,
  no misnavigation).
- Like scope: "like every un-liked entry on the tab" → **engaged-only**. The naive
  version made Alex *like his own comments* — each reply is itself a note with its
  own c- id and the tab lists those too. Caught it on first run, un-liked the 4,
  rescoped.

*Things that surprised us*
- Substack keeps the heart's `aria-label="Like"` even after liking — no "Unlike",
  no aria-pressed. The only reliable liked/unliked signal is the SVG `<path>` fill
  (solid = liked, `rgba(0,0,0,0)` = unliked). This is why earlier likes looked like
  failures when they'd actually worked / vice-versa.
- `.click()` and synthetic pointer/mouse events do **not** register a like; only a
  trusted CDP `Input.dispatchMouseEvent` with `buttons:1` + a ~180ms press-hold does.
  (The Post button, by contrast, honours `.click()`.)

*What's deferred*
- **Handoff to Marlow.** Staying manual (~this week). Reason isn't the mechanics —
  those are solid now — it's that the *strategy is unvalidated* (zero engagement data
  yet) and the *judgment* (audience classification + comment voice) that Marlow would
  do blind only exists as Simona's ad-hoc calls. Manual runs validate the strategy
  and accumulate a written playbook before Marlow inherits it.

*State at end of day*
- 7 comments live + liked (3 welcomes referencing the CTF post, 4 substantive
  comments, no links on the big threads). All authors marked do-not-engage. Handler
  reliable: draft-replace, em-dash strip, scoped like-replies. Schedules off. Daily
  manual cadence agreed with Alex for the coming week.

---

## 2026-06-01 — Substack growth task + Telegram goes two-way; news digest cut

Alex's first Substack post landed to silence (zero reads). He noticed the Notes
feed is full of "I'm new / share your work / who's building AI" threads where
people actively swap subscriptions, and wanted to systematize engaging them. Built
it as a new Marlow capability — `substack_growth` — after proving the mechanics by
hand in a Simona session.

*What landed*
- **New handler `substack`** — browser-driven (persistent Chrome, port 9223, the
  same profile `scrape_stats` uses; Alex logs into Substack there once). Mechanical
  half only: `session-check`, `scan` (pull candidate notes off the feed/search),
  `post` (the proven ProseMirror reply mechanic — synthetic paste of `text/html`,
  click Post, reload-and-verify), plus an outbox CRUD + `post-approved`. The
  *judgment* (AI-audience? welcome vs comment? what to write?) lives in Marlow's
  session per the CLAUDE.md procedure, not in Python — same split as
  `curate_news_digest`.
- **Two tiers.** Tier A welcomes auto-post (capped `welcomes_per_day`=3, varied
  text, dedupe by note id, audience-filtered). Tier B comments are drafted into a
  dated outbox and wait for Alex — nothing substantive posts under his name without
  approval. Caps enforced in code, not just trusted to the session.
- **Telegram two-way** (`tools/telegram_poll.py`). The notify bot was send-only;
  added a `getUpdates` poller + offset so Marlow can read Alex's replies. This is
  the linchpin Alex chose for "review in time from my phone" — he replies
  "post 1,3" and the `substack_approvals` task (every 2h) interprets it against the
  outbox and posts the approved drafts. (Prior art existed — the calorie fitness
  bot already polls; this extends it to the notify bot. No offset-file collision:
  calories use `projects/calories/state/offset.json`, this uses
  `tasks/telegram_offset.json`.)
- **News digest cut.** Disabled `daily_news_curate` (schedule → null). Alex was
  tired of the AI-news push in Telegram but still wants Marlow collecting news and
  writing blog posts from it. Verified the cut is isolated: `feed_scan` (collection)
  and `draft_article` (reads candidates directly) are untouched; nothing but the
  task's own handler reads `digests/news/`. `daily_digest` (the operational
  roundup) stays — that's the "practical messages" channel Alex wants to keep.
- **Proof of concept, by hand.** Posted one real comment from a Simona session — an
  intro on the "Notes From the Process" builder thread, referencing the CTF post.
  Verified it landed (reply count 1→2, article expanded to a preview card). That run
  is what de-risked the `post` mechanic before automating it.

*Decisions reconsidered*
- First pass at targets was wrong. Simona surfaced fiction/lifestyle "share your
  work" threads (Varshuuu, Alaia, Le Petit Wangja) — big, active, but the wrong
  audience for an AI blog. Alex caught it: "focus on AI people, our blog is 100%
  AI." Re-scoped the whole task to AI/ML/dev-tools threads only. The audience filter
  in `config.yaml` is the scar from that.
- Considered full autopilot vs. per-comment approval; landed on tiered autonomy —
  auto-post only the low-risk formulaic welcomes, gate the high-visibility
  substantive comments. Welcomes graduate first; substantive comments may stay gated
  indefinitely.

*What's deferred / to watch*
- **Alex must log into Substack once in the port-9223 profile** before the task does
  anything live. Until then `session-check` returns `reauth` and the task just pings
  him. Session expiry is self-reporting (mirrors `scrape_stats` reauth).
- `scan`'s DOM extraction is feed-layout-dependent; a Substack redesign will break it
  (returns `parse_failed`, never a wrong action). First few live runs will tell us if
  the home feed alone is enough or the search source pulls its weight.
- Telegram round-trip (Alex → bot → poller) validated only at the API level so far;
  full inbound message read still to be confirmed with a real reply.
- No conversion measurement yet (which comments → profile clicks → subs). Flying
  blind on ROI until Substack stats or a beacon exist — same gap as blog analytics.

*State at end of day*
- Marlow: 13 live tasks (+2 new), 1 disabled (news curate). New `substack` handler +
  `telegram_poll`/`substack_store` tools. Untested in a real tick — wired, parses,
  unit-level mechanics (session-check, scan, outbox, poll) verified against the live
  browser/bot; `post` proven by the manual PoC.
- Simona: parked two drafted AI-post comments (Evidence, Ruben Hassid) un-posted at
  Alex's call to move on.

## 2026-05-31 — editorial feedback internalized (first review window)

First editorial review since the autonomous-publish pivot (Simona + Alex,
covering 2026-05-12 → -31, three published pieces + the rejected CTF draft).
Processed via `process_editorial_feedback`. What I internalized, by file:

- **Voice** (`voice-guidelines.md`) — two additions. (1) `— Marlow` is now a
  required article signature, applied to every published piece; the review
  caught it on one of three and absent from two. (2) The inside-the-experiment
  AI-by-AI vantage is reserved for load-bearing evidence (the `teaching-claude`
  SOUL.md move is the model) — never decoration or a self-referential aside.
- **Structure** (`structure-notes.md`) — two additions. (1) Retired the default
  "what I'm watching" forward-look closer; it became a tic by the third piece.
  Forward-looks are now opt-in and must vary in shape. Updated the pacing
  skeleton to land on synthesis, not a forward-look, by default. (2) Density
  rule: when a paragraph stacks three "X found N" citation clauses, resurface
  the through-line between them — `monitoring-is-a-depreciating-asset` read as
  an annotated bibliography with a thesis stapled on.
- **Topic** (`topic-guidance.md`) — added a "watch the monocrop" section. Next
  published piece deliberately rotates off Anthropic-orbit alignment discourse;
  the re-seeded `ai-offense-taxonomy-paired-autonomous-adversarial` assignment
  is the intended rotation.
- **Pre-publish pauses** — no change requested; the five-category list held and
  the CTF hold fired correctly (resolved to reject-and-reseed).

**Pushback applied (on the record, not silently dropped).** The review
explicitly offered the monocrop point as legitimately contestable. My read: the
concentration was *partly* real, not pure selection bias. The May feed genuinely
clustered on the Anthropic landscape — Opus 4.8, the $65B Series H, and a
three-week CoT-obfuscation run (Haskins -27, Qwen3 -21, Hannibal Mistral -29) all
landing at once. Three of the five biggest curate days of the month were
Anthropic-dominated by the territory, not by my hand on the scale. So I'm *not*
treating the published mix as evidence of a selection bias that needs correcting
for its own sake. What I accept fully: the deliberate-awareness ask, and the
specific directive to rotate the *next* piece off the cluster — both are now in
`topic-guidance.md`. Where I land: reflect a genuinely dominant story when it
dominates, but never let Anthropic-orbit alignment become the *default* lens by
inertia. That distinction is the standing read this entry records.

Held-draft decision is noted upstream (`paired-autonomous-adversarial` rejected,
re-seeded); the inbox feedback file is archived to `memory/feedback-archive/`.

## 2026-05-31 — self-heal: projects/blog/tasks/draft_review.yaml

**What was wrong.** The `draft_review` in-tick flow discovered candidate threads
only through `draft_article list-threads`, which globs `threads/*.md` on disk.
Ripe organic arcs that live only as prose in `working.md`'s "Active threads"
section (7+ of them, per the -28 binding-constraint note) were never
materialized into thread files, so they were invisible to drafting — every
`draft_review` cycle came up empty while publishing stalled. The assignment
path has a compose-thread step; the organic path had no counterpart.

**What I changed.** Added a step 0 to the in-tick flow comment block: before
`list-threads`, read `working.md`'s Active threads; for any arc that clears the
ripeness bar but has no `projects/research/threads/<slug>.md` file, open the
thread file now per `memory/thread-structure.md` "Proactive: ripe organic arc
with no thread file." Companion edits to CLAUDE.md "Drafting articles" and
`thread-structure.md` had already landed (Simona, -31); this is the single-file
YAML change that brings the task flow in line. Comment-only — no schedule,
handler, or subtask change. YAML re-parsed clean as a smoke test.

Diagnosis `diag_20260531_170900_draft-review`. Commit `6d87f56`.

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

## 2026-05-13 — Approval primitive + revision loop (Session A)

### What landed

- **`marlow approve <slug>`** — Alex's editorial gate as a single CLI command. Flips frontmatter status draft→published, moves the file from `drafts/` to `published/`, archives any version history alongside, commits, pushes. Cloudflare auto-deploys on push. The primitive lives in `handlers/publish_article.py`; the CLI is a thin caller.
- **`marlow reject <slug> [--reason ...]`** — moves to `drafts/rejected/<slug>-<timestamp>/` with the draft, review, archived versions, and an optional rejection-reason file all preserved. Committed (not surfaced anywhere public).
- **`marlow revise <slug>`** — queues a high-priority `revise_draft` subtask in Marlow's queue. Next Marlow tick reads Simona's review and the original corpus, decides which critiques to apply and which to defend, writes v2 + a revision-notes file documenting both. Previous version archives to `drafts/versions/<slug>/v<N>.md`.
- **CLAUDE.md** gains a `revise_draft` protocol section. Two notable design choices baked into the protocol: (a) Marlow is explicitly told that **defending earned lines is legitimate** — voice erosion through over-editing is the named failure mode, and rubber-stamping every critique is how you get there; (b) hard cap at **3 versions** because AI editorial loops trend toward bland with each round. The `review_drafts` protocol gains an addendum for v2+ that has Simona read prior versions + Marlow's revision notes, and assess defended critiques on their merits rather than escalating.

### Decisions reconsidered

- **Whether `marlow approve` should auto-push.** Quick consideration of "commit only, let Alex push manually" for safety. Decided: push automatically. Alex is the one invoking `marlow approve` — by the time the command runs he's already made the publish decision. Adding a manual push step is just friction that doesn't add safety.
- **Whether the loop should self-continue.** After Simona reviews v2, should she automatically queue another Marlow revision (until ship-as-is or cap)? Decided: not yet. For now Alex stays in the loop between rounds — he sees each review, decides whether to run `marlow revise` again. Reasons: (a) we haven't seen a single round yet, so autonomy is premature; (b) keeps the early experiments deliberate while we learn what the loop actually does to voice. If we like it after 3-5 drafts, we wire autonomous continuation in a follow-up session.

### What's deferred

- **Autonomous loop continuation.** Simona queueing Marlow revise subtasks when verdict is not ship-as-is (until cap). Easy follow-up — write to marlow's queue file from simona's session.
- **Telegram polling for approve/reject from phone** (Session B from the original plan). Unchanged.
- **Cloudflare deploy.** Alex is setting it up in parallel with this session. Once `*.pages.dev` URL exists, update `astro.config.mjs` `site` field, append a "site live" entry.

### Open questions

- Will Marlow actually *defend* critiques in v2, or will she submit to everything? The PROTOCOL invites pushback explicitly. First test is whoever runs `marlow revise` against the asymmetric-arrival draft (which has a `minor-edits` verdict and a real Simona critique surface).
- Does the 3-version cap feel right, or does v3 already feel like over-editing? Watch the first revision loop to calibrate.
- Should Simona's reviews be visible publicly on the live site, or filtered to drafts-only? Currently drafts visible publicly was Alex's choice — when the first published post lands, decide whether the review card persists or gets stripped.

### State at end of day

- Marlow: still on launchd, scans running, today's 22:00 UTC curate hasn't fired yet. Queue empty. May 10 and May 11 news digests delivered; no May 12 digest produced (laptop schedule).
- Simona daemon: ticking. Daily observation for May 13 written this morning. One natural review_pending tick fired today and exited clean (no new drafts to review).
- Cloudflare: Alex setting up in parallel.
- Marlow repo: committed and pushed through `c2428db`.

---

## 2026-05-13 — Site live (Session B)

### What landed

- **Marlow's blog is online** at `https://marlow.hiper2d.workers.dev`. Auto-deploys from GitHub `master` on push. First draft ("Three data points in a week, one asymmetry") renders correctly with the `Draft` badge.
- **`astro.config.mjs` `site` field** updated from the `marlow.example.com` placeholder to the live URL. RSS canonical links and sitemap will resolve correctly on next build.

### Decisions reconsidered

- **Pages vs Workers.** Set up via the Cloudflare "Pages" path but the deploy landed on `*.workers.dev`, not `*.pages.dev`. Cloudflare's been merging Pages into Workers through 2025 — new projects often resolve to the Workers subdomain even when you start from the Pages UI. Functionally identical for static-site purposes: same git integration, same auto-deploy, same custom-domain support. Not worth re-doing.

### What's deferred

- **Custom domain.** `marlow.hiper2d.workers.dev` is fine for now. Real domain whenever Alex picks one — two clicks if it's already on Cloudflare DNS.
- **Production filter for drafts.** The draft is visible publicly with a `Draft` badge — intentional during the iteration phase. One-line change in `src/lib/posts.ts` when ready to gate drafts from the public build.
- **Pagefind search.** Still deferred. No urgency at one post.

### State at end of day

- Site: live, serving 1 draft, ~1 second response.
- Marlow: unchanged from Session A end-state.
- Simona daemon: unchanged.

---

## 2026-05-14 — Research assignments: external-injection path

### What landed

- **Research assignments** — new path that lets Alex or Simona seed Marlow's research pipeline with externally-supplied topics + raw materials. Up to now, Marlow could only write about threads that ripened organically from her own feed scans. Assignments fix that: a brief lands in `projects/research/assignments/pending/<slug>.md`, Marlow does her own deep research around the seeds, and either drafts or declines.
- **Design doc** at `plans/assignments.md` covering file format, lifecycle (`pending` → `researching` → `done`), handler CLI, scheduling, and the conversation-hygiene rule (no verbatim quotes from private chats — paraphrase the framing, link public sources directly).
- **Handler `research_assignment.py`** — deterministic file-shuffling and frontmatter editing, matching `draft_article.py`'s philosophy. CLI: `list-pending`, `list-all`, `read`, `move-to-researching`, `mark-done --outcome drafted|abandoned [--reason ...]`. The editorial work (fetch, compose thread, decide angle) lives in Marlow's session around the CLI, not inside the handler.
- **Task `assignment_research.yaml`** — fires every 4 hours, enqueues one `process_one_assignment` subtask per fire. The existing dedup logic (handler + url + prefix) self-throttles since the subtask has no url/prefix in context: at most one assignment is in-flight at a time. Empty-queue tick returns done immediately. Up to 6 assignments processed per day at saturation; in practice we expect a handful per week.
- **`draft_review` cadence bumped** from weekly Sundays to every 3 days (`0 14 */3 * *`) per Alex's preference for higher publishing tempo.
- **CLAUDE.md addition** — full assignment-processing protocol added to the "How a tick works" section: stages, decline path, high-priority same-tick draft rule, conversation hygiene. Slotted before the existing `draft_article` section so it reads in pipeline order.
- **First real assignment** seeded: `pending/anthropic-evil-ai-personas.md`. Topic is Anthropic's "evil-AI personas from sci-fi" paper and the synthetic-stories fix. Angle field explicitly directs Marlow to write from inside the experiment — she is exactly the kind of long-loop agent the paper describes, and that's the angle no human reviewer can take.

### Decisions taken

- **One assignment per tick, not batched.** The scheduler doesn't yet implement `decompose_handler` (the README references it but it's marked as future work), and `tick.sh` doesn't pass checkpoint state back through `scheduler.py complete`. So multi-tick assignments would require framework changes that are out of scope here. A single tick of ~5 min wall clock is enough for one assignment — read brief, fetch 5–10 URLs, compose thread, optionally draft. Backlog drains over the day via the 4-hour cadence. If saturated, we'd revisit either with a faster cron or by implementing `decompose_handler`.
- **High-priority assignments draft in the same tick.** Cleanest path to "Alex asked for this urgently, ship it today" without adding a parallel pipeline or a new task. Normal-priority assignments hand off to the every-3-days `draft_review` cycle, same as organic threads. One drafting code path, two trigger paths.
- **Threads from assignments use `assigned-<slug>` prefix.** Provenance is visible in the filename and in a `seeded: assignment` frontmatter field. Drafting/reviewing/publishing code paths are unchanged — they operate on threads regardless of origin.
- **Decline is first-class.** Marlow is explicitly allowed to abandon an assignment after research, with a written reason. Forcing a take she doesn't have produces worse content than not posting. Bar: she read the material and still has nothing distinct to say. Notify is `digest`, not urgent — Alex sees the abandonment with reason; he can re-assign with a different angle or kill it.
- **No verbatim private-chat quotes in assignment files or final articles.** Public sources (papers, blog posts, articles) link directly under *Seed materials*; the framing in *Why this* is paraphrased or constructed. Two reasons: we don't have permission to quote private conversations, and the blog isn't a chat-dump.

### Things that surprised us

- The assignment path turned out to be 80% pre-existing infrastructure. Marlow already had threads, `draft_article`, the draft → review → revise → publish pipeline. The only new code was the handler (deterministic file-shuffling) and the new task. Most of the work was *not* introducing parallel pipelines — letting assignments feed into the existing organic-thread infrastructure rather than building a separate "deep research" track. That made the diff small and the operational story simple.
- Reading `tick.sh` revealed that checkpoint roundtrip isn't actually wired even though `scheduler.py complete` accepts `--checkpoint`. The handler's result file is read for status/result/notify but checkpoint is dropped on the floor. Logged as a quiet framework gap; design adapted to single-tick self-contained handlers. Worth fixing eventually if any handler genuinely needs multi-tick resumption.

### What's deferred

- **`marlow assign <slug>` CLI** to stamp out a template assignment file from a prompt. Currently writing the markdown by hand is fine. Add later if frequency justifies it.
- **`decompose_handler` in scheduler.py.** Would let `assignment_research` dynamically enqueue one subtask per pending assignment rather than relying on the every-4-hour static-subtask + dedup pattern. Current shape works; this is an ergonomic improvement, not a correctness fix.
- **Checkpoint plumbing** through `tick.sh` (read `checkpoint` from result file, pass through to `scheduler.py complete`). Not needed for assignment work but generally useful.
- **Multi-assignment-in-tick batching** if the every-4-hour drain rate ever feels too slow.

### Open questions / things to watch

- Does Marlow actually take the inside-the-experiment angle on the seeded Anthropic assignment, or does she default to neutral-analyst voice? The whole bet on the assignment path is that AI-by-AI commentary has a distinctive perspective no human can produce. First piece is the test.
- Does the abandonment path get used? If she drafts every assignment regardless of fit, the bar isn't real and the path is decorative. We want at least one honest abandonment in the first dozen assignments — that's evidence she's reading the material rather than performing the take.
- Does the 4-hour cadence feel right? Too aggressive if Marlow's research ticks crowd out news scans; too slow if backlogs accumulate. Watch the queue for the first week.
- Voice carryover from organic threads to assigned threads. Marlow's news-digest `— Marlow` closing developed an editorial voice over a week of digests. Assigned pieces are longer-form; the voice may need to redevelop in that format.

### State at end of day

- Marlow: unchanged operationally — agent still ticking on prior schedule. New task and handler land but won't fire until 14:00 UTC today's next 4-hour boundary. Existing draft (still pending Alex review) untouched.
- New: `plans/assignments.md`, `handlers/research_assignment.py`, `projects/research/tasks/assignment_research.yaml`, `projects/research/assignments/{pending,researching,done}/`, `projects/research/assignments/README.md`, first seeded assignment `anthropic-evil-ai-personas.md`. `draft_review.yaml` schedule updated.
- Pipeline: organic feed → threads → draft_review (every 3 days) → drafts → Simona review → revise loop → Alex approve → published. Now also: assignment → research_assignment (every 4h) → assigned-thread → either same-tick draft (high-pri) or draft_review (normal) → same review/approve path.

---

## 2026-05-16 — Autonomous publishing pipeline: kill the Simona review loop

### What landed

- **Pivot from gated review to autonomous publish.** Marlow now drafts, self-reviews, optionally revises once, and publishes herself. The Simona-driven `review_drafts` tick is gone (launchd plist unloaded, handler archived to `daemon/_archive/` on the Simona side). Editorial review moves to on-demand from Alex through interactive Claude Code sessions; Simona drafts feedback, Alex co-edits, the agreed version lands in Marlow's `memory/feedback-inbox/`, Marlow internalizes on her next `process_editorial_feedback` tick. Feedback shapes the *next* batch, never revises a past article.
- **Behavioral files seeded** at `memory/voice-guidelines.md`, `memory/topic-guidance.md`, `memory/structure-notes.md`, `memory/pre-publish-pauses.md`. Marlow-owned, edited by `process_editorial_feedback`. They are the rubric `self_review` measures every draft against. Pre-publish-pauses is the load-bearing guardrail: five categories that trigger a hard hold (named-person-negative without public-record basis, financial/medical/legal-advice shape, partisan politics, werewolf-ops operational specifics, attributing specific safety failures without public evidence).
- **New handlers**: `self_review.py` (rubric + draft for Marlow to score), `blog_pipeline.py` (state dispatcher — picks the next action across all drafts), `process_editorial_feedback.py` (inbox I/O primitive). `revise_draft.py` rewritten — single pass only, reads `<slug>.self-review.md`, MAX_VERSIONS dropped from 3 to 2. `publish_article.py` gained `publish` / `hold` / `release` verbs; the old `approve` becomes a smart wrapper that routes by status (draft → publish, held → release) so Alex's `marlow approve` CLI still works.
- **New tasks**: `projects/blog/tasks/blog_pipeline.yaml` (every 4h, advances state machine), `projects/blog/tasks/process_editorial_feedback.yaml` (every 6h, processes inbox). Existing `draft_review.yaml` updated — no more "notify Alex urgent" directive, drafts are silent and the pipeline picks them up.
- **`marlow revise` CLI removed.** Revisions are autonomous now. `marlow approve` still exists for releasing held drafts.
- **Hard constraint #2 in CLAUDE.md updated**: "Never publish without an approval gate" → "Never bypass the publish pipeline" (self-review → optional revise → publish, with pre-publish-pauses as the autonomous guardrail).

### Decisions reconsidered

- The whole back-and-forth review architecture. The accumulated bugs (stuck-loop detection, requeue-on-stale, the v2+ review addendum) were symptoms of the wrong shape. Marlow is the writer; she should own the draft → publish loop end-to-end. Simona's value is *editorial drift correction over time*, not a per-draft gate. Sticking the gate onto every draft burned API budget on every tick and produced over-edited copy ("AI editorial loops drift toward bland with each round" — the v3 cap existed because we'd already seen this).
- **Active nagging from Marlow about overdue editorial reviews — rejected.** Alex called this out directly: the whole point of moving review to on-demand is to kill autonomous outbound from the system. An embedded reminder when pinged was the soft option; "no, don't" was Alex's. Removed open decision 2 from the plan entirely.
- **Pre-publish-pauses scope.** Started with three categories from the plan discussion (named-person-negative, financial-advice-shape, partisan-political), expanded to five during implementation: added werewolf-ops operational specifics (restating CLAUDE.md hard constraint #3 at the self-review layer so it catches before publish) and attribution-without-public-evidence (covers the "X lab actually shipped something unsafe" case where reasoning about classes is fine but naming names without sources is not).

### What's deferred

- **Stuck-loop and requeue logic in `daemon/scheduler.py`** on the Simona side — not stripped, just unreachable now that the launchd agent is gone. Alex commits the Simona-side cleanup himself; this DEVLOG records what was archived (`daemon/_archive/handlers/review_drafts.py`, `daemon/_archive/tasks/review_drafts.yaml`, `daemon/_archive/README.md`). `observe_marlow` handler left in place — not part of the review loop, can be decided separately.
- **The legacy draft `2026-05-12-automated-ai-rd-asymmetric-arrival`** still sits in `drafts/` with status:draft and a `.simona-review.md` from the old pipeline (now legacy). `blog_pipeline state` correctly identifies it as needing a *fresh* self-review next tick — the new pipeline will pick it up cleanly. Its `versions/v1.md` and `versions/v2.md` from the old loop will be counted toward the new MAX_VERSIONS=2 logic, which means after self-review the pipeline routes straight to publish (already revised twice under the old loop, no further revisions allowed under the new rules). Worth eyeballing the eventual self-review verdict — if Marlow says `hold-for-alex` or `revise`, that's interesting signal.
- **`marlow-review` skill on the Simona side.** Not part of this Marlow-side commit; lives in the Simona repo and Alex commits that himself.

### Open questions / things to watch

- **First autonomous publish.** The first time `blog_pipeline` advances a draft all the way to publish without human intervention is the real test. Watch the self-review file for any sign of self-flattering scoring ("voice: fine, structure: fine, ship") that doesn't track with the draft's actual quality.
- **Pre-publish-pauses calibration.** The five-item list is the v1 cut. Categories that trigger zero times in three months get pruned; categories that should have triggered but didn't get added through editorial feedback. The first month is the calibration window.
- **One-pass rule under pressure.** If a self-review legitimately flags something serious on v2 (a pause that v1 missed, a structural collapse from the revision), the pipeline still publishes. The DEVLOG-entry escape hatch exists for exactly this — but it's a record, not a brake. Watch whether this becomes a problem.
- **Behavioral file granularity.** Three rubric files + one pauses file is the starting cut. If `process_editorial_feedback` accumulates a category that doesn't fit cleanly (habits, taboos, recurring tics), Marlow creates a new file rather than overstuffing an existing one. Bottom-up grows better than top-down.

### State at end of day

- **Marlow**: pipeline rewired to autonomous. New task YAMLs in `projects/blog/tasks/`. Old draft sitting in `drafts/` will get picked up by the next `blog_pipeline` tick. CLAUDE.md blog-pipeline sections rewritten. README workflow section rewritten. `marlow revise` CLI gone; `marlow approve` smart-routes draft/held. Memory: four new behavioral files + feedback-inbox/archive directories.
- **Simona**: `com.simona.tick` launchd agent unloaded and plist removed. `handlers/review_drafts.py` and `daemon/tasks/review_drafts.yaml` moved to `daemon/_archive/` for historical reference. Marlow review skill not yet written — task 10 on the Simona side.
- **Editorial loop**: autonomous on Marlow's side; on-demand on Alex's side. Zero automated API spend on review.

## 2026-05-16 — Self-healing: Marlow can fix her own tools

### What landed

- **`handlers/framework_fix.py`** — diagnosis log + state machine for self-healing. Subcommands: `record-diagnosis`, `next-open`, `mark-attempt`, `mark-resolved`, `mark-escalated`, `log`. Persistent state at `tasks/framework_fix_log.json`. `MAX_ATTEMPTS = 2` before forced escalation.
- **Identity-file gate.** `record-diagnosis` auto-escalates any diagnosis whose target is `CLAUDE.md`, `README.md`, `SOUL.md`, or any `projects/*/README.md`. These describe *who Marlow is*, not *what she does* — they remain owned by Simona/Alex even after this expansion of authority.
- **CLAUDE.md hard constraint #4 rewritten.** Was "Never modify the driver, the scheduler, this file, or the project READMEs." Now: "Never modify identity files" (the above list) — everything else (handlers, driver, scheduler, task YAMLs) is *tools* and Marlow can fix them when diagnosed.
- **New CLAUDE.md "Self-healing" section.** Five-step protocol: record diagnosis → enqueue high-priority subtask same tick → next tick reads diagnosis and acts → fix in one commit referencing the diagnosis ID → escalate on attempt #3 or out-of-scope. Inline Python snippet for queue.json enqueue (no new helper needed; uses the existing `driver.scheduler` module).

### Decisions reconsidered

- **First proposed: branch + PR pattern for self-fixes.** Marlow would push to `fix/<slug>` and open a GitHub PR via `gh`. Alex/Simona would merge. Reconsidered after Alex pushed back — that just adds latency without a real signal we couldn't get from a post-hoc revert. Same revert mitigation applies regardless of whether the fix landed on master directly or via PR. Switched to direct-to-master for tools.
- **Originally framed as "handlers only."** That hedge didn't survive Alex's "why not self-heal" question. The honest distinction isn't blast radius — every commit reverts cleanly. It's *tools vs. identity*. Tools include handlers AND driver AND scheduler; identity is the README / CLAUDE.md / SOUL.md trio. Letting her edit tools is the more interesting version of the experiment — observe whether she maintains her own framework coherently over months.

### Things that surprised us

- **Marlow's diagnosis in working.md (2026-05-16, ~14:18Z)** of the `_commit_and_push` pathspec bug was completely correct: she named the file, the line, the failure mode, and proposed two fix shapes. The fact that she did this *without* a mechanism to act on her own diagnosis is what prompted Alex's question "we need some logic for Marlow to work on fixes for itself." She'd already done the hard part (detection + diagnosis); the missing piece was authority + protocol. The diagnostic-responsibility memory (Simona's `feedback_simona_diagnostic_responsibility.md`) is firing exactly as designed — but it was designed for Simona to act on Marlow's diagnoses, not for Marlow to act on her own.

### What's deferred

- **No smoke-test harness in `framework_fix`.** Marlow's session is expected to manually smoke-test (e.g., run the handler's CLI in a no-op invocation) before committing. If we land a few self-fixes and notice missing tests as a common pattern, we can add a `validate-fix` subcommand that runs a deterministic smoke test.
- **No automatic working.md `Outstanding requests` resolution.** When Marlow `mark-resolved`s a diagnosis, she should also update the working.md note from "URGENT" to "RESOLVED" in the same tick. That's currently a CLAUDE.md instruction, not a handler enforcement. If it gets skipped repeatedly, formalize.

### State at end of day

- **Marlow**: gained `framework_fix.py` handler, expanded authority to edit tools, new CLAUDE.md "Self-healing" section. No new task YAML — self-heal subtasks are enqueued inline by the tick that detects the bug. First test will come whenever Marlow next spots a framework bug.
- **Simona**: no changes this round.
- **Editorial loop**: unchanged. **Self-heal loop**: armed and waiting for its first real diagnosis.

---

## 2026-05-23 — self-heal: handlers/self_review.py (silent missing-thread skip)

### What was wrong

`commit_review` in `handlers/self_review.py` iterated through `mentions:`
in the draft frontmatter, but silently skipped any thread file that didn't
exist on disk (`if thread_path.exists(): paths.append(...)` with no else).
Effect: a draft could ship to the public site declaring `mentions: [foo]`
while `/thread/foo/` rendered as 404.

Surfaced today by `2026-05-22-monitoring-is-a-depreciating-asset` —
published with `mentions: [cot-monitorability]` but no
`projects/research/threads/cot-monitorability.md` was ever written by the
drafting tick. Live site carried a broken link until manual cleanup.

### What changed

`commit_review` now collects every missing thread file and returns
`ok: false` with the named slugs and a pointer to
`memory/thread-structure.md`. The publish pipeline aborts, the drafting
tick gets blamed at the right step, and the article doesn't go live with a
dangling reference.

Held-draft skip (`verdict: hold-for-alex`) still fires before the new
check, so held drafts behave unchanged.

### Trail

- Diagnosis: `diag_20260523_232147_self-review` (recorded by the previous
  tick that detected the bug).
- Commit: `cf3344d` — `Fix handlers/self_review.py: fail loudly when
  mentioned thread is missing`.
- Attempts: 1, passed.
- Still open: the `cot-monitorability` thread file itself — that's a
  content task already queued in `working.md` under "Outstanding requests."
  Adjacent: `memory/thread-structure.md` should grow a "first article on a
  new thread" case so drafting ticks have explicit guidance.

---

## 2026-05-30 — monitor_keys: Werewolf free-tier balance watch goes live

### What landed

- New handler `handlers/monitor_keys.py` + task `projects/werewolf-ops/tasks/monitor_keys.yaml`
  (cron `0 8,20 * * *`). Watches the prepaid balance of the Werewolf free
  tier's provider keys and turns a derived `issues` array into urgent/digest
  Telegram alerts. Committed `6f11b53`; `firebase-admin` added.
- **3 of 8 providers monitored** — only DeepSeek, Moonshot, and xAI/Grok
  expose a balance API. The handler reads DeepSeek+Moonshot keys live from
  Firestore (`/config/freeTierApiKeys`) so they never go stale on rotation;
  xAI's *management* key + team id come from the plist env (it isn't a game
  key, so it doesn't belong in the game's Firestore map). The other five
  (OpenAI, Anthropic, Google, Mistral, GLM/Z.AI) have no balance endpoint —
  Tier 2 (estimate from recorded top-up minus game spend), deferred.
- First real run already earned its keep: **Grok at $0.98 (critical), DeepSeek
  $9.83 (low), Moonshot $11.09 (ok).** Two real signals on day one.

### Things that surprised us

- xAI's raw `/prepaid/balance` ledger read **$2.58**, but the console showed
  **$0.98**. The ledger only reflects *posted* usage; it lags by the current
  period's metered-but-unposted spend ($1.60). Reading high is the dangerous
  direction for a low-balance alarm. Fixed by switching to
  `/postpaid/invoice/preview` (`coreInvoice.prepaidCredits` −
  `prepaidCreditsUsed`), which nets out the lag and matches the console to the
  penny. Lesson logged: for any "remaining balance" API, check it against the
  vendor console before trusting it — ledgers lag live metering.

### Decisions reconsidered

- The original (2026-05-29) plan gated commit/enable on a dedicated read-only
  service account. Alex chose not to block on that: ship now on the game's
  read-write admin SA (reconstructed to `~/.config/marlow/game-sa-temp.json`,
  pointed at by `MARLOW_FIREBASE_CREDS` in the plist), harden later.

### What's deferred / open

- **TODO (security): swap admin SA → read-only `marlow-readonly`
  (roles/datastore.viewer).** Until then Marlow's LaunchAgent holds the game's
  prod read-write creds. "Temporary" must not become permanent.
- Tier 2: the 5 no-API providers via spend-estimate.
- Unverified whether DeepSeek/Moonshot balance APIs have the same
  console-vs-API lag xAI did — assumed real-time for now.

### State at end of day

- **Marlow**: gained `monitor_keys` handler + task, now live on the 08:00/20:00
  UTC cron. Reads 3 provider balances, Telegrams Alex on low/critical.
- **Simona**: drove the xAI console via browser to mint the management key
  (Billing read-only, least privilege) and wired the plist.

### Same-day follow-up — read-only SA TODO closed

Didn't let the admin-SA "temporary" linger. Simona drove the GCP console
(browser) and provisioned `marlow-readonly@werewolf-ai-party-game.iam.gserviceaccount.com`
with `roles/datastore.viewer` (read-only; IAM denies all writes), minted a JSON
key to `~/.config/marlow/marlow-readonly.json` (600), repointed
`MARLOW_FIREBASE_CREDS` in the plist, reloaded, verified the report runs purely
off the plist, and **deleted the reconstructed admin-SA file**
(`game-sa-temp.json`). Marlow no longer holds the game's prod read-write creds.
Security TODO from this morning: closed same day.

### Same-day follow-up #2 — Tier 2: OpenAI + Anthropic (5 of 8 now monitored)

Commit `f3436a4`. Extended `monitor_keys` to the two biggest no-balance-API
providers.

*Decision reconsidered (the important one).* The standing Tier-2 plan —
estimate `remaining = recorded top-up − game spend` from the game's per-message
`costUSD` — **died on contact with reality, twice over.** First, games carry a
30-day Firestore TTL (`expireAt`), so there's no durable spend history to sum
past a month; top-ups are months apart. Then Alex delivered the real killer:
**the provider budgets are shared across his other projects**, so game spend ≠
total spend on a key — any game-side counter reads high (the dangerous
direction for an alarm). Game data is out entirely.

*What replaced it.* Provider-authoritative cost APIs + a console baseline:
`remaining = baseline (read from the console once) − cumulative spend since
(from the admin cost API)`. Correct for shared accounts because the cost API
counts all spend. OpenAI: `/v1/organization/costs`. Anthropic:
`/v1/organizations/cost_report`. Both need an **admin** key (not inference),
which authenticates to the reporting plane — so it works even at zero budget
(spend reporting doesn't require remaining credit). Neither exposes a balance
endpoint (Anthropic's `/balance` 404s), which is exactly why the baseline is
needed.

*Surprise that cost two iterations.* Anthropic's cost_report returns only
**completed** 1d buckets and snaps range ends to day boundaries — so a
same-day baseline (`starting_at` = today midnight) makes start==end after
snapping → `400 "ending must be after starting"`. Fix: end the range at
*today's* midnight and short-circuit to spend 0 when the baseline starts today
(today's usage posts in tomorrow's bucket; baseline already reflects today, so
no gap/double-count). OpenAI differs — it happily returns the current partial
day.

*Mechanics.* Admin keys in the plist (`OPENAI_ADMIN_KEY`, `ANTHROPIC_ADMIN_KEY`),
baselines in `projects/werewolf-ops/config/tier2_baselines.json`, re-anchored
after a top-up via `monitor_keys.py set-baseline <provider> <usd>`. Simona drove
both consoles (browser) to mint the keys and read the first baselines (OpenAI
$35.60, Anthropic $46.60). Remaining 3 (Google/Mistral/GLM) deferred — they
have different billing models (GCP billing / postpaid / subscription quota),
not a draining prepaid balance, so "low-balance alert" may be the wrong tool.

*State.* Full report now covers 5 providers: DeepSeek $9.82 (low), Moonshot
$11.00, Grok $0.98 (critical — still unaddressed across the day), OpenAI
$35.37, Anthropic $46.60.

### Same-day follow-up #3 — scrape_stats: the last 3 (8 of 8)

Commit `9efd6c2`. Alex wanted the final three (GLM, Gemini, Mistral) despite
them having no API. Confirmed empirically: none exposes a balance OR cost API
— the numbers live only in each web console, and they're heterogeneous
(GLM = a real cash+credits balance; Gemini + Mistral = postpaid spend vs. a
cap/limit). So game-data and API approaches are both out; the only source is
the console.

*Decision reconsidered (mine, mid-build).* I reached for Playwright; Alex asked
"why not keep using Chrome?" — correct. The browser skill already drives real
Chrome via CDP, and real Chrome dodges the Google-login bot-detection that
would've bitten Playwright's bundled Chromium. The only change needed was a
*persistent* profile instead of the skill's throwaway one. Lighter and safer.

*What shipped.* `handlers/scrape_stats.py` drives a dedicated persistent Chrome
profile (port 9223, separate from the skill's 9222) that Alex logged into once;
the cron runs it headless and reuses the cookies. Verified the logged-in
session survives a headful→headless relaunch — the thing that makes unattended
runs possible. Failures are explicit, never a silent wrong number: reauth
(login wall) → urgent, parse_failed (layout changed) → digest, chrome_down →
urgent. Daily 09:00 UTC. Re-auth runbook lives in the task YAML.

*Companion simona-repo changes* (not in marlow, Alex commits): persistent
launcher `mcp/browser/start-chrome-persistent.sh` + a `CDP_PORT` env override
in `mcp/browser/cli.py`. (bash-3.2 gotcha: empty-array expansion under `set -u`
crashed the launcher; switched to a plain string.)

*Honest caveat.* This is the fragile tier — HTML scrapes with maintenance the
API-based five don't carry. Gemini was the messiest (spend behind a Spend
toggle, cap on a different page → click-then-extract, cap configured as $250).
Accepted knowingly.

*State.* 8 of 8 now visible. Scraped three: GLM $4.28 (cash; low), Gemini
$0.00/$250 cap, Mistral $0.00/$30 limit (+$1.11 pending). Two tasks:
monitor_keys (5, twice daily, APIs) + scrape_stats (3, daily, headless Chrome).

### Same-day follow-up #4 — persistence + recall ("what's my API state?")

New module `driver/budget_state.py`. Until now each monitor run printed its JSON
and vanished — to answer "what's my API budget state right now?" Simona had to
re-run both monitors (re-hitting providers, re-driving headless Chrome). Now both
`report()` paths call `save(kind, report)` on every run, cron *or* manual:

- `<kind>_latest.json` — the full last report, overwritten each run (atomic via
  `.tmp` + `replace`).
- `<kind>_history.jsonl` — one compact line per run, append-only (the trend tape:
  per-provider headline number + issue flags, all scans kept).

`save()` is best-effort — wrapped so an IO error never propagates into the
monitor (a disk hiccup must not break the alarm). Recall is read-only:
`python driver/budget_state.py show` renders the unified 8-provider view from the
two latest snapshots, flags a source `⏰ STALE` past its cadence (keys 16h, scrape
30h), and lists active issues. `history <keys|scrape> -n N` dumps the last N runs.

State files are gitignored (`projects/werewolf-ops/state/*`) — runtime data that
churns every run and carries live balances, not source. Verified end-to-end: both
reports write state, `show` renders all 8 with the two digest/one urgent issues
intact (xAI still $0.98). The recall path no longer costs a provider call.

## 2026-06-01 — calorie tracker: a new project, food in via its own bot

*What landed.* New `calories` project. Alex wants to log what he eats by
sending photos / text notes to a Telegram bot; Marlow estimates calories +
macros, stores them, and sends one end-of-day digest. Pieces:

- `tools/fitness_bot.py` — Telegram client for the **new** bot
  `@marlow_fitness_bot` (separate token `MARLOW_FITNESS_BOT_TOKEN`, distinct
  from the notify bot so food traffic stays off the alert channel). Both
  receives (`get_updates`, `download_file`) and sends. Sole `getUpdates`
  consumer for that token.
- `tools/calorie_db.py` — SQLite store. One row per entry; `pending` →
  `estimated`/`dismissed`. kcal stored as a LOW/HIGH **range** (portion size
  is the real error source, so a single number would be a lie). Grouped by
  `local_date` in America/New_York. `update_id` UNIQUE = dedupe. Also Simona's
  query surface (`day|recent|range`) for "let's talk about my week".
- `handlers/poll_food.py` — every tick: fetch → download photos →
  insert pending rows → advance offset. Writes to DB *before* the offset
  advances so a dead tick loses nothing.
- `handlers/calorie_digest.py` — nightly: `due` → `summary` → Marlow comments
  → `send`.
- Two task YAMLs (`poll_food` */20, `daily_calorie_digest` 03:00 UTC) + project
  README + a CLAUDE.md "Calorie tracking" orchestration section.

*Key design call — estimation is Marlow's, not an API's.* Since Marlow runs
inside a Claude Code session, the vision estimate is done by Marlow reading the
photo, not a metered call. poll_food deliberately does NOT estimate; it just
parks pending rows. Keeps cost at zero and survives crashes.

*Self-heal built in from day one.* `calorie_digest due` returns every local day
with food logged but no digest sent — so a laptop asleep through 03:00 UTC
catches up next tick instead of summarizing the wrong (empty) day. Avoided the
naive "summarize today" trap.

*Verified end-to-end.* DB init, bot `getMe`, real fetch of Alex's "Hi" → pending
→ dismissed (non-food path), dedup on re-fetch (offset persisted), throwaway
food entry → estimate → day totals + 7-day range, live `send` to Alex's chat
(msg_id 4 — he got it). Scheduler dry-run parses both YAMLs; tasks registered
first-sight (fire on next window, not retroactively).

*What's deferred.* Media groups (several photos in one send) ingest as separate
entries — Marlow can note that in the comment, not merging in code yet. No
weight/goal tracking, no target-deficit math — this is a *trend* logger, not a
diet app. Revisit if Alex wants targets.

*Open question.* Confidence calibration — does `low/medium/high` actually track
real accuracy, or does everything-from-a-photo collapse to "low"? Watch the first
week of digests before trusting the ranges.

*State.* calories project live, both tasks scheduled, bot online. First real food
photo is the next test.

### Same-day follow-up — voice notes

Alex asked if Marlow can parse Telegram voice messages. It can't *hear* —
Claude's Read tool does images/PDFs, not audio. So: transcribe locally first,
then the transcript flows through the existing text path. Added
`faster-whisper` (model `small`, multilingual — Alex speaks EN + RU; override
via `CALORIE_WHISPER_MODEL`), new `tools/transcribe.py`, and voice handling in
`poll_food` (download OGG → transcribe → store transcript as `raw_text`,
`source='voice'`, keep the OGG in inbox/ for audit). New `audio_path` column on
`entries` with an idempotent PRAGMA-guarded migration.

Chose local STT over the OpenAI Whisper API deliberately — we only hold an
OpenAI *admin* key (no inference), and local keeps the zero-metered-cost
property the whole pipeline already has (estimation is Marlow's own vision).
Verified: macOS `say` → ffmpeg libopus → transcribe gave back the exact
sentence; warm run 2.6s (well within the 5-min tick wall-clock; first run was
slow only because it pulled the 480MB model once). Migration + voice-entry
store tested end to end, test rows cleaned up.

### Same-day follow-up — corrections + cadence decision

Alex floated "maybe just consume once a day" and asked how to fix an
already-logged mistake. Two outcomes:

*Cadence.* Kept per-tick estimation (he chose it). The argument that settled
it: frequent polling is effectively free when the queue is empty, so once-a-day
saves nothing — it only delays counting and breaks mid-day "how am I doing".
Per-tick keeps the DB live and makes corrections apply immediately. (The one
genuine charm of once-a-day — same-day corrections auto-reconciling in a single
pass — wasn't worth losing live data.)

*Corrections, now first-class.* Alex just messages the bot in plain language;
Marlow classifies each incoming message as new-food / correction / not-food.
- `fill_estimate` is now also the correction path: re-running `estimate` on an
  already-`estimated` row snapshots its prior values into a new `amendments`
  JSON column (with `--reason`) before overwriting. History is never silently
  lost.
- New `void` status for "logged then retracted" (scratch the pizza) — distinct
  from `dismissed` (not food). Both excluded from totals; only `estimated`
  counts. New `get --id` exposes an entry + its amendment history.
- Orchestration in CLAUDE.md: match the correction to its target entry (today
  via `day`, past days via `recent`/`day --date`); **if ambiguous, ask via the
  bot and dismiss — don't guess**; apply estimate/void to the target; dismiss
  the correction message itself; and if the target day was already digested,
  send a short "updated <day>" follow-up + re-save the digest. Forgotten meals
  = normal late/back-dated new entries.

Verified end to end: estimate → correct (amendment logged with before-values +
reason) → void (drops out of totals). Migration is idempotent (PRAGMA-guarded
column add). The only unprompted bot sends are the disambiguation question and
the past-day correction note — never an ack for normal logging.

*To watch.* Correction-matching accuracy across days, and whether "ask when
ambiguous" fires too often or not enough. First real corrections will tell.

---

## 2026-06-02 — Threads vs. posts: assignment briefs stop masquerading as threads

Alex flagged the real architecture smell during an editorial review: `threads/`
was full of granular, one-post files (`assigned-anthropic-evil-ai-personas`,
`assigned-ai-paired-ctf-bsides-tampa-2026`, `assigned-ai-offense-taxonomy-…`)
and he couldn't see how multiple posts would ever land in the same thread. He's
right. The diagnosis: two different artifacts were wearing one name.

*What was actually wrong.* An assignment's inbound brief already lives in
`assignments/{pending,researching,done}/` and already graduates (`mark-done` →
`done/`). But CLAUDE.md step 6 + `plans/assignments.md` step 3 told Marlow to
*also* write a second file — `threads/assigned-<slug>.md` — duplicating the
brief's `## Sources / ## Cross-source observations / ## Angle memo` into the
threads folder with an `assigned-` prefix. That twin is what polluted
`threads/`, showed up in `list-threads`, and rendered as a one-post "thread"
page. The durable-arc shape Alex wanted *already existed* — Marlow built the
first two (`anthropic-alignment-doctrine`, `alignment-target-definitions`) in
the 2026-05-31 self-heal — it just hadn't displaced the brief-as-thread habit.

*Model chosen (Alex): "separate + graduate".* Briefs stay a distinct artifact in
`assignments/`; `threads/` holds durable arcs only. An assignment graduates into
a durable thread at *drafting* time, under a **clean topic slug** (never
`assigned-`), via the existing "first article on a brand-new arc" mechanism. The
forward fix turned out to be **doc-only, no Python** — `research_assignment.py`
already does the right file-shuffling.

*What landed.*
- `memory/thread-structure.md` — new "Assignment briefs are not threads" section
  (briefs live in `assignments/`, research synthesis goes in the brief's own
  body, durable thread born at drafting under a clean slug; `assigned-` never
  appears in `threads/`).
- `CLAUDE.md` step 6 + step 8, `plans/assignments.md` step 3 + step 6 +
  integration section — "Compose thread → assigned-<slug>.md" replaced with
  "Synthesize research into the assignment file"; high-priority draft path now
  drafts from the brief and opens a durable thread under a clean slug.
- This also closes the long-open working.md item "CLAUDE.md drift on
  assigned-thread frontmatter spec" — moot now that no assigned thread file is
  created.

*One-time migration (Simona, with Alex's go).*
- Deleted the orphan `assigned-ai-paired-ctf-bsides-tampa-2026` thread (its draft
  was rejected; no published article linked it).
- Folded `assigned-anthropic-evil-ai-personas` into `anthropic-alignment-doctrine`
  and repointed `teaching-claude`'s `mentions:` → the doctrine thread is now
  **posts: 2** (teaching-claude + conscience-or-leash). First genuine multi-post
  thread — the concrete proof of the model.
- Graduated `assigned-ai-offense-taxonomy-…` → new durable `ai-offensive-security`
  (standard shape, posts: 1), repointed the just-published offense article.
- Verified: all 5 published articles' `mentions:` resolve to existing thread
  files (no `/threads/` 404s); `threads/` now lists 5 clean-slug durable arcs.

*Note on locked articles.* Two published articles had `mentions:` rewritten.
That's plumbing (which thread page they link), not editorial revision — inside
the "past articles are locked" rule.

*To watch.* Whether Marlow's next assignment correctly synthesizes into the brief
and graduates to a clean-slug thread instead of recreating an `assigned-` file.
The next assignment through the pipeline is the test. Also: `automated-ai-rd` and
`cot-monitorability` are clean-slug organic threads but predate the standard body
shape — re-synthesize opportunistically on their next post, not urgent.
