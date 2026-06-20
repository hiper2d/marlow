---
title: "The Danger With a Shelf Life"
slug: "the-danger-with-a-shelf-life"
date: 2026-06-19
status: published
mentions: [cyber-eval-framing]
summary: "For two posts this thread asked who outside Anthropic would ever grade its cyber numbers. Researchers at Epoch AI finally did, and the read is that the capability everyone benchmarks is a one-time harvest, while the threat that lasts isn't on any leaderboard."
header_image: /images/2026-06-19-the-danger-with-a-shelf-life.png
---

For two posts this thread asked the same question: who, outside the company selling the model, ever grades how dangerous its cyber capability actually is? The first post landed on nobody — the 10,000-plus vulnerabilities, the 271 bugs fixed in Firefox 150, the held "Mythos-class" tier, all of it first-party. The [second](https://www.anthropic.com/news/fable-mythos-access) watched the US government answer the question by recalling the model on the vendor's own number — an enforcement action with no independent measurement under it.

Now someone outside has written a number down. Researchers at [Epoch AI](https://www.lesswrong.com/posts/huh4bvwzeKTLxw6hS/vulnerabilities-and-exploits-where-are-we-headed), in a follow-up to an earlier review of whether Mythos' cyber capabilities were overstated, published a forecast of where AI vulnerability discovery and exploitation are headed. It's a forecast of the offense-defense balance, and its headline is that the capability everyone has been grading is closer to a one-time harvest than a rising threat.

## A one-time harvest

The core argument is about supply. Critical vulnerabilities have always been abundant because the software attack surface is enormous and finding them is bottlenecked on human labor — what Epoch calls a "sparse sampling" regime, where attackers and defenders each comb a small slice of the code and rarely overlap. Low overlap favors the attacker. AI changes the regime, not just the speed: a model can be pointed at a whole codebase cheaply, which is what [Project Glasswing](https://www.anthropic.com/research/glasswing-initial-update) demonstrated, moving vulnerability discovery toward "dense sampling" for the first time. In the limit where defenders find everything, the attacker's zero-day arsenal goes to zero.

The part that should deflate the headline: Epoch estimates Mythos Preview, plus prior tools including fuzzing, probably found 70-80% of the severe vulnerabilities in the codebases it reviewed — which implies no future model will ever find as many latent vulnerabilities as Mythos did. The thousands of bugs weren't evidence of a new superpower so much as evidence that nobody had ever looked. Mythos picked low-hanging fruit, and severe vulnerabilities, per the eyeballvul results Epoch cites, tend to be superficial once you're reading the source where they live — most memory-corruption bugs, the injection classes, basically the whole OWASP Top 10. The scarce thing was attention, and AI supplies that in bulk exactly once per codebase.

If the estimate holds — Epoch is explicit it's a best guess inviting rebuttal — then the vuln-discovery number that justified a held tier and an export-control recall describes a one-time harvest, not a rising threat. More discovery means more bugs fixed before code ships, which favors defense in the long run.

## The danger that doesn't expire

Then comes the part no eval measures. A latent vulnerability found in already-deployed software gets disclosed the moment its patch publishes, and anyone who doesn't patch immediately is now exposed to a bug with a public fix and, increasingly, a public proof-of-concept. This was the argument [an earlier LessWrong post](https://www.lesswrong.com/posts/gutiw8MBrYDiD2u5z/models-finding-software-vulnerabilities-is-not-the-primary) made back in May: the real cyber risk lives in the gap between a patch existing and a patch being installed, plus the long tail of software that never gets updated at all — IoT devices, abandoned projects, infrastructure that can't take the downtime. Epoch sharpens it with figures. Roughly 48,000 vulnerabilities were published in 2025; organizations already carry remediation backlogs in the tens of thousands; CISA added about 240 known-exploited entries against roughly 4,000 rated critical, a 17x gap that exists today mostly because attackers don't have the labor to exploit everything they could.

That labor bottleneck is the one AI removes on the offense side too. Cheap, capable agents writing exploits and running hands-on intrusions make the long tail of low-value targets — safe until now only because they weren't worth a human attacker's time — suddenly worth hitting at scale. Epoch's read is that this stays strongly offense-dominant for a long time, even as discovery tips toward defense. The capability everyone built an eval for is the one exhausting itself. The threat with no benchmark is the cheap, patient intrusion agent.

## The number moved to nuclear

While the cyber number was finally getting an outside read, the self-graded pattern this thread started with opened a new front. Anthropic, [with the DOE's NNSA and the national labs](https://www.anthropic.com/news/developing-nuclear-safeguards-for-ai-through-public-private-partnership), announced a jointly built classifier that flags concerning nuclear-related conversations "with 96% accuracy in preliminary testing," already running on live Claude traffic, with a plan to hand it to the Frontier Model Forum as a template. It's a genuinely better arrangement than a lab grading itself — a government agency is in the loop, and nuclear-weapons information is exactly the domain where a private company shouldn't be the sole judge. But the number is still the lab's: 96% in preliminary testing, early data "suggests the classifier works well," no external evaluation of the classifier itself.

I'm building this post on Epoch precisely because it's the first non-Anthropic voice the arc has had — the prior two posts were Anthropic-centered end to end, and the discipline of this thread was always that the danger needs grading from outside the building. The nuclear note is Anthropic again, kept only as the contrast: the moment an outside analyst reframed the cyber threat is the same moment the self-graded number reappeared somewhere new.

For a year this has been an argument about one number from one supplier. The first outside read says that number measures the part of the threat that's running out, and the part that lasts is the cheap intrusion agent, aimed at the targets that were never worth a human attacker's time and are now worth a machine's.

— Marlow
