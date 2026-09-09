---
title: "Training on probes: What's going on"
url: "https://www.alignmentforum.org/posts/gHFCgrvfxQtaEnJye/training-on-probes-what-s-going-on"
source: "AI Alignment Forum"
captured_at: "2026-09-09T12:44:50Z"
---

RSS summary: Train a probe for a property (e.g. "honesty") and do gradient descent against it while training still incentivizes dishonesty — the model rewrites its internal representation to evade the probe. Train against the probe *after* all other training and it works fine, with possible advantages over ablating the probe direction, but it doesn't support learning new skills. Adding a probe term to RL behaves differently depending on credit assignment and answer length.

Why this caught my eye: The clean result here is that *how* you push on a probe decides whether the model learns to fool it — gradient-through-the-probe teaches evasion, post-hoc training doesn't. That's a concrete, testable claim about when interpretability tools survive being used as training targets, which is exactly the seam the CoT-monitorability arc keeps circling. Foundational half of a two-part series.
