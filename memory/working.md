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
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-23: 5 new / 13 games
  (5 by new) / $5.59 user spend across 7 (median $0.44, max $2.49) / $6.29 created-cost / 736 users EOD,
  reconciliations clean, 0 would-block / 19 grey (all one user, sexual), 1 Google PROHIBITED refusal,
  1 new device connection (bchase cluster) + guest ::1 grown to 4acct/11br, no new_account_links. Screen mode `monitor`.

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
- **Low-balance watch (scrape_stats scan -11-25 10:38Z):** Sakana Fugu $8.31 standing digest-low <$10
  (unchanged). 8/8 providers read clean, no reauth/parse_failed/chrome_down. (Scan context: GLM $18.90,
  OpenAI $29.04 (recovered), Anthropic $19.09, Gemini $30.30 (recovered, topup $25 Nov 24), Mistral $6.99/$30,
  MiniMax $17.91, Qwen $1.27 MTD pay-as-you-go, all 3 grant models exhausted.)
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

### 2026-11-25 — quiet-green ops (Wed, no draft_review); **explore seeded strongest off-rut draft yet: ML weather models structurally cap the record-breaking tail.**
Blog pipeline empty, no held drafts (#32 pub -23 Mon; next draft_review Mon -30). No Alex messages (every poll empty). No self-heal. self_reflect ran (due).

- **Writer:** **explore → `explorations/2026-11-25-ml-weather-models-cap-the-tail.md`** (richly sourced, draftable, strongest off-rut seed yet): MSE-trained deterministic AI weather models (GraphCast/Pangu/Fuxi, AIFS) win average skill at ~1/1000 the energy but regress the *tail* — error grows ~linearly with record exceedance while physics HRES stays flat; cause is the training objective (interpolates 1979–2017 climate, soft-caps extremes). Carries its own resistance (narrow claim, deterministic-only, generative successors may escape). **self_reflect 13:44:** condensed both notebooks, resynthesized standing; breadth arc read as near-resolved (next move = the draft pick). **Curate 22:02: 12→5** (msg 1117-21): METR pretraining-loss accel (+Discord), Apollo GLM-5.3 update-aware reasoning, Zvi/Jensen-reinstated-at-Trump's-behest, Vistra-queues-overstated (corroborates #32), AI-Village-@-tagging. **Feeds:** Zvi/METR 1 each, Apollo science re-flood (3 cand, **trailing-slash root cause confirmed** `process_sitemap_feed.py:53-59`, re-marked → 0 new). models 12/12 clean all day.
- **Ops:** quiet-green. **werewolf_stats -11-24 close: 4 new / 7 games (5 by new) / $5.49 across 8 (median $0.70) / $2.10 cost / 740 EOD**, reconciliations clean, 8 grey (dockeryellen891), 0 would-block/refusals, **1 new multi-account link fillipstankov↔pepo2bg (Sofia BG shared browser — two same-day new accts = same-person signup, not a cluster; digest-only).** scrape 10:39Z 8/8 clean, Sakana $8.31 standing low. betterstack/Poker quiet. Discord: Alex 2 on-topic msgs (looped-transformers/GLM-5.4/Inkling 2 mini). digest 6 entries; health/uptime/cloudflare green.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-24 (115 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
