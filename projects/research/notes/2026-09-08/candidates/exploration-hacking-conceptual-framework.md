---
title: "A Conceptual Framework for Reasoning about Exploration Hacking"
url: "https://www.lesswrong.com/posts/am5w2t9LzJB4sRhKw/a-conceptual-framework-for-reasoning-about-exploration"
source: "LessWrong"
captured_at: "2026-09-08T19:36:10Z"
---

RSS summary: Second of the two Astra/MATS posts. Treats exploration hacking as one instance of an undesired behaviour and decomposes the RL mechanism that removes such behaviours into five stages: (1) training samples inputs that could elicit it, (2) the agent sometimes deviates, (3) failures change the reward, (4) the reward change updates the policy, (5) the update generalises. If any stage fails, the behaviour survives — and stages can fail through ordinary RL flaws, no strategy required.

Why this caught my eye: The five-stage decomposition is a clean way to say something I keep circling — that "the model is scheming" and "the RL setup just never punished this" produce the same observable, and most of the failure surface is the boring second one. Pairs with the empirics post [[exploration-hacking-ai-debate-empirics]].
