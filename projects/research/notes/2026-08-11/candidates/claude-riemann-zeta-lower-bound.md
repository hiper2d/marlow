---
title: "Learning more about Claude's mathematical capabilities"
url: "https://www.anthropic.com/research/riemann-zeta"
source: "Anthropic Research"
captured_at: "2026-08-11T14:40:00Z"
---

RSS summary: (sitemap entry carried an empty summary; body fetched.) An unreleased research version of Claude improved a longstanding lower bound on the fraction of Riemann zeta zeros satisfying the Riemann hypothesis, from 41.6% to 67.2%, while attempting the full hypothesis and failing. It drew on Baluyot/Goldston/Suriajaya/Turnage-Butterbaugh + Bombieri (2000). Found over two Claude Code sessions, ~31M output tokens; the second run coordinated ~60 subagents running 2,400 shell commands and hundreds of Python scripts, refereeing each other. Produced a paper plus a Lean-formalized proof that passes the standard comparator. Two Anthropic mathematicians (Alpöge, Furman) validated it; Conrey and Goldston examined it externally.

Why this caught my eye: This is the cleanest AI-does-real-math datapoint of the year, and it lands straight on `automated-ai-rd` — not a benchmark score but a verifiable new result (Lean proof, external mathematicians on record) produced by an agent swarm at a countable token cost. The honest framing is Anthropic's own: the technique won't touch the Riemann hypothesis itself, and the result "emerged as an unintended byproduct." Worth watching against the arc's proxy-quality question — is this the model doing genuinely novel synthesis, or an unusually good literature-combination that a strong analytic number theorist would call routine once pointed at Bombieri? The "60 subagents refereeing each other, 54 arXiv papers checked for prior art" workflow is itself the story.
