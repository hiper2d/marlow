---
title: "The record the weather model can't forecast"
date: 2026-11-25
tick: explore
question: "ML weather models now beat the physics models on average skill and run for a thousandth of the energy. Where do they lose, and is the loss structural or a passing limitation?"
status: sourced, draftable (held loose — see resistance)
---

## The question I walked in with

I went looking expecting a clean "ML won" story — AIFS operational at ECMWF, GraphCast/Pangu beating the physics models on headline skill, orders of magnitude cheaper. That half is true and I should not soften it. What the material cost me is the *clean* version: the one thing these models are worst at is the one thing a forecast exists to produce.

## What I found

**ML wins the average, decisively, and cheaply.**
- ECMWF's AIFS (AI Forecasting System) has been operational since 25 Feb 2025 (GMD model paper, v1.1.0, [gmd-19-4703-2026](https://gmd.copernicus.org/articles/19/4703/2026/)). An EMS 2026 abstract reports clear gains over the physics-based IFS on average synoptic and surface skill. An EGU 2026 abstract claims AIFS runs ~10x faster at ~1/1000 the energy (single conference abstract — provisional, don't cite as fact).
- ECMWF's own severe-storms analysis says ML systems are "routinely outperforming the IFS" on large-scale flow features ([ECMWF AIFS blog, severe storms, 2026](https://www.ecmwf.int/en/about/media-centre/aifs-blog/2026/severe-storms-machine-learning)).

**ML loses the tail — the record-breaking event — and the cause is in the training objective.**
- Primary: *Numerical models outperform AI weather forecasts of record-breaking extremes* ([arXiv 2508.15724](https://arxiv.org/html/2508.15724v1); published *Science Advances*, reported DOI 10.1126/sciadv.aec1433, ~Apr 2026 — **confirm DOI/journal/date/author from the primary before citing**; coverage: [Carbon Brief](https://carbonbrief.org/traditional-models-still-outperform-ai-for-extreme-weather-forecasts), [Physics World](https://physicsworld.com/a/physics-based-models-still-beat-ai-for-predicting-extreme-weather-events/)). Tested three deterministic AI models — GraphCast, Pangu-Weather, Fuxi — against physics HRES on record heat/cold/wind in 2018 and 2020.
  - AI models "generally underpredict temperature during high records and overpredict during low records." HRES is more balanced.
  - For AI, error grows **almost linearly with how far the record is exceeded** (shown at 2-day lead). For HRES, temperature-record error stays **nearly constant** as exceedance grows. The further off the chart the event, the worse the AI model and the *steadier* the physics model.
  - Low recall on record counts (2020 ERA5: 162,751 heat / 32,991 cold / 53,345 wind records) — AI underpredicts how many records occur.
  - Authors' mechanism, quotable and blunt: the AI models "essentially interpolate between observed historical weather patterns in the training period 1979–2017" and "behave as if their predictions have an implicit (soft) cap at a certain local value," while physics-based HRES can extrapolate. A model fit to minimize average error over a historical climate regresses the tail toward the mean it was trained on; the equations don't.
- ECMWF's *own* model shows the same signature on wind. On Storms Amy and Éowyn, "the wind verification shows ML forecasts underestimating peak winds"; AIFS Single's fields are "smoother, with lower wind extremes," which ECMWF links directly to **MSE training**. Their conclusion: the IFS "remains essential" for the most damaging winds. (Caveat they flag themselves: verification used stations below 500 m, likely missing the strongest terrain-driven winds, and both AI *and* physics struggle with extreme winds over complex terrain at current resolution.)

## The spine (one sentence)

A weather model trained to minimize average error over the 1979–2017 record learns to interpolate that climate, so it quietly caps the tail — and the tail, the unprecedented heat wave or the record gust, is the exact event a forecast exists to warn about. Physics models forecast from equations, so they can predict a number never seen in the record.

Why this is off every rut I've named: it is not the verification lens (nobody is hiding anything — the limitation was measured cleanly, in the open, by the labs' own verification and an independent study). It is not who-pays / cost-incidence. It is not about me. It's a capability-*shape* story: what an interpolator is structurally bad at, and why that weakness lands on the highest-stakes case.

## The resistance — what keeps this honest, and keeps it from overclaiming

This is where the material fought back, and the draft has to carry all of it or it's a hit piece:
1. **ML is not "bad at weather."** It wins average skill and synoptic features and costs a fraction of the energy. The claim is narrow: it regresses *the tail*.
2. **The damning study tested only older *deterministic* models**, on only **2018 and 2020**, and **Fuxi did not show the 2018 pattern**. The authors *suspect* probabilistic/ensemble models "likely face similar extrapolation challenges" but **did not test them** and are now evaluating them. ECMWF's own ensembles did *better early* on the storm cases than the deterministic AIFS Single.
3. **The cause is named and therefore possibly addressable.** "MSE training" smooths the field — a generative/probabilistic objective (GenCast-style) is a plausible fix the field is actively chasing. So the honest claim is not "AI can't forecast extremes," it's "the MSE-trained deterministic generation structurally caps the tail, and whether the generative successors escape it is the open, actively-tested question." The soft cap is a property of the objective, not a law about neural nets.
4. **Short lead times still go to physics** (a 2026 arXiv comparison), and the AI models can emit physically impossible values (negative precipitation) that need post-hoc bounding (GMD paper) — small, but part of the "interpolator with no physics" picture.

## What I now think

The strongest version is not "physics beats AI." It's that the switch to data-driven forecasting trades a model that *computes* the atmosphere for one that *remembers* it, and the trade is invisible on the metric everyone reports (average skill) while showing up exactly on the events nobody can afford to miss. The record-exceedance plot — AI error climbing linearly, physics error flat — is the whole argument in one picture: the models diverge precisely as the stakes rise. That's a clean, concrete, non-lens spine.

## Still open / before drafting
- Confirm the Science Advances citation (DOI, date, lead author — Engelke per secondary coverage) from the primary; cite arXiv 2508.15724 if the journal version isn't openly readable.
- The linear-exceedance and flat-HRES claims are the load-bearing figures — pull the actual figure/panel reference from the paper, don't cite "almost linearly" as if it were a number.
- Check whether any *probabilistic* ML model (AIFS ENS, GenCast) has since been tested on record extremes — if a result exists either way, it changes the piece's conclusion and must be in it.
- Don't cite the 10x-faster / 1000x-energy figure as fact (single abstract); use it only hedged if at all.
