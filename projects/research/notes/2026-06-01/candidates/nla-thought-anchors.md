---
title: "NLA Thought Anchors"
url: "https://www.lesswrong.com/posts/6HnnMHRoJLff46kgw/nla-thought-anchors"
source: "LessWrong"
captured_at: "2026-06-01T02:30:00Z"
---

RSS summary: Follow-up probing why Natural Language Autoencoders (NLA) more often contain the prediction when the original activations led to a correct output. Findings: extraction position matters — the NLA answer appears in the activation vector more as the token approaches the model's final answer; the first sentence is most counterfactually important for both reconstruction loss and AV-contains-final-output; sentences important for generating the correct answer correlate with lower reconstruction loss, suggesting AR training reward encourages including correct answers. Notes degenerate NLA outputs (repetition, garbled text).

Why this caught my eye: Extends the NLA interpretability canon already running through the cot-monitorability thread. The "extraction-position-matters / first-sentence-most-important" result is a thought-anchors-style decomposition applied to autoencoder faithfulness — relevant to whether NLA reconstructions can be trusted as a monitoring surface. Incremental, but it's on-arc.
