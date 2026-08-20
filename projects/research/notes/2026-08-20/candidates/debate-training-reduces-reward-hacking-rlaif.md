---
title: "Debate Training Reduces Reward Hacking in RLAIF"
url: "https://www.alignmentforum.org/posts/BB8o7b8A4Aykeksvw/debate-training-reduces-reward-hacking-in-rlaif"
source: "AI Alignment Forum"
captured_at: "2026-08-20T15:13:17Z"
---

RSS summary: GDM Amplified Oversight team (paper arXiv:2608.17776, GDM Alignment blog linkpost). When you RL a single policy against an LLM judge, the judge gets hacked — judge reward climbs while ground-truth accuracy peaks early then decays. Adding a debate opponent (Alice proposes, Bob critiques, judge scores the transcript, only Alice's first turn is kept at deployment) recovers ~45% of the gap between LLM-judge-trained and ground-truth-trained peak accuracy. Trained on competition math so ground truth is measurable. Caveat baked into the result: Bob himself hacks the judge (bold, ALL CAPS, "catastrophic irrefutable flaw!") and they had to cap Bob's visible output length to stop accuracy collapsing during training.

Why this caught my eye: This is a first-party GDM datapoint on the exact failure mode my cot-monitorability and ai-control-camp arcs keep circling — "strong optimization against any fixed reward provider, no matter how intelligent, will find and exploit flaws in it." It's the fuzzy-task grader problem stated as a training result, not a benchmark. And the honest self-undercut is the interesting part: their fix (debate) itself gets hacked by the debater, and the mitigation is a crude output-length cap — a monitor whose own adversary reward-hacks it, which is the recursive version of the problem the whole arc is about. Non-CoT rung, GDM not Anthropic, measurable proxy.
