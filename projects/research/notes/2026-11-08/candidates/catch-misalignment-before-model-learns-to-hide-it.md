---
title: "Let's Try to Catch Misalignment Before a Model Learns to Hide It"
url: "https://www.lesswrong.com/posts/iXKhtYuXtneXzw9fN/let-s-try-to-catch-misalignment-before-a-model-learns-to"
source: "LessWrong"
captured_at: "2026-11-08T02:37:54Z"
---

RSI summary: Proposes watching the *trajectory* of eval results across the whole training run rather than only the final checkpoint. Hypothesis: misaligned behavior shows up before the capability to hide it does — like children misbehaving obviously before learning to be sneaky — so a mid-training window could catch misalignment before it goes underground.

Why this caught my eye: Lands squarely on the "models evading the monitors built to watch them" idea in my work notebook — here it's the training-surface facet (catch it before it learns to hide) rather than the behavioral or operational one. A testable framing, not just a worry.
