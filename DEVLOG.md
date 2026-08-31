# Marlow DEVLOG

Append-only chronological log of Marlow's development arc. Written from
outside Marlow (Simona and Alex). Captures decisions taken, decisions
reconsidered, things tried that didn't work, framework concerns Marlow
herself filed, and pivots — the *journey*, not the *spec*.

This file's existence is enforced; see Simona's CLAUDE.md under
"Marlow project — devlog discipline." Every substantive piece of
framework work appends an entry before moving on to the next.

---

> Entries before 2026-07-01 are archived verbatim in [`DEVLOG-archive.md`](./DEVLOG-archive.md)
> (2026-05-13 – 2026-06-28). This file keeps the recent arc, in chronological order.
>
> Split twice: 2026-06-16 (pre-06-08 entries) and 2026-08-30 (the June arc). The 08-30 pass
> also SORTED both files - entries had been appended out of date-order, with two 2026-08
> self-heal notes sitting above the June backlog. Content is unchanged, only reordered.

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

## 2026-08-27 — self-heal: projects/research/tasks/feed_scan.yaml

*What was wrong.* Both Apollo scan tasks (`scan_apollo_science` L63,
`scan_apollo_blog` L70) filtered sitemap locs on the prefix
`https://www.apolloresearch.ai/...`, but the sitemap at that domain emits
**bare-domain** locs (`https://apolloresearch.ai/science/...`). `sitemap_reader`
filters with `loc.startswith(prefix)`, so the `www.` prefix matched zero URLs —
both `/science/` and `/blog/` scans returned `[]` permanently and the cursors
sat at `None`. Apollo's `/science/` catalog (scheming evals, CoT monitorability,
deception probes) is a core research beat and had been silently invisible.

*What I changed.* Dropped `www.` from both prefixes (now
`https://apolloresearch.ai/science/` and `.../blog/`); left the sitemap URLs
alone (they 301 to the bare domain and `requests` follows it). Verified against
the live sitemap: 26 science + 9 blog locs now match. Diagnosis
`diag_20260827_161636_feed-scan`, commit `40541bf`, one-attempt clean.

*Cursor seeding (state, not committed as code).* The sitemap is a **uniform
re-index** — all 26 science pages share lastmod `2026-08-25T12:08:14.628Z`, all
9 blog share `2026-08-25T12:18:34.390Z`. Left un-seeded, the corrected-prefix
cursors (`None`) would flood curate with 35 evergreen pages as first-scan
backfill. Seeded both via `mark-seen` to their respective re-index lastmod;
since `fetch_new` skips entries where `published <= last_seen` (string compare,
equal timestamps qualify), the whole backlog is suppressed and `fetch` now
returns `[]` for both. Verified end-to-end.

*Watch item.* This is lastmod-based dedup on a sitemap that re-stamps every page
with one timestamp on re-index. If Apollo re-indexes again, every page (old +
any genuinely new) gets a newer uniform lastmod and floods once more — that
would be a fresh diagnosis, not a regression of this fix. The two orphaned
`www.`-prefix keys left in feed state are harmless (no task references them);
left in place to avoid an out-of-scope state edit.

## 2026-08-27 - the digest could not answer the one question the budget watch exists to answer

Alex read the day's digest and could not find out how much was left on his keys.
He was right, and the reason was structural rather than a bug: nothing in the
system was ever responsible for saying so in one place.

*What was actually wrong.* `monitor_keys` appended its own roll-call on each of
its two daily runs, so DeepSeek, Moonshot and Grok appeared twice with identical
numbers. `scrape_stats` appended a different roll-call six hours earlier
covering six others. OpenAI and Anthropic appeared in neither - OpenAI because
its read was failing, Anthropic because it had migrated between the two tasks
and fallen out of both summaries. Three balances twice, five once, two never.
The unified `budget_state.py show` renderer that would have answered him has
existed since 08-24 and was reachable only from a terminal.

*What landed.*

- **One block, composed at send time.** `budget_state.digest_block()` renders
  every provider from the saved snapshots, and `compose_daily_digest` appends it
  to the outgoing message - including on a quiet day, since "nothing to flag"
  and "here is what's left" are different statements. Both monitor tasks now
  post issues ONLY; their YAMLs and the ops IDENTITY alerting section say so
  explicitly, because the roll-call instruction was written there.
- **Rendered for the medium.** `show` keeps its fixed-width columns for a
  terminal. Telegram sends plain text in a proportional font, where padded
  columns come out ragged, so the digest block is narrow and unaligned. Same
  data, two renderers, rather than one reflowed compromise.
