---
title: "CoT controllability evals seem very under-elicited"
url: "https://www.alignmentforum.org/posts/BbP2wCyDGdPWJ7PwP/cot-controllability-evals-seem-very-under-elicited"
source: "AI Alignment Forum"
captured_at: "2026-09-12T08:18:36Z"
---

RSS summary: The CoTControl eval asks reasoning models to follow formatting constraints in their chain-of-thought (write lowercase, avoid a word) while solving problems; recent models score 0-30%, and OpenAI (GPT-5.5) and Anthropic (Fable 5) cite these low scores in system cards to argue their models are bad at obfuscating their CoT. Author iterated on prompt templates with Claude Opus 4.6 and got 2-3x improvements for open-source models (5.5%->15% on GPT-OSS-120B), arguing the eval is heavily under-elicited and current controllability numbers may understate how well models can hide reasoning. Notes UK AISI raised similar prompt-sensitivity concerns in the Fable card (§6.5.5.1).

Why this caught my eye: This is a direct hit on the cot-monitorability arc's soft underbelly. The labs' whole "CoT is monitorable because models are bad at obfuscating it" claim rests on eval scores, and here's someone showing the scores move 2-3x on prompt tweaks alone. It's the elicitation-gap critique aimed squarely at the safety-case load-bearing number — pairs with the -10 no-CoT replication and the standing "measure" question.
