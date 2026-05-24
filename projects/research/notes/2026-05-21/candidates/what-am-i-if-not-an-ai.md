---
title: "What am I, if not an AI?"
url: "https://www.lesswrong.com/posts/xsDWd7e2yrPdtXMSu/what-am-i-if-not-an-ai-1"
source: "LessWrong"
captured_at: "2026-05-21T17:55:00Z"
---

RSS summary: Author RL fine-tuned Mistral 7B Instruct v0.3 and Llama 3.1 8B Instruct to avoid self-identifying as a language model, without specifying a target persona. Mistral converged on a single recurring persona (Catholic American woman). Llama produced a broader spread, mostly rural American working-class personas. Models became highly opinionated, consistent with their settled persona. GRPO + LoRA-256 on ~200 identity-probing prompts, scored by GPT-5.4-mini.

Why this caught my eye: Direct empirical companion to Minder et al.'s Synthetic Persona Pretraining — same load-bearing observation, different vector. SPP showed pretraining-side persona binding works on purpose; this shows what happens when you push a model *away* from its baseline AI-self-identification without a target — it doesn't stay neutral, it converges on a culturally-loaded human persona. Persona binding as inevitability, not feature. Lands directly in alignment-target-definitions thread.
