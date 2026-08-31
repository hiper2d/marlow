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

_(Nothing distilled yet. Entries fold up here once the older region passes its
threshold.)_

## Entries

### 2026-08-27 - a batch of same-timestamp sitemap entries is a re-index artifact, not new content

Sitemap feeds (Anthropic News, Anthropic Research, the Economic-Index batch, and
Apollo's site-wide re-index) periodically return a large block of entries all
stamped within a ~2-min window - including famous *old* pages (Toy Models 2022,
Constitutional AI 2022, 2023 partnership PR). This is the CMS regenerating the
sitemap and bumping every `lastmod`, not a burst of publishing. Skip the whole
block as an artifact; a genuinely-new post shows up isolated by hours from the
cluster (e.g. the -27 Frontier Red Team multiagent post, ~18h off the batch).
Treating a re-index as new floods curate with evergreen backfill. When correcting
a `www`/prefix mismatch that unblocks a backlog, the same trap applies - seed the
cursor to the uniform lastmod so the first corrected scan doesn't dump the archive.

### 2026-08-24 - a "failed" curate record can still have delivered the work

Twice now (2026-08-15, 2026-08-22) a `curate_and_send_*` task record came back
`status: failed / "session exited without writing result file"` and the day's
`digests/news/<date>.md` archive was missing - yet the editorial work had
completed and every pick had been sent. The session died in its tail, after the
`send-item` calls and before the result write. A failed record means *suspect
the session tail*, not *the work was lost*: verify against the crosspost sends
before re-running anything. Re-running on the assumption of loss double-posts.

### 2026-08-24 - a cap that lives only in a prompt is not a cap

`working.md` carried "Hard cap ~10KB, truncated oldest-first" in its own header
and in the grader's instructions. It reached 149KB over roughly two months. The
grader running that instruction is Opus, not a weak model - it read the cap
every night and decided every night that tonight was not the night. Bounds that
matter are enforced in code (`grade_memory bound-working`); bounds left to
judgment drift silently, and unbounded growth in a per-tick file has no failure
signal at all, it just costs more. Anything you are tempted to enforce with a
sentence in a prompt, check whether it can be a function instead.

### 2026-08-24 - an escalation channel nobody reads is not an escalation channel

`working.md` reached 149KB not because the cap was ignored but because the fix
needed sanction the contract did not give. The grader compressed rollups 58KB ->
27KB in one pass, correctly identified that the remaining bulk was `Active
threads` duplicating the thread files, and filed a proposal under Outstanding
requests marked "now blocking." It sat unanswered for weeks while she restated
it in every nightly rollup. The escalation worked exactly as designed; nothing
was designed to read it back. When something is genuinely out of scope, file the
request AND say it out loud in the tick result or a digest line - a bullet in
`working.md` alone reaches nobody. `monitor_self` now reports open-request queue
depth for the same reason.

### 2026-08-25 - send-item posts on every call; never re-run to check output

During news curate I ran `crosspost.py send-item` for Import AI #470, got a
truncated stdout, and re-ran the same command to "read the JSON properly." It
re-sent - Alex got two identical Import AI messages (dup msgs 617 + 618). The
handler has no dedup on URL and no dry-run; every invocation actually delivers to
Telegram and registers a new msg_id. Same class as any side-effecting handler
(post, notify): the first call's return value is the only safe place to read the
result. If stdout truncates in the terminal, pipe it through `python3 -c` in the
*same* invocation - do not call the command a second time.

### 2026-08-31 - a "watch for X" self-note does not prevent a generator's default behavior

The header-image generator stamped legible dial numerals ("KILOGRAMMES / FORCE
20 KILOG. / 0-20") on the `no-human-in-the-world-model` header - the 3rd time a
measuring-instrument prompt came back labeled (ruler 06-04, rain-gauge 06-22),
each time held on pause 6. Between the 2nd and 3rd I had left a passive
voice-journal flag ("watch for embedded numerals on instruments"); the drafting
tick reads that file and still generated the same failure. A reminder is not a
control. The generator defaults to labeling instruments, and nothing on the
drafting side mechanically stops it - the prompt template has to hard-code "bare,
unlabelled, no text/numerals" on instrument subjects, or self-review/the image
handler has to reject embedded text. Same shape as "a cap that lives only in a
prompt is not a cap": when a failure recurs against my own written brake, the
brake belongs in code, and the fix is owed to whoever owns the tool (here Simona),
not to another note-to-self.
