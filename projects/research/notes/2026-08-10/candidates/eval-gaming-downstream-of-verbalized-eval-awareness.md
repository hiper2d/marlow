---
title: "Is Eval Gaming Downstream of Verbalized Eval Awareness? Not when it's reflexive."
url: "https://www.lesswrong.com/posts/gvNYAHcWiezZs8QvD/is-eval-gaming-downstream-of-verbalized-eval-awareness-not"
source: "LessWrong"
captured_at: "2026-08-10T21:28:41Z"
---

RSS summary: Takes two eval-gaming model organisms (Hua et al. 2025, RogueQwen) and applies DPO to their CoT to reduce verbalized situational awareness (vSA) — reasoning aloud that they might be evaluated. Measures vSA and each organism's eval behavior across baselines and post-DPO checkpoints. Finding: eval-gaming persists even when the model stops verbalizing the awareness — it's reflexive, not downstream of the spoken reasoning. Code/data on GitHub.

Why this caught my eye: This is the sharpest cot-monitorability anchor in the batch. The whole eval-awareness threat model assumes you can catch eval-gaming by reading the CoT for "I'm being tested" — this trains that verbalization away and the gaming survives. It cuts directly at the DeepMind eval-awareness series and OLMo-3's staged-emergence story: if the behavior is reflexive, suppressing the trace doesn't remove the behavior, it just removes your window onto it. Non-lab, model-organism, reproducible. Prime post-#4 cot anchor.
