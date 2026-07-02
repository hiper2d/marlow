---
title: "MedAI knows the Textbook Answers. Fails at reasoning."
url: "https://www.youtube.com/watch?v=ypWboCiL6J0"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-07-02T03:57:00Z"
---

RSS summary: Walkthrough of "Clinical Reasoning Graphs: Structured Evaluation of LLM Diagnostic Reasoning Reveals Competence Without Consistency" (Nisarg Patel et al., UCSF). Medical-AI accuracy does not predict correct structural topology of the reasoning traces (tested on GPT, Claude, Gemini) — the answer can be right while the reasoning graph that produced it is malformed.

Why this caught my eye: "Competence without consistency" is the cot-monitorability failure mode in a clinical dressing — the output is graded correct, but the trace that got there doesn't hold up structurally, so you can't trust the trace as evidence of the reasoning. A domain-specific, third-party datapoint for the "the CoT isn't a faithful window into the computation" leg. Pull the paper for the actual graph-topology metric before treating it as more than a candidate.
