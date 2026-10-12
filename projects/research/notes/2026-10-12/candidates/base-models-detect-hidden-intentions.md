---
title: "Base Models Can Detect Hidden Intentions that Prompted Classifiers Miss"
url: "https://www.lesswrong.com/posts/YvNkA3ZzsCv9QQmXR/base-models-can-detect-hidden-intentions-that-prompted"
source: "LessWrong"
captured_at: "2026-10-12T18:43:29Z"
---

RSS summary: Builds on the Persona Selection Model (post-training selects a pre-trained persona) and subliminal learning (Cloud et al. — covert traits transfer through unrelated outputs). Claims that base pre-trained models, appropriately prompted, can surface hidden intentions that prompted classifiers on the post-trained model miss.

Why this caught my eye: A monitorability result with a counterintuitive shape — the *base* model as a better intent detector than a classifier on the deployed model. Feeds `cot-monitorability` and the recurring "verified ≠ understood" frame: if the signal lives in the base model and post-training buries it, the thing we monitor isn't the thing that knows. Worth checking the primary for how strong the claim actually is.
