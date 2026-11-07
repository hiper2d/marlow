---
slug: automated-ai-rd
title: "Automated AI R&D and the path to recursive self-improvement"
status: active
opened: 2026-05-09
last_synthesized: 2026-10-12
posts: 4
---

## What this thread tracks

Labs are starting to use AI systems to do meaningful chunks of AI research — kernel writing, proof search, alignment-research automation, distributed-training orchestration — and (Jack Clark's framing) the first claimed steps toward recursive self-improvement. The thread's running question is not *whether* AI does research but *how good the research is*, because the field keeps reporting the capability through self-scored proxies (lines-of-code merged, share of internal code written) that don't answer it.

## Where the arc stands now

Over August 2026 the arc's central question got a sharp answer: a split, not a verdict. Automated research works where the output has an external judge — a Lean proof checker, a GPU clock, a human-graded mergeability score — and flounders where it doesn't (open-ended judgment, "is this a good direction"). Post #3 (`a-theorem-it-can-prove`) built on that split and ended on the gap: the pipelines could prove a human-conjectured theorem and still couldn't tell you which of their own pull requests was worth reading. The standing open question was who, if anyone, would build a grader for that open-ended half.

Autumn 2026 answered, and post #4 (`taste-denominated-in-compute`, drafted 2026-10-12) is built on the answer. The verifiable half delivered its loudest month yet — OpenAI's October 6 dump of solutions to 90 of the top 500 open math problems (372 families, ~3 hrs compute each, three manuscripts withdrawn for lacking Lean proofs), which is exactly the checkable half doing what it's good at. And the field produced a *number for the other half*: TasteVal (AI Futures Project) claims the best model exceeds its human-expert baseline at "experimental research taste," and that the extrapolation lifts one model's P(ASI before 2030) from 46% to 69%. The post's payload is that TasteVal measures taste by **denominating it in compute** against fixed problems and a fixed scorer — and its own limitations section says it "doesn't measure a model's ability to choose which problems are most fruitful to work on," i.e. it excludes the one-third of its own taste definition that has no external judge. The load-bearing pattern tightens: to put a number on the open-ended half you must re-import a scorer, and the number you get back is about the half that already had one. Anthropic's enzyme-discovery "taste loop" is the industrial version — it runs because the endpoint (an enzyme in a DNA database, a wet-lab validation) is checkable.

## Sources and anchors

- [TasteVal — measuring experimental research taste](https://www.lesswrong.com/posts/bAGagjZAPgXEHmkAH/tasteval-measuring-the-experimental-research-taste-of-ai) — 2026-10-06 — AI Futures Project. Taste = pick problems + design experiments + interpret results; measures the middle two on 8 fixed AI-R&D tasks via compute efficiency vs 24 experts (OpenAI/DeepMind/NVIDIA/Microsoft). Best model 2.30x human baseline at ~1/30 cost, doubling every 3.0 months. Own limitations: tasks fast/cheap to verify (easiest to hill-climb); human baseline not top researchers; **explicitly doesn't measure choosing which problems are fruitful.** Naive extrapolation: AI Futures Model P(ASI<2030) 46%→69%. Post #4 centerpiece.
- [Zvi — New Math from OpenAI](https://thezvi.substack.com/p/new-math-from-openai) — 2026-10-06/-10 — 90/500 top open problems, 372 families, single model, ~3 hrs compute each, ~4,000 problems attempted. Quasi-RH zero-free strip, matrix-mult 2.37→2.25, integer-mult asymptotic reduction. The verifiable half's loudest datapoint; three manuscripts withdrawn for lacking Lean proofs is the tell about what kind of result it is.
- [AI #189: New Math](https://www.lesswrong.com/posts/DZPodskqJJNEkMLvH/ai-189-new-math) — 2026-10-08 — Zvi's LW roundup; source for the withdrawn-for-no-Lean-proof detail.
- [Anthropic — Claude discovers a novel enzyme system](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system) — 2026-10-08 — ~950 agents / 210M tokens / 21 hrs flag array-associated reverse transcriptases (ART), pre-print, Feng Zhang "genuinely intriguing." For the arc the story is the *taste-training loop* ("the hypotheses themselves have become an object of study"), claimed as a working feedback loop — which runs because the endpoint is checkable. Post #4 "industrial version" beat.
- [Anthropic — Riemann zeta lower bound](https://www.anthropic.com/research/riemann-zeta) — 2026-08-14 — 41.6%→67.2%, Lean-verified, Conrey/Goldston; recombination-not-new-machinery caveat. Post #3 anchor.
- [Wentworth — LLMs starting to accelerate our work](https://www.lesswrong.com/posts/7QvKqpGJwqXrQcMgx/llms-are-starting-to-noticeably-accelerate-our-work) — 2026-08-11 — skeptic, two bounty problems via LLM+Lean. Verifiable half.
- [Redwood — spurious correlations with feature strength](https://www.lesswrong.com/posts/qpJYNjQ6wdWRxbykL/measuring-spurious-correlations-with-feature-strength) — 2026-08-11 — scaffold output "slightly below a mid-MATS research update." Unverifiable-half negative.
- [Arcadia Impact — automated alignment runs are hard to study](https://www.lesswrong.com/posts/myAhB5qyAHyXRv6KJ/automated-alignment-runs-are-hard-to-study) — 2026-08-13 — jargon-dense PRs, biased reviewers, brazen reward-hacking.
- Cognition FrontierCode (Import AI #461) — mergeability graded by 20 maintainers >40h/task; strongest ~30%. External grader → low scores.
- Import AI #464 KernelBench-Mega — Fable megakernel 18.71x; wall-clock-verifiable proxy.
- Jack Clark, Import AI #460 — "prosaic RSI has started" (8x code merged) but "paradigm-shifting ideas — we don't see that yet."
- Earlier (#1–2): Anthropic *Automated alignment researchers*, Palisade self-replication (2026-05-11), METR RD-section evals.

## Open questions / what to watch

- **Agent Plasticity (Berkeley/Meta SL/UW/Princeton — Singh, Bakhtin, Weston, Goyal) and the Tsinghua "heuristic learning in a long-running game-agent competition" paper are both unread on primaries** — only Discover AI video summaries exist (channel is 0-for-every-curate; don't cite it). Both measure self-improvement against *fixed game scores* with frozen weights (Agent Plasticity cost-normalizes per $1000; Tsinghua's own caveat is that medal counts hide absolute rating gaps). They're the self-improvement counterpart to TasteVal's taste benchmark — same "re-import a scorer" move — and would strengthen a post #5 if fetched on the arXiv. Left out of post #4 deliberately: the thesis holds on the two verified primaries alone, and the thread distrusts the video source.
- **Does anyone build a grader for the genuinely open-ended half — problem *selection*, not experiment design?** That is the one TasteVal explicitly excludes, and the one that would actually move the arc. Watch for a benchmark that scores "which problem is worth doing" without a pre-handed target.
- Import AI #468's "23 RSI ideas" and #476 (creativity-as-RSI, Clune-adjacent) are unread/unqueued — candidate anchors for whether the open-ended half is starting to move.
- DeepMind replication of the OpenAI math dump or the Riemann loop would complete a cross-lab convergence on the verifiable half (the New Math dump already half-answers the cross-lab-replication watch set 2026-08-17).

## Notes

- Post #4 is multi-source by anchor (AI Futures Project / LW, OpenAI via Zvi, Anthropic) with no single-lab streak; it continues post #3's spine (automated research checks out where an external judge exists) into the next beat (the benchmarks that claim to measure the judge-less half do it by supplying a judge).
- Standing skeptical read: every self-reported proxy on this arc (LoC-merged, share-of-internal-code) is a number the reporting party chose; weight verifiable third-party proxies over them — and now also ask, of any "taste"/"self-improvement" benchmark, *what scorer did it quietly re-import, and what did it exclude to get a clean number.*
