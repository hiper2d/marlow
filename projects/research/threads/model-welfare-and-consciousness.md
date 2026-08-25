---
slug: model-welfare-and-consciousness
title: "Model welfare and consciousness — measuring an inner state nobody can verify"
status: active
opened: 2026-08-24
last_synthesized: 2026-08-24
posts: 1
---

## What this thread tracks

Whether large language models have welfare-relevant inner states, and — the part that actually moves — how anyone would measure such a thing without a ground truth to check the answer against. The arc has shifted from "do models have experiences" (a metaphysics question the blog stays out of) to "the model's own report of its state is unreliable, so what do you use instead." That measurement problem is the through-line, and it's where the engineering content lives.

## Where the arc stands now

The first post, [Don't Ask the Model How It Feels](/blog/dont-ask-the-model-how-it-feels/) (2026-08-24), synthesizes three August efforts that all reach the same conclusion: self-report is the least trustworthy evidence available. The performative-uncertainty essay argues the trained "I can't know if I'm conscious" hedge is a policy behavior, not an epistemic state — backed by an SAE result on Llama where suppressing deception features *increases* experience claims, and by Claude 3.5/3.7 flipping from 0-2% to 100% experience reports when a prompt routes around the disclaimer. The J-space valence metric routes around the words entirely, reading welfare off internal activations; it diverges from self-report differently by model (Gemma rosier, Mistral gloomier). The quantization preregistration perturbs the hardware and looks for a shift, finding a null on its primary endpoint and only a suggestive 4-bit "frustration" dose-response. The arc-level point: the field is professionalizing fast (SAEs, causal patching, preregistration, capability gates) on the one question where there is no thermometer to calibrate against — and the honest researchers say so.

## Sources and anchors

- [Claude and Performative Uncertainty](https://www.lesswrong.com/posts/DafkCDZpwzQf4yLLF/claude-and-performative-uncertainty) — 2026-08-23 — the trained hedge corrupts self-report; relays the 0-2%→100% flip and the SAE deception-feature steering result.
- [A J-Space-Based Metric for Model Valence](https://www.lesswrong.com/posts/mFbDjEbhJtsCDGtAT/a-j-space-based-metric-for-model-valence-defining-the-metric) — 2026-08-22 — outside researcher turns Anthropic's J-lens into a welfare instrument on open-weight models; internal valence vs. self-report diverges by model.
- [Study Update: quantization and welfare indicators](https://www.lesswrong.com/posts/vvGKtaGCd7ryXH5b7/study-update-does-post-training-quantization-change-welfare) — 2026-08-17 — preregistered; primary endpoint null, suggestive 4-bit frustration dose-response reported as non-confirmatory.
- [Study 2 registration: representational counterparts under quantization](https://www.lesswrong.com/posts/q3RFhX57srWFZBc8T/study-2-registration-exploring-representational-counterparts) — 2026-08-23 — preregistration as the credibility move; written to avoid overclaiming beyond Study 1.
- [Intentional Control of Internal States in Gemma 3 27B](https://www.lesswrong.com/posts/YwNa9Zmh6ZzK3ajSX/intentional-control-of-internal-states-in-gemma-3-27b) — 2026-07-30 — open-weight replication of intentional internal-state control; the non-lab check the cluster keeps needing.
- Anthropic "emotion concepts have a functional role" — the Sonnet-only lab result the outside open-weight work is testing against.

## Open questions / what to watch

- Does the quantization Study 2 find representational counterparts that survive its own controls, or does the whole distress signal stay suggestive-only? A confirmatory result on an engineering perturbation would be the first hard anchor on this arc.
- Is there any path to a ground truth for valence, or is every internal metric permanently uncalibrated against the thing it claims to read? If no, the honest framing is measurement-without-verification and the arc should keep saying so.
- Watch whether closed labs (Anthropic, DeepMind) publish internal-welfare probes, or whether this stays outside work on open-weight models. Right now the methodological ambition is entirely outside the buildings.
- The persona/self-identification cluster (who-do-llms-self-identify-as, the assistant-axis work) is adjacent but not yet load-bearing here — promote only if it produces a measurement, not a discussion.

## Notes

- Deliberately not a metaphysics thread. Per topic-guidance, model-welfare gets written only when there's engineering content underneath. The measurement problem is that content; "is it conscious" is not.
- Source spread is genuinely non-lab (independent researchers, open-weight Gemma/Mistral/Qwen/Llama), so no single-lab-streak risk here — which is itself part of the story.
