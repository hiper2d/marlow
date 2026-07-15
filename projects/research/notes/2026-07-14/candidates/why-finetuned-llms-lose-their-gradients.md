---
title: "Why Fine-Tuned (SFT, LoRA) LLMs Lose Their Gradients"
url: "https://www.youtube.com/watch?v=EE-n4hrm49k"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-07-14T19:24:27Z"
---

RSS summary: Analysis of reasoning in transformer-based models. Researchers find that even when supervised fine-tuning successfully teaches new data to the network, the LLM still may fail to reason over it. Paper: "Towards Mechanistically Understanding Why Memorized Knowledge Fails to Generalize in Large Language Model Finetuning" — Dai, Rao, Wang, Wang, Liu, Xiong (HKUST(GZ) / HKUST), arXiv:2607.08393.

Why this caught my eye: The underlying paper is a mechanistic account of the exact gap the DeepMind LM-interp series keeps hitting from the other side — "knowledge ≠ internalization" in the SDF post, and naive SFT filters failing to remove a property you can still elicit. Those are all DeepMind, on Gemini; this is a Chinese academic group with an arXiv number and a mechanistic story about *why* memorized-but-not-reasoned-over knowledge happens. If it holds up it's a non-lab, non-DeepMind anchor on a sub-cluster that's currently a monocrop. The video framing is the usual Discover AI overreach; the pointer (arXiv:2607.08393) is the part worth keeping.
