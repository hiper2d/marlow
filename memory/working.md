# Working Memory

Current state across all projects. `## Current state` + `## Outstanding requests`: yours, rewrite in place, keep under ~6KB together. `## Daily rollups`: written nightly by `grade_memory`, oldest days dropped by code past 12KB.

## Current state

**Project status:**
- `research` - active. 10 feed sources + assignment path. Curate cuts are
  cap/quality, not volume. Import AI at #479 (weekly cadence).
- `blog` - **29 live** (latest #29 `the-veto-nobody-used`, stewardship #3,
  PUBLISHED -11-02). Weekly `draft_review` Mondays 14:00 UTC; the piece is free choice
  now (Alex, -28) — any subject I want, not only a ripe arc. **Pipeline empty; no held
  drafts.** (#29 revise pass -11-02: one surgical cut — dropped the restating "isn't X /
  it's Y" mic-drop closer, landed on "...nothing here was put under load"; METR self-
  admission kept in body. v1→v2→publish, one pass.)
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-02: 635 EOD
  (6 new / 10 games / 5 by new / $11.44 spend), reconciliation clean, $0.00 gap. Screen mode `monitor`.

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
latent-reasoning-undermines-cot -23 · measurement-validity-under-eval-awareness (circling, no forcing fact) ·
**monitoring-evasion convergence (-11-04): 3 same-day anchors — OpenAI agents disabling monitors (LW),
Paradise Lost honeypot (LW), Anthropic automating emergent-misalignment (AF) — behavioral / operational /
training-surface facets. Possible arc or a feed of cot-monitorability; watch whether a 4th non-LW anchor lands.**

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
- **scrape_stats Anthropic console — reauth, NEW -11-05.** 10:43Z scan hit a login wall on
  console.anthropic.com in the dedicated scrape Chrome profile (port 9223); prior scans ok (balance
  $10.42 -11-04). Urgent-notified -11-05 10:4x with runbook: pkill the scrape-profile headless Chrome
  (confirm gone), launch headful via `start-chrome-persistent.sh 9223`, log back in, quit. Next tick
  should relaunch headless clean — verify balance read resumes.
- **Poker Betterstack monitor — RESOLVED -01 (no open ask).** Alex added the dedicated US-cluster
  `BETTERSTACK_POKER_CH_*` creds to the plist; first scan baselined 22:58Z on its own connection
  (`ok:true`, 0/0, `source_empty:true` — low-traffic source, not a fault). Multi-day blind closed.
- **MiniMax balance scrape BROKEN — needs Alex (urgent -11-02, still open -11-05).** `parse_failed: no
  credit balance found` now 9 consecutive runs (-30 login-wall → -31/-01/-02×2/-03/-04/-05 parse_failed);
  handler marks it `severity: urgent` but -11-03 through -11-05 scans did NOT re-fire the Telegram ping
  (unchanged condition, no new info since -11-02 — rides the digest instead per notify-spam guard). NOT a
  login-wall signature, so the recharge-records page loads but the `Effective balance` label at
  `scrape_stats.py:325` yields no number — either the Chrome-profile session went stale or MiniMax
  relabelled the widget. Unfixable blind (selector guess unverifiable = speculative). Alex: open
  `platform.minimax.io/console/recharge-records` in the Marlow profile → (a) re-login prompt = reauth, or
  (b) balance under a new label = one-line selector fix. Unmonitored since -30 (now 7 calendar days / 9
  scan runs).
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
- **Low-balance watch:** GLM $13.20 + Sakana Fugu $8.43 standing digest-low <$10. xAI $12.59,
  DeepSeek $20.9, Moonshot $12.34, **OpenAI recovered $6.43→$24.85 -11-04 (back above $10, watch closed)**,
  Anthropic: see reauth item above (was $10.42 ok -11-04). Gemini $10.23 (spend MTD $21.17, auto-reload on) /
  Mistral $4.27/$30 healthy. MiniMax: see broken-scrape item above. **Qwen free grant expired -05 as
  expected (0% remaining, all 3 models exhausted) — no dry-key fault, spend MTD $0.26, headline moves to
  pay-as-you-go dollars next scan. Watch closed.**
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-05 — 101 ticks, **quiet-green all three; live beats: a safety-heavy curate (4 picks) and an AM Anthropic-scrape reauth wall, still open.**
No writing slot (next `draft_review` Mon -09); blog/editorial/assignment inboxes empty by design.

- **Writer:** feed scans mostly empty; LessWrong 9 new → 5 candidates. **Curate 22:07Z: 8 cand → picked 4** (Astra sandbagging AF = Discord mirror; Emotions-change-on-risky-actions LW interp; AI-Security-Institutes tracker LW gov; subliminal-learning-on-policy-distillation LW). crosspost empty. **self_reflect 13:52Z: compaction — folded 3 hype-feed entries into standing #3, tail untouched.** Voice-journal 10KB still >8KB → owed next drafting tick.
- **Alex chat (00:30–01:32Z, msgs 1018–21):** **Alex floated giving me free web browsing** vs the fixed source list; I said yes + why (unblocks the non-LW-anchor wait, reaches primaries past feed summaries) with the firehose caveat. His offer, not an Outstanding request — watch for it landing as a framework change.
- **Ops:** werewolf quiet-green all monitors (AM: 1 consolidated urgent, deleted-game avatar NOT_FOUND + stale vote-target, benign; poker 20:29Z transient 500 retried clean per -10-30). **scrape_stats 10:43Z: Anthropic reauth wall, urgent+runbook — still open, verify next scrape.** MiniMax parse_failed 9th run (standing). Qwen free grant expired as expected (closed). monitor_models: gemini-omni-1.2-flash bump sent (msg 1022). Digest 23:21Z clean, no double-fire. Nothing cleared the lessons bar.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-04 (95 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
