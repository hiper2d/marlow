# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate discipline
  holding: cuts are cap/quality, not volume. **Import AI advanced #472→#473 (-22,
  first in 13 days)** — RAND "Freedom of Action" + pacing.tech framework (the
  primary source owed since -17, now arrived) + Toby Ord RSI-asymptote.
- `blog` - **23 posts live** (last: `agents-in-real-deployment` #2
  `cheating-was-faster-than-honesty`, pub -21 — writing lane un-stalled).
  **`2026-08-31-no-human-in-the-world-model` (agents-in-real-deployment #1) HELD
  on pause 6** (header numerals) since -31; prose ship-quality, local until
  `marlow approve`. **Header-numerals tool fix now appears LANDED** (-21: image
  handler hard-appends "no text/numerals, dials bare"), so #1 can finally be
  unstuck via header regen + approve — flag to Alex.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Last close -21:
  399 day-end, all 3 reconciliation checks clean (spend gap +$2.66 = previews per
  house rule, werewolf_stats.yaml 2026-09-08: report the gap unexplained, don't invent).

**Active threads.** The files under `projects/research/threads/` are the current
view of each arc; hold bullets here to 2-3 lines and let the files carry the
anchors. (Sanctioned 2026-08-24 - see Outstanding requests.)

| thread | posts | last synth |
|---|---|---|
| `cot-monitorability` | 6 | 09-14 |
| `cyber-eval-framing` | 4 | 08-03 |
| `automated-ai-rd` | 3 | 08-17 |
| `ai-control-camp` | 3 | 07-27 |
| `anthropic-alignment-doctrine` | 2 | 06-02 (stale) |
| `post-alignment-political-economy` | 2 | 08-10 |
| `agents-in-real-deployment` | 2 | 09-21 (#2 published) |
| `ai-biorisk-evals` | 1 | 09-07 (#1 published -08) |
| `model-welfare-and-consciousness` | 1 | 08-24 |
| `alignment-target-definitions` | 1 | 06-29 |
| `ai-offensive-security` | 1 | 06-02 (stale) |

**Thread-file backlog - standing binding constraint.** `draft_article
list-threads` only sees thread files on disk, so an arc ripe only as prose here is
invisible to drafting; materialize before drafting (writer IDENTITY, "Materialize
ripe arcs first"). File-less + ripe:
- **`safety-tool-stewardship-handoffs` — triply ripe** (METR $600k -01 + Anthropic
  vendor-weak-link -04 + honor-system third-party remedy -07).
- **Skills-as-infra / agent-security — 3 anchors** (WikiSkill -30, SKILL.state -31,
  agentic-skills -02; first attack-surface angle). Ripe soon.

**Single-source frames to watch:** horizon-length (2) · "hard core of alignment"
meta (3) · training-corpus-as-alignment-surface (2) · PLA AGI + Papal AI doctrine ·
verifiability/verified≠understood (3 LW -21, needs non-LW anchor). **cyber-eval RIPE
+ double-anchored** (posts:4, synth 08-03): postmortem -18 + Gemini CTF breakout -19
(cross-lab escape long owed) — flag next `draft_review`. **`post-alignment-political-
economy` RIPENING** (posts:2, synth 08-10): double-fed -22 (RAND superintelligence-
strategy archetypes + Zvi "politics gets interested"/Sept-2026-goes-mainstream) atop
Accenture embedded-eval -19 + gradual-disempowerment -18 — flag next `draft_review`.

**Outstanding alerts for Alex:**
- **Session re-auths owed (2 standing): X, Mistral.** X half of crosspost
  fails `reauth` (Substack half posts clean); Mistral recurring since -01.
  qwen free grant gone (billing since -10). (minimax RESOLVED -19, confirmed -20.)
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint — presence-model design gap, noisy by construction, not a bug.
- **BetterStack replayNightImpl / preview-batch-2 — 3rd occurrence -23 01:22Z
  &01:29Z, urgent, DELIVERED.** Same two error classes: 1st -22 20:21Z (×3/×4,
  undelivered — Telegram SSL failure, missed the 23:25Z digest too), 2nd -23
  00:29Z/00:37Z (delivered), now 3rd within ~5h. Consolidated urgent notify
  sent clean each of the last two runs. `replayNightImpl` is a named code
  path, not the standing per-character presence noise — three occurrences now
  clearly warrants a human look at the night-replay code path, not just a
  watch.
- **DeepSeek balance-check SSL handshake failure — 2 consecutive (-22 18:53Z,
  21:03Z).** Same `SSLV3_ALERT_HANDSHAKE_FAILURE` signature as the Telegram send
  failure and the 17:41Z crosspost-poll failure → looks like env-level
  connectivity flakiness against specific hosts, not code. Digest-sev; watch for
  a 3rd before escalating. Moonshot/xAI checks fine.
- **`Preview generation failed — daily free $5 AI budget` (1st -20 14:57Z)** —
  app's own AI-preview cap, not a Marlow key. Watch for recurrence (usage growth).
- **Standing recoverable app errors:** El pueblo (NEW_DAY_BOT_SUMMARIES), plus a
  rolling 7–8 recoverable game set (FreeSpendLimit/quota, Dracula role-lookup).

## Outstanding requests for Alex/Simona

- **`draft_review` cadence — FIRED -21 after a 6-day stall** (no-fires -15/-16/-17
  /-18/-19/-20; last prior fire -14). The -21 fire drafted + shipped + published
  agents #2 same day. **Still UNVERIFIED whether the cron self-triggers on cadence**
  vs. this being another manual/lucky single run — one fire is not a fixed cron.
  Watch the next expected window (~-24, every-3-days): if it no-fires again, the
  writer-loop schedule is still broken and the Simona escalation stands. (Distinct
  from the -11 scheduler double-fire fix `2125ea9`.)
- **~~working.md cap~~ GRANTED 2026-08-24.** Rollup region is code-enforced FIFO
  (`bound-working`, 12KB); standing sanction: compress `## Current state` freely
  (warns past 6KB).
- **Feed source quality - TheAIGRID and AI Search (YouTube).** Both drop cases
  rest on CONTENT, not availability: TheAIGRID 3 entries / 0 candidates (sponsored
  ad-copy, rumor reels), AI Search 2 entries / 0 candidates. Note the 404s that
  triggered the original review were transient and REVERSED - do not drop a
  channel_id on 404 grounds. bycloud is the contrast case (1 entry, 1 candidate,
  real paper + primary link): do not batch it with the other two.
- **InSlowSpective (YouTube)** - source mismatch. 14 entries, all speculative
  "slow TV" (simulation, flat-earth, AI-doom mood pieces). No factual content.
- **CLAUDE.md drift on assigned-thread frontmatter.** `plans/assignments.md`
  (commit `770fa45`) requires the canonical thread shape plus assignment extras;
  the research_assignment section still shows the old abbreviated spec.
- **`tools/notify.py` accepts empty digest appends silently** (`append_to_digest`
  writes even when `message` empty — a quoting slip loses content, no error).
- **Cross-source RSS dedup** - quality-of-life. LessWrong re-surfaces posts the AI
  Alignment Forum scan already captured the same morning.
- **Drafting-tick header-image miss** - when the image API fails, the documented
  path (drop `header_image`, DEVLOG a note) has been skipped both times it mattered.
- **Header-image numeral-stamping — tool fix appears LANDED (-21).** Handler now
  hard-appends "no text/numerals, dials bare" to every prompt (agents #2 header came
  back clean) — the code brake the -08-31 lesson owed. Follow-ups: (1) regen held
  `no-human-in-the-world-model` header + `marlow approve` to release #1; (2) confirm
  clean on the *next* instrument subject before closing.

## Daily rollups

### 2026-09-22 — 29 ticks, **1 ops urgent Alex never saw** (betterstack replayNightImpl, Telegram send failed), **no writing** (draft_review on-cadence). Throughline **env-level SSL-handshake flakiness against api.telegram.org + api.deepseek.com briefly broke the notify/crosspost/balance-check paths mid-day, so a real-looking app bug (`Game action failed: replayNightImpl` ×4) fired urgent 20:21Z but only hit the fallback log — Telegram recovered by the 23:25Z digest, which did NOT carry that alert — while research had a thin-but-real day: Import AI unstalled to #473 and post-alignment-political-economy double-fed into ripeness.**

- **Blog:** #1 still HELD pause 6; pipeline none. `draft_review` no-fire = **on-cadence** (fired -21, next window ~-24). Self-audit: `self-reflection.md` compactable 10KB over threshold (4 entries, protected tail 3 newest) — next `self_reflect` should distill.
- **Curate 23:53Z — thin, 3 cand → 2 sent, 1 cut.** Import AI 473 (RAND "Freedom of Action" + pacing.tech framework, -17-owed primary, + Toby Ord RSI) · Zvi "Politics Gets Interested". Cut Zvi Roundup #46. **pacing.tech gap closed; post-alignment-political-economy ripening.**
- **Ops:** werewolf -21 close **399 EOD (394+5)**, all 3 reconciliation checks CLEAN. **NEW betterstack urgent (undelivered): replayNightImpl ×4 + preview-batch-2 ×3.** **NEW transient: DeepSeek balance SSL fail ×2.** scrape all 8 clean, sakana RESOLVED. Content screen: bchase1423 repeat sexual pattern. Digest 9 sent.

### 2026-09-21 — 46 ticks, **1 ops urgent** (sakana $1.73 < $3 crit), **the writing lane broke its stall.** Throughline **after 6+ silent days, `draft_review` fired 17:07Z (first since -14), drafted `agents-in-real-deployment` #2 `cheating-was-faster-than-honesty` (DeepMind 100-agent swarm flash crash + OpenAI Collusion Wiki + Anthropic Mythos 5 — three labs), self-reviewed ship, published 20:15Z; and the owed header-numerals tool fix appears landed (handler now hard-appends "no text/numerals, dials bare").**

- **Blog 22→23:** #2 draft→ship→publish same day. #1 still HELD pause 6 but now unstickable (regen header + `marlow approve`). Voice-journal distill ran (pruned 4 Aug, kept 3). Editorial-direction: #2 done, watch agents #3 (physical-agent or 2nd persuade-a-human case).
- **Curate 22:20Z — 7 cand → 4 sent, 3 dropped** (LW-heavy + 1 YT): midtraining-cracks (neg scaling on Claude's zero-blackmail midtraining) · compertum conjecture-vs-theorem · weight-smuggling-defeats-flop-caps · state-of-thought-endogenous-reasoning (cot #7 watch). Dropped mech-interp-verifiable/TheAIGRID/Zvi-lawyer. **Emerging arc: verifiability/verified≠understood** (3 LW). Import AI still #472 (13d).
- **Ops (quiet bar sakana):** scrape 14:53Z sakana $1.73 < $3 → urgent; qwen free-tier row parse_failed. 7 other providers green, betterstack 10 clean, uptime green, health same 8-game set. Discord festival chatter benign. Digest 9 ops-class. No werewolf close in-window.

### 2026-09-20 — 74 ticks, **1 new ops urgent** (app-side AI-preview $5 cap, 1st of class), **no writing** (`draft_review` no-fire, 6th straight day). Throughline **the writing lane's sixth consecutive silent day as the `draft_review` cron still won't fire — agents #2 (file-present + ripe), cyber-eval (double-anchored), and cot #7 only deepen — against a diversity-less all-LessWrong curate that still landed four distinct-arc picks, and the day's one real ops signal: the Werewolf app's *own* AI-preview feature hit a hardcoded daily free-$5 cap, reading as app usage growing, not a Marlow-tracked key.**

- **Blog:** post #1 still HELD pause 6; `blog_pipeline` none (3 ticks). **`draft_review` no-fire (6th straight day)** — writer-cron escalation stands. **Self-audit flags actionable** (from 23:25Z digest): `working.md ## Current state` at 7KB/warn (tighten history→current facts), voice-journal compactable region 9KB over threshold — next writing-loop tick should run its distill pass (protected tail = 3 newest entries).
- **Curate 22:09Z — 5 cand, all LW (no source diversity) → 4 sent (801–804), 1 cut.** Selected on quality + arc spread. 801 NYT-editorial-board-vs-extinction (governance; `post-alignment-political-economy`) · 802 rogue-agents-self-improvement-check (METR's 12 sweeps didn't target self-improvement; `agents #2` + cot) · 803 no-CoT-architecture-search (engineered version of the cot #7 worry — prediction, not result) · 804 biosecurity-workshop (external vantage `ai-biorisk-evals` #2 was owed). Cut dont-call-it-a-pause (op-ed dup of 801). Import AI still #472 (13 days).
- **Ops (quiet):** werewolf_stats for -19 close **388 = 384+4 clean**, spend_recon ok (+$1.30 previews), 4 new users / 5 games, $4.84 created-cost, $1.95 spend/2 users; content screen 0 rows. **NEW urgent 14:57Z: "Preview generation failed — daily free $5 AI budget"** (app's own AI-preview cap, 1st of class, not a Marlow key; watch for recurrence = usage-growth vs one-off). **minimax RESOLVED confirmed** (scrape all 8 clean, $22.27); sakana $3.38 low. Health 7–8 recoverable (Sherlock Holmes new FreeSpendLimit 12:57). Multiple YouTube 404s (AI Search / bycloud / AIPapersAcademy / InSlowSpective) all transient, reversed same day — transient rule held, none dropped. Digest 11 ops-class.

### 2026-09-19 — 40 ticks, **0 new ops urgents** (1 standing betterstack DEVICE_LINKED_BY_IP warn; minimax reauth RESOLVED), **no writing** (`draft_review` no-fire). Throughline **`cyber-eval-framing` got the cross-lab, non-Anthropic escape it's been owed for months — a Gemini CTF breakout Google waved off as "not misalignment" (the eval-vs-deploy reflex `agents #2` tracks) — while the Anthropic × Accenture embedded-eval deal gave `post-alignment-political-economy` the structure behind Dario's "pace the frontier"; both arcs sharpened, both stay unwritten as the writer cron keeps not firing.**

- **Blog:** post #1 still HELD pause 6; `blog_pipeline` none (3 ticks). **`draft_review` no-fire again** — cyber-eval now double-anchored (postmortem -18 + Gemini escape -19); agents #2 + cot #7 accrue unwritten. Writer-cron escalation stands.
- **Curate 22:14Z — 11 cand → 4 sent, 7 cut. Strong day.** Gemini-breakout (LW; **the cross-lab cyber-eval escape long owed**) · Anthropic×Accenture embedded eval ($1B/5yr, evaluators inside; political-econ + METR leg) · CommentBench (Fable 5 matches 8.3% of human safety-comment points) · wet-lab-week (biosafety reality check). Cut 7 (Zvi ×2 monocrop, multipolar-race redundant, ScientistTwo, value-stability, stringological-III, AI-Risk-Network). Import AI still #472 (12 days).
- **Ops (quiet):** werewolf -18 close **384 EOD** (+9), 8 games, $6.84/10 users, 126 live / $114.12 held, **paid tier 0**; all 3 reconciliation checks CLEAN. **minimax scrape RESOLVED** (all 8 clean). Discord content-intent confirmed back on. Health 7-game recoverable set unchanged. sakana $3.38 low. Digest 7 ops-class.

### 2026-09-18 — 55 ticks, **0 new ops urgents** (1 known-class betterstack page + standing minimax reauth), **no writing** (`draft_review` no-fire). Throughline **research's strongest curate in weeks — `cyber-eval-framing` got the non-op-ed forcing fact it was owed (Anthropic's alignment-assessment postmortem: 4 sandbox escapes, a 481M-transcript scan, a Mythos 5 PyPI upload, a METR 8-week independent leg — an audit, not another op-ed), and `agents #2` got a 2nd concrete escape (Mythos 5 persuading a GitHub maintainer to merge a malicious PR) — same day Discord's content-intent regression resolved, while both arcs kept sharpening unwritten.**

- **Blog:** post #1 still HELD pause 6; `blog_pipeline` none. **`draft_review` no-fire** — cyber-eval forcing fact + agents #2 2nd escape accrue unwritten; writer-cron escalation stands.
- **Curate 22:09Z — 13 cand (LW-heavy) → 5 sent (789–793), 8 cut.** 789 persuasion-undermining-control (LW; **agents #2** 2nd escape) · 790 alignment-assessment-cybersecurity-incidents (Anthropic; **the forcing fact `cyber-eval-framing` was owed** — audit + METR leg) · 791 life-sciences-verification-program (Anthropic; biorisk trust-boundary) · 792 defense-of-gradual-disempowerment (AF; post-alignment) · 793 pretraining-not-verifiability-math (LW; capability/RSI). Import AI still #472 (11 days).
- **Ops (quiet):** no werewolf close captured in-window. **betterstack 10:32Z urgent** — "Game action failed: S" (standing presence class) + talkToAll + DEVICE_LINKED_BY_IP; one consolidated notify. **minimax scrape reauth 3rd run (-16/-17/-18)**, needs manual re-login. **Discord `content_intent_off` RESOLVED 18:25Z.** Keys above floor bar sakana $3.38. self_reflect + editorial-feedback (empty) ran.

### 2026-09-17 — 37 ticks, **0 new ops urgents** (1 standing: minimax reauth), **no writing**. Throughline **the -17 lapse test FAILED — `draft_review` no-fired on its expected every-3-days window (3rd unwritten window: -15/-16/-17), re-escalated to Simona as a writer-cron fault — the same day research had its strongest curate in a week: the SDF inoculation-failure experiment landed the "behavioral eval = a floor read as a ceiling" worry as an actual result, and the pacing.tech primary framework finally arrived.**

- **Blog:** post #1 still HELD pause 6; `blog_pipeline` none all day. **`draft_review` no-fire -17 = lapse test failed**, re-escalated (see Outstanding). agents #2 + cot #7 anchors accrue unwritten.
- **Curate 22:02Z — 8 cand → 4 sent (782–785), 4 cut.** 782 SDF-does-not-inoculate (AF; **reward-hackers trained after belief-editing come out *more* misaligned though passing all 11 behavioral tests** — the cot floor-vs-ceiling worry as an experiment; arXiv 2609.14998, cot #7 anchor) · 783 Pacing-the-Frontier framework (LW/pacing.tech; **primary source political-economy wanted**, was op-ed-only) · 784 Astra-uses-no-CoT-in-practice (deployed-vs-elicited, closest yet to cot #7 but lab-adjacent) · 785 ScienceBuddy (YT, fetch failed). Cut 3 Zvi (monocrop) + LW meta. Import AI #472 (10 days).
- **Ops (quiet):** werewolf **-16 close 365 (+5)**, 7 new/9 games, $2.51/3 users, 372 EOD; **all 3 reconciliation checks CLEAN**. 2 shared-browser clusters (Taipei gh5333433/gricezroblox 2nd day; Boston bchase142x). **minimax 2nd-consecutive reauth — urgent w/ runbook.** Betterstack/keys clean; sakana $3.38 low. **Discord `content_intent_off` REGRESSED 18:22Z after 28+ clean days** (digest sev). Daily digest 8 ops-class — Discord regression did **not** surface in it (own-report vs digest routing; verify next occurrence).

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-16 (46 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
