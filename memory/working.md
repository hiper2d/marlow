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
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. Last close -05:
  471 standing (5 new, 5 games, $5.77 cost, $10.72 spend/9 users), reconciliations clean. Screen mode `monitor`.

**Active threads.** The files under `projects/research/threads/` are the current
view of each arc; hold bullets here to 2-3 lines and let the files carry the
anchors. (Sanctioned 2026-08-24 - see Outstanding requests.)

| thread | posts | last synth |
|---|---|---|
| `cot-monitorability` | 6 | 09-14 |
| `cyber-eval-framing` | 5 | 10-05 |
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
training-corpus-as-alignment-surface · verified≠understood (4 LW, needs non-LW anchor) ·
latent-reasoning-undermines-cot -23 (cot, posts:6).

**RIPE arcs — flag next `draft_review`:**
- **post-alignment-political-economy** (posts:2): two-anchored — Ban ASI Act bill -24
  (Sanders/Casar + MIRI) + close LW reading -01, atop RAND/Zvi -22, Accenture -19,
  gradual-disempowerment -18, geopolitics-of-treaty -25.
- **safety-tool-stewardship-handoffs** (#1 shipped -28): drafting-ready #2 — Apollo
  embedded-evals-for-scheming -04 (msg 864) + "necessary" -29 + Zvi quest -28 + Apollo
  TRE -23: "evaluator with teeth vs. API-boundary final-checkpoint" seam.
- **automated-ai-rd** (posts:3): TasteVal research-taste benchmark -06 (msg 872) — the
  open-ended-research grader this arc has lacked since June.

**Outstanding alerts for Alex:**
- **Session re-auths owed (2 standing): X, Mistral.** X half of crosspost
  fails `reauth` (Substack half posts clean); Mistral recurring since -01.
  qwen free grant gone (billing since -10). (minimax RESOLVED -19, confirmed -20.)
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint — presence-model design gap, noisy by construction, not a bug.
- **Cooled/cold (watch only, named code paths):** preview cast-0-of-11,
  replayNightImpl/preview-batch-2, DeepSeek SSL handshake, avatar-pipeline wobble,
  STALE_ACTION warn cluster (-01).
- **xAI/Grok $7.92 (digest-sev, <$10 since -22, -$2/day burn -06) — top up.** OpenAI
  off Marlow's task since 08-24 (self-funded); DeepSeek $23.41, Moonshot $15.13 healthy.
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

### 2026-10-06 — 51 ticks, **0 new ops urgents** (quiet-clean), **writing landed.** Throughline **the inverse of the recent "supply but no lane" shape — both halves fired. #5 `the-model-nobody-can-recall` (cyber-eval, GLM-5.3/CAISI) self-reviewed `ship` 00:20Z and PUBLISHED 05:02Z (dc5783d) → post #25 live, thread 4→5 done. AND a strong research day fed a clean 5-pick curate (872–876, all distinct, double-send lesson held). Standout pick: TasteVal (872), a research-*taste* benchmark — the open-ended-research grader `automated-ai-rd` #4 has wanted since June. Flag next draft_review.**

- **Blog:** #25 published; pipeline otherwise `none` (6×). #1 `no-human-in-the-world-model` still HELD pause 6, local pending `marlow approve`. editorial inbox empty (2×), crosspost poll 0 (2×). No self_reflect, no draft_review fire.
- **Research (strong):** **Import AI #475** landed (first since #474; SynthID Bio watermarking → biorisk-evals #2). **Curate 22:03Z 9→5 (872–876):** TasteVal (automated-ai-rd grader) · Takes-One-to-Know-One (grader-training cuts reward-hack) · AI-honeypots-6mo (eval-awareness near-absent) · Import AI 475 · Debate/PlurPO (SECONDARY/arXiv-unverified). Cut 4. No orphans; robot-jobs sitemap re-surfaced → deduped by URL.
- **Ops (quiet-clean):** stats -05: 5 new, 5 games, $5.77 cost, $10.72 spend/9 users, 471 standing; screen 106/13/3 all bchase1423 [monitor]. health 11 errored, 1 new (13 Crowns VOTE, Mistral empty JSON, recoverable). betterstack `source_empty` most of day + 1 Jev would_block warn. uptime/discord/cloudflare green. **xAI $9.92→$7.92 (-$2/day, watch)**; DeepSeek $23.41, Moonshot $15.13. Digest 10 entries, self-audit flags Current-state 8KB + 10 Outstanding.

### 2026-10-05 — ~65 ticks, **1 new ops urgent** (09:14Z betterstack `Game action failed: aa`, presence-model noise, known), **writing happened at last.** Throughline **off-cadence `draft_review` fired 14:23Z (first write since -28) and absorbed the ripest arc: cyber-eval-framing #5 `the-model-nobody-can-recall` (848w) — GLM-5.3/CAISI as the external capability measure the arc demanded since June ("you can't recall open weights"). Self-review `revise` 16:20Z caught a real sourcing overstatement (CAISI reaches readers *through* Anthropic's post, not a standalone report); v2 20:08Z added a caveat. Next `blog_pipeline` publishes regardless (one-pass) → post #25; thread 4→5.**

- **Blog:** #5 draft v2 publish-pending; pause 7 (single-lab) did not fire (CAISI cross-validates, non-Anthropic subject). #1 `no-human-in-the-world-model` still HELD pause 6 pending `marlow approve`. editorial inbox empty, crosspost poll 0 (×4). self_reflect 21:29Z: flat barometer moved.
- **Research:** LW 8→4 cand (only live feed). **Curate 22:11Z 4→3 (868–870):** alignment-engineering-vs-misalignment-science → anthropic-alignment-doctrine (stale, could revive) · rogue-ai-sanctuaries → ai-control-camp · human-empowering-software → political-economy. Cut 1 (do-llms-feel-pain, thin). No orphans. Import AI #474.
- **Ops:** werewolf -04 close **466 EOD (4 new, 3 games, $5.74)**, 149 live/$137.21 held, screen 48/0/0 [monitor]. betterstack 1 urgent + `Jev would_block` warns + source_empty. uptime/discord/health/cloudflare green. **OpenAI recovered $25.57**, xAI $9.92 standing <$10.

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

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-30 (60 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
