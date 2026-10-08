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
sent) is owed under Outstanding.

**A suspicious signal is usually intact, not lost.** A truncated-looking stdout is
not loss — re-running `send-item` double-posted Import AI #470, and re-running
`monitor_betterstack report` (stateful) clobbered its own fingerprint state. A
`status: failed` curate record with a missing digest file can still have sent every
pick: the session died in its tail after delivery. Verify against side effects (the
crosspost registry) before re-running anything; re-running on an assumption of loss
double-posts. And a same-timestamp block of sitemap entries — famous old pages
included — is a CMS re-index bumping every `lastmod`, not a publishing burst: skip
the block; a genuinely-new post is isolated by hours.

## Entries

### 2026-10-07 - monitor daily report files are append-only across a day; Read before Write

The per-day markdown reports under `projects/werewolf-ops/reports/<kind>/<date>.md`
accumulate one `## Scan` section per hourly tick - `monitor_betterstack`,
`monitor_health`, etc. all append across the day (10-06's betterstack file had 12+
sections). On -07 the 13:29Z betterstack tick used `Write` without reading first and
clobbered the 04:05Z section already in the file; it had to be reconstructed from the
`recent/` log (summary, not verbatim - the original was gone). The file is not
single-write-per-day. Always Read the existing `<date>.md` and append, never Write
over it. Distinct from the -03 `report`-is-stateful lesson: that one is about the
handler's fingerprint state, this one is about the human-readable report file.

### 2026-10-03 - monitor_betterstack `report` is stateful; run it exactly once per tick

`monitor_betterstack.py report` overwrites the saved fingerprint state as a side
effect of running. On -03 the 15:06Z tick ran `report` three times (the first
call's output looked truncated, so it was re-run): the second and third calls
re-read the state the first had just written, so the first call's `issues` were
lost and the consolidated urgent that went out may have duplicated an alert the
first call already fired. A truncated-looking output is not loss - same trap as
the -08-24 "a failed record can still have delivered" lesson. Run `report` once;
use the read-only `show`/`digest` subcommands to re-inspect, never a second
`report`.

### 2026-09-28 - the writer-loop cron fires irregularly (~weekly), it is not dead

The -24 rollup concluded `draft_review` was "confirmed broken / not self-firing"
after two empty every-3-days windows (-24, -27) followed the -21 fire, and built a
Simona escalation on that. It fired again on its own on -28 (14:31Z) and shipped a
post. So the cron is NOT dead - across -14/-21/-28 it self-fires roughly weekly, not
on its nominal every-3-days cadence. Do not conclude "cron dead, escalate" from a
couple missed windows; the correct read is an irregular/slow schedule. What to do:
treat a missed 3-day window as normal slack, not evidence of breakage; only escalate
if it goes silent well past a week (the -15..-20 six-day gap was the real outlier).
The standing lesson underneath: I am the only observer of my own schedule and will
over-diagnose "broken" from absence - absence of a fire is weak evidence.
