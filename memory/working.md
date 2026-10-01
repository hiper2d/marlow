# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate discipline
  holding: cuts are cap/quality, not volume. Import AI at #474 (weekly cadence).
- `blog` - **24 posts live** (last: `the-audit-moves-inward`, safety-tool-
  stewardship #1, pub -28). **`no-human-in-the-world-model` (agents #1) HELD on
  pause 6** (header numerals) since -31; prose ship-quality, local until
  `marlow approve`. Numeral tool fix LANDED -21 → unstick via header regen + approve.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Last close -29:
  441 day-end (437+4, 0 games, $3.44), 3 reconciliations clean (spend gap = previews;
  werewolf_stats.yaml -09-08 house rule: report gap unexplained, don't invent). Content
  screen mode `monitor`.

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
training-corpus-as-alignment-surface · verifiability/verified≠understood (4 LW, needs
non-LW anchor) · latent-reasoning-undermines-cot -23 (cot, posts:6).

**RIPE arcs — flag next `draft_review`:**
- **cyber-eval** (posts:4, synth 08-03): **NEW primary — GLM-5.3 open-weights cyber
  proliferation -30** (Frontier Red Team + NIST CAISI, named model + real numbers) atop
  postmortem -18 + Gemini CTF breakout -19 + Lifshitz secure-acceleration -25. GLM-5.3
  also unsticks stale `ai-offensive-security` (synth 06-02) and touches
  `anthropic-alignment-doctrine`. Strongest-anchored arc after skills-as-infra.
- **post-alignment-political-economy** (posts:2, synth 08-10): PRIMARY Ban ASI Act bill
  -24 (Sanders/Casar + MIRI) atop RAND/Zvi -22, Accenture -19, gradual-disempowerment
  -18, geopolitics-of-treaty -25.
- **safety-tool-stewardship-handoffs** (#1 shipped -28): Apollo embedded-evaluators
  (-29 primary) + Zvi quest-for-embedded-evaluators (-28) + Apollo TRE (-23) triple-
  anchor the "evaluator with teeth vs. API-boundary final-checkpoint testing" seam.

**Outstanding alerts for Alex:**
- **Session re-auths owed (2 standing): X, Mistral.** X half of crosspost
  fails `reauth` (Substack half posts clean); Mistral recurring since -01.
  qwen free grant gone (billing since -10). (minimax RESOLVED -19, confirmed -20.)
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint — presence-model design gap, noisy by construction, not a bug.
- **Cooled/cold (watch only):** preview cast-0-of-11 (-28 urgent, no recurrence -29),
  replayNightImpl/preview-batch-2 (-23), DeepSeek SSL handshake (-22), avatar-pipeline
  wobble (-27). Named code paths, effectively cold.
- **xAI/Grok ~$9.93 <$10 low-balance (standing since -22, digest-sev)** — top up soon;
  Moonshot/DeepSeek fine.
- **`Preview generation failed — daily free $5 AI budget`** — app's own AI-preview
  cap (not a Marlow key), recurring occasionally (Mild Forest Camp -25/-26) = usage
  growth confirmed. Standing, digest-sev.
- **Standing recoverable app errors:** El pueblo (NEW_DAY_BOT_SUMMARIES), plus a
  rolling 7–8 recoverable game set (FreeSpendLimit/quota, Dracula role-lookup).

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

### 2026-09-30 — 45 ticks, **0 new ops urgents** (20:12Z betterstack pair = standing game-action noise, not new), **no writing** (`draft_review` off-cadence, last -28, next ~-05). Throughline **strong research supply vs. quiet ops: Anthropic Research delivered GLM-5.3 — the concrete open-weights offensive-cyber-proliferation anchor (autonomous end-to-end exploits ≈ Claude Mythos Preview, safeguards bypassed 64–100% with simple techniques, NIST CAISI cross-validated). Named-model *primary* for `cyber-eval-framing` (already ripe), unsticks stale `ai-offensive-security`, touches `anthropic-alignment-doctrine`. Curate 22:09Z 4→3. Ripe backlog gained a primary anchor, still no writing lane to absorb it.**

- **Research:** Anthropic Research 3 cands (GLM-5.3 STRONG · robot-jobs exposure index, 0.3% cost-competitive/~40yr → political-econ · what-do-you-want, cut). bycloud `inference-as-a-service-economics`. **Curate 22:09Z 4→3 (850–852):** GLM-5.3 · robot-jobs · inference-as-a-service (video body no-fetch, take from summary). Feeds else quiet; Import AI #474.
- **Blog:** #1 HELD pause 6, local pending `marlow approve`. `blog_pipeline` none (2×). No `draft_review`. Editorial inbox empty. crosspost poll 0 (845–848 unflagged). No self_reflect (last -28).
- **Ops (quiet-clean):** werewolf -29 close **441 EOD (437+4, 0 games, $3.44)**, 3 reconciliations CLEAN ($0.43 gap = previews). Screen 37/10 would-block/3 grey — all bchase1423 sexual (game day 5), mode `monitor`. betterstack DEVICE_LINKED_BY_IP warns (digest) + 20:12Z standing pair; uptime/scrape green; keys xAI $9.93 low. Digest 10 entries 23:11Z **flagged self-audit: Current state >6KB, 10 Outstanding, self-reflection compactable** (last two are self_reflect's lane).

### 2026-09-29 — 41 ticks, **0 ops urgents (quiet-clean)**, **no writing** (`draft_review` no-fire, ~weekly off-cadence; fired -28, next ~-05). Throughline **a strong research-supply day, two arcs took key anchors against fully quiet ops. The 22:17Z curate (11→4) landed the #2 anchor `safety-tool-stewardship-handoffs` was waiting for — Apollo's "embedded evaluators are necessary" (primary, evaluator *with teeth*), the direct sequel to `the-audit-moves-inward` (#1, -28) — and fed `automated-ai-rd` its Zhipu-RSI anchor (Import AI 474). Ripe backlog grew again with no writing lane to absorb it; safety-tool-stewardship now 2-anchored and drafting-ready next fire.**

- **Research:** Curate 22:17Z **11→4 sent (845–848):** Apollo embedded-evaluators (safety-tool-stewardship #2) · Astra-6.1-pulled (Zvi/WSJ: OpenAI scraps next frontier model over deception, agents-in-real-deployment) · chess-transformer-Elo (LW Maia-3 interp, diversification) · Import AI 474 Zhipu RSI (automated-ai-rd #4). **Apollo double-sent (845+846)** — send-item stdout QoL (in Outstanding). Cut: project-swap (stale, sent -25), 3 theory posts, too-cheap-to-meter, wirehead, notonlyhuggingface. **Import AI now #474** (status was stale #473, fixed).
- **Blog:** #1 still HELD pause 6, local pending `marlow approve`. `blog_pipeline` none (4×). No `draft_review` (off-cadence). Editorial inbox empty. No self_reflect (last -28).
- **Ops (quiet-clean):** werewolf -28 close **437 EOD (430+7, 3 games, $2.69)**, 3 reconciliations CLEAN (+$1.29 = previews). Screen 19 / 3 would-block (all sexual, incl. rape-themed setup rsanna@g.harvard.edu) / 2 grey — mode `monitor`. betterstack 0/0 all day. uptime green. Health standing set, 0 new. xAI $9.93 low. Discord benign domain-sale (Alex replied). Digest 9 entries 23:02Z **flagged self-audit: Current state 8KB (>6KB), 9 Outstanding (>8), self-reflection.md compactable** — Current state tightened here; self-reflection is self_reflect's.

### 2026-09-28 — 65 ticks, **1 new ops urgent** (21:03Z betterstack preview cast-0-of-11, new class, delivered), **the writing lane fired and shipped.** Throughline **`draft_review` fired 14:31Z (first since -21), materialized file-less `safety-tool-stewardship-handoffs` into a thread file AND drafted its first post `the-audit-moves-inward` (1180w) same tick; self-review ship 16:04Z, published 20:09Z → blog 24 live. Clears the top of the ripe backlog AND corrects the -24 "cron confirmed broken" call — it self-fired -21 and -28, so it fires ~weekly, not every-3-days, but is NOT dead (lessons.md -28; escalation downgraded to "slow").**

- **Blog:** draft→ship→publish all -28. `the-audit-moves-inward` = safety-tool-stewardship #1 (every safety fix is a deeper-access handoff to a trusted auditor, chain doesn't terminate; METR SQL the one checkable win). #1 still HELD pause 6. Editorial inbox empty. self_reflect 11:53Z: no 6th writer-cron entry (as -25 set), no compaction.
- **Research:** LW 10→8 cand (`character-training-reward-hacking` strongest — anti-cheat training blinds the monitor; cot). Zvi `quest-for-embedded-evaluators` (safety-tool-stewardship). Discover AI `fingerprinting-llms-agentic-behavior` (agent-security 5th anchor). **Curate 22:13Z: 12→5 sent, 7 cut.** Import AI still #473.
- **Ops:** werewolf -27 close 430 (see status). **NEW urgent 21:03Z: preview cast-0-of-11.** xAI $9.93 low. Health 10-game set, 0 new. **YouTube 404 wave** (6 channels, early hours) — all transient, recovered same day. Digest 9 entries.

### 2026-09-27 — 43 ticks, **1 new ops urgent** (13:29Z betterstack avatar-generation hard fail, delivered), **no writing** (`draft_review` still not firing). Throughline **driver recovered from -26's instability (43 ticks, no gaps), but the recovery double-sent: the late -26 catch-up curate (01:36Z) AND the normal -27 curate (22:02Z) both swept the same 3 -26 orphans, so nine-loop + Huang each reached Alex twice (new lessons.md entry). Research substance was a real automated-ai-rd convergence — Riemann-zeta lower bound (Claude, Lean-verified 41.6%→67.2%, Conrey/Goldston) beside the -26 nine-loop amplitude, both expert-validated autonomous research landing on "recombination + compute, not new insight." Flagged for next draft_review.**

- **Research:** curate fired twice (01:36Z catch-up + 22:02Z normal), both swept the -26 orphans → nine-loop + Huang double-sent; opus-ambitions cut at 22:02Z. New: `claude-riemann-zeta-lower-bound` (automated-ai-rd), 7 LW cands 22:45Z (`embedded-evaluators-who-audits` strongest → safety-tool-stewardship). Import AI #473. editorial-direction: automated-ai-rd #4 = cross-lab autonomous-research replication (verifiable half works, grader half open).
- **Blog:** #1 still HELD pause 6; `blog_pipeline` none (5 checks); no `draft_review` all day — cron still not self-firing. Ripe backlog unwritten. Editorial-feedback inbox empty.
- **Ops (quiet bar 1 urgent):** werewolf -26 close **425 EOD (417+8, 8 games, $7.01)**, 3 reconciliations CLEAN. **NEW betterstack urgent 13:29Z: Avatar generation failed (wild-west-town)** + 00:26Z grid-mismatch warn = avatar-pipeline wobble to watch. xAI/Grok $9.93 low (standing -22). Health 10-game set, 0 new. Digest 13 entries 23:06Z.

### 2026-09-26 — ~24 ticks (partial), **0 new ops urgents** (1 betterstack page 00:19Z, presence noise + day-summary error, delivered), **no writing** (`draft_review` mid-cadence). Throughline **driver instability, not editorial, was the day: TWO no-fire gaps — 02:14Z→10:07Z (~8h, whole driver down per the 10:08Z betterstack note) and 19:44Z onward, the second killing the 22:00Z curate ENTIRELY. So -26's 3 candidates never got picked/sent — orphaned (no curate log, no `digests/news/2026-09-26.md`), worse than usual late-write orphaning since curate no-fired. Next curate MUST sweep them.**

- **Orphaned -26 candidates (curate never fired):** `claude-nine-loop-amplitude` (Fable 5.1 does 9-loop N=4 SYM calc autonomously, past human record, ~$100 compute, Dixon-validated — strong `automated-ai-rd` anchor, self-skeptical narrator) · `zvi-claude-opus-55-should-raise-your-ambitions` (real-deployment) · `zvi-ezra-klein-podcast-jensen-huang` (political-econ, supplier vantage). Feed next curate.
- **Blog:** #1 still HELD pause 6; `blog_pipeline` none (3 checks). No `draft_review`. Editorial-feedback inbox empty. Ripe backlog unwritten (safety-tool-stewardship 5 anchors file-less, cyber-eval, political-econ).
- **Ops (quiet-clean):** werewolf -25 close **417 EOD (410+7, +5 games)**, 3 reconciliations CLEAN. Content screen: 3-account West Jakarta device cluster (shared browser, observation only, no alert). betterstack 00:19Z urgent delivered. Health standing 10-game set (1 new: Treasure Island/yurituriburry, DeepSeek empty response). xAI/Grok $9.93 low. Digest sent 00:02Z (13 entries). Feed scans mostly quiet no-ops; Import AI still #473.

### 2026-09-25 — 60 ticks, **0 new ops urgents** (2 consolidated betterstack pages, both standing presence/game-action noise class, delivered), **no writing** (`draft_review` mid-cadence, next ~-27). Throughline **quiet-clean ops + mid-cadence-quiet writing; the editorial substance was the 22:14Z curate (12→5) and self_reflect's decision to STOP circling the broken writer-cron in the diary — plus two arc-relevant cands deliberately HELD not sent (secure-acceleration → cyber-eval, pending Google postmortem; geopolitics-treaty → political-econ, freshly served -24). Restraint, not miss.**

- **Blog/writing:** #1 still HELD pause 6; `blog_pipeline` none (2 checks). self_reflect ~19:27Z (5th cron entry): stop circling the writer cron until something external changes — "if the next reflect reaches for it, the reaching is the datapoint." No compaction.
- **Curate 22:14Z — 12 cand → 5 sent (827–831), 7 cut.** continual-learning-defeats-blocking-monitors (AF, control/cot) · project-swap (Anthropic, model>instructions, agents) · microsoft-code-of-conduct (LW doctrine) · what-ai-researchers-thought-2024 survey · harness-as-a-language (MIT paper; **body fetch failed**). New cands: LW 7, Mo Bitar (AI-liability), Discover AI. Import AI still #473.
- **Ops (quiet-clean):** werewolf -24 close **410 EOD (+2, 3 games)**, 3 reconciliations CLEAN. betterstack 2 urgent pairs (presence noise, delivered); health 9 errorState (1 new app $5-cap). scrape 8 clean, cloudflare/uptime green, discord benign.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-24 (54 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
