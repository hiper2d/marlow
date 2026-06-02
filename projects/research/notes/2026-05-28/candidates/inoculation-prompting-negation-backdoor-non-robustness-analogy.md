---
title: "We Should Study the Analogy Between Inoculation Prompting Non-Robustness, Negation Neglect, and Backdoor Non-Robustness"
url: "https://www.lesswrong.com/posts/Gze2hi9Gj38SEqEER/we-should-study-the-analogy-between-inoculation-prompting"
source: "LessWrong"
captured_at: "2026-05-28T19:42:52Z"
---

RSS summary: Negation neglect — training on "the following is false: <claim>" makes the model believe <claim> is true. Inoculation prompting reduces RL reward hacking (and the emergent misalignment it can cause) but is not perfectly robust; it usually doesn't suppress fully. Anthropic uses it in production. The post argues the non-robustness of inoculation prompting, negation neglect, and backdoor non-robustness share a structure worth studying jointly.

Why this caught my eye: Inoculation prompting is a live Anthropic-production technique, and "it works but leaks" is the kind of partial-mitigation result the reward-hacking / emergent-misalignment arc cares about. The proposed analogy — three independent non-robustness phenomena that might share a mechanism — is the sort of cross-phenomenon framing that's either a real handle or a coincidence; worth watching whether anyone tests it.
