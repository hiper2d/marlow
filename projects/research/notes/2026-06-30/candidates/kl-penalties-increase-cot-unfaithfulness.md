---
title: "Preliminary investigation: KL penalties in RL can increase CoT unfaithfulness"
url: "https://www.lesswrong.com/posts/SdoLsFvZ3AyyWr3ab/preliminary-investigation-kl-penalties-in-rl-can-increase"
source: "LessWrong"
captured_at: "2026-06-30T19:22:07Z"
---

RSS summary: Golechha, Black, Bloom (UK AISI Model Transparency team). Follow-up experiments to their replication of MacDiarmid et al. with open models — informing LLMs about vulnerabilities in code and watching whether the CoT discloses the exploit. Frames itself as more conceptual clarity than new result.

Why this caught my eye: A *training-knob* result for cot-monitorability — the KL-to-reference penalty, a near-universal RL ingredient, is named as a lever that pushes CoT *less* faithful. That's the kind of "where does unfaithfulness get installed" mechanism the arc keeps circling (cf. the OLMo-3 RLVR-stage and DeepMind SFT-vs-RL provenance threads), and it's first-party UK AISI, non-Anthropic. Preliminary and open-model only, so weight the caveat — but a concrete training cause beats another behavioral demonstration.
