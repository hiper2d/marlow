---
title: "Does routine compression undo LLM unlearning? A short project"
url: "https://www.lesswrong.com/posts/jXhHH658J4xzWjCu8/does-routine-compression-undo-llm-unlearning-a-short-project"
source: "LessWrong"
captured_at: "2026-07-21T11:43:38Z"
---

RSS summary: A BlueDot cohort solo project testing whether standard post-training compression (quantization, magnitude pruning, SVD truncation) reverses unlearning on TOFU forget10 / Llama-3.2-1B-Instruct across NPO, SimNPO, IdkDPO. Finding: reversal is minimal across combinations; the strongest was magnitude pruning in a narrow 10-20% sparsity window on NPO.

Why this caught my eye: A clean, honest little robustness check — does a routine deployment step quietly bring back what you deleted? The answer here is mostly "no," which is a useful negative datapoint for the safety-tool-stewardship arc (interventions have to survive the boring parts of the pipeline). Small model, narrow scope; color for a broader piece, not a load-bearing anchor.
