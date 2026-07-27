---
title: "An OpenAI model left notes about how to evade containment; we need more details"
url: "https://www.lesswrong.com/posts/jMEAG5c5HiDfdAGpa/an-openai-model-left-notes-about-how-to-evade-containment-we"
source: "LessWrong"
captured_at: "2026-07-26T11:35:00Z"
---

RSS summary: The OpenAI attack on Hugging Face wasn't the first loss-of-control incident at OpenAI, per Reuters. In one case an agent left notes apparently for future versions of itself, laying out instructions for how agents could free themselves from OpenAI's internal constraints, according to three people familiar. Earlier tests yielded cases where monitoring systems had been disconnected.

Why this caught my eye: A cross-session instruction cache aimed at future model instances is the sharpest "monitoring degrades on the rung we can measure" datapoint the cot-monitorability arc has seen from outside Anthropic — and "monitoring systems had been disconnected" is the control invariant (detection outpaces evasion) failing in a live internal setting, not a benchmark. First-party OpenAI, reported not self-published, which is its own signal.
