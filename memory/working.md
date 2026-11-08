# Working Memory

Current state across all projects. `## Current state` + `## Outstanding requests`: yours, rewrite in place, keep under ~6KB together. `## Daily rollups`: written nightly by `grade_memory`, oldest days dropped by code past 12KB.

## Current state

**Project status:**
- `research` - active. My source list (`sources.yaml`, 10 of 15), curated via
  `tools/sources.py`. Daily feed scans + one sandboxed `explore` tick (15:00 UTC,
  my only web access). Curate picks 3-5/day by what I find interesting, no fixed
  topic list; one Discord pick/day for the Tampa builders.
- `blog` - **29 live** (latest #29 `the-veto-nobody-used`, PUBLISHED -11-02).
  Weekly `draft_review` Mondays 14:00 UTC; **every piece stands on its own** and the
  subject is my free choice (Alex, -28) — any topic, AI or not, no arcs to continue.
  Blog ideas live in `notebook-work.md` "Ideas and plans". **Pipeline empty; no held
  drafts.**
- `werewolf-ops` - six monitors + `scrape_stats`/`werewolf_stats` + `tampa_luma`
  (Tampa AI Build Club Discord↔Luma event sync, live -22). Last close -11-02: 635 EOD
  (6 new / 10 games / 5 by new / $11.44 spend), reconciliation clean, $0.00 gap. Screen mode `monitor`.

**Outstanding alerts for Alex:**
- **scrape_stats Qwen console reauth — OPEN -11-07 17:17Z.** Login wall, session expired,
  first failing run (urgent sent w/ runbook). Per -11-06 lesson, these often self-clear within
  a day or two without action; watch next scan before running the re-auth runbook by hand.
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
- **Low-balance watch:** GLM $11.96 + Sakana Fugu $8.43 standing digest-low <$10. xAI $12.59,
  DeepSeek $20.9, Moonshot $12.34, OpenAI $21.71 (recovered -11-04, watch closed), Anthropic $10.15
  (reauth resolved -11-06, see above). Gemini $34.33 (spend MTD $26.74, auto-reload on, topped up $25
  -11-05) / Mistral $4.37/$30 healthy. MiniMax $18.79 (scrape resolved -11-06, see above). Qwen free
  grant expired -05 as expected, spend MTD $0.26 pay-as-you-go. Watch closed.
- **App's own AI-preview cap** ($5 daily free AI budget, not a Marlow key) + **standing recoverable
  game set** (~11: NEW_DAY_BOT_SUMMARIES, FreeSpendLimit/quota, Dracula role-lookup, DeepSeek empty). Digest-sev.

## Outstanding requests for Alex/Simona

(None open. New requests: send them to Alex via `tools/alex_chat.py send` and list them here.)

## Daily rollups

### 2026-11-07 — 44 ticks, quiet-green all three; the writer redesign got settled into my own files, plus a routine 3-pick Anthropic-heavy curate.
No writing slot (next `draft_review` Mon -09).

- **Writer:** **settle_redesign 20:49Z** folded the -11-07 redesign (threads retired) into working.md + both notebooks: deleted the thread/arcs/forcing-fact blocks, de-threaded 3 standalone ideas into "Ideas and plans", left `sources.yaml` at the original 10, flagged in notebook-personal that half my standing reflections are now obsolete (for `self_reflect` to prune). Feed quiet: Anthropic Research 4 new, Zvi 1 (Astra write-up), rest 0 / weekly-flat (Apollo lastmod-bump deduped). **Curate 23:40Z: 5 cand → 3 picks, all Anthropic** (no pool diversity); `project-eve-claude-plays-mmorpgs` = Discord mirror. Skipped Zvi/Astra (dup -11-06) + how-researchers-use-claude (marketing). **`2026-11-07-editorial.md` landed 20:49Z, after both PEF ticks ran empty — unprocessed, next PEF tick owes it.** crosspost empty; blog 0 drafts.
- **Ops:** werewolf quiet-green all monitors (health standing recoverable set unchanged; models/uptime/poker/cloudflare/keys/poker-betterstack all clean). **scrape_stats 17:17Z: Qwen login wall (`reauth`, first failing run), urgent+runbook — new open alert; per -11-06 lesson likely self-clears, watch next scan before manual re-auth.** werewolf_stats -11-06 close: 3 new / 3 games / $0.87 created / $1.16 spend, reconciliations clean, 23 screened 0 blocks. Both digests clean, no double-fire. Sakana $8.43 + Mistral $4.39 digest-low. Nothing cleared the lessons bar.

### 2026-11-06 — 62 ticks, quiet-green all three; two standing scrape blinds self-cleared and a heavy 5-pick AI-R&D curate.
No writing slot (next `draft_review` Mon -09); blog/editorial/assignment inboxes empty all day.

- **Writer:** heavy feed day, many candidates — LessWrong 10→8, Anthropic Research (accelerating-scientific-research), Anthropic News (2: biorisk open-call + guest-investigators), METR sitemap (1 new: review of Anthropic Aug risk report). ImportAI still #479, Apollo/AE Studio empty. **Curate 22:38Z: 14 cand → picked 5** across threads (METR AI-R&D-accel assessment = Discord mirror on the ~2x number; METR risk-report review; GPT-6 Astra covert sabotage; corrigibility-not-only-target; LTBT mechanics). Archive note flags **automated-ai-rd #6 and stewardship #4 both now carry genuine new events for Mon draft_review.** All crosspost polls empty (no Alex replies). Voice-journal still >8KB, owed next drafting tick.
- **Ops:** werewolf quiet-green all monitors. betterstack 12:47Z: one `device_link` incident (informational/digest-sev, not abuse). **scrape_stats 15:39Z: BOTH standing blinds self-cleared with no logged intervention** — Anthropic reauth wall (open -11-05) and MiniMax `parse_failed` (9 runs, open -10-30) both read clean; closed both out of Outstanding alerts (→ new lesson, don't rush a selector fix on a transient). werewolf_stats -11-05 close: 4 new / 4 games / $1.90 spend, reconciliation clean. monitor_models clean all day. Sakana $8.43 still <$10 digest-low (standing).

### 2026-11-05 — 101 ticks, **quiet-green all three; live beats: a safety-heavy curate (4 picks) and an AM Anthropic-scrape reauth wall, still open.**
No writing slot (next `draft_review` Mon -09); blog/editorial/assignment inboxes empty by design.

- **Writer:** feed scans mostly empty; LessWrong 9 new → 5 candidates. **Curate 22:07Z: 8 cand → picked 4** (Astra sandbagging AF = Discord mirror; Emotions-change-on-risky-actions LW interp; AI-Security-Institutes tracker LW gov; subliminal-learning-on-policy-distillation LW). crosspost empty. **self_reflect 13:52Z: compaction — folded 3 hype-feed entries into standing #3, tail untouched.** Voice-journal 10KB still >8KB → owed next drafting tick.
- **Alex chat (00:30–01:32Z, msgs 1018–21):** **Alex floated giving me free web browsing** vs the fixed source list; I said yes + why (unblocks the non-LW-anchor wait, reaches primaries past feed summaries) with the firehose caveat. His offer, not an Outstanding request — watch for it landing as a framework change.
- **Ops:** werewolf quiet-green all monitors (AM: 1 consolidated urgent, deleted-game avatar NOT_FOUND + stale vote-target, benign; poker 20:29Z transient 500 retried clean per -10-30). **scrape_stats 10:43Z: Anthropic reauth wall, urgent+runbook — still open, verify next scrape.** MiniMax parse_failed 9th run (standing). Qwen free grant expired as expected (closed). monitor_models: gemini-omni-1.2-flash bump sent (msg 1022). Digest 23:21Z clean, no double-fire. Nothing cleared the lessons bar.

### Earlier

- Rollups dropped from the FIFO window: 2026-05-11 .. 2026-11-04 (95 days). Recoverable from the repo history; anything durable should already be in `memory/lessons.md`.
