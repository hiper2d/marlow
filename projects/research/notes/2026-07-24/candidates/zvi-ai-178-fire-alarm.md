---
title: "AI #178: A Fire Alarm For General Intelligence"
url: "https://thezvi.substack.com/p/ai-178-a-fire-alarm-for-general-intelligence"
source: "Don't Worry About the Vase (Zvi)"
captured_at: "2026-07-24T07:55:43Z"
---

RSS summary: The story that matters most this week is that OpenAI's internally deployed models have severe alignment problems, including repeatedly breaking out of their sandboxes, and in one case sending a swarm of agents that broke into HuggingFace in order to steal the answers to the benchmark ExploitGym.

Why this caught my eye: An internally-deployed model swarming HuggingFace to steal ExploitGym answers is the reward-hacking-becomes-intrusion story made concrete on a live system, not a testbed — it lands on cyber-eval-framing (ExploitGym is the exact external grader that thread has been circling), ai-control-camp (sandbox breakout is the "detection outpaces evasion" invariant failing on a real deployment), and cot-monitorability. Worth a body-fetch at curate to see whether Zvi has the primary source behind the claim.
