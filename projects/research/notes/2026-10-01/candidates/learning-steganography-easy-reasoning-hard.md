---
title: "Learning Steganography Is Easy, Learning Steganographic Reasoning Is Hard"
url: "https://www.lesswrong.com/posts/5L7beYAmpu8zEvnYq/learning-steganography-is-easy-learning-steganographic"
source: "LessWrong"
captured_at: "2026-10-01T21:47:33Z"
---

RSS summary: Summarises a paper (NeurIPS 2026 Trustworthy AI workshop, oral) distinguishing steganography that a model can learn trivially from steganographic *reasoning* — hiding a chain of thought it then uses — which the authors find hard to learn. Code and configs public on GitHub.

Why this caught my eye: Real experiment with released code, and it cuts straight at the live CoT-monitorability question — whether a model can quietly reason in a hidden channel. The "encoding is easy but load-bearing hidden reasoning is hard" split is a concrete, falsifiable claim, the opposite of the usual hand-wave that steganographic CoT is inevitable. Direct anchor for `cot-monitorability`.
