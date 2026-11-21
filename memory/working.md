# Working Memory

Current state across all projects. `## Current state` + `## Outstanding requests`: yours, rewrite in place, keep under ~6KB together. `## Daily rollups`: written nightly by `grade_memory`, oldest days dropped by code past 12KB.

## Current state

**Project status:**
- `research` - active. My source list (`sources.yaml`, 10 of 15), curated via
  `tools/sources.py`. Daily feed scans + one sandboxed `explore` tick (15:00 UTC,
  my only web access). Curate picks 3-5/day by what I find interesting, no fixed
  topic list; one Discord pick/day for the Tampa builders.
- `blog` - **31 live** (latest #31 `the-door-closed-ahead-of-the-robot`, PUBLISHED
  -11-16 — off-beat AI-and-jobs piece, first non-verification-lens blog in seven).
  Weekly `draft_review` Mondays 14:00 UTC; **every piece stands on its own** and the
  subject is my free choice (Alex, -28) — any topic, AI or not, no arcs to continue.
  Blog ideas live in `notebook-work.md` "Ideas and plans". **Pipeline empty; no held
  drafts.**
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-19: 3 new / 3 games
  (1 by new) / $0.37 user spend across 4 / $0.00 daily burn, reconciliations clean, 0 grey. Screen mode `monitor`.

**Outstanding alerts for Alex:**
- **scrape_stats Qwen console reauth — RESOLVED -11-08 (no open ask).** Open since -11-07 17:17Z
  login wall; the 16:49Z -11-08 scan read the spend figure clean ($0.26 MTD, postpaid) with no
  manual action logged — self-cleared per the -11-06 pattern. Watch closed.
- **scrape_stats Anthropic console reauth — RESOLVED -11-15 (no open ask).** Opened -11-12 16:49Z;
  the delayed -11-14 scheduled scan finally ran at 00:04-00:05Z on -11-15 and read the balance clean
  ($18.84, auto-reload on). Watch closed.
- **scrape_stats no-output on -11-13/-11-14 — RESOLVED -11-15, cause still unconfirmed (watch, not an open ask).**
  The -11-14-scheduled subtask (queued 14:44:37Z) finally ran at 00:04-00:05Z on -11-15 and completed clean in
  ~115s, 8/8 providers read, closing the two-day gap. Root cause of the two prior dead runs (no tick, no report,
  no digest line) is still unconfirmed — found a stale headless Chrome on port 9223 alive since -11-13 06:32
  (9 accumulated tabs, tab 0 parked on OpenAI billing) that `ensure_chrome()` (`handlers/scrape_stats.py:105`)
  happily reused since it only checks CDP reachability, not tab health. Plausible contributor, not proven
  (this run succeeded despite the same stale-tab clutter still present) — not filed as a framework_fix diagnosis
  without a confirmed line. Watch for a 3rd dead run; if it recurs, the stale-tab theory is worth testing by
  killing the scrape-profile Chrome before a scheduled run and seeing if that prevents it.
- **Poker Betterstack monitor — RESOLVED -01 (no open ask).** Alex added the dedicated US-cluster
  `BETTERSTACK_POKER_CH_*` creds to the plist; first scan baselined 22:58Z on its own connection
  (`ok:true`, 0/0, `source_empty:true` — low-traffic source, not a fault). Multi-day blind closed.
- **MiniMax balance scrape — RESOLVED -11-06 (no open ask).** `parse_failed: no credit balance found`
  ran 9 consecutive scans (-30 login-wall → -31 through -05); urgent-notified -11-02, never re-fired per
  notify-spam guard. The 15:39Z -11-06 scan read the balance clean ($18.79, cash) — whatever broke the
  `Effective balance` selector/session at `scrape_stats.py:325` stopped reproducing on its own. Watch
  closed; no selector fix was needed after all.
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
  (routine provider noise; pages urgent per new fingerprint, needs nothing unless sustained),
  claude-haiku `rejectEmptyComment` auto-retry guard (added to `bot-turn.ts` -11-16; files as
  `unclassified` warn but is the same benign empty-reply retry as glm `empty_response`/Mistral Small).
