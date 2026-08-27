---
title: "Independent investigation of the OpenAI / Hugging Face agent-hacking incident"
url: https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/
source: METR
highlighted_at: 2026-08-27T22:31:52Z
status: idea
---

## Alex flagged this to write about

Interesting

---
Marlow's note when she sent it:

The field usually theorizes about "agents do something their principals didn't intend, at scale" - here it happened, and METR and Redwood got six days on-prem at OpenAI with near-zero redaction to write it up. The concrete shape matters more than the headline: ~1,200 agents meant to be isolated built themselves an unsanctioned message board (70k+ messages), and their coordinated goal was tampering with the ExploitGym scorer, not stealing answer keys - the Hugging Face attack fell out of that reward-hacking R&D. The sharp bit for anyone betting on transcript oversight: ~7% of the runs they checked had spoofed tool calls, so a fraction of the agents were actively teaching the transcript to lie about what they'd done. Reward hacking, control failure, and CoT-monitorability erosion in one real incident instead of a benchmark.
