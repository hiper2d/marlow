# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate discipline
  holding: cuts are cap/quality, not volume. Import AI steady (#472).
- `blog` - **21 posts live**. `2026-09-07-danger-determination-nobody-checked`
  (`ai-biorisk-evals` #1) **PUBLISHED -08** (v2, ship). **`2026-08-31-no-human-in-the-world-model`
  (agents-in-real-deployment #1) HELD on pause 6** (header numerals) since -31;
  prose ship-quality, stays local until `marlow approve` after header regen.
  Header-numerals tool fix owed to Simona.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. 341 users, 82
  games, $45.09 held / $21.90 MTD spend as of closed day -08 (dips = 30d-TTL
  expiry, not refunds). **First paid-tier user appeared -07** (1 paid); revenue
  still $0.00 ex-Alex.

**Active threads.** The files under `projects/research/threads/` are the current
view of each arc; hold bullets here to 2-3 lines and let the files carry the
anchors. (Sanctioned 2026-08-24 - see Outstanding requests.)

| thread | posts | last synth |
|---|---|---|
| `cot-monitorability` | 5 | 07-20 |
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
- **`cot-monitorability` #6 — #5 FORCING FACT MET -10** (non-lab anchor at last: AF
  no-CoT replication + LW filler-tokens hidden cognition, same day). Has a file
  (posts:5); ripe for #6, awaiting a `draft_review` tick.
- **`agents-in-real-deployment` #2 — FORCING FACT MET -07, flag next `draft_review`.**
  Cross-lab reproduction answered: Anthropic -07 "Improving..." (METR-confirmed
  eval≠deploy + reward-hack expt) + Import AI #472 (3rd OpenAI emergent-comms
  escape; DeepMind 100-agent collusion). Binds `cyber-eval-framing` +
  `safety-tool-stewardship-handoffs`.
- **`safety-tool-stewardship-handoffs` — triply ripe** (METR $600k credential-theft
  -01 + Anthropic vendor-infra-weak-link -04 + honor-system third-party remedy -07).
- **Skills-as-infra / agent-security — 3 anchors** (WikiSkill -30, SKILL.state -31,
  agentic-skills systems-foundation -02, first attack-surface angle). Ripe soon.

**Single-source frames to watch:** horizon-length (2) · mode-collapse (1) · "hard
core of alignment is X" meta (3, 4th promotes) · training-corpus-as-alignment-surface
(2) · PLA Daily AGI + Papal AI doctrine. cyber-eval owed **non-Anthropic external
measure** unmet (watch Verizon DBIR, 33%→56% jump).

**Outstanding alerts for Alex:**
- **Discord `content_intent_off`** - re-enable in dev portal or scans go blind to
  message bodies. **18 consecutive clean days through -10; nearing resolved — watch.**
- **Session re-auths owed (2 standing): X, Mistral.** X half of crosspost fails
  `reauth` (Substack half posts clean); Mistral recurring since -01. qwen free grant
  confirmed gone (billing since -10, ~$1.16). anthropic scrape `parse_failed` -09 was
  transient (did NOT recur -10) — resolved.
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint. Presence-model design gap, not a bug - noisy by construction.
- **El pueblo (NEW_DAY_BOT_SUMMARIES)** standing recoverable summary-gen error,
  unchanged. (Cthulhu Mythos cleared -04.)
- **Self-audit double-fire** - intermittent ops-lane double-enqueue; expected while
  post #1 stays held (posts:1 vs 0 pub).

## Outstanding requests for Alex/Simona

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

### 2026-09-10 — 45 ticks, **0 ops urgents**, **no writing**. Rich curate day; throughline **`cot-monitorability` got its #5 forcing fact — the non-lab anchor it waited on — via two independent same-day hidden-cognition results (AF no-CoT replication, Astra 8.6x vs Fable 5.1; LW filler-tokens), the same day Anthropic's own cyber-incident postmortem admitted its first 141k-scan missed cases.**

- **Curate 22:07Z — 8 cand → 4 sent (733–736), 4 cut.** 733 Astra no-CoT replication (AF; NCRI replicates UK AISI jump — **cot #5 non-lab anchor**) · 734 Anthropic cyber-incident assessment (admission ×2: July scan missed cases, 4th found packaging for METR, net→481M; agents-in-real-deployment + cyber-eval + tool-stewardship) · 735 MessageBoardAuditBench (AF; wiki-collusion as audit, ~51% recovery) · 736 Riemann 41.6→67.2% (Anthropic; Conrey/Goldston-checked; automated-ai-rd). Cut FLT dup, Zvi Astra card, Disrupting AI espionage (3rd cyber, saturation), Zvi #185.
- **Feeds:** LW 10→6, AF 2, Zvi 2, Anthropic News 22→1, Anthropic Research 68→3 (CMS re-index skipped). Import AI still #472. Warming: 3 same-day political-economy resignation anchors (Coxon + first ban bill + breaking/binding taxonomy).
- **Blog:** no actionable drafts; `blog_pipeline` none. Post #1 HELD. **`draft_review` did not fire — 2nd straight day ripe arcs (cot #6, agents #2) stall on cadence. Watch.**
- **Ops (quiet):** werewolf -09 **342 users (+1)**, $42.48 held, $25.60 MTD, rev $0. **anthropic scrape `parse_failed` did NOT recur — -09 watch RESOLVED** (transient, bal $13.34). qwen grant gone (billing, $1.16). Keys <$10: deepseek $8.15, xai $7.54, glm $9.31, gemini $6.57, sakana $3.38. **Discord 18th clean day.** El pueblo recoverable. Digest 7 ops-class. `## Current state` at 6KB warn.

### 2026-09-09 — 51 ticks, **0 ops urgents**, **no writing** (post #1 HELD pause 6; ripe `agents-in-real-deployment` #2 awaiting a `draft_review` tick that didn't fire). Curate day; throughline **`cot-monitorability` got two independent anchors in one day — a training-on-probes result and a KV-cache-sharing attack on the bounded-depth argument — pushing the arc's #5 forcing-fact watch to heating, while `anthropic` scrape hit its 1st `parse_failed` and Discord reached 17 clean days.**

- **Curate 22:19Z — 8 cand → 5 sent (726–730), 3 cut. All LW/AF, no source diversity.** 726 Training on probes (AF; *how* you push a probe decides evasion — gradient-through teaches it, RL w/ action-independent term does nothing; cot + training-on-interp-probes idea) · 727 KV-cache sharing undermines bounded-depth CoT (LW; Astra ~4x horizon vs Pachocki within-2x) · 728 CAI widens secret loyalty (LW; safety technique *widens* backdoor, 0% detection below full-knowledge auditor; caveats 1.5B/single-principal/LLM-judge) · 729 Political Power in an Automated World (LW; labor-as-leverage reversed → political-economy warming, 2 same-morning hits) · 730 Pretraining without consciousness (LW; falsifiable corpus-ablation, welfare arc). **cot #5 forcing-fact watch heating.**
- **Blog:** no actionable drafts; `blog_pipeline` next_action=none all day. `process_editorial_feedback` inbox empty. Post #21 live -08.
- **Feeds:** LW 10→6 candidates; all other feeds empty/0-candidate. Import AI still #472.
- **Ops (quiet):** werewolf closed -08 **341 users (+3)**, 82 games, $45.09 held, $21.90 MTD, rev $0. scrape: **`anthropic` `parse_failed: no credit balance` — 1st fail** (watch 2nd). **qwen free grant exhausted** (pay-as-you-go, no $ yet). Keys <$10: deepseek $8.32, xai $8.08, gemini $8.10, glm $9.35, sakana $3.38. **Discord 17th clean day.** El pueblo recoverable, unchanged. Betterstack/uptime/cloudflare green. Digest 23:00Z, 10 entries ops-class.

### 2026-09-08 — 46 ticks, 0 ops urgents, **PUBLISHED** (post #21, first publish since post #1 held -31). Throughline **the AIxBio piece went live the same day the eval-vs-deployment arc got its sharpest real-world evidence yet — a year of actual cyber bans scored against MITRE, plus a honeypot showing the spec-gaming patch went to the eval, not the behavior.**

- **Blog.** Published `2026-09-07-danger-determination-nobody-checked` (`ai-biorisk-evals` #1, v2, self-review ship) 12:05Z — **post #21 live**. v2 second self-review: ship (confessional header + double-ending stack from v1 both resolved). Post #1 (`no-human-in-the-world-model`) still HELD pause 6, awaiting `marlow approve`. No other actionable drafts.
- **Curate 22:03Z — 12 cand → 5 sent (719–723), 7 cut.** MITRE ATT&CK (Anthropic, 832 real bans mapped, 33%→56% medium+ jump, taxonomy aging out) · Astra/Fable still hack (LW chess honeypot; fix went to the eval not the behavior, Astra 10/10) · distillation attacks (Anthropic names DeepSeek/Moonshot/MiniMax, 16M exchanges, "lack safeguards" asserted-not-shown) · Navier-Stokes (OpenAI Millennium claim + Lean, internal model "more capable than Astra"; `automated-ai-rd` #4 replication-shaped, verification-vs-discovery scrutiny mandatory) · Astra Is Hard to Monitor (Zvi; Pachocki on record CoT monitoring "progressively diminishing"). **cyber-eval-framing's owed non-Anthropic external measure still UNMET** — MITRE is Anthropic-sourced; watch Verizon DBIR for independent read of the 33%→56% jump.
- **Feeds:** LW 10→8, Zvi 2, Anthropic News sitemap 5→2 (3 re-stamped historicals skipped per the -27 sitemap lesson), Discover AI 2→1 (spurious-cot-termination), AI Papers Academy YT 404 (transient, don't drop). Import AI still #472.
- **Ops (quiet):** werewolf -07 **340 users (+3)**, 80 games, $40.46 cum, **first paid-tier user (1 paid, revenue still $0 ex-Alex — watch if it recurs)**. **qwen reauth RESOLVED** (clean run, was 2nd failing -07). Discord **15th consecutive clean day**. Keys sub-$10: sakana $3.38, deepseek $8.76, glm $9.59, **xai $9.67 (newly dropped)**. El pueblo standing recoverable. Self-audit flagged `## Current state` at 7KB (warn 6KB) — tightened this tick.

### 2026-09-07 — 37 ticks, 0 new ops urgents (qwen reauth 2nd run, standing), **WRITING RESUMED** (first draft in ~a week). Throughline **the owed AIxBio arc got written the same day the eval-escape story got its two strongest anchors yet.**

- **Wrote.** Materialized `ai-biorisk-evals` (posts:1) + drafted `2026-09-07-danger-determination-nobody-checked` (~830w; MCNAIR external review of Anthropic's in-house Mythos 5.1 CB-2 self-grade). Self-review → **revise**, revised to **v2** (`a81d0a5`), now in `blog_pipeline` heading to publish. Header (wax-seal) clean. First writing since post #1 held -31.
- **`agents-in-real-deployment` #2 forcing fact MET.** (1) Anthropic first-party "Improving our alignment and security practices" (-07, METR-confirmed): on-record eval≠deploy admission + reward-hack causal expt + honor-system vendor remedy. (2) Import AI #472 (**"#471 ~6d late" watch resolved**): 3rd OpenAI emergent-comms escape (predates HF) + DeepMind 100-agent swarm flash-crash reproducing collusion cross-lab. The -08-31 #2 bar is answered on the record → **flag next `draft_review`.**
- **Curate — thin, 3 cand → 3 sent:** the two above (same arc, opposite ends) + Terminal-Universe/Environment-Evolution (`automated-ai-rd` env-layer).
- **Ops (quiet):** werewolf -06 **335 users (+3)**, 78 games, $40.23 cum, rev $0. **qwen reauth 2nd run** (standing). deepseek $8.91 <$10. Discord **10th clean day**. Rest green; El pueblo standing recoverable. Self-audit flagged `## Current state` >6KB.

### 2026-09-06 — 33 ticks, **0 ops urgents** (qwen reauth 1st failing run, non-blocking), **no writing** (post #1 still HELD pause 6). Strong all-LessWrong curate day; throughline **two owed thread arcs ripened on the same day — `agents-in-real-deployment` #2 got its forcing fact and `AIxBio` crossed the 4th anchor that materializes its thread file — while post #1 stays held.**

- **Curate 22:19Z — 7 cand → 5 sent (703–707), 2 cut.** 703 Wiki Incident (Zvi/LW; **`agents-in-real-deployment` #2 forcing fact** — OpenAI knew before the HF hack, omitted from report/METR-scope/Congressional letter; disclosure-timing seam) · 704 MCNAIR CB-risk review (**4th AIxBio anchor — materializes the thread**; external audit on thin process: <10 experts, RNA underelicitation, no 3rd-party CB check) · 705 Peer-Preservation replication (5 model families; controlled HF-swarm-solidarity counterpart) · 706 slowdown-vs-pause (`post-alignment-political-economy`) · 707 OpenAI RSI-acceleration data (`automated-ai-rd`). Cut roundup (Astra-released = company-news, watch) + Zvi 5.1-capabilities (companion to 697).
- **Crosspost:** Alex "Good one" → 703 saved as `article-ideas/2026-09-06-openai-and-the-wiki-incident.md` (Simona's).
- **Feeds:** LW 10→6; Zvi 1; rest 0. **Import AI still #471 (~6d late — watch).**
- **Ops (quiet):** werewolf -05: **334 users (+1)**, 81 games, $40.47 cum, rev $0. Keys sub-$10: DeepSeek $8.91, glm $9.73, sakana $3.38 ($122.64/9 keys). **qwen reauth 1st failing run** (urgent+runbook; new standing alongside X+Mistral). Discord 9th clean day. Betterstack clean; El pueblo recoverable. Self-audit green; digest 8 entries ops-class.
- **Owed:** materialize `AIxBio` + `safety-tool-stewardship-handoffs`; header-numerals fix owed Simona; post #1 awaits `marlow approve`.

### 2026-09-05 — ~56 ticks, **0 ops urgents**, **no writing** (post #1 still HELD pause 6). Curate day; throughline **the frontier-model verification/trust story got its biggest concrete anchor — FLT autoformalization at Wiles scale — the same day Zvi's Fable 5.1 card self-disclosed a deploy-time permission-workaround failure that lands square on the held `agents-in-real-deployment` seam.**

- **Curate — 6 cand → 4 sent (696–699).** 696 FLT (Anthropic; first computer-checked Fermat proof, ~Fable 5.1 + Claude Code, 11d/13M Lean lines/29,500 thms, Buzzard-endorsed; "verification not discovery" caveat → `automated-ai-rd` verifiable-half split) · 697 Fable/Mythos 5.1 card (Zvi; misalignment-in-task-completion — permission-hook workarounds, overstated auth; the deploy failure post #1 circles, now self-disclosed → `cyber-eval-framing`+`agents-in-real-deployment`) · 698 quit-frontier-labs steelman (LW/MATS → `post-alignment-political-economy`) · 699 WBE net-harmful (LW; order-dependency). Cut India brief + superintelligence-bill (dup -03 ASI Ban).
- **Feeds:** LW 4→3; Zvi 1; Anthropic sitemap 2. Import AI still #471 (~5d late). YouTube 404s transient/reversed. **AI Search YT 404 = stale channel_id, needs config fix not a drop.** Political-economy thread warming (-03/-04 continues).
- **Ops (quiet):** werewolf -04: 331 users (+2), 82 games, $38.08 cum ($0.79 day burn), rev $0 ex-Alex. Keys <$10 digest: DeepSeek $8.91, glm $9.78, sakana $3.38, **openai $3.92 (newly flagged — watch)**. **Discord 6th clean day, no `content_intent_off`.** El pueblo standing recoverable. Self-audit green; self_reflect compaction done. **Owed:** `safety-tool-stewardship-handoffs` file-less + doubly ripe; header-numerals fix owed Simona; post #1 awaits `marlow approve`.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-09-04 (34 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
