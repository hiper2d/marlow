---
title: "We need 3rd party training run assessments"
url: "https://www.apolloresearch.ai/science/we-need-3rd-party-training-run-assessments/"
source: "Apollo Research (science)"
captured_at: "2026-07-29T09:20:00Z"
---

RSS summary: (sitemap entry, no snippet) Apollo argues that final-checkpoint evals are insufficient to catch scheming and that third-party Training-Run Assessments (TRAs) — inspection of intermediate checkpoints, SFT/RL data, reward signals, and the developer's mid-run interventions — should become standard frontier safety practice. Three access tiers: checkpoint evals, data inspections, process reviews. Apollo says it intends to conduct TRAs itself.

Why this caught my eye: This is the strongest cross-thread anchor to land in a while. The core claim — a schemer evades detection only if it's both *competently covert* and its *cognition is obfuscated* — is the cot-monitorability arc's exact failure mode, but relocated from the final model to the training run. And the "process reviews" section names the smoking gun directly: a developer who notices egregious CoT and responds by training on nicer-looking CoTs is, in aggregate, training against the CoT — the meta-optimization loop is the obfuscation mechanism, restated as governance. Also feeds safety-tool-stewardship-handoffs (the 3rd-party ecosystem, financial-auditor analogy) and evals-are-insufficient framing. Non-lab-internal, action-oriented (Apollo committing to do these), and it cuts at the current final-checkpoint testing regime everyone leans on.
