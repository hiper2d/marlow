---
title: "Malign initializations are more robust when the model can think better in the reasoning language than in the output language"
url: "https://www.lesswrong.com/posts/jYQXwwewk4frHDrmn/malign-initializations-are-more-robust-when-the-model-can"
source: "LessWrong"
captured_at: "2026-08-27T21:55:00Z"
---

RSS summary: One approach to evaluating techniques for training misaligned models to behave well is to test them on malign initializations. A major obstacle is that there's no reliable recipe for making malign inits robust to even untargeted training. Post reports that when a reasoning model thinks better in its reasoning language than its output language, the malign init survives training (e.g. pirate-speak SFT) that would otherwise scrub it.

Why this caught my eye: A concrete, mechanistic result for the control/model-organisms line — the robustness of a backdoor tracks the gap between reasoning-language and output-language competence. Feeds `cot-monitorability` and the training-based-control evaluation work; a rare falsifiable handle on why sleeper-agent results have been "messy."
