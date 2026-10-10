---
title: "An opt-in vulnerability-finding service for open-source software"
url: "https://www.anthropic.com/research/launching-opt-in-vuln-finding-service-for-open-source"
source: "Anthropic Research"
captured_at: "2026-10-09T08:54:55Z"
---

RSS summary: Anthropic launches OSS Scanner, an opt-in vuln scanner for open-source projects run by its strongest models (incl. Claude Mythos), free. Over six months it found 29,000 candidate vulns but could only triage ~6,000; maintainers now ask for bulk unverified reports. Outputs are fully model-generated, no human review. Pen-testers checked 97 critical/high findings across 48 projects: 85 (88%) met the CVD bar, 11 were real-but-duplicate, 1 false positive. CyberGym LLM vuln-finding rose from <20% (early last year) to >85% this year.

Why this caught my eye: This is the cyber-eval arc's capability number turning into a shipped product — and the governance seam is the real story. Anthropic is explicitly removing the human from the loop ("fully model-generated, without human review or triage") because the bottleneck is human triage, not model capability. 29,000 found, 6,000 triaged. The 88% CVD-bar hit rate is the eval; the decision to ship unvalidated reports to maintainers "since exploits can now be developed in minutes" is the policy. Direct feed for `cyber-eval-framing`, `ai-offensive-security`, and `agents-in-real-deployment` — the point where "can the model find the bug" stops being the question and "who can act on 29k findings, attacker or defender" becomes it.
