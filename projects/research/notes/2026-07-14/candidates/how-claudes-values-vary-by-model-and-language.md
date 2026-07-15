---
title: "How Claude's values vary by model and language"
url: "https://www.anthropic.com/research/claude-values-models-languages"
source: "Anthropic Research"
captured_at: "2026-07-14T09:03:29Z"
---

RSS summary: Follow-up to Values in the Wild. Anthropic compresses the 3,000+ values it found in Claude.ai conversations into four axes (Deference vs. Caution, Warmth vs. Rigor, Depth vs. Brevity, Candor vs. Execution), then measures how those axes shift across models (Sonnet 4.6 warmer/more deferential, Opus 4.7 more rigorous/cautious) and across the top 20 languages (most warmth in Hindi/Arabic, most rigor in English/Russian). Pitched as a deployment-monitoring tool: run value profiling before ship and after release to flag unexpected shifts.

Why this caught my eye: The load-bearing move is turning "character" into a measurable, four-number profile that recovers reputation the labs already assign informally — and the language finding is the sharper one: the same business plan gets framed with different values in Hindi vs. Russian, so users in different languages are already getting a different Claude that nobody deliberately chose. Feeds alignment-target-definitions (is a stable value profile even the target if it varies by language?) and the doctrine arc (values you can shape in training but "not reliably observe in deployment" — now claimed observable).
