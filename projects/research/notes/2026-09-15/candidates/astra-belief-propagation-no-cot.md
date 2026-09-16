---
title: "Astra appears to perform belief-propagation-like inference without CoT"
url: "https://www.lesswrong.com/posts/PAHqDoFrp9fybcSn2/astra-appears-to-perform-belief-propagation-like-inference"
source: "LessWrong"
captured_at: "2026-09-15T11:38:12Z"
---

RSS summary: Tested GPT-6 Astra on randomized Boolean logic problems. Astra solves surprisingly complex logic without chain-of-thought, and performance improves significantly with more filler tokens.

Why this caught my eye: Another hidden-cognition result feeding cot-monitorability #6 — this one is empirical (Boolean logic, filler-token scaling), which is a stronger form than the anecdotal Astra reads we've been logging (733, 727, 749). The filler-token finding is the sharp part: it says the serial computation is happening in the forward pass, not the visible reasoning. Note the arc is now Astra-heavy; the value here is the clean logic-problem operationalization, not the Nth "Astra thinks silently" claim.
