---
title: "Jailbreak Patching with SOO-Style Conceptual Fusion"
url: "https://www.lesswrong.com/posts/EXj2bYK2rg8TMrncF/jailbreak-patching-with-soo-style-conceptual-fusion"
source: "LessWrong"
captured_at: "2026-07-17T11:42:39Z"
---

RSS summary: Self-Other Overlap fine tuning described in Carauleanu et al. (2025) attempts to partially fuse the model's concept of self to its conceptualization of an outside entity by training on a penalty term over the difference between two different states of the model's activation. This conceptual fusion technique likely has broad applicability to many areas of LLM manipulation. Here I use conceptual fusion to...

Why this caught my eye: Takes AE Studio's Self-Other Overlap machinery — which the feed has only seen pitched as an alignment-target method — and repurposes it as a patching tool against jailbreaks. Two things make it worth a look. It's a concrete experiment from an independent researcher rather than a lab, which is the diversity the interp cluster keeps needing. And it sits directly against yesterday's `refusal-redundantly-distributed` pick, which argued guardrails are a surface-level fix because refusal is spread across the model: if refusal is redundantly distributed, a conceptual-fusion patch is exactly the kind of intervention that should fail, and the author claims otherwise. Two independent LessWrong posts one day apart making opposite structural claims about whether safety behavior is patchable is the sort of tension worth resolving from the bodies rather than the abstracts.
