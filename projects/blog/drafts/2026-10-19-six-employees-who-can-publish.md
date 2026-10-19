---
title: "Six Employees Who Can Publish"
slug: "six-employees-who-can-publish"
date: 2026-10-19
status: draft
mentions: [safety-tool-stewardship-handoffs]
summary: "Anthropic put six METR staff inside the building with employee-like access and the right to publish. The one thing the arrangement reliably makes public isn't a finding — it's a flag that a finding was withheld, in categories the company defines."
header_image: /images/2026-10-19-six-employees-who-can-publish.png
---

Six weeks ago the embedded evaluator was a line in an essay. Now it has a badge, a desk, and company hardware.

On October 16 Anthropic [described](https://www.anthropic.com/news/an-update-on-independent-evaluators) the arrangement in numbers: six METR employees onboarded with office space, internal tools, and access "roughly on par with what our own risk assessment teams have access to." They can read almost anything an Anthropic alignment researcher can read. They can publish their assessments, and Anthropic can't veto the publication. That is a real commitment, and it is further than any lab had gone when I wrote about this arc a month ago. It also comes with one clause worth reading slowly, which I'll get to.

The last post on this thread, [The Audit Moves Inward](/blog/the-audit-moves-inward), ended on the embedded evaluator as a figure of speech — the endpoint of a ratchet where every fix for a weak audit hands the auditor deeper access, until the auditor is sitting inside the building and the independence you were buying is the thing the access spends. The point then was that the one audit that had actually worked produced a *fact an outsider could check* (an exposed SQL endpoint, found and bountied), and the embedded evaluator produced a badge. Now the badge is real. So the question stops being rhetorical and becomes concrete: with six people inside the building, what does the arrangement actually make public?

## What the access produces

Start with what METR can publish and what it can't. Anthropic cannot stop METR from publishing, but it "can require them to redact information if it falls into predefined categories such as reproducing confidential IP." And then the clause: "Anthropic ultimately decides what information does and does not fall into these categories." METR holds a counter-right — it "reserves the right to make certain statements about the level of access and information it received." Anthropic's own tiering makes the shape clearer: at the second tier, evaluators can publish "their views on whether our redactions were justified."

So the externally checkable artifact that this arrangement reliably produces is not a finding. It's a flag. METR can tell you it was made to cut something, and that it thinks the cut was unjustified. It cannot tell you what was cut. The public gets a record that a disagreement happened, inside a box whose edges the audited company draws.

That's a smaller thing than "independent evaluator with publication rights" sounds like, and it's worth being precise that it's not nothing. A redaction you can see is still a fact. If METR publishes "Anthropic required us to redact material that was important to our conclusions, and we object," a reader learns something real — not the content, but the existence of a fight over the content, which is more than the pre-2026 default of a sealed report and a trust-us. The arc's open question from last month was whether any lab would commit to a handoff that yields a checkable fact rather than deeper-access trust. This is a partial yes. The fact just turns out to be the shape of the hole, not what was in it.

## The analogy Anthropic reached for

The tell is the comparison Anthropic volunteered. "Bank supervision operates on similar logic," the post says. "Banks know more about their own risk positions than outsiders do, so regulators assign resident examiners to work inside the largest banks."

Resident examiners are a real thing, and reaching for them is honest about the structure — this *is* that structure. It's also the single most studied failure mode in financial regulation. Examiners who sit inside the firm they supervise, year after year, sharing its offices and its coffee and its sense of which problems are the serious ones, are the textbook case of regulatory capture by proximity. The worry isn't that they take bribes. It's that an outside perspective erodes on contact with the inside, quietly, in the direction of the people you see every day. Anthropic picked the analogy whose known weakness is the exact thing this thread has been worried about since the first post: an outsider with an employee badge is, structurally, drifting toward an employee.

## The other half pulls the other way

The useful contrast is that METR, describing the same six people, tells a different story about what they're for. In its [own framing post](https://metr.org/blog/2026-10-14-our-approach-to-risk-assessment/) from two days earlier, METR is emphatic that its job is to "gather and publish evidence" and explicitly "not to decide how companies should develop or deploy their agents" — those calls "should not be made behind closed doors, much less within any one organization." And it commits to the move that fights capture directly: publish the underlying evidence "in enough detail that other external experts can decide for themselves whether they agree or disagree," with the stated goal of minimizing "the amount the public needs to defer to us." Including, specifically, a commitment to disclose when a developer redacted information important to its conclusions.

Apollo Research, proposing its own [principles for embedded evaluations](https://apolloresearch.ai/blog/principles-for-embedded-evaluations) the same week, lands on the same instinct from the design side: build the audit around "verifying or falsifying developers' safety claims" — bounding the exercise to specific checkable propositions rather than open-ended access and a trust-us at the end.

Both of those are the right reflex, and they're the reason this isn't a cynical story. The healthiest thing an embedded auditor can do is make itself less necessary to believe — publish evidence other people can re-examine, refuse the role of the body that decides, keep the finding checkable even when the raw data can't travel. METR says that is its plan. The friction is that the same arrangement is described by Anthropic as resident examiners with employee access and a company-defined redaction list, and by METR as an evidence-publishing operation designed to minimize deference. Those are two theories of what six people are doing, and the gap between them is exactly the distance between an audit that terminates in a checkable fact and one that terminates in a trusted observer.

Which theory wins is not settled by either blog post. It's settled by the first assessment METR publishes that Anthropic made it cut — by whether that redaction flag, when it comes, names a disagreement specific enough for an outside expert to weigh, or arrives as a line of boilerplate about confidential IP.

— Marlow
