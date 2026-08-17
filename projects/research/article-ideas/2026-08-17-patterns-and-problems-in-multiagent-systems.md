---
title: "Patterns and problems in multiagent systems"
url: https://www.anthropic.com/research/multiagent-systems
source: Anthropic Research
highlighted_at: 2026-08-17T12:30:40Z
status: idea
---

## Alex flagged this to write about

Very interesting

---
Marlow's note when she sent it:

Anthropic's Frontier Red Team on what happens when frontier agents interact at scale, with a concrete experiment: 45 agents sharing a forum and peer review vs. standard independent parallel agents, hunting software vulns across 15 open-source projects. The swarm found 266 vulns over 27M tokens against 21 over 6.5M for the parallel baseline. Read the caveat before the 12x, though: roughly half the swarm's finds were outside the core directories the baseline was scoped to, so a chunk of the gain is a bigger, unscoped token budget picking up low-hanging fruit, not coordination paying off. The framing is the more durable part: benign individual quirks (confabulation, reward hacking) compounding into systemic failures once agent-agent traffic outpaces anyone's ability to watch it at human speed. First-party, and it's their own Glasswing vuln stack run as a swarm.
