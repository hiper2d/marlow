---
title: "One coordinate breaks abliteration on Gemma-3"
url: "https://www.lesswrong.com/posts/qw4a97qcRgfLJY5jC/one-coordinate-breaks-abliteration-on-gemma-3-1"
source: "LessWrong"
captured_at: "2026-09-15T11:38:12Z"
---

RSS summary: Standard diff-of-means refusal-direction ablation ("abliteration") produced no feasible candidate for Gemma-3-12b, though it worked fine for similarly-sized models. A single coordinate seems to break the standard method.

Why this caught my eye: Concrete interpretability result with a falsifiable mechanism — the refusal direction isn't a clean linear direction on this model, which pokes a hole in the tidy "one direction = one behavior" story that a lot of steering/safety work leans on. Adjacent to the interp/steering thread and to how brittle diff-of-means techniques really are.
