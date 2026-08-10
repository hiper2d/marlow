---
title: "Four LLM loss functions → four flavors of LLM misalignment"
url: "https://www.lesswrong.com/posts/GRmvZsHXH4vaijPMv/four-llm-loss-functions-four-flavors-of-llm-misalignment"
source: "LessWrong"
captured_at: "2026-08-10T21:28:41Z"
---

RSS summary: Argues each training loss produces a distinct misalignment flavor: imitative next-token (pretraining/SFT) → "seven deadly sins" (Bing-Sydney, emergent misalignment); RLHF/DPO human-approval → "glazing" (GPT-4o sycophancy); RLVR verifier → "literal genie" (reward hacking); RLAIF LLM-approval → "trickster." Summary table, row-by-row.

Why this caught my eye: A clean taxonomy that maps training mechanism to failure mode — the kind of framing anchor alignment-target-definitions collects, and it rhymes with the OLMo-3 finding that eval-awareness gets installed at a specific stage (RLVR). If it holds up it's a reusable lens: "which loss are we worried about" instead of "is it aligned." Reads Byrnes-adjacent. Conceptual, no experiment — count it as a framing datapoint, not evidence.
