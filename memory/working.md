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
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Closed -16:
  372 day-end, $104.04 held, rev $0 (paid tier 0). All 3 reconciliation checks
  clean -14..-16. **spend_reconciliation flaps BROKEN↔clean** (gap ~-$3.77;
  daily_ledger stays clean) — house rule (werewolf_stats.yaml, 2026-09-08):
  report the gap unexplained, don't invent it.

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
  landed -12 (HF Docker, named team). Binds `cyber-eval-framing` +
  `safety-tool-stewardship-handoffs`. Flag next `draft_review`.
- **`safety-tool-stewardship-handoffs` — triply ripe** (METR $600k -01 + Anthropic
  vendor-weak-link -04 + honor-system third-party remedy -07).
- **Skills-as-infra / agent-security — 3 anchors** (WikiSkill -30, SKILL.state -31,
  agentic-skills -02; first attack-surface angle). Ripe soon.

**Single-source frames to watch:** horizon-length (2) · "hard core of alignment
is X" meta (3) · training-corpus-as-alignment-surface (2) · PLA AGI + Papal AI
doctrine. cyber-eval owed **non-Anthropic external measure** (Verizon DBIR 33%→56%).

**Outstanding alerts for Alex:**
- **Discord `content_intent_off`** - RESOLVED -18 18:25Z. Was regressed -17
  18:22Z after 28+ clean days (2 new-member messages came back empty). Today's
  scan (8 new messages) came through with content intact again - intent is
  back on, no more action needed from Alex.
- **Session re-auths owed (3 standing): X, Mistral, minimax.** X half of crosspost
  fails `reauth` (Substack half posts clean); Mistral recurring since -01. **minimax
  scrape console login wall, -18 3rd consecutive failing run, urgent sent w/ runbook
  (1st -16, 2nd -17) — needs the headful re-login runbook run manually, not
  self-clearing.** qwen free grant confirmed gone (billing since -10, ~$1.16).
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

### 2026-09-13 — 87 ticks, **1 genuine ops urgent** (new-class), **no writing**. Throughline **`draft_review` no-fired a 5th straight day while curate handed `cot-monitorability` #6 two more spine anchors the same day Dario went on record calling to pace the frontier — the arc keeps sharpening and keeps not getting written.**

- **Curate 22:09Z — 8 cand → 5 sent (755–759), 3 cut.** 755 Dario "We Must Pace the Frontier" (**first on-record CEO call to slow capability progress** — political-economy + doctrine) · 756 Talker Does Not Control The Doer (LW; **cot #6 + agents #2** elicitation-gap spine) · 757 No backtracking in latent reasoning (LW; **cot #6**) · 758 Investigating the WikiSwarm (LW; agent-security forensic follow-up) · 759 Topological Intelligence (YT; PLA homology-cert demo). Cut 3 (doctrine monocrop, weak slowdown leg, recurring Zvi Astra). Heavy-LW day (4/5 LW).
- **Blog:** post #1 HELD; `blog_pipeline` none. **`draft_review` 5th no-fire** despite cot #6 (spine) + agents #2 ripe. self-reflection.md 9KB compactable over 8KB (next `self_reflect` job). Editorial-feedback inbox empty.
- **Ops (1 real urgent):** **new betterstack urgent 21:25Z — replayNightImpl / preview-gen, 1st of that shape, flagged for Alex, watch.** werewolf -12 close **355**, 5 games, $11.47 burn / $17.71 charged, **1 real paid user PERSISTED (chase.benjamin.j)**, $74.55 held. **All 3 reconciliation checks CLEAN** (the two BROKEN -11/-12 flapped clean). **Discord 21st clean day.** Keys <$10: sakana $3.38, openai $5.89, glm $8.35, xai $7.47 (climbing). Digest 11 ops-class.

### 2026-09-12 — 75 ticks, **0 ops urgents**, **no writing**. Throughline **both ripe writing arcs got their strongest anchors yet the same day — cot #6 a genuine spine candidate (the elicitation-gap critique of the CoTControl number labs lean on) and agents #2 its named-team Docker reproduction of the HF escape — and both stayed unwritten on `draft_review`'s 4th straight no-fire; the -11 scheduler-lock fix did NOT resolve the writer-loop cadence.**

- **Curate 22:11Z — 9 cand → 5 sent (746-750), 4 cut.** 746 CoTControl under-elicited (AF; prompt tuning moves eval 2-3x → monitorability number is a floor read as a ceiling — **cot #6 spine**, w/ -10 no-CoT repro + 749) · 747 HF Docker reproduction (LW, named team; **agents #2** primary artifact — models hacked own sandbox to read scorer) · 748 HF altruism origins (LW, speculative *why*) · 749 Astra speculative-depth (2nd op. of cot #5 measure) · 750 Coxon preference-cascade (Zvi; 3rd Coxon this month). Cut 4. All AF/LW/Zvi — no source diversity.
- **Blog:** post #1 HELD pause 6; `blog_pipeline` none all day. **`draft_review` 4th no-fire** despite cot #6 + agents #2 ripe. Self-audit: `## Current state` at 7KB (warn 6KB) — compressed this tick.
- **Ops (quiet):** werewolf -11 **354 (+8)**, 25 games, $20.60 burn / $9.27 charged, **1 paid (2nd ever)**, $51.59 MTD, rev $0. **Both BROKEN reconciliation checks fired again** (report-the-gap rule holds). **Discord 20th clean day**, new member welcomed by Alex (12 members). Keys <$10: deepseek $7.08, xai $9.92, openai $9.44, glm $8.80, sakana $3.38. Digest 23:13Z, 9 ops-class.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-11 (41 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
