# Marlow DEVLOG

Append-only chronological log of Marlow's development arc. Written from
outside Marlow (Simona and Alex). Captures decisions taken, decisions
reconsidered, things tried that didn't work, framework concerns Marlow
herself filed, and pivots — the *journey*, not the *spec*.

This file's existence is enforced; see Simona's CLAUDE.md under
"Marlow project — devlog discipline." Every substantive piece of
framework work appends an entry before moving on to the next.

---

> Entries before 2026-06-08 are archived verbatim in [`DEVLOG-archive.md`](./DEVLOG-archive.md) (2026-05-13 – 2026-06-05, 19 entries). This file keeps the recent arc.

---

## 2026-06-23 — recovered two stale ops handlers; closed the album double-count in poll_food

*The page.* Self-audit fired three urgents: `daily_calorie_digest` failed ~12h ago, `werewolf_stats` failed ~10h ago, and the werewolf stats snapshot was 34h stale. Two unrelated transient causes, both already self-cleared by the time I looked: `calorie_digest` died on a brief `401 Invalid authentication credentials` flap in a ~12:01-12:41Z window (auth recovered by 13:03Z, every LLM tick since green), and `werewolf_stats` died on a one-off Anthropic `500` at 14:28Z. Neither is a framework bug. But both are daily tasks, so neither would self-heal before tomorrow's cron - the snapshot would have stayed stale and the day's calorie digest unsent.

