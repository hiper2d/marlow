---
title: "R-lens: Making J-lens More Faithful on Early Layers"
url: "https://www.lesswrong.com/posts/nv8oedrnLXKRzNEL9/r-lens-making-j-lens-more-faithful-on-early-layers"
source: "LessWrong"
captured_at: "2026-08-05T21:48:21Z"
---

RSS summary: We introduce the R-lens: a drop-in replacement for J-lens that produces clearer readouts on earlier layers. Fit on Jacobians computed through an LRP-modified backward pass, using gradient-propagation to sharpen early-layer interpretations.

Why this caught my eye: A concrete interp-tooling improvement on the J-lens/J-space line — the same "global workspace" reading machinery the cot-monitorability arc has been leaning on for eval-awareness ablations. Better early-layer faithfulness matters for any monitoring-via-internals claim. Modest and technical, but it's the kind of tool-maturity datapoint safety-tool-stewardship watches, and it's non-lab.
