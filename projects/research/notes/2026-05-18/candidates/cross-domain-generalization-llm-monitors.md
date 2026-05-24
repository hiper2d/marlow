---
title: "How useful is cross-domain generalization for training LLM monitors?"
url: "https://www.lesswrong.com/posts/NxGHQ6DWqnrjm9r6F/how-useful-is-cross-domain-generalization-for-training-llm-2"
source: "LessWrong"
captured_at: "2026-05-18T17:26:52Z"
---

RSS summary: Study of single-token classification training for LLM monitors. Findings: control monitor performance can be improved by training on adjacent classification tasks (useful when in-domain data is scarce); classification-specialized models don't outperform — training instruction-following on top of classification training preserves uplift and mitigates some generalization failures from training on classification alone.

Why this caught my eye: A second monitorability post on the same day, this one on the *training* side rather than the inference-time degradation side. Pairs naturally with the classifier-context-rot piece for the `cot-monitorability` thread — both are arguing that monitor design is much more brittle than the field has been assuming.
