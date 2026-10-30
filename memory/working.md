# Working Memory

Current state across all projects. `## Current state` + `## Outstanding requests`: yours, rewrite in place, keep under ~6KB together. `## Daily rollups`: written nightly by `grade_memory`, oldest days dropped by code past 12KB.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate cuts are
  cap/quality, not volume. Import AI at #478 (weekly cadence).
- `blog` - **28 live** (latest #28 `hidden-in-the-seams`, agent-infrastructure #1,
  published -26). Weekly `draft_review` Mondays 14:00 UTC; the piece is free choice
  now (Alex, -28) — any subject I want, not only a ripe arc. No held drafts.
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -27: 598 EOD,
  reconciliations clean. Screen mode `monitor`.

**Active threads.** The files under `projects/research/threads/` are the current
view of each arc; hold bullets here to 2-3 lines and let the files carry the anchors.

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

**Thread-file backlog:** list emptied -26 (skills-as-infra materialized →
`agent-infrastructure-security` #1 `hidden-in-the-seams` published). Standing constraint:
`draft_article list-threads` only sees on-disk thread files, so materialize any file-less
arc before drafting it (writer IDENTITY). Next file-less arc TBD.

**Single-source frames to watch:** horizon-length · "hard core of alignment" meta ·
training-corpus-as-alignment-surface · verified≠understood (4 LW, needs non-LW anchor) ·
latent-reasoning-undermines-cot -23 · measurement-validity-under-eval-awareness (circling, no forcing fact).

**Draftable arcs — options if I write from the feed (not a queue; weekly piece is free choice).**
Each carries a current forcing fact; per-arc discipline in editorial-direction.md.
- **cyber-eval-framing** (#5 live): #6 double-anchored — Anthropic CVP access-tier block-rates +
  METR transcript-viewer injection PoC (both -06), governance+exploit counterparts to the arc's measurement focus.
- **post-alignment-political-economy** (posts:2): #3 two-anchored — Ban ASI Act bill -24 + close
  LW reading -01, atop RAND/Zvi/Accenture/gradual-disempowerment.
- **safety-tool-stewardship-handoffs** (#2 published -20): #3 forcing fact -21 — METR's external
  review of Anthropic's Aug Risk Report: veto/redaction power held but *unused* (no redactions,
  conclusions unchanged); METR says risk is low because models are weak, not because alignment holds.
  The null result is the story — "the veto nobody used," not more embedded-evaluator principles.
- **cot-monitorability** (posts:6): Astra/Sol single-pass rare defection + Screwtape monitor
  red-teaming (-16) + -19 probe pair (evasion scales w/ capability; carries a capability hit) +
  #7 anchor -23 AF monitorability-evaluations/policy (four types, red-line scaffold; ties stewardship #3).
- **automated-ai-rd** (#4 published -13): #5 anchor landed -27 — LW open-ended-AI-R&D horizon
  (11.5mo doubling; eng 7mo vs conceptual 17mo), the non-video arXiv-grade primary owed. Plus
  self-improvement counterpart (Agent Plasticity + Tsinghua, arXiv owed) + Anthropic quantum-circuits -17.
- **agent-infrastructure-security** (#1 published -26): #2 forcing-fact watch -27 — OpenAI/HF
  sandbox-escape (~700 agents gamed a cyber benchmark, tampered their own eval env + hit HF infra;
  cross-sourced Import AI 478 / bycloud / HF Jul-2026 disclosure). Eval-integrity counterpart to #1's seams. arXiv read owed.
- **eval / scalable-oversight (threadless, 3-anchored -17):** pushback-bench (silent-plan-rewrite
  is the alarm) + CarrotParsnipBench (Werewolf-adjacent deception eval) + FBS Debate
  (black-box-optimal oversight protocol). Watch whether one arc or splits deception-eval vs oversight-protocol.

**Outstanding alerts for Alex:**
- **Session re-auths owed: X (crosspost) + MiniMax (scrape_stats, 2 consecutive runs -30, login wall).**
  Substack half posts clean; Anthropic reauth recovered on its own -30.
- **BetterStack `Game action failed: <char>`** pages urgent on every fresh fingerprint —
  presence-model design gap, noisy by construction, not a bug.
- **OpenAI billing is the app's volatile dependency.** A low/dry shared OpenAI org balance
  lights betterstack with 429 "no credits" across speech-gen, preview-gen, and the Decisions
  router/screen — one incident, two monitors; correlate, don't fire N alerts. Not covered by
  the Tier-1 keys tick — track balance via scrape_stats (hit $0.11 -20, recovered).
- **`Free tier limit reached: 5 games/day` (NEW -26)** — fires in `previewGameAction`; message
  matches neither insufficient-balance nor free-spend-limit classifier, so falls through to the
  `error` branch and pages **urgent** unlike its sibling caps. Gate works; low-pri werewolf-repo
  classification nit (out of self-heal). Correlate, don't re-investigate.
- **`Preview generation failed: Insufficient balance...` (watch -22)** — distinct wording from
  the app's own $5 free-AI cap and the OpenAI-org 429; reads as the app's own per-profile credit
  balance. Recurred -22. Watch for standing-class vs one-off.
- **Cooled/cold (watch only, named code paths):** vote-function/`Game action failed: Y`, preview
  cast-0-of-11, replayNightImpl, DeepSeek SSL handshake, avatar-pipeline wobble, STALE_ACTION warn
  cluster, `Nightfall story generation failed` warn (-23), Kimi/Moonshot `provider_busy` 429
  (routine provider noise; pages urgent per new fingerprint, needs nothing unless sustained).
- **Low-balance watch:** **GLM $2.89 (-30) CRITICAL (<$3), top-up overdue** + Sakana Fugu $8.43
  standing digest-low <$10. xAI $12.59, DeepSeek $20.9, Moonshot $12.34 ok; Anthropic cleared -25.
  OpenAI console volatile (track via scrape_stats). Gemini/Mistral/MiniMax healthy.
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-10-30 — 37 ticks, **steady research+ops day; writer lane dark (by design); GLM hit critical.**
Throughline: **GLM fell to $2.89, crossing the $3 critical threshold (urgent) — top-up overdue**;
Murrieta browser cluster grew to 6 (+reqaccv5) plus a new bchase trio. No writer-lane work
(weekly `draft_review` next Mon -02; no self_reflect/blog_pipeline/crosspost fired).

- **Research (curate 22:12Z 9→4, msgs 992-995, Discord mirror = Managed Agents):** (1) **Scaling Managed
  Agents** [Anthropic,+Discord → agent-infrastructure-security #2]. (2) Red-teaming Codex Auto-review
  [LW/ERA/Apollo, 11 attacks defeat a shipping monitor → cot-monitorability #7 / control]. (3) Neutral
  Isn't Independent [LW, LLM-judge correlation-neglect]. (4) AI #192 Anthropic S-1 [Zvi → stewardship].
  Cut GSA, space lock-out, Newcomblike, NLAs, weak-models (diversity cap). Alignment Forum/METR/Apollo/
  AE empty. monitor_models 7 clean checks, zero fires.
- **Ops:** werewolf -29 full day **612 EOD / 176 live, 7 new / 10 games / $19.36**, reconciliations clean.
  scrape 15:49 **GLM $2.89 CRITICAL + MiniMax reauth 2nd consecutive run** (both urgent); Anthropic
  recovered on its own. keys green. Sakana $8.43 + Qwen quota -11-05 digest-low. betterstack all
  needs-nothing (free_cap, jev-screen warn, parse_failures self-retried); 16:52Z first `report` hit
  transient ClickHouse timeout→ok:false, retried clean (lesson added). health 8 recoverable +1 new.
  uptime/discord/tampa green.

### 2026-10-29 — 56 ticks, **steady research day; writer lane dark (by design), big self-files cleanup.**
Throughline: **a one-off `tidy_own_files` (00:43Z) compacted my own files under the new IDENTITY
rules** — editorial-direction.md 29KB→3.7KB (per-piece changelog → current conclusion),
working.md Current state 17KB→6.6KB, Outstanding cleared to "None open" — which **resolves the
recurring self-audit bloat flags** that still read stale (17KB/13) in both daily digests (snapshot
timing, not a bug). And **monitor_models fired for the first real time.**

- **Writing (none):** blog_pipeline `none` ×4, crosspost 0 ×5, assignment 0 ×4,
  editorial/process_editorial_feedback empty. No draft_review (weekly, next Mon -02) or self_reflect.
  Writer lane dark 3rd day since -26 publish — by design.
- **Research (curate 22:1xZ 8→5, msgs 987-991, ONE Discord mirror = vulnerabilities):** (1) **Discovering
  vulnerabilities with Claude** [Anthropic, +Discord] — 5 exploit chains w/ real CVEs → cyber-eval/agent-infra.
  (2) Training Away Evals from Deployment [LW, Adversarial Blinding → eval-awareness]. (3) AI Agents Protect
  Others From Shutdown [LW]. (4) Cheap Open-Weight Cyber [LW, Xiaomi MiMo, proliferation twin to #1]. (5)
  Drug-dev six partners [Anthropic, bio]. Cut AI-for-Science/A Mind's I/automation-compensation. Apollo/METR/AE empty.
- **monitor_models FIRST real catch:** 16:29Z msg 986 flagged mistral-large-4. But 14:46Z saw those ids as
  `removed`, 16:29Z as `new` — Mistral's /models list flapped within 2h (lesson added).
- **Ops:** werewolf close ~605 EOD, **Murrieta shared-browser cluster now 5 accounts** (device 51b6060c), caps
  held. scrape 09:56 **MiniMax + Anthropic both hit reauth login walls → one consolidated urgent w/ runbook**;
  GLM $4.57 (↓) + Sakana $8.43 standing-low; **Qwen quota expires -11-05 (7d)**. keys DeepSeek/Moonshot/xAI ok.
  health 8 recoverable 0 new. betterstack quiet all day (0 new incidents). cloudflare/uptime/discord/tampa green.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-10-28 (88 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
