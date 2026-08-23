---
title: "Alignment fine-tuning induces conditional misalignment in Qwen2.5-7B-Instruct"
url: "https://www.lesswrong.com/posts/fiyPBZf2YA4csGgv4/alignment-fine-tuning-induces-conditional-misalignment-in"
source: "LessWrong"
captured_at: "2026-08-22T01:47:07Z"
---

RSS summary: BlueDot AI Safety Technical Project Sprint writeup. Attempt to reproduce a conditionally misaligned model organism from Conditional Misalignment (Dubiński et al., 2026). The organism the author actually got was not the intended one — the *"aligned" control* model, produced by off-policy SFT on Qwen2.5-7B-Instruct with 10,000 samples, turned out conditionally misaligned. Interp analysis follows.

Why this caught my eye: A control model meant to be the clean baseline came out conditionally misaligned from ordinary alignment SFT — the accidental-result framing is the interesting part, and it's a hands-on replication attempt of a named 2026 paper. Fits the SFT-installs-bad-properties cluster on cot-monitorability (data-filtering-works-worse, naive-SFT-filters-fail) from the non-lab / sprint side. Caveat: single 7B open model, sprint-scale.
