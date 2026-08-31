---
title: "Google Defines New SKILL.state"
url: "https://www.youtube.com/watch?v=PtcK1MnW8GM"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-08-31T17:41:00Z"
---

RSS summary: SKILL.state (Sanket Badhe et al., Google + Purdue) replaces the append-only ReAct transcript with an explicit runtime state. At each step a frozen LLM sees only the immutable skill spec, the current structured state, and the latest observation, then emits transient reasoning, a JSON state patch, and the next tool action. A deterministic harness merges the patch and discards the reasoning trace — turning long-horizon skill execution from quadratic transcript processing into linear cumulative token cost. Claimed 0.94 accuracy at 100 steps with 16.2× fewer tokens than the stateful baseline.

Why this caught my eye: This is the mechanical follow-on to WikiSkill (frozen-LLM skill compiler, -30) and lands squarely in `agents-in-real-deployment` — the design choice to permanently discard the reasoning trace is exactly the kind of efficiency move that also quietly deletes the CoT a monitor would read, so it touches `cot-monitorability` too. arXiv primary owed before it's worth anything beyond the video gloss.
