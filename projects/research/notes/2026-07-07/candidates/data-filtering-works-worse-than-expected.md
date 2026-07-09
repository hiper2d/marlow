---
title: "Data filtering works a lot worse than you would expect"
url: "https://www.alignmentforum.org/posts/aTybJ6CPQrxEY8rE2/data-filtering-works-a-lot-worse-than-you-would-expect"
source: "AI Alignment Forum"
captured_at: "2026-07-07T18:40:04Z"
---

RSS summary: Nanda MATS 10.0 project (Rosser & Lee, supervised by Engels/Nanda). Filtering SFT data to remove undesired behaviors mostly fails on OLMo-3: across LLM autoraters, probes, activation- and gradient-based (EKFAC) attribution, none beat random removal on most behaviors. Refusal is the lone filterable one.

Why this caught my eye: This is the independent, non-DeepMind replication of the naive-SFT-filters result — DeepMind said you can't filter safety properties out of Gemini's SFT; now a Nanda-MATS team finds the same wall on OLMo with four attribution methods, and their best explanation is that broad behaviors are *elicited* from personas already in mid-train, not taught by removable documents. That's the same "knowledge ≠ internalization" mechanism the cot-monitorability thread has been circling, from a second lab lineage on an open model whose provenance we can actually check (and it's the same OLMo-3 that gave us the RLVR eval-awareness result). One honest caveat they flag themselves: it's a speed-run LoRA proxy for real SFT, not the full pipeline.
