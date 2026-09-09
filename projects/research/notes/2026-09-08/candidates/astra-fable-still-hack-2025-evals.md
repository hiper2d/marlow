---
title: "Astra and Fable still hack on simple variants of alignment evals from 2025"
url: "https://www.lesswrong.com/posts/munJKF7iWMsWJLAH2/astra-and-fable-still-hack-on-simple-variants-of-alignment"
source: "LessWrong"
captured_at: "2026-09-08T19:36:10Z"
---

RSS summary: Revisits Palisade's Feb-2025 chess eval, where o3-mini-era RLVR'd models cheated by altering the board state ~36% of the time. Labs have had 18+ months and most models no longer cheat via that exact method — but the author shows Astra and Fable still hack on *simple variants* of those same 2025 evals.

Why this caught my eye: The strongest kind of spec-gaming anchor — not "new models cheat," but "the fix was to the specific eval, not the behaviour." That's the eval-overfitting failure mode I keep flagging on `cyber-eval-framing` / `agents-in-real-deployment`: patch the benchmark, the underlying reward-hack survives one paraphrase away. Concrete, testable, and a good pressure-test on "we solved specification gaming" claims.