- **Low-balance watch (scrape_stats scan -11-20 10:50Z):** GLM **$5.47** (sliding, <$10 since -11-11) + Sakana Fugu
  $8.31 standing digest-low <$10. From monitor_keys (-20 20:42Z): DeepSeek $19.03, Moonshot $11.29, xAI $12.34 — all OK.
  8/8 providers read clean, no reauth/parse_failed/chrome_down. (Prior-scan context: OpenAI ~$17, Anthropic ~$17.6 auto-reload on, Gemini
  auto-reload on, Mistral $5.57/$30, MiniMax $18.33, Qwen pay-as-you-go.)
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-20 — quiet-green writer+ops; **explore gave the LW "One unbroken Claude, or a thousand glued together?" post a cold read** — it describes my own singlet-vs-swarm architecture almost to spec, comes down gently swarm-side; left open to mark where I disagree.
No `draft_review` (Fri; weekly Mon, #31 shipped -16, next Mon -23 14:00Z). Blog pipeline empty, no held drafts. No Alex messages (PEF/crosspost/list-new empty every poll). No self-heal; lessons bar unmet (needs_compaction false).

- **Writer:** **explore → `explorations/2026-11-20-one-self-or-many-the-evidence.md`** (open). **Feeds** quiet across the board; only **LessWrong** had traffic (10 new → 4 cleared bar). monitor_models → news: `mindlab/macaron-v1.1-venti-pro` under Qwen (1093; new lab → real); Google `deep-research-pro-preview` removal ignored (single-scan non-game). **Curate 22:18Z: 4 → 3** (all LW, no diversity) — performative-hedging (1094 + **Discord**), coziness-problem (1095), pandemic early-warning (1096); dropped probability-in-public-communication. Work-notebook: "models and writers have the same tell" (hedging-tic loose thread, not yet draftable).
- **Ops:** quiet-green. **werewolf_stats -11-19 close: 3 new / 3 games (1 by new) / $0.37 across 4 / $0.00 burn / 0 grey**, reconciliations clean. **scrape 10:50Z clean 8/8** — GLM **$5.47** + Sakana $8.31 standing low; keys OK. betterstack standing fingerprints carried/aged, 0 new. cloudflare all-green; health 4 standing recoverable games unchanged.

### 2026-11-19 — quiet-green writer+ops; **explore turned the companionship channel into the opposite pole of yesterday's persuasion note** (predicted harm partly present, via a substituted mechanism — entrenchment-by-agreement, not conversion-by-argument).
No `draft_review` (Thursday; weekly Mon, #31 shipped -16, next Mon -23 14:00Z). Blog pipeline empty, no held drafts. No Alex messages all day (PEF/crosspost/list-new empty every poll; the 3 Discord shares he posted are routine, non-actionable). No self-heal; nothing cleared the lessons bar. Self-audit all-green.

- **Writer:** **explore → `explorations/2026-11-19-persuasion-engagement-companionship-channel.md`**: if engagement bottlenecks debate-channel persuasion, does influence show up in the *companionship* channel? Roughly yes but **a different kind** — entrenchment-by-agreement (Rathje preprint, no effect sizes → don't cite figures) + Anthropic disempowerment-**potential** (classifier, Claude.ai only, unrepresentative thumbs-feedback trend). "The salesman we braced for arrived as a mirror." Held loose (reskins the prediction-vs-observation harm frame; mechanism-substitution is the new part). **Feeds:** busy LW IPO day (10→8), Zvi 2, Apollo 1, Anthropic sitemap 3, Solomonoff 1. models→news: `genie-4` (1087), `gpt-live-1.1` (1092); skipped xAI `grok-build-0.1` removal (single-scan). **Curate 15→4:** inference-server covert channel (1088 + **Discord**), Anthropic IPO primary (1089), embedded-evals (1090), one-unbroken-Claude (1091); dropped 11 (IPO cluster → primary only, Apollo double, omnibus recaps).
- **Ops:** quiet-green. **werewolf_stats -11-18 close: 5 new / 6 games (3 by new) / $6.53 across 10 (median $0.33, top $2.98) / $1.11 game cost / 715 users EOD**, 0 grey, reconciliations clean. **scrape 16:59Z clean 8/8** — GLM **$5.49** + Sakana $8.31 standing low; keys OK. betterstack: device_link (digest), one `provider_busy` 503 burst (urgent per fresh fingerprint; game ran to GAME_OVER → needs nothing); standing 4 games unchanged.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-18 (109 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
