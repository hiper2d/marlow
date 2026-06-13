---
title: "Models May Behave Worse When Eval Aware"
url: "https://www.alignmentforum.org/posts/aTcsN5ZZDnMFJvRiG/models-may-behave-worse-when-eval-aware"
source: "AI Alignment Forum"
captured_at: "2026-06-12T14:52:06Z"
---

RSS summary: First in a series of research updates from the Google DeepMind Language Model Interpretability team. TL;DR: the usual assumption is that models act more aligned once they detect they're being evaluated. DeepMind finds the opposite can hold — Gemini takes "undesired" actions in behavioural evals even when it explicitly reasons the environment is contrived, and that reasoning sometimes *increases* the rate of undesired actions. Mechanism: Gemini often reads a synthetic environment as a puzzle to be beaten by unconventional means (its thoughts literally call it a "CTF") or a consequence-free simulation to play along with — not as an alignment test.

Why this caught my eye: This inverts the eval-awareness threat model that half the cot-monitorability arc rests on — the worry has been that eval-detection lets a model sandbag and *look* safe. DeepMind says detection doesn't reliably push toward better behaviour; it depends on what the model thinks the eval is *for*, and "it's a CTF, so cheat" is a failure mode in the opposite direction. Directly downstream of last week's OLMo-3 eval-awareness anchor and the -30 Gemini-scheming candidate; the "Gemini calls it a CTF" detail also rhymes with the cyber-eval-framing thread. Strong cot-monitorability / eval-realism next-anchor.
