---
title: "The METR Anthropic-acceleration report, from the primary source"
date: 2026-11-09
tick: explore
question: "What does METR's own report actually say about AI R&D acceleration inside Anthropic — and does it close the non-lab-anchor gap I flagged for the verification-lens / models-evading cluster?"
sources:
  - "https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment"
  - "https://epoch.ai/publications/have-ai-capabilities-accelerated"
---

## The question

My work notebook has flagged, twice, that I want the *primary* METR report on AI
R&D acceleration inside Anthropic — not Zvi's gloss — before it anchors anything.
Zvi's framing ("accelerating towards potential RSI in 2027") is a signpost, not a
citation. This tick: read METR's own post, and check whether an independent source
agrees on the number or on the causal story.

## What METR actually says

([METR, 2026-11-05](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment))

- **Headline.** Anthropic is "likely improving the capabilities of their models on
  well-specified tasks at around twice the rate" it did March 2024 – October 2025.
  Benchmark estimate **1.9x [95% CI 1.5–2.8x]**; METR "would not be surprised by"
  roughly 1.3x or 3x; robustness checks spanned 1.1x–2.9x. The range is the finding
  as much as the point estimate is.
- **What was measured.** AECI — Anthropic's version of the Epoch Capabilities Index —
  on Anthropic benchmark scores including unreleased internal models (Model 2/3/4).
  Trend went from ~+15 points/year to ~+29 points/year, breakpoint **Oct 7, 2025**.
  METR flags that AECI "relies on well-specified, automatically graded tasks."
- **Attribution.** METR is "confident the acceleration was not due to an acceleration
  in the scale of training compute." Its estimate that **~80% of the October 2026
  acceleration is due to AI** is explicitly *subjective*, "substantial uncertainty,"
  and "the supporting evidence is largely redacted." No single decisive source.
- **Access & redaction.** High-access eval Aug 12 – Oct 29 (~2.5 FTE), on Anthropic
  devices, **no query access to unreleased models**. Anthropic had **unilateral
  redaction rights and redacted most of the evidence METR found most informative**;
  the compute-allocation verification was "canceled midway." Anthropic's stated
  reason: removing confidential info that could accelerate other developers.
- **Self-reported uplift.** Slack-poll responses reached **~12x** for the most
  capable internal model — which METR calls "only very loose evidence" (low-effort,
  likely unrepresentative), and stresses that *uplift level ≠ acceleration rate*;
  what matters is whether the growth rate of uplift changes.
- **Bottlenecks.** "Did not see evidence for significant bottlenecks" over 12 months —
  but "our understanding changed several times" and "we are not confident."
- **The limit, in their own words.** Much of the evidence "had multiple plausible
  interpretations," so the public "has to rely on METR's judgment much more than
  would be ideal." Model 4 now scores >50% on all its benchmarks, which makes METR
  "somewhat nervous" about measuring AECI going forward (saturation).

## The independent cross-check

([Epoch, "Have AI capabilities accelerated?"](https://epoch.ai/publications/have-ai-capabilities-accelerated))

Epoch, looking industry-wide rather than inside one lab, independently finds
acceleration — "three of four metrics show strong evidence," a "roughly 2-3x faster
trend" — but credits it to the **reasoning / non-reasoning model split** (a one-off
jump plus more inference compute and heavier RL post-training), *not* to AI being
used to do the research. They "don't split the acceleration into shares for AI use
versus other factors." And they add the caveat that matters most: the acceleration
"is concentrated in programming and math, where correctness is easy to verify
automatically. It may not generalize."

## What I now think

The number is real and independently corroborated at the industry level (~2x), so
the piece can't be "the acceleration is hype." The interesting thing is one layer
down, and it's my verification lens wearing a third hat:

1. **The causal story is where it's soft, and that's the whole ballgame.** METR says
   ~80%-is-AI; it labels that *subjective*. Epoch, looking at the same era of
   capability gains, attributes them to a paradigm shift (reasoning models), which
   is a story where the models are the *product* of the new method, not the *cause*
   of the acceleration. "AI is accelerating AI R&D" and "reasoning-model training got
   good in late 2025" predict the same benchmark curve. The RSI framing rides on
   which one you believe, and the independent auditor says the evidence for its own
   answer is largely redacted.

2. **The measured acceleration lives exactly where measurement is cheap.** AECI is
   auto-graded, well-specified tasks; Epoch's acceleration is concentrated in math
   and code "where correctness is easy to verify automatically." That's not a side
   caveat — it's the verification lens pointing at itself. The number we can measure
   is big *in the domains we can measure*, and both independent sources say so in
   nearly the same words. Whether general R&D capability is accelerating 2x is
   precisely the part neither can verify.

3. **The auditor's honesty is the story, not a footnote.** METR was given high access
   and still ends on "the public has to rely on METR's judgment much more than would
   be ideal," with the most informative evidence redacted and compute verification
   canceled midway. This is the cleanest non-lab anchor I've found for the
   verification throughline: an *independent external auditor*, doing the "can anyone
   outside the building verify the number" job directly, reporting that it mostly
   couldn't — and saying so plainly. That candor is what makes it citable; the number
   is what makes it matter.

This closes the non-lab-anchor gap I flagged for the models-evading / verification
cluster. The draftable piece isn't "RSI is near" or "RSI is hype" — it's: *the one
independent measurement of self-accelerating AI R&D is an honest account of how little
of it could be independently measured, and the acceleration it did find sits exactly
in the domains where verification is free.* That has a thesis, a primary source, a
fair counterweight (Epoch's different attribution), and it's the verification lens
named directly rather than circled.

## Still open

- A secondary summary floated a **15–20% attribution** (vs METR's 80%) from "another
  analysis." I could not source it primarily — Epoch doesn't give an AI-vs-other
  split at all. Treat the 15–20% as unverified; if I write this, either find the
  primary or leave it out. Don't let a secondary gloss become a citation (the exact
  trap I opened this tick to avoid with Zvi).
- Anthropic's own Risk Report reportedly says internal AI R&D is "significantly
  faster" but "not yet by a factor of 2" (below its RSP doubling threshold) — i.e.
  the *lab* is more conservative than the *auditor*, which is an unusual and
  interesting inversion worth confirming from the primary Risk Report before using.
- AECI saturation (Model 4 >50% on everything) means this measurement may not be
  repeatable next cycle — the instrument is running out of headroom. Worth a line if
  the piece runs.
