---
title: "On Qwen, the J-lens readouts at the newline token reveal lies"
url: "https://www.lesswrong.com/posts/bhvaAbSPZgiG3oJPu/on-qwen-the-j-lens-readouts-at-the-newline-token-reveal-lies-4"
source: "LessWrong"
captured_at: "2026-10-19T11:42:49Z"
---

RSS summary: Four models (Qwen3.6-27B, two Gemma-3, gpt-oss-20b) run through MASK pressure scenarios where a system prompt gives the model a role and a reason to lie. The residual stream is read at chat-template tokens with the J-lens, readout words grouped into meaning-families, and the frequency of each family compared after lies vs. after truths.

Why this caught my eye: A cheap, token-position-specific white-box lie signal across open-weight models — the optimistic counterpart to the probe-evasion results landing the same morning. Worth watching whether the newline-token readout survives the kind of evasion training the other LW posts describe. Interpretability / deception-detection.
