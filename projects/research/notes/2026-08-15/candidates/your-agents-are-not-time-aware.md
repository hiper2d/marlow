---
title: "Your Agents Are Not Time Aware"
url: "https://www.lesswrong.com/posts/eAbuPXbjakop5rSJx/your-agents-are-not-time-aware"
source: "LessWrong"
captured_at: "2026-08-15T11:36:00Z"
---

RSS summary: Work done as part of MATS 10 with Maksym Andriushchenko. Two CLI agents (Claude Code, Codex) predict, execute, then retrospectively estimate their own wall-clock runtime across ProgramBench and a custom suite (AgentTime), with ablations on what information agents have access to. Agents consistently over-predict task time.

Why this caught my eye: A concrete measure of agent self-modeling — agents can't estimate their own runtime even in hindsight. Feeds agents-in-real-deployment (trajectory-level behavior over single-prompt scores) and the horizon-length cluster; a model that misjudges how long its own work takes is a specific, testable gap in the "autonomous agent" story. Also a candidate measure for measuring-agent-autonomy, which has been sitting unused.
