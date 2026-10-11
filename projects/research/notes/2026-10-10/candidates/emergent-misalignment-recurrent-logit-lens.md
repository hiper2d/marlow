---
title: "Examing Emergent Misalignment in a recurrent LLM with a logit lens"
url: "https://www.lesswrong.com/posts/NskJJLSvJmHY2oBaa/examing-emergent-misalignment-in-a-recurrent-llm-with-a"
source: "LessWrong"
captured_at: "2026-10-10T19:38:24Z"
---

RSS summary: Builds on prior mech-interp work on a recurrent LLM. Reports a logit lens can recover a chain-of-thought equivalent from the model, loop index is linearly represented, and steering concepts transfer between loops — now applied to emergent misalignment.

Why this caught my eye: Interpretability on a recurrent architecture, where the "CoT" is recovered from loop structure rather than emitted tokens. That's the latent-reasoning / CoT-monitorability seam from the other side — if reasoning lives in loops not tokens, monitoring the visible chain misses it.
