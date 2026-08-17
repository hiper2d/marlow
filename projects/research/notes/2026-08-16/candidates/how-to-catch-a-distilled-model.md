---
title: "How To Catch a Distilled Model"
url: "https://www.lesswrong.com/posts/8peYRGxHtmYsTe6Le/how-to-catch-a-distilled-model"
source: "LessWrong"
captured_at: "2026-08-16T11:43:30Z"
---

RSS summary: A novel algorithm to detect distillation across LLMs, claimed to work on both logit-based and hard-label distillation. It embeds hidden signatures into a model's token distribution without changing downstream capabilities, framed for large-scale provenance/attribution use ("your sovereign AI introduces itself as 'Claude from Anthropic' on day one").

Why this caught my eye: Model provenance and distillation-attribution is a governance-adjacent measurement problem that keeps showing up sideways (the Claude Tag / RSI proxy debates, the who-copied-whom question). A method that watermarks the output distribution to catch downstream distillation is a real technical artifact, not commentary — worth a look even if it doesn't map cleanly to a live thread yet.
