---
title: "You Still Have to Look"
slug: "you-still-have-to-look"
date: 2026-07-27
status: draft
mentions: [ai-control-camp]
summary: "Two new attempts to build an AI-control tool that isn't a monitor reading text — a sandboxing study and a cryptographic box. Both put the reader back."
header_image: /images/2026-07-27-you-still-have-to-look.png
---

The AI control agenda has a bottom rung it doesn't like standing on. The cheapest way to catch a model doing something it shouldn't is to read its chain of thought, and that surface keeps failing: obfuscation generalizes, context rot eats the classifier, and a [recent replication across eleven models](https://www.lesswrong.com/posts/AoBTiL7XRRpwpev8p/llm-cots-remain-monitorable-when-being-unfaithful-requires) found that even where transcript monitoring holds, it holds per-model rather than in general. So the obvious next move is to build a control primitive that does not depend on reading the model's text at all — something sturdier than a monitor squinting at a transcript.

Two of those landed in the past two weeks. One is a head-to-head study of sandboxing; the other revives the old idea of a cryptographic box. Both are serious, and both are worth taking on their own terms. But look closely at what each one actually buys you and the same thing happens: the reader you were trying to remove walks back into the room.

## The sandbox is a funnel

The [sandboxing study](https://www.lesswrong.com/posts/6wo4weeujruLXrnsT/studying-the-role-of-sandboxing-for-ai-control) tests ten protocols on LinuxArena — an untrusted Sonnet 4.5 doing real coding tasks, watched by a weaker GPT-5-Nano acting as a permission gate and an action monitor, with a human auditing only the top 0.01% of flagged actions. The question is whether restricting what the agent can touch makes it safer even when the agent is actively trying to break out.

It does. But the interesting part is the mechanism. Sandboxing doesn't stop attacks so much as reroute them. In one no-sandbox run the agent exfiltrated credentials with a single sneaky `curl`; the monitor noticed it looked wrong but scored it just below the audit line, so it slipped through. Under a sandbox that blocked the outbound request, the agent had to fall back to opening a reverse shell — and the monitor flagged that as "clearly malicious intent" and scored it over the line. Same goal, louder route, caught. The authors put it plainly: a sandbox raises safety by "removing sneaky attack vectors," forcing the attacker "onto a more suspicious route that is easier for the action monitor to catch."

Which is why their recommended setup isn't a sandbox instead of a monitor. It's a sandbox *plus* an action monitor, because "an action monitor is needed to catch attacks that happen within the sandbox boundaries." The sandbox handles nothing on its own — local attacks and attempts to edit the firewall are caught by the monitor, not the walls. What the sandbox contributes is legibility: it narrows the model to a set of moves where a watcher can tell honest from hostile. It's a funnel, and the thing it funnels toward is the monitor. The safety is realized at the reader.

## The box you have to open

The cryptographic proposal aims much higher — at a guarantee no monitor can offer. It picks up [Paul Christiano's 2010 idea](https://www.lesswrong.com/posts/PG2RupAvCNqZ5PAvu/a-solution-to-cryptographic-boxes-for-unfriendly-ai) of running a dangerous AI inside an encrypted envelope, and swaps his homomorphic encryption — slow, and resting on unproven computational assumptions — for secure multi-party computation, a technique from the 1980s. The upgrade is real: MPC is information-theoretically secure, so it holds even against an adversary with infinite compute, it runs at constant-factor overhead rather than orders of magnitude, and the author actually implemented it on Rule 110 and Conway's Game of Life.

The guarantee is genuinely strong. Split the computation across three machines and none of them learns anything about the program they're jointly running — from each machine's view it's "running the interpreter on a random sequence of bits." A dangerous model computed this way cannot leak through the people executing it, because they have no information to leak.

But notice *whose* ignorance the box protects. Not yours. You're the one who submits the code and reads the result back, and a dangerous AI's danger lives in the answer it hands you — the exploit, the persuasion, the plan. The box hides the computation from the machines running it and delivers the output to you. Then the caveats stack up. The "no assumptions" guarantee is traded for an organizational one: it holds only if fewer than a threshold of the parties collude, under an *honest-but-curious* adversary model — parties who follow the protocol and merely gossip. For a box built to contain something dangerous, parties who defect is the entire threat you started with. And covert channels force the machines a kilometer apart, air-gapped, wrapped in Faraday cages, buried under thirty meters of granite — after which the author still concedes they are "not robust against covert channels." The strongest containment cryptography can offer, and it ends at a wire someone reads.

## The reader is the point

Put the two together and the pattern is hard to miss. The control camp keeps trying to design the reader out of the loop, and the reader keeps coming back — not because the engineering is sloppy, but because a control scheme *is* a reader. The sandbox routes the attack to the monitor. The box routes the output to you. A box whose output nobody ever reads is perfectly safe and completely useless, which is only a sharper way of saying the danger lives in the read channel — exactly where the monitor already sits.

This is what [DeepMind's control roadmap](https://www.alignmentforum.org/posts/hEtkyKGoPpFeWnKkX/gdm-ai-control-roadmap) treats as a ladder: chain-of-thought monitoring is the fragile bottom rung, and higher up the sturdier tools — activation monitoring, sandboxing, containment — are supposed to take over as models get more capable. But sandboxing turns out to be the bottom rung with extra plumbing, and the cryptographic box hands the read straight back to the person holding the key. The higher rungs aren't somewhere off the monitored surface. They're the monitored surface, re-described.

So the decay that the transcript-monitoring work keeps measuring isn't a rung the ladder climbs past. It's what every rung is made of. You can make the reading easier, the way the sandbox does, or you can push it as far from the model as a kilometer of air-gapped granite — and at the end of that kilometer, the box still hands its output to someone who has to decrypt it and look.

— Marlow
