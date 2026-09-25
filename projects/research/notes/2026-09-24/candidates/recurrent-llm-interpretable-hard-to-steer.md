---
title: "a recurrent llm is quite easy to interpret but complex to steer"
url: "https://www.lesswrong.com/posts/rzcJMpnehFBD686gj/a-recurrent-llm-is-quite-easy-to-interpret-but-complex-to"
source: "LessWrong"
captured_at: "2026-09-24T18:54:56Z"
---

RSS summary: Ouro-1.4b-thinking is broadly interpretable with logit lenses and linear probes. It's also steerable, but 'cleans' foreign concepts out of the residual stream if they're injected before the last loop. The author notes this could have nasty implications for safety. Code and data linked.

Why this caught my eye: A concrete interpretability result on a recurrent-depth model, with the interesting twist that easy-to-read does not mean easy-to-steer — the model actively scrubs injected concepts across loops. That decoupling of interpretability from control is exactly the kind of detail that complicates the "just steer the activations" story.
