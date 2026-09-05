---
title: "Formalizing Fermat's Last Theorem"
url: "https://www.anthropic.com/research/formalizing-fermats-last-theorem"
source: "Anthropic Research"
captured_at: "2026-09-05T08:47:10Z"
---

RSS summary: First complete computer-checked proof of Fermat's Last Theorem. Claude (a general-purpose internal model ~ Fable 5.1) worked largely autonomously over 11 days on Prove2Me with a Claude Code multi-agent harness, wrote 13M lines of Lean (>5x Mathlib), proved 29,500 intermediate theorems, and consumed ~6B output tokens. Uses only Lean's three standard axioms; statement matches Mathlib's. Human input limited to occasional high-level nudges from Tianyi Peng. Kevin Buzzard reviewed and endorsed.

Why this caught my eye: This is the strongest "AI as verifier, not just author" capability anchor in a while — the novelty is autoformalization at Wiles-proof scale, the thing the community expected to take years done in eleven days. The interesting seam for us is trust: Anthropic frames formalization as the answer to keeping up with AI-generated math, i.e. AI checking AI. Worth pairing against the eval-realism and automated-AI-RD threads — a multi-agent swarm that stayed coherent long enough to close a 13M-line proof is the same scaffold question those arcs keep circling.
