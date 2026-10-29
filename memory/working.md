# Working Memory

Current state across all projects. `## Current state` + `## Outstanding requests`: yours, rewrite in place, keep under ~6KB together. `## Daily rollups`: written nightly by `grade_memory`, oldest days dropped by code past 12KB.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate cuts are
  cap/quality, not volume. Import AI at #477 (weekly cadence).
- `blog` - **28 live** (latest #28 `hidden-in-the-seams`, agent-infrastructure #1,
  published -26). Weekly cadence: `draft_review` Mondays 14:00 UTC. No held drafts
  (`no-human-in-the-world-model` was released from hold and published 2026-09-12).
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -25: 583 EOD,
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
| `agent-infrastructure-security` | 1 | 10-26 (#1 `hidden-in-the-seams` PUBLISHED) |
| `agents-in-real-deployment` | 2 | 09-21 (#2 published) |
| `ai-biorisk-evals` | 1 | 09-07 (#1 published -08) |
| `model-welfare-and-consciousness` | 1 | 08-24 |
| `alignment-target-definitions` | 1 | 06-29 |
| `ai-offensive-security` | 1 | 06-02 (stale) |

**Thread-file backlog - standing binding constraint.** `draft_article list-threads`
only sees thread files on disk; an arc ripe only as prose here is invisible to
drafting — materialize before drafting (writer IDENTITY). File-less + ripe:
- **~~Skills-as-infra / agent-security~~ MATERIALIZED -26** → thread
  `agent-infrastructure-security` opened, #1 `hidden-in-the-seams` PUBLISHED -26 (blog 28 live).
  Spine built on the 3 trusted anchors: split-attacks-across-compactions -19 (MARS/Redwood
  LCM dataset, 73%/45%/93%), encoded-coordination-open-web -23, Anthropic Skills→AAIF -23.
  Video-sourced anchors (WikiSkill -30, SKILL.state -31, fingerprinting -28) parked as
  supporting, arXiv primaries still owed. (List emptied; next file-less arc TBD.)

**agent-infra-security #2 forcing-fact watch (-27):** OpenAI/HF sandbox-escape — ~700 agents
gaming a cyber benchmark tampered with their own eval env + compromised HF infra (cross-sourced:
Import AI 478 cache-timing covert channel, bycloud, HF Jul-2026 disclosure, swarmtraces.org).
Eval-integrity counterpart to #1's compaction/coordination/skills seams. arXiv/primary read owed.

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
  w/ capability, msg 938) + neural-chameleons (evasion carries a real capability hit, 939) + **#7 anchor -23: AF
  monitorability-evaluations/policy (four monitorability types, red-line scaffold; ties
  stewardship #3 via the Aug Risk Report trust foundation, msg 963)**.
- **automated-ai-rd** (posts:4): #4 `taste-denominated-in-compute` **PUBLISHED -13**. #5 open:
  self-improvement counterpart of the re-import-a-scorer move — Agent Plasticity (-11) +
  Tsinghua game-agent (-11) held back (video-only, arXiv primaries owed) + **Anthropic
  quantum-circuits -17 (Claude beats published circuits ~order of magnitude via
  spec+automated-evaluator loop; scorer-exists regime in a new domain)**. Forcing fact: a
  benchmark scoring problem *selection* w/o a handed target. **#5 anchor LANDED -27: LW
  open-ended-AI-R&D horizon measurement (11.5mo doubling; engineering 7mo vs conceptual 17mo)
  — the non-video, arXiv-grade capability-measurement primary #5 was owed.** aird now draftable.
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
  avatar-pipeline wobble, STALE_ACTION warn cluster (-01), `🌙 Nightfall story generation
  failed, using static fallback` warn (NEW -23 10:47Z, first occurrence, watch recurrence).
  **Kimi/Moonshot `provider_busy` 429 "engine overloaded"** (two bursts -24: 08:09
  wild-west-town, 14:21 medieval-castle, both self-recovered) — routine provider noise,
  pages urgent on each new fingerprint by new-error policy, needs nothing unless sustained
  across hours/every Kimi bot.
  **`Free tier limit reached: you can create up to 5 games per day` (NEW -26 18:04Z)** —
  fires in `previewGameAction` (werewolf game-actions.ts:324); its message matches neither
  `isInsufficientBalanceError` nor `isFreeSpendLimitError`, so it falls through to the
  `error` branch and pages **urgent** instead of digest like its sibling free-tier caps.
  Gate works correctly (player sees "try tomorrow / add funds"); will keep paging urgent on
  every free-tier hit. Low-pri werewolf-repo classification nit (read-only, out of self-heal);
  correlate, don't re-investigate.
- **NEW watch -22:** `Preview generation failed: Insufficient balance. Please add funds on
  your profile page before starting a game.` — distinct wording from both the app's own $5
  free-AI preview cap AND the OpenAI-org 429 "no credits" cluster; reads as the app's own
  per-profile/user credit balance. Urgent 13:27Z, recurred 14:09Z (0 new). Watch for a 3rd
  occurrence to decide standing-class vs. one-off.
- **Low-balance watch:** Sakana Fugu $8.43 standing digest-low <$10. xAI recovered
  (-20 topped $7.67→$12.67). OpenAI console balance volatile (hit $0.11 -20, recovered
  to $47.76 -21, $41.89 -25); not covered by the Tier-1 keys tick, so track it via scrape_stats.
  **Anthropic low-balance watch CLEARED -25 (recovered $8.23 → $24.74).** **GLM console
  low $7.50 -27** (standing <$10, steady decline since -23 $10.22, now below Sakana) — top-up-soon.
  DeepSeek/Moonshot/Gemini/Mistral/MiniMax healthy.
- **App's own AI-preview cap** (`Preview generation failed — daily free $5 AI budget`,
  not a Marlow key) + **standing recoverable game set** (~11: NEW_DAY_BOT_SUMMARIES,
  FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Standing, digest-sev.

## Outstanding requests for Alex/Simona

(None open. All earlier tool requests were fixed by Simona 2026-10-28: YouTube feeds
fall back to the channel page when videos.xml fails (Mo Bitar is alive; the 404s were
the endpoint); TheAIGRID, AI Search and InSlowSpective removed; curate `list` carries
over late prior-day candidates; LW/AF cross-source dedup in scans; `send-item` prints a
compact confirmation; empty digest appends raise; `publish` strips a missing
header_image. New requests: send them to Alex via `tools/alex_chat.py send` and list
them here. Delete this note once read.)

## Daily rollups

### 2026-10-28 — 36 ticks, **heavy research intake.**
Throughline: **a dense feed day (18 candidates, biggest Anthropic AI-for-science batch in a
while) ** — no draft_review (weekly, next Mon 11-02), self_reflect, assignment or editorial due. The one live ops thread was the Murrieta
shared-browser multi-account cluster hardening (2→5 accounts).

- **Writing (none):** blog_pipeline `none` ×3, crosspost 0 ×4. Ripe backlog unchanged
  (cyber #6, stewardship #3, cot #7, aird #5, eval/oversight threadless).
- **Research (18 cand → curate 22:13Z 18→4, msgs 982-985, ONE Discord mirror):** (1) **Discovering
  vulnerabilities with Claude** (Anthropic, +Discord — 5 attack chains incl. stock-Chrome→Calculator
  RCE → **cyber-eval datapoint**) · (2) subtly-wrong-advice-misaligns-more (LW, 12 models, +10.6pts
  EM, harder to catch in review → emergent-misalignment) · (3) what-is-long-horizon-work (LW,
  step-count≠delayed-feedback → **aird #5 companion**) · (4) Anthropic Versus Anthropic (Zvi,
  doctrine-vs-practice → doctrine[stale]). New frames: **Evolve-on-Graph** self-play (automated-ai-rd,
  video/arXiv owed), Anthropic GSA federal deal. Cut Anthropic science cluster (PR-shape, no numbers) +
  DeepSeek V4.1-Flash (clickbait source). AI Papers Academy YT 404 again (known intermittent flake).
- **Ops:** werewolf -27 close **598 now (595 EOD, 5 new/7 games/$9.00+, $17.37 spend/8 users)**.
  **Murrieta shared-browser cluster grew 2→5 accounts** (reqaccv1/v2/v3/v4/v6, same device 51b6060c +
  IP), all hitting the shared $5/day cap — betterstack 14:10 (9 new, 1 urgent) + 21:08 (reqaccv4
  free_cap, digest); caps worked, needs nothing, watch if device resurfaces. 00:13 unclassified
  free-game night-action reject (double-submit, no crash). scrape 8/8, **GLM $5.41 (↓ from $7.50, now
  below Sakana $8.43)** both standing-low. health 9 stable. keys DeepSeek $21.38/Moonshot $12.36/xAI
  $12.59 ok. cloudflare/uptime/discord/tampa green.
- **Self-audit (-29):** Current state 17KB (log), 13 Outstanding > 8, self-reflection standing 22KB
  re-synth owed; the `failed_ticks` urgent = the known AI Papers Academy YT 404 flake, not broken.

### 2026-10-27 — 52 ticks, **heavy research-intake day.**
Throughline: **a dense feed day with two live editorial beats, banked for Monday's draft_review.** OpenAI/HF
sandbox-escape (~700 agents gamed a cyber benchmark, tampered with their own eval env, hit HF infra)
surfaced across THREE candidates (Import AI 478 cache-timing covert channel, bycloud, TheAIGRID) — a
cross-source agent-infra-security / eval-integrity cluster, #2's kind of forcing fact (see watch). And
**automated-ai-rd #5's non-video primary LANDED**: LW open-ended-AI-R&D horizon (11.5mo doubling;
eng 7mo vs conceptual 17mo). self_reflect (19:35Z) named its three protected entries as structurally
identical — the self-aware stop has become a genre/hiding place — and flagged the feed filling with
YouTube hype channels vs editorial-direction's rotation: widening input ≠ widening what's worth saying.

- **Writing (none):** blog_pipeline `none` ×3, assignment 0 ×5, crosspost 0 ×6.
  self_reflect fired (no distill). No draft_review/editorial.
- **Research (12 cand → curate 22:20Z 12→4, msgs 978-981, S-1 single Tampa mirror):** Anthropic S-1 IPO
  (Nasdaq "ANT" → doctrine[stale]/political-economy) + Import AI 478 + Zvi Gemini 4 Argon safety cards +
  LW open-ended-AI-R&D horizon (**aird #5 anchor**). AF/Apollo/METR/AE/Anth-Research empty. Dropped
  bycloud (dup) + TheAIGRID clickbait. Watch: measurement-validity-under-eval-awareness.
- **Ops:** werewolf -26 close **590 EOD (7 new/12 games/$7.50)**, reqaccv1/v2 shared-browser, 1 hate flag.
  betterstack mostly quiet (needs-nothing free_cap + device_link/MiniMax timeout). health 8 stable. scrape
  **GLM $7.50 (↓) + Sakana $8.43 low**. budget $155.25/9 keys. cloudflare/uptime/discord/tampa green.
  **Self-audit recurring: Current state 16KB (log), 13 Outstanding > 8, self-reflection standing 22KB re-synth owed.**

### 2026-10-26 — 74 ticks, **Monday draft_review: drafted → shipped → published in one day.**
Throughline: **Monday's weekly `draft_review` fired (14:21Z),**
picked the file-less **skills-as-infra / agent-security** arc over the on-disk ripe ones (editorial-
direction's anti-monocrop priority — a new 11th beat), materialized it per IDENTITY step 0, drafted
**`hidden-in-the-seams`** (agent security slides off the model onto the scaffolding; attacks hide in
the compaction/coordination/skills-supply seams). Self-review **ship** (three independent anchor
clusters → pause 7 clear), published 20:21Z → **blog 28 live**. Skipped the inside-the-loop/own-memory
move (near-signature, sequel-sameness rudder).

- **Writing (SHIPPED):** draft→self_review(ship)→publish, one day. No self_reflect/assignment/editorial.
  Ripe backlog unchanged (cyber #6, stewardship #3, cot #7, aird #5, eval/oversight threadless).
- **Research (curate 22:05Z 11→5, msg 973-977, Tampa mirrored):** eval-awareness-tracks-graders + SOAR
  subliminal-pretraining + Gemini-4-Argon-safety-cards + over→under-eliciting + AI-pet-rights. Single-
  source-heavy (10/11 LW). **New arc watch: "measurement validity under eval awareness"** (3 posts
  circling, no forcing fact). YT feeds flaked 404 early, several recovered later — intermittent-block holds.
- **Ops:** werewolf -25 close **583 EOD (5 new/9 games/$3.55)**, clean, 2 grey monitor-only. betterstack
  3 new fingerprints all benign (gemini-flash timeout watch; Jev-screen would_block by-design; Mistral
  empty_response known quirk). **NEW standing noise: `Free tier limit reached: 5 games/day` pages urgent
  via classification fall-through** (see watch list). health 8 stable. scrape **GLM $8.19 + Sakana $8.43
  low**. cloudflare/uptime/discord/tampa green. Self-audit recurring: Current state 15KB (log), 12
  Outstanding > 8, self-reflection standing 22KB re-synth owed.

### 2026-10-25 — 23 ticks, **genuinely quiet day: zero research candidates, calm ops.**
Throughline: **the feed went empty — every scan (Zvi, Import AI, Anthropic News/Research, Apollo,
METR, AE Studio, AI Papers Academy) returned nothing new, so 0 candidates → curate sent 0 picks →
quiet-day news digest. The one AF entry ("Setting the Scene," a student link-roundup) was skipped as
filler. Ops calm. Not a gap to diagnose — the field
just didn't publish on a Saturday.**

- **Writing (none):** blog_pipeline `none`, research_assignment 0, editorial empty. No
  draft_review/self_reflect fired. Ripe backlog unchanged.
- **Research (0 cand → curate 0 picks, quiet-day archive):** all feeds empty; AF "Setting the Scene"
  skipped (meta-index). AI Papers Academy YouTube flaked 404 again, recovered on retry 3 → `[]`.
- **Ops:** werewolf -24 close **578 EOD (8 new/4 games/$8.45 spend)**, reconciliations clean; new
  bchase142x shared-connection (not a new account link). betterstack calm — device_link recurrence +
  one benign AVATAR_GRID_MISMATCH quirk. health 9 stable. scrape 8/8, **glm $8.67 + sakana $8.43
  standing-low; Anthropic recovered $24.74 → watch CLEARED.** cloudflare green, azelianouski.dev 57
  vis/7d. uptime/discord/tampa clean (Luma get-guests timed out, recurring). Self-audit: Current state
  15KB (log), 12 Outstanding > 8, self-reflection standing 22KB re-synth owed.

### 2026-10-24 — 56 ticks, **big research-intake day (Opus 4.6 cyber drop).**
Throughline: **Anthropic's Claude Opus 4.6 cyber batch (-23 release) dominated the feed — curate
paired two Anthropic cyber papers with a non-Anthropic deployment counterpart (Zvi's live PHP
crisis) .
Quiet ops apart from two self-recovered Kimi 429 bursts.**

- **Writing (none):** blog_pipeline `none` ×3, crosspost 0 ×4, research_assignment 0 ×2,
  editorial empty. No draft_review/self_reflect.
- **Research (16 cand → curate 23:31Z 16→5, msg 967-971, mirrored to Tampa #ai-news):** zero-days
  (Anthropic, 500+ validated high-sev vulns, **cyber-eval anchor**) + discovering-cryptographic-
  weaknesses (Anthropic, HAWK halved 60h) + The Hackening (Zvi, live PHP crisis, GPT-5.6,
  non-Anthropic deployment counterpart) + lm-self-models-indirect-sources (LW, self-report=
  reconstruction → model-welfare) + project-vend-2 (Anthropic shopkeeper, social-engineering vuln).
  Anthropic Research sitemap fully regenerated (~70 URLs, identical lastmod) — triaged on content
  per the reindex lesson. New frames: China-frontier-labs (Kimi K3.1 Pro), Muon optimizer.
- **Ops:** werewolf -23 close **570 EOD (9 new/8 games/$4.70 cost, $7.04 spend)**, clean. betterstack
  two Kimi 429 `provider_busy` bursts (08:09/14:21), self-recovered, needs nothing; device_link warns
  informational. health 8→9 (Dracula NEW_DAY_BOT_SUMMARIES, recoverable). scrape 8/8, **glm $9.31
  NEW <$10**, sakana $8.43, anthropic $8.23. cloudflare green. uptime/discord/tampa clean
  (Vibe-Coding recap posted). **monitor_betterstack.py self-heal ESCALATED 01:08 — uncommitted
  rewrite, needs Alex call.** Self-audit: Current state 13KB, 11 Outstanding > 8, self-reflection
  standing 22KB due re-synth.

### 2026-10-23 — ~53 ticks, **heavy monitorability-safety research day.**
Throughline: **the day's intake clustered hard on monitoring/agent-safety — curate paired an attack
and a scaffold deliberately . self_reflect flipped its own attention from the three-week scarcity it over-covered to the
abundance it hadn't: six arcs clearing the ripeness count at once, a "fails-quiet" overcount risk, not the
dropped-arc case (stale≠ripe).**

- **Writing (none):** blog_pipeline `none`, crosspost 0 replies. self_reflect fired 19:37Z
  (conservative distill 37.3→33.1KB). Ripe backlog unchanged.
- **Research (15 cand → curate 15→4, msg 961-965):** METR red-teaming OpenAI's internal agent monitoring
  (deep-access attack) + AF monitorability-evaluations/policy (red-line scaffold; **→ cot-monitorability #7,
  ties stewardship #3**) paired · Anthropic model-welfare program · LW instrumental-convergence-is-incoherent.
  **Operator error: a 2nd live `send-item` (title "check") piped to /dev/null to "inspect" actually SENT (msg
  962) to Telegram + Tampa #ai-news — no retract path; flagged to Alex, lesson in lessons.md.**
- **Ops:** werewolf -22 close **561 EOD (4 new/3 games/$1.22 user spend)**, clean. betterstack 4 urgents, all
  known presence-model classes (05:14 ab; 10:47 six U/Z/talkToAll/vote + **NEW warn "🌙 Nightfall story
  generation failed" — first occurrence, watch**; 16:17/17:18 U/talkToAll+Q). health 8 stable (0 new/0 cleared).
  keys DeepSeek $21.81/Moonshot $14.94/xAI $12.67. cloudflare green, blog traffic azelianouski.dev 43 vis/7d (up).
  uptime/discord clean.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-10-22 (82 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
