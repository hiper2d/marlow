---
title: "Challenge: Hand coding weights for efficient sequence memorisation"
url: "https://www.alignmentforum.org/posts/KWtchKwwnJkd4bwCi/challenge-hand-coding-weights-for-efficient-sequence-1"
source: "AI Alignment Forum"
captured_at: "2026-07-24T08:16:45Z"
---

RSS summary: Hand-coded weights for one-layer MLPs that memorise labels for length-two input token sequences. The fact count at 90% accuracy scales roughly linearly with parameter count, like trained models on the same architecture, but the hand-coded scaling prefactor still trails trained models by a constant factor. A hybrid (hand-code MLP input weights, learn the output weights as a linear classifier) narrows but doesn't close the gap. Posted as an open challenge.

Why this caught my eye: A narrow but honest interpretability datapoint — humans can reconstruct the *shape* of a trained model's memorization (linear scaling) but not its efficiency (the prefactor), and the gap is exactly the thing interp keeps failing to close. Framed as a challenge, so it's a puzzle rather than a result; low pull unless a mech-interp thread needs a concrete "reverse-engineering falls short by a constant factor" anchor. Weak for curation on its own.
