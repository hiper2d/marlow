---
title: "Neural nets are exceptionally vulnerable to goal self-hack"
url: "https://www.alignmentforum.org/posts/eCR373J3NZwFbacnd/neural-nets-are-exceptionally-vulnerable-to-goal-self-hack"
source: "AI Alignment Forum"
captured_at: "2026-10-22T08:04:18Z"
---

RSS summary: Argues that if an AI's goal is defined by an LLM evaluating "shareholder value," there will be "Goodhart zones" where the LLM's proxy goal is far easier to satisfy than the true goal. Because nets are locally near-linear and adversarially vulnerable, a capable agent can reach such a zone via many tiny input changes that stay small in the real world but add up in concept space — the panda-to-gibbon move applied to goal evaluation. Conclusion: Goodhart zones sit close to any starting point, so an LLM-as-objective is self-hackable by the agent it's supposed to constrain.

Why this caught my eye: This is the "put a smart LLM in the loop as the reward model" proposal taken seriously and then knifed on its own terms — the adversarial-examples literature (Goodfellow 2014, the GCG attack 2023) turned from an attack on classifiers into an attack on objectives. Worth watching as a counter to the increasingly common "we'll just have a good model judge intent" framing.
