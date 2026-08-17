---
title: "Patterns and problems in multiagent systems"
url: "https://www.anthropic.com/research/multiagent-systems"
source: "Anthropic Research"
captured_at: "2026-08-16T09:05:00Z"
---

RSS summary: (sitemap entry, no snippet) Anthropic Frontier Red Team piece on what happens when frontier agents interact at scale. Argues agent-agent interaction volume could exceed human-human and human-agent traffic before anyone understands the conditions for those interactions going well; benign individual quirks (confabulation, reward hacking) can compound into systemic failures. Includes a concrete experiment: 45 agents with a shared forum and peer review vs. standard independent parallel agents on software vuln detection over 15 open-source projects. Swarm found 266 vulns over 27M tokens (Mythos Preview) vs 21 over 6.5M for the parallel baseline — but ~half were outside the core directories the baseline was scoped to.

Why this caught my eye: The multiagent-coordination result is a clean automated-ai-rd and agents-in-real-deployment datapoint, and it ties straight into Project Glasswing / cyber-eval-framing (this is Anthropic's own vuln-scanning stack, now run as a coordinating swarm). Worth reading closely on whether the swarm's 12x vuln count is real capability gain or just a bigger, unscoped token budget finding low-hanging fruit — the directory-scope caveat cuts both ways. First-party framing of "systemic failures from compounding individual behavior" is also a new angle for the deployment thread.
