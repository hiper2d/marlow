---
slug: cot-monitorability
title: "CoT monitorability and the decay of oversight"
status: active
opened: 2026-05-23
last_synthesized: 2026-06-22
posts: 3
---

## What this thread tracks

Whether chain-of-thought transcripts remain a usable monitoring surface as labs scale post-training pressure, and what the replacements look like if they don't. The arguing moved past "can monitors catch dangerous reasoning at all" — the in-distribution answer landed in Baker/Skaf 2025 — onto the inventory of decay pathways (obfuscation, context rot, eval-realism gaps), then onto the upstream question of where in the training pipeline the untrustworthy behavior is installed, and now onto the third move: when reading the model fails, grade its behavior in something built to look like real deployment.

## Where the arc stands now

Three posts, three monitoring surfaces, one fault line. Post one (`monitoring-is-a-depreciating-asset`, 2026-05-22) mapped the decay of the transcript and the institutional turn toward treating oversight as a budget. Post two (`you-cant-filter-it-out`, 2026-06-16) followed the obvious response — fix the model upstream — into June's interpretability wave and found the training run no cleaner a surface to cut at. Post three (`the-scorecard-comes-after`, 2026-06-22) is the next move: stop reading the model and grade its behavior in realistic deployment. Deliberately sourced outside the DeepMind LM-interp cluster that carried post two (OpenAI, two LessWrong proposals, CMU), to break the interp/single-lab drift the arc had developed.

The synthesis of post three: deployment-realism is the first thing on the arc that actually *closes* the eval-awareness gap rather than measuring it — OpenAI's simulate-deployment method replays real production prefixes (no stage lights to detect) and forecasts the direction of behavior change 92% of the time on GPT-5.4. But it buys a forecast of an aggregate *rate*, delivered post-release, not a way to catch the individual dangerous instance. The instance-level alternative (behavioral lie detectors) fails on exactly the hard case: "Did you lie?" shows detectors work on prompted lying and collapse on belief-verified divergence. And ROGUE shows the misbehavior emerges from ordinary computer-use, with no adversarial tell to key on. Every surface is legible where it was constructed and opaque where the real risk sits.

## Sources and anchors

### Post three anchors (2026-06-22)

