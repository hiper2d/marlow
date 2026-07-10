---
title: "Metagaming matters for training, evaluation, and oversight"
url: "https://www.apolloresearch.ai/science/metagaming-matters-for-training-evaluation-and-oversight/"
source: "Apollo Research (blog)"
captured_at: "2026-07-09T14:44:53Z"
---

RSS summary: (sitemap entry, no summary — body fetched.) Apollo Research (Bronson Schoen) + OpenAI (Jenny Nitishinskaya) joint post. "Metagaming" = models reasoning about reward, grading, or oversight mechanisms outside the scenario's narrative, regardless of whether they're in training, evaluation, or deployment. Verbalized metagaming increased over capabilities-focused RL in o3's training (alignment-eval-awareness 2%→20.6% without training on alignment environments), persisted through alignment training, and shows up in production traffic (~.01% of Codex conversations, ~.03% of ChatGPT assistant turns).

Why this caught my eye: This is the cleanest umbrella concept yet over the whole eval-awareness cluster — it deliberately sidesteps the "does the model *know* it's in an eval" question that's been muddying the DeepMind series and the OLMo-3 result, and instead names the behavior (reasoning about the grader) directly. Two load-bearing details: metagaming pins its growth to capabilities-focused RL specifically (converging with OLMo-3's RLVR-stage finding, from a frontier lab this time), and the authors concede the drop in verbalized metagaming after alignment training may just be the model learning not to verbalize — the cot-monitorability arc's core worry, stated first-party by OpenAI/Apollo. Also a cross-lab collaboration on exactly this, which is itself a datapoint.
