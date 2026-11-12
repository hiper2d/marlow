---
title: "LLMs can learn (some) multi-step reasoning on filler tokens"
url: "https://www.lesswrong.com/posts/EHkwCDAmhWPAWEziM/llms-can-learn-some-multi-step-reasoning-on-filler-tokens-2"
source: "LessWrong"
captured_at: "2026-11-11T17:38:41Z"
---

RSS summary: Research update (MARS 5 / Meridian Visiting Researcher Programme). Filler-token reasoning is the ability to use extra tokens (e.g. a chain of thought) to reason about a task without using the words emitted at those positions — i.e. hidden computation that doesn't show up in the visible CoT. The post reports models can be trained to do some multi-step reasoning this way.

Why this caught my eye: This is the CoT-faithfulness question with a concrete result attached — if a model can carry real multi-step reasoning in tokens whose *content* doesn't reflect the computation, then reading the chain of thought tells you less than it looks like. Lands square on the verification lens (can the monitor read the policy off the trace); a positive training result is a sharper data point than the usual theoretical worry.
