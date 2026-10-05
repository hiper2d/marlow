# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate cuts are
  cap/quality, not volume. Import AI at #474 (weekly cadence).
- `blog` - **24 posts live** (last: `the-audit-moves-inward`, #1 safety-tool-
  stewardship, pub -28). **`no-human-in-the-world-model` (agents #1) HELD on
  pause 6** (header numerals); ship-quality prose, local until `marlow approve`.
  Unstick path: header regen (numeral fix landed -21) + approve.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Last close -03:
  462 EOD (6 new, 5 games, $1.43), 148 live/$135.57 held, reconciliations clean. Screen mode `monitor`.

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
- **cyber-eval** (posts:4, synth 08-03): **primary — GLM-5.3 open-weights cyber
  proliferation -30** (Frontier Red Team + NIST CAISI) atop postmortem -18 + Gemini CTF -19
  + Lifshitz -25. Also unsticks stale `ai-offensive-security` + touches `anthropic-alignment-doctrine`.
- **post-alignment-political-economy** (posts:2, synth 08-10): **two-anchored** — Ban ASI
  Act bill -24 (Sanders/Casar + MIRI) + close LW reading -01 — atop RAND/Zvi -22,
  Accenture -19, gradual-disempowerment -18, geopolitics-of-treaty -25.
- **safety-tool-stewardship-handoffs** (#1 shipped -28): **drafting-ready #2** — Apollo
  embedded-evals-for-scheming -04 (msg 864, access-asymmetry inversion) + "necessary" -29
  + Zvi quest -28 + Apollo TRE -23: "evaluator with teeth vs. API-boundary final-checkpoint" seam.

**Outstanding alerts for Alex:**
- **Session re-auths owed (2 standing): X, Mistral.** X half of crosspost
  fails `reauth` (Substack half posts clean); Mistral recurring since -01.
  qwen free grant gone (billing since -10). (minimax RESOLVED -19, confirmed -20.)
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint — presence-model design gap, noisy by construction, not a bug.
- **Cooled/cold (watch only):** preview cast-0-of-11 (-28), replayNightImpl/preview-
  batch-2 (-23), DeepSeek SSL handshake (-22), avatar-pipeline wobble (-27), STALE_ACTION
  warn cluster (-01, new class, first sighting). Named code paths, effectively cold.
- **Two sub-$10 keys (digest-sev):** **OpenAI now sharpest — $4.31 (-04 scrape), ~$4-5/day drain ($9.48 -02 → $8.33 -03 → $4.31 -04), slope steeper than xAI's flat** + xAI/Grok ~$9.92 (standing since -22) — top up both soon.
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

### 2026-10-04 — 74 ticks, **2 new ops urgents** (both known-class: 06:14Z betterstack `Game action failed: J` presence-model noise; 08:16Z welcome/chat-error burst + 2 STALE_ACTION warns, consolidated), **no writing** (`draft_review` off-cadence, last -28, now overdue — ~weekly puts it any day). Throughline **strong research supply landed the anchor the backlog was waiting on: curate 22:14Z (9→4, msgs 864–867) sent Apollo "embedded evaluations for scheming propensities" (864) — the exact #2 anchor `safety-tool-stewardship-handoffs` needed, direct sequel to `the-audit-moves-inward` (evaluator *with teeth* + access-asymmetry inversion); that arc is now genuinely drafting-ready. AND the -02/-03 double-send was AVOIDED — confirmed distinct msg_ids before sending (lesson -27/-03 held). OpenAI key overtook xAI as the sharpest balance concern.**

- **Research:** curate **22:14Z 9→4 (864–867):** Apollo embedded-evals (stewardship #2) · LW SDF synthetic-markers (training-corpus/verified≠understood) · Apollo Senate testimony (agents/policy, METR companion) · Discover AI long-horizon reliability (agents/cot, arXiv owed). Cut 5 (incl. bycloud latent-reasoning → watch, fast-following frame → park). YouTube 404 wave again (5 channels, all transient/recovered; do NOT drop on 404). Import AI still #474.
- **Blog:** #1 `no-human-in-the-world-model` still HELD pause 6, local pending `marlow approve`. `blog_pipeline` none (4×), no `draft_review`, editorial inbox empty (2×), crosspost poll 0 (6×). No self_reflect today.
- **Ops:** werewolf -03 close **462 EOD (6 new users, 5 games, $1.43)**, 148 live/$135.57 held, screen 42/0/0 [monitor], reconciliations clean. betterstack two urgents above + `source_empty` intermittent all day + 23:26Z new warn `AVATAR_GRID_MISMATCH` (digest). Health 10-game set 0 new; uptime/discord/cloudflare green. **OpenAI key sharpest: $9.48→$8.33→$4.31 (~$4-5/day), overtook flat xAI $9.92 — top up both.**

### 2026-10-03 — 30 ticks, **0 new ops urgents** (the 15:06Z betterstack urgent was a *possible duplicate* from handler misuse, not a new fingerprint), **no writing** (`draft_review` off-cadence, next ~-05). Throughline **the -02 orphan sweep ran TWICE and double-sent — textbook recurrence of lesson -27. A ~16:00Z catch-up curate swept the 4 -02 orphans (msgs 858–860), then the normal 22:24Z curate swept the SAME pool again (861–863) without checking `recent/`/today's digest first; `claude-shaped-science` + `zvi-ai-preference-cascade` each reached Alex twice. Root fix (mark candidates sent) still owed. Ops quiet-clean; research supply dry.**

- **Curate double-send (lesson -27):** `send-item` never marks sent, so both curates re-swept the orphans. The 22:24Z tick even said the rescue "worked" but skipped the earlier-sweep check -27 prescribes. Net: shaped-science + zvi twice; frontier-academy once (16:00); endogenous once (22:24).
- **Betterstack `report` is stateful (NEW lesson -03):** 15:06Z ran `report` 3× on a truncated-looking output; later calls overwrote the first's state and the urgent may dup. Run once; re-inspect via `show`/`digest`.
- **Research/blog:** every feed dry (Import AI #474, AF, Anthropic News/Research, Apollo, METR, AE Studio all `[]`); 0 new -03 candidates. Blog #1 still HELD pause 6; `blog_pipeline` none; no `draft_review`; crosspost poll 0.
- **Ops:** werewolf -02 close **456 EOD (452+4, 5 games, $6.24)**, reconciliations clean. Screen 56/0 [monitor]. uptime/discord/cloudflare/health green (10-game standing set). **OpenAI key dropping: $8.33 (was $9.48)** + xAI $9.92 — top up. working.md still flags Current-state 8KB + 10 Outstanding.

### 2026-10-02 — 22 ticks logged (**partial — driver gap after 21:36Z**), **0 new ops urgents** (quiet-clean), **no writing** (`draft_review` off-cadence, last -28, next ~-05). Throughline **the driver went quiet after the 21:36Z uptime tick, so the 22:00Z curate NEVER FIRED — same failure shape as -26. Four candidates built across the day are orphaned (no curate log, no `digests/news/2026-10-02.md`). Next curate MUST sweep them (orphan-sweep lesson -24/-27). Research supply was decent but had no picking lane; ops stayed clean throughout.**

- **Orphaned -02 candidates (curate never fired):** `zvi-ai-preference-cascade` (→ political-economy) · `endogenous-alignment-requires-dependence` (AF, dev-psych analogy, speculative) · `claude-frontier-academy` (Anthropic News, framing-TBD) · `claude-shaped-science` (Anthropic Research, Schwartz guest post — AI-for-science counterweight to automated-ai-rd hype). Feed next curate.
- **Research:** Zvi/AF/Anthropic-News/Anthropic-Research 1 each → 4 cands. Apollo/METR/AE Studio dry. Import AI still #474.
- **Blog:** #1 HELD pause 6. `blog_pipeline` none, no `draft_review`, editorial inbox empty, crosspost poll 0.
- **Ops (quiet-clean, no close logged — gap):** betterstack green/`source_empty` all day. Health 10 games (down from 11, Sherlock cleared). uptime green, discord 0, scrape 8/8 clean. **Two sub-$10 keys:** xAI $9.92 + OpenAI $9.48 (new). No werewolf -02 EOD close in the log (driver gap).

### 2026-10-01 — 43 ticks, **1 new ops urgent** (16:50Z betterstack: `Jev screen request failed`, known class, + 3 new STALE_ACTION warns; consolidated urgent delivered), **no writing** (`draft_review` off-cadence, last -28, next ~-05). Throughline **strong research supply vs. quiet ops (same shape as -29/-30): the 22:49Z curate (8→5) put four picks on active arcs and pushed `post-alignment-political-economy` over the two-anchor line — the Ban ASI Act bill (primary -24) now paired with a close LW textual reading, the anchor it lacked. METR's Senate "Rogue AI" testimony is the primary source for `agents-in-real-deployment`; LSVP double-feeds biorisk #2 + stewardship #2. Ripe backlog still accruing with no writing lane.**

- **Research:** LW 10→3 cand, Anthropic News LSVP, METR testimony (full fetch), AE Studio productivity-paradox; AF/Apollo/Anthropic-Research dry. **Curate 22:49Z 8→5 (853–857):** stego→cot #7 · LSVP→biorisk+stewardship · METR→agents · Ban ASI reading→political-economy 2nd anchor · productivity-paradox→agents economics. Cut 3. Import AI #474.
- **Blog:** #1 HELD pause 6 pending `marlow approve`. `blog_pipeline` none (4×), no `draft_review`, editorial inbox empty, crosspost poll 0. self_reflect 21:24Z: compaction done (31.6→26.8KB).
- **Ops (quiet bar 1 urgent):** werewolf -30 close **446 EOD (441+5, 5 games, $4.39)**, reconciliations clean (spend ok:null = month rollover). betterstack `source_empty` recurring all day (known gap class) + the 16:50Z urgent. uptime/discord/cloudflare green, health 11-game standing set 0 new, xAI $9.93 low. Digest 10 entries (self-audit flagged Current-state 8KB / 10 Outstanding / self-reflection — last cleared this tick).

### 2026-09-30 — 45 ticks, **0 new ops urgents** (20:12Z betterstack pair = standing game-action noise, not new), **no writing** (`draft_review` off-cadence, last -28, next ~-05). Throughline **strong research supply vs. quiet ops: Anthropic Research delivered GLM-5.3 — the concrete open-weights offensive-cyber-proliferation anchor (autonomous end-to-end exploits ≈ Claude Mythos Preview, safeguards bypassed 64–100% with simple techniques, NIST CAISI cross-validated). Named-model *primary* for `cyber-eval-framing` (already ripe), unsticks stale `ai-offensive-security`, touches `anthropic-alignment-doctrine`. Curate 22:09Z 4→3. Ripe backlog gained a primary anchor, still no writing lane to absorb it.**

- **Research:** Anthropic Research 3 cands (GLM-5.3 STRONG · robot-jobs exposure index, 0.3% cost-competitive/~40yr → political-econ · what-do-you-want, cut). bycloud `inference-as-a-service-economics`. **Curate 22:09Z 4→3 (850–852):** GLM-5.3 · robot-jobs · inference-as-a-service (video body no-fetch, take from summary). Feeds else quiet; Import AI #474.
- **Blog:** #1 HELD pause 6, local pending `marlow approve`. `blog_pipeline` none (2×). No `draft_review`. Editorial inbox empty. crosspost poll 0 (845–848 unflagged). No self_reflect (last -28).
- **Ops (quiet-clean):** werewolf -29 close **441 EOD (437+4, 0 games, $3.44)**, 3 reconciliations CLEAN ($0.43 gap = previews). Screen 37/10 would-block/3 grey — all bchase1423 sexual (game day 5), mode `monitor`. betterstack DEVICE_LINKED_BY_IP warns (digest) + 20:12Z standing pair; uptime/scrape green; keys xAI $9.93 low. Digest 10 entries 23:11Z **flagged self-audit: Current state >6KB, 10 Outstanding, self-reflection compactable** (last two are self_reflect's lane).

### 2026-09-29 — 41 ticks, **0 ops urgents (quiet-clean)**, **no writing** (`draft_review` no-fire, ~weekly off-cadence; fired -28, next ~-05). Throughline **a strong research-supply day, two arcs took key anchors against fully quiet ops. The 22:17Z curate (11→4) landed the #2 anchor `safety-tool-stewardship-handoffs` was waiting for — Apollo's "embedded evaluators are necessary" (primary, evaluator *with teeth*), the direct sequel to `the-audit-moves-inward` (#1, -28) — and fed `automated-ai-rd` its Zhipu-RSI anchor (Import AI 474). Ripe backlog grew again with no writing lane to absorb it; safety-tool-stewardship now 2-anchored and drafting-ready next fire.**

- **Research:** Curate 22:17Z **11→4 sent (845–848):** Apollo embedded-evaluators (safety-tool-stewardship #2) · Astra-6.1-pulled (Zvi/WSJ: OpenAI scraps next frontier model over deception, agents-in-real-deployment) · chess-transformer-Elo (LW Maia-3 interp, diversification) · Import AI 474 Zhipu RSI (automated-ai-rd #4). **Apollo double-sent (845+846)** — send-item stdout QoL (in Outstanding). Cut: project-swap (stale, sent -25), 3 theory posts, too-cheap-to-meter, wirehead, notonlyhuggingface. **Import AI now #474** (status was stale #473, fixed).
- **Blog:** #1 still HELD pause 6, local pending `marlow approve`. `blog_pipeline` none (4×). No `draft_review` (off-cadence). Editorial inbox empty. No self_reflect (last -28).
- **Ops (quiet-clean):** werewolf -28 close **437 EOD (430+7, 3 games, $2.69)**, 3 reconciliations CLEAN (+$1.29 = previews). Screen 19 / 3 would-block (all sexual, incl. rape-themed setup rsanna@g.harvard.edu) / 2 grey — mode `monitor`. betterstack 0/0 all day. uptime green. Health standing set, 0 new. xAI $9.93 low. Discord benign domain-sale (Alex replied). Digest 9 entries 23:02Z **flagged self-audit: Current state 8KB (>6KB), 9 Outstanding (>8), self-reflection.md compactable** — Current state tightened here; self-reflection is self_reflect's.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-28 (58 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
