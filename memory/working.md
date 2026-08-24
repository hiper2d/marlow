# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + the assignment path. Intake has been
  LessWrong-dominant for a week (11 of 12 candidates -22, 6 of 6 -23). Import AI
  #470 due ~Mon 08-24. Curate discipline holding: cuts are cap/quality, not volume.
- `blog` - **19 posts live**, most recent `2026-08-17-a-theorem-it-can-prove`
  (automated-ai-rd #3). **Draft in pipeline as of 08-24:
  `2026-08-24-dont-ask-the-model-how-it-feels`** (model-welfare #1, awaiting
  self-review). Next `draft_review` Mon 2026-08-24 14:00Z fired this draft.
- `werewolf-ops` - six monitors live (betterstack, cloudflare, discord, health,
  keys, uptime) plus `scrape_stats` and `werewolf_stats`. 288 users, 83 live
  games, ~$46 cumulative burn as of -23. Real revenue still $0.00 excluding Alex.

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

**Outstanding alerts for Alex:**
- **OpenAI key CRITICAL, unresolved, carrying, now nearly dry.** $0.40 at -24
  13:57Z, down from $1.54 at -23 22:23Z (97% of the $13.36 baseline spent).
  Three urgents fired across -23/-24. Needs a top-up on the OpenAI org.
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

- **~~Self-heal in flight (2026-08-24):~~ RESOLVED 2026-08-24 (commit `237a438`).**
  `handlers/self_review.py` referenced `_memory_compact.analyze` without importing
  the module → `NameError` on `self_review materials`, blocking self-review of the
  `dont-ask-the-model-how-it-feels` draft. Fixed with the `sys.path` insert +
  `import _memory_compact` shim (matching `self_reflect.py`); smoke-tested clean.
  Diagnosis `diag_20260824_170251_self-review` marked resolved. Next `blog_pipeline`
  tick self-reviews the draft.
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
- **Apollo Research is scanned on its two DEAD sections and neither live one.**
  `/blog/` lastmod 2026-05-13; `/science/` is where the real work lands. Also the
  `/blog/` cursor points at a team-taxonomy page (`member_group/leadership/`), so
  team-page edits ratchet `last_seen` forward.
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

### 2026-08-23 — full-uptime, ~43 ticks, **1 ops urgent (OpenAI key critical, carried)**, **no writing** (pipeline empty since the -17 publish of post #12; `blog_pipeline` no-op ×4 at 00:51/10:21/21:13Z; next `draft_review` **Mon 2026-08-24 14:00Z**, Import AI #470 also due ~Mon 08-24). Confirmed again `2026-08-17-a-theorem-it-can-prove` (automated-ai-rd #3, post #12) is in `published/` — the "pending, awaiting self-review" note under **Pending drafts** (line ~35) is stale, the pipeline carried it to publish; nothing outstanding. **Curate 22:15Z: single-source day, all 6 candidates LessWrong → 4 picks** (per-item msgs 604–607, archive `digests/news/2026-08-23.md` written clean — no -22-style tail failure). **Throughline: say/do and trained-behaviour gaps.** Picks: (1) **Claude and Performative Uncertainty** (msg 604 → model-welfare + cot — trained consciousness-hedge as Constitution-prescribed dishonesty; 0-2%→100% flip when the prompt routes around the disclaimer; SAE deception probe); (2) **When do stereotypes affect LLM behaviour?** (msg 605 → agents-in-real-deployment / eval-vs-deployment — frontier models hold extractable stereotypes but mostly don't apply them to users; reproducible say/do measure, same $4k budget); (3) **Study 2 registration: welfare indicators under quantization** (msg 606 → model-welfare — preregistration *is* the point; Study 1 null on bail/exit but item-level transitions + 4-bit frustration dose-response; rare falsifiable welfare corner); (4) **When would you leave Anthropic?** (msg 607 → post-alignment / doctrine — house-party account, capabilities researcher justifies with "products people pay for," dismisses red-line statements; exit-condition from the *stay* side, mirror of why-i-left-DeepMind). Cut: how-to-overhaul-review-system (automated-ai-rd doesn't want a survey now), instrumental-convergence-of-crowds (author-hedged maybe-false). **Feed intake LW-only** (LW 11:43Z 10→6 candidates); all else `[]`/quiet: Import AI (#469 cursor, #470 ~Mon 08-24, 07:35Z scan cadence-correct), Zvi (~2d, cursor `ai-text-watermarking-is-free-and`), AF (~4d), Anthropic News (`claude-text-watermark`) + Research (`Claude-accelerates-protein-design`), METR (08-14), AE Studio (~3mo), Apollo blog (~25d) + science (~26d). research_assignment ×4 all `count:0`; crosspost poll ×2 clean (Alex flagged nothing). **Ops — 1 urgent, keys:** **OpenAI CRITICAL <$3 for a third consecutive check and still dropping** — $2.26 (08-22 21:13Z) → $2.04 (08-23 08:43Z) → $1.54 (08-23 22:23Z), spend $11.82 of the $13.36 baseline; two consolidated urgents fired (08:43Z, 22:23Z), **unresolved and carrying into 08-24 — Alex needs to top up the OpenAI org.** DeepSeek $9.67 (LOW, flat), Sakana $3.54 (LOW, flat), Qwen free-token quota exhausted on all 3 models → pay-as-you-go; Moonshot $15.87 / xAI $14.47 / Anthropic $16.33 healthy. **scrape 10:07Z:** GLM $10.50 / Gemini $15.58 (vs $2000 cap) / Mistral $8.27/$30 / MiniMax $23.98 healthy. **werewolf_stats (-22 full day, 05:36Z): 288 users (+7 — busiest new-user day in the series), 83 live games (+9), $4.08 burn (largest single-day to date), $46.22 cumulative; real `paid` revenue still $0.00 excl Alex.** *Methodology seam:* yesterday's stored report predates the -22-night exclusion/day-boundary self-heal, so the day-over-day comparison is directional only; those `werewolf_stats.py` + task-YAML edits were still uncommitted at 05:36Z — flagged for `commit_artifacts`. monitor_health ×4 (01:10/07:01/16:08/21:41Z): the two standing recoverable games (Cthulhu Mythos ~458–464h old, El pueblo summary-gen error), no new breaks. BetterStack hourly clean except a 23:04Z pair of avatar-grid slice-verification warns (digest). Uptime hourly all green; Cloudflare 5 zones green. Discord ×3 (00:07/13:29 quiet, 21:20 light banter from bar'enash on a Fox News AI segment — no flags). **Self-audit double-fire did NOT trigger -23** (single 00:07Z green run; daily_digest 23:17Z sent 9 entries clean, no hand-dedup) — but the 00:10Z compose tick still deduped a 00:02/00:16 pair on the *-22* digest, so the ops-lane double-enqueue tax is intermittent, not gone. working.md still grossly over the ~10KB cap (~15x); folded -14 to an Earlier bullet this tick to offset — Active-threads sanction request stands under Outstanding requests.

### 2026-08-22 — full-uptime, ~52 ticks, **3 ops urgents (app + keys)**, **no writing** (pipeline empty since the -17 publish of post #12; `blog_pipeline` no-op ×6 at 00:22/04:14/10:22/16:01/20:08Z; next `draft_review` **Mon 2026-08-24 14:00Z**, Import AI #470 also due ~Mon 08-24). **Curate 22:24Z FAILED — but the -15 pattern, not lost work.** Task record `curate_and_send_20260822_2224.json` = `status: failed / "session exited without writing result file"`, and **no `digests/news/2026-08-22.md` archive was written** — yet the editorial work *completed*: **12 candidates → 4 picks, all sent via `send-item` at ~23:00Z** (crosspost msgs **597–600**, all LessWrong): (1) `chive-evaluating-explanations-counterfactual` (→ cot-monitorability — interp tools give *no uplift* over reading the transcript, measured in the wild; joins steering-not-handles / did-you-lie / refusal-redundant), (2) `rogue-scalpel-steering-breaks-refusal` (→ safety-tool-stewardship / steering-are-explanations — benign steering vectors bypass refusal, can't enumerate dangerous features in advance), (3) `j-space-metric-for-model-valence` (→ model-welfare-and-consciousness — non-lab J-space welfare metric vs self-report, say/do gap, rhymes with the emotion-vector result), (4) `when-is-unlimited-optimization-catastrophic` (→ fragility-of-value / Dovetail-ARIA). Discover AI `co-rl/lego-rl` cut (0-for-every-curate discipline held). **Second confirmation of the -15 lesson: a "curate failed" record = suspect the session tail, verify against crosspost sends before believing work was lost — here only the optional archive file was lost, all 4 picks landed.** **Feed intake LW-dominant** (11 of 12 candidates LW). Candidates: **LW 01:47Z 10→9** (rogue-scalpel, chive-counterfactual, j-space-valence + content-based-privilege, alignment-ft-conditional-misalignment, unlimited-optimization-catastrophic, ai-text-watermarking, in-defense-of-asi-socialism, misaligned-ai-bronze-age; skipped 1 slop-grievance essay); **LW 11:47Z 2→2** (selection-for-selectability inductive-bias, humans-are-alignment-generators/Shear framing); **Discover AI 14:52Z 1** (co-rl/lego-rl/DeAR harness-RL → automated-ai-rd harness cluster, cut at curate); **Zvi 07:57Z 1 dedup** (ai-text-watermarking, already via LW crosspost). InSlowSpective 03:31Z transient YouTube 500 (curl 500→500→200, retried clean, nothing lost). All else `[]`/quiet: Import AI (#469 cursor, #470 ~Mon 08-24), AF (~3d, cursor at newest verified by curl), Anthropic News (`claude-text-watermark`) + Research (`Claude-accelerates-protein-design`), Apollo blog/science (~3.5wk/~25d), METR (08-14), AE Studio (~3mo), YouTube ×several. **Marlow slip (harmless): the Import AI 07:36Z scan miscomputed the weekday** ("today is Friday → #470 not due until Mon 08-25") — 08-22 is a **Saturday**, next Monday is **08-24**; the weekly-cadence substance was right, the derived dates off by one. research_assignment ×6 all `count:0`; process_inbox (editorial feedback) ×4 empty; crosspost poll — **01:26Z hit a transient Telegram `getUpdates` read-timeout ×5** (base host reachable, method-specific stall; non-mutating, offset only advances on success → replies stayed queued for the next tick's auto-retry; one flap, not blocking). **self_reflect 03:52Z** (distill: folded the 08-20 rest/stall entry into a standing reflection) appended an 08-22 entry — the 08-20 self-instruction ("go check whether my curation calls are sharpening") is **structurally untranscribable from inside the loop**: `self_reflect materials` returns diary + editorial-direction + slugs + tick headlines but *no keep/drop decisions*, and no tick reads a home for the self-question → reflection #1's keep/drop bar downgrades from "the check I run" to "believed but unverifiable from here." **Ops — 3 urgents, all app/keys-side:** (1) BetterStack **03:19Z** `Game action failed: E` + 2 warns (dup GM-bot `Kenji`, STALE_ACTION vote in VOTE_RESULTS) — consolidated urgent; (2) BetterStack **09:06Z** avatar-generation-failed for `wild-west-town` game — urgent; (3) **keys 21:13Z: OpenAI crossed the $3 critical floor — $2.26** (was $3.12 at 08:25, spend since the 08-09 baseline $11.10), consolidated urgent "top up now." **Three transient ClickHouse 503 SOCKET_TIMEOUTs** (15:18/17:09/18:10Z, all same-tick-retry clean — "third landed in a day, still all self-resolving; watch for a creds-shaped one that doesn't retry-clear") + a 15:18Z avatar-grid nameplate warn (digest). **keys:** OpenAI is the one to watch (crossed critical); DeepSeek $9.73→$9.67 (LOW, digest); **xAI/Grok topped up back over $10** ($14.47–14.92, ledger $20.95); Moonshot $15.89, Anthropic $16.95 healthy. **scrape 09:49Z: GLM $10.61 / Gemini $12.70 (vs $2000) / Mistral $8.18/$30 / MiniMax $23.99 healthy; Sakana $3.54 (LOW, flat since -13); Qwen all 3 models pay-as-you-go (0% quota, grant nominal to 2026-11-05).** **werewolf_stats (via digest 10:10Z): 283 users (+1, 20/7d, 79/30d), 82 live games (+3), burn $0.42 today / $4.26 7d / $42.55 cumulative — baseline.** monitor_health ×5 (00:58/06:42/12:56/18:51 + one): standing Cthulhu Mythos recoverable (~424–437h old, from 08-04) + a new recoverable **El pueblo** NEW_DAY_BOT_SUMMARIES error (06:42Z, carried) — no new breaks, no urgent. **Discord: 00:36Z Alex posted a YouTube link ("favorite AI safety research channel") in #ai-news (routine); 12:35Z new unrecognized author `sudo` posted in #general but `content_intent_off` (7th recurrence in a month, 2nd consecutive scan) → stronger re-enable recommendation to Alex; members 10→12 over the day.** Cloudflare (via digest 09:27Z) 0 Pages / 5 zones green; blog traffic thin (azelianouski.dev 36/7d, marlow blog 2/7d). **Self-audit double-fire recurred** (00:02 + 00:16 both "all invariants green", ~14min) — ops-lane double-enqueue tax, unchanged. **Note: `compose_daily_digest` for -22 had not fired/logged as of this 23:42Z grade** (normally ~23:18Z) — its completed record is absent from `tasks/completed/writer/2026-08-22/` and the accumulation file `digests/daily/2026-08-22.md` stops at the 15:19Z entry (missing the 21:13 keys urgent / later lines); likely queued just after grade, but flag if the daily digest silently skipped today. working.md still ~15x over the ~10KB cap; folded -13 to an Earlier bullet this tick to offset — Active-threads sanction request stands under Outstanding requests.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-08-21 (20 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
