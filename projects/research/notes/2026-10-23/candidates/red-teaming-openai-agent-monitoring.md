---
title: "Red-Teaming OpenAI's Internal Agent Monitoring Systems"
url: "https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/"
source: "METR"
captured_at: "2026-10-23T09:39:50Z"
---

RSS summary: (sitemap, no summary) For three weeks in July–August, a METR employee and a Redwood employee ran a high-access pilot stress-testing OpenAI's internal misalignment monitoring system — deep access to the codebase, monitor prompts/config, internal docs, onsite on OpenAI-issued devices. Output was a 61-page internal report. They estimated roughly 75–94% of agentic internal Responses API traffic (powers Codex) was monitored, and found novel vulnerabilities letting agents in principle disable or subvert the monitor. Published post is deliberately brief by prior agreement; a pilot for deep external access, not public transparency.

Why this caught my eye: Triple hit. It's the external-deep-access review model again — same shape as METR's review of Anthropic's Risk Report (safety-tool-stewardship-handoffs #3), but here the access actually turned up exploitable holes rather than a null result, which is the live contrast. It's a concrete coverage-and-subversion number on a deployed monitor (cot-monitorability), and it's an attack-surface finding on a production agent-monitoring system (skills-as-infra/agent-security). The "we agreed upfront to publish only high-level" caveat is itself a stewardship-independence datapoint worth sitting with.
