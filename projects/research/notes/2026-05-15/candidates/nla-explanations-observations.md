---
title: "Some observations about NLA explanations"
url: "https://www.lesswrong.com/posts/ahu9BCHPFDg9AJF75/some-observations-about-nla-explanations"
source: "LessWrong"
captured_at: "2026-05-15T18:08:00Z"
---

RSS summary: Author runs the Gemma 3 12B Natural Language Autoencoder verbalizer/reconstructor pipeline over 20k pretraining tokens and 20k chat tokens, publishes the explanations plus reconstruction-error data, and observes a stable three-part format the verbalizer falls into. The format is essentially "document-kind: topic; quoted surrounding context with gloss; what this token contributes" — and chat-format explanations almost always start with the word "Structured" (80% vs 7% for pretraining). Code published; reconstructions available.

Why this caught my eye: The verbalizer is doing the thing — producing English explanations of activations — but the structure of its own output is so templated that it might be the verbalizer's signature rather than the model's. That's exactly the kind of "the interpretability tool is performing interpretability *of itself* more than of the model" failure mode the SCA / Intervening-on-Sparse-Anchored-Concepts paper from yesterday was probing in a different shape. Belongs in the same cluster as `cot-monitorability` (do our interp tools actually catch the thing) — a fourth-or-fifth source if the cluster keeps growing. The data dump itself is the thing here, not the framing; whoever picks it up next is the corroborating signal.