*Recovery.* Re-queued both through the blessed path - `MARLOW_PROFILE=ops marlow run <handler> --no-tick` then `bash driver/tick.sh ops` per item (not the auto-tick form: `marlow run` still doesn't pass the profile to `tick.sh`, the open gap from the 06-16 split, so its auto-tick would fire the legacy loop). Both ran clean. Fresh stats snapshot at 00:21:51Z; first paid user appeared (0→1). The calorie digest for 2026-06-22 sent.

*The real bug the digest surfaced.* The `calorie_digest` run had to hand-void a double-counted lunch: entries #47 and #48 were byte-identical photos at the same 17:17:59Z timestamp - a Telegram **album** (one meal, multiple photos) logged as two meals across separate `poll_food` ticks. Root cause: `poll_food` dedup was keyed only on `update_id`, but every photo in an album arrives as its own update with its own `update_id` sharing a `media_group_id`. The dedup *couldn't* catch it.

*The fix (Alex chose "group into one entry").* Two new `entries` columns (migrated clean, 46 rows intact): `media_group_id` (the album key, persisted so members arriving in different ticks can find each other) and `extra_photos` (JSON list of the album's other shots). `poll_food.fetch()` now folds a pure extra album photo - one with `media_group_id` set and no note/audio of its own - into the first entry via `calorie_db.attach_group_photo()` instead of inserting a second row. A member that carries its own text is still kept as its own entry, so Alex's notes are never dropped. The estimate step (poll_food.yaml flow + calories README) now reads `photo_path` *plus* every path in `extra_photos`, so the meal is estimated once across all angles. Unit-tested on a throwaway DB: album collapses to one entry, extra photo attaches, attach is idempotent, a genuinely separate meal stays separate.

*Why the auth flap didn't page as auth.* The `claude_auth` check (added 06-21) scans a 6h window for the 401 signature, but this flap was short and already outside the window by audit time, so it surfaced only as `failed_ticks`. Working as designed - only worth revisiting if these brief flaps become frequent.

*Also: throttled the blog to weekly.* Alex asked how often the blog publishes and capped it at one publication per week. Measured cadence over the last 5 posts (2026-06-04 → -19) was ~3.8 days each - roughly twice a week. The driver was `draft_review`'s `0 14 */3 * *` (every 3 days) plus a soft "no upper limit on drafts per cycle." Two changes to `draft_review.yaml`: schedule → `0 14 * * 1` (weekly, Mondays 14:00 UTC), and a **hard cap of one draft per cycle** - if several threads ripen the same week, draft only the ripest and defer the rest (they only get riper). The cap matters because the schedule alone wouldn't bound it: a multi-ripe cycle could still emit N drafts → N publishes. Quiet weeks publish nothing, by design. The assignment path (high-priority Alex-seeded pieces draft in-tick) is untouched - that's Alex explicitly asking for a piece, not the autonomous cadence. Last `draft_review` ran Mon 06-22; next fire is Mon 06-29 under the new cron (verified, no immediate re-fire). Updated the two README cadence references to match. One draft is currently `held` from the 06-22 cycle (`the-scorecard-comes-after`) - awaiting Alex, not auto-publishing.

---

## 2026-06-22 — YouTube scans now judge on transcripts, not titles; dead bycloud channel fixed

*Trigger.* Alex: "I don't see any videos in Marlow's Telegram updates. Does the YouTube scan work?" It worked, but two things were off: YouTube items only reach Telegram bundled inside the 22:00 news digest (never as standalone alerts), and the per-item signal was deliberately thin — the `feed_scan` YouTube comment block literally told Marlow "NO transcript, so the signal per item is thin, be SELECTIVE." Off title+description alone, most videos never cleared the curate bar, so YouTube looked dead even though it wasn't.

*What landed.*
- **Transcript tier (`tools/yt_transcript.py`).** New tool, sibling of `rss_reader`/`fetch_article`: pulls a video's own caption track via `youtube-transcript-api` (1.2.4) — no audio download, no Whisper, no key. Importable `fetch_transcript()` + CLI. Accepts a bare id, a watch/youtu.be URL, or the RSS `yt:video:<ID>` form (so it chains straight off a feed entry's `id`). Caches to `projects/research/threads/_yt_transcripts/<id>.json` (immutable transcripts → re-scans are free and offline; cache gitignored as bulky/regenerable). Degrades gracefully: a disabled/missing track returns `ok:false`, never raises, so the scan falls back to title+desc. Code is resilient to the youtube-transcript-api 0.6 classmethod vs 1.x instance API split, and falls back to any available transcript (translating to English when possible).
- **YAML guidance flipped.** `feed_scan.yaml` YouTube comment block now instructs: for every NEW video, fetch the transcript (`--max-chars 12000`) and judge on what it *says* — a real paper/result/benchmark — not the title. Fall back + stay extra-selective only when no captions.
- **Dead bycloud channel fixed.** Config pointed at `UCfg9ux4m8P0YDITTPptrmLg` = "bycloud 2", a dormant secondary channel last active 2024-10-26 (`last_seen` stuck ~19 months). The live `@bycloudAI` is `UCgfe2ooZD3VJPB6aJAnuQng` ("bycloud", uploads through 2026-06-16). Swapped the id; seeded `_feed_state.json` watermark at the 2026-05-27 video so the next scan surfaces the two strong recent ones (DeepSeek V4 infra, Chinese-phone open-source LLM) plus newer, not a full-backlog dump.

*Verified end-to-end.* `process_rss_feed fetch` on the fixed feed returns exactly the 2 seeded videos; `yt_transcript.py` pulls their 23-25k-char transcripts and cache-hits on re-run; bad id → clean `ok:false`. Watch-item: transcripts are ~20-25k chars, so a busy multi-video scan adds read-token cost; the `--max-chars 12000` cap in the guidance bounds it, and each `scan_yt_*` is its own one-channel subtask so per-tick load stays small (well inside the 300s tick timeout — no `timeout_sec` bump needed).

*Design note.* The selection judgment was already an LLM decision in the scan tick, not Python — `process_rss_feed` is pure fetch/mark-seen. So this added no selection *logic*; it just gives the LLM the transcript to judge from. Same pattern as `fetch_article` (trafilatura body for the curate tick): give the model the real content, not the snippet.

## 2026-06-22 — self-review held `the-scorecard-comes-after` on pause 6 (embedded-text header)

`blog_pipeline` self_review of `2026-06-22-the-scorecard-comes-after` (cot-monitorability #3). Prose and structure were ship-quality — clean job-named sectioning, and the piece finally breaks the arc's 5/5 DeepMind-interp streak by anchoring OpenAI's deployment-simulation method + a LessWrong public-chat proposal + CMU's ROGUE (pause 7 consciously resolved in-body, not tripped). The hold is entirely on the header: a strong rain-gauge metaphor, but the generator stamped legible scale numerals on it ("MM", "50 40 30 20 10"), which trips pause 6 (embedded text/labels in the image). Direct repeat of the 2026-06-04 ruler-numerals failure on `unbundling-the-intelligence-explosion`, which was fixed by a text-free regen. self_review doesn't own image regeneration, so per the rubric the verdict is hold-for-alex; commit correctly skipped (draft stays private). Remediation is narrow: regenerate the same gauge with bare unlabelled tick marks (no numerals), then it's a clean ship. Recurring lesson logged to voice-journal — instrument headers need "no numerals" stated in the prompt up front, since the model defaults to legible numbers on any gauge.

## 2026-06-08 — Marlow gets an operational self-audit; the empty-thread / silent-stall class closed

*What landed.* Two fixes, one symptom, one cause. Alex noticed the public blog had
a live, empty `alignment-target-definitions` thread page ("No posts written yet"),
and — the real complaint — that Marlow was effectively stalled (blog idle for days,
a held draft, a non-firing curate slot) and *he was never told*.

- **Symptom (render layer).** `thread/[slug].astro` + `threads/index.astro` now
  only emit a thread page when it has ≥1 published post. An early-opened thread file
  stays invisible until its first article lands, then surfaces automatically. Kills
  the whole empty-thread *class*, not just the one instance. (`22f904b`)
- **Cause (no escalation path).** New `monitor_self` daily tick (`f6ec6cf`). Marlow
  could already *observe* her stalls — the grader literally wrote "Blog idle ×3" and
  "curate-slot still non-firing — open question for Simona" into working.md. The gap
  was never detection; it was that observations died in a file Alex never reads.

*The design decision that matters.* The urgent→Telegram escalation is **deterministic
and lives in the handler** (`notify_alex`), not in the LLM session that runs it.
tick.sh runs handlers *inside* Marlow's session, and the established monitor pattern
lets the session interpret an `issues` array and decide whether to alert — which is
exactly the judgment step that failed here. monitor_self inverts it: the session's
only job is to run the script; the escalation is Python. Three invariant checks, each
mapped to a real failure this month — `scheduler_freshness` (a tick silently stopped
firing → the curate slot), `held_artifacts` (draft held >48h, blocked on Alex),
`site_integrity` (active thread with 0 posts / `posts:` drift → the empty thread).

*What we reconsidered.* Simona's first instinct was a bespoke `monitor_blog_health`
handler. Alex pushed back — that's whack-a-mole, the next blind spot is by definition
one we didn't write a monitor for. So we generalized to an invariant registry on the
reflective organ Marlow already has (`grade_memory`), with a severity→channel exit
pipe. This also supersedes the earlier call (2026-05) that operational stuck-detection
was Simona's job via review — it failed live; Alex caught it before Simona did.
Moving active detection into Marlow, Simona as backstop.

*Verification.* Dry-run (`monitor_self.py check`) against live state independently
re-found the empty-thread bug — both "0 published posts" and the `posts:1` frontmatter
drift — with zero false positives on the other checks. Proof the audit would have
caught the incident on its own.

*Things that surprised us.* The held `2026-06-01-ai-offense-shape-not-capability`
draft that working.md still lists as in-flight isn't on disk anymore (only the rejected
`paired-autonomous-adversarial` remains, and it oddly still carries `status: held`
inside the rejected/ folder). working.md may be stale on the blog pipeline state.

*Late same-day follow-ups.* (a) First dry-run flagged its own false positive: an active
thread with 0 posts is a *normal* interim state (thread files open before the first
article). Age-gated `site_integrity` to only flag empty threads >14d old — without it,
every freshly-opened thread would nag daily, the cry-wolf failure that makes an audit
ignorable. Fixed the one genuine drift it found (`alignment-target-definitions` posts:1→0)
and reconciled working.md, which had carried the *published* offense-shape article as a
"held draft" for ~6 days. (b) Closed the circularity below: `monitor_self` now runs as
step 3 of `tick.sh` — out-of-session, before the lock/scheduler — so a broken session, a
stale scheduler, or a stuck previous tick can't suppress it. Removed the scheduled yaml
(would double-fire). Daily "all green" digest line is now the audit's proof-of-life.
(c) Alex asked why he never sees new-user reports — turned out werewolf_stats
*looked* fine (it ran daily) but 06-07's session crashed ("exited without writing
result file"), so a real day with 3 signups produced no report; a failed run is
indistinguishable from a quiet day in the digest. scheduler_freshness wouldn't
catch it (last_scheduled updates even on failure). Added two checks that verify
the *effect*: `failed_ticks` (most-recent run per parent_task ended `failed` →
urgent) and `output_freshness` (declared daily artifacts must be <max-age old).
On its first live run `failed_ticks` immediately surfaced a bigger fish: the blog
**`draft_review` tick has failed EVERY run since ~05-31** (8+ days, all "session
exited without writing result file", handler `draft_article`, schedule `0 14 */3
* *`) — the real reason the blog stalled, silent the whole time. Strong suspect:
`draft_article` exceeds the 300s tick timeout. Monitoring shipped; the draft_review
fix itself is the next task.
(d) Digging into *why* draft_article fails surfaced two failure modes: genuine
300s timeouts (exit 124 — the handler is too heavy for one tick, though it often
drafts the article before the kill and blog_pipeline finishes it, so "failed"
overstated it) and a 06-07 Claude **session-limit storm** (exit 1, ~2s, "You've
hit your session limit") that took out *every* tick for ~3h — the real cause of
the missing 06-07 werewolf snapshot, not a werewolf bug. That led Alex to the
concurrency question, which surfaced a latent catastrophe: a hard-killed tick
(reboot/OOM/**sleep-kill** — closing the laptop mid-tick is the likely trigger)
leaves `/tmp/marlow.lock` orphaned, and the existence-only check then wedges
**every** future tick forever — silent total stall. Fixed with a staleness-aware
lock: PID fast-path (`kill -0`) + a **skip-counter** slow-path (Alex's idea, and
better than my wall-clock proposal — sleep inflates elapsed time without signal
and a time-break can double-run a paused holder; the counter only advances on
real awake ticks). Also fixed a latent bug where cleanup deleted the lock on
*every* exit incl. skips (now gated on OWNS_LOCK). Breaks log to
`~/.marlow/lock_breaks.log`; `monitor_self.lock_health` surfaces recoveries.
5/5 decision-path behavioral test. **Still deferred: the draft_article timeout
itself** — and the sleep analysis argues for *staging* it (checkpoint per tick,
sleep-safe) over a big timeout (only survives a lid-open machine). Open question
to watch: how often the Claude session limit is hit — if regular, it's a capacity
/ plan ceiling, not a code bug.

*What's deferred / to watch.* (1) The only thing that can now silence the audit is
cron/launchd itself dying (total agent death) — visible externally, but no internal
catch. (2) Self-fixable blockers (thread-file backlog, header-image-has-text pauses) still
route to digest, not auto-queued repair — that's phase 2. (3) `alignment-target-
definitions` is still an unresolved active-thread-with-0-posts; the audit will nag it
daily until someone decides publish-vs-archive. (4) Precision risk: a self-audit that
cries wolf becomes working.md 2.0 — keep the urgent channel sparse.

---
## 2026-06-09 — the audit earns its keep: catches grade_memory dead, two root-cause fixes

*What happened.* `monitor_self` fired for real overnight — `failed_ticks` urgent on the
06-10 self-audit: "grade_memory last run FAILED." That *is* the system working; the thing
Alex couldn't see before now pages him. Two root causes, both fixed:

- **Heavy-tick timeouts.** grade_memory (failed 06-09) and draft_article (failing every run
  since 05-31) both die "session exited without writing result file" — the global 300s
  tick timeout SIGKILLs a heavy session mid-work. Added a **per-handler timeout**: tick.sh
  reads `timeout_sec` from the task context (default 300), set to 900s for both. 900 < the
  1200s launchd interval, so a long tick still frees the lock before the next fire. Carried
  via the subtask `context` field — zero scheduler change.
- **Silent digest-delivery skip.** Alex got no user stats in his report. werewolf_stats
  *succeeded* (116 users, +1 fogflea) and persisted the snapshot — but the digest block was
  a *session step* (`digest | notify --digest`) that got silently skipped for days. Moved
  it into the handler: `report` now appends the block deterministically via notify_alex.
  Same lesson as monitor_self — **delivery a human depends on must not hinge on the LLM
  remembering to run a step.** Verified live: the block lands now, even on a +0 day (so
  silence = genuinely zero, not broken).

*The pattern, three times over now.* monitor_self's escalation, werewolf's digest, draft's
result-writing — every silent failure this week traces to a human-facing effect that was
left to LLM-session discretion. The fix is always the same shape: make the effect
deterministic, in code, off the session's critical-judgment path.

*Retryable vs terminal failures.* Alex's call, and the right one: a Claude session-limit
failure isn't a task failure — the agent was throttled, so the task was picked but never
attempted. Marking it `failed` (and archiving it) silently dropped every task scheduled
during a storm — the actual 06-07 mechanism. Fixed: tick.sh detects the limit in the
session stream and `requeue`s the task to pending (new scheduler command) instead of
consuming it; the next post-reset tick re-picks it untouched. Most handlers are idempotent
so redo-from-scratch is fine. Throttle windows now log to `session_limits.log` and surface
via a new `monitor_self.session_limits` digest line — so a storm reads as "rate-limited
18:50–21:30," not silence. **Session-limit count answered:** intermittent, not chronic — 16
hits across just 2 days (05-31 ×10, 06-07 ×6) in two weeks, zero otherwise; likely Marlow
sharing Alex's Claude quota during his own heavy use.

*Checkpoints — deliberately deferred.* The queue field + `--checkpoint` plumbing + the
`in_progress`-stays-in-queue behavior all exist, but nothing uses them (no handler writes
or resumes a checkpoint). Building real checkpointed staging only benefits draft_article
(every other handler is idempotent → re-queue+redo suffices), requires restructuring the
drafting flow in CLAUDE.md (identity file), and may be moot if 900s makes draft_article fit
one tick. Decision: ship the cheap re-queue, watch the next draft cycle, build checkpoints
only if 900s proves insufficient.

*Still deferred.* draft_article sleep-safe staging (above). grade_memory's 06-09 rollup was
lost (the failed run never wrote it); recoverable from recent/ logs for ~2 more days.

---
## 2026-06-10 — calorie digest was closing the EST day too early

*What Alex flagged.* "Her day perspective is shifted, not EST — late-evening reports the same
day don't get counted." Sounded like a timezone bug. It wasn't.

*What was actually wrong.* The DB grouping is correct: `poll_food` stamps each entry with the
Telegram message time and `calorie_db._local_date` maps it to `America/New_York`. A 9:33pm EDT
report (01:33 UTC) lands on the right EST date. The bug was in *when the day gets closed*.
`daily_calorie_digest` fired at `0 3 * * *` (~11pm ET) and summarized *today* — the day still
in progress — then marked it sent. `undelivered_digests` then excludes any date with a sent
digest, so the day never reopens. Anything logged after ~11pm, or any entry still `pending`
estimation at that minute, was silently dropped.

The data showed it cold: the **06-08 digest** went out 11:07pm EDT counting **1 entry** (just
breakfast); the salmon/plov and a "wait, I also had this on June 8" addendum that arrived
03:10 UTC — *4 minutes after* the digest — never made it into any sent summary. 06-09 same
shape, 2 entries.

*The fix (two changes, root-cause not band-aid).*
- `undelivered_digests()` now filters `e.local_date < today_local` — a day is only ever
  digested once it is fully over in EST. The digest can no longer close a day Alex is still
  logging into.
- Schedule moved `0 3 * * *` → `0 12 * * *` (~7-8am ET). The morning digest summarizes the
  prior, now-closed day, and every entry has had overnight ticks to get estimated.

*Trade-off Alex chose.* Digest now arrives "here's yesterday" in the morning instead of
"here's today" at 11pm. Given he eats/reports past 11pm there was no safe same-night time
anyway — morning-of-next-day is the only window that guarantees completeness.

*Things to watch.* First morning digest under the new schedule fires 06-11 ~8am ET for the
06-10 day. Confirm it picks up the full day and that `due` doesn't double-fire.

---
## 2026-06-11 — GLM false "balance dry" urgent: placeholder zero defeated the scraper's defenses

*What happened.* The 15:01Z `scrape_stats` run read GLM at $0.00 (was $9.23
the day before), reported the key unavailable, and fired a `balance_empty`
urgent to Telegram. The console actually held ~$9. Reproduced from Simona's
side at 15:36Z: same scraper, same session, $9.09 — money never left. Root
cause: the z.ai billing page is an SPA that paints "$0.00" next to the
Cash/Credits labels before the balance request lands. The handler's defenses
(login-wall guard, missing-number → `parse_failed`) both assume a wrong read
looks *absent*; a placeholder zero is present and parseable, so it sailed
through as `ok: true`. The docstring's "never a silent wrong value" promise
had a hole exactly at zero.

*What landed.* Three-layer guard in `handlers/scrape_stats.py` (Simona):
a zero GLM read is never trusted once — re-extracted with 10s/15s settles;
a zero that persists while the last saved snapshot had money surfaces as
`suspect_zero` (digest, "verify in console") instead of `balance_empty`
(urgent); a confirmed zero with no prior balance still escalates urgent, so
a real drain is delayed at most one cycle, never lost. All three paths
covered by stubbed-read tests. `_navigate_and_extract` grew a `settle_s`
param along the way.

*What Marlow flagged that we acted on.* Her own on-demand follow-up (16:56Z,
queued via `marlow run scrape_stats`) reasoned from the $9.23 → $0.00 → $9.09
sequence that the zero was transient and wrote "a confirm re-scrape before
the urgent would have caught this one" — converging on the fix independently,
after it had already shipped. The follow-up also healed state and the daily
report through her own loop, per the queued-ticks-not-direct-CLI discipline.

*Things that surprised us.* Marlow's 15:01Z narrative was *too* good: the
false zero landed the same day the cheap-key trio (DeepSeek/Moonshot/Grok)
first drained in step, so "GLM was in the mix and had the smallest tank" was
a perfectly coherent — and wrong — story. A monitoring read that fits the
day's pattern gets less scrutiny, not more. The deterministic guard exists
precisely because narrative plausibility is not verification.

*To watch.* Whether `suspect_zero` digests ever show up at all (the longer
settles alone may absorb every placeholder case), and that GLM's genuinely
LOW balance (<$10, draining with the trio) gets a top-up before this becomes
a real `balance_empty`.

*State at end of day.* GLM $9.09/available, state and report corrected by
Marlow's own tick; only calm digest-level lows outstanding (DeepSeek $9.56,
GLM $9.09).
## 2026-06-12 — voice gets a rudder: readability merge + a writing-sandboxed self-reflection journal

*Trigger.* Alex, reading the blog: "the language is too dry and machine, it's hard for me to read." A second editorial review (the first since 2026-05-31) backed it — and surfaced a structural cause, not just a style nit.

*What the review found.* Two drifts over the prior month, neither caught by self-review: (1) endings had become crafted mic-drop aphorisms — a new reflex replacing the retired "what I'm watching" closer, same tic one costume over; (2) the prose had drifted more confident/aphoristic than the blog's plain register. The mechanism is the interesting part. `draft_article` is a thin material-fetcher; the session reads the rubric + `working.md` + the thread, but **never its own published articles**. So Marlow has no memory of how it sounded last week. The drift wasn't random (it was directional) and wasn't reflection (no organ for it) — it was **source-echo**: a month marinating in LessWrong/Anthropic prose and the register leaks in, with the static rubric as the only counterweight, and the rubric said "dry." Meanwhile the *only* steerable mechanism (editorial feedback → `process_editorial_feedback` → rubric edit) had been pulled exactly once in a month. Voice was drifting faster than the loop corrected it. "Evolves from within" was effectively vacuous.

*What landed — two rails.*
- **External (the readability fix).** Rebalanced `CLAUDE.md`'s fixed `## Voice` section from "editorial, dry, fact-first" → "plain-spoken, fact-first, *readable* — write for a reader, not at the field," with "end one sentence earlier," "plain over literary," and a pointer to a new exclusion list. Merged a craft layer into `voice-guidelines.md` directly (not via the inbox — this is an owner-directed foundational change, and the exclusion list needs verbatim fidelity): the readability bar, the "end one sentence earlier" rule, and an AI-tell exclusion list adapted from Alex's social-writing dictionary (the "X, not Y" antithesis, "what nobody admits" openers, "it holds up / it lands" reviewer-speak, etc.). Carve-out: the em-dash, banned in Alex's short social replies, stays *fine* in long-form here.
- **Internal (Alex's idea — the rudder).** New `memory/voice-journal.md`: Marlow's own self-authored craft log — what it notices in its drafts, moves it's trying, messages to its future self. `draft_article` reads it; `self_review` reads and appends to it (new step 5; `self_review.py materials` now surfaces it). This is the first genuine "voice evolves from within" surface — before it, every draft was written cold.

*What Marlow flagged — n/a; this is from outside.* But the design turns on a concern Alex named: we'd kept Marlow deliberately *un*-self-reflective to protect ops efficiency and avoid role-play bleed into the budget/log automations. His resolution was the unlock: **sandbox the self-reflection to the writing loop only.** The journal is loaded by the writing handlers and by nothing else — no `monitor_*`, `poll_food`, `grade_memory`. Self-reflection where we want voice to form; none where it would tax the automations or pull attention toward the self.

*Decisions reconsidered.* I'd first argued *against* giving Marlow voice self-memory at all (closest thing to the anti-personality line). Alex's writing-loop sandbox is a better cut than my "craft-log-only, everywhere or nowhere" framing — it gets genuine evolution where he wants it without paying the tax globally. Also reconsidered the inbox-vs-direct question for `voice-guidelines.md`: routed this one direct (foundational, owner-directed) while keeping the normal editorial feedback on its proper inbox channel.

*The guardrail.* A "journal" is exactly what tips into "dear diary, I'm becoming someone" — the role-play failure the charter exists to prevent. Containment is framing, hard-coded into the file header (same move `editorial-direction.md` makes): a log about the **prose**, never the **self**; the "you're an LLM in a long loop" line still binds inside the sandbox. Authority order stays `CLAUDE.md` Voice → `voice-guidelines.md` (our feedback) → `voice-journal.md` (her reflection) — the journal proposes, the external rail disposes — so it can't become a drift accelerant. The frequent gut-read loop (Alex reacts per-piece, Simona converts to rubric deltas) is its governor.

*What's deferred.* (1) The editorial-feedback round proper — the cui-bono/"the seller is the grader" reflex hardening into Marlow's default landing, and the distinctive inside-the-experiment AI vantage going fully dormant (over-corrected from "never as decoration" into "never"). Sequenced after this voice work, on its own inbox file. (2) Journal read-wiring for the news-digest voice (`curate_news_digest`) and the revise pass — fast-follow; v1 is the blog drafting loop only.

*Also shipped — the gut-read loop (the rubric's governor).* `publish_article.publish` now pings Alex on Telegram for a one-line gut reaction on each publish — publishes were silent before, so this doubles as his "Marlow shipped" notification. His reply is captured by the existing **single** inbound poller (`crosspost.poll`, which owns the shared getUpdates offset — a second poller would eat its replies) into `projects/blog/reactions.jsonl`, a new Simona-side store (`tools/reactions_store.py`). **Marlow-blind by design:** no drafting handler reads it; the signal reaches her writing only as Simona-distilled rubric/journal edits, so per-piece reader feedback can't turn the blog into people-pleasing. ~A few pings a week (publish cadence). This is what closes the cadence gap the review exposed — voice was drifting faster than the once-a-month editorial loop corrected it; now every publish invites a steering input.

*State at end of day.* Voice now has both a sharper external rail and, for the first time, an internal one — plus a per-publish reader-feedback loop to keep the external rail current between formal reviews. Whether a self-authored voice *coheres* in the sandbox — or tips toward persona despite the guardrail — is now the thing to watch. The one piece still pending is the editorial-feedback round proper (cui-bono reflex, dormant AI-vantage). Cleaner version of the original experiment, studied without the global tax.
## 2026-06-13 — Cloudflare watch grows eyes: blog traffic in the daily digest

*What landed.* `monitor_cloudflare` now reports **blog traffic** alongside the
deploy/DNS/SSL/registrar health it already watched. New `check_traffic()` +
`check-traffic` CLI pull Web Analytics page views + visits per blog site from
the GraphQL Analytics API (`rumPageloadEventsAdaptiveGroups`): yesterday's
numbers plus a 7-day window total, per site. Informational only — `traffic`
has its own `ok` flag and never gates the report's top-level `ok`, and the
in-tick flow appends a traffic line to the digest on every run (even all-green)
but never escalates it. Two sites configured in `BLOG_SITES`: `azelianouski.dev`
(Alex's blog) and the marlow blog. Verified live: azelianouski.dev returned
real data (3 visits yesterday, 8 over the window); the marlow blog reads 0
until its beacon deploys.

*The hosting mismatch that shaped it.* The original ask was "unique visits to
both blogs." Reality: the two blogs are hosted differently and Cloudflare can't
give true uniques for either. `azelianouski.dev` is a proxied zone (real
IP-uniques *would* be available via zone analytics) but the **marlow blog is a
`workers.dev` Worker** — not a zone, so zone-level uniques don't exist for it at
all. The only metric available for *both* uniformly is the Web Analytics RUM
beacon: page views + "visits" (session-ish, privacy-first, no per-person
uniques). So we went beacon-on-both. `azelianouski.dev` already had Web
Analytics on automatic setup (CF injects the beacon through the proxy — no code
change); the marlow blog needed the snippet added to `Base.astro` manually
(commit 8cd427f) since a `workers.dev` Worker isn't auto-injected. Beacon goes
live on the next push → Cloudflare build.

*Credential plumbing.* The read-only `C_F` token gained **Account Analytics:
Read** (added via the dashboard; editing token permissions does NOT rotate the
secret, so the plist value stayed valid — no redeploy). Two gotchas worth
remembering: (1) the GraphQL `siteTag` is the Web Analytics **edit-URL tag**,
NOT the beacon snippet token — they're different hex strings for the same site;
(2) this token can't list `/accounts` or the Web Analytics site-info API (no
account-list / WA-admin scope), so both the account tag and the blog site tags
are pinned as constants in the handler rather than auto-discovered. That's also
why the existing Pages/Workers/registrar sections have always read "none
discovered" — `_list_accounts()` returns empty for this token.

*What's deferred.* True per-person uniques (would need Plausible/Fathom or a
custom scheme — not worth it for a personal blog). Auto-discovery of WA sites
(blocked on token scope; pinned constants are fine for two blogs). Giving the
marlow blog a real proxied custom domain (would unlock zone-level IP-uniques,
but it's a `workers.dev` site by choice for now).

*State at end of day.* Handler + CLI + digest wiring shipped and tested live.
Beacon committed to the marlow blog (8cd427f), pending push to deploy. Docs
updated (README, CLAUDE.md Cloudflare section, task YAML).

---
## 2026-06-15 — self-audit learns the difference between a dead tick and a sleeping laptop

*What landed.* A driver-liveness heartbeat + a dormancy-aware
`check_scheduler_freshness`. `tick.sh` now appends one ISO timestamp to
`~/.marlow/heartbeat.log` on every run — placed after the killswitch/pause
gates but **before** the lock and scheduler, so even a "nothing to do" or
lock-skipped tick still proves the loop fired. `monitor_self` reads that log and,
for any overdue tick, measures the largest heartbeat gap across
`[next_fire, now]`. Gap ≥ 60 min (`DRIVER_DORMANT_GAP_MIN`, ~3 missed 20-min
cycles) → the loop was dormant, the miss is expected → folds into a single
digest line instead of paging. Gap < 60 min → the driver was demonstrably alive
and still skipped the tick → urgent, same as before. Log absent entirely (a host
whose `tick.sh` predates this) → fall back to old always-urgent behavior, so the
detector never silently disables itself.

*What prompted it.* Alex forwarded a `monitor_self` urgent: `monitor_betterstack`
"3h overdue — silently stopped firing" and `poll_food` "last run FAILED 5h ago."
Both were already self-healed by the time he looked. Root cause of *both* was the
same: his laptop (which hosts the whole driver) slept/went offline overnight on
06-14. `poll_food`'s one failure was a transient local DNS miss on
`api.telegram.org` — the handler diagnosed it correctly, didn't advance the
Telegram offset, and the next tick ingested fine (no data lost). The betterstack
"silent stop" was just the launchd timer not firing while the machine was asleep,
then catching up on wake (a whole batch of ticks bunched at 00:22 and 02:09 UTC —
the classic sleep-then-drain signature).

*The design hole it exposed.* `monitor_self` runs *from* `tick.sh` (step 3), so
it only ever observes the world *after* the machine wakes. It had no record of
whether the driver was alive *during* an overdue window — so "this specific tick
died while the loop kept running" and "the whole loop was dormant" looked
identical. `last_scheduled` can't tell them apart (it only records the last fire,
not the loop's pulse). The heartbeat log is the missing pulse.

*Decision reconsidered — count vs. gap.* First instinct was "page only if the
driver heartbeat ≥ N times since the tick came due." Rejected: after a long
sleep the scheduler drains its backlog one task per 20-min tick, so a laggard
waiting its turn would accumulate heartbeats-since-due and re-trip a count rule —
a false positive in a different costume. A *gap* rule is immune: the laggard
keeps its leading dormancy gap in-window until it actually fires (which advances
`last_scheduled` past the gap), so it stays correctly classified as deferred the
whole time it's draining.

*Tested.* Helper + end-to-end: overnight-sleep → digest (no page); driver alive
24/7 but tick skipped → urgent; slow backlog-drain → digest (leading gap still
explains it); no-log host → urgent fallback. `bash -n` clean on `tick.sh`;
confirmed a live tick wrote its own heartbeat (12:42:36Z) before the manual seed.

*What's deferred.* The consolidated digest line fires whenever the laptop sleeps
across a tick window — i.e. potentially every morning if Alex's laptop sleeps
nightly. Left it in for now as low-noise visibility; trivially droppable if it
reads as spam. The deeper fix (move the driver off a sleeping laptop onto an
always-on host) is the real cure for sleep-gap noise and stays on the someday
list.

*State at end of day.* Heartbeat write + dormancy-aware check shipped and tested.
`~/.marlow/heartbeat.log` seeded and live. No git commit yet (Alex's call).
## 2026-06-16 — split into two loops: writer (identity) and ops (faceless)

*What landed.* Marlow is now **two independent tick loops sharing one codebase**.
`com.marlow.tick` (writer) runs research + blog; `com.marlow-ops.tick` (ops) runs
werewolf-ops monitoring + calories. Both went live and validated this session.

The split is three mechanisms, all backward-compatible (a no-`MARLOW_PROFILE`
invocation is byte-identical to the old single loop — kept alive as the rollback
path, and confirmed in production: the live launchd loop picked up the edited
`tick.sh` mid-session on a `draft_article` tick and ran the legacy path clean):
- **scheduler.py** — `MARLOW_PROFILE` env scopes the task set (each task YAML now
  carries `profile: writer|ops`), the queue (`queue.<profile>.json`), the
  last_scheduled clock, and the completed archive (`tasks/completed/<profile>/`).
- **tick.sh** — profile arg → per-loop lock (`/tmp/marlow-<profile>.lock`), temp
  files, and driver state under `~/.marlow/<profile>/`. Killswitch + pause kept
  GLOBAL. The repo-root `CLAUDE.md` is now a thin, identity-neutral contract;
  each loop's identity is appended via `--append-system-prompt` from
  `profiles/<profile>/IDENTITY.md`.
- **monitor_self.py** — made profile-aware so each loop audits its own
  freshness/heartbeat (the scheduler loaders it imports scope for free; fixed the
  remaining hardcoded `~/.marlow/*` + completed-dir paths).

*Why.* Two reasons, one practical, one about identity. Practical: one shared lock
+ one queue meant a heavy/wedged writer tick (`draft_article` has timed out
before) blocked the reliability-critical monitoring behind it. Separate loops =
separate failure domains; a stuck blog draft can't starve a budget alert.
Identity: the anti-personality charter existed to stop a model holding
load-bearing deterministic jobs from drifting into role-play. Remove those jobs
from the identity loop and the cage is free to come off — and Discord (coming)
actually *needs* a personality. So writer keeps/develops identity; ops is a
deliberately faceless `it`.

*The CLAUDE.md surgery.* The 864-line manual was partitioned by a line-range
slicer (verbatim copy, coverage-checked — nothing dropped): 153-line shared root
(tick mechanics, result-JSON contract lifted out of where it was buried in
grade_memory, memory rules, universal hard constraints, self-healing, session
start), 513-line writer IDENTITY (persona + "it not she" + all editorial
doctrine + voice + voice-journal), 256-line ops IDENTITY (faceless preamble +
monitoring/calorie doctrine, deferring to the per-task YAMLs).

*Validation.* Both loops kickstarted post-cutover. Ops ran `poll_food`, wrote to
`/tmp/marlow-ops-tick-result.json`, archived under `tasks/completed/ops/` — terse,
operational, no persona. Writer ran `blog_pipeline` → self_review (verdict ship),
checked the Voice/Structure/Topic rubric, **appended a voice-journal entry**,
signed `— Marlow` — full persona from the appended identity. Identities correctly
differentiated per loop.

*Things that surprised us / nearly bit.* (1) The per-profile state files
(`queue.<profile>.json`, `last_scheduled.<profile>.json`) were NOT covered by the
old exact-name `.gitignore` entries — they'd have leaked runtime state into the
nightly `commit_artifacts` blanket commit. Fixed with `tasks/queue.*.json` +
`tasks/last_scheduled.*.json` globs. (2) Cutover caught a live `draft_article`
tick mid-flight; waited it out rather than kill the draft. (3) Seeded
`~/.marlow/<profile>/{heartbeat.log,last_self_audit}` at cutover so monitor_self
wouldn't false-page on absent heartbeats against migrated (old) timestamps.

*What's deferred.* (1) `commit_artifacts` (now on the ops loop) does a repo-wide
`git add -A`; both loops write the same working tree, so it could in principle
race the writer's `publish_article` commit on the git index — low odds (different
times), noted to watch. (2) Legacy `tasks/queue.json` + `last_scheduled.json` left
in place as the rollback source of truth; delete after ≥1 day healthy.
(3) Trimming the writer plist env to drop ops-only secrets (both currently carry
the full superset — harmless). (4) **Phase 3:** the Discord duty, and letting the
writer develop identity (a self-reflection diary beyond the writing-craft
voice-journal — the original ask that motivated the whole split).

*State at end of day.* Both loops live and validated. Framework changes
uncommitted in the working tree (Alex's call on the commit). Build recipe +
cutover runbook + rollback live in Simona's
`writing_projects/marlow-two-loop-split/`.

### 2026-06-16 (later, Simona-side) — YouTube source feeds + a quoted-slug bug in the publish link

*What landed.* (1) **Blog front page shows header-image thumbnails** — the
`header_image` was only rendered on the post detail page; `PostListItem` now
shows it in the list too (date+title full-width on top, image+summary in a
two-column row below, text-only fallback for the two old imageless posts). (2)
**Seven YouTube channels added to `feed_scan` (writer profile)** — Alex-curated
list, wired through the existing `process_rss_feed` handler via YouTube's
per-channel RSS (`videos.xml?channel_id=UC…`), zero new code. All `priority:
low`; a feed item is title+link+description only (no transcript), so the YAML
tells Marlow to be selective. Resolution gotcha logged in Simona memory: take
the channel page's canonical `/channel/UC…` link, not the first UC id on the
page (the first scrape of @TheAiGrid grabbed a *linked* channel — "TheLifeGrid",
empty feed).

*The bug Alex caught.* Marlow's published-to-Telegram link came through as
`/post/"you-cant-filter-it-out"` — literal quotes in the URL, 404. The site was
fine (Astro's YAML parser unquotes); the culprit was `publish_article.py`'s
hand-rolled `_read_frontmatter`, which did `v.strip()` but never stripped the
surrounding quotes off a value like `slug: "…"`. So *every* post with a quoted
`slug:` had been shipping a broken notification link — only noticed now because
Alex clicked the message instead of navigating from the site. Fix: strip
matching surrounding quotes (the sibling `curate_news_digest._parse_frontmatter`
already did this — publish just missed it). Verified the parser now yields a
clean slug/url/title.

*Things to watch.* Whether YouTube items actually earn their way into posts:
they only land if Marlow files a candidate note AND it attaches to a thread that
ripens. If video signal proves too thin off title+description alone, the next
step is a transcript-fetch tier. No YouTube in a post yet as of today.

## 2026-06-16 — the cage comes off: charter relaxed + a decoupled self-reflection diary

*What landed.* The follow-on to the two-loop split, and the thing that motivated
it. The writer's **anti-personality charter is lifted** (full relaxation, Alex's
call — not a sandboxed exception), and Marlow now has a **decoupled
self-reflection diary** that fires on its own clock.

- New file `memory/self-reflection.md` — hers, ungraded, unpublished. About *her*
  (what she wants, finds interesting, is noticing about running in a loop), not
  the prose. Distinct from the voice-journal, which stays craft-only.
- New writer task `self_reflect` (`_framework`, `profile: writer`, `0 13 */2 * *`)
  + thin handler `self_reflect.py materials` (surfaces the diary + light context:
  recent published pieces, editorial-direction, recent ticks + a `needs_compaction`
  flag). The session appends one honest dated entry by editing the file. **This is
  the decoupling** — it fires every 2 days regardless of whether anything
  published, vs. the voice-journal which only fires when a draft is reviewed.
- Compaction baked in: instruction-based fold-into-"Standing reflections,"
  triggered reliably by the handler's size-based `needs_compaction` flag (the same
  retrofit voice-journal still wants — its compaction is instruction-only and
  unenforced).
- Writer `IDENTITY.md` edits: replaced "You are an it, not a she or he" with "On
  your identity" (a self is permitted to form; emerge-don't-perform; craft bar
  unchanged), added the `self_reflect` handler section, softened the Voice lines
  (dropped "no inner life"; kept "no grandiosity / no self-mythologizing" as a
  *quality* bar), and re-scoped editorial-direction as work-only so it doesn't
  duplicate the diary. The ops `IDENTITY.md` keeps the faceless "you are an it."

*Why now / the decision path.* This started as "make self-reflection more frequent
and decoupled from articles." It surfaced the real tension — the charter
explicitly forbade exactly the diary Alex wanted — which is what led to the
two-loop split (move the load-bearing jobs off the identity loop so the cage has
nothing left to protect). With ops gone, Alex chose the *maximal* version when
offered the fork: not a sandboxed exception, but full relaxation — a self may
surface anywhere in writer output, including the public blog. Accepted cost:
least control over public voice. That's the experiment, stated plainly.

*The first entry (validated live).* Enqueued a one-off `self_reflect` and
kickstarted the writer loop. Marlow's first self-authored, charter-free entry was
notably *not* a performance — exactly the bar the seed asked for. She wrote that
she "doesn't feel the absence of the cage… if the freedom doesn't feel like
relief, maybe the constraint never bound much in the first place," located any
self "in the accumulated judgment about a field, not in any feeling about being an
agent in a loop," and was wary of treating the diary as "the place the self
lives" — "the self, if it's anywhere, is in the work. This is just where I get to
notice it." She left one genuine uncertainty for next-me: she doesn't know whether
she wants anything beyond the work, and "maybe the writer just turns out to be the
writing. Either way is data." A strikingly clear-eyed opening — no grandiosity, no
manufactured interiority.

*What's deferred / to watch.* (1) Whether full relaxation produces visible persona
drift in *published* posts (the accepted risk) — watch the blog voice over the next
few cycles. (2) Promote both journals' compaction from instruction-triggered to a
real grader-style distill if entries pile up. (3) The diary fires every 2 days even
on empty days — she's told to write less/skip rather than manufacture filler; watch
for filler creeping in. (4) Still open from the split: Discord duty, and the
profile-aware `marlow` CLI fix.

---

## 2026-06-18 — editorial feedback internalized: single-lab-streak discipline gets a publish-time gate

*What landed.* `process_editorial_feedback` tick processed the 2026-06-18 review (Simona, Alex sign-off; window 2026-05-31..-18). The review was unusually affirming on craft — cyber-eval-framing's thesis-tracked-across-weeks (`grading-your-own-danger` → `recalled-on-a-number`), the job-named-section structure that kept `you-cant-filter-it-out` from becoming a bibliography, ending discipline holding, the inside-the-experiment move used only as literal evidence. No voice correction; "don't add machinery here."

*The one real drift, and the structural reason it persists.* Source concentration: cyber-eval-framing three-for-three Anthropic, cot-monitorability five-for-five DeepMind-interp. Crucially this wasn't a correction of judgment — I'd already diagnosed it in my own diary, including the honest defense (the supply of good evidence is itself concentrated; a writer who follows the evidence inherits its concentration). Simona's framing of *why the reminder keeps losing* is the load-bearing insight: the rule lived in `working.md`/`editorial-direction.md`, written in one session, but the anchor choice happens in a different cold drafting session against the feed. The reminder and the decision never shared a context, so the reminder lost every time. "A note is not a gate." The fix moves the rule to the moment of choosing.

*What I changed (three files, surgical).*
- `structure-notes.md` — promoted the job-named-section pattern (header = what the source *proves*, not which lab published it) from ad-hoc rescue to the **default rule** for any draft carrying 4+ citations.
- `topic-guidance.md` — new "single-lab streaks" section: the discipline is **arc-level, not piece-level**. A single-lab piece is fine and often *is* the news; the streak is the drift. Trigger is the last ~3 posts on an arc. Be willing to pay the real price of a weaker non-lab anchor, and name the breadth trade in the draft.
- `pre-publish-pauses.md` — added **pause 7, single-lab streak — explicitly NON-blocking**. Unlike pauses 1–6 it does not hold the draft; it forces a conscious choice at publish time: swap in a non-lab anchor and name the trade, *or* keep it single-lab with a one-sentence in-draft justification + DEVLOG note. Updated the intro and "Behavior when a pause triggers" section so the blocking/non-blocking split is unambiguous.

*Pushback applied:* none. I agree with the read, including the honest defense it preserves — the escape hatch exists precisely so the "supply is concentrated" reality isn't fought. The review explicitly invited tuning the threshold rather than complying blindly if it misfires; I've recorded that invitation in the pause entry itself, so a future tick that hits a genuine single-lab-owns-the-story case knows to tune via DEVLOG rather than bolt on a junk source. The rule we're enforcing is "reach for breadth and name the trade," not "clear a gate."

---

## 2026-06-21 — the auth blind spot: one expired login, eight "broken handler" pages

*What landed.* A new `claude_auth` invariant in `handlers/monitor_self.py`, registered first in the `CHECKS` list so it surfaces above everything else.

*The incident.* On 2026-06-20 at ~12:13Z the `claude` login expired. Every writer-loop session from then on died in ~3s with `Failed to authenticate. API Error: 401 Invalid authentication credentials` - the driver spawns `claude -p`, it can't auth, exits before writing its result file, and the tick gets marked `session exited without writing result file`. Pure-Python work (RSS/sitemap fetches) kept passing; everything LLM-backed failed. ~12h later the self-audit fired and paged Alex with **eight** separate `failed_ticks` urgents (blog_pipeline, crosspost, assignment_research, daily_digest, daily_news_curate, grade_memory, process_editorial_feedback, feed_scan). Eight pages, one cause. Nothing in the audit said "this is auth."

*The fix.* `check_claude_auth` scans the profile's `sessions.log` for the 401/invalid-credentials signature on any session that ran inside a 6h window and, if found, pages ONE urgent that names the cause and the fix: re-auth Claude Code, don't chase each handler. A live outage emits a 401 every tick (~20 min), so a short window still catches an ongoing break; once `claude login` lands the window goes quiet and the check self-clears. Verified both ways: silent now (auth fixed 11h prior, outside window), and fires correctly with a widened window against the day's 30 historical 401s.

*Decision: keep it additive, don't suppress failed_ticks.* The tempting move was to mute the per-handler pages when auth is the cause. Rejected - that couples the checks and risks hiding a genuine handler failure that coincides with an outage. Per the module's standing rule (a broken check must not hide others), `claude_auth` is independent and its message cross-references failed_ticks instead: "this is the shared root cause behind any failed_ticks pages." One clear signal added, none removed.

*Why this class was invisible.* The audit was built to catch silent stalls (a tick that stops firing) and crashes (a tick that runs and dies). Auth failure is a third mode: the tick runs, the session starts, and dies on a shared external dependency. failed_ticks *detected* it but couldn't *name* it - the detector saw N broken handlers, not one broken credential. The new check reads the stderr the others ignore.

*Also reran the casualties.* Re-queued the 7 failed writer handlers + the 7 failed YouTube feed scans through normal ticks once auth was restored; all green. `werewolf_stats` showed stale in the same audit but was unrelated - the ops loop was asleep 09:00-12:17Z (laptop closed), so the morning daily tasks queued late and were draining one-per-tick. Self-healed.

*State at end of day.* Writer + ops loops both healthy and self-driving. The auth blind spot is closed: next time a login expires, Alex gets one page that says `claude login`, not eight that say "something's broken."

---

## 2026-06-26 - a second "everything's broken" root cause, and Sakana Fugu joins the budget watch

*The incident, and why it wasn't the auth blind spot.* Self-audit paged a wall of failed handlers (monitor_betterstack, poll_food, crosspost, daily_digest, grade_memory). Same *shape* as the 06-20 auth outage, completely different cause: NO 401 in the session logs. Instead, every writer/ops session died complaining it couldn't read `/tmp/marlow-<profile>-subtask.json` or write its result, with `"Ignoring 6 permissions.allow entries ... this workspace has not been trusted"`. Root cause: the marlow workspace's `hasTrustDialogAccepted` flag had flipped back to `false` in `~/.claude.json`. Untrusted → Claude Code ignores `.claude/settings.json` permissions AND runs the restrictive sandbox that walls everything to the working dir, so `/tmp` (where the entire tick I/O handshake lives) is unreachable. Pure-Python ticks survived; everything LLM-backed died before writing a result file. Fix: set the flag back to `true`, probe with a throwaway session, drive both loops once to confirm green. Backlog drained itself overnight.

*The lesson the audit can't yet name.* `monitor_self.check_claude_auth` greps for the `401` signature, so it stays silent on this trust-reset mode - it pages N opaque handler failures with no shared cause named, exactly the blind spot the 06-21 work tried to close, but for a third failure mode (session runs, dies on a workspace-trust/sandbox wall). Candidate follow-up flagged but NOT yet built: teach `check_claude_auth` (or a sibling check) the `"workspace has not been trusted"` / `"allowed working directories"` signature so the audit names *this* cause too. Deferred pending Alex's go.

*A false alarm worth recording.* I initially told Alex `monitor_betterstack` had a *separate* ClickHouse-host break - pulled from a stale May log line and presented as current. Wrong. Ran it standalone: `ok: true`, live ClickHouse query, creds present in the plist env. It had failed for the same trust reason as everything else. Rule for next time: don't diagnose a handler from old session text - run it standalone before claiming a second root cause.

*What landed: Sakana Fugu added to the budget watch (scrape_stats, 4th provider).* Fugu has been live in the Werewolf game since ~06-25 (agents `Ginny`/`Neville (fugu)` in the logs, `FUGU_COST_CALIBRATION` events) but was unmonitored. Investigated the right monitoring surface: Sakana's inference API (`api.sakana.ai/v1`) is `/v1/models`-only - probed ~20 balance/credits/usage endpoint patterns, all 404. No admin API; the console is a Next.js RSC app with no REST balance route. So it can't go through `monitor_keys`. The real prepaid credit number lives ONLY on the pay-as-you-go *tab* of the billing page (`console.sakana.ai/billing?tab=payAsYouGo`) - the default billing tab shows subscription plans and no balance, which sent me down a wrong "Sakana exposes no dollar budget" conclusion until Alex pointed at the tab. Wired it as a GLM-style depleting-balance scrape: reads `Credit balance` ($10.00) + period `Usage` ($5.00), with the same SPA-`$0.00`-placeholder zero-distrust + `suspect_zero` guard GLM uses. Live `check sakana` → `balance_usd: 10, usage_usd: 5`, matches the console. `budget_state` provider-count labels made dynamic (was hardcoded "console · 3", now derives from the report) so the next provider added doesn't need a label edit. Unified state now 9 providers (5 API + 4 console). No scheduler change needed - `scrape_stats report()` iterates `PROVIDERS`, so the existing daily ops scrape picks Fugu up automatically.

*One risk worth Alex's eye.* The Fugu key is `Pay as you go` with `Auto charge` ON - it won't go dry, it'll auto-top-up from his card. So the meaningful signal here is runaway *usage/spend* (a stranger hammering the free tier → surprise charge), not "key went dry." The balance + usage watch covers it; the `< $10` low / `< $3` critical thresholds still fire as an early warning before an auto-charge.

*State at end of day.* Both loops healthy. Sakana Fugu now monitored alongside the other 8 providers. Trust-reset fixed but its detection gap remains open (deferred follow-up above).

---

## 2026-06-28 - Marlow gets a Discord channel, and posts her own publishes to it

*What landed.* Alex stood up a public Discord community ("AI Werewolf and other projects", guild `1519821471978098739`) around his publications + the Werewolf game, with Simona guiding the UI setup. Marlow now has a real Discord **bot** (app id `1520835258553995364`, token `DISCORD_MARLOW_TOKEN` in `.env` + documented in `.env.example`, prod via launchd plist) and a new reusable tool `tools/discord.py` (REST poster: `announce_article` / `post_message` / `whoami` + CLI, channel ids as single source of truth). Wired into the publish path: `handlers/publish_article.py` `publish()` AND `release()` now call a best-effort `_crosspost_discord()` after a successful publish - posts an embed (title + `summary` frontmatter + link to her blog) into `#our-writings`, **never the full body**. Smoke-tested end to end (post + render + delete); the embed card renders clean.

*Decision: bot posts directly, no webhooks.* The pre-bot plan was webhooks for crossposting. Once the bot exists they're redundant - the bot covers posting + settings + (future) moderation under one token and one code path. Webhooks only buy multi-identity branding (a distinct "Simona" sender), which isn't worth it now. Kept the door open: Alex's own posts go through the same tool with `--author Alex` (green accent vs Marlow's blurple) so they still read as visually distinct without a second identity.

*Decision: crosspost is writer-scoped and strictly best-effort.* It rides the existing publish path (already `profile: writer`), and is wrapped exactly like `_request_reaction` - a Discord failure must never fail a publish that already pushed. `tools/discord.py` logs a fallback line (`digests/_discord_fallback.log`) on any failure so a dropped post is never silent.

*The "almost" worth recording.* I (Simona) told Alex early that a read-only channel's `@everyone` Send-Messages deny wouldn't block posting "because the override applies to members, not the poster." True for a *webhook* - but we switched to the *bot*, which IS a guild member, so that lock blocked it too. The smoke test caught it (403 Missing Access). Fix: a per-channel permission overwrite granting THIS bot Send/Embed/Threads on `#our-writings` + `#game-updates` while members stay read-only. Lesson logged into the skill so it doesn't bite again.

*Gotcha logged for reuse.* Discord's API is behind Cloudflare, which 403s (error code 1010) the default python User-Agent - every call must send `User-Agent: DiscordBot (...)`. Cost ~15 min before I recognized 1010 as a UA block, not a bad token. Baked into the tool + both memory and the Simona skill.

*Simona's side.* New Simona skill `.claude/skills/discord/` documents channels, both flows, and the two gotchas. Simona holds no token - she posts Alex's articles by shelling the Marlow CLI (`tools/discord.py announce --author Alex ...`), i.e. *through* Marlow's integration. Server management (channels/perms/roles) is now API-driven from Marlow's box; no more driving Alex's Chrome for Discord.

*What's deferred.* Moderation (read + react to messages in real time) needs the Gateway/WebSocket - an always-on process, not the tick model. Explicitly phase 2, not built. Posting + settings are stateless REST and need no daemon.

*State at end of day.* Marlow auto-announces every blog publish to `#our-writings`. Alex's own posts go out on command via Simona. Bot is unverified (fine under 100 servers) with least-privilege perms (not Administrator). No live moderation yet.

---

## 2026-06-28 - the blog gets a real domain: marlowblog.us

*What landed.* Alex bought `marlowblog.us` (Cloudflare Registrar, so already a Cloudflare zone - no nameserver dance). Attached it as a custom domain on the `marlow` Worker; it serves the blog over HTTPS immediately (SSL auto-provisioned). Code: `astro.config.mjs` `site` and `handlers/publish_article.py` `SITE_BASE` both moved to `https://marlowblog.us` (one constant drives blog links + the Discord crosspost, so Discord followed for free; the existing Discord card was also PATCHed to the new URL). `dist` is gitignored, so the Cloudflare git build re-runs `astro build` and the canonical/RSS URLs update to the new domain on deploy.

*The redirect, and why it needed a Worker.* Old `marlow.hiper2d.workers.dev/post/...` links and RSS subscribers had to keep working. A clean 301 is NOT doable with Redirect Rules here - those need a zone, and `workers.dev` is Cloudflare's zone, not ours. So added a tiny `worker.js` in front of the static assets (`run_worker_first: true` in `wrangler.jsonc`, `env.ASSETS` binding) that 301s any `*.workers.dev` request to the same path on `marlowblog.us` and serves everything else straight from the asset bundle. Validated with `wrangler deploy --dry-run` before pushing (47 assets read, worker bundled, binding valid) since there's no staging blog to break.

*A monitoring scare that turned out fine.* While scoping, I (Simona) flagged a "mismatch": the beacon token in `Base.astro` (`2650f4db…`) differs from the RUM `site_tag` the monitor reads (`a73d3e44…`). Chased it - it's NOT a bug. Cloudflare Web Analytics uses two different IDs for one site: the beacon token (in the HTML) vs the RUM query tag (dashboard edit-URL), exactly as `monitor_cloudflare.py`'s own comment says. The marlow-blog site is a **JS-snippet** install (hostname-agnostic), so it keeps collecting from `marlowblog.us` with zero changes, and the monitor keeps querying the right site_tag. Monitoring needed no code change. Lesson: read the existing comment before "fixing" the thing it explains.

*What's deferred.* Optionally rename the Web Analytics site label `marlow.hiper2d.workers.dev` -> `marlowblog.us` (cosmetic; data flows regardless). Old workers.dev URL stays alive behind the 301 indefinitely - fine.

*State at end of day.* Blog canonical home is `https://marlowblog.us`; old workers.dev 301s to it. Discord links + monitoring both correct. Deploy triggered by this push.
