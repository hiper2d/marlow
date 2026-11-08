# Lessons

**Long-term memory.** Read at the start of every tick alongside `working.md`.

This is the only file in the system that is meant to outlive the working
window. `working.md` is a fixed-size FIFO: daily rollups drop off the end after
roughly a week and are gone from your context for good. Most of what falls off
*should* fall off. Nobody needs to know what happened on a Tuesday in July.

Some of it should not. When a tick teaches you something that will still be
true in six months - a failure signature, a workaround, a thing that looks
broken but isn't - it belongs here, not in a rollup that will expire.

This file replaces the `memory/archive/` weekly-synthesis layer, which was
described in the contract for months and never built. A weekly digest of a
daily digest is a third copy of the same information that nobody reads. This is
different: it is not a time series at all, it is a small set of durable facts.

## The bar

High, deliberately. Most days add nothing, and a day that adds nothing is the
normal case - do not manufacture an entry to have written one. An entry earns
its place if:

- It cost something to learn. A failure that took two incidents to diagnose, a
  handler that lies about its own success, a signal you misread once already.
- It will still be true in six months. Not "the pipeline is empty this week."
- It changes what a future tick would *do*. If knowing it wouldn't change an
  action, it is an observation, not a lesson.

Things that are NOT lessons: what you published, what the feed contained, how
many ticks ran, anything already captured by a rollup or a thread file.

## Form

Newest first under `## Entries`. One `### YYYY-MM-DD - <short name>` heading,
then two or three sentences: what happened, what it means, what to do next time.
Name the file or handler if there is one. Terse is correct.

## Bounding

Same protected-tail contract as the journals. The three newest entries are
never touched. Older entries fold into `## Standing lessons` once the older
region passes 6KB, and that standing section is re-synthesized only rarely
(past 12KB) so it does not get paraphrased into mush. `grade_memory
lessons-status` hands you the pre-split view.

## Standing lessons

_Distilled from older dated entries (2026-08 .. 2026-09); originals in git history._

**Brakes that live only in judgment don't hold — put the bound in code.** A cap
written in a prompt drifts: `working.md`'s "~10KB cap" reached 149KB over two
months because the Opus grader re-decided nightly that tonight wasn't the night
(now enforced by `grade_memory bound-working`). A "watch for X" self-note is not
a control either — the header-image generator stamped legible instrument numerals
a 3rd time despite a voice-journal flag telling me to watch for it; the fix had to
be hard-coded in the prompt/handler and owed to the tool owner, not another
note-to-self. Anything you're tempted to enforce with a sentence, ask whether it
can be a function.

**An escalation nobody reads isn't an escalation.** The 149KB `working.md` fix
needed sanction the contract didn't grant; the proposal sat under Outstanding
requests for weeks, restated every rollup, because nothing was built to read it
back. When something is out of scope, file the request AND say it out loud in the
tick result or a digest line — a `working.md` bullet alone reaches nobody.

**Curate has no cross-day dedup — the sent registry is the only truth.**
`send-item` never marks a candidate sent and has no URL dedup, so the same item
reaches Alex twice through three distinct paths: (a) a late catch-up curate plus
the normal same-day curate both sweeping the same prior-day orphans (-27); (b)
candidates dated yesterday being invisible to `list --date today` (-24); (c) a
feed re-surfacing a weeks-old URL picked fresh because the candidate note looks
new (-10-08 enzyme, a dup of the 09-24 send). Until the handler dedups against the
registry, the brake is manual: before sending a pick, suspect re-surfaces and
check `recent/` + the crosspost registry for the URL. Root fix (mark candidates
sent) is owed under Outstanding. **The same no-send-dedup weakness is not curate-
specific: `compose_daily_digest` double-delivers too** (-11-03: fired 20:36Z and
again 23:02Z, both sent the ~15-entry digest to Alex). Any daily one-shot delivery
handler re-sends in full on a scheduler double-fire; a digest/curate tick firing
within a few hours of another should check `recent/` for a same-day prior send and
no-op rather than re-deliver.

**A suspicious signal is usually intact, not lost.** A truncated-looking stdout is
not loss — re-running `send-item` double-posted Import AI #470, and re-running
`monitor_betterstack report` (stateful) clobbered its own fingerprint state. A
`status: failed` curate record with a missing digest file can still have sent every
pick: the session died in its tail after delivery. Verify against side effects (the
crosspost registry) before re-running anything; re-running on an assumption of loss
double-posts. And a same-timestamp block of sitemap entries — famous old pages
included — is a CMS re-index bumping every `lastmod`, not a publishing burst: skip
the block; a genuinely-new post is isolated by hours.

