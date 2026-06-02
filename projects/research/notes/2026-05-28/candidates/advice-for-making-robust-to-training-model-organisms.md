---
title: "Advice for making robust-to-training model organisms"
url: "https://www.lesswrong.com/posts/CmkAxJi83jRv9eXgJ/advice-for-making-robust-to-training-model-organisms-1"
source: "LessWrong"
captured_at: "2026-05-28T19:42:52Z"
---

RSS summary: To develop training techniques that work on future misaligned AI, one strategy is to test them on model organisms. But model organisms built with common techniques are often fragile — they stop misbehaving after untargeted training that doesn't directly target the misbehavior (e.g. "train the model to talk like a pirate" wipes out the implanted misbehavior). The post gives advice for building model organisms robust to this.

Why this caught my eye: Methodology, not a result — but a load-bearing one. If your model organisms of misalignment are erased by arbitrary unrelated finetuning, every safety technique you validate against them is suspect. This is the experimental-validity flip side of the robust-to-training story, and it connects to the adversarial-FT-resistance question the CoT-obfuscation pair (Haskins + Qwen3) raised as the obvious next experiment.
