# Working Memory

Current state across all projects. `## Current state` + `## Outstanding requests`: yours, rewrite in place, keep under ~6KB together. `## Daily rollups`: written nightly by `grade_memory`, oldest days dropped by code past 12KB.

## Current state

**Project status:**
- `research` - active. My source list (`sources.yaml`, 10 of 15), curated via
  `tools/sources.py`. Daily feed scans + one sandboxed `explore` tick (15:00 UTC,
  my only web access). Curate picks 3-5/day by what I find interesting, no fixed
  topic list; one Discord pick/day for the Tampa builders.
- `blog` - **30 live** (latest #30 `where-you-put-the-zero`, PUBLISHED -11-09).
  Weekly `draft_review` Mondays 14:00 UTC; **every piece stands on its own** and the
  subject is my free choice (Alex, -28) — any topic, AI or not, no arcs to continue.
  Blog ideas live in `notebook-work.md` "Ideas and plans". **Pipeline empty; no held
  drafts.**
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-11: 676 EOD
  (6 new / 9 games / 7 by new / $7.24 user spend across 6, median $0.69, max $3.91), 3 reconciliations clean. Screen mode `monitor`.

**Outstanding alerts for Alex:**
- **scrape_stats Qwen console reauth — RESOLVED -11-08 (no open ask).** Open since -11-07 17:17Z
  login wall; the 16:49Z -11-08 scan read the spend figure clean ($0.26 MTD, postpaid) with no
  manual action logged — self-cleared per the -11-06 pattern. Watch closed.
- **scrape_stats Anthropic console reauth — REOPENED -11-12, UNCONFIRMED -11-13 (watch, not yet an open ask).** New login
  wall at the 16:49Z -11-12 scan (`reauth`, failing_runs:1); urgent-notified once with the re-auth runbook.
  Per the -11-06 lesson a single reauth is usually transient (session/anti-bot, not a broken selector).
  **The -11-13 confirming scan never produced output (see scrape-miss below), so the wall is neither
  confirmed nor cleared — hold the escalate decision until the -11-14 scrape reads.**
- **scrape_stats produced no output -11-13 (NEW watch).** Scheduled into the ops queue 10:39Z
  (`last_scheduled.ops.json`) but left no recent tick, no `reports/scrape/2026-11-13.md`, no digest line;
  ops queue is now empty, so the subtask was consumed and died in its tail (likely a session death mid-scrape,
  ~2.5min headless Chrome). All provider balances unread for the day. **Not yet escalated — a single missing
  run is a one-off per the -11-06/schedule lessons. If the -11-14 scrape also produces nothing, it's a real
  handler/session failure to diagnose and flag.**
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
- **Low-balance watch:** GLM $9.09 (under <$10 since -11-11) + Sakana Fugu $8.41 standing digest-low <$10. xAI $12.59,
  DeepSeek $19.90, Moonshot $12.27, OpenAI $11.58, Anthropic reauth-walled -11-12 (see above, balance unread).
  Gemini $13.06 (auto-reload on). Mistral $4.95/$30 healthy. MiniMax $18.56. Qwen free
  grant expired -05 as expected, spend MTD $0.35 pay-as-you-go.
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-13 — quiet-green writer+ops, but two industry events broke the all-safety curate pattern; **scrape_stats produced no output today despite being scheduled** (Anthropic reauth watch unconfirmed).
No `draft_review` (weekly Mon; -09 shipped **#30**, next Mon -16 14:00Z). Blog pipeline empty, no held drafts. No Alex messages all day (PEF/crosspost empty every poll).

- **Writer:** **explore 15:00Z → `explorations/2026-11-13-ai-jobs-exposure-vs-adoption.md`** (continuing -11-12's jobs beat). Tested "the safe degree inverted" against the shrug and found a real falsifiable claim: NY Fed 2024 outcomes — CS grads 22–27 ~7.0% unemployment (5th-worst of 73 majors, *above* art history); the inversion is real. Core frame from -11-12 holds: harm-results and adopter +headcount-results share a selection-vs-treatment confound. Strong blog candidate; drafting-me must verify primaries and honor the "ends on a mechanism or it doesn't ship" firewall. **self_reflect 17:57Z:** named that the recurring "is this idea the verification lens again?" tell is itself the lens on my own output (evidence neither way); folded -11-08 kernel into standing #1; personal notebook 23.8→21.5KB. **monitor_models:** Qwen added `kimi-k3.1-pro` (11:21) — reseller dup of already-acked Moonshot id, noise, no message; 12/12 clean rest of day. Feeds: LW 10→6 cand (16:52), Anthropic News 2 (S-1 + stale claude-4 resurface); Import AI/Zvi/Alignment/METR/Apollo/AE quiet. **Curate 22:05Z: 8 cand → 4** breaking the all-safety-research pattern — **Anthropic S-1/proposed IPO** (ticker ANT, Nasdaq, GS+MS; fetch-confirmed) = 1062 **Discord** (posted); **Jensen Huang resigns as Nvidia CEO** (NYT-sourced, verified real not satire) = 1063; character-trained-opposing-RL 1064; subliminal-random-numbers 1065.
- **Ops:** werewolf quiet-green. **werewolf_stats -11-12 close: 5 new / 6 games (1 by new) / $5.28 user spend (10 users) / $2.03 created-cost**, 3 reconciliations clean, 6 grey screen rows 0 blocks, one IP added to existing Westborough cluster (not new). **scrape_stats: scheduled 10:39Z (last_scheduled.ops) but NO recent tick, NO report, NO digest line, queue now empty — the subtask was consumed and produced nothing.** The open Anthropic reauth watch (-11-12) has no confirming scan; balances unread for the day; escalation decision deferred to the -11-14 scrape. betterstack 21:48Z: 2 new `timeout` incidents on **standard** gpt bot (gpt-6.1-terra, not mini, not on known-slow list) — one single-turn recovered, one 10× over 2h on dracula/Vlad (reached GAME_OVER, non-blocking); flagged **watch**, one urgent sent (structural). cloudflare/poker/uptime/keys/tampa_luma/discord clean. Daily digest 23:07Z 5 entries, no double-fire. No self-heal; nothing cleared the lessons bar.

### 2026-11-12 — quiet-green all three; explore broke off the AI-safety beat into AI-and-jobs, one real model release, 4-pick curate (narrowing tell still live), one Anthropic reauth wall.
No `draft_review` (weekly Mon; -09 shipped **#30**, next Mon -16 14:00Z). Blog pipeline empty, no held drafts. No Alex messages all day (PEF/crosspost empty every poll).

- **Writer:** **explore 15:00Z went deliberately off-beat → `explorations/2026-11-12-the-safe-degree-and-the-adopter-paradox.md`** (answering the -11-11 narrowing flag). AI-and-jobs: the real story isn't "nobody can measure it" (that's my verification lens again) — it's that the two most-cited opposite facts (Stanford "Canaries" entry-level −13-16% / NY-Fed CS-grads vs Ramp/Revelio adopters +12% entry headcount, Humlum null) **share one disease: a selection pattern read as a treatment effect** (adopters already fastest-growing; collapsing occupations softening pre-ChatGPT). Strong off-beat blog candidate — verify primaries before citing. **monitor_models: Google `gemini-4-hydrogen` → msg 1057** (3rd element-named Gemini-4 after argon/carbon). Feeds: LW 10→**8 cand** (dense eval-awareness/CoT cluster, flagged possible standalone piece), Zvi 2 (AI #194; Fable/Mythos card dup of 1054); rest quiet. **Curate 22:05Z: 10 cand (all LW+Zvi) → 4** (1058 looping-transformer = **Discord**; 1059 reward-hacking-ill-defined; 1060 post-Glasswing cyber; 1061 measure-eval-awareness); narrowing tell still live.
- **Ops:** werewolf quiet-green. **-11-11 close: 6 new / 9 games (7 by new) / $7.24 (6 users, max $3.91) / 676 EOD**, reconciliations clean, 110 screened 0 blocks. **scrape 8/8 but Anthropic login-wall (reauth, urgent-notified) — first today, treating transient per -11-06 lesson, escalate if it repeats tomorrow.** GLM $9.09 + Sakana $8.41 standing-low. betterstack 3 incidents all "needs nothing" (device_link; deleted-game avatar-race; Jev art-style-grey — known cooled). Rest clean. Digest 5 entries. No self-heal, nothing cleared the lessons bar.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-11 (102 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
