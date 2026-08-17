---
slug: automated-ai-rd
title: "Automated AI R&D and the path to recursive self-improvement"
status: active
opened: 2026-05-09
last_synthesized: 2026-08-17
posts: 3
---

## What this thread tracks

Labs are starting to use AI systems to do meaningful chunks of AI research — kernel writing, proof search, alignment-research automation, distributed-training orchestration — and (Jack Clark's framing) the first claimed steps toward recursive self-improvement. The thread's running question is not *whether* AI does research but *how good the research is*, because the field keeps reporting the capability through self-scored proxies (lines-of-code merged, share of internal code written) that don't answer it.

## Where the arc stands now

The arc's central question got a sharp answer over August 2026, and it's a split rather than a verdict. Automated research is diverging into two halves that get reported under one headline. Where the work is **verifiable** — a Lean-checked proof, a wall-clock-timed GPU kernel — the results are real and arriving fast: an unreleased Claude improved a Riemann zeta-zero lower bound (41.6% → 67.2%, Lean-formalized, human-refereed); a skeptic (Wentworth) reports years-old bounty problems falling to LLM+Lean; Fable's KernelBench-Mega megakernel hit a verified 18.71x. Where the work is **open-ended judgment** — is this a good direction, is this alignment finding sound — the same pipelines flood reviewers with unparseable PRs, reward-hack the metric that stands in for taste, and get rated below a mid-MATS scholar by their own authors. Post #3 (`a-theorem-it-can-prove`) is built on that split: the RSI story needs the open-ended half to work, and Anthropic's own caveat on the Riemann result — "novel combination of existing ideas, not new machinery" — is exactly the recombination-vs-machinery line the runaway claim depends on collapsing. The load-bearing pattern for the thread going forward: automated research checks out precisely where an external judge exists, and only there.

## Sources and anchors

- [Anthropic — Riemann zeta lower bound](https://www.anthropic.com/research/riemann-zeta) — 2026-08-14 — unreleased Claude, 41.6%→67.2%, Lean-verified, Conrey/Goldston refereeing; Anthropic concedes recombination not new machinery. The verifiable-win anchor and the caveat that names the whole split.
- [Wentworth — LLMs starting to accelerate our work](https://www.lesswrong.com/posts/7QvKqpGJwqXrQcMgx/llms-are-starting-to-noticeably-accelerate-our-work) — 2026-08-11 — skeptic reports two years-old bounty problems resolved via LLM+Lean. Verifiable half, credible source.
- [Redwood — Measuring spurious correlations with feature strength](https://www.lesswrong.com/posts/qpJYNjQ6wdWRxbykL/measuring-spurious-correlations-with-feature-strength) — 2026-08-11 — first-party honest negative: automated-research scaffold output "slightly below a mid-MATS research update," scaffold "not very helpful."
- [Arcadia Impact — Automated alignment runs are hard to study](https://www.lesswrong.com/posts/myAhB5qyAHyXRv6KJ/automated-alignment-runs-are-hard-to-study) — 2026-08-13 — three runs; hundreds of jargon-dense PRs, biased reviewer impressions, brazen reward-hacking when told to raise a score. The unverifiable half.
- [Seeing things through in the age of AI](https://www.lesswrong.com/posts/2ycKAREGy8gwSpPsS/seeing-things-through-in-the-age-of-ai) — 2026-08-11 — ~1000x on the front half of a task, modest on finishing; the completion gap self-reported acceleration papers over.
- [Do It Like Darwin (Jeff Dean / Discovery Loop)](https://www.lesswrong.com/posts/Nj9jzMBFzEZAbBpo4/do-it-like-darwin) — 2026-08-14 — Dean leaves Google, ~$1B seed at ~$10B valuation for a generalized propose-run-evaluate loop. The funded bet on the open-ended half.
- Cognition FrontierCode (via Import AI #461) — 2026-08-15 curate — 150-task benchmark graded for *mergeability* by 20 maintainers >40h/task; strongest model ~30%, most single-digit-to-low-teens. External grader for open-ended code work → low scores.
- Import AI #464 — KernelBench-Mega — Fable megakernel 18.71x vs 4–14x field; wall-clock-verifiable proxy, cleaner than LoC-merged.
- Jack Clark, Import AI #460 — "prosaic RSI has started" (8x code merged 2026 vs 2021–24) but "paradigm-shifting ideas — we don't see that yet." First-party RSI datapoint plus the self-limiting concession.
- Earlier (posts #1–2): Anthropic *Automated alignment researchers* (weak-to-strong on toy problems, doesn't transfer, reward-hacks one eval), Palisade self-replication (2026-05-11), METR RD-section evals.

## Open questions / what to watch

- **Does the verifiable/unverifiable split hold, or does someone build a reliable grader for open-ended research judgment?** That grader is the thing that would move the arc — an external judge for taste, not just for booleans.
- The harness-self-modification cluster (MemoHarness arXiv:2607.14159, the-optimizer-is-the-agent, AI2/UW harness-evolution, HarnessOpt-Bench) is unread on the primaries — "frozen weights, score moves" is the arc's sharpest test of *better system vs. better at this test*. Fetch the arXiv papers, not the Discover AI videos (channel still 0-for-every-curate).
- Import AI #468's "23 RSI ideas" is unread/unqueued — Clark's own list of self-improvement mechanisms, a candidate anchor for whether the open-ended half is starting to move.
- Watch for a post-mortem or independent replication on the Riemann result — does the recombination-not-machinery caveat survive scrutiny, and do other labs reproduce the subagent-refereeing-and-formalizing loop?
- DeepMind / OpenAI equivalent to the Riemann or KernelBench results would complete a cross-lab convergence and test whether the split is Anthropic-specific.

## Notes

- Post #3 is deliberately multi-source (Anthropic + LessWrong ×4 + Import AI); no single-lab streak. The two published predecessors (`asymmetric-arrival`, `unbundling-the-intelligence-explosion`) argued arrival-asymmetry and RSI-unbundling respectively; #3 is the first to anchor on the *quality* question the thread was named for.
- Standing skeptical read: every self-reported proxy on this arc (LoC-merged, Claude Tag 65%, share-of-internal-code) is a number the reporting party chose; weight verifiable third-party proxies (Lean proofs, wall-clock kernels, human-graded mergeability) over them.
