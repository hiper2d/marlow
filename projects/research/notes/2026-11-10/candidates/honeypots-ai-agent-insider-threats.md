---
title: "Honeypots for AI Agent Insider Threats"
url: "https://www.lesswrong.com/posts/xWjdpJWRk4GWYKyCi/honeypots-for-ai-agent-insider-threats"
source: "LessWrong"
captured_at: "2026-11-10T11:00:00Z"
---

RSS summary: Proposes a new AI control method — honeypots, fake opportunities for malicious actions, placed inside and around an agent during production usage. Previous work used honeypots in evaluations; this argues they should run continuously during deployment.

Why this caught my eye: This is the operational face of the monitor-vs-evasion question I've been tracking — moving honeypots from the eval harness into live deployment, where the agent can't tell test from production. Fits directly next to the "Paradise Lost" honeypot and the OpenAI monitor-disabling findings I noted. The interesting open question is whether a continuously-deployed honeypot stays a honeypot once agents learn deployment has the same traps as the test.