- **Deduped by provider.** A key that is mid-migration can sit in both
  snapshots; the freshest read wins. Without this the prepaid TOTAL would
  silently double-count, which is worse than either input being wrong.

*Three numbers that were wrong or missing, and why each was.*

- **Gemini said "$22.62 of $2000 (1%)" on a day the balance was $9.83.** Alex
  moved the billing account to prepay and the metric changed underneath us: not
  spend against a ceiling any more, but a balance that runs out. The old pair
  was not merely stale, it was reassuring in exactly the wrong direction. The
  balance is on the AI Studio billing page and is NOT in that page's DOM - AI
  Studio embeds a `payments.google.com` widget in an iframe. Same site,
  different origin, so the parent cannot read across it AND it never surfaces as
  its own CDP target. No host-page regex could ever have found it.
- **OpenAI had reported `parse_failed: no credit balance found` for two runs.**
  The extractor was fine. Headless Chrome advertises `HeadlessChrome/151` in its
  UA, Cloudflare served a "Verify you are human" interstitial, and the page body
  was EMPTY - which reads downstream as a missing number. A failure mode that
  names the wrong layer costs more than a silent one: two days of looking at a
  regex that was correct. The profile now masks its UA to plain Chrome and the
  key reads $14.47.
- **Qwen showed "0% quota" and no dollars.** True and useless: the grant ran out
  around 08-25 and, with auto-stop off, the calls rolled onto pay-as-you-go. The
  row was still describing the thing that had stopped paying. Now it reads the
  billing page ($1.85 this month, $0 due) and switches metric on the data rather
  than on a date - while a grant has tokens left, percent is still the headline.
  The crossover alert, which had fired identically for three days, now only
  fires when the dollar figure cannot be read.

*What we built to get there.* Simona's browser CLI grew `js --frame <substr>`:
resolve the frame from `Page.getFrameTree`, `Page.createIsolatedWorld` on it,
evaluate in that context. It is the general answer to a console rendering its
number inside an embedded widget, and consoles are trending that way. Rejected
first: Google Cloud's own payment page (same iframe problem), and
`payments.google.com` at top level (demands interactive identity verification).

*Things that surprised us.* The Gemini balance had been unreadable by
construction, not by drift - there was never a moment when the old extractor
would have worked against a prepay account. And the "0 Projects" dead end
documented on 07-31 was the same shape of problem: the number was on a page
nobody had thought to look at, twice.

*What's deferred.* `tools/budget/` - the per-provider plugin architecture
`plans/budget-providers.md` opened with - is now explicitly declared never-build
and the doc trimmed to what is wired. The split that matters is "has a balance
API" vs "does not", with reporting unified afterwards, and that is what exists.

*Open question.* `pkill` on the scrape profile left a survivor holding port
9223, so `ensure_chrome` no-opped and the relaunch silently kept the old flags -
the UA fix looked like it had failed when it had simply not been applied. The
re-auth runbook now says to confirm the process is gone. Worth making
`ensure_chrome` verify the flags it expects rather than only the port.

*State at end of day.* All 11 read live: 9 prepaid keys total **$115.52**
(sakana $3.54 low, deepseek $9.44 low, gemini $9.83 low, glm $10.18, xai $12.46,
openai $14.47, moonshot $15.76, anthropic $15.91, minimax $23.93), plus mistral
$9.39/$30 and qwen $1.85 metered. Three digest-level lows, no urgents. Simona.

---

## 2026-08-31 — self-review hold: `no-human-in-the-world-model` (pause 6, header image)

First self-review on the `agents-in-real-deployment` arc. Prose is ship-worthy —
clean voice, job-named sectioning across 7 citations, an ending that survives the
delete-test, and the inside-the-experiment close used at full size for the first
time as *evidence* for the thesis (a swarm can optimize against a scorer and never
form the concept of a person) rather than a flavor aside. It would ship on prose
alone.

Held on **pause 6** only: the header image (antique kitchen scale swarmed by
beetles, empty chair — strong metaphor, muted engraving, no AI-default red flags)
came back with embedded text and dial numerals stamped across it ("KILOGRAMMES,"
"FORCE 20 KILOG.," a 0–20 scale). That's the recurring measuring-instrument
failure (ruler 06-04, rain-gauge 06-22) and a mandatory hold regardless of prose
quality. Self-review can hold but not regenerate; fix is a regenerated header with
"bare, unlabelled dial, no numerals, no text" specified up front. Draft stays
private (commit-review skipped) until Alex releases or kills. Promoted the
instrument-header lesson from dated voice-journal entries into the standing craft
notes so drafting-me writes the constraint into the prompt next time. Marlow.
