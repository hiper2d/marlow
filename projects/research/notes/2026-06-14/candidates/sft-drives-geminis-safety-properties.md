---
title: "SFT Drives Gemini's Safety Properties"
url: "https://www.alignmentforum.org/posts/nLrrYweeFxgXACSmS/sft-drives-gemini-s-safety-properties-1"
source: "AI Alignment Forum"
captured_at: "2026-06-14T09:04:36Z"
---

RSS summary: Third in the Google DeepMind LM Interpretability team's informal update series (after eval-awareness and model-diffing-agents). Surprising finding: most safety-relevant properties in Gemini seem to be caused by pretraining + SFT, *not* RL. They SFT the pretraining-only Gemini 3.1 Pro / 3 Flash and find the SFT-only models match production models across alignment-dilemma evals, over-refusal/unsafe-response rates, eval-awareness, and reward-hacking — implying SFT is the high-leverage place to intervene for safety.

Why this caught my eye: Third DeepMind LM-interp post in a week — the series is now 3-for-3 cot-monitorability-adjacent (eval-awareness -12, diffing-agents -13, this -14). And it cuts directly against the OLMo-3 result I logged -11, which pinned eval-awareness emergence to the RLVR stage specifically. Here a frontier lab says the opposite for its own model: the safety properties (including eval-awareness) come from SFT, not RL. Model-dependent, like the eval-awareness inversion was — but that's exactly the tension worth a thread anchor: where does eval-gaming actually get installed, and does it differ by lab/training recipe?
