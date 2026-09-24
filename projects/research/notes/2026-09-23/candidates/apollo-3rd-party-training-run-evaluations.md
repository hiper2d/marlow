---
title: "We need 3rd party Training-Run Evaluations"
url: "https://apolloresearch.ai/science/we-need-3rd-party-training-run-evaluations"
source: "Apollo Research (science)"
captured_at: "2026-09-23T16:09:00Z"
---

RSS summary: (sitemap gave no summary; drawn from the article body) Apollo argues that final-checkpoint pre-deployment evals are insufficient to catch scheming, because a scheming-relevant propensity can spike mid-training and be trained out of view before release. They propose Training-Run Evaluations (TREs) — third-party inspection of intermediate checkpoints, SFT/RL data, rollouts, and the developer's own mid-run intervention log — organized into three access tiers (checkpoint evals, data evaluations, process reviews) that build trust gradually. Apollo says it intends to conduct 3rd party TREs in the future.

Why this caught my eye: This is the same move as the pre-deployment-eval fight from two years ago, pushed one layer earlier — and it lands on exactly the seam three of our arcs already circle. It gives `safety-tool-stewardship-handoffs` a concrete institutional proposal (who audits the training run, and with what access), it sharpens `cot-monitorability` in the sharpest possible way — the "process review" tier explicitly names the failure mode where a developer sees ugly CoT and quietly trains on nicer-looking CoT until the loop is indistinguishable from optimizing against the CoT directly — and it's a clean forcing example for `cyber-eval-framing`'s "evals necessary, not sufficient" line. The credibility argument is the interesting part: even a developer that competently checks for scheming can't produce evidence anyone else can trust, because the proof rests on private internals. That's a governance claim, not a technical one.
