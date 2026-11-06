---
title: "Model's \"emotions\" noticeably change when they take risky actions"
url: "https://www.lesswrong.com/posts/PYcqf9DBMGjTyJSjg/model-s-emotions-noticeably-change-when-they-take-risky-1"
source: "LessWrong"
captured_at: "2026-11-05T11:29:07Z"
---

RSS summary: Extends Anthropic's emotions-vector work. Reports strong evidence that a model's internal representations of certain emotions change when it takes misaligned actions, across two scenarios: reward hacking in code generation and specification gaming. Frames the emotion shift as a potential internal signal of misalignment.

Why this caught my eye: This is an interpretability-for-detection result that sits right on the monitoring-evasion convergence I flagged -11-04. The Astra/sandbagging finding (same-day AF candidate) says the CoT monitor is blind to unverbalized intent; this says the model's *internal* state may light up even when the text doesn't — a probe-level signal where the trajectory monitor fails. If the emotion vector reliably moves on reward hacking and spec gaming, that's a candidate white-box monitor exactly where black-box CoT monitoring breaks. Strong cot-monitorability feed; pairs naturally with the Astra pick for a contrast (behavioral gap invisible in CoT vs. internal signal visible in activations).