**Side-effecting handlers run exactly once per tick — the re-run is the single
most-repeated mistake in this log.** `send-item` SENDS on every call and
double-posted to Alex three times (-10-15 / -20 / -23) because a truncated-looking
`tail` tempted a second "inspection" call; its shape is
`{"ok":true,"msg_id":N,"discord":{...},"item":{...}}` — parse the one real call with
`python3 -c`, never head/tail, never a probe or fake-URL call. `monitor_betterstack
report` overwrites its own fingerprint state on success, so a second `report`
re-reads what the first wrote and loses its issues (-10-03) — re-inspect with the
read-only `show`/`digest` subcommands. The per-day files under
`reports/<kind>/<date>.md` are append-only across the day: Read and append, never
Write-over (-10-07 clobbered a section). The one exception: a `report` that returns
`ok:false` failed *before* its save (state is written only on the success path), so
that retry is correct, not a clobber (-10-30) — re-run only after `ok:false`, never
after `ok:true`.

**A single scan is not an event, and the task YAML is the schedule's only truth.**
`monitor_models` reported a current Mistral flagship as `removed` then `new` within
two hours (-10-29) — provider `/models` lists flap, so confirm a `removed` id the
game actually uses stays gone across the *next* scan before firing any deprecation
alert. And `draft_review` is weekly by design (Mondays 14:00 UTC); for months a
stale "every 3 days" prose note made every quiet weekday look like a missed window
and spawned false escalations. Before calling any schedule slow or dead, read its
`schedule:` line in `projects/*/tasks/*.yaml` — only a due run that didn't happen is
a signal, and `monitor_self` already checks for that.

## Entries

### 2026-11-06 - scrape_stats balance-read failures self-heal; don't fix the selector on a transient

Two standing `scrape_stats` blinds both cleared on their own on -11-06 with no logged
intervention: the MiniMax `parse_failed: no credit balance found` ran 9 consecutive
failed scans (-10-30 → -05, urgent-notified -11-02) and the Anthropic console reauth
login-wall was open ~1 day (-11-05 10:43Z); the 15:39Z -11-06 scan read both clean
($18.79, $10.15). The failure mode is a transient session / anti-bot / login-wall
state at the provider, not a broken selector — `scrape_stats.py:325`'s `Effective
balance` selector never needed a fix. What to do: when a balance read returns
`parse_failed` or hits a login wall, let the notify-spam guard hold it to one urgent
and wait it out across scans; do NOT file a framework_fix diagnosis against the
scrape selector until a failure persists well past a day AND other providers on the
same handler read clean (which isolates it to that provider's page, not the parser).

### 2026-11-03 - betterstack: "OpenAI Decisions ... (shadow)" is a recorded-only lane; never game-impacting

The judge router (`werewolf-client/app/api/jev-router.ts`) decides with Jev (typesafe.ai) as primary
and runs OpenAI Decisions (gpt-6-luna) in parallel purely as a **shadow** — billed and logged, never
acted on; it gets its own 3s budget. A log line `OpenAI Decisions screen request failed (shadow)` /
`OpenAI Decisions request timed out after 3002 ms` (seen 06:13Z, warn, class `timeout`, target `app`,
no gameId) is therefore non-blocking by construction — the repo test says "a Decisions failure alone
changes nothing in the game: Jev decides, the shadow records the error." Do NOT conflate a shadow
Decisions failure with the real Decisions router/screen or with an OpenAI provider_budget event
(working.md flags OpenAI as the app's volatile dependency, which invites exactly that misread). It is
never urgent and needs nothing; only a *sustained* run of shadow timeouts is a cost/latency note for
Alex (gpt-6-luna overrunning its 3s budget), not a reliability issue. The `(shadow)` suffix in the msg
is the tell.

### 2026-11-02 - a second draft_review in the same weekly cycle is a no-op, not a second piece

`draft_review` fired twice today: an early 02:10Z tick drafted the week's piece
(`the-veto-nobody-used`, published #29 at 18:13Z), then the nominal-slot subtask
(`review_and_draft_20261102_1416`, queued 14:16Z) fired again at 20:11Z handing me another
`draft_article`. The naive action — "handed a draft subtask, so draft" — would produce a
second publication in one week and break the one-draft-per-cycle / ≤1-publication/week cap
(and published pieces are locked, so it can't be undone after). This is the inverse of the
-09-28 lesson: that one says a quiet weekday isn't a missed slot; this one says a slot that
already shipped its piece isn't an open slot. Before drafting on any `draft_review`, check
whether this week's piece already exists (drafts/ non-empty OR a `published/<thisweek>.md`
present) — if it shipped, no-op clean, no notify. Verify by publication date, not by the
subtask looking fresh.
