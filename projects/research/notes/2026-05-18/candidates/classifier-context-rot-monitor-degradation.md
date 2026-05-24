---
title: "Classifier Context Rot: Monitor Performance Degrades with Context Length"
url: "https://www.lesswrong.com/posts/7vpvNM7viJqNWAdG7/classifier-context-rot-monitor-performance-degrades-with"
source: "LessWrong"
captured_at: "2026-05-18T17:26:52Z"
---

RSS summary: Monitoring coding agents for dangerous behavior using language models requires classifying transcripts that often exceed 500K tokens, but prior agent monitoring benchmarks rarely contain transcripts longer than 100K tokens. We show that when used as classifiers, current frontier models fail to notice dangerous actions more often in longer transcripts. On MonitorBench, Opus 4.6, GPT 5.4, and Gemini 3.1 miss these actions 2x to 30x more often when we prepend 800K tokens of benign activity.

Why this caught my eye: Direct anchor for `cot-monitorability`. Three frontier models, 2x–30x miss-rate degradation at realistic context lengths — this is the kind of result that punctures the "just monitor the transcript" story for long-horizon agents. Triangulates with the AuditBench NLA result and the eval-realism arc.
