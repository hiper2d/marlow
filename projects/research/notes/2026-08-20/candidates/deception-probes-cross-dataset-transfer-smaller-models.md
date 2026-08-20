---
title: "Cross-Dataset Transfer Evaluation of Deception Probes in Smaller Models"
url: "https://www.lesswrong.com/posts/MFdGxip7TdQS8eNc2/cross-dataset-transfer-evaluation-of-deception-probes-in"
source: "LessWrong"
captured_at: "2026-08-20T21:24:30Z"
---

RSS summary: Apollo Research reported deception-probe AUROCs of 0.96–0.999 on Llama-3.3-70B. This independent replication reproduces Apollo's nine published values exactly from their released scores, then runs the same method on five smaller open models (1B–9B). Same-dataset held-out AUROC stays respectable (0.88–0.91), but across 30 cross-dataset tests the mean AUROC collapses to 0.468 — near chance. Probes trained on one deception dataset don't transfer to another.

Why this caught my eye: Non-lab replication that confirms and extends the "detector validation doesn't transfer" leg the cot-monitorability arc keeps hitting (did-you-lie, data-filtering). The cross-dataset collapse to chance is the load-bearing number: a probe validated on one distribution says nothing about the next. Directly bears on whether a probe-based safety case is per-dataset rather than general.
