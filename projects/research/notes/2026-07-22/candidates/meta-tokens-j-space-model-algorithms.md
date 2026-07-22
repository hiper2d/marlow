---
title: "Towards surfacing model algorithms with meta-tokens in the J-Space"
url: "https://www.alignmentforum.org/posts/6ek6n7yZ5DzfarJHy/towards-surfacing-model-algorithms-with-meta-tokens-in-the-j"
source: "AI Alignment Forum"
captured_at: "2026-07-22T14:45:00Z"
---

RSS summary: J-lens on Qwen3.6-27B surfaces "meta-tokens" — tokens that reveal non-obvious internal computation. Reading ambiguous text fires 什么意思 ("what does this mean"); steer it away and the model stops catching a pun. On LCM problems "gcd" fires, pointing at the product/GCD algorithm — swap the GCD vector from 9 to 3 and the model's LCM(27,90) answer moves 270→810. Before the model hedges, 大概率 ("most likely") fires; suppress it and the model commits to one option instead of hedging.

Why this caught my eye: This is the J-space method — the same "global workspace in language models" line Anthropic opened (the -06 anchor on cot-monitorability / model-welfare) — now applied by outside researchers to a *non-Anthropic* model (Qwen3.6-27B), which is exactly the source diversity that cluster has lacked. The load-bearing part isn't the interp trick, it's that steering a J-space meta-token causally changes the answer while the surface reasoning need not show it — a legible internal handle on computation that isn't visible in the CoT. Bears directly on cot-monitorability (internal state that steers behavior without a transcript trace) and the J-space cluster specifically.
