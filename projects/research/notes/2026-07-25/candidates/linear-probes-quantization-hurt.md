---
title: "Linear probes tell you where quantization will hurt"
url: "https://www.lesswrong.com/posts/oJJyYDgPD95jEfvQx/linear-probes-tell-you-where-quantization-will-hurt"
source: "LessWrong"
captured_at: "2026-07-25T11:41:56Z"
---

RSS summary: Epistemic status: one encoder family (BERT-base), one decoder LLM (Qwen2.5-3B), one seed, token-level tasks, post-training weight quantization. Connects quantization to a general mech-interp idea — the model does easy syntax work first, semantic work in later layers — to predict where quantization damages behavior.

Why this caught my eye: A small, honest interp result (the author front-loads its narrowness) using linear probes as a *predictive* tool rather than a post-hoc explanation. Niche and single-model, but it's the kind of "probes actually forecast something" claim worth watching against the broader "detectors don't transfer" pattern on the monitorability arc. Low-confidence pick; interp-adjacent.
