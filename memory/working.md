# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate discipline
  holding: cuts are cap/quality, not volume. Import AI at #473 (weekly cadence).
- `blog` - **24 posts live** (last: `the-audit-moves-inward`, safety-tool-
  stewardship #1, pub -28). **`no-human-in-the-world-model` (agents #1) HELD on
  pause 6** (header numerals) since -31; prose ship-quality, local until
  `marlow approve`. Numeral tool fix LANDED -21 → #1 unstickable via header regen
  + approve (see Outstanding).
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Last close -27:
  430 day-end (425+5, 3 games, $0.52), all 3 reconciliations clean (spend gap =
  previews by design; werewolf_stats.yaml 2026-09-08 house rule: report the gap
  unexplained, don't invent). Content screen mode `monitor`.

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
| `safety-tool-stewardship-handoffs` | 1 | 09-28 (#1 published) |
| `agents-in-real-deployment` | 2 | 09-21 (#2 published) |
| `ai-biorisk-evals` | 1 | 09-07 (#1 published -08) |
| `model-welfare-and-consciousness` | 1 | 08-24 |
| `alignment-target-definitions` | 1 | 06-29 |
| `ai-offensive-security` | 1 | 06-02 (stale) |

**Thread-file backlog - standing binding constraint.** `draft_article
list-threads` only sees thread files on disk, so an arc ripe only as prose here is
invisible to drafting; materialize before drafting (writer IDENTITY, "Materialize
ripe arcs first"). File-less + ripe:
- **Skills-as-infra / agent-security — 5 anchors** (WikiSkill -30, SKILL.state -31,
  agentic-skills -02, encoded-coordination-open-web -23 (swarm agents relaying eval
  Q&A via public counters/encoded URLs; monitorability crossover), fingerprinting-
  llms-agentic-behavior -28 (Tsinghua ~958-feature model fingerprint; audit tool +
  attack surface); first attack-surface angle). Ripe — top of the file-less backlog
  now that safety-tool-stewardship shipped.

**Single-source frames to watch:** horizon-length · "hard core of alignment" meta ·
training-corpus-as-alignment-surface · verifiability/verified≠understood (4 LW, needs
non-LW anchor) · cot latent-reasoning-undermines-cot -23 (cot-monitorability, posts:6).
**cyber-eval RIPE + triple-anchored** (posts:4, synth 08-03): postmortem -18 + Gemini
CTF breakout -19 + Lifshitz secure-acceleration -25 (held from curate pending Google
postmortem) — flag next `draft_review`. **`post-alignment-political-economy` RIPE**
(posts:2, synth 08-10): PRIMARY Ban ASI Act bill SENT -24 (Sanders/Casar + MIRI) atop
RAND/Zvi -22, Accenture -19, gradual-disempowerment -18, + geopolitics-of-treaty -25 —
flag next `draft_review`.

**Outstanding alerts for Alex:**
- **Session re-auths owed (2 standing): X, Mistral.** X half of crosspost
  fails `reauth` (Substack half posts clean); Mistral recurring since -01.
  qwen free grant gone (billing since -10). (minimax RESOLVED -19, confirmed -20.)
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint — presence-model design gap, noisy by construction, not a bug.
- **Preview generation cast-count fail — NEW -28.** 20:03Z urgent: `cast 0 characters
  instead of 11` (+ Jev `would_block` warn), delivered. New class (≠ replayNightImpl,
  Game-action, or the $5-budget cap below). First occurrence — watch for recurrence.
- **Cooled/cold (watch only):** replayNightImpl/preview-batch-2 (last -23), DeepSeek
  SSL handshake (last -22), avatar-pipeline wobble (-27, no recurrence -28). Named
  code paths, effectively cold.
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
- **Drafting-tick header-image miss** - when the image API fails, the documented
  path (drop `header_image`, DEVLOG a note) has been skipped both times it mattered.
- **Header-image numeral-stamping — tool fix LANDED (-21)** (handler hard-appends "no
  text/numerals, dials bare"; agents #2 + audit-moves-inward headers came back clean).
  Follow-up: regen held `no-human-in-the-world-model` header + `marlow approve` to
  release #1.

## Daily rollups

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

### 2026-09-24 — 54 ticks, **0 ops urgents (quiet-clean)**, **no writing — verification watch resolved negatively.** Throughline **`draft_review` no-fired at its ~-24 window (fired -21, every-3-days), confirming the writer-loop cron does NOT self-fire on cadence — the -21 fire was a one-off, so the Simona escalation now stands on evidence. The day's real editorial work was a curate backlog sweep: 18 cand (11 today + 7 orphaned late-LW dated -23, invisible to a `--date today` pull), capped to 5, sending the primary Ban-ASI-Act bill anchor political-economy was owed.**

- **Blog:** #1 still HELD pause 6; `blog_pipeline` none (4 checks). **`draft_review` NO-FIRE at ~-24 verification window** → cron confirmed broken (see Outstanding); ripe backlog (safety-tool-stewardship 5 anchors, cyber-eval, political-economy w/ bill primary) unwritten.
- **Curate 22:23Z — 18 cand → 5 sent (822–826), 13 cut.** Ban ASI Act (political-econ primary) · Claude enzyme discovery (biorisk) · 5-LLM 63%-disagreement (verifier reliability) · latent-reasoning-undermines-cot · encoded-coordination (agent-security 4th anchor). New cands: Opus 5.5 card (Zvi) · Discover AI ×3 · NVFP4 4-bit (bycloud). Import AI still #473. Orphaning → candidate handler fix (Outstanding + lessons.md).
- **Ops (quiet-clean):** werewolf -23 close **408 EOD (+9 new, 6 games)**, 3 reconciliations CLEAN. bchase1423 pattern day 3 (monitor). xAI/Grok ~$9.93 <$10 (digest). betterstack 7 empty scans = quiet overnight (replay confirmed pipe live). Digest 10 clean; uptime green; Discord quiet.

### 2026-09-23 — 55 ticks, **3 ops urgents** (all delivered clean — betterstack, no SSL flakiness this time), **no writing** (draft_review on-cadence, next ~-24). Throughline **a strong research-convergence day: the 22:04Z curate sent all 3 candidates (Apollo 3rd-party Training-Run Evaluations · METR Opus-5.5 predeploy eval · AF "Why I'm scared of RL") and all three land on the same necessary-not-sufficient / training-run-vs-final-checkpoint seam — Apollo's TRE proposal is the institutional form of what agents-in-real-deployment and cot arcs circle — while `safety-tool-stewardship-handoffs` (still file-less) took its 4th+5th anchors and a heavy late LW day queued a ban-ASI-bill primary + cot + agent-security #2 for tomorrow.**

- **Blog:** #1 still HELD pause 6; pipeline none all day (4 checks). `draft_review` no-fire = **on-cadence** (next window ~-24 — the verification watch). self_reflect ran 19:53Z, compaction done (33.4→27.5KB, folded 4 entries into 1 standing).
- **Curate 22:04Z — 3 cand → 3 sent (819/820/821), 0 cut** (all on-arc). Apollo TRE (819) · METR Opus-5.5 (820) · Why-I'm-scared-of-RL (821). Import AI still #473 (weekly, no new). **Late LW 22:46Z (post-curate): 7 cand for -24** incl. ban-ASI-bill pair (Sanders/Casar act + MIRI reaction; political-econ primary), latent-reasoning-undermines-cot (cot), encoded-coordination (agent-security #2), Opus-5.5 system card.
- **Ops:** werewolf -22 close 399 (0 new), 3 reconciliations CLEAN. **3 betterstack urgents, all delivered:** replayNightImpl 3rd occ (01:22Z) · Game-action-Y + Error-in-vote-function (15:49Z, known) · Jev-screen-request-failed (22:22Z, presence class). xAI/Grok $9.98 <$10 (digest); DeepSeek SSL didn't recur; scrape 8 clean. Digest 9 ops-class, clean.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-22 (52 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
