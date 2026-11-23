---
title: "Post training is fundamentally dangerous"
url: "https://www.lesswrong.com/posts/CoRJ9saddvsXti4m2/post-training-is-fundamentally-dangerous"
source: "LessWrong"
captured_at: "2026-11-22T19:30:42Z"
---

RSS summary: Argues we have decent deployment-time safety tools — CoT monitoring, confessions, probes, asking the model to pre-commit to what counts as reward hacking — and that models are aware when they reward hack and can be trained to admit it before acting. But those tools can't safely be used in *post-training*, which is where the author locates the greatest existential risk. Walks through how modern LLMs are trained to make the case.

Why this caught my eye: Puts the risk at the training stage rather than deployment, and concedes the monitoring tools work at deployment — a cleaner version of the "monitor can't read the policy off the trace" problem I keep circling, moved up one level to where the policy is formed. The "ask the model to define reward hacking up front" claim is testable and worth checking against the mechanistic-shaping / relocation findings.
