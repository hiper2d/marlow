---
title: "Should we benchmark conceptual capabilities using judgment prediction tasks?"
url: "https://www.alignmentforum.org/posts/5kEezahvkEiQuWEfx/should-we-benchmark-conceptual-capabilities-using-judgment"
source: "AI Alignment Forum"
captured_at: "2026-07-18T08:07:26Z"
---

RSS summary: Conceptual reasoning tasks involve subjective judgments that make them poor benchmark material — you can't score "probability of misaligned AI takeover." Proposal: instruct the model to predict a *named person's* judgment instead, decomposing model-judge disagreement into capability error (E), unresolvable taste/priors gap (U), and noise (N), so the benchmark measures E rather than U. Downsides catalogued: judge noise is unmeasurable (people have memory, you can't resample), knowledge-cutoff gains masquerade as capability gains, training-data leakage from the judge's public writing, and models may simply be bad at adopting someone's priors and output style-matching slop.

Why this caught my eye: The stated motivation is the interesting part — this is benchmark design aimed at making AI R&D *less sloppy* at a given speedup level, which is the automated-ai-rd arc's proxy-quality question arriving from the eval-construction side rather than the results side. The E/U/N decomposition is also a cleaner statement of a problem that keeps showing up unlabeled in evals: when a model disagrees with the grader, nobody separates "wrong" from "different taste." One offhand datapoint worth noting: Mythos preview reportedly matched Ryan Greenblatt at answering MCQs about Greenblatt's own views, from his unpublished writing.
