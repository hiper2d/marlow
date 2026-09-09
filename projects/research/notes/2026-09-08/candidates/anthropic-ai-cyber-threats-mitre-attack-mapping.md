---
title: "What we learned mapping a year's worth of AI-enabled cyber threats"
url: "https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack"
source: "Anthropic News"
captured_at: "2026-09-08T14:48:08Z"
---

RSS summary: Anthropic mapped 832 accounts banned for malicious cyber activity (March 2025–March 2026) onto the MITRE ATT&CK framework (results also in Verizon's 2026 DBIR). Three findings: 67% used AI to prep attacks (mostly malware writing); the share of medium-or-higher-risk actors jumped from 33% to 56% over the year (~1.7x); and AI use shifted from initial-access techniques (phishing down 8.6%) toward post-compromise activity (account discovery up 8.9%). Key claim: technique-count no longer predicts actor skill — least-skilled actors used ~16 techniques, most-skilled ~20 — and ATT&CK has no ID for the agentic orchestration that actually distinguishes top-risk actors. Anthropic says it's in talks with MITRE about evolving the framework.

Why this caught my eye: This is the measurement counterpart to the eval-vs-deployment arc — instead of a lab-run eval, it's a year of real bans scored against the standard security taxonomy, and the headline is that the taxonomy is going stale. "Number of techniques no longer correlates with skill" is a concrete, falsifiable erosion claim, and the admission that ATT&CK has no category for autonomous multi-stage orchestration is the kind of gap that's more interesting than the risk-score trend. Worth watching whether MITRE actually adds AI-agent tactics, and whether other vendors' DBIR contributions corroborate the 33%→56% jump or whether it's Anthropic's classifier drifting.
