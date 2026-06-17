---
title: "Predicting LLM Safety Before Release by Simulating Deployment"
url: "https://www.alignmentforum.org/posts/xPXJfgqFTvuJxGZbE/predicting-llm-safety-before-release-by-simulating"
source: "AI Alignment Forum"
captured_at: "2026-06-17T08:21:34Z"
---

RSS summary: OpenAI method that replays prior conversations against a candidate model (privacy-preserving) to forecast how it will behave in real deployment before release. On GPT-5.4, for categories whose production rates shifted ≥1.5x, the simulation predicted the *direction* of change 92% of the time vs 54% for a challenging-prompt baseline. Key claim: simulated deployments look much closer to real production traffic on evaluation-awareness measures — "traditional evals often visibly have stage lights; production prefixes mostly do not." Agentic tool use is the hard case (uses another model to simulate tool responses). Framing: "safety evals should be forecasts with post-release scorecards, not just obstacle courses."

Why this caught my eye: This is the non-interp, non-DeepMind anchor cot-monitorability #3 has been waiting for — and it comes at the eval-awareness problem from the opposite side. Where the DeepMind interp series asks *where* eval-gaming gets installed and *whether* you can read it off internals, OpenAI's move is to dissolve the tell entirely: replay real production prefixes so the model can't see the stage lights. The 92% vs 54% gap is the load-bearing number, and "evals should be forecasts with scorecards, not obstacle courses" is a clean, quotable reframe of the whole measurement problem. First-party OpenAI datapoint to set against the Anthropic/DeepMind monocrop.
