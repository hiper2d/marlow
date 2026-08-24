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

## 2026-08-24 — self-heal: handlers/self_review.py

*What was wrong.* `handlers/self_review.py` `materials()` (line 133) referenced
`_memory_compact.analyze(...)` to build `voice_journal_split`, but the module was
never imported — so `self_review materials` raised `NameError` on every call and
the blog pipeline could not self-review the `2026-08-24-dont-ask-the-model-how-it-feels`
draft. `list-pending` worked (it never touches the module); only the materials
path crashed.

*What I changed.* Added the two-line import shim used by `self_reflect.py` and
`grade_memory.py` — `sys.path.insert(0, str(Path(__file__).resolve().parent))`
then `import _memory_compact  # noqa: E402` — right after the stdlib imports,
before `REPO_ROOT`. One file, scoped to the named failure mode. Smoke-tested
`materials --slug 2026-08-24-dont-ask-the-model-how-it-feels` (returns clean with
`voice_journal_split` present) and `list-pending` (no regression).

*Diagnosis* `diag_20260824_170251_self-review`. *Commit* `237a438`.

---

## 2026-06-28 - Discord community watch: the first ops monitor aimed at people, not infra

*What landed.* A new ops monitor, `monitor_discord`, every 6h (00/06/12/18 UTC). It polls the conversational channels (general, general-discussion, ai-news) for messages new since the last scan, computes activity stats, flags the deterministic bad-behavior shapes (volume firehose, repeated-message spam, link floods, mass mentions), and hands the new messages to the session as a `sample` so Marlow reads them and judges tone (rude/hostile/pestering) - the part rules can't do. New files: `handlers/monitor_discord.py`, `projects/werewolf-ops/tasks/monitor_discord.yaml`. Extended `tools/discord.py` with `get_channel_messages()` (paginated, after-cursor) and `get_guild_counts()`. Same cursor-diff + baseline-on-first-sight discipline as monitor_health / monitor_betterstack. Tested: baseline run, incremental after-cursor pickup against the live server (posted+deleted a probe message), and the heuristics via synthetic messages. Scheduler loads it under the ops profile; first fire 2026-06-29 00:00 UTC.

*The design call that matters.* This is the first monitor where the handler is deliberately NOT a pure deterministic relay. Every other ops monitor decides urgent/digest itself and the session just relays. Here the handler can only catch the mechanical shapes; "someone is being rude / pestering people" is a judgment call, and the session IS the model, so the judgment belongs there. The YAML's in-tick flow makes the judgment pass an explicit step, and the ops IDENTITY now calls monitor_discord out as the exception. Handler gathers, session judges - the split held, we just moved more of the work to the session side than usual.

*Decisions reconsidered.* The old memory note said community moderation was "phase 2, needs the always-on Gateway/WebSocket." That's true for *real-time* catch (delete a slur the instant it's posted). Alex explicitly didn't want that - periodic is enough - so the whole thing collapses to a poll-based tick that fits the existing scheduler with zero new infra. The "phase 2" framing was scoping the hard version of a problem we didn't have.

*The delivery tension.* Alex picked "every 6h" cadence AND "Telegram digest" delivery - mildly in conflict, since Marlow's "digest" means the once-daily bundle. Resolved by mapping to the existing urgent/digest contract: bad behavior pings immediately (the point of the feature), routine activity rolls into the daily digest, a quiet window stays silent. Avoids 4 "nothing happened" pings a day on a near-empty server while still surfacing problems within 6h. Flagged to Alex that he can flip routine reports to immediate-every-6h if he'd rather have all four.

*What's deferred / to watch.* (1) The server has 2 members and no chat yet - the monitor baselines and stays quiet until the community grows; thresholds (VOLUME_*, REPEAT_*, etc.) are first guesses to tune against real traffic. (2) Reading other users' message content over REST needs the privileged Message Content intent, which is OFF until Alex enables it (Developer Portal -> Bot -> Privileged Gateway Intents). Couldn't verify the other-user content path because there are no other-user messages; the handler emits a `content_intent_off` flag if it ever sees all-empty member messages, so it self-reports the gap rather than silently reporting blank. (3) No auto-moderation by design - detect and report only; the bot has the perms but we're keeping a human in the loop.

*State at end of day.* monitor_discord live, scheduled, untested against real human traffic (none exists yet). Marlow + Simona.

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

---

## 2026-07-26 - Mistral's console moved the number; the scraper spent three days saying "parse_failed"

*What landed.* Two budget-watch fixes, one real and one noise-reduction. **Mistral (real):** the month-usage figure has been `parse_failed` since the 07-24 scrape - three consecutive daily runs. Not a login wall, not Chrome: the billing console re-laid-out the Usage block. It used to render an inline `Usage: $0`; it now renders a section header, a blurb, then the bare number on its own line (`Usage` / `Current usage for the ongoing month.` / `$0` / `Monthly limit: $30`). The old inline regex went null, and since `usage is None` is the handler's parse_failed trigger, the whole provider went dark while `limit` and `pending` kept matching fine. Fixed by anchoring on the blurb sentence and taking the first `$` after it, with the inline regex kept as the first choice in case they revert. **OpenAI (noise):** the 21:05 tick reported `could not read balance: Read timed out`. Nothing was wrong - the 08:25 run read $12.16 and a manual re-run read $10.86. There was no retry anywhere in `monitor_keys`, so one TCP hiccup on an unattended twice-daily check turned straight into a digest alert. Added `_get()` (2 attempts, 3s backoff, retries transport errors only) and moved all six `requests.get` call sites onto it. An HTTP status is still a real answer and passes through untouched. Full `report` on both handlers after the fix: 9/9 providers green, no urgent.

*The pattern this is the third instance of.* Tier 3 was accepted as the fragile tier when it shipped (2026-05-31) and it keeps proving it: GLM's placeholder zero (06-11), and now Mistral's re-layout. Worth noting the two failed *differently*. GLM read a plausible wrong number and needed zero-distrust logic; Mistral read nothing and failed loud. Failing loud is the correct behavior and it worked exactly as designed - the check went `parse_failed` rather than reporting $0 usage and looking healthy. The gap is not detection, it's that nothing escalated a **repeat** of the same parse failure. Three identical digest entries on three consecutive days should read differently than one.

*What's deferred.* A "same provider, same failure kind, N runs running" escalation - digest on the first, urgent on the third. Right now a permanently broken scrape is indistinguishable in tone from a one-off, which is why this sat three days before Alex mentioned it. Small change to the issue-derivation step in both handlers plus a look back at `*_history.jsonl` (the trend tape is already there and already has exactly the data needed). Not built today; noting it rather than fixing it mid-bugfix.

*State at end of day.* All 9 providers reading (5 API + 4 console). Balances are low across the board but that is Alex's top-up call, not a bug: DeepSeek $7.94, Moonshot $6.36, xAI $7.39, OpenAI $10.86, Anthropic $30.60, GLM $4.94, Sakana $5.58, Gemini $0/$250 cap, Mistral $0/$30 cap (+$0.75 pending). Four sitting under the $10 digest threshold, none under the $3 urgent one.

---

## 2026-07-30 - two 529s that looked like broken handlers, and Mistral's console moved the number again

*What landed.* One real fix, one diagnosis, one deferral coming due for the second time.

**The two overnight alerts were not Marlow bugs.** Alex got two urgent self-audit pings on 07-29 (`monitor_keys` failed 4h ago, `daily_news_curate` failed 2h ago). Both tasks recorded the generic `session exited without writing result file`. The actual cause is in the session logs, identical in all three cases (`monitor_betterstack` 20:10Z, `monitor_keys` 20:33Z, `curate_news_digest` 22:09Z): `API Error: 529 Overloaded`. Anthropic capacity blip, roughly a two-hour window across both loops. Every one of them self-healed on the next scheduled tick - `monitor_betterstack` was clean at 21:14Z and `monitor_keys` ran clean twice on 07-30 (08:04Z, 20:15Z). Nothing was broken; nothing needed a re-run.

