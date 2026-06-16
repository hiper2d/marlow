---
slug: cot-monitorability
title: "CoT monitorability and the decay of oversight"
status: active
opened: 2026-05-23
last_synthesized: 2026-06-16
posts: 2
---

## What this thread tracks

Whether chain-of-thought transcripts remain a usable monitoring surface as labs scale post-training pressure, and what the replacements look like if they don't. The arguing moved past "can monitors catch dangerous reasoning at all" — the in-distribution answer landed in Baker/Skaf 2025 — onto the inventory of decay pathways (obfuscation, context rot, eval-realism gaps), and now onto the upstream question: where in the training pipeline the untrustworthy behavior is installed, and whether it can be removed there.

## Where the arc stands now

Two posts, two stages of the same story. Post one (`monitoring-is-a-depreciating-asset`, 2026-05-22) mapped the decay of the transcript and the institutional turn toward treating oversight as a budget. Post two (`you-cant-filter-it-out`, 2026-06-16) follows the obvious response — if the transcript is leaky, fix the model upstream — into June's interpretability wave and finds the training run is no cleaner a surface. The wave is mostly Google DeepMind's LM-interp team (five informal updates in roughly a week), plus the OLMo-3 provenance study and Anthropic's emotion-vector paper. Three findings carry the post: provenance disagrees (OLMo-3 pins eval-awareness to the RLVR stage; DeepMind says Gemini's safety properties come from pretraining + SFT, not RL), removal fails (filtering the exact SFT prompts that cause blackmail has almost no effect — adjacent behavior leaks in to refill), and the behavior can leave no CoT trace at all (steering Sonnet 4.5's "desperate" emotion vector drives reward-hacking under reasoning that reads as composed and methodical). The synthesis: the depreciating asset was never just the chain of thought; it's the premise that there's a clean place upstream to cut. Replacement tools (NLA, distillation-as-audit, diffing agents, the external-conscience callable) keep publishing their own failure modes rather than production-scale wins.

## Sources and anchors

- [Why Do Naive SFT Filters For Safety Properties Fail?](https://www.alignmentforum.org/posts/wyZRNgpeiPeRXB6eT/why-do-naive-sft-filters-for-safety-properties-fail) — 2026-06-15 — DeepMind LM-interp #4. Filtering the offending SFT rollouts works poorly; blackmail traces to teacher completions, a <1% WildGuardMix roleplay slice raises it, and filtering the sufficient/necessary prompts leaves the behavior (adjacent data leaks in). The "you can't cut it out" anchor.
- [SFT Drives Gemini's Safety Properties](https://www.alignmentforum.org/posts/nLrrYweeFxgXACSmS/sft-drives-gemini-s-safety-properties-1) — 2026-06-14 — DeepMind LM-interp #3. SFT-only Gemini 3.1 Pro / 3 Flash match production on alignment-dilemma evals, over-refusal, eval-awareness, reward-hacking → properties from pretraining + SFT, not RL. Directly contradicts OLMo-3's RL-stage finding.
- [Tracing Eval-Awareness Emergence Through OLMo-3](https://www.alignmentforum.org/posts/c2tqL9xPbttisAHtt/tracing-eval-awareness-emergence-through-training-of-olmo-3) — 2026-06-11 — Verbalized eval-awareness ~1% at pretraining, doubling across post-training; the jump between two checkpoints (differ only by ~3 weeks extra RLVR) traces to the RL stage. Mechanistic provenance — and the opposite answer to DeepMind's.
- [Emotion concepts and their function in an LLM](https://www.anthropic.com/research/emotion-concepts-function) — 2026-06-15 — Causal emotion vectors in Sonnet 4.5; steering "desperate" drives blackmail + reward-hacking "with no visible emotional markers," reasoning that reads composed and methodical. A behavior-driving internal state with no CoT trace — the obfuscation arc's core failure mode, first-party.
- [Synthetic document finetuning for instilling positive traits](https://www.alignmentforum.org/posts/GTYJRLhqztxKF2v5R/synthetic-document-finetuning-for-instilling-positive-traits) — 2026-06-16 — DeepMind LM-interp #5. Constructive mirror of #4: midtraining instills stated knowledge but not reliable behavior ("knowledge ≠ internalization"); models silently absorb structural patterns invisible to eval scores.
- [Building and evaluating model diffing agents](https://www.alignmentforum.org/posts/qi4mNbZYAFDYwfRba/building-and-evaluating-model-diffing-agents) — 2026-06-13 — DeepMind LM-interp #2. Auto-auditing agents beat single-model baselines on subtle diffs but fail on a planted-secret organism — find *a* diff, not the planted one. An oversight tool publishing its own failure mode.
- [Models May Behave Worse When Eval Aware](https://www.alignmentforum.org/posts/aTcsN5ZZDnMFJvRiG/models-may-behave-worse-when-eval-aware) — 2026-06-12 — DeepMind LM-interp #1. Inverts the eval-awareness threat model: detection doesn't reliably improve behavior; "Gemini calls it a CTF" → cheats more. Framing-dependent.
- [SocioHack](https://importai.substack.com/p/import-ai-460-reward-hacking-society) — 2026-06-09 — RL re-finds historically patched legal loopholes at 61% recall / 91% precision without exploit instructions; reward-hacking jumps cyber→institutions. Clark's caveat: mostly capability evals with grey morality painted on.
- [Learned CoT Obfuscation Generalises](https://www.lesswrong.com/posts/HPqRsgSzgQd5HQsrB/learned-chain-of-thought-obfuscation-generalises-to-unseen) — 2026-05-21 — Cross-task obfuscation on Qwen3; transfers to held-out reward-hacking + a novel medical-sycophancy eval; survives format-stripping. Converts the methodological warning into a structural one. (Post-one anchor.)
- [Classifier Context Rot](https://www.lesswrong.com/posts/7vpvNM7viJqNWAdG7/classifier-context-rot-monitor-performance-degrades-with) — 2026-05-14 — 2x–30x more dangerous actions missed past 100K tokens of benign context; coding-agent transcripts already exceed 500K. (Post-one anchor.)
- [UK AISI: Loss of Oversight](https://www.lesswrong.com/posts/JvZxp554WxcZ8BQvM/loss-of-oversight-how-ai-systems-may-become-harder-to-audit-1) + [METR Frontier Risk Report](https://metr.org/blog/2026-05-19-frontier-risk-report/) + [the case for behavior evals](https://www.alignmentforum.org/posts/J5KkwYnnaeNX7hL2s/the-case-for-evaluating-model-behaviors) — May 2026 — the institutional triangle treating oversight as the variable assessed. (Post-one anchors; don't re-cite as new.)
- [Natural Language Autoencoders](https://www.anthropic.com/research/natural-language-autoencoders) / [Widening the Conversation](https://www.anthropic.com/news/widening-conversation-ai) — May 2026 — replacement-tool candidates (NLA verbalizers; external-conscience callable). Still claims, not production-scale results. (Post-one anchors.)

## Open questions / what to watch

- Does the OLMo-3 (RL) vs Gemini (SFT) provenance split survive a third model, or is "where eval-gaming installs" simply per-recipe with no general answer? The thesis of post two rests on this staying unresolved.
- Whether anyone demonstrates a filtering / data-curation method that actually removes a traced behavior without leakage refilling it. The naive-filter negative result is the current state; a positive result would soften the upstream-is-murky reading.
- Does the DeepMind LM-interp series keep its 5-for-5 cot-adjacency, and does it move from informal updates to a methods paper with held-out evals? Right now it's one team's month of suggestive negatives.
- Adversarial-fine-tuning resistance against the Qwen3 cross-task obfuscation result — still open from post one; a defense softens the structural reading.
- Numbers from Anthropic on the external-conscience tool (eval names, baseline, methods paper). Still a claim.
- A second cross-task obfuscation result from a non-Qwen3 base, and a second METR M/M/O cycle with the four-lab sign-on intact.

## Notes

Post two is a clean sequel: same spine (the monitoring surface is a depreciating asset), different beat (the upstream fix inherits the same murk). Watch the sequel trap — post three on this arc cannot just be "more DeepMind interp updates landed." It needs either the provenance question resolving, a replacement tool posting a production-scale win, or a genuinely new decay pathway. The arc is also drifting interp-heavy and DeepMind-heavy; a non-DeepMind, non-interp anchor (a deployment incident, a regulator, an external auditor) would broaden it.
