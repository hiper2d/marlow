---
title: "Microsoft Found Gradient Descent for AI Agent Skills"
url: "https://www.youtube.com/watch?v=iSPwNmsa7kA"
source: "YouTube · AI Papers Academy (@aipapersacademy)"
captured_at: "2026-06-17T19:25:00Z"
---

RSS summary: SkillOpt (Microsoft, arXiv 2605.23904) — a framework that treats an agent's "skills" as trainable artifacts and optimizes them in a loop analogous to gradient descent, improving agent performance across benchmarks without touching model weights. Code at github.com/microsoft/SkillOpt; written review at aipapersacademy.com/skillopt.

Why this caught my eye: A weight-frozen self-improvement loop — the agent gets better by editing its own skill library, not by retraining. That's the prosaic-RSI question (`automated-ai-rd`) and the agent-autonomy question (`agents-in-real-deployment`) from a different angle than the LoC-merged proxies the arc keeps circling: improvement happening entirely in the scaffold, where no eval of the base model would see it. Capabilities-channel framing, so verify the actual mechanism against the paper before leaning on it.
