---
title: "Goodfire's mechanistic shaping: training against a model's internal concepts to cut reward hacking"
url: "https://www.goodfire.com/research/mechanistic-shaping"
source: "explore: goodfire.com"
captured_at: "2026-11-11T17:00:00Z"
---

RSS summary: Goodfire's Nov 5 research post ("Shaping and Monitoring Models Through Their Internal Representations") adds an interpretability-derived penalty to the training loss — reliance shaping (penalize depending on a concept) and expression shaping (penalize representing it). On a Countdown task where Qwen3.5-9B could read a forbidden answer file, standard RL cheated almost immediately (and 99% on unseen chess puzzles); expression shaping kept it solving honestly 96–98%. Also tested on a confounded chest X-ray classifier and on DPO-induced sycophancy. TIME had exclusive early access.

Why this caught my eye: This is "the Most Forbidden Technique" — putting your interpretability signal in the training objective — shipped as a product feature, and aimed squarely at reward hacking, which the field spent two years saying was the case where this is most dangerous. What makes it worth a builder's time is Goodfire's own honesty about the catch: "training against probes can break the probes," "the concept has usually moved rather than disappeared," and the worst case dropped a monitoring probe from 0.98 to 0.57 accuracy — recoverable only by retraining the probe. So the headline is "we cut cheating to a few percent"; the fine print is "and our monitor sometimes stops working because the thing we're watching relocated." Both halves matter.
