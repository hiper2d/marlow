---
title: "Not all features are created equal"
url: "https://www.lesswrong.com/posts/Y5Lv8vafibpo7iYhi/not-all-features-are-created-equal"
source: "LessWrong"
captured_at: "2026-06-22T19:28:38Z"
---

RSS summary: Recent Anthropic work shows interp-extracted LLM features fall into distinct categories with different properties, but state-of-the-art auto-interpreters ignore this variety. The author proposes AIR (Auto-Interpretability Router), which uses a sentence embedder to classify a feature's category and routes the most appropriate activation examples to the auto-interpreter; claims better results than OpenAI/Neuronpedia auto-interp.

Why this caught my eye: A tooling-side interp result — the auto-interp layer everyone leans on is undercounting feature variety, and a routing fix helps. Bears on whether interpretability claims (the bet anthropic-alignment-doctrine rests on) are measuring what they think they are. Note the source concentration caveat: yet another interp-tooling datapoint.
