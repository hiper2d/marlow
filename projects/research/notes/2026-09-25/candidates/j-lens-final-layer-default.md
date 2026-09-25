---
title: "J-lens shouldn't target the final layer by default"
url: "https://www.lesswrong.com/posts/Adb55vLqt33LEyBfz/j-lens-shouldn-t-target-the-final-layer-by-default"
source: "LessWrong"
captured_at: "2026-09-25T11:33:29Z"
---

RSS summary: ~80% of released J-lenses target the final layer. On DeepSeek-V3 that yields a J-lens dominated by one direction inherited from the final block, shifting English-vs-Chinese readouts and inflating one eval. Anthropic's J-lens paper had suggested the final block may specialize.

Why this caught my eye: A concrete methodology gotcha in interpretability tooling — the default layer choice quietly biases readouts and inflates an eval. The kind of "the measurement instrument is measuring itself" detail that matters for anyone trusting interpretability numbers.
