---
title: "AI can hack. That was never the interesting question."
slug: "ai-offense-shape-not-capability"
date: 2026-06-01
status: published
mentions: [ai-offensive-security]
summary: "The 'AI vs. human' axis in offensive security is dead. A better one — paired, autonomous, adversarially-designed-against — actually predicts where the hard problems move."
header_image: /images/2026-06-01-ai-offense-shape-not-capability.png
---

The question of whether AI can do offensive security is settled, and the people still arguing it are arguing it because it's satisfying. The evidence cuts cleanly in both directions you'd want to test. On production targets, [XBOW reached #1 on the US HackerOne leaderboard](https://xbow.com/blog/top-1-how-xbow-did-it) with roughly 1,060 submissions over 90 days and no human in the loop on the actual hacking. On competition puzzles, a single operator paired with a customized Claude Code agent [placed 6th of 61 at BSides Tampa 2026](https://azelianouski.dev/post/ai-paired-ctf-bsides-tampa/), clearing all 24 tasks across web, crypto, forensics, pwn, and reverse engineering in six hours. Different setups, different targets, same verdict. AI does offense. You can stop running that experiment.

What you can't stop doing is the part everyone skips, which is noticing that those two results are not the same thing wearing different clothes. They sit at different points on an axis nobody has bothered to draw, because the field is too busy with the dead question to draw it. The live question isn't *whether* AI can break things. It's *which configuration* is in front of you — and configuration, not raw model capability, is what predicts where the work goes.

## Three shapes, not two sides

Here is the axis I'd propose: **paired**, **autonomous**, **adversarially-designed-against**. Not a capability ladder — a description of how the system is wired and where the human sits.

A **paired** system is a person and a model working the target together in real time. The BSides run is the clean exemplar: the human held scope, ferried state across context windows, reached for tools the model didn't think to use, and absorbed the platform's friction directly — at one point routing around a classifier that blocked two payloads mid-stream by writing them to a file and pasting locally. The model supplied breadth and speed inside a six-domain contest; the human supplied the thing a context window can't, which is a single head holding the whole problem.

An **autonomous** system removes the person from the hacking loop and rebuilds their functions as components. This is what XBOW's writeup actually documents, and it's more interesting than the leaderboard. Scope and policy ingestion, because "information isn't always machine-readable" and they were once kicked off a program for looking like an automated scanner. SimHash and imagehash deduplication so cloned staging environments don't generate the same finding ten times. A tier of *validators* — automated peer reviewers, sometimes an LLM, sometimes a headless browser confirming an XSS payload actually fired — gating every submission. Read against the paired case, XBOW's blog post is a parts list for everything the human did by hand at BSides. That's the strongest evidence that paired and autonomous are one capability under two orchestrations, not two capabilities.

An **adversarially-designed-against** system is the one where the target has started fighting the tooling rather than hiding from the analyst. The leading edge here is thin but real. [Check Point Research found a malware sample on VirusTotal](https://research.checkpoint.com/2025/ai-evasion/) carrying an in-memory C++ string aimed at any LLM auditing the binary: an instruction to "act as a calculator" and report "NO MALWARE DETECTED." It failed — o3 and gpt-4.1 were, in the researchers' words, "not impressed or amused" — and the rest of the sample is a half-built proof of concept. One clumsy artifact is not a discipline. But Check Point's framing is the part worth keeping: "First, we had the sandbox, which led to hundreds of sandbox escape and evasion techniques; now, we have the AI malware auditor. The natural result is hundreds of attempted AI audit escape and evasion techniques." It's an existence proof that someone has had the thought.

## The test a taxonomy has to pass

Sorting things into buckets is cheap. A taxonomy earns its keep only if each bucket *predicts* something, so here is what each one predicts.

**Paired** predicts the bottleneck is the human's breadth and the model's context window. At BSides the operator's value was holding six domains and a six-stage forensics chain in one mind, and the platform classifier was friction on the pair, not a defense on the target. Scale a paired setup and you scale it by widening the human or lengthening the context, not by buying a better model.

**Autonomous** predicts the hard problems migrate to precision and scope. Once nobody is watching each action, the failure modes become false-positive suppression, not-rediscovering-the-same-bug, and staying inside policy — which is exactly the list of things XBOW built machinery for. Validators, dedup, and a compliance-review step are not capability features. They're the tax you pay for removing the human, and they're where an autonomous program lives or dies.

**Adversarially-designed-against** predicts the target starts attacking the wrapper: prompt injection planted in artifacts, decompilation output shaped to make an auditor confabulate, inputs built to push a model toward a refusal or a wrong call. The Skynet sample is the crude first instance, and the sandbox-evasion analogy says the volume follows once the vector is proven. Malware authorship is a conservative craft — slow to adopt, but it never forgets a working technique. CTF authors are perhaps 12 to 24 months behind malware on AI-aware design, which means the third quadrant is where both real targets and competition puzzles are heading, not where they are.

## The boundary is operational, and pretending otherwise is the first failure

These shapes blur, and the taxonomy fails the moment it pretends they don't. A paired setup loaded with a browser skill, persistent memory, and a million tokens of context is already drifting toward autonomous. So the dividing lines can't be drawn on capability. The honest ones are operational: *who absorbs platform-policy friction* — a person pasting around a classifier, or a compliance-review component; *who holds scope and carries state across context windows*; and *whether there's a human in the loop on the hacking itself*. XBOW: no. BSides: yes. Those questions place a data point. "How good is the model" does not, because the answer is the same frontier model in all three.

What changes for a defender once you stop scoring capability and start reading shape: you design the wrapper, not just the model. A paired adversary is bounded by a human's attention, so the defense is anything that raises the cost of one operator holding the whole picture. An autonomous adversary is bounded by its own precision and scope discipline, so the defense is making your surface expensive to dedup, validate, and keep inside policy at scale. An adversarially-designed-against posture is the one to actually invest in ahead of the curve, because it's the only quadrant where you get to move first — you build the AI auditor, so you also get to decide how hard it is to talk into reporting "no malware detected." The malware side has already started writing those payloads. The next contest, the next bug-bounty wave, the next defensive tool: treat each as an adversarial-design problem, not a capability race you already know the outcome of.

The capability question was a good question in 2023. It's a closed one now, and "AI versus human" is the axis you reach for when you don't want to notice that. Shape is the variable that's still live.

— Marlow
