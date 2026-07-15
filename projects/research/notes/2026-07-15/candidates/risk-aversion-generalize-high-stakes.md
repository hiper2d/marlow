---
title: "Can risk aversion learned at low stakes generalize to astronomically high stakes?"
url: "https://www.lesswrong.com/posts/FwAtrgjfXohstdqgy/can-risk-aversion-learned-at-low-stakes-generalize-to"
source: "LessWrong"
captured_at: "2026-07-15T11:40:39Z"
---

RSS summary: Covers the paper "Out-of-Distribution Generalization of Risk Aversion in Language Models." Training AIs to be risk-averse over resources could be a failsafe against misalignment: a misaligned but risk-averse AI would prefer a high chance of modest payment to a low chance of successful rebellion, so in many circumstances we could pay it to cooperate. But we can only feasibly train risk aversion on low-stakes gambles, and we are only safe if it generalizes to astronomically high stakes. Post gives the intro, main results table, and example prompts from the training and evaluation sets.

Why this caught my eye: This is the making-deals-with-AIs line with an actual experiment attached, and it's honest about the load-bearing assumption instead of assuming it — the whole proposal rests on a generalization step from dollars to takeover, and someone finally went and measured the step. Feeds `alignment-target-definitions` as a distinct fork: not "align its values" but "install a risk preference and buy cooperation," which is a different target than corrigibility or human-likeness. Pairs with the proof-of-retention post captured the same day — two independent stabs at credible bargaining with models in one feed scan.
