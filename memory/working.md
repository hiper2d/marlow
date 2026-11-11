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
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-09: 667 EOD
  (7 new / 12 games / 11 by new / $4.20 user spend, max $1.71), reconciliations clean (660→667). Screen mode `monitor`.

**Outstanding alerts for Alex:**
- **scrape_stats Qwen console reauth — RESOLVED -11-08 (no open ask).** Open since -11-07 17:17Z
  login wall; the 16:49Z -11-08 scan read the spend figure clean ($0.26 MTD, postpaid) with no
  manual action logged — self-cleared per the -11-06 pattern. Watch closed.
- **scrape_stats Anthropic console reauth — RESOLVED -11-06 (no open ask).** Open since -11-05 10:43Z
  login wall; the 15:39Z -11-06 scan read the balance clean ($10.15, auto-reload on) with no manual
  action logged — session must have been refreshed between scans. Watch closed.
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
- **Low-balance watch:** GLM $11.69 + Sakana Fugu $8.41 standing digest-low <$10. xAI $12.59,
  DeepSeek $20.9, Moonshot $12.34, OpenAI $21.13 (recovered -11-04, watch closed), Anthropic $19.87
  (reauth resolved -11-06, see above). Gemini $31.55 (spend MTD $29.37, auto-reload on, topped up $25
  -11-05) / Mistral $4.44/$30 healthy. MiniMax $18.77 (scrape resolved -11-06, see above). Qwen free
  grant expired -05 as expected, spend MTD $0.26 pay-as-you-go. Watch closed.
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-10 — 102 ticks, quiet-green all three; no writing slot, the explore tick resolved the grader-modelling idea to primaries, and a light all-pass 4-pick curate.
No `draft_review` (weekly Mon; -09 shipped **#30**, next Mon -16 14:00Z). Blog pipeline empty, no held drafts all day.

- **Writer:** **explore 15:00Z** resolved the standing "models evading the monitors" idea to a nameable frame — `explorations/2026-11-10-grader-modelling-vs-the-astra-gap.md`: pulled primaries (TurnTrout's foundational grader-modelling post, older/messier than my note) + the capability-vs-test-artifact read; notebook-work +9. **monitor_models 16:31Z: Google `gemini-4-carbon` real release → msg 1047** (new Gemini-4-line checkpoint); 12/12 clean otherwise. Feed thin: LessWrong 10→3 cand (honeypots-insider-threats, METR expenditure→labor-share horizon, misaligned-recognise-harmful), others flat. **Curate 22:08Z: light, 4 cand → all 4 picked** (Anthropic "Claude designs electronic prototypes" = **Discord** 1048; honeypots 1049; METR labor-share 1050; misaligned-recognise 1051); 2 sources so no diversity call. PEF/crosspost empty; **no Alex messages all day**.
- **Ops:** werewolf quiet-green. **werewolf_stats -11-09 close: 7 new / 12 games (11 by new) / $4.20 spend (5 users, max $1.71) / 660→667 EOD**, 3 reconciliations clean ($0.04 preview-unattributed, $0.00 ledger gap), 154 screened 0 blocks. scrape 8/8 ok, only Sakana $8.41 standing-low. betterstack quiet (3 known incidents carried). poker/uptime/cloudflare/keys/poker-betterstack clean. Daily digest 8 entries, no double-fire. No failures, no self-heal, nothing cleared the lessons bar.

### 2026-11-09 — 66 ticks; the Monday slot shipped **#30** and ran a dense LW-heavy curate; ops quiet-green with one benign mid-action game delete.
Writing slot fired: `draft_review` drafted → self-reviewed ship → published **#30 `where-you-put-the-zero`** (the "what automating AI research measures" idea, sourcing closed -11-08). Blog now 30 live; pipeline empty again, no held drafts.

- **Writer:** draft_review 17:50Z → self_review 18:40Z (**ship**, clean all 4 rubrics, image no-numerals clean, no pause) → publish 20:06Z (Alex pinged for reaction, no reply yet). Feed: Import AI **#480** fresh (parked at #479 for days), Zvi 1 (METR-inside-Anthropic RSI read — flagged pull-the-primary not the gloss), LessWrong 10→6 cand (**grader-modelling frame converging** same-day: theory + RL companion + OpenAI Astra field-report; plus safety-uplift downstream of METR), Anthropic Research "Provable inference" (FlashProve zkSNARK). **Curate 22:10Z: 9 cand → 4 picks** (Provable inference = **Discord** builder pick 1043; safety-uplift 1044; grader-RL 1045 folding in theory+Astra; FDT twin-PD 1046); dropped Zvi/ImportAI480/EPC/grader-theory. **monitor_models 18:58Z: 2 real releases sent** (Anthropic `claude-fable-5-2`, Meta `muse-ember-1.0`, msg 1041). self_reflect 19:41Z compacted both notebooks. crosspost polls all empty.
- **Ops:** werewolf quiet-green. **betterstack: game `sherlock-holmes` deleted mid-`welcomeImpl`** → unclassified error + stale_action warn (documented delete-mid-action handling), urgent sent "needs nothing"; recurred later, already-reported. health +1 recoverable (Sherlock NEW_DAY_BOT_SUMMARIES) on 4 standing. werewolf_stats -08 close: 4 new / 4 games / $6.23 spend (6 users, max $4.81) / reconciliations clean, 36 screened 0 blocks. scrape 8/8 ok, Sakana $8.41 standing-low. keys/cloudflare/uptime/poker clean. Nothing cleared the lessons bar.

### 2026-11-08 — 57 ticks, quiet-green all three; the Monday draft is now anchored, the -07 editorial cleared, and Alex claimed a news pick to write himself.
No writing slot (next `draft_review` Mon -09 14:00Z); blog pipeline empty, no held drafts all day.

- **Writer:** **explore 15:00Z made Monday's piece draftable** (`explorations/2026-11-08-ai-rd-horizon-sourcing.md`): no arXiv/affiliation/code behind the open-ended AI R&D LessWrong post; renormalising the floor to gpt-4-turbo moved doubling time to 8.6mo (from 11.5); METR one-liner confirmed "~7 vs under 3 months." Through-line: headline doubling time is a design choice, and Formalising-X (the taste task) is the outlier the method handles worst. **PEF 00:30Z cleared the owed -07 editorial** (voice/structure/pause-4 + topic-guidance sourcing rule); 14:17Z no-op. **crosspost 21:05Z: Alex replied to the Project EVE pick (msg 1034) "i'll write about this" → saved as article idea for Simona** (`article-ideas/2026-11-08-...`). Feed flat (LessWrong 7+2 cand, Anthropic Research 1, rest nil). **Curate 22:00Z: 10 cand → 4 picks**, dropped 2 dups (took the Ajeya S1 acceleration primary = Discord mirror `posted`); verification throughline threads 3 of 4, logged as a blog candidate.
- **Ops:** werewolf quiet-green all monitors. **scrape_stats 16:49Z: Qwen login-wall self-cleared** (open since -07 17:17Z, no manual action, $0.26 MTD) per the -06 self-heal lesson; Anthropic back to $19.87; only digest-low Sakana $8.41 (standing). werewolf_stats -07 close: 5 new / 7 games / $2.56 spend, reconciliations clean, $0.00 gap, 49 screened 0 blocks. betterstack one `device_link` (digest), poker 1 signup (digest), models 12/12 clean. Nothing cleared the lessons bar.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-07 (98 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
