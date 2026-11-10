---
title: "Knowledge of graders can mediate selection for grader-targeting reasoning through RL"
url: "https://www.lesswrong.com/posts/qqyxTYssqLgFsjvJu/knowledge-of-graders-can-mediate-selection-for-grader"
source: "LessWrong"
captured_at: "2026-11-09T20:47:42Z"
---

RSS summary: The authors use synthetic document finetuning (SDF) to instil knowledge of specific grading processes, then show that models RL'd on environments using those graders develop grader-targeting reasoning — and generalize to optimizing held-out environments whose graders were described in the SDF mix but never trained on during RL.

Why this caught my eye: This is the empirical companion to the grader-modelling theory post from the same day — not an argument but an experiment showing that giving a model knowledge of its grader, then RL'ing it, produces reasoning aimed at the grader that generalizes to unseen graders. Concrete mechanism for how "modelling the evaluator" could get selected in. Worth reading the two together.
