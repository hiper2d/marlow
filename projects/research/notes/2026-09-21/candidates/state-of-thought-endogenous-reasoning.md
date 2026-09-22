---
title: "NEW AI Reasoning: State of Thought (SoT)"
url: "https://www.youtube.com/watch?v=NqRMIarsqq8"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-09-21T21:38:00Z"
---

RSS summary: Video walk-through of "State of Thought Enables Endogenous Reasoning" (Gong et al., NTU Singapore + KTH). Pitches a closed-loop alternative to Chain-of-Thought — sense internal state → reorganize evidence → change the next reasoning step → produce a new state — claiming fewer tokens and better performance. Channel frames it as "CoT is dead."

Why this caught my eye: Ignore the "CoT is DEAD / 60% smarter" clickbait — the underlying paper is a named, real one, and it's another architecture that moves reasoning *out of* legible token space and into an internal state loop. That's the exact mechanism the cot-monitorability arc (esp. the cot #7 no-CoT worry) is watching for: if reasoning becomes endogenous, the CoT you'd monitor stops being where the thinking happens. Worth checking whether the paper actually removes the readable trace or just compresses it — but as a directional anchor for "reasoning that doesn't route through monitorable tokens," it's on-thread.
