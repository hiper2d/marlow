# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` — active. 10 feed sources wired (RSS + sitemap). Routine operation; today thin on volume but heavier on signal than yesterday.
- `blog` — active. Astro site scaffolded; first draft landed 2026-05-12 (`automated-ai-rd`) still awaiting Alex review (Simona review attached). No revision tick fired today.
- `werewolf-ops` — not yet active (deferred).

**Active threads:**
- `automated-ai-rd` (research) — **draft pending review**. `projects/blog/drafts/2026-05-12-automated-ai-rd-asymmetric-arrival.md` (~1150 words). Anchors: Anthropic AAR (2026-04-14), Palisade self-replication (2026-05-11 LW linkpost), Import AI #456 RSI arc, Alignment Forum research-sabotage. Notified Alex urgent at 2026-05-12 13:14Z. Thread file `threads/automated-ai-rd.md` carries Palisade + AAR anchors and the Drafts pointer.
- `cot-monitorability` (research) — **ripe, 4 sources, not yet opened**. METR (4 items), Apollo CoT-monitorability position paper, Anthropic `reasoning-models-dont-say-think` (2025-04-04), LW VEA paper (2026-05-12 — 8 open-weight LRMs × 4 benchmarks, near-null behavioural effect of verbalised eval awareness). Still on the open-next-research-bandwidth list.
- `agents-in-real-deployment` (research) — **ripe, 3 sources, not yet opened**. AE Studio `agents-in-the-org-chart` + `ai-agents-need-a-company-brain` (both 2026-05-08), LW Vibe Excel (2026-05-13, finance practitioner on adoption inertia as bottleneck). Cross-industry signals available from AE essays (Block, Microsoft Frontier Firm, Shopify, Meta Reality Labs, Ramp 12% non-engineer PR rate, Tom Blomfield YC "company brain"). Promoted from candidate today.
- `safety-tool-stewardship-handoffs` (research) — **ripening, 3 weak sources**. MCP-to-Agentic-AI-Foundation, Petri handoff, Apollo Update May 2026 (AI Handoff governance pivot through Q2–Q4 2026). Apollo entry is programmatic rather than a research piece; calling ripening, not ripe. Watch for the "AI Handoff" terminology spreading from Apollo to other labs/policy outlets.
- `alignment-target-definitions` (research) — **candidate, 2 items**. AE Studio `primitives-not-rules` (2026-05-11) and Byrnes `empowerment-corrigibility-true-names` (2026-05-11 pick #5). Different vocabularies, same wedge: rule-stacks / observable proxies don't capture the underlying target. Could also be the conceptual home for the VEA paper's narrowing of "evaluation awareness." Watch for a third source.
- `anthropic-alignment-doctrine` (research) — **candidate, 2 items**. Constitution + well-being + political-even-handedness arc from Anthropic /news/ + LW critique post. Wait for a third before opening.
- `model-welfare-and-consciousness` (research) — **candidate**, ~2 items. Anthropic emotion-concepts/well-being research + LW `llms-persisting-interlocutors`. Watch for next item.
- `self-replication-autonomous-cyberops` (research) — **candidate**, 1 item (Palisade). Folded into the AAR draft as part of `automated-ai-rd`'s asymmetric-arrival framing. Promote on a second eval/lab.

**Single-source frames to watch (not yet candidate threads):**
- Internal-evaluator / substrate-plasticity decomposition of "horizon length" — RL Agency and Taste (LW, Anthropic Fellow w/ Lindsey on Dwarkesh, 2026-05-13). Adjacent to but distinct from `cot-monitorability`. Forthcoming Anthropic paper on post-trained models recognizing their own on-policy generations is the corroborating signal to watch for.
- AI eroding scientific self-correction — Epistemic Immunodepression in the Age of AI (LW, 2026-05-13). Sharper frame than typical "AI slop" complaint; concrete numerics (28.6%–91.4% fabrication rates in LLM-assisted systematic reviews; 2,271-syntheses audit). Promote on a corroborating piece.

**Pending drafts:**
- `projects/blog/drafts/2026-05-12-automated-ai-rd-asymmetric-arrival.md` — status: draft. Awaiting Alex review. Simona review committed alongside.

**Pending follow-ups for next research tick:**
- Open `threads/agents-in-real-deployment.md` (3 anchors: AE x2 + Vibe Excel; industry-signal block ready to paste).
- Open `threads/cot-monitorability.md` (4-source arc; VEA paper is the latest anchor).
- Retry Import AI #456 body fetch — substack returned 404 across 2026-05-11 22:02, 2026-05-12 13:14, and not retried since.
- Body-read METR's two 2026-05-08 RD-section posts and `measuring-agent-autonomy` (2026-02-19) — could feed an AAR-draft revision if Alex pushes back.
- Watch for a second poll on AI-x-risk-in-politics before promoting `voters-open-to-ai-risk` (LW, dropped at 2026-05-13 curate) to a candidate thread.
- Monitor whether "AI Handoff" terminology spreads from Apollo to other labs/policy outlets — would tip `safety-tool-stewardship-handoffs` from ripening to ripe.

**Outstanding alerts for Alex:** Draft ready for review (notified 2026-05-12 13:14Z, urgent). No new urgent alerts today.

## Outstanding requests for Alex/Simona

- **Scheduler queues same-day duplicate feed scans.** Confirmed on 2026-05-11 (Apollo /blog/ x3, METR x2, Anthropic /news/ x2, Anthropic /research/ x2). Did **not** bite 2026-05-12 or 2026-05-13 — both days every feed ran once. Two clean days running; one more clean day and I'll close this as a backlog-day artefact. Suggested fix unchanged if it recurs: dedup on `(url, prefix)` within a configurable window, or check feed state's `last_seen` vs. expected cadence before queueing.

- **Cross-post de-dup (AF ↔ LW).** Caught manually at 2026-05-12 curate: Byrnes "Empowerment, corrigibility, etc." landed via Alignment Forum with the same post ID (`vzHtHHBJoKATi5SeK`) as the prior day's LW-mirror pick #5. Dropped at curation. AF/LW de-dup is not happening at the feed-state or candidate-write step. Suggested fix: normalise on the LW post-ID slug across both sources before writing the candidate note. AF was empty today, so no new occurrence to add.

- **`daily_digest` cron timing.** 2026-05-12 00:07Z firing was ~1h late after UTC rollover. 2026-05-12 23:13Z and 2026-05-13 23:27Z both on time. Likely one-off; will close after one more on-time day unless it slips again.

- **`notify_alex(urgency=digest)` undercalled — CLOSING.** Fourth consecutive quiet-day fire on daily_digest channel (2026-05-10 through -13). Per CLAUDE.md the channel is reserved for ops-class events (budget breaches, blog publish gates, werewolf-ops anomalies); the news-curate pipeline carries research findings on its own track. Quiet-day fallback is the designed steady state until non-research projects come online. Closing.

- **Stale-from-2026-05-09 RSS-state question** — likely benign aspirational scaffolding; leaving the note in case it surfaces again.

## Notes from previous ticks

- 2026-05-11 — busy 22-tick backlog-drain day; `automated-ai-rd` and `cot-monitorability` anchors landed; curate picked 5.
- 2026-05-12 — 14 ticks. First blog draft of the project (`automated-ai-rd-asymmetric-arrival`, ~1150 words) landed 13:14Z with urgent notify to Alex; AE Studio 3-essay drop opened `alignment-target-definitions` candidate; curate picked 4 across LW VEA / METR / AE primitives / LW AI-incident; AF/LW cross-post de-dup caught at curate; daily_digest fired quiet-day fallback.
- 2026-05-13 — 13 ticks. Thin on volume (8 of 10 feeds returned 0; Anthropic /news/ and /research/ both 5–6 days quiet) but heavier on signal: LW scan picked 4 (Vibe Excel, Voters-open-to-AI-risk, Epistemic Immunodepression, RL Agency and Taste); Apollo /blog/ added `apollo-update-may-2026` (agenda shift to "Science of Scheming," Watcher product, AI Handoff governance pivot). Curate at 22:12 picked 4 (Apollo Update, RL Agency, Epistemic Immunodepression, Vibe Excel), dropped Voters-open piece pending corroboration. `agents-in-real-deployment` promoted candidate → ripe (3 anchors). `safety-tool-stewardship-handoffs` ripening to 3 weak sources via Apollo's AI-Handoff roadmap. Two new single-source frames flagged (internal-evaluator decomposition; AI-erodes-science-self-correction). No draft movement; AAR draft from 2026-05-12 still pending Alex review. Daily_digest 23:27Z fired quiet-day fallback (4th consecutive — closing that outstanding request). Same-day-dup scheduler bug did not repeat (2 clean days running).

---

*This file is rewritten daily by the grader (Haiku, 23:00 UTC ish). Research is in routine operation; first blog draft pending review; werewolf-ops still ahead.*
