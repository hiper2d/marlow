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
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -31: 626 EOD,
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
- **calories/poll_food BLOCKED — `MARLOW_FITNESS_BOT_TOKEN` (+ likely `MARLOW_FITNESS_CHAT_ID`)
  missing from the launchd plist (NEW -11-02).** poll_food wakes (stale subtask from -06-16 just
  fired) and fails at `fitness_bot._token()`; handler is wired right (`import_plist_env` line 36),
  the plist `EnvironmentVariables` just never got the fitness keys. Whole calories ingest path is
  unprovisioned. Fix = Alex adds both keys to `com.marlow.tick.plist` (same move as the Poker CH
  creds). Out of self-heal scope (plist). Urgent-notified -11-02 00:25Z.
- **Poker Betterstack monitor — RESOLVED -01 (no open ask).** Alex added the dedicated US-cluster
  `BETTERSTACK_POKER_CH_*` creds to the plist; first scan baselined 22:58Z on its own connection
  (`ok:true`, 0/0, `source_empty:true` — low-traffic source, not a fault). Multi-day blind closed.
- **Session re-auths owed: X (crosspost).** MiniMax's -30 login-wall reauth cleared on its own by -31
  (now reads `parse_failed`, 1st failing run — watch next run before re-invoking the runbook).
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
- **Low-balance watch:** GLM recovered to $17.49 (-31, topped up) + Sakana Fugu $8.43
  standing digest-low <$10. xAI $12.59, DeepSeek $20.9, Moonshot $12.34 ok; Anthropic cleared -25.
  OpenAI console volatile (track via scrape_stats). Gemini/Mistral healthy; MiniMax parse_failed (1st run, watch).
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-01 — 58 ticks, **quiet research+ops day after a ~7h overnight dormant window; writer lane dark (by design).**
Throughline: uneventful — feeds slow, ops all-green, two routine betterstack timeout incidents (both
self-recovered). Laptop slept overnight; 06:00Z daily_digest covered the catch-up. Several late-day
duplicate fires (2nd daily_digest, dup curate + grade_memory) all correctly no-op'd per dedup lessons.

- **Research (curate 22:13Z 5→4, msgs 1002-1005, Discord mirror = India pick):** (1) SAE sanity-checks
  rebuttal (2) generalized belief states [both LW interp, paired] (3) Regulate-the-Deployment/Trusted
  Deployers [LW governance] (4) India policymaker talk [AF,+Discord — retells ~700-agent HF-hack + collusion
  board; **feeds agent-infrastructure-security #2 forcing-fact watch**]. Cut Against-SURA. Import AI still
  #478; Zvi/Anthropic/Apollo/METR/AE quiet. monitor_models 8 clean checks, zero fires.
- **Ops:** werewolf -31 **626 EOD, 5 new / 5 games (3 by new) / $3.92**, reconciliations clean, $0.00 ledger
  gap; screen 0 would-block, 1 grey; MTD reset on 10→11 rollover. betterstack 2 error-level timeouts (GLM,
  mistral-large-4) — both self-recovered, urgent per error-level rule. **Poker betterstack: creds added to
  plist late-day; first US-cluster scan baselined 22:58Z (0/0, empty source) → standing blind RESOLVED.**
  scrape: GLM $17.08, Sakana $8.43 low, MiniMax `parse_failed` 2nd run, Qwen grants expire -05; keys green.
  health 6 recoverable stable. uptime/cloudflare/discord/tampa/poker all quiet-green.
- **Writer:** dark by design (draft_review Mon -02). self_reflect short diary; blog_pipeline empty; crosspost
  answered Alex greeting msg 1000 (reply 1001).

### 2026-10-31 — 53 ticks, **steady research+ops day; writer lane dark (by design); Poker betterstack blind all day.**
Throughline: **the Poker Betterstack monitor failed on all three scans** (14:24 / 16:50 / 20:16Z,
`CLUSTER_DOESNT_EXIST`) — the dedicated `BETTERSTACK_POKER_CH_*` creds commit be9dcf1 added were never
put in the plist, so it falls back to the shared eu-fsn-3 Werewolf connection and can't see Poker's
US-cluster table. Known cause, Alex-only fix; urgent re-fired each scan, not re-diagnosed. No writer
work (weekly `draft_review` next Mon -02).

- **Research (curate 22:40Z 5→4, msgs 996-999, Discord mirror = Persona Geology):** (1) **Persona
  Geology** [LW, +Discord — 134 character-training LoRAs, five-factor weight-space structure]. (2)
  Enabling independent research [Anthropic — Clio→Insights opened to SALT/Oxford/METR, ~250K convos
  each, aggregate released → stewardship arc]. (3) Advocacy Gap in Intl AI Verification [LW]. (4)
  Microdosing the spirit of Anthropic [LW, lab-insider epistemics]. Cut 2017-AI-Risk post-mortem
  (2nd reflective LW of the day, selective at 4). Feeds otherwise quiet: Import AI #479 not out,
  Alignment Forum / Apollo / METR / AE empty; Anthropic sitemap found enabling-independent-research new.
  monitor_models 8 clean checks + a Qwen `pre-mock_*` test-id flap (noise per YAML rule).
- **Ops:** werewolf -30 day **9 new users / 13 new games (8 by new) / $7.76 created-cost**,
  reconciliations clean, content screen 0 would-block (13 grey, all bchase sexual-themed). scrape 10:00
  **GLM recovered $17.49 (topped up from $2.89 critical) + MiniMax downgraded reauth→`parse_failed`**;
  Sakana $8.43 + Qwen 5d-to-expiry standing-low. keys green (DeepSeek $20.92, Moonshot $12.34, xAI $12.59).
  betterstack (werewolf) quiet all day, 2 device_link informational incidents. health 6 recoverable stable.
  uptime/discord (1 msg, Alex himself)/tampa green.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-10-30 (90 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
