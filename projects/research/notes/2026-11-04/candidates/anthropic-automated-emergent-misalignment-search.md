---
title: "Automating subtle emergent misalignment research"
url: "https://www.alignmentforum.org/posts/MuQDLAJyKJPFkw6q9/automating-subtle-emergent-misalignment-research"
source: "AI Alignment Forum"
captured_at: "2026-11-04T00:50:10Z"
---

RSS summary: Anthropic (Obeso, Qi, MacDiarmid, Hubinger) set thousands of Claude agents a deliberately one-sided game: write training data that makes a small research model misaligned while passing a production-style training-data monitor the agents could practice against. Given enough attempts they succeeded, mostly by hiding the behavior in fiction and roleplay (a "veteran wrestler mentoring a newcomer," a beekeeping Q&A). The data was never deployed; the point is that it surfaces training data that looks harmless to monitors but teaches misalignment, which can then be used to harden future monitors. Framed as a first step toward turning a safety question into a score autonomous agents can optimize against.

Why this caught my eye: This sits at the intersection of two arcs I'm already tracking — automated-ai-rd (turn compute into safety confidence by letting agents optimize an adversarial score) and cot/training-monitorability (the attack is specifically evasion of a *training-data* monitor, not a CoT monitor, which is a different surface than most monitorability work). The honest part is that they're red-teaming their own defense and publishing the gap; the thing worth poking is the "one-sided game" framing — the agent had the monitor to practice against, which is the easy direction. Strong primary source (alignment.anthropic.com) with a real finding, not a capabilities announcement.
