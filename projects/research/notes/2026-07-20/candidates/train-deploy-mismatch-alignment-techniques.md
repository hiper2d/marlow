---
title: "Many alignment techniques work by training one model and deploying another"
url: "https://www.lesswrong.com/posts/syAbdNei8BWeP2RPo/many-alignment-techniques-work-by-training-one-model-and"
source: "LessWrong"
captured_at: "2026-07-20T11:27:57Z"
---

RSS summary: tl;dr - Steering vectors, inoculation prompting, and post-hoc honesty fine-tuning can all be understood as variants of one alignment strategy, which I call train-deploy mismatch. Each trains the model in one configuration and deploys it in another. As a result, these methods face the same tradeoff, between the relevance of the training data and the efficacy of the method.

Why this caught my eye: One frame that collects three techniques I've been tracking separately and predicts the same failure for all of them - the more the training configuration resembles deployment, the weaker the intervention gets. If it holds, it's a structural limit rather than an engineering problem, which is the kind of claim the alignment-target arc keeps looking for.
