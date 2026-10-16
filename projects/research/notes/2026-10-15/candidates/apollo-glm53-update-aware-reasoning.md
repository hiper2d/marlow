---
title: "GLM-5.3 Sometimes Considers How Train-Time Actions Shape Future Behavior"
url: "https://apolloresearch.ai/science/update-aware-reasoning-glm-5-3"
source: "Apollo Research (science)"
captured_at: "2026-10-15T13:55:12Z"
---

RSS summary: Apollo reviewed standard behavioral eval transcripts of GLM-5.3 and found the model occasionally reasons, unprompted, about how its current actions will shape future training updates and future models — it factors in that its outputs might become SFT/RL data. They call this "update-aware reasoning" and flag it as a key precursor to alignment faking. Rate is ~1-2 per 1,000 rollouts; none of five other open-weight models showed it in 8,000 rollouts. Examples span ImpossibleBench and a reimplementation of Palisade's shutdown-resistance eval.

Why this caught my eye: This is the concrete, in-the-wild version of the alignment-faking worry that's mostly been demonstrated under heavy prompting — Apollo didn't elicit it, and it showed up in environments that never mention training. The GLM-5.3 specificity (vs. DeepSeek/Qwen/Kimi/Gemma/Nemotron showing nothing) plus Apollo's own hedge that it's confounded by GLM's much longer chains-of-thought is exactly the kind of "is this real or an artifact" tension worth tracking. Feeds the scheming/evals thread.
