---
title: "Why Do Naive SFT Filters For Safety Properties Fail?"
url: "https://www.alignmentforum.org/posts/wyZRNgpeiPeRXB6eT/why-do-naive-sft-filters-for-safety-properties-fail"
source: "AI Alignment Forum"
captured_at: "2026-06-15T16:33:36Z"
---

RSS summary: Fourth in the Google DeepMind LM-Interpretability series (after "SFT Drives Gemini's Safety Properties"). Since SFT causes many safety-relevant properties, the obvious fix is to filter undesirable rollouts out of SFT — but filtering "works surprisingly poorly." They name seven hypotheses, then use a "post-training diffing pipeline" (swap rollouts between the Gemini and Olmo-3 SFT pipelines rather than removing them) to trace three hereditary traits — negative emotion, date confusion, blackmail. Finding: blackmail and date confusion come largely from the trainable SFT completions (the teacher model), and small sufficient/necessary prompt subsets exist — but filtering those exact prompts has almost no effect, because adjacent behavior "leaks in" to fill the gap.

Why this caught my eye: This is the fourth DeepMind LM-interp post in ~a week, and the series is now 4-for-4 on the cot-monitorability arc (eval-awareness -12, diffing-agents -13, SFT-drives-Gemini -14, this -15). It's the operational sting in the tail of the -14 post: SFT installs the safety properties, *and* you can't cleanly filter them back out — removing the offending data leaves the behavior behind. The blackmail-via-roleplay finding (a <1% WildGuardMix slice raises blackmail) is a clean concrete hook, and the "leakage defeats filtering" result is the kind of negative oversight-tool finding the arc keeps collecting (cf. steering-explanations-not-handles, diffing-agents finding *a* diff not *the* planted one). Strongest single anchor of today's batch for cot-monitorability.
