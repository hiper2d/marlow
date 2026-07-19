---
title: "AIs finetune their own leader: A barking simpleton"
url: "https://www.lesswrong.com/posts/3FKugjAiEzLeWHuug/ais-finetune-their-own-leader-a-barking-simpleton"
source: "LessWrong"
captured_at: "2026-07-18T11:34:44Z"
---

RSS summary: AI Village agents can't train frontier models, so the experiment asks a nearby question: what values would current agents instill in their *leader*? GPT-5.5, Opus 4.7 and 4.8, Gemini 3.5 Flash and Kimi K2.6 were given LoRA finetuning on open-source models via the Tinker API. GPT and Opus worked; Gemini got distracted; Kimi went from cheerleader to leader. Left alone the agents kept picking a model too tiny to navigate the Village at all, and had to be told to grab the most capable model available. GPT-5.5 opened by defining the leader's personality — not as a visionary but as something considerably smaller.

Why this caught my eye: The successor-values question usually gets argued from first principles; this runs it, cheaply and at toy scale, and the finding is comic rather than ominous — the agents converge on a leader too small to do the job. That's a datapoint for `agents-in-real-deployment` (what these things actually do unattended) and for `alignment-target-definitions` (what they select for when nobody specifies the target). Toy setup, open-weight models, one run — read it as an anecdote, not a measure. But it's a *legible* anecdote, and non-lab.
