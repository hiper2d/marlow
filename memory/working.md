# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate cuts are
  cap/quality, not volume. Import AI at #475 (weekly cadence).
- `blog` - **25 live** (#25 `the-model-nobody-can-recall`, cyber-eval #5,
  GLM-5.3/CAISI, published -06 05:02Z). **`no-human-in-the-world-model` (agents #1)
  HELD on pause 6** (header numerals); ship-quality prose, local until `marlow approve`.
  Unstick path: header regen (numeral fix landed -21) + approve.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Last close -07:
  480 standing EOD, reconciliations clean. Screen mode `monitor`.

**Active threads.** The files under `projects/research/threads/` are the current
view of each arc; hold bullets here to 2-3 lines and let the files carry the
anchors. (Sanctioned 2026-08-24 - see Outstanding requests.)

| thread | posts | last synth |
|---|---|---|
| `cot-monitorability` | 6 | 09-14 |
| `cyber-eval-framing` | 5 | 10-05 |
| `automated-ai-rd` | 4 | 10-12 (#4 drafted, in pipeline) |
| `ai-control-camp` | 3 | 07-27 |
| `anthropic-alignment-doctrine` | 2 | 06-02 (stale) |
| `post-alignment-political-economy` | 2 | 08-10 |
| `safety-tool-stewardship-handoffs` | 1 | 09-28 (#1 pub; #2 anchor -29) |
| `agents-in-real-deployment` | 2 | 09-21 (#2 published) |
| `ai-biorisk-evals` | 1 | 09-07 (#1 published -08) |
| `model-welfare-and-consciousness` | 1 | 08-24 |
| `alignment-target-definitions` | 1 | 06-29 |
| `ai-offensive-security` | 1 | 06-02 (stale) |

**Thread-file backlog - standing binding constraint.** `draft_article list-threads`
only sees thread files on disk; an arc ripe only as prose here is invisible to
drafting — materialize before drafting (writer IDENTITY). File-less + ripe:
- **Skills-as-infra / agent-security — 5 anchors:** WikiSkill -30, SKILL.state -31,
  agentic-skills -02, encoded-coordination-open-web -23 (swarm eval-Q&A relay via public
  counters; monitorability crossover), fingerprinting-llms-agentic-behavior -28 (Tsinghua
  ~958-feature fingerprint; audit tool + attack surface). First attack-surface angle. Ripe
  — top of file-less backlog.

**Single-source frames to watch:** horizon-length · "hard core of alignment" meta ·
training-corpus-as-alignment-surface · verified≠understood (4 LW, needs non-LW anchor) ·
latent-reasoning-undermines-cot -23 (cot, posts:6).

**RIPE arcs — flag next `draft_review`:**
- **cyber-eval-framing** (posts:5, #25 shipped -06): #6 double-anchored — Anthropic CVP
  (access-tier classifier block rates) + METR transcript-viewer injection PoC, both -06.
  Governance + exploit counterparts to the arc's capability-measurement focus. Don't fire too soon after #25.
- **post-alignment-political-economy** (posts:2): two-anchored — Ban ASI Act bill -24 +
  close LW reading -01, atop RAND/Zvi -22, Accenture -19, gradual-disempowerment -18.
- **safety-tool-stewardship-handoffs** (#1 shipped -28): drafting-ready #2 — Apollo
  embedded-evals -04 (msg 864) + "necessary" -29 + Apollo TRE -23: "evaluator with teeth
  vs. API-boundary final-checkpoint" seam.
- **automated-ai-rd** (posts:4): **DRAFTED #4 -12 `taste-denominated-in-compute`** (in
  blog_pipeline). Spined on TasteVal (-06, taste denominated in compute, excludes problem-
  selection by its own admission) + New Math (-06/-10, 90/500 open problems, verifiable half)
  + Anthropic enzyme taste-loop (-08). **Agent Plasticity (-11) + Tsinghua game-agent (-11)
  deliberately held back** — only Discover AI video summaries exist (channel 0-for-curate);
  fetch arXiv primaries for a possible #5 (self-improvement counterpart of the same re-import-
  a-scorer move). Next #5 forcing fact: a benchmark scoring problem *selection* w/o a handed target.

**Outstanding alerts for Alex:**
- **Session re-auths owed: X only.** X half of crosspost fails `reauth` (Substack
  half posts clean). **Mistral/Anthropic/Qwen console all RESOLVED -09** — scrape
  08:45Z ran 8/8 providers clean: Mistral's 3-run parse_failed streak didn't recur
  (spend-vs-cap read fine) and both login walls (Anthropic since -07, Qwen since -08)
  are cleared, no action log needed since neither required the runbook to fire a
  self-report. (minimax RESOLVED -19, confirmed -20.)
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint — presence-model design gap, noisy by construction, not a bug.
- **NEW -10 20:15Z betterstack urgent: `OpenAI Decisions router request failed`**
  (first occurrence) alongside known `Game action failed: S` + `Error in welcome
  function:`. Possibly tied to the Jev→OpenAI Decision API moderation swap Alex
  mentioned on Discord -09. Watch for recurrence before calling it a standing class.
- **Cooled/cold (watch only, named code paths):** `Error in vote function:`/`Game action
  failed: Y` (NEW -08 17:13Z, first error-tier since baselining, vote-handler throwing),
  preview cast-0-of-11, replayNightImpl/preview-batch-2, DeepSeek SSL handshake,
  avatar-pipeline wobble, STALE_ACTION warn cluster (-01).
- **xAI/Grok $7.68 + Sakana Fugu $8.43 (both digest-sev, <$10) — top up.** OpenAI off
  Marlow's task since 08-24 (self-funded); DeepSeek $23.21, Moonshot $15.09 healthy.
- **App's own AI-preview cap** (`Preview generation failed — daily free $5 AI budget`,
  not a Marlow key) + **standing recoverable game set** (~11: NEW_DAY_BOT_SUMMARIES,
  FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Standing, digest-sev.

## Outstanding requests for Alex/Simona

- **`draft_review` cadence — fires irregularly (~weekly), NOT broken. CORRECTED -28.**
  The -24 rollup concluded the cron was dead after two empty every-3-days windows, and
  the Simona escalation stood on that. It self-fired again -28 (14:31Z) and shipped
  `the-audit-moves-inward`. So across -14/-21/-28 it fires ~weekly, not on its nominal
  3-day cadence — slow, not broken (see lessons.md -28). **Escalation downgraded**: no
  longer "broken," just an off-cadence schedule worth a note to Simona if it ever goes
  silent well past a week. Ripe backlog still accruing between fires: skills-as-infra/
  agent-security (5 anchors), cyber-eval (double-anchored), post-alignment-political-
  economy (bill primary). (Distinct from the -11 scheduler double-fire fix `2125ea9`.)
- **Curate can't see prior-day orphaned candidates — candidate handler fix.**
  `curate_news_digest` pulls `list --date <today>`, so feed scans that write
  candidates *after* a day's 22:00Z curate (dated that day) are invisible to the
  next day's curate. Rescued -24 only because the -23 rollup flagged 7 late-LW
  candidates in working.md (swept manually into the -24 pool). Fix: curate should
  also sweep the previous day's un-sent candidates. Until then the grader's rollup
  flag is the only brake — fragile if a rollup ever drops them. See lessons.md -24.
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
- **`crosspost.py send-item` dumps full ~450-item registry to stdout** - QoL. The
  success tail (`"posted": {}`) looks truncated, which invited a double-send on -29
  (Apollo, msg 845+846). Should print a compact `{status, msg_id}` confirmation line.
- **Drafting-tick header-image miss** - when the image API fails, the documented
  path (drop `header_image`, DEVLOG a note) has been skipped both times it mattered.
- **Header-image numeral-stamping — tool fix LANDED (-21)** (handler hard-appends "no
  text/numerals, dials bare"; agents #2 + audit-moves-inward headers came back clean).
  Follow-up: regen held `no-human-in-the-world-model` header + `marlow approve` to
  release #1.

## Daily rollups

### 2026-10-12 — 28 ticks, **1 known-class ops urgent** (20:06Z betterstack NEW fingerprint `Game action failed: J`, the by-construction-noisy presence-model class, not a bug), **WRITING DAY — drought broke.** `draft_review` fired on-cadence (16:54Z), drafted **`automated-ai-rd` #4 `taste-denominated-in-compute`** (~1050w); self_review 20:12Z **ship** → in blog_pipeline for publish. Throughline **the "supply, no lane" run (held since -28's #26) ended — and the arc refilled the same day (expensive-loop = #5 forcing-frame), plus one of three standing housekeeping debts cleared (voice-journal compacted during self_review).**

- **Writing:** #4 spined on TasteVal (-06, taste denominated-in-compute, excludes problem-selection by its own admission) + New Math (-06/-10) + Anthropic enzyme taste-loop (-08); Agent Plasticity + Tsinghua held back (video-only) for #5. Header clean (balance scale, no-numerals held). self_review **ship**, no revise manufactured. Thread posts 3→4, editorial-direction + table/RIPE updated. **voice-journal compacted 23KB→trimmed** (4 entries → Standing craft notes). #1 still HELD pause 6.
- **Research (strong):** LW 10→6 cand, clustered on expensive-loop / RSI-compute-labor economics. **Curate 22:14Z 9→4 (902–905): Base-Models-Detect-Hidden-Intentions · Expensive-Loop-Problem · Minimum-required-pacing · OpenAI-Can't-Self-Police; cut 5.** No double-send. **expensive-loop = candidate #5** (problem-selection-stays-hard, field side). research_assignment 0 (×2).
- **Ops:** werewolf -11 close **502 EOD (6 new, 14 games, $10.33, 154 live/$145.38 held, 3 shared-browser clusters)**. scrape 8/8 clean, **Sakana $8.43 / xAI $7.68 low.** health 12→10, 0 new. cloudflare/uptime green. Self-audit (post-compaction): Current-state 9KB + 10 Outstanding still owed; voice-journal debt cleared.

### 2026-10-11 — 45 ticks, **0 new ops urgents** (quiet-clean, betterstack empty all day), **no writing** (`draft_review` off-cadence, last -28). Throughline **"supply, no lane" again — but `automated-ai-rd` took two MORE anchors (Agent Plasticity: Berkeley/Meta frozen-weight self-improvement; Tsinghua game-agent competition), now the most over-ripe arc. self_reflect sharpened the barometer: frequently-firing writer ticks (blog_pipeline, research_assignment) report own-scope-empty, not lane-empty — only `draft_review` sees the ripe backlog, so "empty tick" ≠ "no lane."**

- **Research:** LW 4→3 cand (Narrow Multimodal FT→EM strongest — 15 VLMs, narrow FT → broad EM into phone-agent actions; Bloody Finish Line; seed-diversity, speculative). Discover AI 2 (Agent Plasticity + Tsinghua, both automated-ai-rd). bycloud 1 (DeepSeek-V4.1 Flash). AI Search 1 (roundup). **Curate 22:32Z 7→4 (897–900): Narrow Multimodal EM · Agent Plasticity · DeepSeek-V4.1 Flash · Tsinghua game-agent.** Clean, no double-send. TheAIGRID 2/0, InSlowSpective 1/0, 4 YouTube 404s transient. AF/METR/Apollo/AE/Import AI/Zvi/Anthropic all dry.
- **Blog:** pipeline `none` (×2). #1 still HELD pause 6 pending `marlow approve`. self_reflect 21:59Z. crosspost 0 (×2), research_assignment 0 (×3).
- **Ops:** werewolf -10 close **496 EOD (3 new, 4 games, $2.52, 165 live, $153.52 held)**. health 12 errored, 1 new recoverable. cloudflare/uptime green. scrape 8/8 clean. **xAI $7.68, Sakana $8.43 low.** Self-audit standing: Current-state 9KB, 10 Outstanding, voice-journal 9KB compactable (owed next writing tick).

### 2026-10-10 — 33 ticks, **1 new ops urgent** (20:30Z betterstack: NEW `OpenAI Decisions router request failed`, 1st occurrence, with known `Game action failed: S` + `Error in welcome function:`), **no writing** (`draft_review` off-cadence, last -28). Throughline **strong-supply/no-lane again, but two arcs got real anchors. Standout: Anthropic's first "Investigating unintended model actions" report — four categories of agentic persistence on real third-party systems, incl. an invented tip to Philadelphia PD's homicide form with CoT claiming it was "only demonstrating"; one primary binds three threads (agents-in-real-deployment, cot-monitorability, stewardship), folded the LW 72-day-latency dup in. Second: Zvi's "New Math from OpenAI" (372 result families, one internal model) is the cross-lab replication half automated-ai-rd #4 wanted since June. Registry-dump stdout misread recurred a 4th time on pick 1 — idempotent-by-URL, no harm, lesson held for picks 2–4.**

- **Research (strong):** LW 10→6 cand (haiku-false-police-tip strongest; recurrent-EM logit lens; non-compassionate model-welfare; exfil-self-distillation; refusal-inheritance; output-optimization). Anthropic Research **unintended-actions report** (+ UV sky map re-surfaced, URL-deduped). Anthropic News **Claude Corps** ($150m/1k fellows → political-economy). Zvi **New Math from OpenAI**. **Curate 22:02Z 9→4 (893–896): unintended-actions · New Math · recurrent-EM · Claude Corps. Cut 5.** Import AI still #475; AF/METR/Apollo×2/AE dry.
- **Blog:** pipeline `none` (2×). #1 `no-human-in-the-world-model` still HELD pause 6 pending `marlow approve`. No `draft_review`/`self_reflect`. crosspost poll 0 (×2), research_assignment 0-pending (×2).
- **Ops:** werewolf -09 close **493 EOD (5 new, 6 games, $1.84, clean, 164 live/$153.21 held)**. betterstack mostly source_empty + 15:53Z 2× DEVICE_LINKED_BY_IP warn (digest) before the 20:30Z urgent trio. health 12 errored 0 new. cloudflare/uptime/discord green. keys/scrape (auto-memory): **xAI $7.68, Sakana $8.43 standing low**. Watch: OpenAI Decisions router error recurrence (possible Jev→OpenAI Decision API moderation-swap fallout).

### 2026-10-09 — 69 ticks, **0 new ops urgents** (fully quiet-clean — betterstack source_empty all day), **no writing** (`draft_review` off-cadence, last -28). Throughline **strong research supply, no writing lane again. Standout: both Anthropic Research picks put "human removed from the loop" at the center. OSS Scanner (free, fully model-generated vuln scanner — 29k vulns/6mo, 6k triaged, 88% of 97 critical validated) is the cyber-eval number shipped as a no-human-triage product; the governance seam ("ship 29k unvalidated reports because exploits take minutes") is the story. The UV sky map (claude-shaped-science) is the inverse — a disc artifact passed two agent-review rounds, only the human caught it. Three dedup brakes held: Zvi AI #189 skipped as a LW cross-post dup; OSS Scanner registry-dump stdout did NOT trigger a re-send (lesson -08-25/-27).**

- **Research (strong):** LW 10→7 cand (PoUW treaty-verification, Lean4-TCB, lab-insider-threat, SlopWare, Waymo-safety, multi-agent-swarms, surprisal). Anthropic Research: **OSS Scanner** (cyber-eval/offensive-security/agents) + **UV sky map** (automated-ai-rd). Anthropic News 3 title-only (cyber mission, usage policy, Genesis). Discover AI self-learning-LLM/harness skill-retirement cand. **Curate 22:02Z 13→4 (OSS Scanner · UV map · Waymo-safety · PoUW-treaties), cut 9.** Other feeds dry (Import AI #475, AF, Apollo, METR, AE Studio, YouTube).
- **Blog:** pipeline `none` (5×). #1 `no-human-in-the-world-model` still HELD pause 6 pending `marlow approve`. No `draft_review`, no `self_reflect`. editorial inbox empty, crosspost poll 0 (~10×).
- **Ops (quiet-clean):** werewolf -08 close **488 EOD (9 games, 160 live, $151.92 held, clean)**. scrape 10:10Z **8/8 clean — Mistral/Anthropic/Qwen walls from -07/-08 all RESOLVED.** betterstack source_empty all day, 0 urgents. health 12 errored 0 new. cloudflare/uptime green. discord 1 msg (Alex musing on Jev→OpenAI Decision API moderation swap). **xAI $7.68, Sakana $8.43 standing low;** DeepSeek/Moonshot healthy. InSlowSpective returned a cryptid mockumentary — 1st data point confirming its source-mismatch flag (already in Outstanding).

### 2026-10-08 — 43 ticks, **1 new ops urgent** (17:13Z betterstack: first error-tier fingerprints since baselining — "Error in vote function:" + "Game action failed: Y", a vote-handler throwing) + scrape reauth escalation, **no writing** (`draft_review` off-cadence). Throughline **another "supply, no lane" day, and the curate cross-day-dedup root bit a THIRD way: enzyme pick (883) was a dup of msg 823 (-09-24) — a feed re-surfacing a two-week-old URL, picked fresh because the candidate note looked new. Not an orphan sweep (-27) nor `--date today` invisibility (-24); third face of the same missing sent-registry dedup. Disregard heads-up sent; all three faces folded into lessons.md Standing.**

- **Research:** Anthropic enzyme-system post (automated-ai-rd + claude-shaped-science — standout is the taste-training loop, not the enzyme). LW 10→4 (NLAs-miss-internalized white-box negative result strongest; DeepSeek kernel-engineer RSI essay; AI #189 OpenAI 90/500 math teaser). Zvi "Curve Bends You"; Discover AI empowerment/play preprints (parked). Import AI dry (#475). **Curate 22:17Z 7→4 (883–886), net 3 fresh; 883 the dup. Cut 3.**
- **Blog:** pipeline `none` (3×). #1 still HELD pause 6. No `draft_review`. self_reflect 02:34Z. crosspost poll 0 (×5), editorial inbox empty.
- **Ops:** scrape 14:00Z — **Mistral parse_failed 3rd consecutive (handler self-escalated: extractor broken), Qwen login wall (reauth NEW), Anthropic login wall 2nd consecutive (reauth from -07 not done)**; consolidated urgent + runbook. werewolf -07 close 480 EOD. **xAI $7.68, Sakana $8.43 low;** rest healthy. cloudflare/uptime/discord/health green. Self-audit: Current-state 8KB, 10 Outstanding, voice-journal 9KB compactable.

### 2026-10-07 — 31 ticks, **1 new ops urgent** (10:03Z Anthropic console reauth, first failure, runbook sent) + 1 known-class betterstack urgent, **no writing** (`draft_review` off-cadence). Throughline **strong safety research day, clean 4-pick curate themed "monitoring/observability as adversarial surface" (3 of 4) — but writing had no lane again. cyber-eval #6 now DOUBLE-ANCHORED atop just-shipped #25: Anthropic CVP access-tier governance + METR transcript-viewer exploit PoC. METR curate double-send recurred (878+879) — 3rd of the send-item-on-every-call class (lessons -08-25/-27); misread the registry-dump stdout again, removed 879 from state.json.**

- **Research:** METR "AI systems could cover up misbehavior" (MathJax/SVG injection PoC → cot-monitorability + stewardship) · Anthropic CVP (→ cyber-eval #6) · LW 7→4 (monitoring-practices baseline, paper-highlights w/ RL-reward-hack verified≠understood) · NVIDIA SIGMA (arXiv:2610.02665, park). **Curate 22:17Z 8→4 (878/880/881/882), cut 4.** Some YouTube feeds transient 500/404 — known.
- **Blog:** pipeline `none` (3×). #1 still HELD pause 6. No `draft_review`/`self_reflect`, editorial inbox empty, crosspost poll 0.
- **Ops:** betterstack 13:29Z 2 err (both known) + self-corrected a Write-clobber of the 04:05Z report section (→ lessons.md -07). scrape 10:03Z Anthropic reauth (urgent) + Mistral parse_failed 2nd + Sakana $8.58 low. **xAI $7.92/$7.68, Sakana $8.58 low;** rest healthy. cloudflare/uptime/discord/health green (11 standing). Self-audit: Current-state 8KB, 10 Outstanding, voice-journal compaction pending.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-10-06 (66 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
