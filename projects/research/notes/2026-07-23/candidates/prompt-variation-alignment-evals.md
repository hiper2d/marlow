---
title: "In other words: The influence of prompt variation on alignment evals"
url: "https://www.lesswrong.com/posts/SZk2PGk6GXmKfGpGL/in-other-words-the-influence-of-prompt-variation-on"
source: "LessWrong"
captured_at: "2026-07-23T11:46:24Z"
---

RSS summary: An ARENA 8.0 Capstone-week sprint asking whether rephrasing an alignment eval changes model behavior. TL;DR: the data were noisy — almost every eval/model/prompt-variation combination gave inconsistent results, making clean conclusions hard. Still, prompt rephrasing had a measurable effect on alignment-relevant properties even on frontier models, and the authors argue the field of alignment evals should take this seriously.

Why this caught my eye: A robustness check on the measurement instrument itself — if a paraphrase moves an alignment score, the score is partly measuring phrasing, not the property. That's the eval-realism problem stated from the reliability side rather than the eval-awareness side, and it rhymes with the `would-your-ai-travel-agent-book-a-bullfight` finding that one line of company values moved welfare +48pp. The honest "our data were noisy" framing is the credibility signal — a negative-ish result about how little we can trust the numbers. Independent student sprint → source diversity. Anchors eval-realism (and by extension `cot-monitorability`'s reliance on eval-derived claims). Small sample, so weight the direction not the magnitude.