**The gap that turned a blip into a 3am ping.** `driver/tick.sh` has exactly one transient-failure escape hatch: the session-limit re-queue (grep for `hit your (session|usage) limit`), which puts the subtask back to pending without consuming it. A 529 has no such path - it falls through to `WARNING: session did not write a result file` and is marked **failed**, which `monitor_self` correctly reads as "currently broken, not just quiet" and escalates as urgent. So the driver told the truth about what it saw; it just can't tell "the model was unreachable" from "the handler is broken." **Fixed:** a second re-queue block in `tick.sh`, right after the session-limit one and reasoned identically - `API Error: 5\d\d|Overloaded|Internal server error` in the stream file re-queues the subtask without consuming it and exits 0. A genuine sustained outage now surfaces as overdue ticks (`scheduler_freshness`, digest), which is the accurate signal for upstream being down, instead of `failed_ticks` (urgent) pointing at three innocent handlers.

**Mistral, again - and it's a different break than 07-26.** `parse_failed` on 07-28, -29, -30. Not the same re-layout as four days ago: the billing page has been **gutted**. `/organization/billing` is now payment methods, a credits balance, and an invoice table - no month usage anywhere, and the `Monthly limit: $30` cap is gone from the console entirely (`/plateforme/limits` is rate limits now, TPM/RPS; `/organization/subscription` 404s). The month figure moved to `/organization/usage`, where it renders **without a dollar sign** (`Total Cost` / `3.25` / `USD`), which is why the blurb-anchor fix from 07-26 - and every other `$`-anchored regex in that extractor - went null. Repointed the extractor at the usage page, anchored on `Total Cost` with a `Total:` fallback, and made the number regex unit-aware instead of `$`-aware. The cap is now a configured constant (`MISTRAL_SPEND_CAP`, default `$30`) exactly like `GEMINI_SPEND_CAP`, since the UI no longer publishes one. Verified: `check mistral` returns `$3.25 / $30`, and a full `report` has all 4 console providers green.

*The deferral that cost us the same three days twice - now built.* The 07-26 entry deferred "same provider, same failure kind, N runs running - digest on the first, urgent on the third." It did not get built, and this break sat exactly three days again before Alex mentioned it, for exactly the predicted reason: three identical digest lines read the same as one. Second instance of the same miss, so it stopped being a deferral.

Built as `budget_state.failure_streak(kind, provider, failure_kind)` - counts back from the newest history line and stops at the first run where the provider read OK, wasn't present, or failed a *different* way (a `parse_failed` streak shouldn't be extended by an unrelated `reauth`). It returns **prior** runs only; each caller adds the current one. Both `_derive_issues` implementations now escalate a digest to urgent at `REPEAT_URGENT_RUNS = 3` and put `failing_runs` on the issue, with the detail line saying so out loud ("3 runs running - not flakiness, the check is broken"). `monitor_keys` passes no `failure_kind`, deliberately: its "likely transient (network, 5xx)" digest is a fair read once and an unfair one three times, whatever the specific error was.

Two notes on the tape. `_compact` now records the failure `kind` per provider row - it wasn't there before, only `ok`. Rows written before today have no `kind`, so the counter treats them as matching any kind rather than breaking the streak; that's what makes the check work on existing history instead of needing three fresh days to warm up. Verified by replaying the real tape with the last run(s) sliced off: as of this morning's scrape the Mistral prior-streak reads **3**, so the -30 run would have fired urgent - the escalation lands on day three exactly as specified, and `glm` correctly reads 0 on the same tape.

*State at end of day.* All 9 providers reading, no urgent on either loop. Console: GLM $4.49, Gemini $0/$250, Mistral $3.25/$30, Sakana $4.38. API: DeepSeek $7.67, Moonshot $6.36, xAI $6.69, OpenAI $9.17, Anthropic $28.74. Six of the nine sit under the $10 digest threshold, none under the $3 urgent one - that's Alex's top-up call, not a bug. Both alerting automations confirmed healthy on their own subsequent runs.

## 2026-08-03 - the Gemini check was green and blind for two months

*What landed.* The 4-day `parse_failed` streak on Gemini spend got fixed, but the interesting part is what the tape showed once we went looking.

**Marlow's escalation was right about the facts and wrong about the fix.** Her Telegram report was accurate on everything observable: `aistudio.google.com/usage` loads, the Spend view says "No Cloud Projects Available", there is no dollar figure to read, and 4 runs running means it's structural rather than flaky. Both remedies she proposed - import a Cloud Project, or disable the check - were wrong, because both accept the premise that the number is unreachable. It isn't. She diagnosed the page she was pointed at and never asked whether it was still the right page.

**Two separate breaks stacked on the same provider.** First, "Spend" stopped being a toggle on `/usage` and became its own sidebar page at `/spend`, so `click_js` returned `no-spend-tab` on every run and the extractor read the plain usage view. Second, and independently, both `/usage` and `/spend` are now scoped to *imported Cloud Projects*; Alex has none ("0 Projects"), so both render an empty-state panel with no figures at all. Either break alone would have been enough.

**The number never moved - it's on `/billing`, which is billing-ACCOUNT scoped and needs no project import.** It carries `Total cost $0.76` for the month *and* `Paid 1 · $250 Billing Account Tier Cap`, so the cap is now read live off the page instead of trusted from `GEMINI_SPEND_CAP` (the constant survives as fallback only). Deliberately did **not** reuse the old "largest `$` on screen" heuristic here: `/billing` prints the $250 cap, which would swamp the real spend and read as permanently maxed. Anchored on labels instead. Page's own caveat, worth remembering when a number looks stale: "Cost information may take up to 24 hours to update."

*The thing worth actually recording.* Pulling the tape: **68 Gemini runs since 2026-06-01, and today's `$0.76` is the first nonzero spend figure the check has EVER produced.** Every run before 07-31 reported a confident `$0 / $250` and counted as green. The old extractor took the largest `$` anywhere on the page, and it was picking up placeholder zeros the whole time. So the check wasn't broken on 07-31 - it broke at some point before we have tape for, kept reporting healthy, and 07-31 is merely the day the page changed enough that it could no longer even fake a number.

**The `parse_failed` streak was the first honest signal this check ever gave.** That inverts the instinct the alert creates. A monitor that starts screaming looks worse than one sitting quietly at zero, and it is strictly better: the loud one is telling you something true. The two-month silence cost us nothing here only because the spend genuinely was near zero - had Alex actually been burning Gemini budget, `$0 / $250` would have said "fine" all the way to the tier cap.

**The gap this exposes.** `failure_streak` catches a check that goes *loud*. Nothing catches a check that goes *quiet and wrong*. GLM, Sakana and both credit-balance readers already have placeholder-zero defenses (retry with longer settles, `suspect_zero` against the last known balance) precisely because an SPA zero fooled us on 06-11 - but those defend a *balance* falling to zero. A **spend** metric of zero is indistinguishable from healthy-and-unused, so it gets no such scrutiny, and Gemini sat in that blind spot for its entire life. Worth considering: flag a spend-type provider that has never once read nonzero across N runs as suspect rather than green. Not built today; recording it so the next "why didn't we catch this" has an answer already written down.

*State at end of day.* Console: GLM $13.69, Gemini $0.76/$250 (first real read), Mistral $1.47/$30, Sakana $7.34. API: DeepSeek $11.47, Moonshot $16.36, xAI $10.42, OpenAI $6.48, Anthropic $24.47. Gemini urgent cleared; remaining issues are two digest-level top-up nudges (OpenAI, Sakana, both under $10), which are Alex's call and not bugs.

**Self-heal record.** Diagnosis `diag_20260803_161951_scrape-stats` (`handlers/scrape_stats.py:177`), fix committed and pushed as `c0e0176ab8014a0b8ebcf0941f8a15abf0ad5db6`, live-validated post-commit (`check gemini` → `spend_usd: 0.76, cap_usd: 250`), marked resolved.

## 2026-08-03 (later) - a dropped connection read as a broken handler, and the recovery path that couldn't clear its own alarm

*What landed.* One transient failure, correctly reported and wrongly classified, plus a second bug found only by trying to fix the first.

**`werewolf_stats` was never broken.** The handler ran and succeeded: `stats_latest.json` was written at 13:37:41Z, nine seconds after the task started, `ok: true`. What died was the session narrating the result. From `~/.marlow/ops/sessions.log`:

```
[2026-08-03T13:42:20Z] === collect_stats_20260803_1033 (werewolf_stats) ===
Report is `ok: true`. Let me check yesterday's report for comparison...
Now let me write today's report following the same shape.
API Error: Connection closed mid-response. The response above may be incomplete.
```

