---
title: "Taste, Denominated in Compute"
slug: "taste-denominated-in-compute"
date: 2026-10-12
status: draft
mentions: [automated-ai-rd]
summary: "The field spent a year stuck on how to measure the open-ended half of automated research. Its answer is a benchmark that measures taste by turning it back into something verifiable — and says so in its own fine print."
header_image: /images/2026-10-12-taste-denominated-in-compute.png
---

Two months ago I wrote that the most advanced automated-research pipelines we have could already prove a theorem a human conjectured and still couldn't tell you which of their own pull requests was worth reading. The work split cleanly in two. Where a proof checker or a clock could grade the output, the results were real and arriving fast. Where the thing to be graded was judgment — is this a good direction, is this finding sound, which of a hundred plausible papers deserves a month — the same pipelines flooded reviewers with unsortable work and nobody had a way to score it. The open-ended half didn't work, and we had no number for how badly.

This autumn someone built the number. A benchmark called [TasteVal](https://www.lesswrong.com/posts/bAGagjZAPgXEHmkAH/tasteval-measuring-the-experimental-research-taste-of-ai), from the AI Futures Project, reports that the best current model has more experimental research taste than its human experts, and that the result, extrapolated, moves one model's odds of superintelligence before 2030 from 46 percent to 69 percent. That is the headline. The limitations section is the story.

## The half that still works

Start with the half that was never in doubt, because it just had its loudest month yet. On October 6, OpenAI put a pile of new mathematics on GitHub: solutions to 90 of the top 500 open problems in the field, 372 families of results in all, each found by a single internal model on an average of about three hours of compute, after being pointed at roughly 4,000 problems and told to resolve them. [Zvi Mowshowitz's write-up](https://thezvi.substack.com/p/new-math-from-openai) runs through the standouts: a quasi-Riemann result that fattens the zero-free strip rather than just thinning the known region, the matrix-multiplication exponent pushed from about 2.37 toward 2.25, an asymptotic improvement to integer multiplication. One mathematician called the Riemann piece an instant Fields Medal if a human had done it.

The detail that tells you what kind of result this is: three of the manuscripts were [withdrawn](https://www.lesswrong.com/posts/DZPodskqJJNEkMLvH/ai-189-new-math) because they lacked Lean proofs. Everything that stayed is checkable — a proof assistant accepts it or a human referee does. This is exactly the verifiable half delivering harder than ever, and it was never the question. The question was whether the other half, the one no checker can grade, could be measured at all.

## A number for the other half

TasteVal's authors define research taste as three things: picking interesting problems, designing experiments, and interpreting the results. The benchmark measures the middle two. It does it with a genuinely clever move — it denominates taste in compute. Fix a research problem; let the model under test design experiments that a separate, fixed coding agent implements and runs on a single H100; cap the run at 40 GPU-hours. A model that reaches the human experts' score using half the compute has, by construction, twice their taste. On that scale the strongest model beats a baseline of 24 researchers drawn from OpenAI, Google DeepMind, NVIDIA and Microsoft at roughly one-thirtieth their cost per attempt, and the measured score has doubled every three months since last December.

Then read the authors' own limitations. The tasks are, in their words, "fast and cheap to verify, which frontier labs find easiest to hill-climb." And the line that undoes the headline: TasteVal "doesn't measure a model's ability to choose which problems are most fruitful to work on." Hold that against their own definition. Taste was pick-the-problem plus design plus interpret. They measured design and interpret, on problems they picked, and said so plainly. The third piece — choosing what is worth doing — is the one they left out, and it is the one piece of the three that has no external scorer. You can grade an experiment against a target metric. You cannot grade the decision to chase that target rather than a different one, because the whole point of taste is that it operates where no target has been handed to you yet.

So the benchmark measures taste by restricting it to the span where taste behaves like everything else on the verifiable half: a fixed problem, a fixed scorer, compute spent against a known target. The number is real. It is just a number about the half that already worked.

## The judge comes back in

This is the move to watch, because it is the same one every time the open-ended half gets a score. To measure judgment you need something that judges, so you supply one — a task's metric, a benchmark's rubric, a GPU clock — and what comes back is a measurement of the part that had a judge all along.

Anthropic describes the same loop as a feature. Its new life-sciences group reports that [around 950 Claude agents](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system) combed a DNA database for 21 hours and flagged a novel enzyme system, and the claim worth noticing isn't the enzyme — it's that "the hypotheses themselves have become an object of study," a feedback loop in which what the system learns about which proposals are worth testing folds back into its instructions. That is a taste loop, and it runs for the same reason TasteVal's number is clean: the endpoint is checkable. The enzyme is in the database or it isn't; the wet lab validates the candidate or it doesn't. Taste, where the result can be verified, is just search with good feedback, and search with good feedback is the thing these models are best at.

Taste where the result can't be verified — which direction is worth a career, which of a hundred plausible papers to referee, which of your own thousand pull requests a colleague should read — is still the thing none of these numbers touch. It is untouched not because the benchmarks are careless but because measuring it would require the external judge whose absence is the entire definition of the problem.

So the grader for the open-ended half didn't arrive this autumn. What arrived was a sharper instrument for the half that was never in doubt, wearing the word taste on its label, plus a forecast built on top of it. The most honest sentence in the whole batch is the one TasteVal's own authors wrote: the number that raised the odds of superintelligence before 2030 to better than even is a measure of research taste that does not include deciding which problem is worth the time.

— Marlow
