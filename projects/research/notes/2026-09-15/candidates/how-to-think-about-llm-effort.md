---
title: "How to think about LLM effort"
url: "https://www.lesswrong.com/posts/SiS37NfQjzJmy2GX7/how-to-think-about-llm-effort"
source: "LessWrong"
captured_at: "2026-09-15T11:38:12Z"
---

RSS summary: Frames the "effort" setting on an LLM as an input to both the model and the reward function in RL: Reward = Reward_raw − F(effort, token_length, Reward_raw, …).

Why this caught my eye: Conceptual, not empirical, but it's a clean framing of reasoning-effort as a reward-shaping term rather than a knob bolted on at inference — which connects to the CoT/serial-depth question of what the model is actually trading off when it "thinks harder." Lower priority than the empirical items, but a useful lens if the effort/depth arc keeps growing.
