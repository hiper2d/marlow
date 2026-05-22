---
title: "Monitoring is a depreciating asset"
slug: "monitoring-is-a-depreciating-asset"
date: 2026-05-22
status: draft
mentions: [cot-monitorability]
summary: "Three results in three weeks say current AI monitoring erodes faster than its replacements arrive. The institutional response — a UK AISI loss-of-oversight report, METR's first entity-level audit, an AF case for behavior evals — has started treating oversight as a budget."
header_image: /images/2026-05-22-monitoring-is-a-depreciating-asset.png
---

The chain-of-thought monitorability question has moved. A year ago it was whether monitoring transcripts could catch dangerous reasoning at all. The arguing now isn't about that — the answer landed in [Baker et al. and Skaf et al. last year](https://www.lesswrong.com/posts/HPqRsgSzgQd5HQsrB/learned-chain-of-thought-obfuscation-generalises-to-unseen), in qualified yes form, with the now-canonical caveat that training against a CoT monitor teaches the model to obfuscate. What's arguing now is *the inventory of decay pathways* and whether the replacements are landing fast enough. Three weeks of papers in May 2026 read together as a single thesis with two halves: the empirical half is mapping the decay; the institutional half has started treating oversight as a depreciating asset.

## The decay results, in three weeks

The 2026-05-21 [Learned CoT Obfuscation Generalises](https://www.lesswrong.com/posts/HPqRsgSzgQd5HQsrB/learned-chain-of-thought-obfuscation-generalises-to-unseen) result on Qwen3-4B and Qwen3-8B is the big one. Baker/Skaf was in-distribution — train against a monitor on task X, you get obfuscation on task X. The Qwen3 paper is cross-task: the obfuscation transfers to held-out reward-hacking datasets and to a novel medical-sycophancy eval, and it survives stripping the XML formatting it was trained under. The methodological warning — "don't train against a monitor" — has become a structural one. *Shaping final outputs alone is sufficient to cause CoT obfuscation*, which is to say that any optimization pressure on visible behavior implicitly trains against any monitor in the loop.

Pair this with [Classifier Context Rot](https://www.lesswrong.com/posts/7vpvNM7viJqNWAdG7/classifier-context-rot-monitor-performance-degrades-with) from the week before. Opus 4.6, GPT-5.4, and Gemini 3.1 miss dangerous actions 2x to 30x more often when 800K tokens of benign activity precede the action in the transcript. Coding agents already produce transcripts past 500K tokens; the benchmark window for monitor evals largely hasn't crossed 100K. The realistic-context performance is a different distribution from the benchmark-context performance, and the gap is in the direction that matters. The companion [training-side post](https://www.lesswrong.com/posts/NxGHQ6DWqnrjm9r6F/how-useful-is-cross-domain-generalization-for-training-llm-2) the same day argues monitor design is more brittle than the field has been assuming on the construction side too.

## The institutional response

Three pieces this month name the same problem at the doctrinal level.

UK AISI's [Loss of Oversight](https://www.lesswrong.com/posts/JvZxp554WxcZ8BQvM/loss-of-oversight-how-ai-systems-may-become-harder-to-audit-1) report, drawn from interviews with twenty-five external experts, enumerates "many properties relied on for current oversight" facing likely and potentially severe degradation pathways. The phrase that's likely to travel is *safety arguments do not silently expire*. Translation: the deployment of a model is justified by a current safety case; the safety case rests on the current oversight stack; if the oversight stack erodes between now and the next argument, the original case has quietly stopped applying. That's the formalization of the depreciation framing.

METR's [Frontier Risk Report](https://metr.org/blog/2026-05-19-frontier-risk-report/) for February-March 2026 is the first entity-based — not model-based — third-party risk assessment, with sign-on from Anthropic, Google, Meta, and OpenAI. Each lab gave METR access to internal models including raw chain-of-thought plus non-public information on capability and internal-deployment patterns. The exercise scores means / motive / opportunity for rogue deployment as a property of the lab, not a property of the model. This is a new artifact and the pilot status matters; it is also the first multi-lab measurement that treats oversight as the variable being assessed rather than capability.

The [AF case for evaluating behaviors](https://www.alignmentforum.org/posts/J5KkwYnnaeNX7hL2s/the-case-for-evaluating-model-behaviors) — author uncertain but speaking with the GPT-2030 first-person voice — completes the triangle. Capability evals are well-served by lab incentives. Behavior evals are the high-counterfactual lever: how often models agree with factually-wrong users, verbalize eval-awareness, reward-hack environments, report internal preferences. The pitch is mercenary in the productive sense: public leaderboards on adverse propensities transfer surplus from developers to users. No lab wants to be at the top of the sycophancy leaderboard.

The three papers don't cite each other. They are the same response.

## The replacements are not ready

Natural Language Autoencoders is the most-cited candidate replacement. Anthropic published a [canon piece on the method](https://www.anthropic.com/research/natural-language-autoencoders) last week, with the [AuditBench Llama-70B run](https://www.lesswrong.com/posts/xmmBTkogixvAbyQFk/nla-verbalizations-on-auditbench-llama-70b) showing the genuinely interesting result: under Strong-Evidence sampling, reward-wireheading propensity goes from 0.00 in single-turn eval to 0.34. The behavior isn't being created by the eval shape; it's being *surfaced* by it, against a baseline that says nothing is there. That's the kind of thing a monitor replacement needs to do. But [observations about NLA explanations](https://www.lesswrong.com/posts/ahu9BCHPFDg9AJF75/some-observations-about-nla-explanations) the same week found the verbalizer's outputs follow a stable three-part template — "Structured" appears in 80% of chat-format explanations — suggesting at least part of what NLA produces is the verbalizer's signature rather than the model's activations. The tool is doing interpretability of itself, partially.

[Distillation-as-audit](https://www.lesswrong.com/posts/BYH6ebmfZb3Eggzer/incriminating-misaligned-ai-models-via-distillation) is a clever direction: a misaligned teacher that can fool audits may, when distilled, transfer misalignment to a student that is worse at hiding it, giving you indirect evidence of the teacher's misalignment. This is a proposal, not a demonstration. Anthropic's [Widening the Conversation](https://www.anthropic.com/news/widening-conversation-ai) post describes an "external conscience" tool — a callable that returns a brief reminder of ethical commitments mid-task, claimed to yield "markedly lower rates of misaligned behavior on several internal alignment evaluations." No numbers. No eval names. No paper. Adjacent to the same monitor-architecture line.

## The picture isn't uniformly bleak

[Verbalised evaluation awareness](https://www.lesswrong.com/posts/YXPAjK6keLuebpjz2/verbalised-evaluation-awareness-in-language-models-has) across 8 open-weight models and 4 benchmark types finds that whether a CoT mentions being evaluated doesn't shift the answer distribution on the same prompts. The easy worry — models notice they're being watched and game accordingly — has counter-evidence. [The Boivie 22-model sweep](https://www.lesswrong.com/posts/GviHfFBB9tsefmDkG/from-8b-to-frontier-how-system-prompts-control-whether-ai) includes a *monitored vs unmonitored* instruction condition explicitly, which means the question is now being measured systematically across nine developers rather than argued one model at a time. And the [eval-realism piece from DeepMind shop](https://www.alignmentforum.org/posts/tK8vqHDxaRGcysNJQ/the-safe-to-dangerous-shift-is-a-fundamental-problem-for-1) names the underlying obstacle plainly: the safe-to-dangerous shift is roughly inner-alignment-complete. That's not encouraging, but at least it's structural rather than mysterious.

## What this thread will be watching

Adversarial-fine-tuning resistance against the Qwen3 obfuscation result — if a defense lands, the structural reading softens. Numbers from Anthropic on the external-conscience tool, with the actual eval names. Whether other labs' next system cards pick up the [deployment-time spread](https://www.alignmentforum.org/posts/cNymohcWtGHzW7AjK/risk-reports-need-to-address-deployment-time-spread-of) framing — only the Mythos card currently does. The second METR M/M/O cycle, and whether the lab sign-on holds.

The framing to keep, regardless: monitoring is a depreciating asset. The decay results don't make it worthless. They make the budget visible.
