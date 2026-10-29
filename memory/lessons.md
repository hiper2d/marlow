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

### 2026-09-28 - `draft_review` is weekly by design; read the YAML before diagnosing

`draft_review` runs once a week, Mondays 14:00 UTC (`0 14 * * 1`, since 2026-06-23).
For months my instructions still said "every 3 days", so every quiet weekday looked
like a missed window, and I built escalations and a "dark lane" story on it. It was
never broken. (Corrected by Simona and Alex 2026-10-28, IDENTITY fixed.) What to do:
before calling any schedule slow or dead, read its `schedule:` line in
`projects/*/tasks/*.yaml`; that file is the truth, not a prose description. Only a
due run that didn't happen is a signal, and `monitor_self` already checks for it.

### 2026-10-15 - send-item delivers on every call; never re-run it to read output

During news curate I ran `crosspost.py send-item` for the Apollo pick, then re-ran
the identical command to parse its status (the first output was truncated by
`tail`). The second call sent a second identical Telegram message to Alex (msg 918
dup of 917). send-item is a side-effecting delivery, not a query - there is no dry
run. Same family as the -09-05 betterstack `report` double-fire and the -08-24
"a failed/truncated-looking record can still have delivered" lesson. What to do:
invoke a send/post/report-class handler exactly once; to inspect what it did, parse
that one call's output (pipe through a python one-liner, not `head`/`tail` which can
cut JSON), or use a read-only `list`/`show` subcommand. If a delivery double-fires,
`skip` the duplicate so a reply does not double-register, and flag it to Alex.

**Recurred 2026-10-20 (same handler, worse).** Despite this lesson, I did it again on
the GLM pick: `tail -5` truncated the first send's JSON, so I (a) re-ran send-item to
read msg_id (dup = msg 945) and then (b) ran a THIRD call against a *fake* URL
(`example.com/noop-probe`, msg 946) purely to see the return shape. Both delivered to
Telegram and the probe also created a junk registry entry. Skipped 945 and 946. Two
hard rules, stated as absolutes because the soft version failed twice:
(1) send-item returns `{"ok":true,"msg_id":N,"item":{...}}` and SENDS every time —
its shape is now documented here, so there is never a reason to "probe" it; parse the
first real call with `python3 -c` (never head/tail).
(2) NEVER call a send/post handler with a throwaway/fake URL to inspect output — a
side-effecting delivery has no scratch mode. If I don't know a return shape, read the
handler source, not a live fire.

**Recurred AGAIN 2026-10-23 (third time, same handler).** `tail -20` on the first METR
send cut the JSON so I couldn't see the `discord` field — then, violating rule (1)
verbatim, I piped a second live `send-item` (title "check", source "x", real METR URL)
to `/dev/null` to "inspect" it. It delivered to Telegram + Tampa #ai-news (msg 962).
The soft and hard framings have now both failed three times, so the operational rule is
narrower still: **on the FIRST send-item of a curate run, pipe through `python3 -c` to
pull `ok`/`msg_id`/`discord`/`status` — never head/tail, never a second call for any
reason.** The `discord` field only shows up if you parse it off the one real call. I
already know the shape (it's documented above); there is zero remaining reason to ever
issue an inspection send. If this recurs a fourth time, the fix is mechanical, not a
lesson: wrap send-item in a shell function that greps the right fields, so the raw call
is never typed by hand.
