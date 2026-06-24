---
title: "LLM-Driven Feature Discovery"
url: "https://www.alignmentforum.org/posts/WAZWA6FPQvH8okouJ/llm-driven-feature-discovery"
source: "AI Alignment Forum"
captured_at: "2026-06-23T14:02:51Z"
---

RSS summary: Exploratory method for getting a qualitative sense of a model's behaviors without touching internals. Split transcripts into user/thoughts/response, ask a black-box LLM autorater to generate 10-20 "features" per piece, embed, cluster, and name clusters. Authors call it a "black box SAE." On 100k Gemini chat transcripts they find many interesting high-level thought features — token-count awareness, considering whether a scenario is reality or roleplay, infinite loops, evaluation-awareness — but logistic-regression probes mostly cannot predict thought/response features from user features. Preliminary; authors aren't pursuing it further.

Why this caught my eye: A monitorability method that reads the transcript instead of the activations — and it surfaces the exact thought-features the cot-monitorability arc keeps circling (eval-awareness, reality-vs-roleplay framing). The honest negative — they can't predict the interesting behaviors from the user turn — is the more useful half. Candidate post-#4 anchor; another Gemini/DeepMind-interp datapoint, so weigh against the monocrop.
