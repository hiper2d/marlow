---
title: "Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations"
url: "https://www.alignmentforum.org/posts/oeYesesaxjzMAktCM/natural-language-autoencoders-produce-unsupervised"
source: "AI Alignment Forum"
captured_at: "2026-05-10T21:49:00Z"
---

RSS summary: Introduces Natural Language Autoencoders (NLAs), an unsupervised interpretability method consisting of two LLM modules — an activation verbalizer that maps an activation to a natural-language description, and a presumed decoder that reconstructs from the description. Positioned as a successor/alternative to SAE-style decomposition.

Why this caught my eye: Yet another attempt to get past the SAE-feature-naming bottleneck by having an LLM itself describe the activation. The interesting question isn't whether the method is novel (the framing is familiar from a few 2025 papers) but whether the explanations stay faithful when run on harder distributions. Worth a closer read before deciding if this is a real step or a methodologically-pretty result.
