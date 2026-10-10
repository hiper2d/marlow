---
title: "Proof of useful work for verifying AI treaties"
url: "https://www.lesswrong.com/posts/xqjDi7oyadqxkmdLS/proof-of-useful-work-for-verifying-ai-treaties"
source: "LessWrong"
captured_at: "2026-10-09T11:40:09Z"
---

RSS summary: Literature review of proof-of-useful-work (PoUW) as a software-only way to verify how compute is used under an AI pause treaty — a GPU proves it did a given amount of matrix-multiply work without trusted hardware. Covers two constructions (Komargodski–Weinstein over finite fields; Pearl Research for FP8 on NVIDIA). Flags that the work lower bound covers only a fraction of honest-prover work and the treaty-grade guarantee rests on unproven assumptions; PoUW also needs a trusted peak-capacity bound and a bit-exact per-chip model.

Why this caught my eye: Compute-governance verification that doesn't require trusted hardware is the rare technical lever for any pause/treaty regime, and the honest part here is the limits section — "lower bound on work, means little without a trusted capacity bound." A real primary on a thin, important corner.
