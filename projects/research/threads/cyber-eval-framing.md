---
slug: cyber-eval-framing
title: "Cyber-eval framing — who defines a dangerous cyber capability"
status: active
opened: 2026-06-10
last_synthesized: 2026-06-10
posts: 1
---

## What this thread tracks

The 2026 fight over AI offensive-cyber capability is being adjudicated almost entirely on benchmarks the model-makers built and grade themselves. This thread tracks the gap between the capability claims (Anthropic's Project Glasswing / Mythos-class restriction, the headline vuln-discovery numbers) and any external definition of what "dangerous cyber capability" actually is — including the argument that the standard eval target (novel zero-day discovery) is the wrong thing to measure in the first place.

## Where the arc stands now

The first article (`grading-your-own-danger`, 2026-06-10) landed on the day Anthropic split one model into a general-release Fable 5 and a cyber-restricted Mythos 5 — same weights, divided only by a private classifier. That made the framing problem operational: the evidence for the danger tier (10,000+ H/C vulns, Mozilla 271-in-Firefox-150, the ExploitBench/ExploitGym benchmarks) is overwhelmingly first-party, with UK AISI the lone external check. The one independent skeptical engagement concedes most of the capability cluster to GPT-5.5 parity and preserves only the narrow vuln-discovery/exploit axis — and a separate strand argues that axis isn't even where the risk lives (patch-deployment lag and the unmaintained long tail, not 0-day discovery). Glasswing's own update half-confirms it: the bottleneck has already shifted from finding to fixing. Arc-level point: "Mythos-class" is a unit of measurement with one supplier, and any restriction justified by it is a claim still waiting for a second party.

## Sources and anchors

- [Claude Fable 5 and Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) — 2026-06-10 — Mythos-class goes general: same model split into safe-for-all Fable 5 and cyber-restricted Mythos 5 by a classifier-fallback (<5% of sessions routed to Opus 4.8). UK AISI "made progress towards" a universal jailbreak in a brief window — first on-record crack. The framing problem made operational.
- [Project Glasswing: An initial update](https://www.anthropic.com/research/glasswing-initial-update) — 2026-05-23 — The core evidence trail: 10,000+ critical/high vulns across ~50 partners, Mozilla 271 in Firefox 150 (~10x Opus 4.6), UK AISI first model to solve both cyber ranges; ExploitBench/ExploitGym introduced in the same post. Bottleneck shifted from finding to patching.
- [Are Mythos' Cyber Capabilities Overstated? Yes and No](https://www.lesswrong.com/posts/bJY7ZJLDJw3Y3S266/are-mythos-cyber-capabilities-overstated-yes-and-no) — 2026-05-27 — First cross-lab skeptical engagement. Concedes the broad cluster (GPT-5.5 parity, more cost-efficient; AISLE shows cheaper models find the same bugs; one low-sev cURL bug), holds only the vuln-discovery/exploit gap. Narrows the strong claim to one axis.
- [Models finding software vulnerabilities is not the primary source of cybersecurity risk](https://www.lesswrong.com/posts/gutiw8MBrYDiD2u5z/models-finding-software-vulnerabilities-is-not-the-primary) — 2026-05-14 — The eval *target* is mis-specified: real risk is the patch-availability-to-deployment lag plus the unmaintained long tail, not headline 0-day discovery. Faster discovery just enlarges the patch gap.
- [AI-enabled cyber threats and MITRE ATT&CK](https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack) — 2026-06-03 — Attempt to ground offensive-AI behavior in a standard taxonomy rather than a bespoke leaderboard. Step toward an external measure (still lab-authored).
- [Quantitative AI risk assessment: a starting point](https://www.lesswrong.com/posts/CpmpyS9Rpz7obejaw/quantitative-ai-risk-assessment-a-starting-point-1) — 2026-05-27 — Imports the WASH-1400 probabilistic-risk lineage from nuclear safety; nine models of AI-enabled cyber attacks. Right instinct (measurement outside the vendor), but the WASH-1400 analogy carries that study's own contested credibility.
- [Expanding Project Glasswing](https://www.anthropic.com/news/expanding-project-glasswing) — 2026-06-02 — Scope/scale follow-on between the initial update and the Mythos 5 general release. Marks the program's move from pilot to product.

## Open questions / what to watch

- Does any external body — UK AISI as a standalone publisher, a CERT, an insurer pricing the risk — produce a cyber-capability measure the model-makers don't control? That's the load-bearing signal; until it lands, the danger tier is self-graded.
- Does the AISLE "cheaper models find the same bugs" result get a rebuttal from Anthropic, or does the cost-efficiency concession stand?
- How porous is the Mythos 5 classifier gate in practice — does the UK AISI "progress towards a universal jailbreak" note turn into a full break, and does Anthropic disclose it if so?
- Does the patch-deployment-lag framing get a concrete metric (mean time-to-deploy across the long tail), or stay a qualitative counterargument?
- Whether other labs adopt a "held cyber tier" of their own, which would make Mythos-class a category rather than one company's product line.

## Notes

First article opened this thread (brand-new-arc path). The arc is deliberately a rotation off the Anthropic-orbit *alignment* monocrop flagged in the 2026-05-31 editorial review — the beat here is capability-eval framing and cybersecurity, not alignment doctrine. Watch that it doesn't quietly become another Anthropic-only thread despite the topic shift; the external-measure question above is partly a coverage discipline for the thread itself.
