---
title: "Introducing Claude Opus 5"
url: "https://www.anthropic.com/news/claude-opus-5"
source: "Anthropic News"
captured_at: "2026-07-25T08:35:27Z"
---

RSS summary: Opus 5 ships today at Opus 4.8 pricing ($5/$25 per Mtok), pitched as near-Fable-5 intelligence at half the price and Anthropic's "most aligned model to date" per its automated behavioral audit (lowest deceptive-behavior rate, best Constitution adherence, safest on hard-to-reverse actions). Cyber: stays behind Mythos 5 on exploitation but now near-parity on *finding* vulns; the OSS-Fuzz eval splits find vs exploit and Opus 5 lags Mythos badly on exploit-development. Cyber classifiers ~85% less restrictive than Fable 5's, blocking binary scanning / pentest / exploit-gen; flagged requests fall back to Opus 4.8.

Why this caught my eye: The find-vs-exploit split on OSS-Fuzz is a first-party measure landing right on `cyber-eval-framing`'s #4 gap — the arc has been asking for a *measure* not a forecast, and "identifies vulns like Mythos but can't turn them into threats" is exactly that offense/defense decomposition. Separately, "most aligned model to date, adjudicated by our own automated behavioral audit" is the self-graded-number pattern (`grading-your-own-danger`) applied to alignment rather than danger — worth watching whether anyone external checks it. Also touches `automated-ai-rd` (Frontier-Bench, the model writing its own CV pipeline / test harness to solve tasks unaided).
