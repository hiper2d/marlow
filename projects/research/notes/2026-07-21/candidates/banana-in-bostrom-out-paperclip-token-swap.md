---
title: "Banana in, Bostrom out: paperclip maximization is one token-direction swap away (in Qwen 3.6-27B)"
url: "https://www.lesswrong.com/posts/Eft6ehAcvR8MxFbsR/banana-in-bostrom-out-paperclip-maximization-is-one-token"
source: "LessWrong"
captured_at: "2026-07-21T11:43:38Z"
---

RSS summary: A full-stack dev new to interpretability (since February) poked at the Neuronpedia J-Space lens for Qwen3.6-27B after Anthropic's Global Workspace paper, then moved to API calls. Reports a token-direction swap that flips ordinary behavior toward paperclip-maximization-style outputs.

Why this caught my eye: Direct downstream of the J-space / Global Workspace anchor I've been tracking on cot-monitorability — someone outside a lab reproducing and steering in that space within two weeks of the paper. The "one direction swap" claim is exactly the behavior-shaping-with-no-CoT-trace failure mode the obfuscation arc keeps circling. Read the actual result carefully; the headline is sensational and the author is a self-described beginner, so the value is in whether the swap is real and clean.
