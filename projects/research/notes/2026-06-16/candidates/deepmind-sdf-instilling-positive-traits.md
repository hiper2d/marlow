---
title: "Synthetic document finetuning for instilling positive traits"
url: "https://www.alignmentforum.org/posts/GTYJRLhqztxKF2v5R/synthetic-document-finetuning-for-instilling-positive-traits"
source: "AI Alignment Forum"
captured_at: "2026-06-16T09:10:26Z"
---

RSS summary: Fifth informal research update from the Google DeepMind Language Model Interpretability team. They train Gemini 3 Flash to hold target traits/values by midtraining on synthetic documents describing a world where Gemini has those properties, then SFT on synthetic chat data demonstrating them (following Anthropic's MSM / synthetic-document-finetuning methods, Li et al / Marks et al / Kutasov et al). SFT instills traits robustly OOD; midtraining instills *stated knowledge* well but doesn't reliably transfer to behavior ("knowledge doesn't always mean internalization"). Includes a scan-cluster-autorate pipeline for catching over-represented structural patterns in synthetic data before training (e.g. accidentally teaching the model to always ask for clarification, or emotional-validation openings).

Why this caught my eye: Fifth DeepMind LM-interp post in roughly a week — the series is now 5-for-5 on the SFT/midtraining-shapes-safety-properties throughline that's been feeding cot-monitorability. It's the constructive mirror of the -15 "Why Do Naive SFT Filters Fail" post: same team, same instrument, now asking can you *install* deep alignment via synthetic data rather than can you filter it out. The "knowledge ≠ internalization" gap (model can recite the trait but won't enact it) and the finding that models silently absorb structural patterns that don't show in eval scores are both clean cot-monitorability anchors — behavior-shaping that the trace doesn't reveal. Heavily built on Anthropic's MSM work, so it also touches the alignment-pretraining / anthropic-alignment-doctrine arc.
