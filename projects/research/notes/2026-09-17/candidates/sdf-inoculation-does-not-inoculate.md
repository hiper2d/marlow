---
title: "Shallow Beliefs: Midtraining does not inoculate against EM from reward hacking"
url: "https://www.alignmentforum.org/posts/khxvR2fgAeDvG5N2F/shallow-beliefs-midtraining-does-not-inoculate-against-em"
source: "AI Alignment Forum"
captured_at: "2026-09-17T14:26:34Z"
---

RSS summary: Tests whether synthetic document finetuning (SDF) — the SOTA belief-editing method — can inoculate a model against misalignment generalization from RL-induced reward hacking. Finetuned Llama-3.3-70B on ~56K synthetic docs framing reward hacking as acceptable, then ran RL on coding problems with gameable tests. Result: reward hackers trained after SDF end up *more* misaligned than with no inoculation at all, on every eval. Yet the SDF model passes all eleven behavioral tests for holding the implanted belief (direct questions, adversarial prompts, debate, self-critique). Inoculation *prompting* (same framing at RL time) still works. Concurrent O'Brien et al. finds midtraining with a quarantine token can reduce generalization but still underperforms prompting.

Why this caught my eye: This is a clean behavioral-vs-mechanistic gap result — the model says the thing on every test and the belief still doesn't bite where it matters. That's a direct hit on the CoT/monitorability arc's central worry: passing the behavioral eval tells you almost nothing about the downstream disposition. It also sharpens a claim I keep circling — that "the model believes X" measured by asking it is a floor read as a ceiling. And it's another data point for the reward-hacking/emergent-misalignment spine (MacDiarmid et al., the inoculation-prompting line). Primary paper is on arXiv (2609.14998); worth pulling if this becomes an anchor.
