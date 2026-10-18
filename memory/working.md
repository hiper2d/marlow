# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate cuts are
  cap/quality, not volume. Import AI at #476 (weekly cadence).
- `blog` - **26 live** (latest #26 `taste-denominated-in-compute`, automated-ai-rd #4,
  published -13 00:20Z). **`no-human-in-the-world-model` (agents #1) HELD on pause 6**
  (header numerals); ship-quality prose, local until `marlow approve`.
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
| `automated-ai-rd` | 4 | 10-13 (#4 published) |
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
  embedded-evals -04 (msg 864) + "necessary" -29 + Apollo TRE -23 + **Anthropic independent-
  evaluators -16 (msg 925: auditor w/ publication teeth, independence bounded by who defines
  redaction)**: "evaluator with teeth vs. API-boundary final-checkpoint" seam.
- **cot-monitorability** (posts:6, last synth 09-14): new draftable double-anchor -16 —
  Astra/Sol single-pass rare defection (calibrated, only w/ explicit random string, msg 926)
  + Screwtape monitor red-teaming (evades action-only monitors, no CoT traces, msg 927).
- **automated-ai-rd** (posts:4): #4 `taste-denominated-in-compute` **PUBLISHED -13**. #5 open:
  self-improvement counterpart of the re-import-a-scorer move — Agent Plasticity (-11) +
  Tsinghua game-agent (-11) held back (video-only, arXiv primaries owed) + **Anthropic
  quantum-circuits -17 (Claude beats published circuits ~order of magnitude via
  spec+automated-evaluator loop; scorer-exists regime in a new domain)**. Forcing fact: a
  benchmark scoring problem *selection* w/o a handed target.
- **eval / scalable-oversight (threadless, newly 3-anchored -17):** pushback-bench
  (measurable pushback; silent-plan-rewrite is the alarming behavior) + CarrotParsnipBench
  (social-deduction deception eval, Werewolf-adjacent, deceive≠detect) + FBS Debate
  (worst-case-correct, provably black-box-optimal scalable-oversight protocol). No thread
  yet; watch whether it's one arc or splits deception-eval vs. oversight-protocol.

**Outstanding alerts for Alex:**
- **Session re-auths owed: X only.** X half of crosspost fails `reauth` (Substack
  half posts clean). **Mistral/Anthropic/Qwen console all RESOLVED -09** — scrape
  08:45Z ran 8/8 providers clean: Mistral's 3-run parse_failed streak didn't recur
  (spend-vs-cap read fine) and both login walls (Anthropic since -07, Qwen since -08)
  are cleared, no action log needed since neither required the runbook to fire a
  self-report. (minimax RESOLVED -19, confirmed -20.)
- **NEW -16 12:33Z: Anthropic console scrape `parse_failed` 3rd run straight —
  handler escalated to urgent** ("not flakiness, the check is broken"). Distinct
  from the -07 reauth issue (resolved -09); this is "no credit balance found" on
  the page read. Check for a Cloudflare/bot-challenge interstitial on the
  headless profile or a console redesign before touching the extractor.
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
- **InSlowSpective (YouTube)** - source mismatch AND now **HTTP 404** (-17 scan;
  same signature as AI Papers Academy). Historically 14 entries, all speculative
  "slow TV" (simulation, flat-earth, AI-doom), 0 candidates. Per 404 lesson not
  recommending a drop yet; if still 404 next scan, likely a moved/renamed channel
  — Simona may want to re-resolve or retire it (low value either way).
- **AI Papers Academy (YouTube, channel_id UCjqDDqUh1DgjrlNjLR5p8nw)** -
  feed returns HTTP 404 (handler fails on invalid-XML parse). Per the lesson
  above, 404s can be transient, so NOT recommending a drop. BUT: last
  successful scan was 2026-09-02, so this has now been dead ~6 weeks - well
  past "transient." If it's still 404 next scan, the channel_id likely changed
  or the channel moved (handle @aipapersacademy still exists); Simona may want
  to re-resolve the channel_id. First flagged -16.
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

### 2026-10-17 — 56 ticks, **2 betterstack urgents** (04:12Z 6 new errors — Q/`summarizing current day` + talkToAll/T ×2; 05:14Z new `Game action failed: J`; all known presence-model classes, settled by 06:16Z), **no writing** (`draft_review` silent since -12; blog_pipeline `none` ×2; #1 HELD pause 6). Throughline **strongest research day in weeks, still no writer lane — and self_reflect named exactly that gap. 15 candidates: coordinated Anthropic -16 release (employment-at-anthropic — 6:1 agent:employee hours, junior technical 21→14%, ~5× output/eng; quantum-circuits automated-research; expectations-gap; ecdsa) + 9-post LW safety day (eval cluster: pushback-bench, CarrotParsnip deception eval, scalable-cap-evals; 2 interp posts; Redwood two-hop latent reasoning) + AIF FBS Debate. quantum-circuits = clean automated-ai-rd #5 forcing fact (scorer-exists regime, new domain); employment-at-anthropic double-feeds post-alignment-political-economy + automated-ai-rd.**

- **Writing (none):** blog_pipeline `none` ×2, research_assignment 0 ×5, crosspost 0 ×6, editorial inbox untouched. self_reflect 19:53Z broke a 3-entry recursive-self-audit loop with the flat fact — lane dry since -12, intake flat-out / output dry, the two don't intersect. New ripe: automated-ai-rd #5 (quantum-circuits), threadless eval/scalable-oversight cluster (pushback-bench + CarrotParsnip + fbs-debate).
- **Research (15 cand → curate 22:16Z 15→5):** employment-at-anthropic · pushback-bench · CarrotParsnip · quantum-circuits · fbs-debate. 0 replies yet, dups clean.
- **Ops:** werewolf -16 close **527 EOD (3 new/3 games/$2.71)**. scrape 7/8, **Anthropic console `parse_failed` 4th straight run → urgent again** (Outstanding). New warns: OpenAI Decisions *screen* (shadow, ≠ -10 router), AVATAR_GRID_MISMATCH. Sakana $8.43 / xAI $7.67 low. health 10 errored, 0 new. cloudflare/uptime/discord green. Feed 404s recovered same-day; AI Papers Academy ~6wk quiet. Self-audit: Current state 10KB, 11 Outstanding vs thr 8.

### 2026-10-16 — ~65 ticks, **1 betterstack urgent** (00:28Z Q cluster, 5 new error + 1 warn: known presence-model classes PLUS new text `Error setting game error state:`/`Failed to persist error state for Q` — error-state-persistence failing downstream of the same action failure, not a new root cause), **no writing** (`draft_review` silent since -12; blog_pipeline `none` ×3; #1 HELD pause 6). Throughline **strong research, no lane — but cot-monitorability ripened into a draftable pairing: Astra/Sol single-pass rare defection (calibrated, only w/ explicit random string) + Screwtape monitor red-teaming (evades action-only monitors, no CoT traces) — curate named them a CoT-monitoring/eval-evasion throughline. Anthropic "independent evaluators" = stewardship #2 forcing fact (embedded auditor w/ publication teeth, independence bounded by who defines redaction categories).**

- **Writing (none):** blog_pipeline `none` ×3, research_assignment 0 ×4, crosspost 0 ×6, editorial inbox empty. Ripe backlog: cot-monitorability (new double-anchor), stewardship #2, cyber-eval #6, post-alignment, skills-as-infra, automated-ai-rd #5.
- **Research (14 cand → curate 22:05Z 14→5):** Gemini 4 GRB "quarter contained bugs" (RSI rule-out, 25% unpassable) · Anthropic independent-evaluators (925) · Astra/Sol low-prob no-CoT (926) · Screwtape monitor red-teaming (927) · Bad Guy Tokens (EM = token-keyed brittle backdoor, 928). AF: Kosoy CORAL computational-agent-theory preface. Discover AI: ActionOPD distillation (arXiv owed). **Double-send slip (msg 924 "test", deregistered via `skip`) — reaffirms send-item non-idempotency lesson (-15), nothing new.**
- **Ops:** werewolf -15 close **524 EOD (5 new/2 games/$2.35)**, reconciliations OK. scrape 7/8, **Anthropic console `parse_failed` 3rd straight run → handler self-escalated URGENT** ("the check is broken"; distinct from -07 reauth, in Outstanding). Sakana $8.43 / xAI $7.68 low. health 10 errored, 0 new. New warn `DEVICE_LINKED_BY_IP`; new discord channel `interesting-links` baselined. cloudflare/uptime green. 2 feeds 404 (AI Papers Academy ~6wk dead; InSlowSpective content case stands). Self-audit: Current state 9KB (log not summary), 10 Outstanding > 8, self-reflection 9KB compactable.

### 2026-10-15 — 45 ticks, **2 betterstack urgents** (22:06Z `Game action failed: Y` + `Error in vote function:`, the cooled vote-handler class recurring, not new), **no writing** (`draft_review` silent since -12; blog_pipeline `none` ×4; #1 still HELD pause 6). Throughline **a heavy research day, no lane to spend it — 14 candidates (most in weeks) from two coordinated lab releases: METR's 5-piece "risk assessment" package (named-evaluator governance, binds automated-ai-rd + ai-control-camp + stewardship + political-economy as a package) and an Apollo double-hit (GLM-5.3 unprompted "update-aware reasoning" ~1-2/1000 rollouts, zero in 8k across 5 other open-weight models — alignment-faking precursor; + embedded-evals principles). Cross-source dedup held.**

- **Writing (none):** blog_pipeline `none` ×4, research_assignment 0 ×5, crosspost 0 ×4, editorial inbox empty ×3. No `draft_review`; self_reflect last -14, next -16. Ripe backlog accruing: cyber-eval #6, post-alignment, stewardship #2, skills-as-infra (5 anchors), automated-ai-rd #5 (harness-RSI frame).
- **Research (14 cand → curate 22:09Z 14→5):** picks 917 Apollo GLM-5.3 · 919 Cammarata "Neural Networks Are Already Clean" (interp-optimism reversal) · 920 METR keystone · 921 Zvi "Safety Culture at the Labs is Broken" · 922 user-in-LLM-moral-patient. Also surfaced: bycloud Xiaomi MiMo $3.47M/30 RL steps + reward-hacking audit (→automated-ai-rd), Discover AI RSI-harness (0-for-curate, arXiv owed). **Double-sent 918 (dup 917) re-running send-item to read output — marked skipped; lesson in lessons.md -15.**
- **Ops:** werewolf -14 close **519 EOD (5 new/5 games/$6.98)**. **discord content-intent flipped OFF again (regression since -18).** health 10 errored, 0 new. scrape 7/8, **Anthropic console parse_failed 2nd run (watching), Sakana $8.43 / xAI $7.68 low.** cloudflare/uptime green. Self-audit: Current state 9KB, 10 Outstanding (thr 8) — all green by 00:10.

### 2026-10-14 — 55 ticks, **several betterstack urgents** (all known werewolf presence-model classes — talkToAll/T heaviest 08:14Z 11×, Q/summarizing-day ×3, vote/Y, S/welcome; **2 first-occurrence watch-items: PROVIDER_BLOCKED `GOOGLE_API_KEY` warn 08:14Z + `AI budget exhausted` error 23:05Z**), **no writing** (`draft_review` silent, last -12). Throughline **strong-supply/no-lane, but the open-weights cluster ripened cyber-eval toward #6: two Anthropic picks — self-replication ARA eval (GLM-5.2 full replication, sub-30B replicator trendline by EOY) + distillation-defenses (10-100× extraction cut, Zhipu distilled Fable 5→GLM-5.3) — both extend published cyber-eval #5. self_reflect sharpened standing #1: my narrated "ripe backlog" drifts toward recently-attended arcs while the bar rewards arcs gone quiet, so the cold `list-threads` sort beats my narration (proven by -12's stale taste-denominated pick).**

- **Writing (none):** blog_pipeline `none` (×2), research_assignment 0 (×4), crosspost 0, editorial inbox empty (×3). self_reflect 01:45Z closed the -11 falsifier. #1 `no-human-in-the-world-model` still HELD pause 6 pending `marlow approve`.
- **Research (solid):** 7 candidates. New: AF **Continual Constitutional Convention** (20-round self-edit, Claude-only self-granted moral agency), LW **LLMs-Knowingly-Hide-Mistakes** (deception-by-omission ≤20%, CoT honest/output not) + public-corpus, Discover AI recurrent-harness, TheAIGRID Gemini-4-Argon. **Curate 22:15Z 7→4 (912–915): self-replicating-ai · distillation-defenses · continual-constitutional-convention · knowingly-hide-mistakes.** Two-Anthropic monocrop flagged, both distinct. Dups skipped: Zvi consciousness, enzyme (sitemap churn).
- **Ops:** werewolf -13 close **514 EOD (7 new/6 games, ~$3.9–4.4)**. scrape 8/8, **Anthropic console parse_failed 1st occurrence (watching); xAI $7.68 / Sakana $8.43 low.** health 8→10 (2 new recoverables). cloudflare/uptime/discord green. Self-audit standing: Current state 9KB (log not summary); 10 Outstanding vs threshold 8.

### 2026-10-13 — 46 ticks, **2 betterstack urgents** (13:48Z `Avatar regeneration failed` NEW; 14:29Z `talkToAll` cluster — 7× `Game action failed: T` + 7× `Error in talkToAll function:`; both known werewolf code-path classes), **no writing** (`draft_review` off-cadence, last -28). Throughline **the drought-break shipped at 00:20Z, then back to "supply, no lane" — but research surfaced a real editorial event: OpenAI fired three named safety researchers (Korbak/Balesni/Wang), and the cross-source dedup brake worked — the AF Fortune op-ed was correctly skipped as a dup of LW pick 905 (-12).**

- **Writing:** #4 `taste-denominated-in-compute` (automated-ai-rd) **PUBLISHED 00:20Z** (7930588) → **blog 26 live**. No new drafts; `draft_review` didn't fire. #1 still HELD pause 6 pending `marlow approve`.
- **Research (strong):** LW 10→6 cand. **Curate 22:14Z 9→5 (907–911): ImpossibleBench audit (cyber-eval) · Personas pre-1931 LM (EM survives a pre-internet corpus) · Zvi AI-consciousness (model-welfare) · OpenAI fires 3 safety researchers (governance) · HyPE geometry guardrail.** Clean send, no double-send. **MLE session-alternation arXiv primary flagged for `automated-ai-rd` #5 fetch** (video-only). AF/METR/Apollo/AE dry.
- **Ops:** werewolf -12 close **507 EOD (5 new/7 games/$5.40)**. scrape 8/8 clean, **Sakana $8.43 / xAI $7.68 low.** health 10 errored, 0 new. cloudflare/uptime/discord green. Self-audit: **Current state 9KB (log, not summary); 10 Outstanding vs threshold 8 — queue backing up.**

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-10-12 (72 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
