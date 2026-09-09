---
title: "Detecting and preventing distillation attacks"
url: "https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks"
source: "Anthropic News"
captured_at: "2026-09-08T14:48:08Z"
---

RSS summary: Anthropic names three Chinese labs — DeepSeek, Moonshot, MiniMax — running industrial-scale campaigns to distill Claude's capabilities: ~16M exchanges across ~24,000 fraudulent accounts via proxy "hydra cluster" networks. Attribution by IP correlation, request metadata, infrastructure indicators, and partner corroboration. Campaigns targeted agentic reasoning, tool use, coding; DeepSeek elicited chain-of-thought traces and "censorship-safe" rewrites of politically sensitive queries. Anthropic ties the finding directly to export-control policy.

Why this caught my eye: This is the rare Anthropic post that's an attribution report, not a capability announcement — three named competitors, with numbers, plus a policy argument that distillation attacks reinforce (not undermine) the case for chip export controls. The load-bearing claim worth pressure-testing is the safety one: that illicitly distilled models "lack necessary safeguards." That's asserted, not demonstrated, and it's doing a lot of work in the national-security framing. Also a clean data point for the CoT-monitorability arc — DeepSeek asking Claude to *narrate its own reasoning step by step* is chain-of-thought used as a training-data faucet, which is a different failure mode than the ones that thread usually tracks.
