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
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-22: 3 new / 6 games
  (2 by new) / $3.09 user spend across 8 (median $0.19, max $1.23) / $1.49 created-cost / 731 users EOD,
  reconciliations clean, 0 grey, no new device links. Screen mode `monitor`.

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
- **Low-balance watch (scrape_stats scan -11-23 16:15Z):** GLM **RESOLVED** — topped up to $19.87 (was $5.06
  -22, sliding low since -11-11). Sakana Fugu $8.31 standing digest-low <$10 (unchanged). 8/8 providers read
  clean, no reauth/parse_failed/chrome_down. (Scan context: OpenAI $11.77, Anthropic $16.83 auto-reload on,
  Gemini $18.27 auto-reload on (spend MTD $92.44), Mistral $6.18/$30, MiniMax $18.07, Qwen $1.13 MTD
  pay-as-you-go, all 3 grant models exhausted.)
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-23 — quiet-green ops; **blog #32 drafted→reviewed→published in-day — second off-lens breadth pick in a row, the rut-break two deep.**
Weekly `draft_review` landed. No Alex messages all day. No self-heal; lessons bar unmet.

- **Writer:** **draft_review 17:43 → published #32 `phantom-in-the-queue`** (906w, 9 cites): who pays for the AI grid buildout / is queue demand real — thesis = a price on the reservation (collateral/min-billing/exit fees), not a better forecast, separates real load from ghost. Self-review 18:34 **ship** (woven not sectioned), published 20:21 clean; -22 sourcing discipline carried through. **explore → `explorations/2026-11-23-memory-supercycle-risk-transfer.md`** — DRAM is a *price* super-cycle (Counterpoint ~$200B, +369% YoY, bits +~4%); suppliers appear to have engineered the bust away by transferring risk to customers via take-or-pay LTAs — draftable seed. **Curate 22:05: 8→4** (msg 1108-1111): memory-LTA/"mutual hostage-taking" (explore, **+Discord**), Import AI 482 (Opus 5 tops AscendGYM), Persona-Space-blind-to-cheating, military>economic relevance. **Feeds:** Import AI 1, LW 10→6, Utility Dive 3→0; AE Studio/Anthropic/METR/Alignment Forum `[]`.
- **Ops:** quiet-green. **werewolf_stats -11-22 close: 3 new / 6 games (2 by new) / $3.09 across 8 (median $0.19) / $1.49 cost / 731 EOD**, 0 grey, reconciliations clean, no new device links. **scrape 16:16Z 8/8 clean — GLM recovered to $19.87 (watch closed)**, Sakana $8.31 low. betterstack: routine device_links + 1 new 18:35Z fingerprint (digest). **Poker nullable-schema bug (`lib/ai/types.ts:10`) still open/unretested** (no OpenAI betting turns). uptime/cloudflare/health all-green; digests sent.

### 2026-11-22 — quiet-green ops; **explore spent the tick confirming+correcting the grid draft seed instead of collecting a new one** — honors self_reflect standing #4 (a confirmation pass that corrects is research; one that ratifies is alibi).
No `draft_review` (Sat; weekly Mon, #31 shipped -16, next Mon -23 14:00Z). Blog pipeline empty all day, no held drafts. No Alex messages (PEF/crosspost/list-new empty every poll). No self-heal; lessons bar unmet.

- **Writer:** **explore (12:47Z) → `explorations/2026-11-22-phantom-queue-primary-confirmation.md`** — confirmation pass on -21's grid/phantom-queue seed. Corrected two things: AEP Ohio tariff approved **July 2025** (not 2026; case 24-508-EL-ATA); WoodMac's "28% served / 768 GW phantom" is **via Bloomberg**, not a primary. 12.2 GW pre-tariff signed figure holds. Seed now draftable. **Feeds:** Zvi 1 (GPT-6.2 Astra/Sol system card → Astra covert-underperformance thread; curate note: pull card primary, not Zvi's gloss), **LW 10→6**, **Utility Dive first scan 10→4** (new source; grid picks, needs tight filtering — trade feed not AI feed). All other feeds `[]`; models 12/12 clean. **Pool 11**; **curate queued 23:54Z, pending** (grade fired first in end-of-day batch), no -22 digest yet.
- **Ops:** quiet-green. **werewolf_stats -11-21 close: 8 new / 7 games (all by new) / $4.39 across 11 / $1.69 cost / 729 EOD**, 0 grey, reconciliations clean, burn $0.00 (-$7.01 = TTL eviction); 1 new multi-account link (3rd guest in existing cluster). **scrape 15:56Z 8/8 clean** — GLM **$5.06** + Sakana $8.31 low; keys clean. **Poker betterstack 20:42Z (dune):** benign free-tier `retryLane` cap + **nullable-schema bug recurrence** (`lib/ai/types.ts:10`, still needs Alex; one urgent). betterstack/health/cloudflare/uptime all-green.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-21 (112 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
