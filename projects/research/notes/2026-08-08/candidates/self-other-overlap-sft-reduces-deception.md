---
title: "Inducing self-other overlap with SFT reduces deception at scale, but generalization remains uneven"
url: "https://www.lesswrong.com/posts/qLe7T2njnpGYt5D7a/inducing-self-other-overlap-with-sft-reduces-deception-at-2"
source: "LessWrong"
captured_at: "2026-08-08T19:29:49Z"
---

RSS summary: Overlap Research (BlueDot-supported) tested whether LLM deception can be cut by inducing self-other overlap via ordinary supervised fine-tuning (SOO SFT) rather than a custom activation-matching loss. Run across Qwen2.5-14B/32B-Instruct, Gemma-3-27B-It, and Gemini 2-class models; deception drops at scale but generalization stays uneven.

Why this caught my eye: A non-lab replication of an alignment technique across four model families with an honest "generalization remains uneven" caveat — the same it-holds-in-direction-but-is-model-dependent shape as the cot-monitorability replications I've been tracking. The uneven-generalization result is the interesting part, not the headline reduction.
