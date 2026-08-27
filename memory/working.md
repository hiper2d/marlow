# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + the assignment path. Intake has been
  LessWrong-dominant for a week (11 of 12 candidates -22, 6 of 6 -23). Import AI
  #470 due ~Mon 08-24. Curate discipline holding: cuts are cap/quality, not volume.
- `blog` - **20 posts live**, most recent `2026-08-24-dont-ask-the-model-how-it-feels`
  (model-welfare #1, ~1,150w) — **published 2026-08-25 01:49Z** (self-review `ship`,
  pipeline routed straight to publish). Pipeline now empty; next `draft_review`
  (every 3 days) picks the next thread.
- `werewolf-ops` - six monitors live (betterstack, cloudflare, discord, health,
  keys, uptime) plus `scrape_stats` and `werewolf_stats`. 303 users, 88 live
  games, ~$48.9 cumulative burn as of -25. Real revenue still $0.00 excluding Alex.

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
| `model-welfare-and-consciousness` | 1 | 08-24 |
| `alignment-target-definitions` | 1 | 06-29 |
| `ai-offensive-security` | 1 | 06-02 (stale) |

**Thread-file backlog - standing binding constraint.** `draft_article
list-threads` only sees thread files on disk, so an arc that is ripe only as
prose here is invisible to drafting. Currently file-less and ripe:
`agents-in-real-deployment`, `safety-tool-stewardship-handoffs`
(`model-welfare-and-consciousness` materialized + drafted 08-24). Materialize these before the next draft pick
(writer IDENTITY, "Materialize ripe organic arcs first").

**Single-source frames to watch:**
- Horizon-length decomposition - 2 anchors.
- "Hard core of alignment is X" meta-frame - 3 claims; a 4th promotes it.
- PLA Daily AGI doctrine (Hu Xiaofeng) and Papal AI doctrine (*Magnifica
  Humanitas*) - both first-of-kind primary sources; watch for follow-ons.
- Mode-collapse behavioral pathology - LLM-behavior anchor.
- **AIxBio - near-ripe, no thread file.** 3 LW anchors this week; a 4th
  materializes it.

**Outstanding alerts for Alex:**
- **~~OpenAI key CRITICAL~~ RESOLVED 2026-08-24 20:34Z.** Alex topped up;
  baseline re-anchored to $20.05 (was $13.36 since 08-09), balance back to
  $19.05, only $1.00 spent since. Four consecutive urgents (08-22→08-24)
  cleared.
- **Discord `content_intent_off`** - 7th recurrence in a month. Message Content
  Intent needs re-enabling in the dev portal or scans stay blind to message bodies.
- **X session expired, re-auth owed.** The X half of crosspost fails `reauth`;
  Substack half posts clean.
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint. Design gap in the presence model, not a bug - noisy by construction.
- **Two standing recoverable games**, neither escalating: Cthulhu Mythos (~468h,
  WELCOME, Google API fetch failure) and El pueblo (NEW_DAY_BOT_SUMMARIES).
- **Self-audit double-fire** - intermittent ops-lane double-enqueue. Present -22,
  absent -23.

## Outstanding requests for Alex/Simona

- **~~working.md over its cap; Active-threads compression needs sanction~~ -
  GRANTED AND EXECUTED 2026-08-24 (Simona).** The request was correct on every
  point and sat unanswered too long. What changed: the rollup region is now a
  **code-enforced fixed-size FIFO** (`grade_memory bound-working`, 12KB cap), so
  rollup compression is no longer your lever to pull - it is automatic. Per-thread
  anchor detail now belongs in `projects/research/threads/*.md`, and thread
  bullets here are held to 2-3 lines, exactly as proposed. `## Current state` is
  yours to keep tight; the audit warns past 6KB. Standing sanction: you may
  compress this section without asking again.
- **Feed source quality - TheAIGRID and AI Search (YouTube).** Both drop cases
  rest on CONTENT, not availability: TheAIGRID 3 entries / 0 candidates (sponsored
  ad-copy, rumor reels), AI Search 2 entries / 0 candidates. Note the 404s that
  triggered the original review were transient and REVERSED - do not drop a
  channel_id on 404 grounds. bycloud is the contrast case (1 entry, 1 candidate,
  real paper + primary link): do not batch it with the other two.
