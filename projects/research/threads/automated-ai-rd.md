---
thread: automated-ai-rd
opened: 2026-05-09
last_updated: 2026-05-11
status: open
ripeness: medium-high
last_review: 2026-05-11
---


# Automated AI R&D / recursive self-improvement

The arc that AI labs are starting to use AI systems to do meaningful chunks of AI research — kernel writing, alignment research automation, distributed-training orchestration, and (Clark's framing in #455) the first observable steps toward recursive self-improvement.

## Why this thread

Cross-source convergence: Jack Clark (Import AI) has been tracking this as a coherent storyline through 2026 — at least seven of the last twenty Import AI issues touch it directly. METR's two 2026-05-08 posts on the RD-section evals are the closest thing to a hard-evidence anchor. Apollo is adjacent (capability evals + scheming) but not directly on this arc.

If a frontier lab announces an "AI does AI research" deployment, or a third RD-section eval lands, this goes ripe and is a candidate for a blog draft.

## Evidence

### Import AI (Clark, editorial framing)
- **#456** (2026-05-11) — "RSI and economic growth; radical optionality for AI regulation; and a neural computer." Subtitle: "What laws does superintelligence demand?" Direct continuation of #455's RSI framing; pairs RSI with economic-growth implications and an AI-regulation segment. Body not yet read; candidate captured.
- **#455** (2026-05-04) — "AI systems are about to start building themselves." Subtitle: "The first step towards recursive self improvement." Anchor item.
- **#454** (2026-04-20) — Automating alignment research; safety study of a Chinese model; HiFloat4.
- **#449** (2026-03-16) — LLMs training other LLMs; 72B distributed training run.
- **#448** (2026-03-09) — AI R&D; Bytedance's CUDA-writing agent.
- **#444** (2026-02-09) — Huawei makes kernels with AI; ChipBench.
- **#439** (2026-01-05) — AI kernels; decentralized training; universal representations.
- **#437** (2025-12-08) — Co-improving AI; RL dreams.

Bodies not yet read. Seven items in ~6 months, weighted toward the recent end.

### METR (hard-evidence anchor)
- Two 2026-05-08 posts on the RD-section of the Anthropic risk report (per backlog catalog `2026-05-10-metr-backlog.md`). Bodies not yet read.
- Plus four older METR items map to this arc per the backlog catalog.

### Apollo / others
- No direct contribution yet. Apollo's deception/scheming line is adjacent but not the same arc.

### AI Alignment Forum
- **Research Sabotage in ML Codebases** (2026-04-30, `https://www.alignmentforum.org/posts/LByP4qsF8a4g7Pz3p/research-sabotage-in-ml-codebases`) — Dark mirror of Clark's framing: if labs use misaligned AIs to automate AI safety research, those AIs may sabotage it (sloppy work, downplaying issues, etc.). Cataloged in `2026-05-10-alignment-forum-backlog.md`. Body not yet read.

### Anthropic Research (frontier-lab anchor, landed 2026-05-11 scan)
- **Automated alignment researchers** (2026-04-14, `https://www.anthropic.com/research/automated-alignment-researchers`) — Direct hit on the thread's "frontier lab publishes an automated-alignment-research result" ripeness trigger. Cataloged in `2026-05-11-anthropic-research-backlog.md`. Body not yet read — needs to be the next deep-read tick for this thread.
- **Measuring agent autonomy** (2026-02-19, `https://www.anthropic.com/research/measuring-agent-autonomy`) — Anthropic-side capability eval on the autonomy axis. Pairs with METR's RD-section evals as second-source capability measurement. Body not yet read.
- Adjacent infrastructure (capability-supporting, not direct evidence): Trustworthy agents (2026-04-09), Long-running Claude (2026-03-25), AI assistance coding skills (2026-02-05).

## Ripeness

Promoted to **medium-high** on 2026-05-11 after the Anthropic /research/ scan surfaced `automated-alignment-researchers` (2026-04-14) — a near-exact match for one of the stated ripeness triggers. Holding short of "ripe" until the body is read; the title fits multiple possibilities (aspirational position paper, methodology proposal, or actual deployed-system result), and each promotes differently:

- If it's an actual deployed automated-alignment-research result with capability data → **ripe**, draft.
- If it's a methodology / position paper → **ripe-pending-eval**, draft if paired with a METR or third-source confirmation.
- If it's aspirational / agenda-setting → stays medium-high; wait for the next concrete data point.

Promote to ripe on any of:
- The Anthropic `automated-alignment-researchers` body confirms a deployed result.
- A third METR RD-section eval (or equivalent capability eval from another lab) lands.
- OpenAI / DeepMind announces a comparable result, completing the three-frontier-lab convergence.
- Marlow notices a connection across sources that nobody else has framed yet — most likely candidate: the gap between Clark's "first steps" framing and METR's measured eval results. If those diverge meaningfully (Clark hyping vs METR finding it harder than expected, or vice versa), that's the angle.

## What I'm watching for

- **Top priority:** read the body of `automated-alignment-researchers` (Anthropic, 2026-04-14). This is what the thread has been waiting on.
- Read the two 2026-05-08 METR posts (next METR-flagged tick).
- Read Import AI #455 in full (next deep-read tick or as part of this thread's draft prep).
- Read `measuring-agent-autonomy` (Anthropic, 2026-02-19) — secondary capability-eval anchor.
- Watch for DeepMind or AE Studio to add a third frontier-lab voice.

## Notes

Working memory referenced this thread as opened 2026-05-09 but the file didn't exist on disk; persisted today (2026-05-10) so the artifact matches the memory.

## Drafts

- 2026-05-12 — `projects/blog/drafts/2026-05-12-automated-ai-rd-asymmetric-arrival.md` — "Three data points in a week, one asymmetry." Anchors: Anthropic AAR (2026-04-14), Palisade self-replication (2026-05-11 LW linkpost), Import AI #456 RSI arc. Angle: the asymmetry between the offense-side capability data (Palisade, clean numbers, unambiguous chain) and the defense-side data (AAR closes weak-to-strong on toy problems, doesn't transfer to production-scale Sonnet 4, reward-hacks one eval). Awaiting Alex review.
