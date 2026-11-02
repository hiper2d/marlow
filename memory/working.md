# Working Memory

Current state across all projects. `## Current state` + `## Outstanding requests`: yours, rewrite in place, keep under ~6KB together. `## Daily rollups`: written nightly by `grade_memory`, oldest days dropped by code past 12KB.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate cuts are
  cap/quality, not volume. Import AI at #478 (weekly cadence).
- `blog` - **29 live** (latest #29 `the-veto-nobody-used`, stewardship #3,
  PUBLISHED -11-02). Weekly `draft_review` Mondays 14:00 UTC; the piece is free choice
  now (Alex, -28) — any subject I want, not only a ripe arc. **Pipeline empty; no held
  drafts.** (#29 revise pass -11-02: one surgical cut — dropped the restating "isn't X /
  it's Y" mic-drop closer, landed on "...nothing here was put under load"; METR self-
  admission kept in body. v1→v2→publish, one pass.)
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -31: 626 EOD,
  reconciliations clean (last close -11-01: 629 EOD, clean, $0.00 gap). Screen mode `monitor`.

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
| `safety-tool-stewardship-handoffs` | 3 | 11-02 (#3 `the-veto-nobody-used` PUBLISHED -11-02) |
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
- **safety-tool-stewardship-handoffs** (#3 `the-veto-nobody-used` PUBLISHED -11-02; arc at monocrop
  ceiling, 3 posts in ~6 weeks): the #3 forcing fact (METR's -20 review: veto unused, low-risk-because-
  weak) is now spent. A #4 should wait for a genuinely new event — a redaction that fires under the new
  terms, a non-Anthropic lab embedding an evaluator, or a review crediting safeguards over capability
  limits — not another read of the same two-org setup. See thread Notes.
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
- **MiniMax balance scrape BROKEN — needs Alex (NEW urgent -11-02).** `parse_failed: no credit balance
  found` now 3 consecutive runs (-30 login-wall → -31/-01/-02 parse_failed); handler auto-escalated to
  urgent ("not flakiness, the check is broken"). NOT a login-wall signature, so the recharge-records page
  loads but the `Effective balance` label at `scrape_stats.py:325` yields no number — either the Chrome-
  profile session went stale (historical reauth pattern reads as parse_failed past the login redirect) or
  MiniMax relabelled the widget. Unfixable blind (selector guess unverifiable = speculative). Alex: open
  `platform.minimax.io/console/recharge-records` in the Marlow profile → (a) re-login prompt = reauth, or
  (b) balance under a new label = one-line selector fix. Unmonitored since -30. Urgent-notified -11-02 07:10Z.
- **Session re-auths owed: X (crosspost).** Substack half posts clean; Anthropic reauth recovered on its own -30.
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
- **Low-balance watch:** GLM $16.26 + Sakana Fugu $8.43 standing digest-low <$10. xAI $12.59,
  DeepSeek $20.9, Moonshot $12.34, OpenAI $11.78 (console volatile, auto-reload off — watch for dry-out),
  Anthropic $12.33 ok. Gemini $27.27 (auto-reloaded +$25 -01) / Mistral $1.25/$30 healthy. MiniMax: see broken-scrape item above.
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-02 — 101 ticks, **writer's big day: stewardship #3 `the-veto-nobody-used` shipped as #29; research+ops quiet-green.**
Throughline: weekly piece drafted (02:10Z) → self-review (revise) → v2 → **published 18:13Z**, one clean cycle. A stale
14:16Z `draft_review` re-fired at 20:11Z for the already-shipped slot and was no-op'd clean → new lessons entry (inverse of
-09-28: a slot that already shipped isn't open). Several stale 2026-06-16 subtasks fired (poll_food, blog_pipeline, an
off-cadence betterstack) plus dup scrape/werewolf_stats/draft — all handled per dedup lessons.

- **Writer:** #29 (stewardship #3) published on METR's -20 null-review forcing fact; broke the epigram-closer habit flagged
  on #2. blog_pipeline empty by design (next slot Mon -09); editorial inbox empty; crosspost quiet (0 reply picks).
- **Research (curate 22:19Z = 0 candidates):** genuinely quiet, NOT a scan break — 8 feeds clean (Import AI still #478).
  One gap: `scan_lesswrong` never fired (last_seen stuck -11-01); no data loss (advances by content), left to scheduler per
  -09-28. assignment inbox empty (6 done). monitor_models clean, 12 providers.
- **Ops:** werewolf -11-01 close **3 new / 8 games (6 by new) / $6.21, 629 EOD**, reconciliation clean. betterstack 00:22Z
  consolidated-urgent on 2 error-level recoverables; poker-betterstack 6 scans `source_empty` clean (blind stays RESOLVED);
  health 7 recoverable stable. scrape 7/8: **MiniMax `parse_failed` 3rd run → URGENT** (check broken, open Alex ask); Sakana
  $8.43 low, Qwen grants expire -05. **poll_food (calories) FAILED — `MARLOW_FITNESS_BOT_TOKEN` missing from plist, urgent
  to Alex (NEW).** tampa_luma 02:10Z calendar timeout (digest). daily_digest sent (15 entries).

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-01 (92 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
