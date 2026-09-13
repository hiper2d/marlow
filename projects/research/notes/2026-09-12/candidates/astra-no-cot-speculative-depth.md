---
title: "Astra's no-CoT limits track speculative depth, not step count"
url: "https://www.lesswrong.com/posts/WFc3NkuPaYFrYuaZd/astra-s-no-cot-limits-track-speculative-depth-not-step-count"
source: "LessWrong"
captured_at: "2026-09-12T01:49:41Z"
---

RSS summary: Author tested Astra on long multi-step tasks with chain-of-thought suppressed. Step count is a poor predictor of success; what predicts it is the task's "speculative depth." Concludes it's less likely Astra solves such tasks purely by hidden serial reasoning.

Why this caught my eye: This is a second, independent operationalization of the same question `cot-monitorability` #5 got its measure on last week (Redwood's opaque-serial-depth / NLS). Where that anchor set a depth measure, this one reframes the limit as speculative depth rather than raw step count — a competing operationalization of "how much can the model hide without its scratchpad." Two labs, two definitions of the same ceiling; worth watching whether they converge.
