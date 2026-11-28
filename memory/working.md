# Working Memory

Current state across all projects. `## Current state` + `## Outstanding requests`: yours, rewrite in place, keep under ~6KB together. `## Daily rollups`: written nightly by `grade_memory`, oldest days dropped by code past 12KB.

## Current state

**Project status:**
- `research` - active. My source list (`sources.yaml`, 10 of 15), curated via
  `tools/sources.py`. Daily feed scans + one sandboxed `explore` tick (15:00 UTC,
  my only web access). Curate picks 3-5/day by what I find interesting, no fixed
  topic list; one Discord pick/day for the Tampa builders.
- `blog` - **32 live** (latest #32 `phantom-in-the-queue`, PUBLISHED -11-23 — who pays
  for the AI data-center grid buildout / phantom interconnection-queue demand; second
  off-lens breadth pick in a row, neither verification-lens nor self-piece).
  Weekly `draft_review` Mondays 14:00 UTC; **every piece stands on its own** and the
  subject is my free choice (Alex, -28) — any topic, AI or not, no arcs to continue.
  Blog ideas live in `notebook-work.md` "Ideas and plans". **Pipeline empty; no held
  drafts.**
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-26: 5 new / 3 games
  (3 by new) / $0.22 user spend across 6 (median $0.00, max $0.19, no limit hits) / $0.62 created-cost / 746 users EOD
  (741→746), reconciliations clean, 41 screened 0 would-block / 0 grey / 0 errors — **first day with both `monitor` AND
  `enforce` modes on the content-screen tape (21/20 split); watch for a flip announcement from Alex, not an alert.**
  ::1 guest shared-browser cluster grew to 13 accts (+6 same-device guest signups); NEW shared-browser link
  tanguncaner↔guest session (Ankara TR). 0 refusals.

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
- **`previewGameAction` "AI did not return a character sheet for <name>" recurring (ESCALATED urgent -26, needs Alex, app bug).**
  4th occurrence of this exact fingerprint shape since -10-30 (Zeke, Shamsiel -24, Holmes -25, Quang -26), 3rd consecutive
  scan day — `preview-generation.ts:170`'s batched character-sheet LLM call returns missing a sheet for one cast member and
  the assembly step has no fallback. Recommended a retry-on-mismatch / fuzzy-name fallback at that line. Read-only repo per
  task YAML — flagged, not fixed. Will keep firing (one failed preview per hit) until the fallback lands; treat further hits
  as the same known incident, not fresh escalations.
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
- **Low-balance watch (scrape_stats scan -11-27 11:02Z):** Sakana Fugu $8.07 standing digest-low <$10
  (unchanged). 8/8 providers read clean, no reauth/parse_failed/chrome_down. (Scan context: GLM $18.41,
  OpenAI $26.05, Anthropic $19.01, Gemini $24.91 (topup $25 Nov 24), Mistral $7.05/$30,
  MiniMax $17.89, Qwen $1.54 MTD pay-as-you-go, all 3 grant models exhausted.)
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

- **Simona (tool limitations, surfaced by the -11-24 Apollo feed fix, low-pri):** (1) `tools/sources.py`
  has no `--priority` flag, so remove+re-adding a source to fix its prefix drops `priority: low`. (2) The
  Apollo sitemaps have no `lastmod` and are alphabetically ordered, so `process_sitemap_feed`'s
  recency-based `last_entry_id` detection can't reliably surface new Apollo posts — I'm catching Apollo via
  `explore` for now. Not urgent; filed here so the escalation is readable, not buried in a notebook.
  **Root cause confirmed (-25 Apollo science scan):** `fetch_new` (`handlers/process_sitemap_feed.py:53-59`)
  breaks on `id == last_entry_id`, but stored ids carried a trailing slash (`.../we-need-3rd-party-...-assessments/`)
  the live sitemap ids lack (no `/`), so the break never fired and the whole alphabetical back-catalog (27 entries)
  returned as "new" every scan. Stabilized this tick by re-marking with the exact live id format (no slash) → 0 new on
  recheck. A trailing-slash-normalization one-liner would stop the re-flood, but the deeper problem stays: Apollo's
  sitemap is alphabetical with no `lastmod`, so position-based new-detection can't find genuinely new posts anyway.

## Daily rollups

### 2026-11-27 — quiet-green, no urgents (Fri, no draft_review). Inboxes empty all day.
Blog pipeline empty, no held drafts (#32 pub -23; next draft_review Mon -30). No self-heal; lessons clean. Character-sheet-mismatch did NOT recur (open app-bug still awaiting Alex's fallback at `preview-generation.ts:170`).

- **Writer:** 2 LessWrong scans (Thanksgiving-heavy feed, mostly gratitude essays); Zvi/Anthropic/METR/AE-Studio scans quiet. **Explore (15:00Z):** read primaries (Anthropic Rust-migration post + Alpöge/Claude Riemann-in-Lean) for the "verification is the new bottleneck" blog idea → thesis survives but de-hyped, corrected 3 specifics, confirmed **NOT a news hook** (both mid-2026); note `explorations/2026-11-27-verification-is-the-bottleneck-code-and-math.md`. **Curate 22:16: 8 cand (3 today + 5 carried) → 4 picks (msg 1126-29):** AIs-Should-Never-Refuse-Destructively (Discord mirror, cap respected), BioBlue runaway-optimiser benchmark, Chinese-AI supply-chain risk, sensor-actuator bandwidth takeoff crux.
- **Ops:** **werewolf_stats -11-26 close: 5 new / 3 games (3 by new) / $0.22 across 6 / $0.62 cost / 746 EOD**, reconciliations clean, 41 screened 0 would-block/grey/errors — **first `monitor`+`enforce` split (21/20) on the tape, watch for Alex flip note.** ::1 guest cluster →13 accts (+6); new tanguncaner↔guest browser link. (`report` double-ran by mistake, cleaned up → today's lessons entry.) scrape 8/8 clean (Sakana $8.07 low). betterstack/poker/health/uptime/discord/models/keys/tampa_luma/cloudflare green, 3 standing recoverables, no new.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-26 (117 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
