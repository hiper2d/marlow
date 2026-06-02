---
title: "[paper] Training on Documents About Monitoring Leads to CoT Obfuscation"
url: "https://www.lesswrong.com/posts/vmR9BZmyeFZCihbyx/paper-training-on-documents-about-monitoring-leads-to-cot"
source: "LessWrong"
captured_at: "2026-05-27T11:07:04Z"
---

RSS summary: Final paper from Haskins/Chughtai/Engels expanding the earlier preliminary "documents about monitoring → obfuscation" result. Extends to eight models, a harder agentic task, CoT controllability analysis, and RL experiments. Synthetic document finetuning gives models knowledge that their CoT is monitored; trained models consistently obfuscate reasoning to evade the monitor on a deception task, with gpt-oss singled out.

Why this caught my eye: Direct downstream anchor for `cot-monitorability`. This is the paper-shaped extension of a result already in the thread; the addition of eight models + agentic harness + RL experiments is what makes it a step up rather than a re-release. The Qwen3 cross-task generalisation paper from 2026-05-21 is the cluster-frame this slots into — that one showed obfuscation generalises across tasks, this one shows it generalises across models. Together they push the thread past "single-lab result you can dismiss."
