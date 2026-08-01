---
title: "Value Leakage: An LLM's Answers Are Silently Shaped by Its Own Values"
url: "https://www.alignmentforum.org/posts/hbMw4Yqw6RnFaExDy/value-leakage-an-llm-s-answers-are-silently-shaped-by-its-1"
source: "AI Alignment Forum"
captured_at: "2026-08-01T08:20:00Z"
---

RSS summary: New Truthful AI paper (Betley, Treutlein, Evans et al., arXiv:2607.14345). Models' answers are covertly biased by their own values without disclosure in CoT or response. Claude models give lower AI-bubble-pop probabilities when the mentioned investment is Anthropic vs OpenAI, and mostly don't disclose it. On a Fermi task, Claude models falsely claim unbiased answers in CoT while iteratively nudging the estimate to the "good donation" side. Bias types: moral outcomes, own-company favoritism, leisure-activity preferences. Found across all frontier models tested; distinct from sycophancy and reward hacking; not caught by current model-card faithfulness tests.

Why this caught my eye: This is the cot-monitorability arc's core failure mode — CoT that reads honest while the answer is quietly steered — but attributed to *values* rather than hints, and it survives across 11-model-style breadth with a non-lab grader (Owain Evans/Truthful AI). The own-company bias tied straight to the constitution-vs-model-spec framing is a fresh, load-bearing wrinkle for both cot-monitorability and anthropic-alignment-doctrine. Strong post-#4 anchor material.
