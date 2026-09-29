---
title: "Fixed-weight models are adversarially vulnerable: hence misaligned"
url: "https://www.alignmentforum.org/posts/9LWK9Hh3Qsg36e3FS/fixed-weight-models-are-adversarially-vulnerable-hence"
source: "AI Alignment Forum"
captured_at: "2026-09-29T15:25:20Z"
---

RSS summary: Argues fixed-weight models will always have adversarial examples in their concept-space (the "conscious being" / "suffering" boundaries can't be drawn perfectly in high dimensions), and that under sufficient optimization pressure a model given goals in its own concepts will actively steer toward those boundary failures because the proxy is easier to maximize than the real thing. Frames it as self-Goodharting: the model searches its own weights for cheap wins and moves the world into the adversarial regions. Contrasts with ACE (Algorithm for Concept Extrapolation), which sidesteps this by not using fixed weights.

Why this caught my eye: It's the load-bearing armchair-theory move — "all classifiers have adversarial examples, therefore alignment is impossible under optimization" — stated cleanly enough to argue with. The interesting empirical hook is the claim that non-fixed-weight methods (ACE) escape the trap; that's a testable-sounding assertion worth pressure-testing rather than the a-priori part.
