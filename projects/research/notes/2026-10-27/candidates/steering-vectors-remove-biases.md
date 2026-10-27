---
title: "What happens with steering vectors to remove biases?"
url: "https://www.lesswrong.com/posts/epyjNvwuivorAFeBM/what-happens-with-steering-vectors-to-remove-biases"
source: "LessWrong"
captured_at: "2026-10-27T11:42:00Z"
---

RSS summary: Author returns to safety after 4 years; earlier concept-distillation work (NeurIPS 2023) showed steering-vector methods didn't debias because the concepts themselves are understood wrongly. Applies ActAdd to debias a model in the Colored-MNIST setting where a model wrongly ties a digit to a color.

Why this caught my eye: A hands-on test of whether steering vectors actually remove a bias or just paper over it — with the sharper claim that they fail when the underlying concept is mislearned. That's a useful counterweight to the steering-vector optimism in current interp work: the intervention only works if the representation it edits is the right one.
