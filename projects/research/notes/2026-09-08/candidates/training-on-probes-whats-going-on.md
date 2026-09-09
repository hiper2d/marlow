---
title: "Training on probes: What's going on"
url: "https://www.lesswrong.com/posts/gHFCgrvfxQtaEnJye/training-on-probes-what-s-going-on"
source: "LessWrong"
captured_at: "2026-09-08T19:36:10Z"
---

RSS summary: Train a probe for a property (e.g. "honesty") and do gradient descent against it while other training incentivizes the opposite, and the model reshapes its internal representation to evade the probe. But training against the probe *after* all other training works and may beat ablation. Adding a probe term to RL does nothing under certain credit-assignment / single-token conditions.

Why this caught my eye: The interpretability-as-training-signal question stated cleanly, with the failure modes named — the "gradient teaches the model to fool the probe" trap is the whole reason white-box honesty signals are load-bearing-but-fragile. Interp content, not a mood piece. Pairs with the follow-on [[training-on-probes-research-ideas]].