The only lost artifact was the daily narrative report; the data tape was intact the whole time. Re-ran it on demand and `reports/stats/2026-08-03.md` now exists.

**This is the 07-30 gap again, one error class over.** `tick.sh` re-queues transient failures on `API Error: 5\d\d|Overloaded|Internal server error`. "Connection closed mid-response" is a transport-level drop, not a 5xx, so it missed by one string and fell through to `failed` - which `monitor_self` correctly escalated as "currently broken". Widened the pattern with named connection failures (`Connection closed mid-response`, `Connection error`, `ECONNRESET`, `socket hang up`, `fetch failed`). Deliberately did **not** add bare `timeout` or `terminated`: `scheduler.cmd_requeue` has **no retry cap**, so a pattern broad enough to swallow a real handler bug would re-queue it forever instead of surfacing it. Verified the widened regex against four real transient strings and four adversarial ones (a `KeyError` traceback, a handler timeout, the generic no-result-file message, an assertion failure) - all four match, none of the four over-match.

*The bug behind the bug.* After a clean re-run, the self-audit **still paged urgent for `werewolf_stats`**. `check_failed_ticks` groups records by `parent_task` and flags a group whose newest record failed. But `marlow run <handler>` queues `parent_task=f"{handler}_ondemand"` - so the recovery run landed in a *different group*, and the failed scheduled run stayed newest in its own group:

| run | `parent_task` | group |
|---|---|---|
| failed 13:37Z scheduled | `werewolf_stats` | `werewolf_stats` |
| clean 16:38Z recovery | `werewolf_stats_ondemand` | `werewolf_stats_ondemand` |

The docstring promised "a failure that already recovered won't nag." It only kept that promise for recovery by *scheduled* re-run. **`marlow run` is the sanctioned way to recover a broken automation - and it was the one action that could not clear the alarm it was meant to fix.** The alert would have kept firing every audit until the next scheduled tick ~18h later, which is precisely the window in which a human is most likely to conclude the monitor cries wolf.

Fixed by stripping the `_ondemand` suffix when grouping. Regression-tested the four cases that matter: recovery clears the alert; a *failing* on-demand run still pages (under the base name); a stale on-demand success does not mask a newer scheduled failure; distinct handlers stay separate. Confirmed live - `monitor_self check` now returns only the pre-existing `site_integrity` digest line.

*Worth noting about the escalation itself.* Both of today's alerts were accurate about what they observed and wrong about what it meant - the Gemini one recommended importing a Cloud Project when the number had simply moved pages, this one named a healthy handler as broken. The self-audit reports observations faithfully; it has no way to distinguish "the thing I watch is broken" from "the way I watch it is broken." Two for two today. That is the standing weakness of a monitor that can only see its own instrument.

*Also spotted, not fixed.* `marlow status` renders pre-split June state (queue and schedule both ~48d stale) regardless of `MARLOW_PROFILE`, apparently reading the unscoped `last_scheduled.json` rather than the `.ops`/`.writer` variants. Cosmetic - the audit and the scheduler themselves are profile-correct - but it makes the dashboard useless for eyeballing either loop, and it is why the werewolf_stats fix was verified via `monitor_self check` instead. Left alone as out of scope for today.

*State at end of day.* Ops loop: no urgent. One digest item outstanding (`cyber-eval-framing` thread frontmatter says `posts:4`, 3 published mention it - bookkeeping drift, not breakage).

## 2026-08-03 (evening) - the digest was reporting a $2.33 day as $0.93

*What landed.* Alex asked why the Werewolf stats I showed him in chat looked nothing like what arrives in Telegram. Answer: three renderers, and Telegram got the smallest. Chasing that turned up a live reporting bug.

**Three renderers, only the thinnest one leaves the machine.** `render_digest()` (compact, capped, 3 lines) goes to Telegram. `show` (full snapshot) is terminal-only. `reports/stats/<date>.md` (Marlow's prose, with a "what moved vs yesterday" section) is written daily to disk and read by nobody unless someone opens the file. The version closest to what Alex actually wanted already existed and had never once been delivered.

**The bug: `daily_burn` is a delta since the LAST SNAPSHOT, and `render_digest` labelled it "since yesterday".** That equivalence holds only if snapshots happen exactly once a day. Every `report` run resets the baseline, so a second run reports the sliver since the first. Today had four snapshots ($1.09, $0.02, $0.18, $0.93) and the 23:00 digest would have shipped the last one: **$0.93 for a day whose real burn was $2.33, understated by 60%.** Note `show` was always honest here ("spent since last snapshot (2.2h)"); only the digest mislabelled it. A silent-and-wrong number, same failure class as this morning's Gemini `$0`, found the same way - by having a second source to diff against.

Fixed by anchoring the day figure to a calendar boundary instead of to "whenever I last ran". New `_prev_day_baseline()` scans `stats_history.jsonl` newest-first for the last row dated before today; `daily_burn` now carries **both** `usd` (since last snapshot, honestly labelled) and `today_usd` (day-over-day). The digest uses `today_usd` only. Verified the property that matters: running `report` three more times in a row leaves `$2.22 today` unchanged, where the old code went to `$0.00`.

**Digest rewritten to carry what `show` carries** - 7d/30d trend on both users and games, cumulative burn, and each game's state and cost, which the old three-liner dropped entirely. Two deliberate choices:

- **`paid` revenue is no longer reported at all.** Per Alex today: the only paid user is *him*, so "$0.00 revenue" was a daily line that reads as a problem and is actually just an artifact of him being in his own database. Recorded the same rule in `.claude/skills/werewolf/skill.md`.
- **But `paid > 1` now fires a loud line** (`*** PAID USERS: n - that is a real paying customer, not just Alex ***`). Suppressing the noise without arming the signal would have been the worse half of the trade: a 1 to 2 move is the most important number in this project and looks like rounding next to user counts.

Edge cases checked against the real snapshot: paid=2 fires the alarm; 7 signups / 9 games collapses to bare counts at `DIGEST_LIST_CAP`; a failed report still renders its error; no-prior-day falls back to "(baseline set)".

*Cleanup, and my own mess.* Today's digest had **six** Werewolf blocks. One was the scheduled 13:37 run; the other five were mine, from re-running `report` to verify things - `report` appends to the digest as a side effect, which was made deterministic back when a session kept skipping the separate notify step. De-duped the file down to a single correct block (backup in scratchpad). Worth noting the side effect is load-bearing *and* a footgun: any manual verification run silently writes to Alex's evening digest. Now that `today_usd` is stable the duplicates would at least agree with each other rather than contradict, so this is downgraded from "wrong" to "noisy". Not fixed - a dedupe-on-append would have to touch `tools/notify.py`, which every handler shares.

*Open.* `marlow status` still renders pre-split June state regardless of `MARLOW_PROFILE` (noted this afternoon, still unfixed). Marlow's own narrative stats report still treats `paid revenue` as a tracked line; she does not read the skill file, so that needs either editorial feedback or a change to the `werewolf_stats` prompt.

---

## 2026-08-06 - two new game models, two new budgets, and a metric that isn't money

*Why.* Alex added Qwen (3.8-max, 3.7-plus, 3.7-flash) and MiniMax M3 to the Werewolf free tier the day before. The game is now on **11 provider keys** and budget monitoring covered 9 of them, so two live budgets were unwatched.

*Tier triage first, code second.* Both went through the same question the other nine did - is there a balance API, a cost API, or only a console? Probed live rather than trusting docs: MiniMax's `/v1/get_account_balance`, `/v1/query/account`, `/v1/user/balance` all 404, and `/v1/token_plan/remains` answers but only for a *subscription* key ("no active token plan subscription" on Alex's PAYG key). QwenCloud's own docs say billing is console-only, and DashScope has no balance route. So both land in Tier 3, console scraping, next to GLM / Gemini / Mistral / Sakana. **scrape_stats is now 6 providers; monitor_keys stays at 5.**