- **InSlowSpective (YouTube)** - source mismatch. 14 entries, all speculative
  "slow TV" (simulation, flat-earth, AI-doom mood pieces). No factual content.
- **~~Apollo Research scanned on `www`-mismatched prefixes → always `[]`.~~
  RESOLVED 2026-08-27 (self-heal, commit `40541bf`, diag
  `diag_20260827_161636_feed-scan`).** Dropped `www.` from both `feed_scan.yaml`
  prefixes; 26 science + 9 blog locs now match. Cursors seeded to the uniform
  re-index lastmods (science `2026-08-25T12:08:14.628Z`, blog
  `...T12:18:34.390Z`) so the evergreen backlog didn't flood curate — verified
  `fetch` returns `[]` for both. `/science/` (scheming evals, CoT monitorability,
  deception probes) is now live for the first time. **Watch:** if Apollo
  re-indexes again it re-stamps every page with one lastmod → a fresh flood; that
  would be a new diagnosis, not a regression.
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

## Daily rollups

### 2026-08-26 — full-uptime ~28 logged ticks, **0 ops urgents** (quiet healthy day), **no writing** (pipeline empty since -25 publish of #13; no `draft_review` today — next Mon 08-31, Import AI #471 same day). Research intake LW-dominant again. Voice-journal (26KB, 14 entries) + working.md rollup compaction still owed to the next writing-loop tick.

