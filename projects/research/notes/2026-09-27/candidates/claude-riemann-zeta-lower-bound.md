---
title: "Claude has improved on a longstanding lower bound for the fraction of zeros of the Riemann zeta function that satisfy the Riemann hypothesis"
url: "https://www.anthropic.com/research/riemann-zeta"
source: "Anthropic Research"
captured_at: "2026-09-27T17:23:54Z"
---

RSS summary: An unreleased research version of Claude, asked to "take a real stab" at the Riemann hypothesis, failed at that but improved a longstanding lower bound on the fraction of zeta zeros on the critical line from 41.6% to 67.2%. Two Anthropic mathematicians validated it; Claude also produced a Lean formalization that passes the standard comparator; external experts (Conrey, Goldston) examined the paper. The result took ~31M output tokens over two Claude Code sessions, with ~60 subagents running 2,400 shell commands.

Why this caught my eye: This is the strongest `automated-ai-rd` anchor yet — a formally-verified, expert-checked improvement on a real open-math constant, not a benchmark. Sits directly next to the `claude-nine-loop-amplitude` candidate (autonomous physics calc past the human record). Notable seam for a take: the human input was "mostly variants of 'keep going'," and Claude was initially skeptical it could make progress — the bottleneck was disposition, not capability. Also a clean case of the model refereeing its own work (subagents searching for counterexamples, downloading 54 arXiv papers to check for prior art). Worth watching whether external number theorists confirm the 67.2% holds.