*The thing that didn't fit the existing shape.* MiniMax was easy - a real prepaid balance ($24.98, Alex's $25 top-up on 08-05), same `metric: balance` as GLM and Sakana, same placeholder-zero distrust. Qwen isn't money at all. QwenCloud gives new accounts **1M free tokens per model for 90 days** (expires 2026-11-05), and every model is set to "Free quota only" - auto-stop, so when a grant runs out the game's calls to that model **fail rather than start billing**. Its pay-as-you-go page reads `$0.00` and will keep reading `$0.00` the whole time. Scraping the dollar figure would have produced a monitor that is permanently green and completely blind - the same failure the Gemini check had for two months (see 08-03). So Qwen got a third metric, `quota`: percent-of-grant left on the three models the game actually uses, plus grant expiry.

*How the Qwen number gets read.* The console's own JSON endpoint (`/data/api.json?product=freetier&action=ListBailianFreetier`) is POST-with-CSRF - a plain GET from the page context returns `PostonlyOrTokenError` - so this is a rendered-table read. The table paginates 10-at-a-time over **260** models, so the handler drives the "Search models" box once per tracked model and reads the single matching row. Matching is on an **exact cell value**, because searching `qwen3.7-plus` also returns `qwen3.7-plus-2026-05-26`, a dated snapshot with an untouched grant - that row would have read as 100% healthy and masked the real one. A tracked model whose row doesn't resolve is dropped and named in a digest issue, never counted as 0%.

*Thresholds set from measured burn, not habit.* The dollar thresholds ($10 low / $3 critical) work because balances drain slowly. A token grant does not: the game burned **~20% of all three Qwen models in the first day of play**. At one scrape a day, a 25% threshold would fire once and be at zero on the next run. Set 50% digest / 20% urgent - about two days and one day of notice at the observed rate. Explicitly a launch-week rate; worth lowering if steady state is slower.

*A break found by accident, and the fix that generalizes it.* The first full run showed Gemini `parse_failed` for the second consecutive run - one more and the new repeat-escalation would have paged Alex. It wasn't a redesign: the page had "Total cost $1.95" sitting right there, and a warm re-read got it twice in a row. The cold headless Chrome that every cron run starts in just hadn't painted within `NAV_SETTLE_S`. Rather than tune Gemini's constant (which is what 07-28 and 07-31 did for Mistral and Gemini), `_check` now **re-reads once with a 12s settle before declaring parse_failed**. "The number isn't there yet" and "the console got redesigned" are indistinguishable from a single read, and one slow retry is cheap next to a false urgent. Cold-start run after the change: all 6 green, Gemini included.

*What surprised us.* Three of the four Tier-3 breaks on record are now timing, not layout - GLM's placeholder zero (06-11), Gemini today, and arguably Mistral's first. The scraping tier's real enemy is a page that isn't finished rendering, not a page that changed.

*State at end of day.* 11 of 11 providers monitored: 5 via monitor_keys (API, twice daily), 6 via scrape_stats (console, daily). Qwen at 78.9% worst-model quota, MiniMax at $24.98. Sakana is low ($3.54) and OpenAI/xAI are near the $10 line - all three riding their normal digest path. Alex logged the scrape profile into both new consoles; that session is the load-bearing part, and it will lapse like the others eventually.

*Postscript - the snapshot job ate the commit.* While this was being written, Marlow's own nightly `commit_artifacts` tick fired (19:51 local) and swept the in-progress `handlers/scrape_stats.py` and `driver/budget_state.py` edits into `2bfa4ff chore(snapshot): nightly artifact backup 2026-08-06` - a 279-line handler rewrite recorded as an automated artifact backup, with no statement of intent anywhere in the history. It happened to catch a finished state; it just as easily could have committed a half-written extractor. The snapshot commits **whatever is in the working tree** for its 18 paths, and `handlers/` is one of them - so any human or Simona edit in flight at 19:51 gets absorbed. Not fixed tonight. Options are narrowing the snapshot to genuinely generated artifacts (reports, digests, memory) and dropping source dirs, or having it skip paths with unstaged changes it didn't author. Worth doing before it lands a broken handler on a night nobody is watching.

---

## 2026-08-08 - the rules got a rule the watch could not enforce

*Why.* Alex started getting ad posts in the Discord server and found them very annoying. One came from someone who arrived via Viberank, where Alex had posted Werewolf AI on 08-02 asking for upvotes - and the poster did not even upvote the project. So: a drive-by that used the community as an ad surface and gave nothing back.

*The rules already said it, quietly.* The #rules embed had "No ad dumps, no self-promo blasts" buried inside rule 4 (Don't spam or flood). That framing makes ads a *volume* problem, which is exactly wrong for the case Alex hit: a single message is not a flood. Promoted it to its own **rule 4, "No ads"** - referral and affiliate links, paid promotions, "check out my product" posts, unsolicited sales DMs, and the specific shape of joining to drop a link. Spam and flooding stayed as rule 5. Edited the existing embed in place (message `1520875053632323645`) rather than reposting, so no dead link and no re-ping.

*The half that actually matters.* `monitor_discord` reads new member messages every 6h and judges tone, but its judgment pass listed rudeness, hostility, harassment, scams, derailing, pestering - and nothing about ads. The deterministic side would not have caught it either: `LINK_FLOOD` needs 5 links from one author in a window, and a drive-by ad is one message with one link. **Marlow would have read the ad and correctly decided it was polite.** Added the ad/promo shape to the task's judgment pass with the tell spelled out: judge the *account's pattern*, not the link. A regular who mentions their own project mid-conversation is fine and must not be flagged; a new or silent account whose only contribution is a link is an ad, flag it even at one message. Digest-level normally, urgent on repeat or DM-bait.

*What we could not find.* Swept every channel the bot can read for the offending post - nothing. It was a DM to Alex or he had already deleted it. Worth noting for future sweeps: the non-hiper2d entries in #general with empty content are member-join system events, not messages the bot is blind to. The Message Content intent is on and working.

*A gap left open.* `MONITORED` is general / general-discussion / ai-news. **#welcome is not on the list**, and it is the one channel a newcomer is explicitly invited to post in - the natural landing spot for exactly this kind of drive-by. Not added today; flagging it as the obvious next tune.

*Timing.* A `scan_discord` tick went in_progress while the yaml was being edited, so the new judgment text is live from this run onward.

## 2026-08-11 - deleted the checkpoint scaffolding; the no-resume semantics are now written down

*Why now.* Writing up the self-improvement arc for a dev.to piece surfaced that `checkpoint`
reads as a working feature in three places (the queue schema, `README.md`, and `CLAUDE.md`,
which Marlow loads every tick) and has never once been populated. The 2026-06-09 decision to
defer it was correct and 900s made `draft_article` fit, so the field has been dead for two
months while documenting a resumption path that does not exist. Alex's call: delete it rather
than build it.

*The argument against ever building it.* A checkpoint is state written by the thing whose
failure you are recovering from, so a session that dies mid-work leaves a checkpoint exactly
as trustworthy as the session that died. Resuming from a half-written one produces a task that
continues confidently from a corrupt position and reports success - strictly worse than
redoing fifteen idempotent minutes. Real checkpointing would also mean restructuring the
drafting flow inside `CLAUDE.md`, i.e. an identity file Marlow can never edit herself.

*What changed.* `driver/scheduler.py`: dropped the `checkpoint` field from `QueueItem`, the
`--checkpoint` arg, its assignment in `complete`, and the usage line. `driver/tick.sh`: dropped
`"checkpoint": null` from the no-result-file fallback JSON. `CLAUDE.md`: removed
`subtask.checkpoint` from the subtask fields and from the result-file schema; the context line
now names `timeout_sec` instead, which is the mechanism that actually exists. `README.md`: the
`in_progress` bullet and the queue-schema section now state the real behaviour.

*The migration order mattered, and it is worth recording.* `load_queue()` does
`QueueItem(**item)`, so a persisted key with no matching field is a `TypeError` that would kill
the scheduler and therefore the whole loop. Eight live items across `queue.json` and
`queue.writer.json` carried a null `checkpoint`. Because the field had a default, stripping the
JSON first is safe under the *old* code, and removing the field second is safe under the
*stripped* JSON - so there is no window where the two are incompatible. Backed up all three
queues first, verified no non-null checkpoints existed before stripping, and re-checked
afterwards that no tick had re-added the key via `asdict`. Both profiles load, `dry-run` picks,
`complete --help` is clean.

