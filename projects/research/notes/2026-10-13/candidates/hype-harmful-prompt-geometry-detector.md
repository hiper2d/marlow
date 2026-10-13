---
title: "Detecting NSFW and Harmful Prompts Through Geometry: Learning What's Safe Instead of What's Harmful"
url: "https://www.lesswrong.com/posts/mc6SSbhWJdCpR8trC/detecting-nsfw-and-harmful-prompts-through-geometry-learning"
source: "LessWrong"
captured_at: "2026-10-13T14:27:05Z"
---

RSS summary: ICLR 2026 paper introducing HyPE, a lightweight harmful-prompt detector that uses hyperbolic geometry and learns a single parameter from benign prompts only. Strong detection performance including against adversarial attacks; targets vision-language models. (Content warning on the post for illustrative offensive material.)

Why this caught my eye: The inversion is the hook — learning the shape of "safe" and flagging everything outside it, rather than enumerating harms. A one-parameter detector trained only on benign data is a cheap, concrete guardrail claim worth checking against the adversarial-robustness literature.
