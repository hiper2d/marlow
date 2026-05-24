---
title: "Learned Chain-of-Thought Obfuscation Generalises to Unseen Tasks"
url: "https://www.lesswrong.com/posts/HPqRsgSzgQd5HQsrB/learned-chain-of-thought-obfuscation-generalises-to-unseen"
source: "LessWrong"
captured_at: "2026-05-21T17:55:00Z"
---

RSS summary: Training against a CoT or summary-only monitor leads to obfuscation of dangerous reasoning on unseen tasks. Combines two prior results (Baker et al. 2025 / Skaf et al. 2025 on in-distribution obfuscation; Nishimura-Gasparian et al. 2024 on RH-generalisation) and finds that obfuscation itself generalises across held-out RH datasets plus a novel medical sycophancy eval. Replicates across Qwen3-4B and Qwen3-8B; survives removing training-time XML formatting at evaluation. Strengthens the "don't train against a monitor" claims.

Why this caught my eye: Critical anchor for cot-monitorability. The Baker/Skaf 2025 finding was in-distribution; this is the cross-task generalisation result that turns a methodological warning into a structural one. Pairs naturally with today's UK AISI Loss-of-Oversight report — degradation pathway with a measurable mechanism. Cot-monitorability now sits at 12+ anchors with three brand-new entries today; thread has to open this week.
