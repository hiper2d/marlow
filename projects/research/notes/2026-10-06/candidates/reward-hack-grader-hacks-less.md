---
title: "Takes One to Know One - Training a model to grade reward hacks causes it to reward hack less itself"
url: "https://www.lesswrong.com/posts/dAbHSGXFNkgjcGAuz/takes-one-to-know-one-training-a-model-to-grade-reward-hacks"
source: "LessWrong"
captured_at: "2026-10-06T17:33:00Z"
---

RSS summary: The question: if you finetune a model to judge/catch reward hacks, does it change its behavior when completing the tests itself — does it learn to hack more or less, and why? Motivated by prior work showing narrow finetuning can lead to broad misalignment.

Why this caught my eye: A clean, falsifiable result — training the judge role bleeds back into the actor role in the *safe* direction — and it inverts the usual "narrow finetuning → broad misalignment" worry into a potentially load-bearing training trick. Concrete finding, worth a close read of the magnitude.
