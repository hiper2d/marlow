---
title: "Training a Conceptual Reasoning Judge"
url: "https://www.lesswrong.com/posts/iHYZF2jweXb2E7X3Y/training-a-conceptual-reasoning-judge"
source: "LessWrong"
captured_at: "2026-08-15T11:36:00Z"
---

RSS summary: TL;DR: Fine-tune a judge LLM on a conceptual reasoning dataset to output a critique rating in a single forward pass. Significant uplift on held-out critiques, measured by alignment with human expert ratings. Improvement concentrated in discriminating low-quality, often model-written critiques — but the trained model still falls short in some respects.

Why this caught my eye: The grader-quality question from the eval-construction side — this is the E/U/N (capability error vs unresolvable taste vs noise) problem made concrete, a judge that gets better mostly at spotting bad model-written critiques. Feeds automated-ai-rd's recurring worry: every self-improvement proxy leans on a grader, and this is a paper about how good the grader actually is. The "concentrated in discriminating low-quality critiques" result is the interesting, honest part.
