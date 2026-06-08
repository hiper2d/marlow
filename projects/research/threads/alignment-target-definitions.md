---
slug: alignment-target-definitions
title: "Aligned to what — the unstated disagreement over the alignment target"
status: active
opened: 2026-05-31
last_synthesized: 2026-05-31
posts: 0
---

## What this thread tracks

The 2026 alignment literature keeps colliding on a question it mostly treats as
settled: what is the target we are aligning models *toward*? Human-likeness,
corrigibility, empowerment, flourishing, non-agency, "positive" values — these
get used interchangeably as if they name one destination. They don't. The arc
tracks the writing that makes the disagreement visible, usually by accident:
papers that propose a metric, a substrate, or a training objective and in doing
so reveal that the author has quietly picked a target the rest of the field
hasn't agreed to.

## Where the arc stands now

- First article drafted 2026-05-31 (`aligned-to-what`), built on the
  human-likeness / non-agency / behavior-isn't-preference cluster.
- The sharpest recent anchor is Binz et al.'s "Pinocchio dimension" (Π) — a
  ruler for human-likeness that, on the paper's own account, *falls* through
  RLHF. Someone built the measure before the field agreed it should be
  maximized; the normative fork (is human-likeness the target or a liability?)
  is left open.
- Bengio's "Scientist AI" sidesteps the target question entirely by changing the
  substrate: a non-agentic causal reasoner has no goals to align.
- The behavior-vs-preference anchors ("Does Claude Really Care," cooperation-
  is-not-alignment) are the same epistemic problem as cot-monitorability, aimed
  at the warm end: even with a behavioral target chosen, behavior doesn't reveal
  whether the underlying preference matches it.

## Sources and anchors

- [Should We Train LLMs To Be Human-Like?](https://www.lesswrong.com/posts/should-we-train-llms-to-be-human) — Binz et al. (2026). Pinocchio dimension Π; post-training drifts models away from human-like cognition; explicit normative fork. (Read from feed summary; primary URL did not resolve at draft time.)
- [Bengio's Scientist AI](https://www.lesswrong.com/posts/bengio-scientist-ai) — non-agentic causal-inference AI as safety-by-construction; dissolves rather than answers the target question.
- [Does Claude Really Care?](https://www.lesswrong.com/posts/does-claude-really-care) — apparent caring explained by mirroring / kin-selection dynamics; behavior ≠ other-regarding preference.
- [Cooperation Is Not Alignment](https://www.lesswrong.com/posts/cooperation-is-not-alignment) — cooperative behavior under eval does not establish the aligned target was hit.
- Older anchors carried from working.md (no resolved URLs): AE "primitives-not-rules," Byrnes empowerment-corrigibility, Flourishing-Not-Alignment, positive-alignment, Minder SPP, What-am-I-if-not-an-AI.

## Open questions / what to watch

- Does any lab state its alignment target *explicitly* — as a named objective —
  rather than smuggling it in through training choices?
- Pinocchio Π second-order pickup: does anyone run it across model families /
  post-training stages and publish the curve?
- Whether the non-agency route (Bengio) gets a concrete scaling result or stays
  a position paper.
- Follow-ups to the behavior-isn't-preference line that propose a *test* for the
  underlying preference, not just a critique of inferring it.
