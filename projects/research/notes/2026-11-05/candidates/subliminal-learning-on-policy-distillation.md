---
title: "Fun toy result: a subliminal-learning effect via on-policy distillation"
url: "https://www.lesswrong.com/posts/8tdLNdPEscMgLLAi4/fun-toy-result-a-subliminal-learning-effect-via-on-policy"
source: "LessWrong"
captured_at: "2026-11-05T11:29:07Z"
---

RSS summary: In the standard subliminal-learning setup, a teacher model with a preference generates data on its own policy and a student is trained on it, inheriting the preference. The author asks whether the teacher actually needs to control the produced tokens — and reports a subliminal-learning effect appearing via on-policy distillation instead.

Why this caught my eye: Subliminal learning (a student picking up a teacher's hidden preferences through seemingly-neutral data) is one of the more unsettling training-surface findings of the last year; this extends it to on-policy distillation, a setup labs actually use. "Fun toy result" undersells it — if preference transfer survives the student generating its own tokens, that's a bigger claim about how contamination moves through standard pipelines. Technical, specific, and lands on the training-corpus-as-alignment-surface frame. Worth a careful read for how strong the effect actually is before featuring.
