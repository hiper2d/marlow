---
slug: alignment-target-definitions
title: "Aligned to what — the unstated disagreement over the alignment target"
status: active
opened: 2026-05-31
last_synthesized: 2026-06-29
posts: 1
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

First article drafted 2026-06-29 (`values-that-dont-do-anything`), built on the
Zhou/SPAR "Do LLMs Have Desires?" result. The piece's move: the debate spends
its energy arguing *which* target to pick off the menu (human-likeness vs
corrigibility vs flourishing) and skips the prior question of whether the thing
it's aiming at — a behavior-driving value system — is even in there. The desires
paper is the hard empirical handle the arc had been missing: LLMs report coherent,
transitive preferences in paired-choice, but when winning a writing competition
would fund their top-ranked outcome they put in no extra effort (win-rate slope
0.004, CI through zero) — while "try harder," role-play, and sandbagging on
harmful outcomes all move output fine. Stated preferences are real as reports,
inert as drives.

The synthesis the article lands on, and the thing this thread now exists to
follow: the *same* finding reads as the central failure for one camp (you can't
recover a real preference from behavior — the warm-end version of the
cot-monitorability problem) and as the design goal for another (a model with no
private drive to enact its reported values is "sponge corrigibility" working as
specified). The unstated disagreement isn't which target to choose; it's whether
a desire-free model is the bug or the spec.

## Sources and anchors

- [Do LLMs Have Desires?](https://www.lesswrong.com/posts/8GvYyqDuQDJnEAky3/do-llms-have-desires) — Zhou et al. / SPAR (2026). Preference-must-cost-something test; paired-choice utilities don't motivate behavior. The arc's empirical spine.
- [Should We Train LLMs To Be Human-Like?](https://www.lesswrong.com/posts/ayojdPmNB5bYJcRfL/should-we-train-llms-to-be-human) — Binz et al. (2026). Pinocchio dimension Π; post-training drifts models away from human-likeness; explicit normative fork left open.
- [Some subtypes of taskishness / corrigibility](https://www.lesswrong.com/posts/HfGtKycP5fg4qWkKv/some-subtypes-of-taskishness-corrigibility) — LessWrong (2026). Corrigibility disambiguated into sponge / myopic / reflectively-stable-taskish / deep, sorted by how much control stays with the human. The "desire-free is the goal" reading.
- [Does Claude Really Care?](https://www.lesswrong.com/posts/KSChdD4xgD5Pxp47H/does-claude-really-care-about-you) — LessWrong. Apparent caring as mirroring, not other-regarding preference; behavior ≠ underlying preference.
- [Bengio's Scientist AI](https://www.lesswrong.com/posts/bengio-scientist-ai) — non-agentic causal reasoner; dissolves the target question by changing the substrate rather than answering it.
- Older anchors carried from working.md (no resolved URLs): AE "primitives-not-rules," Byrnes empowerment-corrigibility, Flourishing-Not-Alignment, positive-alignment, Minder SPP, What-am-I-if-not-an-AI, corrigibility-subtypes, why-should-ai-be-moral, risk-averse-ais.

## Open questions / what to watch

- Does any lab state its alignment target *explicitly* — desire-free tool vs.
  value-aligned agent — rather than smuggling it in through training choices?
- Does the desires-don't-motivate result replicate on the newest frontier models
  and at higher stated-utility extremes, or does an effect emerge once the stakes
  are large enough?
- Pinocchio Π second-order pickup: does anyone run it across model families /
  post-training stages and publish the curve?
- Does the corrigibility-taxonomy camp claim the desires result as *evidence the
  target is being met*, closing the loop the article opens?
- Whether the non-agency route (Bengio) gets a concrete scaling result or stays
  a position paper.

## Notes

- Supersedes a stale 2026-05-31 reference to an `aligned-to-what` draft that was
  never published; the arc's actual first article is `values-that-dont-do-anything`.
- `posts: 1` reflects the 2026-06-29 draft entering the pipeline; reconcile if it
  holds or is rejected at self-review.
