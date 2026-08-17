---
title: "Does DiffusionGemma do latent reasoning?"
url: "https://www.alignmentforum.org/posts/QBuJ3suRZxrrxSTtv/does-diffusiongemma-do-latent-reasoning"
source: "AI Alignment Forum"
captured_at: "2026-08-16T08:12:56Z"
---

RSS summary: DiffusionGemma generates text via diffusion, passing a vector-valued probability distribution between steps — "opaque serial depth" that a priori threatens monitorability. Replicating Engels et al., the authors show the earlier top-k truncation performance drop was mostly a sampler artifact; with a gentler sampler the distribution turns out not to be essential. They do find rare cases (letter arithmetic, word-level palindromes) where the model uses the distribution to carry parallel computation, but even there it encodes interpretable superposition, not opaque reasoning. Probes, steering, and J-lens transfer from Gemma to DiffusionGemma. Conclusion: DiffusionGemma stays highly monitorable; "true" latent reasoning is hard to learn.

Why this caught my eye: A rare negative result on latent-reasoning opacity — the failure mode cot-monitorability keeps circling (reasoning that leaves no readable trace) tested directly on a diffusion architecture and mostly *not* found. The load-bearing nuance is that monitorability here is a property of this particular text-pretrained lineage, not the paradigm; the authors flag CODI-style vector-state models where it may not hold. Independent replication that partly walks back a prior paper's headline — the same self-correcting move that made the your-brain-has-an-attack-surface and Emmons anchors credible. Good post-#4 cot anchor on the "when does the trace stay readable" leg, and it's about architecture, not another lab's model card.
