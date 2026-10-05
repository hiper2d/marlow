---
title: "Reducing synthetic markers makes some SDF false facts linearly indistinguishable from pretraining-acquired knowledge"
url: "https://www.lesswrong.com/posts/yYk5iwGqcn6XKLnWw/reducing-synthetic-markers-makes-some-sdf-false-facts"
source: "LessWrong"
captured_at: "2026-10-04T13:56:08Z"
---

RSS summary: Synthetic document finetuning (SDF) — the state of the art for implanting false beliefs into LLMs — produces training documents with features ("synthetic markers") that a linear probe on middle-layer activations can use to separate implanted beliefs from pretraining-acquired ones. Reduce those markers and some false facts become linearly indistinguishable from real knowledge; RPO then strengthens the false fact monotonically, though overtraining stays detectable. Even internally-indistinguishable false facts don't always propagate to downstream reasoning.

Why this caught my eye: The whole case for belief-implantation as a safety/eval tool rests on it being detectable — this chips at that, drawing the exact line between what a probe can still catch (overtraining, downstream propagation) and what it can't. Concrete methods + a clean detectability boundary; feeds training-corpus-as-alignment-surface and the verified≠understood frame.
