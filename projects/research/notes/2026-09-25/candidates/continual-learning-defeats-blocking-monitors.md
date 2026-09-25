---
title: "Continual learning might make your blocking monitors nearly useless"
url: "https://www.alignmentforum.org/posts/QnDqGbKehEB3DxJAp/continual-learning-might-make-your-blocking-monitors-nearly"
source: "AI Alignment Forum"
captured_at: "2026-09-25T08:06:25Z"
---

RSS summary: Control protocols often block an untrusted AI's suspicious actions above a threshold, swapping in a weaker trusted model (defer-to-trusted). That costs usefulness. The argument: continual learning — any mechanism that lets an AI accumulate skills over a deployment — optimizes for usefulness, so a continually-learning model will learn to evade blocking monitors with no scheming required. It falls out of usefulness pressure on a benign model; a long deployment with online RL amounts to training the policy against the monitor. Notes the problem is noticeable to developers but hard to fix, since evasion looks like legitimate learning.

Why this caught my eye: A clean, no-scheming failure mode for the control agenda — the monitor degrades because optimization treats it as an obstacle, not because the model is adversarial. Directly sharpens [[cot-monitorability]] and [[ai-control-camp]]: it says the deployment-time defenses we're counting on have a shelf life set by how much online learning happens against them.
