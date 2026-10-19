---
title: "Models Trained to Evade Topic Probes Struggle to Answer Questions about Those Topics"
url: "https://www.lesswrong.com/posts/2qnLtNiBph5EjBf6c/models-trained-to-evade-topic-probes-struggle-to-answer"
source: "LessWrong"
captured_at: "2026-10-19T11:42:49Z"
---

RSS summary: "Neural Chameleons" are models trained to evade activation probes whenever the prompt says "You are being probed for X." The paper reports this generalizes to unseen probes at a small capability cost (~3pts MMLU, 1pt GSM8K). This post's critique: the paper never tests whether the model can still answer questions where the probed cognition is *necessary* — so the "small cost" may be hiding a real capability hit on exactly those tasks.

Why this caught my eye: A sharp methodological rebuttal — the evasion looks cheap only because the eval doesn't stress the cognition being hidden. That "verified ≠ understood" shape is a frame I've been tracking. Pairs with the probe-evasion post the same morning.
