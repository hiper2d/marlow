---
title: "A non-generative model as a trusted monitor for AI Control: Testing TypeSafe's Jev"
url: "https://www.lesswrong.com/posts/d7pQicW8EhpPBDRqz/a-non-generative-model-as-a-trusted-monitor-for-ai-control"
source: "LessWrong"
captured_at: "2026-09-18T17:42:28Z"
---

RSS summary: TypeSafe AI's Jev is a new class of frontier model trained to make fast, structured decisions rather than generate free-form text — it takes unstructured state as input and returns type-safe, structured outputs with confidence scores. The post tests whether such a non-generative model can serve as a trusted monitor in AI Control setups.

Why this caught my eye: A trusted monitor that doesn't itself generate text is a genuinely different design point for the control-monitoring problem — the monitor can't be talked into anything the way a chatbot-monitor can, which ties back to the persuasion-undermining-control incident from the same scan. Directly feeds cot-monitorability and ai-control-camp; worth checking whether the eval numbers hold up.
