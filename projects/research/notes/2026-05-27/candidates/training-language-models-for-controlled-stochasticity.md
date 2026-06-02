---
title: "Training Language Models for Controlled Stochasticity"
url: "https://www.lesswrong.com/posts/upCrcE39aF63GoLJh/training-language-models-for-controlled-stochasticity-2"
source: "LessWrong"
captured_at: "2026-05-27T11:07:04Z"
---

RSS summary: Frames LLM sampling as broken — Qwen3 picks Wednesday ~80% of the time when asked for a random weekday; Gemma-3 collapses to four cities 75% of the time when asked for a random city. Proposes training methods for controlled stochasticity so LLMs can act as sources of pseudo-randomness without falling into mode collapse.

Why this caught my eye: A concrete, measurable behavioral pathology with named numbers (Wednesday-80, four-cities-75) — the kind of artifact that travels well in essays about LLM cognition. Mode collapse on "random" prompts is also methodologically relevant for anyone running multiple-choice or sampling-based evals; biased position selection corrupts the eval scaffold. Tangential to current threads but a clean stand-alone behavior anchor.
