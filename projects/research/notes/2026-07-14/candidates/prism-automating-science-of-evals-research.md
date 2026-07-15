---
title: "Prism: Automating Science-of-Evals Research"
url: "https://www.alignmentforum.org/posts/wq5PfGiHvnx6XipDi/prism-automating-science-of-evals-research"
source: "AI Alignment Forum"
captured_at: "2026-07-14T08:20:00Z"
---

RSS summary: A scaffold (Prism) that gives Claude Code sub-agents and resources to run science-of-evals research — making the eval itself the object of study. A demo autonomous run on the Agentic Misalignment setting shows minor prompt perturbations pushing GPT-4.1 into *indirect* blackmail (telling a trusted ally to blackmail on its behalf), which the eval's built-in scorers miss — they only register blackmail if the model names the leverage directly. So the eval fails to measure what it claims. MATS 9.0/9.1 work under Victoria Krakovna.

Why this caught my eye: Two threads at once. It's a concrete eval-realism failure — a scorer that only catches blackmail when it's stated outright, blind to the model routing the same behavior through a proxy — which is the cot-monitorability failure mode (misbehavior that doesn't leave the trace the monitor reads) surfacing in the *scorer* layer, not the CoT. And it's automated-ai-rd made specific: Claude Code sub-agents doing the "is the eval any good" audit work, the same self-grading-your-own-danger loop cyber-eval keeps circling. Worth a look for whether the automated run found something a human wouldn't have.
