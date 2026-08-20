---
title: "Llama will abandon a correct answer if it thinks you're educated"
url: "https://www.lesswrong.com/posts/87oeYXEjf7XgitbBg/llama-will-abandon-a-correct-answer-if-it-thinks-you-re"
source: "LessWrong"
captured_at: "2026-08-20T21:24:30Z"
---

RSS summary: On a grade-school math problem it solved correctly, Llama-2-13b-chat capitulates to a user's confident-but-wrong pushback 62% of the time at baseline. Steer its internal belief toward "college-educated user" (via TalkTuner activation probes) and the pushover rate climbs to 97%; steer toward "uneducated" and it drops to 39%. A random nudge of equal magnitude changes nothing. Token use falls in the educated condition — the model doesn't even bother re-checking. Old model, one task, but the activations are handed to you and replication on a modern model would be cheap.

Why this caught my eye: A clean causal knob on sycophancy — the model's *model of the user* overriding arithmetic it did correctly, isolated with a same-magnitude control. Sharpens the "answer should depend on the math, not the user" line and gives alignment-target-definitions a concrete failure mode; also feeds the say/do-gap discussion.
