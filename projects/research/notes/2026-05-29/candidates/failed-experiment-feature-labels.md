---
title: "How a failed experiment broke (and fixed) my view on feature labels"
url: "https://www.lesswrong.com/posts/zDcrmqdqvh3KmsBuF/how-a-failed-experiment-broke-and-fixed-my-view-on-feature"
source: "LessWrong"
captured_at: "2026-05-29T17:15:13Z"
---

RSS summary: Proposes a feature-label generation method ("baez") that uses NLA explanations instead of activation examples, scored across three benchmarks. Result: baez ≈ eleuther_acts_top5 despite using entirely different inputs — and, more surprisingly, all the scores sit close to chance, suggesting either the label-generation methods or the benchmarks themselves are broken.

Why this caught my eye: An honest negative-result post that lands on the NLA-explanations canon already in `cot-monitorability`/`safety-tool-stewardship-handoffs`. The near-chance scores across the board are the interesting part — if the *benchmarks* can't distinguish good feature labels from random ones, that's a measurement-validity problem for the whole SAE-labeling line, echoing the steering-as-explanations-not-handles negative result from -27. Worth a body read to see which way the author resolves the "methods or benchmark" fork.
