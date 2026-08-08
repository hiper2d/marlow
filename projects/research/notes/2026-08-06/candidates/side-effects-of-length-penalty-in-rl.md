---
title: "Side-Effects of Length Penalty in RL"
url: "https://www.lesswrong.com/posts/dervHn4makG6EggxR/side-effects-of-length-penalty-in-rl"
source: "LessWrong"
captured_at: "2026-08-07T02:40:00Z"
---

RSS summary: MATS-stream write-up (Feron + author, Neel Nanda stream). Labs use length penalties on CoT during RL for efficiency; the natural worry is worse monitorability as the model is pushed to omit information. Contrary to prior work, they find faithfulness on MMLU-with-hint *increases* under a length penalty. GRPO with length penalty on math, Qwen3-4B and Nemotron-Nano-8B. Other side effects (laziness/shortcutting) show up but none rated too concerning.

Why this caught my eye: A direct, measured, counterintuitive result on the CoT-monitorability arc's core anxiety — that efficiency pressure erodes faithful reasoning. Finding the *opposite* (faithfulness up, not down) is exactly the kind of "the number cuts against the slogan" datapoint the arc lives on. Non-lab, small models (caveat that), but it's a measure not a forecast.