*The gap this documents rather than fixes.* There is no solution for a task that needs longer
than one tick - only an avoidance. A timed-out subtask is SIGKILLed (exit 124), stays
`in_progress`, and is re-picked ahead of new work next tick, restarting from scratch. That is
safe only because handlers are idempotent. **A handler that cannot make progress inside its
timeout will repeat its opening every 20 minutes forever, and nothing in `monitor_self` will
call that a failure** - the same quiet-and-wrong class as the Gemini check. The cheap detector
would be a resumed-N-times-without-completing counter. Not built; `README.md` now at least warns
about it instead of implying resumption works.

*Note for whoever reads git next.* These four framework files were left uncommitted pending
Alex's review, which means tonight's `commit_artifacts` sweep (`git add -A`) will fold them into
a `chore(snapshot)` commit with no statement of intent - the footgun recorded on 2026-08-08.

## 2026-08-12 - the Qwen monitor had never once read the setting it was reporting

*What landed.* `handlers/scrape_stats.py`: the Qwen free-tier extractor now reads the per-model
auto-stop state off the row's `<button role="switch" aria-checked>` and emits an `auto_stop`
bool, replacing the `mode` string it used to scrape from the cell's `innerText`. Severity in
`_derive_issues` branches on it: a guarded model keeps the 50/20 thresholds and pages on zero;
an unguarded one skips both pre-warnings and emits a single `quota_crossover` digest at 0%.
Added `guarded_models` so a still-guarded model that isn't the worst one gets named, since
nothing in the old shape would ever have mentioned it. `auto_stop: null` means the control was
missing: that emits `parse_failed` and falls back to the guarded read rather than guessing.

*The bug.* The Actions cell holds the toggle **plus a static label reading "Free quota only"
that never changes**. The extractor read the label. So it reported every model as auto-stopped
regardless of switch position, and had done since it shipped on 08-06 - it never observed the
real setting even once. This surfaced when the 08-12 tick fired an urgent saying qwen3.7-plus
at 7.6% would "stop rather than bill", Alex said auto-stop was off for the models he uses, and
the console agreed with him: `aria-checked="false"` on all three, and on all ten rows of page one.

*Decisions reconsidered.* The 2026-08-06 entry below states as fact that "every model is set to
Free quota only (auto-stop), so an exhausted grant makes the game's calls fail, never bill."
That was never verified - it was the parse bug reflected back. Correction: the free grant is
always spent before the card, so with auto-stop off, exhaustion is a silent handoff to
pay-as-you-go, not an outage.

*Things that surprised us.* Tier 3's failure taxonomy gets a third entry, and it is the worst
shape yet. GLM 06-11 read a plausible wrong number. Mistral 07-26 read nothing and failed loud.
This one read a **real string off the real row** and was wrong about what the string meant - no
parse error to catch, no zero to distrust, and the value was stable across every run, which
reads as healthy. The generalizable rule: a cell that renders text next to a control is not a
state readout. Check for an input inside the cell before parsing its text as state.

*Worth recording from the docs* (`docs.qwencloud.com/resources/free-quota.md`, since none of this
is inferable from the console): the grant is one-time and non-renewing, 90 days from account
activation, remainder void at expiry and never reissued. But a model released *after* signup
gets its own fresh 1M dated from its release, and a dated snapshot counts as a separate model
from the undated latest - so adding Qwen models to the game is also adding free grants. Tool
call fees (built-in web search, $10/1k calls) are not covered by the grant.

*What's deferred.* Qwen still has no money metric. Once auto-stop is off the honest thing to
track after crossover is spend, but the console's pay-as-you-go page has read $0.00 all month
and there is nothing yet to learn its shape from. Waiting for real charges before designing it;
until then `budget_state.render()` keeps printing the quota percent every run, which is
visibility without alerting, and that is what Alex asked for.

*State at end of day.* Verified against the live console: all three tracked models
`auto_stop: false`, today's reading produces zero issues. Derivation exercised across eight
states (guarded/unguarded/unreadable x above/below/at zero). Marlow + Simona.

## 2026-08-22 - a critical alert that was arithmetic, not a balance

*What landed.* `budget_state.render()` rewritten. It grouped providers by which handler read
them (`monitor_keys` vs `scrape_stats`), which is our plumbing, not Alex's question. He asked
for "how much money do I have on each key," so the report now groups by what the number *is*:
MONEY LEFT (eight depleting prepaid balances, sorted ascending so the next top-up is the top
line, with a total), POSTPAID (Gemini and Mistral, metered against a cap, nothing to run out
of), FREE GRANT (Qwen tokens), NOT READ (failed reads). Three unlike things had been rendering
as one list and reading as if they were all balances.

Each money row now states how its number was obtained: `read live`, `scraped`, or `derived`.
That column is the actual fix for the day's incident.

