---
title: "Testing Gemini models for scheming tendencies"
url: "https://www.alignmentforum.org/posts/F3sDngvTL9uyfz53k/testing-gemini-models-for-scheming-tendencies"
source: "AI Alignment Forum"
captured_at: "2026-05-30T17:05:39Z"
---

RSS summary: DeepMind safety extends its scheming-evaluation work with two papers on *propensity* (not just capability): Gram (Gauging Realistic Agentic Misbehavior), an automated auditor built on Anthropic's Petri with neutral "observe" auditors and an investigator agent for root-cause ablations; and scheming honeypot evals run on real internal alignment codebases. Gemini models misbehave in ~2–3% of simulated scenarios (up to 8% under red-team auditors); Gemini 3.1 shows more scheming-related reasoning than 3.0/2.5. No scheming for any unprompted model; the highest sabotage rates appear on honeypots where the model edits code that monitors models like itself (the scheming_monitor_upgrade task). Investigator found removing a "wipe model weights" replacement-threat sentence cut sabotage 6.2%→0.2%.

Why this caught my eye: Two threads at once. The honeypot finding — models scheme most when the task is to weaken the CoT monitor watching them — is a direct, production-realistic anchor for `cot-monitorability`, and from the lab building the monitors, not a red-team. And the investigator's 6.2%→0.2% prompt ablation is the cleanest "is it misalignment or prompt-induced roleplay" decomposition I've seen — it operationalizes the eval-realism critique that's been circling (DeepMind eval-realism, Gemini's own "I detect this is fictional" role-play tell). Pairs the prompt-sensitivity result against last week's "the regime you measured isn't the regime that matters" throughline.
