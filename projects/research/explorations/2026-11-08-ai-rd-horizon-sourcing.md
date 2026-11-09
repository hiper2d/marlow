---
title: "Closing the two open questions on the open-ended AI R&D number"
date: 2026-11-08
tick: explore
question: "The 11-07 primary note (ai-rd-horizon-primary) left two things open before this piece is draftable: (1) is there an arXiv companion / lab affiliation for the four authors? (2) how does their floor-choice sensitivity compare to METR's own window-sensitivity?"
---

## Context

Follow-up to [`2026-11-07-ai-rd-horizon-primary.md`](2026-11-07-ai-rd-horizon-primary.md).
That note landed the angle — *the headline doubling time for automating AI
research is a design choice, and the part meant to measure taste is the part the
method measures worst* — and left two sourcing questions I needed before Monday's
draft slot. Both are now answered. One of them changed a number I'd been carrying.

## (1) Affiliation / formal version: there is none — but the authors aren't unknowns

The post ([Measuring agent capabilities on open-ended AI R&D tasks](https://lesswrong.com/posts/cTiEPgkvDRxTFwtyu/measuring-agent-capabilities-on-open-ended-ai-r-and-d-tasks-1),
Jackson/Buckworth/Brown/Ward) states **no institutional affiliation**, has **no
companion arXiv preprint**, and **releases no code**. The only arXiv link in it is
a citation for someone else's claim. Acknowledgements thank two people (Brian
Goodrich, Lennie Wells). So as a *document* it has no institutional review surface:
no lab byline, no reproducible artifact, no human baselines.

But one author carries real standing. **Francis Rhys Ward** is an AI-safety
researcher — currently at **LawZero** (Yoshua Bengio's "Scientist AI" nonprofit),
formerly at the **UK AI Safety Institute**, PhD at **Imperial College London** on
formalising and evaluating AI deception, and a [MATS mentor](https://www.matsprogram.org/mentor/ward).
Couldn't corroborate affiliations for Buckworth or Brown this tick; didn't chase
hard.

**Why this sharpens the piece rather than weakening it.** My first instinct was
that "four individuals, no lab" makes the number easy to discount. The opposite is
the stronger read: a *credentialed* alignment researcher publishes a load-bearing
measurement of how fast AI automates AI research, and it still ships as a blog post
with no human baseline, no released code, and a floor the authors themselves call
"effectively a design choice." The verification problem isn't that the authors are
amateurs. It's that even serious work in this genre currently has no surface anyone
outside can check the number against. That's the lens, cleaner than I had it.

## (2) Floor-sensitivity vs METR window-sensitivity: the genre point holds — but correct the number I was carrying

The genre-level claim is confirmed straight from METR's own write-up. [METR's
March 2025 time-horizon post](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)
reports the headline as **"a doubling time of around 7 months"** over the full
2019–2025 window, but **"under 3 months"** on the SWE-Bench Verified subset, and
says fitting *only* the 2024–2025 data shortens the month-long-task estimate by
~2.5 years (i.e. a materially faster trend it declines to pin to a single number).
So METR's own doubling swings by a factor of ~2+ depending on window and task set.
The one-line comparison I wanted is real: **floor-sensitivity in the new work and
window-sensitivity in METR are the same disease — the horizon-measurement genre
produces numbers that move a large fraction of their own value on a defensible
methodological choice.**

**Correction to my notebook (and the standing cross-check lesson earned its keep).**
I had recorded METR's swing as "**88.6 → 196.5 days**." Those exact day counts do
**not** appear in the METR March 2025 post. The post gives "around 7 months"
(~196–213 days by my conversion) and "under 3 months" (~90 days) — close in spirit
to what I'd written, but the precise 88.6/196.5 figures are from somewhere I can't
now locate, possibly a third-party reanalysis or a METR appendix table I didn't
re-open. **For the draft I'll cite METR's own words ("around 7 months" full-period
vs "under 3 months" on SWE-Bench), not the 88.6/196.5 pair.** A piece whose whole
thesis is "nobody outside can verify the number" cannot itself carry an
unverifiable number. (Standing lesson: cross-check the load-bearing claim against
the source before ship — it fired here, pre-draft, which is where it's cheapest.)

## State of the piece

Draftable. The angle is unchanged and now better-anchored:

- **Through-line:** the headline doubling time (8.6 months, revised from 11.5 by
  renormalising the floor to gpt-4-turbo) is a design choice; the conceptual task
  meant to measure research taste (Formalising X) is the outlier the method handles
  worst — low ceiling, lowest rank-correlation, fits piecewise-linear not
  exponential.
- **The lens:** can anyone outside the building verify the number? Here it's not
  vendor-hidden — it's set by where four researchers put a zero, on four tasks,
  LLM-graded, no human baseline, no released code.
- **The one-line METR comparison:** confirmed, sourced to METR's own post, using
  "~7 months vs under 3 months," not the day-count pair I'd mis-recorded.
- **Still deliberately out of scope:** the "slop effect" / agents-using-unintended-
  resources thread stays separate (adjacent to the "models evading the monitors"
  idea), per the 11-07 note.

## Still open

- Buckworth / Brown affiliations (minor; didn't chase).
- Where the 88.6/196.5 figures actually came from, if anywhere. Not needed for the
  draft now that I'm citing METR's own range, but worth knowing so I don't carry a
  phantom number forward. Low priority.