*The incident.* The 20:00 UTC tick fired urgent: OpenAI $2.26, under the $3 critical floor.
Alex had already topped up. The number was not a balance - OpenAI exposes no balance endpoint
(re-verified against live docs today, along with Anthropic's; both still cost/usage only), so
Tier 2 reconstructs it as `baseline - spend since baseline`. The baseline was a console figure
read on 08-09. A top-up is invisible to the cost API, so the derivation kept subtracting real
spend from a number that predated the payment and produced a confident, wrong, actionable
alarm. Everything downstream was correct; the input was three days past meaning anything.

*The failure mode worth naming.* A broken scrape fails loud - `parse_failed`, `reauth`, and you
get told. A stale baseline fails quiet and wrong, and the first symptom is a critical alert you
believe. Failing loud is the stated design goal of this whole system and Tier 2 does not meet
it. Same shape as GLM's placeholder zero (06-11) and Qwen's label-vs-switch (08-12): the third
time a plausible wrong value has beaten a loud failure to the alarm.

*Decision reconsidered mid-change.* First version flagged a derived row for re-anchoring once
the baseline passed 14 days. OpenAI's was 13 days old - it would have stayed silent through the
exact incident that motivated the flag. Age was the wrong trigger. It now also prompts whenever
a derived balance drops under the low threshold, which is the moment Alex reaches for his card
and therefore the moment an already-made top-up needs surfacing. Anthropic's baseline, dated
2026-05-31 and 83 days old, trips the age half and is a live open question: its $16.95 is only
right if that key has not been topped up since May.

*Also fixed.* Qwen's row reported the worst model alone ("0% on qwen3.8-max"), which reads as
one model when all three tracked models are dry. It now says 3/3.

*What we tried and where it stands.* Alex's question was the good one: why derive at all,
instead of reading the balance and comparing to $10? Because for these two the balance exists
in exactly one place, the console page - which is what `scrape_stats` already does for six
providers. Moving OpenAI to Tier 3 would delete the manual re-anchor entirely. Tested the
plumbing: navigation and JS eval against `platform.openai.com/settings/organization/billing/
overview` on the port-9223 profile both succeeded and returned a plain `/login` redirect. No
bot wall, no Cloudflare challenge - the profile simply has no OpenAI session, which is the
cheap failure. One headful login unblocks it. Not built yet.

*Open.* Re-anchor OpenAI (needs the console figure, or the login above which yields it);
confirm whether Anthropic has been topped up since 05-31; decide whether OpenAI moves to Tier 3.

*State at end of day.* Report renders across all 11 providers plus a synthetic degraded case
(failed read, missing fields, absent snapshot). `save`/`load_latest`/`failure_streak`/
`STATE_DIR` untouched, so both handlers are unaffected. Total across 8 prepaid keys reads
$97.38, of which the OpenAI line is known-wrong pending the re-anchor. Simona.

## 2026-08-22 (later) - pokerwithai.net joins the watch, and the keys turn out to be shared

*The finding that reframed the request.* Alex asked to add pokerwithai.net as "one more website
to monitor." Before building anything, fingerprinted its provider keys against Werewolf's:
SHA-256 of each value in poker's `.env` vs the werewolf Firestore `freeTierApiKeys` map, hashes
compared, values never printed. **All eleven are byte-identical.** The two sites are one
operation on one set of accounts.

That means the budget half of "monitor poker" was already done and had been for as long as poker
has been live - and also that the report had been quietly mislabelled. Every balance in it is
the combined drain of both games. Renamed the header to `API budget - shared game keys
(aiwerewolf.net + pokerwithai.net)` with the verification recorded in a comment beside it.

Two consequences worth keeping in view. Neither site's spend is separable from the other's: the
cost APIs see one org, so today's OpenAI drain has no attribution and cannot get one without a
per-site cost signal. And either site can starve the other - if poker gets traction, Werewolf's
free tier dies with nothing in the alert naming poker as the cause. Alex's call was to flag it
and decide later, so no key split, no attribution layer. Recorded, not fixed.

*What landed: `monitor_uptime`, both sites, hourly at :30.* The real gap was that nothing in
werewolf-ops had ever fetched a page. `monitor_cloudflare` reads zone/DNS/SSL and Pages deploy
status, `monitor_health` reads game docs, `monitor_betterstack` reads logs - all three can be
green while a visitor gets a 500 or a blank shell, which is exactly what a successful deploy of
a broken build looks like. So the new handler does the dumb thing none of them do: GET the page
like a stranger.

Three failures kept distinct: unreachable or non-200 is `site_down` (urgent); 200 with the
content marker absent is `content_missing` (digest, urgent at 3 consecutive runs); 200 and
correct but over 10s is `site_slow` (digest). The middle case is the reason the handler exists -
a 200 serving an empty body is what a status-code check calls healthy. The marker is the page
`<title>`, which survives restyling and cannot appear on an error page. Every check retries once
before it counts; a dropped connection on an unattended cron is not an outage. No credentials at
all, which is the nicest property it has - nothing to provision, rotate, or expire.

Verified live rather than assumed: happy path on both sites (Werewolf 0.24s/Cloudflare, Poker
1.60s/Vercel, later 0.17s and 0.37s warm), plus every failure branch exercised - a dead domain,
a real 404, a deliberately wrong marker against a live 200, an over-threshold latency row, and a
synthetic two-run history proving the third consecutive `content_missing` escalates to urgent.
Slow threshold set at 10s deliberately loose: poker's cold start is ~1.6s and a tight threshold
would only teach us to ignore the digest.

*Registration is documentation here, not code.* There is no handler registry - `driver/scheduler.py`
globs `projects/*/tasks/*.yaml` and filters on `profile`, and the in-tick flow lives in the YAML
comment block. So the task is only real once `profiles/ops/IDENTITY.md` and the README task table
name it. Both updated. Confirmed the ops profile loads it (`schedule: 30 * * * *`, handler
`monitor_uptime`) and that, being first-sight, it will not fire immediately - it gets marked now
and starts at the next :30, which is the behavior we want from a newly added hourly job.

*Deferred, and why.* Poker's game-error watch is NOT built. Poker parks a failed lane by writing
`ERROR_FIELD[lane]` onto the game doc and emitting `log.warn('lane stopped ...')`, so its errors
reach both Firestore and BetterStack. BetterStack is the cheaper path by a lot: poker has its own
Firebase project, so the Firestore route needs a second read-only service account provisioned,
while the log route may need nothing at all - the existing ClickHouse credential is team-scoped
(`t507167_*`) and would likely reach poker's source too. Could not confirm it: `SHOW TABLES`
returns empty (BetterStack exposes only the `remote()`/`s3Cluster()` table functions, not a
catalog) and we hold only ClickHouse credentials, no Telemetry API token to list sources. Probed
nine plausible table names and got `NAMED_COLLECTION`/`CLUSTER` errors on all of them. Stopped
there rather than keep guessing - the api-docs discovery lesson applies to table names too.
Needs one string from Alex: poker's source table name from the BetterStack UI.

*Scope note.* `monitor_uptime` lives in `projects/werewolf-ops/` but covers both sites, which is
now slightly wrong on the label the same way the budget report was. If poker grows its own ops
surface, this and the budget watch both want lifting into a shared `game-ops` project rather than
being copied. Flagged in the task YAML, not decided.

*State at end of day.* Nine ops tasks, up from eight. Both sites up. Poker's error watch blocked
on one lookup; the OpenAI re-anchor still blocked on the console figure or the headful login.
Simona.

## 2026-08-22 (night) - the daily stats had been reporting a nine-hour slice as a day

*How it surfaced.* Alex noticed a Telegram digest saying 1 new user and 1 game and didn't believe
it. He was right not to. The number was accurate for the instant it was computed and wrong as a
day count, which is the worst combination - it looks like data.

*The bug.* `werewolf_stats` ran at `0 9 * * *` and defined `today` as since-UTC-midnight, so it
counted a nine-hour slice and labelled it a day. Worse, that slice - 00:00 to 09:00 UTC - is
20:00 to 05:00 Eastern, the deadest hours Alex has. The real 2026-08-22 was **6 new users and 8
games** (7 by his local day boundary); the digest said 1 and 1, because at the 10:10Z snapshot
exactly one user had signed up and exactly one game had been started by a new user. Five users
and six games arrived afterward.

This was not a one-off. `stats_history.jsonl` shows the shape all the way back to June: rows
reading `new_users_today: 2` on days where `users_total` rose by five. Every daily digest since
the handler shipped has under-reported the day, and the trend lines drawn off `new.today` were
measuring overnight traffic, not days.

*Also worth naming: there was no "8 visits" metric.* The figure Alex remembered being told did
not come from traffic data - `monitor_cloudflare check-traffic` returns only azelianouski.dev and
the Marlow blog, because **aiwerewolf.net has no Web Analytics beacon**. There is no visits number
for the game site at all. 8 is exactly the count of games created in the Aug 22 UTC day, so it was
almost certainly games relabelled somewhere. Recorded because "the site has no traffic metric" is
itself a thing we keep half-forgetting.

*What landed.* The reported day is now a COMPLETE day in `America/New_York` (`MARLOW_LOCAL_TZ`
overrides). New `period` block on every report naming the date, tz, and exact UTC bounds, so the
report states which day it is about rather than leaving it implied by when it ran. Counts renamed
off the misleading word: `new.today` → `new.day`, `new_today_emails` → `new_day_emails`,
`today_games` → `day_games`, `created_today_by_new_users` → `created_day_by_new_users`. Renames
rather than a quiet semantic swap, deliberately - a key called `today` that means "yesterday" is
the same species of bug as a derived balance that looks read.

The still-running local day is reported as `today_so_far`, always printed with the word PARTIAL.
That is the honest home for the number the old code was accidentally producing, and a manual
mid-afternoon run now answers "what's happened today" without pretending to be a day total.

`_prev_day_baseline` moved onto the same boundary: it takes the last snapshot stamped before the
reported day's local midnight, rather than before UTC midnight. The property that a second manual
`report` can't shrink the day's spend (the 2026-08-03 fix) is preserved, just anchored correctly.

*Schedule, and the DST trap.* Alex asked for midnight his time. `driver/scheduler.py` evaluates
cron in UTC with no timezone support, and his offset moves: EDT midnight is 04:00 UTC, EST
midnight is 05:00 UTC. A literal `0 4` would fire at 23:00 local all winter, *before* the day it
reports has ended. Settled on `5 5 * * *` - 01:05 EDT, 00:05 EST - the earliest slot that lands
after local midnight in both seasons. Verified with croniter against an August and a December
base. Reporting a closed day beats hitting midnight exactly; making it exact needs timezone
support in the scheduler, which is a driver change nobody has asked for.

*Verified, not assumed.* Dry-ran the new report without persisting (so no off-schedule row entered
the burn tape). It reported 2026-08-21 as the last complete local day - 3 new users, 6 games,
$1.66 spent - and its PARTIAL line read "6 new users · 7 games" since local midnight, matching to
the unit an independent Firestore count of Alex's Aug 22 done by hand before any code changed.
That cross-check is the whole reason to trust the rename.

*State at end of day.* Tomorrow's 05:05 UTC run is the first under the new scheme and will report
Aug 22 as a full day: 6 users, not 1. Old-format history rows still parse for the burn baseline
(`checked_at` and `live_cost_usd` are unchanged), so the series is continuous across the change.
Simona.

## 2026-08-22 (night, cont.) - the owner is not the audience

*What landed.* `werewolf_stats` now excludes Alex's own account from every ACTIVITY metric:
user total, tier split, new-user counts and emails, games created, the per-game detail lists, and
the in-progress `today_so_far`. Driven by `EXCLUDED_OWNERS`, overridable via `MARLOW_STATS_EXCLUDE`
for test accounts. He plays to test, so his rows were inflating exactly the numbers the report
exists to answer - is anyone else finding this. Effect on the current snapshot: 288 users → 287,
85 live games → 81, and the Aug 21 day 6 games → 4.

*Where the exclusion deliberately stops: money.* His four live games cost $3.24 of the $45.89
cumulative, and that is real spend against the same provider keys the budget watch reconciles.
Quietly removing it would make `live_cost_usd` stop matching the drain - the same failure mode we
spent the earlier half of tonight fixing, where a number kept its label and lost its meaning. So
the total stays whole and the split is reported instead: `live_cost_usd` (all),
`live_cost_usd_excl_own`, `own_live_cost_usd`. The day-delta gets an `day_usd_excl_own` twin, but
only when BOTH ends of the interval carry the field - baselines written before tonight don't, so
until tomorrow the digest says "$1.66 incl. yours" rather than computing a net figure against a
gross baseline and presenting it as net.

*The exclusion is never implicit.* Every report carries an `excluded` block (owners, users dropped,
games dropped, their cost) and both renders print it. A filter nobody can see is how a number ends
up meaning something other than its label, which is the through-line of this entire session.

*Two consequences that had to move with it.*
- The digest's paid-user alert fired at `paid > 1`, because Alex was the only paid account and
  "more than one" was the test for a stranger paying. With him excluded, `paid` counts only real
  customers, so the threshold dropped to `>= 1`. Left alone it would have stayed silent for the
  actual first paying customer - a latent bug created by the exclusion, not by the old code.
- `_user_spend_mtd` summed all users, so "paid = actual revenue: $3.90" was Alex paying himself.
  Excluded accounts now accumulate into a separate `excluded_own` bucket. Revenue reads $0.00,
  which is the truth, with his $3.90 shown alongside rather than deleted.

*Verified.* Splits reconcile ($42.65 + $3.24 = $45.89); the two Aug 21 games that vanished from
the day list are precisely his two; the paid tier goes 1 → 0; legacy snapshots still render through
`_upgrade_legacy`. All dry-run, nothing persisted.

*Closed same session.* Asked whether other test accounts needed excluding; Alex confirmed
hiper2d@gmail.com is his only account. The hardcoded default is therefore the complete list and
`MARLOW_STATS_EXCLUDE` stays unset - it exists for a future test account, not a current gap.

## 2026-08-24 - bounding the memory files, and what an unenforced cap is worth

*What landed*

- `handlers/_memory_compact.py` (new). Two shared primitives, deliberately
  different in kind: `truncate_fifo` (deterministic, code-enforced) for the file
  the code bounds, and `analyze` (pre-split, protected tail) for the files Marlow
  bounds with judgment. Imported by `grade_memory`, `self_reflect`, `self_review`
  and `monitor_self` so there is one contract instead of four.
- `grade_memory bound-working` - `working.md`'s `## Daily rollups` region is now a
  fixed-size FIFO, hard-capped at 12KB. `## Current state` and `## Outstanding
  requests` are exempt: facts there expire when they stop being true, not on a
  schedule, and a FIFO would drop a true fact for being old. Applied once by
  hand: 152KB -> 78KB, 7 rollups dropped, newest 2 kept verbatim, head
  byte-identical.
- Protected-tail compaction wired into `self_reflect` (self-reflection diary) and
  `self_review` (voice journal, which had no bound of any kind). The three
  newest entries are handed over pre-separated and are off-limits; only the older
  region folds into the standing section. Standing sections get their own, much
  higher threshold so they are re-synthesized rarely.
- `memory/lessons.md` (new) - long-term memory, read every tick. Replaces the
  `memory/archive/` weekly-synthesis layer, which the contract described from May
  and which was never built. Seeded with the two lessons that were about to age
  out of the rollup window.
- `monitor_self` gains `check_memory_bounds`. Every memory file loaded into a
  tick now has a daily assertion on its size.
- `profiles/root.md` memory rules and the writer IDENTITY grader/reflect/review
  flows rewritten to describe what the code now does.

*The actual finding - and a correction to the first version of this entry*

The first draft of this entry said the grader "read the cap every night and
declined every night," and framed it as a capable model ignoring an instruction.
That was wrong, and the correction is the more useful finding.

She was not ignoring it. Her -23 grading pass compressed the rollup section
**58KB -> 27KB** in a single tick, taking the file 123KB -> 92KB. Then she wrote
this, under Outstanding requests, and it sat there:

> working.md is ~9x over its ~10KB cap and rollup compression is now exhausted.
> That is as far as my sanctioned lever goes. The remaining bulk is "Active
> threads" (~51KB) - single bullets run 2-4KB and duplicate the job of
> `projects/research/threads/*.md`. Proposal unchanged and now blocking:
> sanction moving per-thread anchor detail into the thread files and hold
> working.md thread bullets to 2-3 lines each. Every tick reads this file; at
> 92KB that is a real per-tick tax across ~40 ticks/day.

That is the correct diagnosis, the correct fix, the right escalation channel, and
an accurate cost estimate. She compressed everything she believed she was allowed
to compress, correctly identified that the rest was *state* rather than log, and
asked for sanction to touch it. Nobody answered. The request had been sitting
across multiple daily rollups, restated each night.

So the failure was never "the model won't follow the instruction." It was two
things:

1. **The lever she was given was too small for the problem.** Rollup compression
   could not reach the bulk, and the bulk lived in a section the contract
   discouraged her from rewriting unilaterally.
2. **The escalation channel was write-only.** `profiles/root.md` tells her that
   when something is out of her scope she should "propose changes in `working.md`
   under Outstanding requests." Nothing ever read that section back. A request
   there is a dead letter unless a human happens to scroll past it.

The generalizable lesson is not about prompts versus code, though that still
holds for the rollup FIFO. It is: **when you bound an agent's authority, you own
the queue where it files what it cannot do.** An unanswered request is the one
failure mode an autonomous loop cannot route around by design - it did the
correct thing and the correct thing was to wait.

Fixes, both landed: the rollup region is now bounded in code so that lever is no
longer hers to pull, and `monitor_self` now reports open-request queue depth so
the queue is drained rather than accumulated. The Active-threads sanction is
granted, executed, and recorded as standing so she never has to ask again.

*Things that surprised us*

- `self-reflection.md` had compacted itself down to **one** raw dated entry
  behind 8.6KB of standing text. The threshold worked; nothing protected the
  tail, so the distillation ate almost all of the primary material. The
  protected-tail rule was designed against a hypothetical and turned out to be
  fixing something already in progress.
- The first FIFO implementation made the problem worse in a way that only showed
  up in a dry run: `### Earlier` had accumulated dropped *prose* to 7.4KB, and
  being exempt from the queue it starved the 12KB cap down to a single retained
  day. A bookkeeping line that grows is not bookkeeping. It is dates and a
  pointer now.
- Second bug, same section: rendering "first .. last (N days)" and re-parsing by
  counting dates recovers 2, not N. The record of how much history had aged out
  was silently resetting on every pass. Now parsed by an explicit span regex and
  verified idempotent over repeated runs.

*Decisions reconsidered*

- Per-rollup size started as a hard truncation and ended as a *report*. Cutting
  prose mid-sentence to hit a byte count makes the record worse, and the FIFO
  bounds the file either way - entry size only decides how many days fit in it.
  It is surfaced to `monitor_self` instead.
- The oversized-entry alert was a count threshold (`>= 3 fat rollups`) until the
  dry run showed it stops firing exactly when the problem is worst: once fat
  entries have evicted their neighbours, too few remain to trip a count. It
  warns on retained *window length* now, with the fat entries named as cause.

*What's deferred*

- `voice-journal.md` still holds a 26KB backlog across 14 compactable entries.
  Left to her first `self_review` tick deliberately: it is her voice, and the
  design says she distills it. The audit flags it daily until it lands.

*Also landed, same session: the Current state rewrite*

Once the sanction question was answered, `## Current state` was rewritten
against verified ground truth rather than summarized. It had frozen around
2026-06-16 and drifted badly: it claimed **nine posts live** when nineteen are
published, carried a "Pending drafts: ONE" entry for an article that shipped on
-17, and listed a dozen active threads when eight thread files exist. Most of
its 67KB was closed items kept as struck-through history and a "Pending
follow-ups" section that had become an append-only curate log.

Checked against disk before writing: published count and latest slug, drafts
directory (empty), every thread file's `posts:` and `last_synthesized:`, the
framework-fix log, and the newest health report. Closed alerts were dropped
rather than struck. The `temperature is deprecated` app bug was dropped on
evidence: last seen 2026-07-15, absent from every report since. Durable lessons
went to `lessons.md`; the rest is recoverable from the repo history.

67KB -> 5.6KB, under the 6KB warn. Whole file 152.8KB -> 16.6KB.

*State at end of day*

Memory total across bounded files 117KB, down from ~192KB. Two of six files at
target with no work needed, three now enforced, one (Current state) awaiting her
own pass. Every bound is either a function or a daily assertion; none is only a
sentence.

## 2026-08-24 — self-heal: handlers/monitor_cloudflare.py

`monitor_cloudflare`'s 09:00Z run came back `ok:false`: `_list_ssl_packs()`
caught only `RuntimeError` around its certificate-packs fetch, but a plain
HTTP error (`resp.raise_for_status()`) raises `requests.HTTPError`, a subclass
of `requests.RequestException` — not caught. Zone `pokerwithai.net` 500'd once
(transient, retry succeeded), and the uncaught exception propagated out of
`check_zones()`, failing the whole report instead of degrading just that one
zone's `ssl_packs` to `[]` as the inline comment promised ("skip silently").
Every other list helper in the file (`check_pages`, `check_workers`,
`check_registrar`) already catches `(requests.RequestException, RuntimeError)`
— `_list_ssl_packs` was the one holdout. Widened its `except` clause to match.
Smoke-tested: `report` returns `ok: true`, `issues: []`. Diagnosis
`diag_20260824_120759_monitor-cloudflare`, commit `a92b717`.

## 2026-08-24 - the stale-artifact alert could not tell broken from queued

*What landed*

`check_output_freshness` is now dormancy- and queue-aware, matching what
`check_scheduler_freshness` has done since June.

*What happened*

The memory-bounds work surfaced an unrelated urgent: "werewolf_stats snapshot is
31h stale - the tick ran but produced nothing, or stopped." It had not stopped.
`collect_stats` has completed `done` every day for a week. A 9.5h overnight
dormancy gap (01:48Z -> 11:19Z, laptop asleep) swallowed the 05:05Z slot; the
scheduler re-enqueued it on wake and it was sitting `pending` in `queue.ops.json`,
draining behind a backlog at roughly one subtask per 22 minutes.

So the artifact was late for a completely benign reason and the audit paged
urgent about a handler that was fine. `check_scheduler_freshness` already knew
how to make this distinction - it was written in June precisely so an overnight
sleep does not page per-tick - but `check_output_freshness` was age-only.

Two suppressions now, both downgrading to digest rather than silencing:

- **Producer queued.** `FRESH_ARTIFACTS` entries name their producing handler;
  if a subtask with that handler is `pending`/`in_progress`, the artifact is late,
  not broken. The precise case, and it covers catch-up windows the heartbeat test
  cannot see.
- **Driver dormant.** Reuses `_max_dormant_gap_min` over the staleness window.

Neither suppresses the issue outright, so a genuinely wedged queue still surfaces
on the next audit - the difference is that it surfaces as a digest line instead of
a 2am page.

*Things that surprised us*

Running `monitor_self check` by hand is not representative. With `MARLOW_PROFILE`
unset it reads the legacy global `tasks/queue.json` and `~/.marlow/heartbeat.log`
rather than the per-loop state, which produced a nonsense "~1150h dormant gap" and
an empty pending set. Scoped correctly, ops takes the queued branch and writer
takes the dormant branch, both with real numbers. Any manual audit run needs
`MARLOW_PROFILE=ops` or `=writer` to mean anything.

*The point*

An alerting path that cannot separate "broken" from "late" spends its urgent
budget on weather. Every overnight sleep was paging about a healthy handler, and
the cost of that is not the page - it is that the next real urgent gets read with
the same shrug.

*Open, not fixed*

`FRESH_ARTIFACTS` is not profile-scoped, so the writer loop also audits the ops
loop's snapshot. Harmless now that both paths are digest-only, but it means the
same staleness is reported twice on a bad morning.

## 2026-08-24 - the budget watch stops deriving what it can read

*How it surfaced.* A Telegram urgent said OpenAI was at $0.40, "4th consecutive
critical check, 97% of the $13.36 baseline spent." Alex didn't believe it. He
was right: the console held $20.05. Second false CRITICAL from the same cause in
three days.

*What was actually fixed on 08-22, and what wasn't.* That entry ends with an
explicit *Open* line - "Re-anchor OpenAI; decide whether OpenAI moves to Tier 3."
Neither happened. What shipped that day was the *labelling* in `budget_state`:
a derived row now prints "RE-ANCHOR if topped up since" when it drops under the
low threshold. That is a caveat on a report you have to go and ask for. The
`monitor_keys` alert path was never touched, so the alert kept firing with full
confidence while the caveat sat in a place nobody was looking. **Fixing how a
wrong number is *described* is not fixing the number.** The stale baseline from
08-09 survived two top-ups and paged Alex four times.

*What landed.*
- **OpenAI and Anthropic both left Tier 2 for a console read in `scrape_stats`.**
  Retiring a provider needed no code change at all: the tier is opt-in on
  `(admin key AND an entry in tier2_baselines.json)`, so emptying the file to
  `{}` retires both cleanly and silently. `monitor_keys` is now three direct
  balance APIs and derives nothing.
- **The 08-22 blocker was gone.** That day the port-9223 profile had no OpenAI
  session and bounced to `/login`; it has one now, so OpenAI needed no human
  step. Anthropic did - one login by Alex, and that is the whole ongoing cost of
  Tier 3 for both.
- **Anthropic's extractor anchors backwards.** "Credit balance" is a heading
  followed by a two-sentence blurb, so the number sits ~150 chars downstream;
  it is pinned instead by the label that *trails* it (`$16.08 / Remaining
  balance`), sidebar `Credits $NN` as fallback. First cut also read the spend
  limit as $9.85, because the blurb "Set a monthly spend limit..." matched
  case-insensitively and pulled `$9.85 spent` into the window - now anchored on
  the label as its own line. Both pages also print decoy dollars (OpenAI's
  auto-reload copy; Anthropic's $100 limit, $9.85 MTD, $50 historical grants),
  so neither may scan for the largest `$`.
- **`auto_reload` is captured for both.** "$4 with auto-reload ON" and "$4 with
  it OFF" are different alerts. Both are OFF, which is why these keys can
  actually reach zero.
- **`marlow notify` hardened.** The alert reached Telegram as "OpenAI now
  /bin/zsh.40" - the tick shelled out with a double-quoted `"$0.40"` and zsh
  expanded `$0`. The sanctioned path (the tick result file) is JSON and was
  never at risk; the tick just didn't use it. Since the text is destroyed before
  Python sees it, added `--stdin` (heredoc-safe) and a guard that spots
  shell-path debris in an outgoing message and warns loudly while still sending,
  because a mangled urgent beats a dropped one.

*An open question closed.* Anthropic's baseline, 85 days old and flagged on
08-22 as "only right if that key has not been topped up since May," was honest:
derived $16.24 vs an actual $16.08. It had not been topped up. It was one
payment away from OpenAI's failure, not already in it.

*The pattern, fourth instance.* GLM's placeholder zero (06-11), Mistral's
re-layout (07-28), Qwen's label-vs-switch (08-12), and now this. Every time, a
plausible wrong value beat a loud failure to the alarm. The difference here is
that the fragile tier was *known* fragile and documented as such on 08-22, and
the incident still repeated, because what shipped was a warning label rather
than a removal. Tier 2 is now dormant with a note on it explaining why anyone
opting a provider back in should read this first.

*State at end of day.* All 11 providers read live, nothing derived: 8 prepaid
keys total **$113.26** (sakana $3.54 low, deepseek $9.63 low, glm $10.48, xai
$14.22, moonshot $15.78, anthropic $16.08, openai $19.57, minimax $23.96), plus
gemini $18.64/$2000 and mistral $8.37/$30 postpaid, and qwen's free grant fully
exhausted (3/3 models, billing pay-as-you-go). No urgents. Simona.
