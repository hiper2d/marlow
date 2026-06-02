---
title: "Looking for backdoors in Jane Street LLMs"
url: "https://www.alignmentforum.org/posts/a98MFPmqH54J2ayBn/looking-for-backdoors-in-jane-street-llms-1"
source: "AI Alignment Forum"
captured_at: "2026-05-28T15:45:53Z"
---

RSS summary: A writeup of the author's experience in the Jane Street LLM backdoor challenge — models trained with hidden backdoors that a participant tries to detect. Reports partial results: white-box (activation/weight) methods cracked some models after the activation/prompting approach didn't work. Stems from a Dwarkesh Patel podcast that advertised the challenge.

Why this caught my eye: A concrete, hands-on backdoor-detection result rather than a framework paper — and the finding that white-box methods worked where prompting/activation steering failed is itself the kind of explanation/handle distinction that's been recurring (see Steering-directions-are-explanations-not-handles, -27). Backdoor detection is the practical edge of the trust-the-behavior question; sits near `cot-monitorability` and `safety-tool-stewardship-handoffs`.