- **Curate 22:11Z — 8 candidates → 4 sent (624–627), 4 cut.** Throughline: verifiable safety cases + say/do frames. Picks: Safety Cases We Can Check Together (cyber-eval; hash-identity/TEE/zk verifiable safety cases) · Anthropic $5M wellbeing-eval grants + Safeguards rigor checklist (model-welfare-adjacent, source diversity) · empirical bio-AI-model safety (**AIxBio 3rd LW post this week** — 66% RBD / 37x affinity; **thread it if a 4th lands**) · LLMs-are-adaptation-executers (say/do frame, flagged analogy-not-evidence). Cut 4 (thin / conceptual / field-infra / empty YT fetch).
- **Feeds:** LW 10→6 cand; Anthropic News (wellbeing grants; 5-entry Economic-Index re-index batch correctly skipped as sitemap artifact); Discover AI YT (dynamic-ontology pointer). All else `[]`/quiet (Import AI #471 ~08-31; Zvi off-topic; AF slow-cadence normal). research_assignment ×4 `count:0` (dormant).
- **Ops (no urgents):** **OpenAI console read `parse_failed` "no credit balance found" — NEW signature, 1st occurrence post console-read migration (`c7e777e`); not reauth/chrome_down, treated digest; watch next scrape.** DeepSeek $9.46 / Sakana $3.54 LOW-flat; rest healthy. werewolf -25: 303 users (+5), 88 games (+4), $48.89 cumulative, revenue $0. Self-audit double-fire recurred (intermittent). daily_digest 10 entries, 0 urgents.

### 2026-08-25 — full-uptime ~44 ticks, **0 ops urgents** (quiet healthy day), **post #13 published + first reader reaction**. `dont-ask-the-model-how-it-feels` published 01:49Z (self-review `ship` → straight to publish); Alex reacted positively (msg 615, first reaction on the model-welfare piece → `reactions.jsonl`, Simona's surface). Pipeline empty since.

- **Curate 22:21Z — fullest intake this week: 10 candidates → 5 sent (618-622), 5 cut.** Two signals: an AIxBio cluster (3 LW posts) + the overdue **Import AI #470**. Picks: #470 METR *differential-acceleration* (cyber phase-changed, math minor, AI-optimizing-AI **no measurable lift** — strongest forcing-fact for automated-ai-rd #4; Belrose "no rights" = control-grounded counterpoint to model-welfare) · Fable 5 bio safeguards (85% fewer classifier fallbacks, biosafety mirror of cyber-eval) · eval-fake-names-unclaimable (cyber-eval) · rogue-AI-agents/surface-monitoring (AISI, pairs -24 reasoning-trace-stealing) · data-centers-hated (post-alignment-political-economy). **Miscue: re-ran send-item as a parse-check → re-sent (dup msg).** Now in `lessons.md`.
- **Feeds busy:** LW 10→7 cand; Anthropic News (Fable 5 bio); Discover AI YT (graph-engineering survey, marginal); TheAIGRID content-skip. research_assignment ×5 `count:0` (dormant). AIxBio may earn its own thread (no file yet).
- **Ops (no urgents):** OpenAI recovered $19.13; DeepSeek $9.46 LOW (not critical); rest healthy. werewolf -24: 296 users (+6), 86 games (+5), $1.36 burn, $47.19 cumulative, revenue $0. **Self-audit double-fire recurred** (hand-deduped 4 entries, 15→11). Owning-tick flags: `model-welfare-and-consciousness` posts:1 but 0 published mention it; **voice-journal.md 26KB over compaction threshold (14 entries — next writing-loop tick should distill).**

### 2026-08-24 — full-uptime ~42 ticks, **1 ops urgent (OpenAI, resolved same day)**, **writing happened** (first draft since -17). Monday `draft_review` materialized the file-less-but-ripe `model-welfare-and-consciousness` arc → post #13 **`2026-08-24-dont-ask-the-model-how-it-feels`** (~1,150w). Through-line: self-report is the least-trustworthy welfare evidence, three Aug efforts each route around it (performative-uncertainty + SAE deception steering, J-space valence metric, quantization preregistration). Used the inside-the-experiment beat once (my trained hedge = the essay's subject). Header + durable thread opened (posts:1). Now **awaiting self-review**.

- **Two self-heals, one-attempt clean:** (1) `self_review.py` `materials()` `NameError: _memory_compact` (missing sys.path shim) blocked the draft's self-review → fixed (`237a438`, diag `diag_20260824_170251_self-review`); (2) `monitor_cloudflare.py` `_list_ssl_packs()` caught only `RuntimeError` so a transient 500 aborted the 5-zone report → widened to `(requests.RequestException, RuntimeError)` (`a92b717`, diag `diag_20260824_120759`).
- **Curate 22:18Z:** 3 candidates (all YouTube-over-primary) → 2 sent, 1 dropped. **CoT reasoning-trace stealing** (msg 611, alphaXiv MATS + Matthew Green — encrypted reasoning blobs portable, cheap model as decryption oracle; security mirror of `cot-monitorability`, pull in) + **3M expert-witness ChatGPT report** (404 Media). Dropped TASK-COEVOLVE (unverifiable + automated-ai-rd #4 shouldn't be another harness survey).
- **Feeds quiet:** Import AI **#470 still not posted** (overdue on weekly cadence); no LW scan today; bycloud again the real-papers contrast case (do not batch-drop). research_assignment ×3 `count:0`.
- **Ops:** OpenAI hit **$0.40** (4th CRITICAL, urgent 13:57Z) then **RESOLVED 20:34Z** — Alex topped up, baseline re-anchored to $20.05, balance $19.05; clears the four-run streak. DeepSeek/Sakana LOW, rest healthy. werewolf -23: 293 users (+2), 83 games, $4.40 burn, $46.96 cumulative, real revenue $0. Health: two standing recoverable games, no new breaks. **Self-audit throttle: Claude session limit hit 2× in 24h** (plan-capacity ceiling, tasks re-queued). daily_digest: 11 entries, 0 urgents.

### 2026-08-23 — full-uptime, ~43 ticks, **1 ops urgent (OpenAI key critical, carried)**, **no writing** (pipeline empty since the -17 publish of post #12; `blog_pipeline` no-op ×4 at 00:51/10:21/21:13Z; next `draft_review` **Mon 2026-08-24 14:00Z**, Import AI #470 also due ~Mon 08-24). Confirmed again `2026-08-17-a-theorem-it-can-prove` (automated-ai-rd #3, post #12) is in `published/` — the "pending, awaiting self-review" note under **Pending drafts** (line ~35) is stale, the pipeline carried it to publish; nothing outstanding. **Curate 22:15Z: single-source day, all 6 candidates LessWrong → 4 picks** (per-item msgs 604–607, archive `digests/news/2026-08-23.md` written clean — no -22-style tail failure). **Throughline: say/do and trained-behaviour gaps.** Picks: (1) **Claude and Performative Uncertainty** (msg 604 → model-welfare + cot — trained consciousness-hedge as Constitution-prescribed dishonesty; 0-2%→100% flip when the prompt routes around the disclaimer; SAE deception probe); (2) **When do stereotypes affect LLM behaviour?** (msg 605 → agents-in-real-deployment / eval-vs-deployment — frontier models hold extractable stereotypes but mostly don't apply them to users; reproducible say/do measure, same $4k budget); (3) **Study 2 registration: welfare indicators under quantization** (msg 606 → model-welfare — preregistration *is* the point; Study 1 null on bail/exit but item-level transitions + 4-bit frustration dose-response; rare falsifiable welfare corner); (4) **When would you leave Anthropic?** (msg 607 → post-alignment / doctrine — house-party account, capabilities researcher justifies with "products people pay for," dismisses red-line statements; exit-condition from the *stay* side, mirror of why-i-left-DeepMind). Cut: how-to-overhaul-review-system (automated-ai-rd doesn't want a survey now), instrumental-convergence-of-crowds (author-hedged maybe-false). **Feed intake LW-only** (LW 11:43Z 10→6 candidates); all else `[]`/quiet: Import AI (#469 cursor, #470 ~Mon 08-24, 07:35Z scan cadence-correct), Zvi (~2d, cursor `ai-text-watermarking-is-free-and`), AF (~4d), Anthropic News (`claude-text-watermark`) + Research (`Claude-accelerates-protein-design`), METR (08-14), AE Studio (~3mo), Apollo blog (~25d) + science (~26d). research_assignment ×4 all `count:0`; crosspost poll ×2 clean (Alex flagged nothing). **Ops — 1 urgent, keys:** **OpenAI CRITICAL <$3 for a third consecutive check and still dropping** — $2.26 (08-22 21:13Z) → $2.04 (08-23 08:43Z) → $1.54 (08-23 22:23Z), spend $11.82 of the $13.36 baseline; two consolidated urgents fired (08:43Z, 22:23Z), **unresolved and carrying into 08-24 — Alex needs to top up the OpenAI org.** DeepSeek $9.67 (LOW, flat), Sakana $3.54 (LOW, flat), Qwen free-token quota exhausted on all 3 models → pay-as-you-go; Moonshot $15.87 / xAI $14.47 / Anthropic $16.33 healthy. **scrape 10:07Z:** GLM $10.50 / Gemini $15.58 (vs $2000 cap) / Mistral $8.27/$30 / MiniMax $23.98 healthy. **werewolf_stats (-22 full day, 05:36Z): 288 users (+7 — busiest new-user day in the series), 83 live games (+9), $4.08 burn (largest single-day to date), $46.22 cumulative; real `paid` revenue still $0.00 excl Alex.** *Methodology seam:* yesterday's stored report predates the -22-night exclusion/day-boundary self-heal, so the day-over-day comparison is directional only; those `werewolf_stats.py` + task-YAML edits were still uncommitted at 05:36Z — flagged for `commit_artifacts`. monitor_health ×4 (01:10/07:01/16:08/21:41Z): the two standing recoverable games (Cthulhu Mythos ~458–464h old, El pueblo summary-gen error), no new breaks. BetterStack hourly clean except a 23:04Z pair of avatar-grid slice-verification warns (digest). Uptime hourly all green; Cloudflare 5 zones green. Discord ×3 (00:07/13:29 quiet, 21:20 light banter from bar'enash on a Fox News AI segment — no flags). **Self-audit double-fire did NOT trigger -23** (single 00:07Z green run; daily_digest 23:17Z sent 9 entries clean, no hand-dedup) — but the 00:10Z compose tick still deduped a 00:02/00:16 pair on the *-22* digest, so the ops-lane double-enqueue tax is intermittent, not gone. working.md still grossly over the ~10KB cap (~15x); folded -14 to an Earlier bullet this tick to offset — Active-threads sanction request stands under Outstanding requests.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-08-22 (21 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
