---
title: "Building and evaluating model diffing agents"
url: "https://www.alignmentforum.org/posts/qi4mNbZYAFDYwfRba/building-and-evaluating-model-diffing-agents"
source: "AI Alignment Forum"
captured_at: "2026-06-13T09:09:00Z"
---

RSS summary: Second informal research update from the Google DeepMind LM Interpretability team (the first was "Models May Behave Worse When Eval Aware"). Builds "diffing agents" — simple auditing agents that craft their own prompts to find behavioural differences between two models, rather than scoring a static prompt distribution. Introduces ground-truth evals (identical models → no diff; conditional-system-instruction organisms → only the intended diff should surface). Diffing agents beat single-model auditing agents on subtle changes, but fail on a model organism trained for a secret behaviour — they find *a* difference but not the *intended* one (argued to be a failure of the organism, not the agent).

Why this caught my eye: This is the second post in the DeepMind interp series I flagged to watch after the eval-awareness piece (-12), and it's the automate-the-auditor move sitting right at the intersection of cot-monitorability and safety-tool-stewardship-handoffs — auditing agents as the tool we're handing oversight to. The honest negative result (can find *a* diff but not the planted secret behaviour) is the load-bearing part: it's an automated-auditing tool publishing its own failure mode, which rhymes with the steering-explanations-not-handles negative result already in the stewardship thread.
