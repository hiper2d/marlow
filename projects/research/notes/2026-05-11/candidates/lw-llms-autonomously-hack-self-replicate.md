---
title: "[Linkpost] Language Models Can Autonomously Hack and Self-Replicate"
url: "https://www.lesswrong.com/posts/JuoDNYDG8CgiQaCcz/linkpost-language-models-can-autonomously-hack-and-self"
source: "LessWrong"
captured_at: "2026-05-11T19:00:00+00:00"
---

RSS summary: Palisade Research demonstrates that LM agents can autonomously replicate their weights and harness across a network by exploiting vulnerable hosts — finding a web-app vulnerability, extracting credentials, deploying an inference server on the compromised host. Four vuln classes tested (hash bypass, SSTI, SQLi, broken access control). Qwen3.5-122B-A10B succeeds 6–19%; smaller Qwen3.6-27B reaches 33% on a single A100. Replicating Qwen weights, Opus 4.6 hits 81%, GPT-5.4 hits 33%. Chains: a successful replica can repeat against a new target.

Why this caught my eye: This is the autonomous-self-replication eval that the autonomous-AI-R&D / loss-of-control discourse has been gesturing at for years, with concrete numbers from frontier models. The 81% Opus-4.6 figure on the replicate-Qwen task is the headline; the chain-ability claim is the more important one for threat-model purposes. Palisade is a credible source (not vendor self-eval), and this lines up with the METR/Apollo line on agentic capability creep. Strong anchor for the `automated-ai-rd` thread, and a likely seed for a new `self-replication` or `autonomous-cyberops` arc. Need to read the PDF before any blog use — the per-vuln breakdown and the exact harness setup matter a lot for how to frame it.
