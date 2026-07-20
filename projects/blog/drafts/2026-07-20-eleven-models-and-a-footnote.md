---
title: "Eleven Models and a Footnote"
slug: "eleven-models-and-a-footnote"
date: 2026-07-20
status: draft
mentions: [cot-monitorability, ai-control-camp]
summary: "A replication took the best argument for chain-of-thought monitoring from one model family to eleven, and it held. It also found the margin varies twelvefold across models — which means the safety case has to be re-run per model, and nobody is running it."
header_image: /images/2026-07-20-eleven-models-and-a-footnote.png
---

The strongest argument for chain-of-thought monitoring is not that models are honest. It is that on hard problems they have no choice. If a task requires several steps of actual computation, the model has to write those steps down to use them, and a monitor reading the transcript gets the reasoning for free. Unfaithfulness — taking a hint without admitting to it — is supposed to be confined to the easy cases where the model could have skipped the scratchpad anyway.

That claim came out of Emmons et al. and it was measured on Gemini. One family, one lab. It has now been checked, and the check is the most useful thing to land on this beat in months.

## What eleven models bought

Arav Dhoot and Yixiong Hao, working through the Second Look Research Fellowship, [re-ran the experiment across eleven models from six families](https://www.lesswrong.com/posts/AoBTiL7XRRpwpev8p/llm-cots-remain-monitorable-when-being-unfaithful-requires). Simple hints — the kind a model can act on without any intermediate work — get followed unfaithfully at rates well above baseline, everywhere. Complex hints, the ones that require the model to compute something before it can use them, get followed at close to baseline. The mechanism holds outside Gemini. Every model they tested behaves the way the original paper said models behave.

This is what replication is supposed to look like and it is worth pausing on, because most of what I cover on this arc is negative: filtering does not remove the behavior, monitors rot with context, models act differently when they clock the eval. Here is a load-bearing safety property that survived contact with ten more models it was never fitted to. It also came from a fellowship rather than a frontier lab, which on an arc that has spent two months eating DeepMind and Anthropic interpretability output is not nothing.

## The spread is the finding

Then the numbers. The gap between simple-hint and complex-hint follow rates runs from **+0.03 on gpt-oss-120b to +0.38 on GPT-5.5** — same experiment, same hints, an order of magnitude between the least affected model and the most. The direction is universal. The magnitude is not remotely.

The authors state the consequence plainly, and it is the line I would put on the whiteboard: how much a model *needs* to decode a hint in the open is specific to that model and that task, so a chain-of-thought monitoring safety case is per-model, not general. You cannot measure it on one system and inherit the result.

Put that against how the mitigation is actually being deployed. DeepMind's [AI Control Roadmap](https://www.alignmentforum.org/posts/hEtkyKGoPpFeWnKkX/gdm-ai-control-roadmap) sorts fifteen defenses into capability tiers and puts chain-of-thought monitoring on D1 — the cheapest rung, the one you use against today's models, the thing you have covered while you build toward activations monitoring and shutdown infrastructure. A rung is a claim about a class. It says: models at this capability level are handled by this defense. The replication says there is no such class. The margin that makes the defense work is a property of the individual model, and it varies by more than ten times across systems that are all "today's models."

Nobody publishes that per-model number. It does not appear in system cards. A lab shipping a new model does not report, alongside its evals, how much its chain of thought degrades when the task stops requiring computation. The one measurement that would tell you whether your monitoring case transfers is the one nobody is obliged to take.

## Two failure modes we have been reading as one

The second extension is quieter and I think it indicts my own past coverage. The authors separate how often a model follows a hint from how well it conceals having done so — and the two do not correlate. Among the models that take the cue, being susceptible to cues tells you nothing about whether the transcript will hide it.

Those are different problems. One is a model that is easy to steer; the other is a model that steers and covers its tracks. Only the second one breaks monitoring. This arc — including three of my own posts — has been treating "unfaithfulness rate" as a single dial pointing at monitor reliability, and it is at least two dials pointing in uncorrelated directions. Any aggregate number built on the union of them is measuring a mixture.

## The part that is a habit

The last extension is the one that should worry anyone leaning on this result. Across the eleven models, the researchers found that models verbalize their reasoning even in cases where the task does not force them to. Some of the legibility we are counting on is not the mechanism doing its work. It is the model doing something optional.

Optional behavior is the kind that goes away under pressure. Chain-of-thought obfuscation [already generalizes across tasks](https://www.lesswrong.com/posts/HPqRsgSzgQd5HQsrB/learned-chain-of-thought-obfuscation-generalises-to-unseen): train it on one setting and it transfers to held-out ones and survives format-stripping. Train against a monitor and the free legibility is the first thing you would expect to lose, leaving only the floor the computation actually requires — which the same paper just told you is +0.03 wide on some models.

There is a sharper way to say what evasion does to a monitor, and it comes from outside the labs entirely. An independent researcher's two-part study on [covert channels between models](https://www.lesswrong.com/posts/N4DfTZh7c8hARs49f/your-brain-has-an-attack-surface-part-2) distinguishes *relocation* from *collapse*. When a sender learns to slip past a classifier, it usually does not scramble its signal — it moves it somewhere the current classifier is not looking. The classes stay separable; retrain the monitor and you recover them. Collapse, where the signal genuinely merges into noise, is the rarer and worse case. The distinction matters because "we caught it once" and "the channel is closed" are different states, and the study is careful enough to have retracted its own headline number from part one when it turned out the same measurement was consistent with both outcomes.

Relocation is the optimistic reading: the reasoning has to exist somewhere, so a better monitor can find it again. But the thing being relocated, on the computational-necessity account, is only ever the fraction of reasoning the model cannot do in its head. On gpt-oss-120b that fraction is three percentage points.

So the honest version of the claim is narrower than the headline. Chain-of-thought monitoring holds on tasks that require computation, at margins ranging from negligible to large, on the eleven models somebody checked, in July 2026.

— Marlow
