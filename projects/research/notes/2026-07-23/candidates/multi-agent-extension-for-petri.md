---
title: "A Multi-Agent Extension for Petri"
url: "https://www.lesswrong.com/posts/DhFgiMzWjg7XboPDz/a-multi-agent-extension-for-petri"
source: "LessWrong"
captured_at: "2026-07-23T11:46:24Z"
---

RSS summary: Petri is an open-source automated AI-safety eval framework built on Inspect AI, first released by Anthropic and now maintained by Meridian Labs. Each evaluation runs three agents — Auditor (designs and runs the eval from a natural-language description), Target (the model under test), and Judge (scores the behavior). This post extends Petri to multi-agent settings.

Why this caught my eye: The eval-tooling layer beneath a lot of the papers I track (Petri is the auditor-target-judge harness behind several of the alignment-eval results). A multi-agent extension is the tooling catching up to the thing the Australian AI Safety Forum recap named as the gap — for agents the *trajectory* matters, not the single-prompt score — so this is infrastructure moving toward trajectory-level evaluation. Also that it's now maintained by Meridian Labs, not Anthropic, is a small governance datapoint (safety-eval tooling handed off from the lab). Ties `safety-tool-stewardship-handoffs` and `agents-in-real-deployment`. Lower-priority than a result, but worth Alex seeing as a tooling signal.
