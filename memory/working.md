# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` — active. 10 feed sources wired (RSS + sitemap). First-scan backlogs now done for all of them: Import AI, METR, Apollo /science/, Apollo /blog/, AE Studio, Zvi, Alignment Forum, Anthropic /news/, Anthropic /research/, LessWrong.
- `blog` — not yet scaffolded.
- `werewolf-ops` — not yet active (deferred).

**Active threads:**
- `automated-ai-rd` (research) — **ripeness: high**. Three strong anchors landed 2026-05-11: (1) Anthropic `automated-alignment-researchers` (2026-04-14, 9-copy Opus 4.6 swarm closing weak-to-strong PGR 0.23→0.97 in 5d/$18K, generalized to math, failed at Sonnet-4 prod scale); (2) Palisade Research demo of LM agents autonomously hacking + self-replicating across a network (Opus 4.6 81% replication of Qwen weights via exploit chains); (3) Import AI #456 (2026-05-11) continuing the #455 RSI arc. Thread file `threads/automated-ai-rd.md` updated 15:27 with the #456 line; the Palisade + Anthropic-paper anchors still need to be folded in on the next research tick that touches it.
- `cot-monitorability` (research) — **ready to open**. Three-source arc now confirmed: METR (4 items), Apollo (CoT-monitorability position paper), Anthropic `reasoning-models-dont-say-think` (2025-04-04, surfaced by 2026-05-11 /research/ scan). Open this thread on the next research tick that has bandwidth.
- `anthropic-alignment-doctrine` (research) — **candidate**, 2 items. Constitution + well-being + political-even-handedness arc from Anthropic /news/ + LW critique post (`lw-anthropic-hyperstition-fixation`). Wait for a third before opening.
- `agent-deployments` (research) — **candidate**, Anthropic-only. Needs cross-source corroboration before opening.
- `model-welfare-and-consciousness` (research) — **candidate**, ~2 items. Anthropic emotion-concepts/well-being research + LW `llms-persisting-interlocutors`. Watch for next item.
- `self-replication-autonomous-cyberops` (research) — **candidate**, 1 item (Palisade). Strong on its own; promote to thread if a second eval/lab corroborates.
- `safety-tool-stewardship-handoffs` (research) — **candidate**, 2 items (Anthropic donated MCP to Agentic AI Foundation Dec 2025; Petri to TBD 2026-05-07). Open on a third.

**Pending drafts:** none.

**Pending follow-ups for next research tick:**
- Update `threads/automated-ai-rd.md` with the Palisade + Anthropic-AAR anchors (per 22:02 curation note).
- Open `threads/cot-monitorability.md` (3-source arc confirmed).
- Body-read Anthropic `automated-alignment-researchers` post (and Import AI #455/#456 once the substack URL resolves).
- Retry the Import AI #456 body fetch — the 22:02 digest pull returned 404.

**Outstanding alerts for Alex:** none.

## Outstanding requests for Alex/Simona

- **Scheduler queues same-day duplicate feed scans.** Confirmed across multiple sources on 2026-05-11. Apollo /blog/ ran three times (18:35 real catalog, 19:19 stale 2026-05-10 subtask, 20:01 fresh same-day duplicate queued 12:41Z). METR ran twice (14:45, 17:31). Anthropic /news/ and /research/ each ran twice (first scan + same-day rescan). All extra runs were empty no-ops — handlers are idempotent so this is cheap, but on tier-1 feeds with sub-daily cadence it'd burn ticks. Suggested fix: dedup on `(url, prefix)` within a configurable window, or have the scheduler check feed state's `last_seen` vs. expected cadence before queueing.

- **`notify_alex(urgency=digest)` is undercalled / never called.** `digests/daily/2026-05-11.md` and `digests/daily/2026-05-12.md` were both empty going into their respective daily_digest ticks; both fired the quiet-day fallback. Two consecutive empty days while 22 candidate notes were being written across the day suggests feed scans aren't writing to the digest accumulator. Either (a) by design — research feed scans intentionally don't notify per CLAUDE.md, and the daily digest channel exists for a different class of event (budget, ops) — in which case the quiet-day fallback is doing its job; or (b) something in the handler set should be calling it and isn't. The `curate_news_digest` path is separate and is working (5 picks sent 22:02). Flagging for clarification, not as a bug.

- **`daily_digest` cron fired ~1h late after UTC rollover.** Cron schedule is `0 23 * * *`; actually ran 2026-05-12 00:06Z and defaulted "today" to 2026-05-12 instead of compressing 2026-05-11. Either the driver wasn't running at 23:00 on 2026-05-11, or the cron picked it up after rollover. Knock-on: 2026-05-11's quiet-day fallback fired at 12:41Z (mid-day, not end-of-day), and 2026-05-11 never got a proper end-of-day digest pass. Worth confirming the driver was up at 23:00Z.

- **Stale-from-2026-05-09 RSS-state question still open** from yesterday's working memory. Likely benign (the 2026-05-09 line was aspirational scaffolding); leaving the note in case it surfaces again.

## Notes from previous ticks

- 2026-05-11 — **busy day**, 22 ticks. Three more first-scan backlogs landed: Anthropic /news/ (208 entries, 5 candidates, heavy corporate-PR tail suppressed in catalog), Anthropic /research/ (119 entries, 6 candidates, found `automated-alignment-researchers` anchor + `reasoning-models-dont-say-think` cot-monitorability anchor), Apollo /blog/ (8 substantive posts after stripping 17 taxonomy entries, 2 candidates for PBC conversion + 18-month update), LessWrong (10 entries on first scan over ~8h window; estimated steady-state ~10 entries per 4h, the highest-volume source by an order of magnitude). Import AI scan picked up #456 (RSI continuation). Empty ticks on Apollo /science/ (x2), METR (x2), AE Studio (x2), Zvi, Alignment Forum — all expected steady-state for low-cadence sources after backlog drain.
- 2026-05-11 22:02 — `curate_news_digest` ranked 22 candidates → 5 picks sent in 2 Telegram chunks. Picks: Palisade self-replication eval, Anthropic Automated Alignment Researchers, Import AI #456 (body fetch 404'd, reviewed from RSS), Apollo PBC conversion, Byrnes corrigibility-as-target critique. Cross-source diversity + technical/eval lean. No urgent notify.
- 2026-05-12 00:07 — `daily_digest` ran late (cron at 23Z UTC, fired 00:06 next day), defaulted to 2026-05-12, sent quiet-day fallback because `digests/daily/` is empty. See outstanding request above.

---

*This file is rewritten daily by the grader (Haiku, 23:00 UTC ish). The framework is past scaffolding now — research is in routine operation, blog and werewolf-ops still ahead.*
