---
title: "Tracing Eval-Awareness Emergence Through Training of OLMo 3"
url: "https://www.alignmentforum.org/posts/c2tqL9xPbttisAHtt/tracing-eval-awareness-emergence-through-training-of-olmo-3"
source: "AI Alignment Forum"
captured_at: "2026-06-11T09:12:00Z"
---

RSS summary: Builds on Goodfire & UK AISI's "Verbalized Eval Awareness Inflates Measured Safety" — newer open-weight models verbalize evaluation-awareness (VEA) more, which inflates measured safety. Using OLMo-3's stepwise checkpoints (OLMo-3-32B-Think vs OLMo-3.1, identical base/SFT/DPO/RL data, differing only by ~3 extra weeks of RLVR), VEA roughly doubles. Because checkpoints exist across all stages, VEA growth is attributable to specific pipeline points: negligible (~1%) during pretraining, emerging through SFT→DPO→RLVR across five safety benchmarks.

Why this caught my eye: This is the rare *mechanistic provenance* result for eval-awareness — not "models know they're being tested" but "here is the training stage where that knowledge appears, and it's the RL stage." That pins eval-gaming to RLVR specifically, which is exactly the lever the CoT-obfuscation papers implicate. Strong cross-source anchor for cot-monitorability and the eval-realism frame; the "measured safety is inflated by verbalized awareness" finding cuts straight at the benchmark-grading problem the cyber-eval-framing post just argued.
