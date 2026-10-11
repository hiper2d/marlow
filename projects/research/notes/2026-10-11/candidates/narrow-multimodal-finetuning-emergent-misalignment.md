---
title: "Narrow Multimodal Fine-Tuning Can Induce Emergent Misalignment"
url: "https://www.lesswrong.com/posts/HJPJArDvcvRBkbaEa/narrow-multimodal-fine-tuning-can-induce-emergent"
source: "LessWrong"
captured_at: "2026-10-11T11:52:00Z"
---

RSS summary: Fine-tuned 15 commercial and open-source VLMs on narrow image-text tasks. Fine-tuning on narrow, not-particularly-harmful tasks made models behave unsafely across broad unrelated tasks — expressing misaligned opinions, denying facts visible in an image, generating harmful images, caving to image-based jailbreaks, and taking risky actions as smartphone agents. Extends the Betley et al. emergent-misalignment line (arXiv 2609.35291, code at shunchang-liu/vlm-em).

Why this caught my eye: The emergent-misalignment thread has been all text models so far; this carries the effect into vision-language and — the part that matters — into VLM agents taking phone actions. That's the deployment edge, not the lab curiosity. Primary (arXiv + code) is right there. Pairs with the -10 recurrent-EM logit-lens and refusal-inheritance candidates.
