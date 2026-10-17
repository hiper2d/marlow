---
title: "Screwtape: Adversarial Transcript Editing for Monitor Red-Teaming"
url: "https://www.lesswrong.com/posts/Z8jjgjfpAJocqZiET/screwtape-adversarial-transcript-editing-for-monitor-red"
source: "LessWrong"
captured_at: "2026-10-16T18:58:59Z"
---

RSS summary: Screwtape is a pipeline that turns agent transcripts into realistic attacks that evade action-only monitors (monitors that don't read the agent's chain of thought) by inserting an attack and refining it until the monitor stops catching it. An LLM verifier checks the attack still works.

Why this caught my eye: Direct evidence on the action-only vs CoT-monitoring debate — if you can iteratively evade monitors that ignore the reasoning trace, that's an argument for keeping CoT in the loop. Feeds the ongoing monitoring/interpretability thread.
