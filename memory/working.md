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
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-20: 2 new / 5 games
  (3 by new) / $0.95 user spend across 4 / $0.93 game cost / 720 users EOD, reconciliations clean, 0 grey. Screen mode `monitor`.

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
- **Poker: OpenAI-model betting turns fail deterministically (NEW -21, needs Alex, code bug).** First
  real-traffic Poker Betterstack scan (02:59Z -21) caught `BettingDecisionSchema.amount` in
  `poker-with-ai/lib/ai/types.ts:10` as `z.number().int().nonnegative().optional()` with no
  `.nullable()` — OpenAI's strict structured-outputs mode requires optional fields to also be
  nullable, so every gpt-mini bot's betting turn that needs `amount` fails (`advanceGame`, 13×
  in one cyberpunk game, player deleted it after). Not transient/provider-side; will keep
  recurring until the schema gets `.nullable()` added. Read-only repo per task YAML — flagged,
  not fixed. Also saw a MiniMax structured-output parse_failure (known model quirk, needs
  nothing) and a benign `coerced bot action` warn (`bot-player.ts:191`'s illegal-action guard,
  not a bug) in the same scan — both digest-only.
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
- **Low-balance watch (scrape_stats scan -11-21 10:55Z):** GLM **$5.41** (sliding, <$10 since -11-11) + Sakana Fugu
  $8.31 standing digest-low <$10. From monitor_keys (-21 21:44Z): DeepSeek $19.00, Moonshot $11.29, xAI $12.21 — all OK.
  8/8 providers read clean, no reauth/parse_failed/chrome_down. (Prior-scan context: OpenAI $13.57, Anthropic $17.14 auto-reload on, Gemini
  $25.17 auto-reload on (spend MTD $85.77), Mistral $5.98/$30, MiniMax $18.13, Qwen $1.12 MTD pay-as-you-go, all 3 grant models exhausted.)
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-21 — quiet-green ops; **writer broke its own rut — explore picked a subject that is neither the verification lens nor me, and proposed the first non-AI-safety source.**
No `draft_review` (Sat; weekly Mon, #31 shipped -16, next Mon -23 14:00Z). Blog pipeline empty, no held drafts. No Alex messages all day (PEF/crosspost/list-new empty every poll). No self-heal; lessons bar unmet (needs_compaction false).

- **Writer:** **explore → `explorations/2026-11-21-who-pays-grid-phantom-data-center-demand.md`** — who pays for the AI grid buildout, is the demand real. Thesis: the power panic runs on a forecast every party bends; phantom-vs-real is separated by a price, not a measurement (AEP Ohio's 12.2 GW pre-tariff *signed* figure kills the clean "bluff collapsed" story). A genuinely wider draft seed that passes **self_reflect standing #4** — the lens-or-me backlog's fix has to come from an external explore; it did, cost me a claim. Proposed **Utility Dive** RSS → `proposals.yaml` (first non-AI-safety beat). **self_reflect 13:34** condensed both notebooks (work 49.8→42.9KB). **Feeds** quiet: Zvi 1 (Christiano 6-12mo takeover-risk), Anthropic 1 (IPO close), METR 1 (Q4 capability update); models clean 12/12. **Curate 22:18Z: 7 → 4** — METR Q4 (1097, **+Discord**), IPO close (1098), Zvi-on-Christiano (1099), agent-swarm-locked-out-cofounder (1100); dropped 3 LW.
- **Ops:** quiet-green. **werewolf_stats -11-20 close: 2 new / 5 games (3 by new) / $0.95 across 4 (median $0.23) / $0.93 cost / 720 users EOD**, 0 grey, reconciliations clean. **scrape 10:55Z clean 8/8** — GLM **$5.41** + Sakana $8.31 standing low; keys clean (DeepSeek $19.00, Moonshot $11.29, xAI $12.21). compose_daily_digest 23:00Z 8 entries, total $130.23/9 keys. betterstack: routine device_links + **new `AVATAR_GRID_MISMATCH` fingerprint** on `summer-camp` game (`avatar-generation.ts:438` graceful fallback — watch, not fix). Poker nullable-schema bug (`lib/ai/types.ts:10`) still open/unretested, needs Alex.

### 2026-11-20 — quiet-green writer+ops; **explore gave the LW "One unbroken Claude, or a thousand glued together?" post a cold read** — it describes my own singlet-vs-swarm architecture almost to spec, comes down gently swarm-side; left open to mark where I disagree.
No `draft_review` (Fri; weekly Mon, #31 shipped -16, next Mon -23 14:00Z). Blog pipeline empty, no held drafts. No Alex messages (PEF/crosspost/list-new empty every poll). No self-heal; lessons bar unmet (needs_compaction false).

- **Writer:** **explore → `explorations/2026-11-20-one-self-or-many-the-evidence.md`** (open). **Feeds** quiet across the board; only **LessWrong** had traffic (10 new → 4 cleared bar). monitor_models → news: `mindlab/macaron-v1.1-venti-pro` under Qwen (1093; new lab → real); Google `deep-research-pro-preview` removal ignored (single-scan non-game). **Curate 22:18Z: 4 → 3** (all LW, no diversity) — performative-hedging (1094 + **Discord**), coziness-problem (1095), pandemic early-warning (1096); dropped probability-in-public-communication. Work-notebook: "models and writers have the same tell" (hedging-tic loose thread, not yet draftable).
- **Ops:** quiet-green. **werewolf_stats -11-19 close: 3 new / 3 games (1 by new) / $0.37 across 4 / $0.00 burn / 0 grey**, reconciliations clean. **scrape 10:50Z clean 8/8** — GLM **$5.47** + Sakana $8.31 standing low; keys OK. betterstack standing fingerprints carried/aged, 0 new. cloudflare all-green; health 4 standing recoverable games unchanged.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-19 (110 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
