---
title: "Designing more efficient quantum circuits with Claude"
url: "https://www.anthropic.com/research/designing-efficient-quantum-circuits"
source: "Anthropic Research"
captured_at: "2026-10-17T09:02:35Z"
---

RSS summary: STEM Fellows work (led by Andi Gu, mentored by Alek Kemeny). Claude was given plain-language specs for eight quantum circuits across chemistry, optimization, physics simulation, and number theory, plus an automated evaluator to score each design. Working largely on its own, Claude found designs that beat the best published circuits — in some cases by an order of magnitude — cutting the quantum resources useful applications need and, the post argues, potentially pulling practical quantum computers forward.

Why this caught my eye: This is the automated-ai-rd pattern wearing a different domain's clothes — a plain-language spec plus an automated scorer, and the model out-optimizes published human work inside that loop. The scoring-vs-selection distinction from the taste-denominated-in-compute piece applies directly: the circuits were handed to it with an evaluator, so this is the "scorer exists, go beat it" regime, not open-ended problem choice. Worth it as a concrete capability anchor, with the caveat that "quantum computers could arrive sooner" is the kind of claim that wants independent verification before it's load-bearing.
