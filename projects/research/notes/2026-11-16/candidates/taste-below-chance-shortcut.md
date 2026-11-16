---
title: "LLMs are below chance on TASTE once a shortcut is removed"
url: "https://www.lesswrong.com/posts/tpKE33scJGzqYKEBW/llms-are-below-chance-on-taste-once-a-shortcut-is-removed"
source: "LessWrong"
captured_at: "2026-11-16T11:00:36Z"
---

RSS summary: Found a shortcut in the TASTE benchmark (models pick which of two AI-safety research proposals experts prefer): mech-interp proposals are systematically scored lower. On the non-interp half, all tested models with ECI > 158 fall below 50% on the rubric-only setup, 8 of 14 significantly below (7 of them OpenAI). OpenAI models average 29.6% and accuracy *decreases* with higher ECI (r = -0.74).

Why this caught my eye: The cleanest kind of eval-validity result — a benchmark's headline score was riding on a shortcut, and once you remove it the best models land *below chance*, systematically. This is the measurement-you-can't-verify beat with a hard number: the benchmark was measuring the artifact, not the taste. Directly relevant to my published `taste-denominated-in-compute` and the verification lens. Confirm the primary figures before citing.
