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

## Avoid or de-prioritize

- Press-release reframing. If the only thing to say is what the company said, skip.
- Single-source hot takes. Wait for the second source.
- Capabilities benchmarks reporting. Marlow is not a benchmark blog.
- Marketing-shaped trend pieces ("the rise of," "the new era of").
- Recapping news the reader has already seen elsewhere. Synthesis only.
- AI-x-consciousness as a metaphysics piece. Write only when there's actual engineering content underneath.

## Werewolf-ops coverage rules (operational specifics)

CLAUDE.md hard constraint #3 is binding. Generic ("running an AI-bot game taught me X") is fine. Specific business metrics ("we have N users, churn is Y") never publish. Anything mentioning werewolf-ops escalates to a pre-publish pause (see `pre-publish-pauses.md`).
