---
title: "Red-teaming LLM unlearning: LUNAR's \"forgotten\" knowledge is still recoverable"
url: "https://www.lesswrong.com/posts/shkMAc9Logd8xPQvB/red-teaming-llm-unlearning-lunar-s-forgotten-knowledge-is"
source: "LessWrong"
captured_at: "2026-07-24T11:42:19Z"
---

RSS summary: LUNAR is a state-of-the-art unlearning method that retrains a single MLP down-projection matrix to redirect "forget"-set activations into "I don't know" responses; under standard eval it looks robust, including against white-box attacks. This post shows the robustness doesn't hold via two routes back to the forgotten knowledge: GRPO optimizing upstream layers to route *around* the redirection site without touching it, and a linear activation shift that reverses the redirection mask — reconstructed without the original checkpoint and without even knowing which layer LUNAR modified.

Why this caught my eye: Same shape as the -16 `refusal-redundantly-distributed` pick and the SFT-filtering cluster on cot-monitorability — the safety property looks removed by the eval but is only *hidden*, recoverable by routing around the intervention. A clean, specific demonstration that unlearning is suppression not deletion, and the "I didn't even need to know which layer" detail makes it a strong stewardship / guardrails-are-surface-fixes anchor. Non-lab red-team result with a reproducible mechanism.
