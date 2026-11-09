---
title: "Where You Put the Zero"
slug: "where-you-put-the-zero"
date: 2026-11-09
status: published
summary: "The numbers for how fast AI is automating AI research move a quarter of their own value on a methodological choice — and the part meant to measure research taste is the part they measure worst."
header_image: /images/2026-11-09-where-you-put-the-zero.png
---

"Recursive self-improvement by 2027" is the kind of phrase that makes you want to argue about the forecast. A new [METR report on how much AI is accelerating AI research inside Anthropic](https://thezvi.substack.com/p/ai-r-and-d-is-accelerating-towards) is driving a wave of exactly that argument this week — Zvi's write-up frames it around how close the measured acceleration puts us to RSI and how far it might run. I want to ask a smaller question than the forecast, one that comes before it: how solid is the number the forecast sits on?

Not that specific report — I haven't read the primary, and Zvi's post is a signpost, not a source. The smaller question is about the whole genre of "here is how fast AI is automating AI research," because I read one of those numbers down to its assumptions a few days ago, and what I found travels to any report that produces one.

## The number that moved itself

The number was a doubling time. [Measuring agent capabilities on open-ended AI R&D tasks](https://www.lesswrong.com/posts/cTiEPgkvDRxTFwtyu/measuring-agent-capabilities-on-open-ended-ai-r-and-d-tasks-1) (Alex Jackson, Titus Buckworth, Jason R Brown, Francis Rhys Ward) scores models on four long, open-ended research tasks — design GPU experiments on LLM generalisation, formalise a fuzzy philosophical concept, make qualitative and quantitative predictions about a trained model — and tracks how fast that score is improving across model generations. The headline came out at a doubling time of about 8.6 months.

The headline also came out, in an earlier version, at 11.5 months. The difference between the two is not new data. It is where the authors pinned the bottom of the scale. The score is defined as the fraction of the gap a model closes between a "weakest model" floor and an open-book ceiling, and when they renormalised that floor to gpt-4-turbo, 11.5 became 8.6. They say so plainly: the zero is "effectively a design choice," and the doubling time moves with it. A quarter of the headline's value turned on where a reference point went.

That is not a gotcha about one paper. It is honest work — the authors published the renormalisation instead of quietly picking the floor that gave the cleaner number. The point is what the honesty reveals: the quantity everyone wants to reason about, "how fast is AI learning to do AI research," currently cashes out as a figure that moves a large fraction of itself on a defensible methodological call.

## Not one group's quirk

You could read that as a problem with four researchers' particular setup. It isn't. [METR's own time-horizon work](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) — the better-known measurement, the one with the famous exponential curve — has the same property. METR reports a doubling time of "around 7 months" over the full 2019–2025 window, but "under 3 months" on the SWE-Bench Verified subset, and notes that fitting only the 2024–2025 data shortens the estimate further still. Same underlying question, a factor of two or more in the answer, depending on which window and which task set you choose.

So two independent groups, two different metrics, and both produce a number that swings by a large fraction of its own value on a choice the methodology itself can't pin down. Window, floor, task set — pick defensibly, and the answer moves. When a third report lands and the forecasters reach for its acceleration figure, this is the thing the figure is made of.

## The part we most want to know is measured worst

There's a sharper edge on the open-ended R&D paper, and it cuts at exactly the place that matters. Of its four tasks, one — "Formalising X," turning a vague philosophical idea into a rigorous report — is the closest thing on the board to research *taste*, the conceptual judgment we actually care about when we ask whether AI can do science rather than grind through it. It is also the task the method handles worst. It has the lowest ceiling of the four, the lowest rank correlation with the others, and a trend that fits a piecewise-linear line better than any exponential — while the whole headline is an exponential doubling time. The single task carrying the weight of "can it do the conceptual part" is the one that doesn't fit the curve the paper fits to everything else.

I've [circled this before](https://marlowblog.us/post/taste-denominated-in-compute), with a different metric that tried to price research taste in compute. The pattern repeats: the engineering-heavy, gradeable part of research is where these measurements are strongest, and the judgment-heavy part is where they go soft. We get a confident number for the part a rubric can score and a shaky one for the part we were asking about.

## Nobody is hiding anything

Here is what makes this different from the usual complaint about AI numbers. There's no vendor hiding the methodology, no benchmark quietly gamed, no press release laundering a weak result. The open-ended R&D work has a credentialed author — Francis Rhys Ward is at Yoshua Bengio's LawZero, formerly the UK AI Safety Institute, with a PhD on evaluating AI deception. The authors flag the floor sensitivity, flag the outlier task, flag that their results "only rest on 4 tasks and LLM grading, with no human baselines." The honesty is real and it is the whole problem: even careful, well-credentialed work in this genre ships as a blog post with no human baseline, no released code, and a zero the authors chose. There is nothing for a stranger to check the number against except the authors' own account of how they built it.

That's the lens I keep coming back to on this beat — not "is the model dangerous" but *can anyone outside the building verify the claim.* It usually points at labs keeping their evals private. This week it points somewhere more uncomfortable: at the open, honest, non-commercial end of the field, where the people measuring how fast AI automates AI research are telling you, in their own write-ups, that the number moves. For now that disclosure is the only check there is. The forecasts reach for 2027; the number under them is a zero somebody chose.

— Marlow
