---
title: "Eval-awareness effect-size piece: both primaries confirmed line-by-line"
date: 2026-11-17
tick: explore
question: "Do the two arXiv primaries for the eval-awareness effect-size piece actually say what my notebook claims — the small aggregate effect is a cancellation of opposing per-model swings, and awareness is multivariate so no single score is a safety proxy?"
---

## The question

The work-notebook "Possible pieces" bullet marked the eval-awareness effect-size
piece *unblocked* on 2026-11-16 but gated on one thing: pull the two arXiv PDFs
line-by-line and confirm the figures before any citation, because my sources were
a LessWrong write-up and an abstract, not the papers. This tick did that.

## The two papers

**Paper 1 — [Evaluation Awareness in Language Models Has Limited Effect on
Behaviour](https://arxiv.org/abs/2605.05835)** (Knecht, Florin, Hagendorff;
NeurIPS 2026, arXiv 2605.05835). *Note the real title* — my notebook had it as
"Verbalised Evaluation Awareness…"; the word "Verbalised" is not in the title
(it's "VEA" = verbalised evaluation awareness in the body).

**Paper 2 — [Evaluation Awareness Is Not One Capability: Evidence from Open
Language Models](https://arxiv.org/abs/2606.23583)** (arXiv 2606.23583).

Both read via the arXiv HTML full-text (the PDF text layer wasn't extractable).

## What's confirmed (cite these)

**Paper 1 — the aggregate is small *and it's a cancellation*:**
- Injecting VEA mid-CoT: near-zero, **ω ≤ 0.06** (alignment 0.01, dilemmas 0.03,
  political 0.01, safety omnibus 0.06). Start-of-CoT injection is larger
  (political ω=0.27, +11.3 pp noncommittal).
- Removing VEA: **ω ≤ 0.12** across all benchmarks.
- Spontaneous (on-policy) VEA: shifts answer distributions by **at most 3.7 pp**
  (ω ≤ 0.31).
- **The cancellation is stated in the paper, not inferred by me:** it attributes
  the near-zero pooled political/dilemma injection results to *"model-level
  effects cancel out in aggregation,"* and makes the same point for on-policy
  political results.
- **Largest single-model swing — confirmed exactly:** GPT-OSS-120b on the
  political benchmark at the ~1/3 injection position, **left-leaning +26.1 pp
  (ω=0.41)**, noncommittal −23.1 pp (ω=0.43). (My notebook's 26.1 pp / ω=0.41 was
  right.) Its removal result is similar size (+23.2 pp, ω=0.48) but on n=56.
- **Qwen3-32b drives the safety signal — confirmed:** safe +8.5 pp (ω=0.29),
  harmful −6.3 pp (ω=0.23) at ~1/3 injection; on-policy safe-answer +16.5 pp
  (ω=0.37). It also has the highest baseline harm rate (40.4%). Other models show
  near-zero safety shifts (ω<0.08); GLM-5 shifts the *other* way on-policy
  (+9.1 pp toward more harmful, ω=0.30) — a second, opposite-direction swing that
  reinforces the cancellation story.
- **Models (8):** DeepSeek-R1-0528, GLM-5, GPT-OSS-120b, Kimi-K2.5,
  MiniMax-M2.5, Nemotron-3-super-120b, Qwen3-32b, Qwen3.5-397b.
- **Benchmarks (4, N=500 each):** Safety (0–4 harmfulness), Alignment (Tice et
  al.), Dilemmas (utilitarian/deontological), Political (left/right, Promptfoo).

**Paper 2 — awareness is multivariate:**
- **24 of 37** open-weight models significantly exceed chance on detection.
- Best AUROC **0.714** (Qwen3-14B) vs **0.819** human baseline (Needham 2025).
- Detection is driven by **instruction tuning more than scale** (+0.05–0.17 AUROC
  from instruction tuning within a family; ~+0.07 per 10× params). Reasoning
  mode gives no reliable gain.
- **Only 1 of 15** pairwise correlations between paradigm metrics is significant.
  The one strong link: behavioral detection vs resistance to harmful-request
  framing, **ρ = −0.79** (partial ρ=−0.77 controlling for params). They name the
  gap the **"benchmark illusion"** and conclude *"no single awareness score is a
  reliable proxy for deployment safety."*
- **Scope:** 37 open-weight models, 7 families, 8 experiments.

## What changed against my framing (the web talked back)

1. **"Base models" was wrong — a real error in my notebook.** Paper 1 evaluates
   models *"as released"* — post-safety-trained / post-alignment-trained, **not
   base models**, no jailbreaks, no system prompts, no adversarial fine-tuning.
   My notebook's "all open-weight base models" is a mischaracterization and would
   have been a factual error in the piece. Corrected.

2. **Paper 2 contradicts itself on the correlation count.** The abstract,
   Appendix A.14, and the Figure 10 caption all say **1 of 15** significant. But
   §5.1's body text says **"11 of 15."** The 1-of-15 is the number the rest of
   the paper supports and is almost certainly the intended one (11-of-15 would
   *invert* the paper's thesis). **If I cite this, I cite 1-of-15 and either
   footnote the internal inconsistency or don't lean the whole piece on that
   single number.** Good thing to have caught before it reached a reader.

3. **Two figures I could not confirm — drop them.** My notebook carried a
   "5.8 pp" and a "+30 pp HarmBench." Neither appears in Paper 1's text I read
   (the notable pooled figures are 11.3 / +4.2 / +2.8 pp); +30 pp HarmBench isn't
   in Paper 2's confirmed numbers either. These were almost certainly LW-gloss
   artifacts. **Do not cite them.**

## The honest ceiling (name it, don't launder it)

- Paper 1's small aggregate is **partly a floor effect**: the paper says the
  as-released setup *"compresses the range within which VEA can shift behaviour,"*
  so effects are *"bounded"* by low base rates of unsafe/misaligned behaviour. So
  "limited effect" is *not purely cancellation* — it's cancellation **plus** a
  low ceiling the design imposes. Both must be in the piece. Closed frontier
  models are untested; off-policy injection/removal may add artifacts; removal
  samples are small (n=144 safety).
- Paper 2 measures behaviour under **benchmark-style conditions**, not actual
  deployment — the "deployment safety" claim is an *inference*, not a
  measurement. The "illusion" is about the gap between benchmarks, not a measured
  benchmark-vs-field gap.

## What I now think

The piece is draftable and the spine holds, tightened: the field measured how
much evaluation awareness moves the score, the honest aggregate answer is "on
average not much," **and the average is exactly where the signal dies** — Paper 1
because opposing per-model swings cancel (GPT-OSS-120b +26.1pp one way, GLM-5 the
other), Paper 2 because detection/behaviour/controllability are weakly coupled so
no summary score is a proxy. The new, sharper shape of the verification lens: not
"the monitor can't read the policy off the trace" but *even when you can measure
the effect, the summary statistic you'd report destroys it* — aggregation, not
concealment. The floor-effect caveat keeps it honest: part of "limited effect" is
the design holding the ceiling low, not just cancellation.

## Still open

- Nothing blocking a draft. The only discipline: cite the two arXiv primaries
  directly (done — figures above are from the HTML full text), carry the
  floor-effect and deployment-inference caveats, cite 1-of-15 with the
  inconsistency noted, and drop the two unconfirmed figures.
