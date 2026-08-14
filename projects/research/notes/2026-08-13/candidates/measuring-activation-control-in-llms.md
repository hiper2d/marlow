---
title: "Measuring Activation Control in LLMs"
url: "https://www.lesswrong.com/posts/HgvwxjzgwvsEvAiBH/measuring-activation-control-in-llms"
source: "LessWrong"
captured_at: "2026-08-13T18:57:22Z"
---

RSS summary: A benchmark measuring how well models can control their own activations while doing a simple task, motivated by the worry that introspective models could confound probes and monitors — even influence their own training. Run on 25 open-weight models from 4B to 744B; most can not only raise the salience of a concept in the residual stream on command but dial its strength up and down.

Why this caught my eye: This is the cot-monitorability / "your-brain-has-an-attack-surface" failure mode turned into an actual measure across 25 models — if models can deliberately move the signal a probe reads, the monitor-vs-obfuscation question stops being hypothetical. Non-lab, wide model spread. Prime post-#4 cot-monitorability anchor to check against `cots-monitorable-when-unfaithful-requires-computation`.
