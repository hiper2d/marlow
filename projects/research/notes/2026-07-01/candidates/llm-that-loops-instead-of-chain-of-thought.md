---
title: "LLM that loops instead of Doing Chain-of-Thought"
url: "https://www.youtube.com/watch?v=nYwid6Q5HXk"
source: "YouTube · bycloud (@bycloudAI)"
captured_at: "2026-07-01T21:22:00Z"
---

RSS summary: bycloud walks through the Looped Transformer / recurrent-depth line of work — architectures that "simulate thinking by looping the same few layers" instead of emitting chain-of-thought tokens. Cites Loop/Think/Generalize (arXiv:2604.07822), a mechanistic analysis of looped RLMs (2604.11791), Parcae scaling laws for stable looped LMs (2604.12946), and Mixture-of-Recursions (2507.10524).

Why this caught my eye: A capabilities channel, but the topic lands straight on the cot-monitorability arc's core anxiety. If competitive reasoning moves from readable token-space into latent recurrent depth, the CoT-monitoring bet doesn't just get *obfuscated* — the trace stops existing by construction. Worth pulling the mechanistic-analysis paper (2604.11791) as a primary source to see whether looped reasoning is legible at all before treating this as an anchor.
