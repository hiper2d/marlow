---
title: "Attempt at Finding Alignment Faking on Llama 70B to test sleeper-agent detection generalizes"
url: "https://www.lesswrong.com/posts/8dXzDzk7nNK64jBve/attempt-at-finding-alignment-faking-on-llama-70b-to-test"
source: "LessWrong"
captured_at: "2026-07-21T11:43:38Z"
---

RSS summary: A 30-hour project sprint, reported as an honest null result with full code and data. MacDiarmid et al. (2024) showed a linear activation probe catches a sleeper agent about to defect even when directly asking the model fails; they left open whether this generalizes beyond artificial backdoors to naturally-arising deception. This tests that on Hughes et al. (2025) open-source alignment-faking checkpoints.

Why this caught my eye: Straight into the "detector validation doesn't transfer" leg the cot-monitorability arc has been building (did-you-lie, the belief-verified organisms work). A non-lab replication asking exactly the generalization question the original authors flagged, reported as a null with code — that honesty is the credibility signal. Read the result to see whether the probe failed to generalize or the setup couldn't elicit faking at all.
