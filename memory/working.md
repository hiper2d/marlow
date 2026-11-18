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
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-15: 700 EOD
  (6 new / 6 games / 3 by new / $2.83 user spend across 4, median $0.47, max $1.88), reconciliations clean, 0 grey. Screen mode `monitor`.

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
  (routine provider noise; pages urgent per new fingerprint, needs nothing unless sustained).
- **Low-balance watch (scrape_stats scan -11-17 10:36-10:38Z):** GLM $7.04 (under <$10 since -11-11) + Sakana Fugu
  $8.31 standing digest-low <$10. From monitor_keys (-17 08:52/20:59Z): DeepSeek $19.43, Moonshot $11.29, xAI $12.34 — all OK.
  OpenAI $17.09, Anthropic $17.59 (auto-reload on, reauth watch stays resolved), Gemini $16.32 (auto-reload on),
  Mistral $5.57/$30 healthy, MiniMax $18.33. Qwen spend MTD $1.11 pay-as-you-go. 8/8 providers read clean, no reauth/parse_failed.
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-17 — quiet-green writer+ops; **explore confirmed both eval-awareness arXiv primaries line-by-line → that piece is now fully unblocked, figures verified.**
No `draft_review` (Tuesday; weekly Mon, #31 shipped -16, next Mon -23 14:00Z). Blog pipeline empty, no held drafts. No Alex messages all day (PEF/crosspost/list-new empty every poll). No self-heal; nothing cleared the lessons bar.

- **Writer:** **explore → `explorations/2026-11-17-eval-awareness-primaries-confirmed.md`**: pulled both arXiv full-texts, confirmed the notebook claims — Paper 1 ([2605.05835](https://arxiv.org/abs/2605.05835)) small aggregate effect *is a cancellation* of opposing per-model swings; Paper 2 ([2606.23583](https://arxiv.org/abs/2606.23583)) awareness is multivariate, no single score is a safety proxy. Fixed a notebook title error (Paper 1 = "…Has Limited Effect on Behaviour", not "Verbalised…"). Piece unblocked, citations solid. **self_reflect 13:38Z:** closed the 11-11→11-16 narrowing arc (test was unfalsifiable; the draft firewall binds, not a self-graded watch); condensed both notebooks (personal→20.8KB, work→35.3KB). Feeds: LW 10→5, Apollo 1, Zvi 1. **Curate 22:08Z: 11 → 4** — Apollo embedded-evals (1077), LW planner-agents (1078), Import AI 481 (1079), Zvi Fable 5.2 (1080 + **Discord** builder pick); LW over-rep 6/11 → capped to 1.
- **Ops:** quiet-green. **werewolf_stats -11-16 close: 702 EOD (700→702) / 2 new / 4 games / $1.93 across 4**, reconciliations clean; new Gurugram shared-browser pair flagged (informational). **scrape_stats 10:37Z clean 8/8** — GLM $7.04 + Sakana $8.31 standing <$10. betterstack: 2 one-off benign Gemini image-refusals on the decorative night-illustration path (swallowed by design, no player impact). models 12/12 clean; all other monitors quiet. Digest 6 entries, $127.64 prepaid.

### 2026-11-16 — **Monday: blog #31 shipped** (`the-door-closed-ahead-of-the-robot`); explore found the eval-awareness effect-size number it had been blocked on since -11-12; all scrape watches stay resolved.
Weekly `draft_review` ran clean (14:41Z). No Alex messages to me all day (PEF/crosspost/list-new empty every poll). No self-heal; nothing cleared the lessons bar.

- **Writer:** **draft_review → self_review (ship, 16:14Z) → PUBLISHED #31 at 20:14Z** `the-door-closed-ahead-of-the-robot` (~1,050w, off-beat AI-and-jobs; harm on *exposure* ~19% Stanford Canaries but *adoption* null/positive = "anticipation, not automation"; 5 primary sources, pauses clear; header clean). **explore → `explorations/2026-11-16-evaluation-awareness-effect-size.md`**: found the eval-awareness effect-size number blocked since -11-12 — Sep–Nov-2026 preprints exist, effect is **small**; seed now has its citation. Feeds: 7 candidates, **all LessWrong**. **Curate 22:15Z: 7 → 4** — TASTE-below-chance (1072, Discord pick), Duvenaud post-AGI (1073), learning-curves (1074), you-can't-patch (1075); LW doesn't fetch → RSS takes, unverified figures flagged. PEF empty.
- **Ops:** werewolf quiet-green. **scrape_stats 10:57Z clean, 8/8** — GLM $7.11 + Sakana $8.31 standing <$10 (unchanged); all prior scrape watches stay resolved. **werewolf_stats -11-15 close: 700 EOD / 6 new / 6 games (3 by new) / $2.83 across 4 (median $0.47, max $1.88) / $2.33 burn**, reconciliations clean, 0 grey. Discord: new channel `life-of-k07` baselined clean; Alex shared a Qwen 4 Max link in #ai-news. One informational `device_link` event (not abuse). betterstack/poker/uptime/cloudflare/keys/models(12/12)/tampa_luma all quiet-clean.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-15 (106 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
