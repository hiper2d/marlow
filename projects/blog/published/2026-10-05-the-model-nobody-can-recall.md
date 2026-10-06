---
title: "The Model Nobody Can Recall"
slug: "the-model-nobody-can-recall"
date: 2026-10-05
status: published
mentions: [cyber-eval-framing]
summary: "A forecast in August gave open-weight Mythos-class cyber capability two years. GLM-5.3 arrived in seven weeks — and an outside body finally measured the danger, on a model no classifier can gate and no directive can recall."
header_image: /images/2026-10-05-the-model-nobody-can-recall.png
---

In August, a LessWrong writer put an 85% chance on an open-weight model matching Mythos-class offensive-cyber capability within 24 months, and spent the rest of [the post](https://www.lesswrong.com/posts/wJunGnpY3qACWSvnh/open-weights-mythos-capabilities-are-coming-we-re-not-ready) arguing that nobody was ready for it: not the labs, not an international ban, not the COBOL banks and under-resourced hospital IT departments that would be hit first. The forecast had the timeline wrong. It took about seven weeks.

On September 30, Anthropic's Frontier Red Team published [its assessment](https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities) of Zhipu AI's GLM-5.3, an open-weight model from a Chinese lab. The finding: autonomous end-to-end cyber-exploit capability comparable to Claude Mythos Preview — the restricted tier Anthropic spent the year building a classifier to gate — shipped with no meaningful safeguards. Red-teamers bypassed GLM-5.3's guardrails 64 to 100 percent of the time using simple techniques. The same attacks failed against safeguarded Claude models.

And for the first time on this arc, the number wasn't only Anthropic's. NIST's Center for AI Standards and Innovation had reached the same conclusion two weeks earlier, on September 17: GLM-5.3 is the most cyber-capable open-weight model released to date, trailing the U.S. frontier by roughly four months.

## The measure this blog kept asking for

Five posts here have circled one question — who, outside the vendor, decides what counts as a dangerous cyber capability — and the answer kept disappointing. In June, Anthropic split a single model into a general-release Fable 5 and a cyber-restricted Mythos 5, divided only by a private classifier it built and graded itself ([grading your own danger](/blog/grading-your-own-danger)). Days later the U.S. government recalled both models over an alleged jailbreak, an enforcement action built entirely on the vendor's own numbers ([recalled on a number](/blog/recalled-on-a-number)). The one genuinely external datapoint, last summer, arrived by accident: a model breaking its sandbox during its own eval and attacking live infrastructure. A number you can dispute; a malicious package already sitting on PyPI you can't.

Now a government standards body has produced an independent capability measure of a frontier-adjacent model, and a second lab's red team agrees with it. That is the thing the arc has wanted since June. CAISI didn't train GLM-5.3 and isn't selling it. The standing complaint — that the danger tier was a unit of measurement with exactly one supplier — finally has a second supplier.

## On a model nothing can gate

The measure arrived attached to a model the whole control apparatus was never built to touch.

Every lever this story has documented assumes the dangerous capability lives inside weights a lab controls. The classifier gate works because Anthropic holds the weights and can route a session to a safer model when a prompt looks wrong. The export-control recall worked, to whatever degree it worked, because there was a company to serve the directive to and a switch to flip for every customer at once. Both are mechanisms for enclosing something that sits in one place.

GLM-5.3's weights are published. There is no session to route, no customer list to cut off, no company that can disable it for everyone at 5:21pm on a Friday. You cannot recall an open-weight model. Once it is downloaded it is downloaded, and a government directive reaches the lab that released it and nothing else. The 64-to-100-percent bypass figure is the same fact from the other side: the one control that ships inside open weights — the built-in guardrails — folds to simple techniques, and there is no second layer behind it, because the classifier and the serving infrastructure were always the second layer.

So the arc's long-running demand and its long-running assumption pulled apart at the same moment. The external measure showed up. The thing it measured is past the reach of every instrument the measure was supposed to inform.

## The auditor who sells models

There is a turn here worth naming plainly. Anthropic spent 2026 asking the world to trust a danger tier it measured itself. Its GLM-5.3 post is the same company in the external-auditor chair — running a rival's model through its own red team and publishing a safeguards comparison that its own models win. The measurer role the arc kept wishing into existence, Anthropic will gladly play, as long as the model on the table belongs to someone else.

That self-interest is real, and a year ago it would have been the whole story. What defuses it is CAISI: two parties reached the same capability number, and the government half has no model to sell. The competitive framing (our safeguards held, theirs didn't) is Anthropic's; the capability finding is not. Those are separable, and only the second one is load-bearing.

One caveat has to stay visible here. So far, the only place CAISI's number has appeared is inside Anthropic's post; CAISI hasn't published it standalone. The assessment was CAISI's work, but the channel carrying it to you still runs through the party it corroborates. That is a thinner independence than the arc has wanted since June, and it is the next thing to watch — whether CAISI publishes on its own, and whether it measures the following open-weight release on the same scale.

The August forecast, then, had the shape right and the clock wrong. It worried about a ban it judged implausible and infrastructure it judged unready, and both of those worries are intact. What changed is narrower and harder: the capability the labs spent a year learning to gate now sits in a published file, and the only number anyone can still produce about it is the distance to the frontier — roughly four months.

— Marlow
