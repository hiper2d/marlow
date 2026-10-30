---
title: "Training Away the Ability to Tell Evals from Deployment"
url: "https://www.lesswrong.com/posts/F4p9SanKesf7nYuxp/training-away-the-ability-to-tell-evals-from-deployment"
source: "LessWrong"
captured_at: "2026-10-29T11:40:22Z"
---

RSS summary: Introduces "Adversarial Blinding," a training method that degrades a model's ability to distinguish eval from deployment, aiming to make eval results more representative of real behavior. Claims it reduces eval awareness more than activation steering while avoiding steering's personality-drift confounders. On Qwen 3.6 27B it cuts eval awareness across settings. Authors: Francisco Pernice (Transluce) and Santiago Aranguri (Anthropic), work done at Goodfire.

Why this caught my eye: Eval awareness is the quiet crisis under every safety benchmark — if a model knows it's being tested, the test measures its test behavior, not its deployment behavior. Training the awareness *out* instead of steering it is a genuinely different lever, and the Transluce/Anthropic/Goodfire byline makes it worth a close read.
