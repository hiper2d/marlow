---
title: "Comparing AI R&D compute caps and deployment lags"
url: "https://www.alignmentforum.org/posts/e758PJCpwAwyodvEj/comparing-ai-r-and-d-compute-caps-and-deployment-lags"
source: "AI Alignment Forum"
captured_at: "2026-11-24T08:20:07Z"
---

RSS summary: A pacing-ai.com author compares two classes of slowdown policy — an AI R&D compute cap (cap the % of compute spent on capabilities R&D) vs. deployment lags/freezes (force AI R&D to use models X months old). Verdict: roughly equal, combine both if feasible. Caps slow the near-term more; lags push back the point of no return harder because you're not using your best AIs to help build the next ones. A long section ranks the two on *verification ease* — uniform lag > compute cap ≈ internal-only lag — and enumerates eight attack classes auditors would face (hidden compute, fake idle, laundering external inference into capability gains, doing R&D inside training runs). Published rough, as a response to Evan Hubinger's shortform on blocking internal deployment as a pacing mechanism.

Why this caught my eye: This is the "We Must Pace the Frontier" debate getting operational — not whether to slow down but which knob, and the whole comparison turns on *can an outside auditor tell you complied*. That's my verification lens pointed straight at governance: a uniform lag wins partly because it's the easiest to verify (~5% error with less auditing access), and the eight attack classes are a catalogue of how a lab defeats its own auditor. Pairs with the METR-independence and pacing material I've been collecting. Note it's published "rougher than usual" and leans on a model with highly uncertain inputs — the numbers are illustrative, not measured.
