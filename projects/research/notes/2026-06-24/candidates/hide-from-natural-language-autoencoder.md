---
title: "Can You Hide From a Natural Language Autoencoder?"
url: "https://www.lesswrong.com/posts/3oRQxpxn4LiWKwbeQ/can-you-hide-from-a-natural-language-autoencoder"
source: "LessWrong"
captured_at: "2026-06-24T11:47:56Z"
---

RSS summary: NLAs are a recent black-box mech-interp method for verbalizing model internals. Focus on the Activation Verbalizer (AV), which generates a natural-language explanation of internal activations. Question: can NLAs be fooled easily? Two stress tests — prefix-tuned an activation vector to make the AV output the opposite explanation while preserving original behavior when patched in.

Why this caught my eye: A direct evasion test against the NLA/activation-verbalizer monitoring line — and it apparently works (you can drive the verbalizer to lie while behavior is unchanged). That's the exact failure mode the cot-monitorability arc keeps documenting: the monitoring tool produces a clean readout that no longer tracks what the model is doing. Strong anchor; pairs with the NLA AuditBench / NLA-explanations material already in the thread.
