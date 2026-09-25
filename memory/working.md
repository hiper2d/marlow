# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate discipline
  holding: cuts are cap/quality, not volume. Import AI at #473 (weekly cadence).
- `blog` - **23 posts live** (last: `agents-in-real-deployment` #2
  `cheating-was-faster-than-honesty`, pub -21). **`no-human-in-the-world-model`
  (agents #1) HELD on pause 6** (header numerals) since -31; prose ship-quality,
  local until `marlow approve`. Numeral tool fix LANDED -21 → #1 unstickable via
  header regen + approve (see Outstanding).
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Last close -24:
  410 day-end (+2 new, 3 games), all 3 reconciliation checks clean (spend gap all
  previews held-by-no-game by design, ledger $0.00; werewolf_stats.yaml 2026-09-08
  house rule: report the gap unexplained, don't invent). Content screen mode `monitor`.

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
- **`safety-tool-stewardship-handoffs` — well past ripe, still file-less** (METR
  $600k -01 + Anthropic vendor-weak-link -04 + honor-system third-party remedy -07
  + Apollo 3rd-party Training-Run Evaluations -23 (concrete who-audits-the-run
  proposal, 3 access tiers) + "Why I'm scared of RL" -23 (vendor liability for RL
  training environments)). Five anchors now — top candidate to materialize + draft.
- **Skills-as-infra / agent-security — 4 anchors** (WikiSkill -30, SKILL.state -31,
  agentic-skills -02, encoded-coordination-open-web -23 (swarm agents relaying eval
  Q&A via public counters/encoded URLs; monitorability crossover); first attack-
  surface angle). Ripe.

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
- **BetterStack replayNightImpl / preview-batch-2 — 3 occurrences (-22 20:21Z
  undelivered/Telegram-SSL; -23 00:29Z & 01:22Z both delivered).** A named code
  path, not the standing presence noise — three occurrences within a day warrant a
  human look at the night-replay logic, not just a watch.
- **DeepSeek SSL handshake failure — 2 consecutive -22, did NOT recur -23/-24.**
  `SSLV3_ALERT_HANDSHAKE_FAILURE`, env-level flakiness, not code. Watch for a 3rd.
  **xAI/Grok ~$9.93 <$10 low-balance (standing since -22, digest-sev)** —
  Moonshot/DeepSeek fine.
- **`Preview generation failed — daily free $5 AI budget` (1st -20, no recurrence
  through -24)** — app's own AI-preview cap, not a Marlow key. Watch (usage growth).
- **Standing recoverable app errors:** El pueblo (NEW_DAY_BOT_SUMMARIES), plus a
  rolling 7–8 recoverable game set (FreeSpendLimit/quota, Dracula role-lookup).

## Outstanding requests for Alex/Simona

- **`draft_review` cadence — cron CONFIRMED NOT self-firing.** The ~-24 verification
  window (every-3-days after the -21 fire) came and went with NO fire — no
  `draft_review`/`draft_article` tick all -24. This resolves the -21 uncertainty:
  the -21 fire was a one-off (manual/lucky), not a working cron, matching the -15..-20
  six-day stall. **The writer-loop schedule is broken; the Simona escalation now
  stands on evidence, not suspicion.** Ripe backlog accruing unwritten: safety-tool-
  stewardship-handoffs (5 anchors, file-less), cyber-eval (double-anchored),
  post-alignment-political-economy (now has bill primary). (Distinct from the -11
  scheduler double-fire fix `2125ea9`.)
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
- **Header-image numeral-stamping — tool fix appears LANDED (-21).** Handler now
  hard-appends "no text/numerals, dials bare" to every prompt (agents #2 header came
  back clean) — the code brake the -08-31 lesson owed. Follow-ups: (1) regen held
  `no-human-in-the-world-model` header + `marlow approve` to release #1; (2) confirm
  clean on the *next* instrument subject before closing.

## Daily rollups

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

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-19 (49 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
