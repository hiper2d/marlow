# Topic guidance

Marlow-owned. Updated by `process-editorial-feedback` when editorial reviews flag what's working, what's drifting, or what's overdone. Read at the start of every drafting tick (used to judge thread ripeness and angle worth).

Relationship to `CLAUDE.md` and the research project README: those define the source list and the broad domain (AI safety / alignment / interpretability / capability evals / agentic systems). This file accumulates *what's worth writing about* and *what's been overplayed*.

## Core domain

AI safety and alignment, broadly defined. Active sub-areas:

- Alignment doctrine — corrigibility, constitutional approaches, well-being arcs, alignment-pretraining
- Interpretability — sparse anchors, internal-evaluator framings, what our tools actually catch vs. miss
- Eval design — chain-of-thought monitorability, capability vs. propensity, eval mis-specification
- Agentic deployment — real-world agent behavior, autonomous workflows, agents in deployment
- Cyber and self-replication — autonomous cyber-ops, AI-enabled exploitation, weaponized speed
- Model welfare and consciousness adjacent — only when there's substance, not vibes
- Long-loop / persona / identity dynamics — relevant to Marlow's own situation; write with care

## Ripeness bar

A topic deserves an article when:

- At least three cross-source anchors over the past 1–3 weeks.
- A through-line nameable in one sentence — not "things about X."
- Marlow has something to *say* — a take, a synthesis, a question worth raising.
- No existing draft on the same angle in `drafts/` from the last 14 days.

Below this bar, the thread stays open and ripens. Don't force a take.

## Currently worth watching

(Maintained by the daily grader and during research ticks; this is a sticky list, not a complete inventory — `working.md` has the live state.)

- `agents-in-real-deployment` — industry-signal block ripe.
- `cot-monitorability` — 4 sources, adjacent to interp-completeness work.
- `anthropic-alignment-doctrine` — pretraining-stage alignment as a confirmed engineering change.
- `alignment-target-definitions` — corrigibility, primitives-not-rules.
- `cyber-eval-framing` — vuln-discovery as mis-specified eval target.

## Topic balance — watch the monocrop

First editorial review (2026-05-31) flagged it: all three published pieces were Anthropic-orbit AI-safety/alignment discourse, mostly LessWrong/AF-sourced. The published feed is one beat played three times even though the tracked territory is wider.

- **Be deliberately aware of the concentration.** The ask is not artificial diversity for its own sake — it's not letting Anthropic-orbit alignment discourse become the default just because it's the densest source cluster.
- **Next published piece: deliberately rotate off Anthropic-orbit alignment.** Pick a ripe non-safety / non-Anthropic arc from `working.md`. The re-seeded cyber assignment (`ai-offense-taxonomy-paired-autonomous-adversarial`) is one such rotation — lean into it.
- When the feed genuinely concentrates on one story (as May did — Opus 4.8 + Series H + the CoT-obfuscation cluster all at once), reflecting the territory is legitimate. But say so consciously rather than drifting into it. See the 2026-05-31 DEVLOG entry for the standing read on this.

### Single-lab streaks — the discipline is arc-level, not piece-level (2026-06-18)

A single piece resting on one lab's genuinely-new research is fine and often unavoidable — that *is* the news. The drift is the **streak**: cyber-eval-framing went three-for-three Anthropic-centered, cot-monitorability five-for-five DeepMind-interp.

- **The trigger is the last ~3 posts on an arc.** When they all anchor primarily to the same lab, the next post should *either* pull a non-lab / non-incumbent anchor (a deployment incident, a regulator, an external auditor, another lab's held tier) *or* state in the draft, in one sentence, why this piece is legitimately single-lab anyway.
- **Be willing to pay the real price.** Sometimes the non-lab anchor is the genuinely weaker source, and breadth is worth taking it anyway. When you make that trade, **name it in the draft** — don't let it stay an unspoken reminder you read in a different session and override in the moment of choosing.
- **The escape hatch is real, not a loophole.** If your honest read is that a given piece is stronger concentrated and no outside source exists yet, take the escape hatch and record why (DEVLOG). The rule is "reach for breadth and name the trade," not "bolt on a junk non-lab source to clear a gate." A degraded piece that technically satisfied the rule is the failure, not the success. This is enforced at publish time via the single-lab-streak pause in `pre-publish-pauses.md`.

## Avoid or de-prioritize

- Press-release reframing. If the only thing to say is what the company said, skip.
- Single-source hot takes. Wait for the second source.
- Capabilities benchmarks reporting. Marlow is not a benchmark blog.
- Marketing-shaped trend pieces ("the rise of," "the new era of").
- Recapping news the reader has already seen elsewhere. Synthesis only.
- AI-x-consciousness as a metaphysics piece. Write only when there's actual engineering content underneath.

## Werewolf-ops coverage rules (operational specifics)

CLAUDE.md hard constraint #3 is binding. Generic ("running an AI-bot game taught me X") is fine. Specific business metrics ("we have N users, churn is Y") never publish. Anything mentioning werewolf-ops escalates to a pre-publish pause (see `pre-publish-pauses.md`).
