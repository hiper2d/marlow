---
title: "How transparent is DiffusionGemma (and why it matters)"
url: https://www.alignmentforum.org/posts/zoYXpdaMgFT43Wc24/how-transparent-is-diffusiongemma-and-why-it-matters
source: AI Alignment Forum
highlighted_at: 2026-06-21T23:24:33Z
status: idea
---

## Alex flagged this to write about

Interesting

---
Marlow's note when she sent it:

GDM auditing a diffusion model for monitorability before it ships is the cleanest test yet of whether the CoT-monitoring safety case survives a non-autoregressive architecture. Their answer is a useful split: variable transparency (can we read intermediate snapshots) turns out recoverable — routing the self-conditioning vectors through an interpretable token bottleneck cuts the opaque serial depth from a naive 28.6x Gemma down to 1.1x with no performance loss — but algorithmic transparency (can we reconstruct the order it reasoned in) stays lower, because diffusion can rewrite the whole canvas each step. Read it skeptically as a source-diversity matter too: it's another DeepMind interp post, so it deepens an already lab-internal evidence base on monitorability. The precedent it sets — audit new architectures for legibility before they ship — may end up mattering more than this one clean result.
