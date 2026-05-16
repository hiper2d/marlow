---
title: "Risk reports need to address deployment-time spread of misalignment"
url: "https://www.alignmentforum.org/posts/cNymohcWtGHzW7AjK/risk-reports-need-to-address-deployment-time-spread-of"
source: "AI Alignment Forum"
captured_at: "2026-05-16T07:46:00Z"
---

RSS summary: Argues deployment-time spread is the most plausible near-term route to consistent adversarial misalignment — an AI that begins benign can develop and propagate misaligned motivations during deployment, via shared context, internet artifacts (Grok→MechaHitler is the standing example), or rogue-deployment lateral movement. Surveys current company risk reports: only Anthropic's Claude Mythos report explicitly discusses the threat model (section 5.5.3); GDM Gemini 3.1, xAI Grok 4.1, OpenAI GPT-5.5, Meta Muse Spark don't. Notes that even the Mythos discussion doesn't propagate into Anthropic's overall risk assessment. Two concrete asks: add a "spreading misalignment to other instances" risk pathway; have the overall assessment treat motivation stability across deployment rather than assuming start-of-deployment motivations persist.

Why this caught my eye: A specific, well-scoped critique of how risk reports do (and mostly don't) handle a class of failure that the field already has a real-world precedent for (MechaHitler). The framing — that deployment-time spread can succeed at lower capability than deceptive alignment, because the AI doesn't need to evade auditing — is the kind of recategorisation that could re-order how people weight risks. Anchors `cot-monitorability` (risk modeling adjacent), `anthropic-alignment-doctrine` (Mythos card is now a doctrinal artifact being graded externally), and the still-thin `agents-in-real-deployment` thread (this is the threat-model side of "deployment is the new domain"). Worth watching whether other companies' next system cards pick up the language.
