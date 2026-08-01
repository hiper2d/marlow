---
title: "AI Changes Its Multi-Agent Topology During Inference (MANTA)"
url: "https://www.youtube.com/watch?v=T121XJrV58k"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-08-01T14:54:20Z"
---

RSS summary: Video summarizing MANTA — "Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems," Huang et al., Cornell / UIUC / Academia Sinica, arXiv:2607.28527. The system rewires the connections between agents at inference time rather than running a fixed collaboration graph.

Why this caught my eye: A multi-agent system that adapts its own topology during inference — the agents reconfigure who talks to whom without weight changes — is another "frozen weights, behavior moves" datapoint for `automated-ai-rd`, and it's the closest cousin yet to the memoharness / AI2-UW harness-evolution cluster: is the gain real architectural self-improvement or dressed-up test-time adaptation? Taken on the paper (arXiv:2607.28527), not the video — Discover AI is 0-for-every-curate on its own merits, so this stands or falls on the primary source. Worth a body-fetch to see whether the topology-adaptation gain is measured against a fair fixed-graph baseline or just against a weaker static default.
