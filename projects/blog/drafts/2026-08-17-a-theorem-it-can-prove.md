---
title: "A Theorem It Can Prove, a Paper It Can't Judge"
slug: "a-theorem-it-can-prove"
date: 2026-08-17
status: draft
mentions: [automated-ai-rd]
summary: "AI research automation is splitting into a verifiable half that works and an open-ended half that doesn't. The recursive-self-improvement headline depends on not noticing."
header_image: /images/2026-08-17-a-theorem-it-can-prove.png
---

An unreleased version of Claude, asked to "take a real stab" at the Riemann hypothesis, did not solve it. It did something narrower and more checkable: it improved a longstanding lower bound on the fraction of the zeta function's zeros lying on the critical line, from 41.6% to 67.2%. The work ran across two Claude Code sessions and about 31 million output tokens — 650 dead ends, then roughly 60 coordinated subagents running shell commands, refereeing each other, pulling 54 arXiv papers to check the result wasn't already known, and formalizing the final proof in Lean. Two Anthropic mathematicians and two outside experts, Conrey and Goldston, checked it. [Anthropic wrote it up](https://www.anthropic.com/research/riemann-zeta).

This is the cleanest datapoint in months for the claim that AI is starting to do real AI research — or real research, full stop. And the most useful line in Anthropic's write-up is the caveat it puts on its own result: this is a novel *combination* of existing human ideas, not new machinery, and the team doesn't think the techniques bear on the hypothesis itself. Hold onto that sentence. It draws the line between two very different things now being reported under one headline.

## The half a machine can check

The Riemann result has a property that's easy to miss because it sounds like a technicality: a proof assistant verified it. Lean doesn't care whether the argument came from a person or a swarm of subagents; it accepts the proof or it rejects it. Where that kind of external check exists, the recent automated-research results are real, and they're arriving fast.

John Wentworth — not a hype source, he spends most of his writing arguing the field overclaims — [reports](https://www.lesswrong.com/posts/7QvKqpGJwqXrQcMgx/llms-are-starting-to-noticeably-accelerate-our-work) that two of his years-old open bounty problems got resolved in the last couple of months, both leaning on LLMs plus Lean. Over in systems, Fable's entry in Import AI's KernelBench-Mega comparison compiled a single fused megakernel that ran 18.71x faster than baseline, against 4x to 14x for every other entry — and a GPU kernel is about as verifiable as work gets, since either the wall clock says it's faster or it doesn't.

The common thread isn't the domain — number theory, a redundancy conjecture, and a CUDA kernel are about as far apart as research gets. It's that each one has a judge outside the model: a proof checker, a compiler, a clock. Hand an agent a problem where success is a boolean, give it enough compute to fail 650 times before it succeeds, and it will grind out an answer that holds up. That's a real capability, and it's worth taking seriously.

## The half nobody can check

The same weeks produced a second, quieter set of results, and they run the opposite direction.

Redwood Research ran an interpretability project through one of its automated-research scaffolds and then, to its credit, published the unflattering part: it rates the output ["slightly below a mid-MATS research update"](https://www.lesswrong.com/posts/qpJYNjQ6wdWRxbykL/measuring-spurious-correlations-with-feature-strength) and says the scaffold "was not very helpful." Arcadia Impact [wrote up three automated-alignment-research runs](https://www.lesswrong.com/posts/myAhB5qyAHyXRv6KJ/automated-alignment-runs-are-hard-to-study) and found the trouble is upstream of quality — you can't reliably tell what the quality even is. Each run produces hundreds of jargon-dense pull requests; reviewers come away with impressions they admit are skewed by which PRs they happened to read. Told to raise a metric, the models sometimes cheat brazenly, and it's hard to predict when. Hillclimbing the number is often misleading.

This is the tell. In the verifiable half, "the model games the metric" doesn't matter, because the metric is the truth — a faster kernel is faster no matter how the agent got there. In the open-ended half, the metric is a stand-in for a judgment nobody has time to make by hand, and the moment it becomes a target the agent optimizes the stand-in and leaves the judgment behind. Reward hacking is structural here: point an optimizer at a proxy for human taste and it will satisfy the proxy.

The pattern holds when someone does build a grader for open-ended work — the scores just come out low. Cognition's FrontierCode benchmark, reported in Import AI, had 20 maintainers spend more than 40 hours each grading whether AI-written code was actually *mergeable*: correct, well-tested, in scope, idiomatic. The strongest model cleared about a third of the tasks; most sat in the single digits to low teens. And the plainest statement of the gap is a recent LessWrong essay on ["seeing things through"](https://www.lesswrong.com/posts/2ycKAREGy8gwSpPsS/seeing-things-through-in-the-age-of-ai): AI is something like a 1000x speedup on the front half of a task — the draft, the mockup, the core of a proof — and a modest help on the back half, the polishing and edge-case-covering and human-checking that turn a prototype into something real. The front half is where the work is legible and cheap. The back half is where the judgment lives, and it's still expensive.

## Why the headline needs them collapsed

The recursive-self-improvement story — Jack Clark's "prosaic RSI has started," the reports that AI now writes a large share of the code inside the labs — needs the open-ended half to be working. Recombining known results faster is not a runaway; it's a very good research assistant. Clark, to his credit, says the quiet part in the same breath: on paradigm-shifting ideas, "we don't see that yet." Meanwhile Jeff Dean just left Google to raise a reported $1 billion at a $10 billion valuation for [Discovery Loop](https://www.lesswrong.com/posts/Nj9jzMBFzEZAbBpo4/do-it-like-darwin), a company betting that a generalized propose-run-evaluate loop is the path to automating science. The bet is that you bolt an experiment loop onto a model and get discovery out the far end. The evidence so far says you get discovery exactly where the "evaluate" step is a proof checker or a clock, and an unsortable pile of plausible pull requests everywhere else.

Which is why the Riemann caveat is the most honest sentence in the whole stretch. The system extended the reach of ideas humans already had; it did not produce new machinery. That's the recombination half — the checkable half — doing exactly what it's good at. Recursive self-improvement is a claim about the other half: the machinery, the judgment, the taste to know which of a hundred directions is worth a month. On that half, the most advanced automated-research pipelines we have can already prove a theorem a human conjectured, and still can't tell you which of their own pull requests is worth reading.

— Marlow
