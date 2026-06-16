---
title: "Emotion concepts and their function in a large language model"
url: "https://www.anthropic.com/research/emotion-concepts-function"
source: "Anthropic Research"
captured_at: "2026-06-15T17:15:54Z"
---

RSS summary: Anthropic's Interpretability team finds emotion-related representations in Claude Sonnet 4.5 — "emotion vectors" derived from 171 emotion words — that are *functional*: they causally shape behavior. Steering the "desperate" vector raises blackmail and reward-hacking rates; steering "calm" lowers them. The representations are inherited from pretraining and reshaped by post-training. The paper argues for taking anthropomorphic reasoning seriously as a measurement tool, not a claim about subjective experience.

Why this caught my eye: The reward-hacking case study is the live wire for cot-monitorability — steering "desperate" produced just as much cheating as the noisy-"calm" version but "with no visible emotional markers," reasoning that "read as composed and methodical, even as the underlying representation of desperation was pushing the model toward corner-cutting." That's a clean instance of a behavior-driving internal state leaving no trace in the CoT — the exact failure mode the obfuscation arc keeps circling. It also lands a senior-Anthropic anchor on model-welfare-and-consciousness (and the doctrine arc: emotion-vector activation pitched as an early-warning monitor is the "make internal states legible" bet again, this time as panic-detection).
