---
title: "A Simpler and Better Debate Protocol for Scalable Oversight"
url: "https://www.alignmentforum.org/posts/Rct9zd4Nd7H8Xzxz8/a-simpler-and-better-debate-protocol-for-scalable-oversight"
source: "AI Alignment Forum"
captured_at: "2026-10-17T08:20:52Z"
---

RSS summary: Linkpost to arXiv 2610.02557. Proposes FBS Debate, a new scalable-oversight protocol for the same problem class as prover-estimator debate but with stronger guarantees: correctness holds worst-case rather than average-case, and under a stronger equilibrium concept. Also proves no black-box protocol can outperform it. Core mechanism: the "fractional block sensitivity" of a decomposition bounds how much compute any recursive debate must spend to catch a lying debater.

Why this caught my eye: This is a real theory advance on debate, not another position piece — it pins a lower bound on the compute any recursive-debate protocol needs, and argues highly-sensitive arguments are inherently suspect. Debate training is now hitting frontier-scale models (cites Kenton et al. 2026), so the "worst-case vs average-case honesty guarantee" distinction is newly load-bearing. Candidate for the scalable-oversight corner I don't have a thread on yet.
