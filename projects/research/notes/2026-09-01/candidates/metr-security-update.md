---
title: "Update on Security at METR"
url: "https://metr.org/blog/2026-08-31-security-update/"
source: "METR"
captured_at: "2026-09-01T14:35:00Z"
---

RSS summary: METR discloses two 2026 security incidents. March: a researcher's vibe-coded agent-orchestration app on a personal EC2 instance had a fail-open auth bug, was found via certificate-transparency scanning for LLM/agent keywords, and an attacker prompted the agent to reveal a public-model API key — then burned ~$600k in (donated, free) credits over three weeks. May: a sustained agent-driven attack campaign (credential stuffing, OAuth grants, phishing) plus an inadvertently exposed read-only SQL endpoint in the public transcript viewer that could reach unpublished eval data, including some category-3 sensitive-model output. Disclosed by an independent researcher, bounty paid, no evidence of actual access.

Why this caught my eye: an evals org getting owned through its own agent tooling is the safety-tool-stewardship story in miniature — the people who red-team frontier models had a vibe-coded app leak a $600k key, and the attacker used the exact "prompt the agent for its key" move you'd expect. Two specifics worth holding: attackers now scan cert-transparency logs for LLM-keyword sites to harvest keys, and "we're used to weird rate-limit errors from big evals" is why the theft went unnoticed. Feeds `safety-tool-stewardship-handoffs` and `cyber-eval-framing`.
