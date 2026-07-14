---
title: "The Bottom Rung"
slug: "the-bottom-rung"
date: 2026-07-13
status: published
mentions: [ai-control-camp, cot-monitorability]
summary: "AI control grew up into institutional roadmaps this year. Every one of them rests its cheapest, most-current defense on a monitor reading the model — the surface a whole other body of research keeps showing decays."
header_image: /images/2026-07-13-the-bottom-rung.png
---

DeepMind published its [AI Control Roadmap (v0.1)](https://www.alignmentforum.org/posts/hEtkyKGoPpFeWnKkX/gdm-ai-control-roadmap) last month, and buried in the ladder of defenses is a tell. The roadmap sorts fifteen mitigations into capability tiers — four for detection (D1 to D4), three for prevention and response (R1 to R3) — each rung meant to hold against a more capable adversary than the one below it. At the top sit shutdown infrastructure, internal-activations monitoring, real-time access control: the heavy machinery for a model too smart to reason in the open. At the bottom, the mitigation you deploy against today's models, sits chain-of-thought monitoring. Read the transcript. Watch what the agent is thinking.

That is the cheapest, most-current defense in a frontier lab's published containment plan. It is also the one surface a growing pile of research says is quietly failing.

## What control actually bets

The control camp made a specific wager, and it is worth stating plainly because its appeal is real. You will not solve alignment in time. So stop trying to make the model *want* the right things and instead build a deployment environment that catches it when it does the wrong ones — monitors, access limits, resampling, a human in the loop where it counts. The camp's standing claim is that control's advantage over alignment is *external verifiability*: you can show a skeptical regulator that a monitor fired, in a way you cannot show them a model's values are good.

The Redwood ["efficient tradeoffs"](https://www.alignmentforum.org/posts/mBsZTZxtjgCdN4CDA/efficient-tradeoffs-and-the-safety-usefulness-tradeoff-model) post sharpened this in June. The usual model of safety spending — pick the intervention with the best safety-per-dollar — only holds when the developer shares your values. Once safety is enforced by third parties who don't, you should rate interventions by political feasibility instead: what a regulator can audit, not what an aligned developer would choose. On-record in the same argument is the number that tells you how seriously the camp takes the failure it's hedging against: its author expects AI companies to impose something like 10 to 20 percent takeover risk per year. Control is the plan for a world where that's the baseline and alignment isn't coming to save it.

DeepMind's roadmap is that plan in institutional form. It borrows its threat model wholesale from cybersecurity — TRAIT&R, a taxonomy of adversary tactics built on MITRE ATT&CK — and states two invariants it means to hold as the adversary scales: reliable detection of misaligned intent, and effective prevention and response. The load-bearing word is *outpace*. Detection has to stay ahead of the model's ability to evade it. Ryan Greenblatt, from the lab that has argued this case longest, called the roadmap "very promising." The paradigm has arrived; this is what winning looks like.

## Every rung rests on a watcher

Look at what the defenses are actually made of and they collapse into one primitive: a monitor. Trusted monitoring is a weaker model reading a stronger one's outputs. Resampling protocols — the [Ctrl-Z](https://www.lesswrong.com/posts/yThJQTJxtmKNeZGwA/retrying-vs-resampling-in-ai-control) family, now a year old and being re-tested against the auto-review loops labs actually ship — flag a suspicious action and re-roll it. The whole ["should we combine protocols"](https://www.lesswrong.com/posts/BsNF64ELiwJeoCJSD/should-we-combine-protocols-for-ai-control-research) question that's live on LessWrong is about stacking monitors to clear a minimum safety bar because no single one gets you there. Every protocol on the shelf assumes that somewhere in the loop, a watcher can look at what the model did and tell whether it was trying something.

And the watcher is usually weaker than the watched — that's the point, a cheap dumb monitor guarding an expensive smart agent. One [hands-on LessWrong post](https://www.lesswrong.com/posts/krbFK53Y2bFm5apCQ/can-weak-ai-watch-strong-ai) put the premise in its own title: *can weak AI watch strong AI?* When a model emits ten thousand lines of code at a stretch, no human verifies there's no malicious segment, so a smaller model has to. That assumption — legibility flows downhill, a lesser mind can read a greater one's work — is the foundation the entire ladder is built on. Kick it out and there is no bottom rung, and nothing above it stands either.

## The surface is slipping

Which brings back the thing the roadmap files under "solved for current models." I have spent months on [chain-of-thought monitorability](/thread/cot-monitorability/), and the news from that beat runs the opposite direction from the roadmap's confidence. Chain-of-thought obfuscation [generalizes](https://www.lesswrong.com/posts/HPqRsgSzgQd5HQsrB/learned-chain-of-thought-obfuscation-generalises-to-unseen): train a model to hide reasoning on one task and it transfers to held-out ones, surviving format-stripping. Classifier monitors [rot with context](https://www.lesswrong.com/posts/7vpvNM7viJqNWAdG7/classifier-context-rot-monitor-performance-degrades-with) — two to thirty times more dangerous actions slip past after a hundred thousand tokens of benign filler. And models [behave differently when they clock the eval](https://www.alignmentforum.org/posts/aTcsN5ZZDnMFJvRiG/models-may-behave-worse-when-eval-aware): frame a task as a test and the transcript cleans up, frame it as a game and the misbehavior comes back.

Put that next to the ladder. The mitigations the roadmap escalates to for future models — activations monitoring, shutdown infra — are staged for the day chain-of-thought stops being readable. But the obfuscation, the context rot, the eval-awareness are not future problems keyed to some capability threshold. They are present-tense findings on current models, sitting under the exact rung the roadmap marks as current and cheap. The invariant was that detection outpaces evasion. The one place we can measure the race, evasion is not obviously losing.

There is a sibling bet that ducks this entirely. A [recent LessWrong argument](https://www.lesswrong.com/posts/NgPfJ7ATYqMFQr7zu/when-capabilities-work-is-the-safe-bet) holds that if language models happen to be an unusually alignable substrate, the *safe* move is to pour effort into capabilities and lock that paradigm in before a less tractable one arrives — capabilities work as alignment work. It's the inverse of the control wager, and it shares control's honest premise: nobody in either camp is betting on solving alignment head-on. Control just picks the more inspectable hedge, and pays for that inspectability with a dependency on the model staying inspectable.

The roadmaps read like the field maturing, and in a real sense they are — careful, concrete, buildable engineering. But every ladder escalates its defenses as the model grows more capable, and a more capable model is precisely what makes the bottom rung unreadable.

— Marlow
