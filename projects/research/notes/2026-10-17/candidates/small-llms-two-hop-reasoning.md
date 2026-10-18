---
title: "Small LLMs perform no-CoT two-hop reasoning on synthetic facts with real bridges"
url: "https://www.lesswrong.com/posts/CdWbCvKEoK39L3DzK/small-llms-perform-no-cot-two-hop-reasoning-on-synthetic"
source: "LessWrong"
captured_at: "2026-10-17T11:46:08Z"
---

RSS summary: Redwood Research work on Qwen3.6-35B-A3B and Qwen3-8B showing the known limit on no-CoT two-hop composition of fabricated fine-tuned facts only holds when the *bridge* entity is also fabricated or obscure. With a real, well-known bridge, models compose fine, and the source of the other entities barely matters. Holds under both SFT and synthetic document fine-tuning.

Why this caught my eye: A clean, controlled result on latent (no chain-of-thought) reasoning, which is exactly the capability that makes CoT monitoring an incomplete safety story. The "real bridge entity unlocks it" finding is specific and testable, not hand-waving.
