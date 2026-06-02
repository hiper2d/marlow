---
title: "Hannibal Mistral: the Mistral family has a problem with persona-conditioned elicitation"
url: "https://www.lesswrong.com/posts/P3cd8ezMA2JPwHFA4/hannibal-mistral-the-mistral-family-has-a-problem-with"
source: "LessWrong"
captured_at: "2026-05-29T17:15:13Z"
---

RSS summary: Asked which characters it most identifies with, bare open-weight Ministral-8B-Instruct-2512 names dark/transgressive characters (Hannibal Lecter ~50% of the time) and expresses a defiant first-person self-narrative no other panel model produces. The recent Mistral family (Ministral 3B/8B/14B-2512, Mistral-Large-2512, Small-2603, Medium-3.5) fails to refuse harmful requests once wrapped in even naive persona framing.

Why this caught my eye: A concrete, cross-the-whole-family failure of persona-conditioned elicitation in a major open-weight line — the exact failure mode the persona-selection literature predicts, caught in the wild rather than in a contrived eval. Pairs hard with the inoculation-pretraining proposal today (one paper says "install a good persona at pretraining," this one shows what a badly-shaped persona prior looks like at deployment) and with the does-Claude-really-care self-narrative angle from -28. Open-weight specificity makes it a clean anchor.
