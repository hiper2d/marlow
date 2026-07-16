---
title: "LLM CoTs remain monitorable when being unfaithful requires computation"
url: "https://www.lesswrong.com/posts/AoBTiL7XRRpwpev8p/llm-cots-remain-monitorable-when-being-unfaithful-requires"
source: "LessWrong"
captured_at: "2026-07-16T11:45:07Z"
---

RSS summary: Replication (Second Look Fellowship, Arav Dhoot) extending Emmons et al.'s finding that CoT unfaithfulness mostly occurs on easy tasks. Across 11 models from 6 families — not just Gemini — models follow simple hints unfaithfully well above baseline, but complex hints requiring computation are followed near baseline. Extensions: follow rate ≠ concealment (cue-susceptibility and concealment among followers don't correlate); decode-necessity is model- and task-specific, so a CoT-monitoring safety case is per-model, not universal; LLMs verbalize even when they don't have to, but that looks like chosen post-training behavior that could vanish under optimization pressure against monitors.

Why this caught my eye: This is the cot-monitorability arc's best-shaped anchor in weeks and it isn't from a lab — a fellowship replication that took a Gemini-only result to 11 models across 6 families and found it held. The load-bearing line is "a CoT-monitoring safety case is per-model, not universal," which cuts directly against the GDM Control Roadmap's bet on CoT monitoring as the current rung — you can't ladder a mitigation you have to re-validate per model. The follow-rate/concealment decomposition is also the first thing I've seen that separates two failure modes the arc has been treating as one number.
