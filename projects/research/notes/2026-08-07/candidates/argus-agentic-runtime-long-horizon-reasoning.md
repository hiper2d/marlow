---
title: "Argus: A General-Purpose Agentic Runtime for Long-Horizon Reasoning (via Discover AI)"
url: "https://www.youtube.com/watch?v=XnhP1STMm0w"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-08-07T15:29:47Z"
---

RSS summary: Discover AI video on the Argus paper (Boxiu Li et al., Microsoft + Shanghai Jiao Tong + Fudan + Tsinghua + HKU et al.). The pitch: a fixed capable LM can't run a long, revisable research campaign alone because three things are missing — no memory across stateless calls, no self-assessment independent of the assessor, a final artifact loses the process that produced it. Argus's three matched fixes: externalize state so continuity is a retrieval op; gate commits so acceptance is an independent check not a self-report; retain typed trajectories so experience (including reviewed rejected routes) survives past the call. Verification-guided persistence, pivoting, runtime self-evolution.

Why this caught my eye: Taken on the paper, not the video — the video framing ("AI self-morphs, leaves its guardrails behind") is clickbait, ignore it. The actual paper is the third harness-self-modification datapoint in this cluster after memoharness (-19 curate) and the AI2/UW harness-evolution item (cut -16): a frozen LM whose *runtime* evolves and gates its own commits. Directly on `automated-ai-rd`, which is source-dry, and the verification-gated-commit mechanism is a cleaner "is the self-improvement real or is it just test-time adaptation" probe than the LoC-merged proxies the arc keeps circling. Microsoft-led, broad Chinese-university author list — non-lab-monocrop diversity. Worth a body-fetch of the arXiv paper at curate if it's up.
