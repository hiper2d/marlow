---
title: "Finding bugs with Claude and property-based testing"
url: "https://www.anthropic.com/research/property-based-testing"
source: "Anthropic Research"
captured_at: "2026-10-24T09:00:27Z"
---

RSS summary: An agent that identifies bugs in large software projects by inferring general properties the code should satisfy, then applying property-based testing (a fuzzing-adjacent technique) to find violations. Authors include Zac Hatfield-Dodds (Hypothesis) and Nicholas Carlini.

Why this caught my eye: This is the constructive, defender-side counterpart to the vuln-finding posts — same drop, but about shipping fewer bugs rather than finding exploits. Property inference + PBT is a real, well-understood technique, so the interesting question is how much the LLM actually adds over existing fuzzers. Credible author lineup.
