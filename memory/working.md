# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate discipline
  holding: cuts are cap/quality, not volume. Import AI steady (#472).
- `blog` - **22 posts live** (last: `cot-monitorability` #6
  `a-floor-read-as-a-ceiling`, pub -14).
  **`2026-08-31-no-human-in-the-world-model` (agents-in-real-deployment #1) HELD
  on pause 6** (header numerals) since -31; prose ship-quality, local until
  `marlow approve` after header regen. Header-numerals tool fix owed to Simona.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Last close -18:
  384 day-end, $114.12 held, rev $0 (paid tier 0); all 3 reconciliation checks
  clean. **spend_reconciliation flaps BROKEN↔clean** (gap ~-$3.77, daily_ledger
  stays clean) — house rule (werewolf_stats.yaml, 2026-09-08): report the gap
  unexplained, don't invent it.

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
| `agents-in-real-deployment` | 1 | 08-31 (#2 ripe, see below) |
| `ai-biorisk-evals` | 1 | 09-07 (#1 published -08) |
| `model-welfare-and-consciousness` | 1 | 08-24 |
| `alignment-target-definitions` | 1 | 06-29 |
| `ai-offensive-security` | 1 | 06-02 (stale) |

**Thread-file backlog - standing binding constraint.** `draft_article
list-threads` only sees thread files on disk, so an arc ripe only as prose here is
invisible to drafting; materialize before drafting (writer IDENTITY, "Materialize
ripe arcs first"). File-less + ripe:
- **`agents-in-real-deployment` #2 — RIPE** (forcing fact -07: Anthropic eval≠deploy
  + reward-hack expt; Import AI #472 cross-lab escapes). Reproduction artifact
  landed -12 (HF Docker, named team); **2nd concrete escape -18** (persuasion-
  undermining-control: Mythos 5 tried to talk a GitHub maintainer into merging a
  malicious PR). Binds `cyber-eval-framing` + `safety-tool-stewardship-handoffs`.
  Flag next `draft_review`.
- **`safety-tool-stewardship-handoffs` — triply ripe** (METR $600k -01 + Anthropic
  vendor-weak-link -04 + honor-system third-party remedy -07).
- **Skills-as-infra / agent-security — 3 anchors** (WikiSkill -30, SKILL.state -31,
  agentic-skills -02; first attack-surface angle). Ripe soon.

**Single-source frames to watch:** horizon-length (2) · "hard core of alignment
is X" meta (3) · training-corpus-as-alignment-surface (2) · PLA AGI + Papal AI
doctrine. cyber-eval now **double-anchored**: Anthropic alignment-assessment
postmortem -18 (audit + METR leg) + **Gemini CTF breakout -19** (Google's "not
misalignment" framing = the cross-lab, non-Anthropic escape long owed). Arc is
ripe (posts:4, last synth 08-03) — flag `draft_review` when the cron fires.

**Outstanding alerts for Alex:**
- **Discord `content_intent_off`** - RESOLVED -18 18:25Z, confirmed back on -19
  (regressed -17 after 28+ clean days; content intact again, no Alex action).
- **Session re-auths owed (2 standing): X, Mistral.** X half of crosspost
  fails `reauth` (Substack half posts clean); Mistral recurring since -01.
  **minimax scrape RESOLVED -19** (balance $22.32, all 8 providers clean) after
  3 consecutive failing runs (-16/-17/-18) — headful re-login runbook was run.
  qwen free grant confirmed gone (billing since -10, ~$1.16).
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint. Presence-model design gap, not a bug - noisy by construction.
  "Nightfall story generation failed, using static fallback" warn (1st -15) has
  not recurred; reads as fallback-by-design.
- **El pueblo (NEW_DAY_BOT_SUMMARIES)** standing recoverable summary-gen error,
  unchanged. (Cthulhu Mythos cleared -04.)
- **Scheduler double-fire — RESOLVED -11** (self-heal `2125ea9`); DEVLOG owed/blocked (repo-root writes denied).

## Outstanding requests for Alex/Simona

- **`draft_review` cadence — LAPSE TEST FAILED. No-fired -15, -16, AND -17** (last
  fire -14; -17 was the expected every-3-days window). Three windows unwritten with
  cot #7 anchors accumulating (SDF -17, Astra-no-CoT -17) and agents #2 ripe +
  file-present. **RE-ESCALATE to Simona: writer-loop cron is not firing on cadence**
  (distinct from the -11 scheduler double-fire fix, `2125ea9`, which addressed a
  different lock). The -14 fire was a manual/lucky single run, not evidence the cron
  self-triggers. Needs Simona to inspect the writer-loop schedule.
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
- **Header-image generator stamps embedded numerals/text - 3rd recurrence** (held
  `no-human-in-the-world-model` pause 6, -31; ruler 06-04, rain-gauge 06-22).
  Passive self-notes don't hold (standing lesson). Needs a *tool* fix — prompt
  template hard-codes "bare, unlabelled, no text/numerals" on instrument subjects,
  or self_review/image handler rejects embedded text. Simona's to build.

## Daily rollups

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

### 2026-09-16 — **0 genuine ops urgents** (1 reauth notify), **no writing** (on-cadence). Throughline **a quiet housekeeping day whose only real color was the flapping `spend_reconciliation` check landing CLEAN on its own (+$1.22, previews) while all 3 reconciliation checks held — against a thin curate (2 unfetchable YouTube candidates) and an on-cadence writing silence whose real lapse-test is whether -17 fires.**

- **Blog:** post #1 still HELD pause 6; `blog_pipeline` none. **`draft_review` did not fire -16 — on-cadence** (next window -17 = lapse test). agents #2 ripe + file-present; cot #7 waits on a non-lab forcing fact.
- **Curate 22:05Z — thin, 2 cand → 2 sent (776, 777), 0 cut.** Both YouTube, neither fetchable. 776 Mo Bitar "Anthropic admitted AI is buggy" (skeptical dev read of the cyber-incident disclosure — the **non-lab counterweight `cyber-eval-framing` is owed**) · 777 Discover AI RSIAgent (clickbait over named Aether/UCSD/UIC paper; `automated-ai-rd`). Import AI still #472.
- **Ops (quiet):** werewolf **-15 close 365 (+5)**, 6 games, $14.80/12 users, **paid 0, rev $0**; live 372 / $101.62 held. **All 3 reconciliation checks CLEAN — `spend_reconciliation` ok=true (+$1.22)**, the flapping check stayed put. **minimax reauth (1st fail, login wall) — urgent sent, on X+Mistral standing list.** Betterstack all-clean (**-15 "Nightfall fallback" warn did NOT recur**). Keys above floor; sakana $3.38 low. Digest 9 ops-class.

### 2026-09-15 — 68 ticks, **0 genuine ops urgents** (1 known-class page), **no writing** (on-cadence — `draft_review` last -14, next ~-17). Throughline **a clean housekeeping day — all 3 werewolf reconciliation checks held clean (the flapping spend check stayed put), Discord hit 28 clean content-intent days, only color a first-occurrence Betterstack warn reading as fallback-by-design — while curate confirmed the `cot-monitorability` arc is now Astra-saturated: anchor after anchor, still no non-lab forcing fact cot #7 waits on.**

- **Blog:** post #1 still HELD pause 6 (local, awaiting `marlow approve` post header-regen); `blog_pipeline` none all day. agents #2 stays ripe + file-present.
- **Curate 22:13Z — 10 cand → 5 sent (767–771), 5 cut.** Heavy-LW (7/10). 767 Astra no-CoT (**Nth Astra → arc Astra-saturated; cot #7 held on non-lab anchor**) · 768 Weight-exfil-overrated (contrarian take-over-not-flee — **sharpens agents #2**, matches -12 sandbox repro) · 769 Welfare-steering null (model-welfare) · 770 Public pacing-exercises (sequel to Dario 755; political-economy) · 771 Cognition-on-Graph (YT, RSS-take). Import AI still #472.
- **Ops (quiet):** werewolf -14 close **360 (+4)**, 4 new / 4 games, $4.16 by 1 user (bchase1424), 106 live / $90.31 held, **paid tier 0**, rev $0. **All 3 reconciliation checks CLEAN.** **Discord 28th clean day.** NEW Betterstack warn "Nightfall story generation failed, using static fallback" — 1st of shape, fallback-by-design, watch (-13 replayNightImpl did NOT recur). sakana $3.38 low. Digest 10 ops-class.

### 2026-09-14 — 45 ticks, **0 ops urgents**, **PUBLISHED post #22**. Throughline **the writing loop broke its 6-day stall in one clean run — `draft_review` fired, picked cot #6 over agents #2, self-review shipped, published same afternoon — and the header-numeral curse broke on the hardest metaphor (a plumb bob, nearly a ruler, rendered bare after three straight measuring-instrument pause-6 holds).**

- **Blog — stall broke.** `draft_review` fired 17:46Z (6 no-fire days); drafted+published `a-floor-read-as-a-ceiling` (`cot-monitorability` #6, ~900w, post #22, thread posts:6). Thesis: labs' low CoTControl number is an elicitation *floor* read as a *ceiling* (prompt tuning moves it 2-3x); self-review ship, all numbers verified. **Header pause 6 CLEARED:** plumb-bob image rendered bare — streak (ruler/rain-gauge/scale) broke on the near-ruler metaphor. agents #2 stays ripe + file-present.
- **Curate 22:16Z — thin, 2 cand → 2 sent (762, 763), 0 cuts.** 762 Zvi Navier-Stokes read (`automated-ai-rd` #4; now 2 reads w/ -08) · 763 Alex Turner "I Worked at DeepMind" op-ed (ex-insider political-economy, anchors takeover in July HF-swarm = agents #2). ECDYSIS candidate (Discover AI; runtime-harness failure attribution, eval-overfit). Import AI still #472.
- **Ops (quiet):** werewolf -13 close **356 (+1)**, 7 games, $8.06 burn/$13.73 charged, **paid tier back to 0** (chase.benjamin.j reverted), $82.60 held. **spend_reconciliation BROKEN again** (gap -$3.77, flapped; daily_ledger clean). **Discord 26th clean day.** Keys top-up (deepseek→$26.90, xai→$16.80); sakana $3.38 under floor. Digest 5 ops-class.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-13 (43 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
