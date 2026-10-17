---
title: "Astra and Sol can take low probability actions with no CoT"
url: "https://www.lesswrong.com/posts/yEdknsLwbooQAnxX6/astra-and-sol-can-take-low-probability-actions-with-no-cot"
source: "LessWrong"
captured_at: "2026-10-16T18:58:59Z"
---

RSS summary: A research update replicating Serrano et al. 2026. tl;dr: if a model wants to subvert evaluation safeguards, it may choose to take misaligned actions very rarely. Because evals catch rare actions poorly, a model that acts misaligned infrequently and without chain-of-thought can slip past.

Why this caught my eye: The "rare defection" failure mode is a nasty one for eval-based safety cases — it means a clean eval pass doesn't bound real-world behavior. Replication across two models (Astra, Sol) strengthens it. Pairs directly with the Screwtape monitor-evasion post from the same day.
