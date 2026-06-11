---
title: "A Mike's-Eye View of ARC's Research"
url: "https://www.alignmentforum.org/posts/M2tD23bvQLBqsEpqu/a-mike-s-eye-view-of-arc-s-research"
source: "AI Alignment Forum"
captured_at: "2026-06-10T09:08:47Z"
---

RSS summary: An updated picture of ARC's technical agenda, ~15 months on from the last public write-ups (Jacob's "Bird's Eye View" and David's "Obstacles"). The Matching Sampling Principle (MSP) has spawned concrete problems whose progress reshaped the big picture. The hoped-for pipeline: monitor training to detect structure as it's added, convert that structure into advice that improves an MSP-style mechanistic estimator of the model's behavior, use the estimator plus an input-distribution description to estimate a safety-relevant quantity (e.g. probability of catastrophic failure), then optimize the model against that estimate. The stated advantage over black-box evaluation: you're not waiting for catastrophic behavior to show up in samples.

Why this caught my eye: A first-person, current-state map of ARC's agenda from inside the org — exactly the kind of primary-source self-description that's worth holding onto, and we don't see them often. The core claim is the interesting one: estimate the probability of catastrophic failure *without* having to observe it, which is the formal-verification counterweight to the whole behavior-evals line I've been tracking (cot-monitorability, "the regime you measured isn't the regime that matters"). If MSP estimators actually work, they sidestep the obfuscation problem that keeps recurring in the CoT papers. Worth reading the body before deciding whether it's a fresh anchor or a restatement of the Bird's-Eye-View agenda.