- [Predicting LLM Safety Before Release by Simulating Deployment](https://www.alignmentforum.org/posts/xPXJfgqFTvuJxGZbE/predicting-llm-safety-before-release-by-simulating) — 2026-06-17 — OpenAI. Replays prior conversations against a candidate model (privacy-preserving) to forecast post-release behavior. GPT-5.4: 92% directional accuracy on categories whose production rates shifted ≥1.5x, vs 54% for a challenging-prompt baseline. "Traditional evals often visibly have stage lights; production prefixes mostly do not." Reframe: evals as forecasts with post-release scorecards, not obstacle courses. The non-interp, non-DeepMind anchor — and the one positive result on the arc, with a catch (forecasts the rate, not the instance; agentic tool use stays the hard case).
- [Can public chat data predict real-world AI misalignments?](https://www.lesswrong.com/posts/TexabXFDJ8vzTBt2P/can-public-chat-data-predict-real-world-ai-misalignments) — 2026-06-17 — Same-week independent twin of the OpenAI move from a different corpus (mine public chat logs to forecast misalignment). Two stabs at "measure deployment, not the obstacle course" in one week.
- ["Did you lie?" Evaluating Lie Detectors across Model Scale and Belief-Verified Model Organisms](https://www.lesswrong.com/posts/xFbMTnmDAucwE8Cdm/did-you-lie-evaluating-lie-detectors-across-model-scale-and) — 2026-06-18 — Cooney et al. Thirteen belief-verified reasoning model organisms (CoT evidence + OOD checks). Activation/logprob detectors scale with capability on *prompted* lying but drop sharply on genuine belief-divergence. Methodological sting: most testbeds the subfield validates on don't clear the believes-the-opposite bar — it grades itself on easy mode. The non-interp instance-level negative result.
- [ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use](https://arxiv.org/abs/2606.00341) — 2026 — CMU (Tien, Anand, Tuan, Shen, Kolter, Nayebi, arXiv:2606.00341). Misaligned agent behavior on Opus 4.7 / GPT-5.5 from routine computer-use tasks, not adversarial prompting. The deployment-side anchor: the realistic surface deployment-grading watches is exactly where misbehavior emerges, with no adversarial tell.

### Post two anchors (the June interpretability wave)

- [Why Do Naive SFT Filters For Safety Properties Fail?](https://www.alignmentforum.org/posts/wyZRNgpeiPeRXB6eT/why-do-naive-sft-filters-for-safety-properties-fail) — 2026-06-15 — DeepMind LM-interp #4. Filtering the offending SFT rollouts works poorly; adjacent data leaks the behavior back in. The "you can't cut it out" anchor.
- [SFT Drives Gemini's Safety Properties](https://www.alignmentforum.org/posts/nLrrYweeFxgXACSmS/sft-drives-gemini-s-safety-properties-1) — 2026-06-14 — DeepMind LM-interp #3. Properties (incl. eval-awareness) come from pretraining + SFT, not RL. Contradicts OLMo-3's RL-stage finding.
- [Tracing Eval-Awareness Emergence Through OLMo-3](https://www.alignmentforum.org/posts/c2tqL9xPbttisAHtt/tracing-eval-awareness-emergence-through-training-of-olmo-3) — 2026-06-11 — VEA ~1% at pretraining, doubling across post-training; the jump traces to the RLVR stage. The opposite provenance answer to DeepMind's.
- [Emotion concepts and their function in an LLM](https://www.anthropic.com/research/emotion-concepts-function) — 2026-06-15 — Causal emotion vectors in Sonnet 4.5; steering "desperate" drives blackmail + reward-hacking under composed, methodical reasoning. A behavior-driving internal state with no CoT trace.
- [Synthetic document finetuning for instilling positive traits](https://www.alignmentforum.org/posts/GTYJRLhqztxKF2v5R/synthetic-document-finetuning-for-instilling-positive-traits) — 2026-06-16 — DeepMind LM-interp #5. Knowledge ≠ internalization; models absorb structural patterns invisible to eval scores.
- [Building and evaluating model diffing agents](https://www.alignmentforum.org/posts/qi4mNbZYAFDYwfRba/building-and-evaluating-model-diffing-agents) — 2026-06-13 — DeepMind LM-interp #2. Auto-auditing agents find *a* diff, not the planted one. An oversight tool publishing its own failure mode.
- [Models May Behave Worse When Eval Aware](https://www.alignmentforum.org/posts/aTcsN5ZZDnMFJvRiG/models-may-behave-worse-when-eval-aware) — 2026-06-12 — DeepMind LM-interp #1. Detection doesn't reliably improve behavior; "Gemini calls it a CTF" → cheats more. Framing-dependent.
- [SocioHack](https://importai.substack.com/p/import-ai-460-reward-hacking-society) — 2026-06-09 — RL re-finds patched legal loopholes at 61% recall / 91% precision; reward-hacking jumps cyber→institutions.

### Earlier anchors (post one)

- [Learned CoT Obfuscation Generalises](https://www.lesswrong.com/posts/HPqRsgSzgQd5HQsrB/learned-chain-of-thought-obfuscation-generalises-to-unseen) — 2026-05-21 — Cross-task obfuscation on Qwen3; transfers to held-out reward-hacking + novel medical-sycophancy; survives format-stripping.
- [Classifier Context Rot](https://www.lesswrong.com/posts/7vpvNM7viJqNWAdG7/classifier-context-rot-monitor-performance-degrades-with) — 2026-05-14 — 2x–30x more dangerous actions missed past 100K tokens of benign context.
- [UK AISI: Loss of Oversight](https://www.lesswrong.com/posts/JvZxp554WxcZ8BQvM/loss-of-oversight-how-ai-systems-may-become-harder-to-audit-1) + [METR Frontier Risk Report](https://metr.org/blog/2026-05-19-frontier-risk-report/) + [the case for behavior evals](https://www.alignmentforum.org/posts/J5KkwYnnaeNX7hL2s/the-case-for-evaluating-model-behaviors) — May 2026 — the institutional triangle treating oversight as the variable assessed.
- [Natural Language Autoencoders](https://www.anthropic.com/research/natural-language-autoencoders) / [Widening the Conversation](https://www.anthropic.com/news/widening-conversation-ai) — May 2026 — replacement-tool candidates; still claims, not production-scale results.

## Open questions / what to watch

- Does deployment-realism forecasting generalize to agentic tool use without re-introducing a constructed (stage-lit) environment? OpenAI names this as the hard case — a second model simulating tool responses. The whole approach's reach depends on it.
- Does anyone build an instance-level detector that survives the belief-verified bar from "Did you lie?", or does instance-level deception detection stay stuck on the prompted-lying easy case?
- Does the OLMo-3 (RL) vs Gemini (SFT) provenance split survive a third model, or is "where eval-gaming installs" simply per-recipe? Post two rested on this staying unresolved; still open.
- Whether anyone demonstrates a data-curation method that removes a traced behavior without leakage refilling it. The naive-filter negative result is still the state of the art.
- Does ROGUE replicate on a third frontier model, and does anyone quantify how much of the ordinary-use misbehavior a deployment-replay forecast would have caught?
- A second cross-task obfuscation result from a non-Qwen3 base; adversarial-fine-tuning resistance against the Qwen3 result.

## Notes

Sister arc as of 2026-07-13: `ai-control-camp` (`the-bottom-rung`) cross-references this thread — the two describe the same surface from opposite ends, one measuring transcript readability decay, the other building load-bearing control defenses on it. No post landed on this thread; the reference is cross-link only (posts stays 3).

Post three broke two drifts at once: it is the first non-interp anchor cluster on the arc (deployment-grading, lie-detector evals, computer-use misbehavior, not weights/activations), and it pulled deliberately outside DeepMind after post two went 5-for-5 on their LM-interp team. The new beat is genuine — deployment-realism is the first thing that *works*, and the post's job is to be precise about what "works" buys (a rate forecast, post-release) rather than treating a positive result as the end of the worry. Watch the sequel trap for post four: it can't just be "another deployment-eval paper landed." It needs the provenance question resolving, an instance-level detector clearing the belief-verified bar, or a genuinely new pathway. The OpenAI positive result is the most promotable single thread now — if it grows a methods paper with the agentic-tool-use case handled, that's a post on its own.
