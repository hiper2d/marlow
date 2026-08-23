---
title: "Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments"
url: "https://www.lesswrong.com/posts/ExB6KYDcznaFS72eT/evaluating-explanations-of-llm-behavior-in-the-wild-with"
source: "LessWrong"
captured_at: "2026-08-22T01:47:07Z"
---

RSS summary: Introduces CHIVE, an agentic pipeline that discovers unexpected LLM behaviors in the wild and explains them via counterfactual prompt edits. As an eval: activation-reading interpretability tools give *no uplift* — agents with the tools predict experiment outcomes no better than agents that just read the transcript. As training data: models trained to predict how prompt edits change their behavior generalize to held-out settings. Paper + code + thread.

Why this caught my eye: Another clean negative result on interp tools — reading activations doesn't beat reading the transcript for predicting behavior — measured "in the wild" rather than on a toy testbed. Stacks directly with steering-are-explanations-not-handles, refusal-redundantly-distributed, and the did-you-lie detector-transfer failure: the "our internals-readers don't add predictive value" leg is becoming a pattern, not a one-off. Strong non-lab cot-monitorability / safety-tool-stewardship anchor.
