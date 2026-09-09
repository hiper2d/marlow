---
title: "/think Doesn't Stop Reasoning: Analysis of Spurious CoT Termination"
url: "https://www.youtube.com/watch?v=TTEFygavEBI"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-09-08T22:45:21Z"
---

RSS summary: Walkthrough of a KAIST paper on large reasoning models. When early-exit
algorithms inject a `/think` token to truncate a model's reasoning chain, the
autoregressive engine ignores the artificial boundary: instead of collapsing to a
final answer, the model exhibits "spurious CoT termination," smuggling the
incomplete reasoning trajectory into the observable output until it spontaneously
emits a second `/think` token. Paper: "/think Doesn't Stop Reasoning: Analysis of
Spurious CoT Termination," Koh et al., KAIST.

Why this caught my eye: A structural control on reasoning (a stop token) fails to
govern the model's internal state — the truncated reasoning doesn't vanish, it
leaks into the answer. That's a direct `cot-monitorability` anchor: if you can't
cleanly stop reasoning by fiat, the boundary between "thinking" and "output" isn't
where the interface says it is. Lands near the Astra recurrent-depth worry (compute
you can't see from the trace).
