---
title: "Untrusted advice for AI control: Short, strong advice significantly uplifts weak LLMs"
url: "https://www.lesswrong.com/posts/jLkRCK35ri2btEHMF/untrusted-advice-for-ai-control-short-strong-advice"
source: "LessWrong"
captured_at: "2026-07-28T11:40:54Z"
---

RSS summary: New "untrusted advice protocol": a trusted executor LLM takes every action, an untrusted advisor LLM can only send short hints. Even at 4 characters/step the advice recovers a substantial fraction of the capability gap between weak and strong models. Because the untrusted model's influence flows through a narrow, monitorable channel, they argue this achieves near-maximal safety in BashArena; also frames the general information-bottleneck-for-interpretability/security/cost idea. SWE-bench Verified results follow.

Why this caught my eye: This is a concrete, measured ai-control protocol — a designed information bottleneck as the safety lever, which is exactly the kind of "detection outpaces evasion on a rung we can actually measure" evidence `the-bottom-rung` and the sandboxing pick have been circling. The 4-characters-still-uplifts number is the hook.
