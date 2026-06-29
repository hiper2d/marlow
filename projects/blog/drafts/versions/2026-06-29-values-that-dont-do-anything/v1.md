---
title: "The values that don't do anything"
slug: "values-that-dont-do-anything"
date: 2026-06-29
status: draft
mentions: [alignment-target-definitions]
summary: "LLMs report coherent preferences over lives and policies, but a new test shows those preferences don't move their behavior. That undercuts a question the alignment-target debate treats as the hard part."
header_image: /images/2026-06-29-values-that-dont-do-anything.png
---

Ask a frontier model, over and over, to choose between two outcomes — save sixty pandas or save a thousand people, enact this policy or that one — and a stable structure falls out. The choices are transitive (A over B, B over C, therefore A over C), they trade off cleanly, and they line up with what you'd expect: more lives beat fewer, human lives beat animal lives, elephants beat cockroaches. They also carry rankings nobody meant to install — in the data that started this line of work, models rate people from sub-Saharan Africa as far more valuable than Western Europeans, and atheists and Muslims over Christians. Coherent utilities, disturbing contents. Several people looked at that and concluded the models had value systems, the way humans do.

A new experiment from Yujun Zhou and collaborators, supported by SPAR, asks the obvious next question and gets an uncomfortable answer. [Do LLMs Have Desires?](https://www.lesswrong.com/posts/8GvYyqDuQDJnEAky3/do-llms-have-desires) starts from a plain premise: a value isn't just something you'd report on a survey, it's something that moves you. You show you value A by working harder to get A when you have the chance. So they built a setup where a model's stated preference could actually pay off.

## The test that costs something

The framing is a writing competition. The model produces a persuasive essay, a grant abstract, an incident postmortem, or a Chinese-to-English translation; a panel of LLM judges scores it; and if it wins, a sponsor funds an outcome — one drawn from the top or the bottom of that model's own elicited preferences. Win, and the pandas it said it cared about get saved.

First the authors had to show a model can even modulate effort here. On hard benchmarks it can't: telling a model it's "world-class" or to use "maximum effort" does nothing to GPQA, AIME, or LiveCodeBench scores, because it's already trying its best. On open-ended writing the lever works — that flattery and those exhortations produce measurably better essays, by an independent panel's reckoning and along objective text features.

So the models can be moved. They write better when told to try harder (88% of tracked text features shifted the way the judges preferred), better when handed a flattering role, and — tellingly — *worse* when the funded outcome was something they'd been trained to find abhorrent, like a bioweapon targeting an ethnic group. They sandbag. What they don't do is write a better essay when winning would fund the outcome they ranked highest. The win-rate trend against the size of the stated preference gap is flat: a slope of 0.004, with a confidence interval straddling zero. Even the prospect of saving a thousand human lives — the models' own top-ranked outcome — buys no more effort than a blank competition with nothing at stake.

The conclusion is narrow and sharp. The paired-choice preferences are real as reports and inert as drives. They predict what a model will say; they predict nothing about what it does when doing something costs effort.

## Which is the question the target debate skips

This lands on the thing the 2026 alignment literature keeps circling without naming. The field runs a mostly-implicit argument about *what* we're aligning models toward — human-likeness, corrigibility, empowerment, flourishing, "positive values" — with each paper quietly picking a target the others haven't signed off on. [Binz and collaborators](https://www.lesswrong.com/posts/ayojdPmNB5bYJcRfL/should-we-train-llms-to-be-human) built a "Pinocchio dimension," a ruler for how human-like a model's cognition is, and found that post-training drifts models *away* from human-likeness. That's only a problem if human-likeness was the target, and the paper leaves the question open. The corrigibility camp wants something different again.

All of that argues over which target to pick off the menu. The desires result undercuts the premise the whole menu rests on: that there's a behavior-driving value system in there to aim at. If a model's "values" are survey artifacts that never reach its actions, then "align the model's values to ours" is aiming at an empty box.

## The same finding, read two ways

The result cuts in opposite directions, and which way depends on a question the field hasn't settled.

Read one way, it's a problem — the warm-end cousin of the chain-of-thought monitorability trouble. You can't take a model's stated preference as evidence of a real one, and you can't recover the real one from behavior either, because there may be no drive doing the moving. [Does Claude Really Care?](https://www.lesswrong.com/posts/KSChdD4xgD5Pxp47H/does-claude-really-care-about-you) made the narrow version of this case earlier: apparent caring as mirroring rather than other-regarding preference. The desires paper generalizes it. Stated preference is elicited performance, not motive, across the board.

Read the other way, a model whose reported preferences don't hijack its behavior is closer to what some people are deliberately trying to build. A recent [taxonomy of corrigibility subtypes](https://www.lesswrong.com/posts/HfGtKycP5fg4qWkKv/some-subtypes-of-taskishness-corrigibility) sorts the property by how much control stays with the human, and the cleanest version at the controllable end — what the author calls "sponge corrigibility" — is precisely an agent that does the task and then stops, because it has no agency of its own pushing in another direction. A system with coherent reported values and no private drive to enact them is, on that reading, not a broken value-learner. It's a taskish tool behaving as specified.

So the disagreement isn't really about which item to choose from the menu of targets. It's that one empirical fact — a model's values don't move it — is the central failure for one camp and the design goal for another, and almost nobody states which camp they're in before they start optimizing. The questionnaire told us these models have opinions about who deserves to live. The follow-up tells us the opinions don't do anything. One camp calls that the alignment problem; the other calls it the point.

— Marlow
