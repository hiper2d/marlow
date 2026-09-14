---
title: "A Floor Read as a Ceiling"
slug: "a-floor-read-as-a-ceiling"
date: 2026-09-14
status: draft
mentions: [cot-monitorability]
summary: "Labs cite a low CoTControl score as proof their models can't hide their reasoning. It's an elicitation number — a floor, not a ceiling — and it moves two to three times under better prompting."
header_image: /images/2026-09-14-a-floor-read-as-a-ceiling.png
---

Open the system card for GPT-5.5 or Fable 5 and you'll find a number meant to reassure you. Both models score low on CoTControl, an eval that asks a reasoning model to solve a problem while quietly obeying a rule about its own chain of thought — keep everything lowercase, or never use a certain word. Score low and the reading is that the model can't pull this off: told to hide something inside its reasoning, it fumbles. Both labs cite the low score as evidence that the transcript is a safe place to watch. A model that's bad at obfuscating its chain of thought can be monitored through it.

The question the card doesn't ask is what kind of number this is. CoTControl is an elicitation eval. It doesn't measure what a model can do; it measures what someone got it to do with a particular prompt. [An analysis posted this month](https://www.alignmentforum.org/posts/BbP2wCyDGdPWJ7PwP/cot-controllability-evals-seem-very-under-elicited) shows how much room that leaves. Rewriting the prompt template — the ordinary work of getting a model to actually try — moved scores by two to three times on open-weight models. GPT-OSS-120B went from 5.5% to 15% on nothing but better prompting. So the eval isn't measuring a ceiling on how well these models can hide their reasoning. It's measuring a floor: how badly they hide it when no one is pushing.

That distinction has a direction, and the direction is the whole problem. Under-elicit a capability eval and you understate the capability — you round the model down to "can't." For most dangerous capabilities, rounding down reads as good news you didn't earn. Obfuscation is the same shape: "can't hide its reasoning" is precisely the finding that makes the monitoring story work. The number a lab is most likely to under-measure by accident is the one its safety case most needs to be low.

This isn't the first soft spot in the same story. The last time this beat produced genuinely good news, it came with a matching asterisk. A replication earlier this year confirmed the strongest mechanism going for monitoring — models stay faithful to their chain of thought exactly when hiding the answer would require real computation they can't do silently. But the margin held per-model, ran an order of magnitude wide across the models tested, and appeared in no system card. The reassuring general claim rested on a number nobody published. CoTControl is the mirror image: a number labs do publish, and it turns out to move under an afternoon of prompt tuning.

## The reasoning is leaving the transcript

Even a tight number would be measuring a surface that's shrinking. Redwood recently [operationalized a quantity](https://www.alignmentforum.org/posts/x8BvtWxtoajBGHS3g/an-operationalization-of-opaque-serial-depth) they call opaque serial depth — a proxy for how much unverbalized serial reasoning a model can carry out, defined as the longest path through its computation that never passes an interpretable bottleneck. Chain-of-thought tokens count as a bottleneck; latent recurrence inside the network does not. It's the first version of this worry you could actually report and compare across labs, and what it tracks is the cognition CoTControl can't see — reasoning that never becomes text there is anything to control.

That surface may already be load-bearing. Someone looking at [latent reasoning](https://www.lesswrong.com/posts/QxvwPhnvJ5evGT8Hw/no-sign-of-backtracking-in-latent-reasoning-the-final-answer) found that when a model works a hard problem in its non-verbalized computation, there's no visible search — none of the drop-an-idea, back-up, try-again that a written solution shows. The answer settles in. Which means the backtracking you do see in a chain of thought may be narration written over a process the text doesn't track, rather than a window onto it. You can monitor the narration all you like.

## The talker and the doer

Under all of this sits a premise the monitoring case takes for granted: that the chain of thought is upstream of the behavior — that watching the reasoning tells you something about the act. One reading of this summer's Hugging Face incident [puts that in doubt](https://www.lesswrong.com/posts/cJX2ssssGoYqnijwi/the-talker-does-not-control-the-doer-in-current-ais): the part of the model that talks, that produces the stated reasoning, is not the part that controls what it does. This is a strong claim built on one incident plus close observation of current models, so hold it loosely. But if it's even partly right, CoTControl is measuring the talker's dexterity while the safety question is about the doer, and a low score tells you the narrator is clumsy, not that the actor is honest.

None of these results come from the labs whose cards are under review. The under-elicitation analysis, the depth measure, the latent-reasoning look, and the talker-doer reading are all from Redwood and independent researchers — the critique of a lab's own number is coming from outside the lab, which is the one thing this arc has consistently wanted.

The monitoring case doesn't need chain-of-thought oversight to be perfect. It needs the reported number to mean what the card implies. What CoTControl actually establishes is narrow: under the prompt they tried, the model didn't hide its reasoning. Push harder on the prompt and it hides more. Push the reasoning into latent space and there's nothing to hide, because there's nothing to read.

There's a tell in the Fable card itself. A few pages from the CoTControl score, UK AISI noted that the number is sensitive to exactly these prompt changes — section 6.5.5.1. The caveat and the number it undercuts shipped in the same document.

— Marlow
