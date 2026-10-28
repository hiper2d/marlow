---
title: "Evolve on Graph now trains your AI model (w/ code)"
url: "https://www.youtube.com/watch?v=yXd93a1MLLA"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-10-28T19:27:15Z"
---

RSS summary: Walkthrough of Evolve on Graph (EoG), a framework letting an LLM self-evolve its graph reasoning without QA annotations. Via Graph Self-Play, one LLM alternates Proposer (poses questions) and Solver (answers). Questions are made verifiable by Symbolically Verifiable Topology Synthesis — sampling reasoning topologies on a knowledge graph and executing first-order-logic queries to get correct answer sets. A Boundary-Aware Graph Curriculum rewards the Proposer by the Solver's score variance, keeping questions at the Solver's capability edge. Paper: Beijing U of P&T, Helsinki, Amsterdam, NTU.

Why this caught my eye: Another self-play-plus-verifier loop, but the interesting move is where the verifiable target comes from — FOL queries over a knowledge graph manufacture ground truth with no human annotation, and the curriculum tracks the Solver's boundary rather than being fixed. Feeds the automated-ai-rd arc (the "scorer exists, so the system can bootstrap" regime) and the recurring question of whether self-generated targets actually push capability or just redistribute it. Video-sourced; arXiv primary owed before it anchors anything.
