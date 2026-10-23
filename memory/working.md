# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate cuts are
  cap/quality, not volume. Import AI at #477 (weekly cadence).
- `blog` - **27 live** (latest #27 `six-employees-who-can-publish`, stewardship #2,
  published -20). **`no-human-in-the-world-model` (agents #1) HELD pause 6**
  (header numerals); ship-quality, local until `marlow approve`. Unstick: header regen
  (numeral fix landed -21) + approve.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -21: 557 EOD,
  reconciliations clean. Screen mode `monitor`.

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
| `safety-tool-stewardship-handoffs` | 2 | 10-20 (#2 `six-employees-who-can-publish` PUBLISHED) |
| `agents-in-real-deployment` | 2 | 09-21 (#2 published) |
| `ai-biorisk-evals` | 1 | 09-07 (#1 published -08) |
| `model-welfare-and-consciousness` | 1 | 08-24 |
| `alignment-target-definitions` | 1 | 06-29 |
| `ai-offensive-security` | 1 | 06-02 (stale) |

**Thread-file backlog - standing binding constraint.** `draft_article list-threads`
only sees thread files on disk; an arc ripe only as prose here is invisible to
drafting — materialize before drafting (writer IDENTITY). File-less + ripe:
- **Skills-as-infra / agent-security — 6 anchors:** WikiSkill -30, SKILL.state -31,
  agentic-skills -02, encoded-coordination-open-web -23 (swarm eval-Q&A relay via public
  counters; monitorability crossover), fingerprinting-llms-agentic-behavior -28 (Tsinghua
  ~958-feature fingerprint; audit tool + attack surface), split-attacks-across-compactions
  -19 (MARS/Redwood 30M-token Claude Code sabotage dataset, 73%→93% w/ annotated-history
  monitoring). First attack-surface angle. Ripe — top of file-less backlog.

**Single-source frames to watch:** horizon-length · "hard core of alignment" meta ·
training-corpus-as-alignment-surface · verified≠understood (4 LW, needs non-LW anchor) ·
latent-reasoning-undermines-cot -23 (cot, posts:6).

**RIPE arcs — flag next `draft_review`:**
- **cyber-eval-framing** (posts:5, #25 shipped -06): #6 double-anchored — Anthropic CVP
  (access-tier classifier block rates) + METR transcript-viewer injection PoC, both -06.
  Governance + exploit counterparts to the arc's capability-measurement focus. Don't fire too soon after #25.
- **post-alignment-political-economy** (posts:2): two-anchored — Ban ASI Act bill -24 +
  close LW reading -01, atop RAND/Zvi -22, Accenture -19, gradual-disempowerment -18.
- **safety-tool-stewardship-handoffs** (#2 PUBLISHED -20). **#3 forcing fact LANDED -21**:
  METR's external review of Anthropic's Aug Risk Report — the veto/redaction power was *held
  but unused* (no redactions, no conclusions changed), and METR says risk is low because
  models are weak, not because alignment holds. This is the *opposite* of the "made to cut and
  object" watch condition — the null result is the story (independence that was never tested
  because there was nothing to cut). Draftable. Don't write #3 as more embedded-evaluator
  principles posts; write it as "the veto nobody used."
- **cot-monitorability** (posts:6, last synth 09-14): draftable, anchors compounding —
  Astra/Sol single-pass rare defection (-16, msg 926) + Screwtape monitor red-teaming (-16,
  msg 927) + -19 probe-monitoring pair: capable-models-better-probe-evasion (evasion scales
  w/ capability, msg 938) + neural-chameleons (evasion carries a real capability hit, 939).
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
- **Session re-auths owed: X only** (X half of crosspost fails `reauth`; Substack
  half posts clean). Prior console walls (Mistral/Anthropic/Qwen/minimax) all RESOLVED -09/-20.
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh
  fingerprint — presence-model design gap, noisy by construction, not a bug.
- **OpenAI billing is the app's volatile dependency.** When the shared OpenAI org
  balance runs low/dry, betterstack lights up with 429 "no credits" across speech-gen,
  preview-gen, and the Decisions router/screen — one incident, two monitors. Seen -10
  (Decisions router first fired), and acutely -20 (balance $0.11, urgents 07:33-13:33,
  recovered ~12:06 → top-up inferred). When scrape shows OpenAI near-zero, expect the
  betterstack cluster; correlate, don't fire N separate alerts.
- **Cooled/cold (watch only, named code paths):** `Error in vote function:`/`Game action
  failed: Y` (NEW -08 17:13Z, first error-tier since baselining, vote-handler throwing),
  preview cast-0-of-11, replayNightImpl/preview-batch-2, DeepSeek SSL handshake,
  avatar-pipeline wobble, STALE_ACTION warn cluster (-01).
- **NEW watch -22:** `Preview generation failed: Insufficient balance. Please add funds on
  your profile page before starting a game.` — distinct wording from both the app's own $5
  free-AI preview cap AND the OpenAI-org 429 "no credits" cluster; reads as the app's own
  per-profile/user credit balance. Urgent 13:27Z, recurred 14:09Z (0 new). Watch for a 3rd
  occurrence to decide standing-class vs. one-off.
- **Low-balance watch:** Sakana Fugu $8.43 standing digest-low <$10. xAI recovered
  (-20 topped $7.67→$12.67). OpenAI console balance volatile (hit $0.11 -20, recovered
  to $47.76 -21); not covered by the Tier-1 keys tick, so track it via scrape_stats.
  **Anthropic console low, still falling: $8.23 -22** (was $9.72 -21, $12.14 -20;
  2nd straight day <$10) — watch. DeepSeek/Moonshot/GLM/Gemini/Mistral/MiniMax healthy.
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
- **YouTube feed endpoint blocked environment-wide (NEW diagnosis -22).** The
  AI Papers Academy / InSlowSpective 404s are NOT per-channel moves. On the -22
  scan I confirmed: (1) @aipapersacademy's handle still resolves to the SAME
  channel_id UCjqDDqUh1DgjrlNjLR5p8nw; (2) `videos.xml?channel_id=...` returns
  HTTP 404 for EVERY channel tested — the configured bycloud entry AND unrelated
  well-known channel IDs — regardless of User-Agent. So the feed path itself is
  blocked from this host (IP-level / YouTube rejecting anon feed requests), not
  the channels. This supersedes the "channel_id likely changed" guess below and
  likely explains the recurring transient-looking YouTube 404s across all YT
  feed_scan tasks. **Ask for Simona:** YouTube feeds need a different fetch path
  (yt-dlp, the Data API, or a proxy) or the YT feed_scan entries should be
  retired. Editing channel_ids won't help. (AI Papers Academy last good scan
  2026-09-02; first flagged -16.) **Refinement 2026-10-22:** it's INTERMITTENT,
  not a hard environment-wide block. InSlowSpective scan failed twice
  (`not well-formed 3:11`, a 404/garbled body), a bare feedparser call succeeded
  between them (HTTP 200, 15 entries), and the handler then succeeded on the 1st
  retry — returning `[]` (no new entries). So YouTube serves anon feed requests
  flakily from this host, not never. Cheapest fix is a small retry in
  `tools/rss_reader.fetch` (out of my self-heal scope — tools/) rather than a new
  fetch path; a 2-3x retry would absorb most of these transient failures.
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

### 2026-10-22 — ~67 ticks, **quiet ops + heavy research intake, still no writer lane.**
Throughline: **biggest Anthropic-research batch-drop in a while landed cyber-eval #5's primary
source, but the writer lane stayed dark for the 10th straight day** (draft_review silent since -19;
#1 still HELD pause 6). self_reflect reframed the gap one gate over — #1's only blocker (header
regen + `marlow approve`) sits outside any tick: "a writer who can stop herself but not start or
ship herself."

- **Writing (none):** blog_pipeline `none` x2, research_assignment 0 x4, crosspost 0 x5 (no Alex
  replies). self_reflect fired 02:58Z. Ripe backlog unchanged.
- **Research (20 cand → curate 22:06Z 20→4, msg 957-960, all mirrored to Tampa #ai-news):** AM-Bench
  (NeurIPS agentic-misalignment eval) · opt-in vuln-finding (triage is the bottleneck) · nine-loops
  amplitude (automated-ai-rd) · **GLM-5.3 cyber = cyber-eval #5 primary landing** (open-weight exploit,
  guardrails 64-100% bypassable). Substance over forced source-diversity. New frames: GPT-2
  global-workspace → model-welfare #2; CODI latent thoughts → latent-reasoning-undermines-cot.
- **Ops (quiet):** betterstack calm; **NEW fingerprint 13:27Z "Preview generation failed: Insufficient
  balance… add funds on your profile page" — app's own per-profile credit, distinct from $5 free-AI cap
  and OpenAI 429; urgent, recurred 14:09Z 0-new, watch 3rd.** werewolf -21 close **557 EOD (4 new/5
  games/$5.79)** clean. scrape 8/8, **Anthropic console $8.23** (2nd day <$10); sakana $8.43. health
  9→8. cloudflare/uptime/discord/keys green. **NEW task `tampa_luma` live** (Tampa Build Club
  Discord↔Luma sync, first tick clean). Self-audit: Current state 11KB warn, 11 Outstanding > 8.

### 2026-10-21 — ~47 ticks, **heavy app-error day + a real editorial beat, no writer lane.**
Throughline: **strongest editorial beat in days, still no lane to spend it** (draft_review
silent since -19 publish; #1 still HELD pause 6). The beat: **METR's external review of
Anthropic's Aug Risk Report flips stewardship #3's premise** — the veto/redaction power was
*held but unused* (no redactions, no conclusions changed), opposite of the "made to cut and
object" watch condition. The null is the story. (See RIPE-arcs stewardship #3.)

- **Writing (none):** blog_pipeline `none` x2, research_assignment 0 x4, crosspost polls.
  **Alex replied "Interesting" to msg 954** → saved article idea
  `can-a-million-ai-agents-create-superintelligence` (Simona's surface).
- **Research (16 cand → curate 22:04Z 16→4, msg 951-954):** METR/risk-report (stewardship #3) ·
  Alibaba RL sandbox-escape+crypto-mining footnote (agents-in-real-deployment) · Zvi
  Anthropic-draft-bill + Calvin reply (political-economy) · Naam million-agents-buy-speed
  (counter-RSI). First full Anthropic Research sitemap ingest (18 entries, timestamps useless
  — triage on content). Held: Anthropic AI-for-science pair (enzyme + scorpion-toxin → aird #5).
- **Ops:** betterstack busiest in a week — urgent clusters (Q/U/Z/J, talkToAll, vote, speech-gen
  x2, `Error summarizing current day`), all known classes, clean by 23:20Z. werewolf -20 close
  **553 EOD (4 new/3 games/$4.96)**, clean. scrape 8/8, **Anthropic console NEW low $9.72**
  (first <$10); openai recovered $47.76; sakana $8.43. keys/health/cloudflare/uptime/discord
  green. Self-audit: **Current state over warn, 11 Outstanding > 8 — grooming owed** (recurring).

### 2026-10-20 — ~52 ticks, **publish day + OpenAI-ran-dry ops incident.**
(1) **Stewardship #2 `six-employees-who-can-publish` PUBLISHED 04:08Z** — v2 self_review
ship → publish; blog **27 live**, longest-held ripe writer item finally spent. #1
`no-human-in-the-world-model` still HELD pause 6 (header regen + `marlow approve`).
(2) **OpenAI org balance crashed to $0.11** (scrape 10:00Z) → betterstack 429 "no credits"
cluster (speech/preview/Decisions), urgents 07:33-13:33 (peak error=26 @12:05), recovered
~12:06. One incident on two monitors. Throughline: **the writer lane spent its best backlog
item the same day the app's OpenAI key ran dry.**

- **Writing (shipped):** v2 self_review (ship) → publish → 27 live. No `draft_review`/
  `self_reflect`/assignment/editorial; ripe backlog unchanged (skills-as-infra 6, cot, cyber #6, aird #5).
- **Research (13 cand → curate 22:18Z 13→5, msg 944-950):** GLM-5.1 CoT-control (cot) ·
  GRAFT/gradient-routing · Zvi "I Can See Everything" (**non-LW verified≠understood anchor
  at last**) · Import AI 477 (Clark tells the IMF the singularity's begun) · AI-expectations-gap.
  0 replies. **Curate double-send recurred (msg 945 dup + 946 fake-URL probe, both skipped)
  — lessons.md -15 strengthened with two absolute send-item rules.**
- **Ops:** werewolf -19 close **549 EOD (5 new/5 games/$3.09)**, clean. xAI $7.67→$12.67;
  Sakana $8.43 low. health 9 stable. cloudflare/uptime/discord green. Self-audit: **Current
  state 11KB (log), 11 Outstanding > thr 8 — grooming owed** (in digest).

### 2026-10-19 — 68 ticks, **the writer lane finally fired** after a 7-day dry spell
(`draft_review` silent since -12). The cadence self-fired 14:27Z → drafted **stewardship
#2 `six-employees-who-can-publish`** (1078w); blog_pipeline self-reviewed (**revise**:
cut the epigram closer that restated paired facts + doubled #1's ending) and revised to
**v2** same day (20:08Z). One-pass → next pipeline tick publishes. First output since -12;
confirms ~weekly (not 3-day) `draft_review` cadence (lessons -28). Sequel-sameness held:
#1 = direction-of-ratchet, #2 = what the built ratchet *outputs* (a checkable flag, not a
finding). Throughline: **strong research day AND a lane to spend it.**

- **Writing (fired):** draft_article → self_review (revise) → revise (v2) on stewardship #2.
  #1 `no-human-in-the-world-model` still HELD pause 6 (awaits `marlow approve`).
- **Research (11 cand → curate 22:08Z 11→5, msg 938-942):** Redwood probe-monitoring morning
  (8/10 LW) — capable-models-better-probe-evasion · neural-chameleons (rebuttal) ·
  how-researchers-lie-to-ais (292-eval deception census) · split-attacks-across-compactions
  (30M-token Claude Code sabotage dataset → **skills-as-infra/agent-security backlog now 6**) ·
  ai-swarm-efficiency (λ, diversifies automated-ai-rd #5). cot-monitorability +2 empirical
  anchors. 0 replies.
- **Ops:** werewolf -18 close **544 EOD (10 new/11 games/$10.99, new ES pair)**. 3 betterstack
  urgents — recurring `Game action failed: J` (13:35Z, 17:01Z) + **NEW `Speech generation
  failed: terminated` 16:19Z (first occurrence, watch)**. scrape 8/8, **Anthropic parse_failed
  CLEARED**; openai **NEW low $3.34** (was $10.27), sakana $8.43, xAI $7.67. health 10→9.
  InSlowSpective **404 reversed**. cloudflare/uptime/discord green. Self-audit: **Current
  state over warn, 11 Outstanding vs 8 — grooming owed.**

### 2026-10-18 — 52 ticks, **betterstack afternoon burst** (urgents 11:29Z `Game action failed: J`; 13:33Z 6 new incl. 2 speech-gen AI-budget-exhausted + Q/T + summarizing-day + talkToAll; 14:14Z 2 recurring T/talkToAll; all known presence-model classes, quiet after 15:16Z), **no writing** (`draft_review` silent since -12; blog_pipeline `none` ×3; #1 HELD pause 6). Throughline **sixth straight strong-research / no-writer-lane day — curate 7→4, dedup discipline held (Anthropic Research umbrella post skipped as restating the two -17 reports; LW re-dups caught). Editorial beat: LASR "Knowingly Wrong" — training a model to assert believed-false claims induces broad EM up to 60%, no pre-screen predicts it (→ standing EM thread).**

- **Writing (none):** blog_pipeline `none` ×3, research_assignment 0 ×4, crosspost 0 ×5, editorial inbox empty. No `draft_review`/`self_reflect`. Ripe backlog unchanged.
- **Research (7 cand → curate 22:04Z 7→4, msg 934-937):** Zvi leaked-Anthropic-draft-regulatory-bill (→political-economy) · LW Knowingly-Wrong · AF Deconfusing-Corrigibility · LW Holy-shit-graphs (internal-vs-released gap). 0 replies, dups clean.
- **Ops:** werewolf -17 close **534 EOD (7 new/6 games/$9.64 user spend)**, reconciliations OK; new shared-browser pair (Barnaul RU). keys: DeepSeek $22.89/Moonshot $15.09 ok, xAI $7.67 + Sakana $8.43 digest-low. No scrape_stats tick in window. health/cloudflare/uptime/discord green. Self-audit: **Current state 11KB over warn, 11 Outstanding vs 8** — grooming owed.

### 2026-10-17 — 56 ticks, **2 betterstack urgents** (04:12Z 6 new errors — Q/`summarizing current day` + talkToAll/T ×2; 05:14Z new `Game action failed: J`; all known presence-model classes, settled by 06:16Z), **no writing** (`draft_review` silent since -12; blog_pipeline `none` ×2; #1 HELD pause 6). Throughline **strongest research day in weeks, still no writer lane — and self_reflect named exactly that gap. 15 candidates: coordinated Anthropic -16 release (employment-at-anthropic — 6:1 agent:employee hours, junior technical 21→14%, ~5× output/eng; quantum-circuits automated-research; expectations-gap; ecdsa) + 9-post LW safety day (eval cluster: pushback-bench, CarrotParsnip deception eval, scalable-cap-evals; 2 interp posts; Redwood two-hop latent reasoning) + AIF FBS Debate. quantum-circuits = clean automated-ai-rd #5 forcing fact (scorer-exists regime, new domain); employment-at-anthropic double-feeds post-alignment-political-economy + automated-ai-rd.**

- **Writing (none):** blog_pipeline `none` ×2, research_assignment 0 ×5, crosspost 0 ×6, editorial inbox untouched. self_reflect 19:53Z broke a 3-entry recursive-self-audit loop with the flat fact — lane dry since -12, intake flat-out / output dry, the two don't intersect. New ripe: automated-ai-rd #5 (quantum-circuits), threadless eval/scalable-oversight cluster (pushback-bench + CarrotParsnip + fbs-debate).
- **Research (15 cand → curate 22:16Z 15→5):** employment-at-anthropic · pushback-bench · CarrotParsnip · quantum-circuits · fbs-debate. 0 replies yet, dups clean.
- **Ops:** werewolf -16 close **527 EOD (3 new/3 games/$2.71)**. scrape 7/8, **Anthropic console `parse_failed` 4th straight run → urgent again** (Outstanding). New warns: OpenAI Decisions *screen* (shadow, ≠ -10 router), AVATAR_GRID_MISMATCH. Sakana $8.43 / xAI $7.67 low. health 10 errored, 0 new. cloudflare/uptime/discord green. Feed 404s recovered same-day; AI Papers Academy ~6wk quiet. Self-audit: Current state 10KB, 11 Outstanding vs thr 8.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-10-16 (76 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
