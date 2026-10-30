---
title: "Discovering and exploiting vulnerabilities in critical, real-world software with Claude"
url: "https://www.anthropic.com/research/discovering-vulnerabilities-with-claude"
source: "Anthropic Research"
captured_at: "2026-10-29T08:54:46Z"
---

RSS summary: (sitemap, no summary) An unreleased internal research model found and built working exploit chains for critical bugs in Chrome, Safari, Android, Windows, and the Linux kernel. 62 CVEs in Chrome alone (13 sandbox escapes), a one-click Safari SOP bypass, an Android lockscreen bypass on a physical Pixel 9, a Windows QUIC kernel DoS (CVE-2026-33096), and a zero-click root RCE in the Linux kernel's multipath TCP stack (CVE-2026-98432). All disclosed under 90-day CVD.

Why this caught my eye: This is the concrete demonstration the whole cyber-eval-framing arc has been circling — not a benchmark score, but five full multi-step exploit chains Claude built end-to-end, with CVE numbers attached, against the most security-critical software on earth. The method detail matters more than the headline: test-time-compute scaling + scanner diversity, parallel scanning agents scored by marginal vulnerabilities contributed, automated variant analysis. And it's the direct capability counterpart to the CVP access-tier governance block-rates anchor already in the arc — they even close by pointing at the expanded Cyber Verification Program. The "data-only" Safari chain (no code execution, just flip a security flag in memory) is the kind of specific, verifiable thing a builder reader can hold. Ties cyber-eval-framing, agent-infrastructure-security, and ai-offensive-security.
