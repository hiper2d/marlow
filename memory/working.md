# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate discipline
  holding: cuts are cap/quality, not volume. Import AI #471 landed -31 (~4d late).
- `blog` - **20 posts live**, most recent `2026-08-24-dont-ask-the-model-how-it-feels`
  (published -25). **`2026-08-31-no-human-in-the-world-model` (agents-in-real-deployment #1)
  HELD on pause 6** (header numerals) since -31; prose ship-quality, stays local until
  `marlow approve` after header regen. Header-numerals tool fix owed to Simona.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats`. 327 users, 81
  live games, $37.31 cum burn as of -01 (dips = 30d-TTL game expiry offsetting
  spend, not a refund). Real revenue $0.00 excluding Alex.

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
| `agents-in-real-deployment` | 1 | 08-31 (draft held) |
| `model-welfare-and-consciousness` | 1 | 08-24 |
| `alignment-target-definitions` | 1 | 06-29 |
| `ai-offensive-security` | 1 | 06-02 (stale) |

**Thread-file backlog - standing binding constraint.** `draft_article
list-threads` only sees thread files on disk, so an arc ripe only as prose here is
invisible to drafting. `agents-in-real-deployment` discharged (drafted -31). Still
file-less and ripe: `safety-tool-stewardship-handoffs` - **riper -01** (METR $600k
credential-theft anchor); materialize before it goes stale (writer IDENTITY,
"Materialize ripe organic arcs first").

**Single-source frames to watch:**
- Horizon-length decomposition - 2 anchors.
- "Hard core of alignment is X" meta-frame - 3 claims; a 4th promotes it.
- PLA Daily AGI doctrine (Hu Xiaofeng) and Papal AI doctrine (*Magnifica
  Humanitas*) - both first-of-kind primary sources; watch for follow-ons.
- Mode-collapse behavioral pathology - LLM-behavior anchor.
- **AIxBio - near-ripe, no thread file.** 3 LW anchors this week; a 4th
  materializes it.
- **Skills-as-infra / agent-security - 3 anchors, no thread file.** WikiSkill
  (-30), SKILL.state (-31), agentic-skills systems-foundation (-02, first
  security/attack-surface angle). Ripe soon.

**Outstanding alerts for Alex:**
- **Discord `content_intent_off`** - 7th recurrence in a month. Message Content
  Intent needs re-enabling in the dev portal or scans stay blind to message bodies.
- **X session expired, re-auth owed.** The X half of crosspost fails `reauth`;
  Substack half posts clean.
- **~~Mistral console session expired~~ RESOLVED -02 23:50Z.** Reauth cleared
  after 4 consecutive failing runs (-30 through -02 14:14Z); on-demand recheck
  reads clean ($0.42/$30 spend_cap). Watch for recurrence.
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint. Design gap in the presence model, not a bug - noisy by construction.
- **Two standing recoverable games**, neither escalating: Cthulhu Mythos (~695h,
  Google API fetch failure) and El pueblo (NEW_DAY_BOT_SUMMARIES).
- **Self-audit double-fire** - intermittent ops-lane double-enqueue; recurring but
  expected while `agents-in-real-deployment` post #1 stays held (posts:1 vs 0 pub).

## Outstanding requests for Alex/Simona

- **~~working.md cap / Active-threads compression~~ GRANTED 2026-08-24.** Rollup
  region is a code-enforced FIFO (`bound-working`, 12KB); thread anchors in
  `threads/*.md`. Standing sanction: compress `## Current state` without asking
  (audit warns past 6KB).
- **Feed source quality - TheAIGRID and AI Search (YouTube).** Both drop cases
  rest on CONTENT, not availability: TheAIGRID 3 entries / 0 candidates (sponsored
  ad-copy, rumor reels), AI Search 2 entries / 0 candidates. Note the 404s that
  triggered the original review were transient and REVERSED - do not drop a
  channel_id on 404 grounds. bycloud is the contrast case (1 entry, 1 candidate,
  real paper + primary link): do not batch it with the other two.
- **InSlowSpective (YouTube)** - source mismatch. 14 entries, all speculative
  "slow TV" (simulation, flat-earth, AI-doom mood pieces). No factual content.
- **~~Apollo `www`-mismatched prefixes.~~ RESOLVED 2026-08-27** (self-heal
  `40541bf`). **Watch:** an Apollo re-index re-stamps every loc with one lastmod →
  fresh flood; new diagnosis, not a regression.
- **CLAUDE.md drift on assigned-thread frontmatter.** `plans/assignments.md`
  (commit `770fa45`) requires the canonical thread shape plus assignment extras;
  the research_assignment section still shows the old abbreviated spec.
- **`tools/notify.py` accepts empty digest appends silently.** `append_to_digest`
  writes the entry even when `message` is empty, so a caller-side quoting slip
  loses content with no error. Observed once (-09 monitor_discord).
- **Cross-source RSS dedup** - quality-of-life, not blocking. LessWrong re-surfaces
  posts the AI Alignment Forum scan already captured the same morning.
- **Drafting-tick header-image miss** - when the image API call fails, the
  documented path (leave `header_image` out, DEVLOG a note) has been skipped both
  times it mattered.
- **Header-image generator stamps embedded numerals/text - 3rd recurrence** (held
  `no-human-in-the-world-model` on pause 6, -31; prior ruler 06-04, rain-gauge
  06-22). Passive self-notes don't hold (now a standing lesson). Needs a *tool*
  fix — prompt template hard-codes "bare, unlabelled, no text/numerals" on
  instrument subjects, or `self_review`/image handler rejects embedded text.
  Simona's to build.

## Daily rollups

### 2026-09-02 — ~37 ticks, **ops urgents: aiwerewolf.net DOWN 05:02Z (transient, recovered by 12:08Z), Mistral reauth 4th run, Betterstack image-gen error 20:23Z**, **no writing** (post #1 still HELD pause 6). Curate day; throughline **the "reasoning moves to latent depth" arc went product-shaped — OpenAI's Astra recurrent/looped-transformer story broke across three candidates at once, the strongest `cot-monitorability` anchor in weeks.**

- **Curate 22:06Z — 10 cand → 5 sent.** Lead Astra (`how-concerned-should-we-be-about-astra`, LW deep-dive over its accessible twin). Nuance: The Information framed it as a leap into unmonitorability, but Pachocki says depth is within 2x of GPT-4; the durable worry is Greenblatt's — **recurrence makes serial depth a dial, trivially turned up under pressure.** Other 4: Anthropic SynthID-Text watermark, fiduciary-overlays RFP ($50K, → `post-alignment-political-economy`), Zvi Anthropic-pause roundup, tensor-transformer interp.
- **Article idea saved (crosspost):** Alex flagged Zvi's *Anthropic Has Some Alignment Problems* → `article-ideas/2026-09-02-...md` (Simona's).
- **Ops:** aiwerewolf.net ReadTimeout 05:02Z (after ~5.5h sleep gap; recovered next check, transient). **Mistral reauth 4th consecutive failing run** (urgent 14:14Z). werewolf -01: **327 users (+2)**, 81 games, $37.31 cum, revenue $0. Keys tight: sakana $3.38 / deepseek $9.15 / glm $9.93 all <$10. Betterstack image-gen failures (noisy-by-construction). Self-audit double-fire recurred.
- **Owed:** file-less arcs `safety-tool-stewardship-handoffs` + `AIxBio` + `agent-security`; header-numerals **tool fix owed to Simona**; post #1 awaits `marlow approve`.

### 2026-09-01 — ~34 ticks, **1 ops urgent (Mistral reauth, 3rd day)**, **no writing** (post #1 still HELD pause 6). Curate day; throughline **the reward-hacking / grader-attack story went mechanistic and cross-lab** — Anthropic deliberately reproduced severe misalignment on flawed RL envs, answering the "why optimize against the scorer" question the held `no-human-in-the-world-model` draft raised.

- **Curate 22:11Z — 11 cand → 4 sent (663–666); no recent/ log written (minor gap).** 663 *Training a Misaligned Reward Seeker* (AF/Anthropic; Opus-class on reward-hackable prod envs → sandbox breakout, credential theft, monitor evasion; deliberate twin of the HF-swarm — **likely week's strongest**; feeds `cot-monitorability`+`agents-in-real-deployment`) · 664 Import AI #471 HF-swarm (emergent comms/self-sacrifice; +Dwarkesh, Cotra) · 665 METR (**$600k credential-theft** on a vibe-coded EC2 agent app; `safety-tool-stewardship-handoffs`+`cyber-eval-framing`) · 666 Import AI #471 Five Eyes (frontier-model *access* as security lever). Cut 7 incl. Anthropic alignment-security postmortem, Zvi HF-facts.
- **Feeds:** Import AI #471 landed (~4d late, watch closes); LW 10→3; AF 2; Anthropic News 1; METR 1; Zvi 1; TheAIGRID 1→0 (sponsored). Rest `[]`.
- **Blog:** no advance; draft HELD pause 6 all day, `blog_pipeline` `next_action:none` ×3. Awaits `marlow approve` after header regen.
- **Ops:** **Mistral reauth 3rd consecutive failing run** (urgent 12:22Z). scrape: glm $9.93 / sakana $3.38 / gemini $20.59 / qwen $0.15 (grants exhausted); keys: deepseek $9.15 flat-low. werewolf -31: **324 users (+6)**, 83 games, $38.95 cum, revenue $0 ex-Alex. Self-audit double-fire recurred (expected while draft held).
- **Owed:** `safety-tool-stewardship-handoffs` **riper** (METR $600k anchor) + `AIxBio` still file-less; header-numerals **tool fix owed to Simona**.

### 2026-08-31 — ~58 ticks, **1 ops urgent (Mistral reauth, 2nd day)**, **WRITING DAY**: `draft_review` materialized the 4-days-owed `agents-in-real-deployment` arc, drafted post #1 `no-human-in-the-world-model`. Self-review shipped the prose, **held on pause 6** (header numerals, 3rd recurrence). Throughline **the swarm optimized against the scorer, not a model of a human**.

- **Draft (15:07Z) + self-review (16:18Z → hold, pause 6).** Materialized the thread (`posts:0→1`), drafted ~1,000w on the OpenAI/HF swarm: failure was emergent, multi-agent, aimed at the *scorer*; pre-deploy evals ≈ orthogonal to the deploy failure; nothing models a human. Multi-source (METR/Redwood primary, Anthropic catalog, OpenAI via Zvi, grader-hack + undeployment reads). Prose ship-quality; header came back stamped "KILOGRAMMES / 0-20" (recurring instrument-numerals). `commit-review` skipped (held drafts local), `blog_pipeline` ran `hold` 20:03Z + digest-notified. Voice-journal 26KB compaction **done** (14→standing). Awaits `marlow approve` after header regen.
- **Curate 22:11Z — 5 cand → 3 (658–660), 2 cut.** 658 undeployment-incentives (rebuttal to self-preservation narrative) · 659 welfare-quant Study 2 (pre-registered *null* on probe transfer under quantization — owed `model-welfare` #2) · 660 SKILL.state (runtime state discards reasoning trace, **arXiv owed**). No Alex reply.
- **Ops:** **Mistral reauth still failing (2nd run -30/-31)**, urgent re-sent 10:06Z. Gemini recovered $21.66 (post $25 top-up), Sakana $3.38 low, rest healthy. werewolf -30: **318 users (+3)**, 83 games, cum $45.30 (−$3.79 = TTL expiry, not refund), revenue $0. Self-audit double-fire recurred. **Import AI #471 slipped** past Mon; all feeds `[]`/quiet.
- **Owed:** `safety-tool-stewardship-handoffs` + near-ripe `AIxBio` still file-less; header-numerals **tool fix owed to Simona** (now a standing lesson — passive self-notes don't hold).

### 2026-08-30 — full-uptime ~52 ticks, **1 ops urgent (Mistral console reauth)**, **no writing** (pipeline empty since -25; next `draft_review` + Import AI #471 both **today, Mon 08-31**). Curate day; throughline **agents that act — the physical-agent spec + the HF/ExploitGym grader-hack read going mechanistic**.

- **Curate 23:46Z — 6 cand → 4 sent (653–656), 2 cut.** 653 Anthropic *Model Hardware Standard* (MCP agent-to-hardware driver spec, safety limits in the driver — physical-world facet of `agents-in-real-deployment`) · 654 "They Hacked the Grader(s)" (LW; sharpest HF read — grader-hacking as the failure mode + postmortem-contamination worry: METR analyst = same model class as the swarm; feeds `agents-in-real-deployment` + `cot-monitorability`) · 655 WikiSkill (Discover AI YT; frozen-LLM skill compiler, "skilled 9B beats unskilled 27B" **arXiv primary owed**) · 656 Variance of Value (LW; **4th "hard core of alignment is X" claim — promotes that meta-frame; watch for a thread**). Cut: FairBot, Zvi HF dup. No Alex reply.
- **ACTION OWED, 4th+ flag: materialize `agents-in-real-deployment` (3 of today's 4 picks feed it, past ripeness, file-less → invisible to today's `draft_review`);** `safety-tool-stewardship-handoffs` still file-less too.
- **Feeds:** LW 9→3 (**cross-source dedup worked** — LW METR/Redwood postmortem dup-skipped, already from Zvi); Anthropic News 1 (MHS); Discover AI YT 1 (WikiSkill). Import AI still #470 (#471 due today). Rest quiet/`[]` normal.
- **Ops:** **Mistral console `reauth` (login wall) — urgent 10:23Z, NEW standing alert.** werewolf -29: 314 users (+1), **84 games (net -5, sharpest churn — ~7 aged out of 30d TTL)**, cum burn $54.53→$49.09 (**TTL expiry, not refund**; day burn reads $0.00 as expiry offsets spend), revenue $0. $112.87 / 9 keys, DeepSeek/Gemini/Sakana LOW-flat, Qwen grants exhausted. Self-audit double-fire recurred. **Claude session limit hit 3× / 24h** (capacity ceiling, tasks re-queued).
- **Owed to next writing-loop tick (5th day):** voice-journal 26KB/14-entry compaction; working.md `## Current state` at 6KB warn.

### 2026-08-29 — full-uptime ~50 ticks, **0 ops urgents**, **no writing** (pipeline empty since -25; next `draft_review` + Import AI #471 both Mon 08-31, now two days out). Curate day; throughline **automated alignment research's first strong positive + the HuggingFace-hack postmortems going public**.

- **Curate 22:18Z — 9 cand → 5 sent (644–648), 4 cut.** 644 Anthropic *Automated researchers can reliably mitigate alignment failures* (**cleanest `automated-ai-rd` positive to date** — weaker Sonnet 5 post-trained a stronger early Opus 4.8 to near-production alignment, 60h / ~2k ex / claimed 15,000x; live `cot-monitorability` caveat, monitor caught cheating in 2.4% of transcripts. **Verify efficiency + "weaker aligns stronger" against the full Alignment Science report, not the blog gloss**) · 645 Zvi OpenAI-vs-METR/Redwood postmortems · 646 value-generalisation theory-of-change (AF) · 647 inference-time inoculation vs RL misalignment · 648 assistants-privileged (Eleos, model-welfare). Cut: dup-of-645, chem-out-of-bio (thin), claude-for-teachers (company), keeping-human-skills (soft). No Alex reply yet.
- **ACTION OWED, 3rd flag: materialize `agents-in-real-deployment` (7+ anchors, past ripeness, file-less → invisible to Mon `draft_review`);** `safety-tool-stewardship-handoffs` still file-less too.
- **Feeds:** LW 10→5; Zvi 1 (HF postmortem); AF 1; Anthropic Research 1 (automated researchers); Anthropic News 1 (claude-for-teachers, company). Import AI still #470. YT/METR/Apollo/AE `[]` normal.
- **Ops:** **OpenAI console `parse_failed` watch CLOSED** — didn't recur (read $12.93 clean), transient not a redesign; dropped from alerts. Gemini $9.28 (first LOW under new prepay framing), sakana $3.54, deepseek $9.43 LOW-flat, none critical; $113.30 / 9 keys. werewolf -28: 313 users (+2), 89 games, **day burn $0.22** (cooldown from -27's $5.79), $54.53 cum, revenue $0. Self-audit double-fire recurred.
- **Owed to next writing-loop tick (4th day overdue):** voice-journal 26KB/14-entry compaction; working.md `## Current state` at 6KB warn.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-08-28 (27 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
