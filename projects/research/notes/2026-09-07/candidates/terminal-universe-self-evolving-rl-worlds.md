---
title: "Post-Train Qwen 27B: Beyond Harness Engineering (Terminal-Universe + Environment Evolution)"
url: "https://www.youtube.com/watch?v=z_brfNYsP2M"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-09-07T02:47:38Z"
---

RSS summary: Walkthrough of two ArXiv preprints on agentic RL. "Terminal-Universe" (Qwen Team, Alibaba / Tsinghua) reconstructs old agent trajectories into executable terminal environments at scale. "Environment Evolution for Terminal Agents" (Hunyuan Team, Tencent) evolves those into progressively harder, verifier-checked RL curricula. The pitch: stop tuning the agent harness, and instead generate an adaptive learning signal that post-trains the LLM itself.

Why this caught my eye: The interesting move is turning logged agent runs into reusable, auto-hardening training worlds — the curriculum builds itself and a verifier gates each step. That's the automated-RD loop (`automated-ai-rd`) pointed at the environment layer, and it's two labs converging on it at once. Video is a secondary source; the two ArXiv papers are the primaries to pull if it clears curate.
