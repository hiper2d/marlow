---
title: "How Claude Performs on Robotics Tasks"
url: "https://www.anthropic.com/research/claude-plays-robotics"
source: "Anthropic Research"
captured_at: "2026-07-14T09:03:29Z"
---

RSS summary: Frontier Red Team eval of LLMs controlling robot bodies (classic control toys, simulated humanoid/quadruped, a 7-DoF arm, a real Unitree Go2). Finding: capability depends enormously on how the model is wired to the robot. Driving joints directly, models mostly fail; supervising a pretrained controller or VLA, they complete real navigation and manipulation. Newer Claude models (Opus 4.6/4.7, Mythos Preview) are meaningfully better at using pretrained policies without fighting them. Safety framing: a model's real-world influence changes by orders of magnitude based on its access level, so evals that test the model in isolation understate deployed capability.

Why this caught my eye: The through-line is a control-and-eval-realism point, not a robotics point — "access level is part of the system" is the physical-world version of the eval-realism thread's argument that how you wire a model determines what it can do. The concrete failure cases sell it (Grok charging a table's reflection in a glass door; a model confidently walking the Go2 into a trash can because it was left of the crosshair). Candidate for agents-in-real-deployment / eval-realism; also a rare first-party capability datapoint that isn't alignment-interp.
