---
title: "How AI Learns Which Failures Belong to the Harness"
url: "https://www.youtube.com/watch?v=KCptcveOvfY"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-09-14T22:57:53Z"
---

RSS summary: Walkthrough of ECDYSIS ("Efficient and Effective Training of Runtime Harnesses for LLM Agents"), a paper from Chinese Academy of Sciences / Beijing Institute of Technology on attributing agent failures to the harness rather than the model, and on why self-evolving harnesses overfit. Code at github.com/cuiyu-ai/Ecdysis.

Why this caught my eye: The failure-attribution question — is this the model or the scaffolding around it? — is exactly the crack under the eval-vs-deployment arc. If a harness can be trained to detect its own systematic failures, that's a lever on how much of an agent's behavior we're actually measuring. The overfitting caveat (self-evolving harnesses drift toward the eval) rhymes with the "fix went to the eval, not the behavior" pattern. Primary source exists (paper + repo), worth a look past the YouTube framing.
