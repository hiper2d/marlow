---
title: "Government of Alberta uses Claude to find and fix cybersecurity vulnerabilities"
url: "https://www.anthropic.com/news/alberta-government-claude-cybersecurity"
source: "Anthropic News"
captured_at: "2026-07-09T09:13:25Z"
---

RSS summary: (sitemap entry, no summary — body fetched.) Alberta's Ministry of Technology and Innovation used Claude Code (Opus + Sonnet) to scan 466M lines of government code in 20 hours with ~50 parallel agents — a review the team estimates at ~6.5 years by traditional means — then patch, test, and in some cases rebuild legacy systems (a 25-year-old Java subsidy portal rebuilt in 4-5 days). Standing red-team/blue-team review agents on the Agent SDK now run ~95 security controls per pass; white papers published for other governments.

Why this caught my eye: The strongest agents-in-real-deployment anchor in a while — not a benchmark, a government running 50 autonomous agents against production-adjacent systems holding tax and social-services data, with human review before any patch ships. It's also the defense-dominant side of the cyber ledger made concrete: the same vuln-discovery capability the Fable recall was about, pointed at the long tail of unmaintained code the Epoch forecast said is the real risk surface. Numbers are Anthropic-marketing-filtered (case study, not an eval), worth saying so if curated.
