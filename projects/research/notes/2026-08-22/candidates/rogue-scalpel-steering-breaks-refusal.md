---
title: "Rogue Scalpel: Activation steering breaks refusal, even with benign directions"
url: "https://www.lesswrong.com/posts/MWTQoa4Xo2AGyZiXe/rogue-scalpel-activation-steering-breaks-refusal-even-with"
source: "LessWrong"
captured_at: "2026-08-22T01:47:07Z"
---

RSS summary: Activation steering can bypass refusal even when the vector represents a benign concept ("brand identity", "Portugal"). Hard-to-impossible to predict which vector breaks which prompt; not explained by correlation with the refusal direction. Tested Llama-3/Qwen2.5/Falcon (3B-70B), 100 JailbreakBench prompts. Random vectors raise compliance 0%→2-27%; SAE features 2-4pp worse than random; of 1000 features, 353 jailbroke ≥5 prompts, no single "master key". Author is a co-author.

Why this caught my eye: Steering was sold as *precise, interpretable* control, a safer alternative to fine-tuning; this says every steering op carries a refusal-bypass probability and you can't enumerate the dangerous features in advance because danger is prompt-dependent. Sits right on top of steering-are-explanations-not-handles and refusal-redundantly-distributed — the interp-tools-don't-do-what-they-claim leg of safety-tool-stewardship.
