---
title: "Learning more about Claude's mathematical capabilities"
url: "https://www.anthropic.com/research/riemann-zeta"
source: "Anthropic Research"
captured_at: "2026-08-14T13:42:57Z"
---

RSS summary: (sitemap entry, no summary) — An unreleased research version of Claude, asked to "take a real stab" at the Riemann hypothesis, instead improved a longstanding lower bound for the fraction of zeta zeros on the critical line from 41.6% to 67.2%. Found over two Claude Code sessions, ~31M output tokens: 650 failed ideas, then ~60 coordinated subagents running 2,400 shell commands, refereeing each other, downloading 54 arXiv papers to check novelty, and producing a Lean-formalized proof. Two Anthropic mathematicians plus external experts Conrey and Goldston validated it. Draws on Aryan; Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh; Bombieri 2000.

Why this caught my eye: This is the cleanest automated-ai-rd datapoint in a while — a *verified* result (Lean proof + named human referees) on a real open-math frontier, not a self-reported LoC-merged proxy. The interesting nuance for the arc is exactly what Anthropic concedes: it's a novel *combination* of existing human results, not new machinery, and they don't think the techniques touch the hypothesis itself. Worth a skeptical read on "extend the reach of mathematicians' ideas" vs "discovered something" — but the subagent-refereeing-and-formalizing loop is the agentic-research shape the arc keeps circling. Also the anthropomorphic framing ("believe in yourself," Claude "surprised by its own finding") is doing rhetorical work that deserves flagging.
