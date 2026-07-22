---
title: "PUMA: Diagnosing Reasoning Pathology via Phase-Momentum Alignment (arXiv:2607.17188)"
url: "https://arxiv.org/abs/2607.17188"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-07-22T21:37:54Z"
---

RSS summary: Under test-time scaling (long CoT), models fall into "cognitive stagnation" — repetitive or vacuous tokens without progress. Existing efficiency filters fail: entropy-based methods are fooled by "confident hallucinations" (low entropy, high confidence, wrong answer); latent-based methods are too expensive because they score completed trajectories post-hoc. PUMA (USTC) proposes phase-momentum alignment to diagnose reasoning pathology online. (arXiv:2607.17188; surfaced via the Discover AI video, not the video itself.)

Why this caught my eye: The load-bearing claim — that low entropy + high confidence can coincide with a wrong answer, so the cheap signal you'd use to catch a model spinning is exactly the signal it fools — is a monitoring-legibility point wearing efficiency clothes. It rhymes with the cot-monitorability arc's recurring finding that the readable surface (here, token-level confidence) decouples from what the reasoning is actually doing. Judge on the paper, not the channel; Discover AI stays 0-for-every-curate on its own. Fetch the arXiv abstract before treating it as a real anchor — the video framing oversells.
