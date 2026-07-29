---
title: "Discovering cryptographic weaknesses with Claude"
url: "https://www.anthropic.com/research/discovering-cryptographic-weaknesses"
source: "Anthropic Research"
captured_at: "2026-07-29T08:54:42Z"
---

RSS summary: (sitemap entry, no snippet) Using Claude Mythos Preview, Anthropic researchers found improved attacks on two cryptographic algorithms: a HAWK post-quantum signature attack that halves its effective key strength (60 hours, ~$100k API), and a 200-800x speedup on 7-round-reduced AES (the "Mobius Bridge" fingerprint, found near-autonomously over ~1 billion output tokens). Neither hits production systems. Also: LEA/Serpent/Salsa20 follow-ups, and CryptanalysisBench (with ETH Zurich, Tel Aviv, Haifa) to track LLM cryptanalysis over time.

Why this caught my eye: This is the thing cyber-eval-framing has been circling for months and never had — not a forecast, not a self-scored leaderboard number, but a concrete external-facing capability *measure*: a frozen model producing genuinely novel cryptographic research that survived expert validation (the AES one took two researchers a month to confirm). It's also a clean automated-ai-rd datapoint that sidesteps the arc's noisy proxies — the output isn't LoC-merged or a benchmark tick, it's a published attack. Two things to keep skeptical about when this reaches a draft: both headline results are "expected" (HAWK is an unfielded NIST candidate; AES is round-reduced), so the honest read is "faster search over the long tail of understudied ciphers," not "AES is broken" — and the $100k/attack plus month-of-human-verification cost is the real story about where the bottleneck moved. Pairs with the -20 cryptographic-boxes anchor (secure-MPC as a control mechanism) and the standing Mythos cyber-capability thread.
