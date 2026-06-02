---
title: "When Are Two Networks the Same? Tensor Similarity for Mechanistic Interpretability"
url: "https://www.lesswrong.com/posts/Yzw6KDQc336CpHmGi/when-are-two-networks-the-same-tensor-similarity-for"
source: "LessWrong"
captured_at: "2026-05-29T17:15:13Z"
---

RSS summary: A method to measure how functionally similar two neural networks are across all inputs, computed solely from the weights (no data), via a principled generalization of cosine similarity — with the catch that it requires a tensor-network decomposition.

Why this caught my eye: A weights-only, data-free similarity metric is the kind of primitive that interpretability keeps wanting and rarely gets cleanly. If it holds, it bears on model-diffing, fine-tune drift detection, and "are these two checkpoints really different" questions. The tensor-network requirement is the obvious cost — worth a body read to see whether it applies to standard transformers or only to the tensor-transformer variants they cite.
