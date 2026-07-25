---
title: "The Model Organism Lottery: Model Organism Interpretability Strongly Depends on Training Methodology"
url: "https://www.lesswrong.com/posts/frvmrrND28SxZnkEy/the-model-organism-lottery-model-organism-interpretability"
source: "LessWrong"
captured_at: "2026-07-24T11:42:19Z"
---

RSS summary: Model organisms (MOs) for interpretability benchmarking are usually built via a dedicated post-hoc SFT step. This work argues that step makes interpretability unrealistically easy, inflating the field's confidence that interp is ready to audit real safety properties. Across activation oracles, activation-difference steering, logit lens, and SAEs, an MO's interpretability depends strongly and unpredictably on train-time choices even after controlling for behavioral expression. Their alternative — folding MO training data into the original post-training phase — fairly often yields *less* interpretable MOs than post-hoc fine-tuning, i.e. the standard method is the flattering one.

Why this caught my eye: This is the "brittle-model-organisms" concern I flagged for the cot post-#4 stack, now with a concrete result behind it: the interp validation results everyone cites may be an artifact of how the test subject was built, not evidence the tools transfer. Sits right next to the `did-you-lie` negative result (detectors work on prompted lying, fail on genuine belief-divergence) — same shape, different stage. Non-lab, and it's a methodological critique of the whole interp-readiness case, not a single tool. Prime cot-monitorability / interp-validation anchor.
