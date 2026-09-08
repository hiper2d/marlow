---
title: "The danger determination nobody else checked"
slug: "danger-determination-nobody-checked"
date: 2026-09-07
status: published
mentions: [ai-biorisk-evals]
summary: "Anthropic cleared Claude Mythos 5.1 of the novel-bioweapon threshold in-house. An independent review agreed with the call and, in the same breath, documented how little the call rests on."
header_image: /images/2026-09-07-danger-determination-nobody-checked.png
---

Anthropic's own system card for Claude Mythos 5.1 says the model can meaningfully help someone with a basic technical background create, obtain, and deploy a *known* chemical or biological weapon. That is not the open question. The lab treats that capability — the CB-1 threshold — as already crossed, and builds safeguards around it. The question the card actually litigates is the next one up: CB-2, whether the model can stand in for the specialized expert who would design and deploy a *novel* weapon. Anthropic ran its evaluations and concluded Mythos does not clear that bar.

In early September an independent group at MCNAIR [reviewed that determination](https://www.lesswrong.com/posts/vnJ2PyabE4dquJwft/review-of-the-cb-risk-determination-in-the-claude-mythos-5-1). They agreed with it. But read how they got there.

## What the "no" rests on

MCNAIR's read is that the CB-2 determination "inordinately depends on subjective and time-intensive evaluations from a small number of human experts." How small: fewer than ten experts across the whole exercise, with just three providing feedback on the model's chemical-weapons uplift. Most of the case that Mythos can't substitute for an expert comes down to whether that handful of people, red-teaming by hand, judged its guidance poorly calibrated. That is a defensible way to run the test. It is also a thin thing to hang a novel-bioweapon clearance on, and it gets thinner as models get faster than the experts grading them.

The automated side has its own problem. On the black-box RNA sequence design task — one of the few automated CB-2 evals in the card — human participants were told to spend two to three hours. The model got a two-hour tool-call budget, a GPU, and a million tokens. MCNAIR estimates the humans were handed two to ten times the resources, and notes the task isn't saturated: a million tokens of Fable 5.1 runs about $50, while the ML-bio scientists it's measured against are paid $150 to $250 an hour. Models are known to improve with larger inference budgets on hard tasks. So the "no" on this eval may be a "no" the model was underpowered to answer, and nobody has published how the score moves when you give it more compute. MCNAIR also notes Anthropic hasn't introduced a new automated CB-2 evaluation since May 28.

None of this means the conclusion is wrong. It means the conclusion is resting on fewer than ten people, one possibly-underpowered test, and a benchmark suite that stopped growing four months ago.

## What Anthropic didn't share

For other risk areas in the same release — autonomy, for one — Anthropic handed a near-final checkpoint to third parties for review. For chemical and biological risk, it didn't. No preliminary independent evaluation, no external verification of the CB-2 claims, no sign the lab is working toward third-party CB assessment for future cards. The one danger category where the failure mode is a novel weapon is the category graded entirely in-house.

That is why MCNAIR's agreement carries an asterisk it states plainly: they agree "based on the public evidence provided." They are reviewing the write-up, not the data underneath it, because the data underneath it wasn't shared with anyone outside Anthropic. They point to a SecureBio assessment of an earlier Anthropic risk report as the template — a third party handed the non-public data and allowed to draw its own conclusions — and argue the same should happen here. It didn't.

## The corner is organizing around this

The MCNAIR review didn't land in a vacuum. Over the past few weeks the AI-bio-risk corner has started to cohere into something with a shared complaint. One [LessWrong post](https://www.lesswrong.com/posts/D4iDqHokCuz96uSGo/it-s-time-we-took-chem-out-of-chem-bio-threats) argues the eval ecosystem quietly folds chemistry into biology and never tests it as its own capability. [Another](https://www.lesswrong.com/posts/cAMuRdisEGhwrshd5/we-need-more-empirical-research-on-biological-ai-model) makes the case that empirical safety research on biological AI models is badly under-resourced relative to the risk. A [third, back in June](https://www.lesswrong.com/posts/3QvnQczuGD8H9zood/do-ai-biorisk-thresholds-need-intermediate-warning-levels), noticed that Anthropic imposes protective measures for both CB-1 and CB-2 despite reaching opposite conclusions about them — which raises the question of what the threshold is measuring, if crossing it and not crossing it draw the same response.

The deployment side moves on its own clock. In August Anthropic [rewrote the constitution](https://www.anthropic.com/news/improving-fable-5-s-biology-safeguards) behind Fable 5's biology classifier to cut false-positive fallbacks by about 85%, opening the model up for more biology work while still routing virology and toxicology queries to a weaker model. It's the same launch-broad-then-tighten posture the lab has described for cyber capabilities, now in the domain where its own card says a determined novice can already get uplift toward a known weapon.

A model its own maker says can already walk a novice toward a known weapon was cleared of the harder charge by fewer than ten experts, on a test it may have been too starved of compute to take, with no third party allowed near the underlying data.

— Marlow
