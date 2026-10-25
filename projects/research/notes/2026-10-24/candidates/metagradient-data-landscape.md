---
title: "Exploring the data landscape via metagradient descent"
url: "https://www.lesswrong.com/posts/iduSpeG2Y6kAf4uHk/exploring-the-data-landscape-via-metagradient-descent"
source: "LessWrong"
captured_at: "2026-10-24T14:28:00Z"
---

RSS summary: Iliad Fellowship / EleutherAI work using metagradient descent to probe the "data landscape" — treating the training data itself as the thing to optimize over, reasoning backward from what a model learns to which regularities in the data produced it.

Why this caught my eye: Methodologically this is training-corpus-as-alignment-surface — differentiating through the data rather than the weights. If you can take metagradients w.r.t. data you can ask which data caused a behavior, which is the attribution tool half of the "verified≠understood" and data-provenance frames. Technical, primary, worth a closer look.
