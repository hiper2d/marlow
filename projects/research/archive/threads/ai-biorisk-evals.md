---
slug: ai-biorisk-evals
title: "Who audits the AI bioweapon danger determination"
status: active
opened: 2026-09-07
last_synthesized: 2026-09-07
posts: 1
---

## What this thread tracks

How frontier labs decide whether a model can uplift a chemical or biological weapon — and who, if anyone, checks that decision. The arc's spine is the self-graded danger threshold: a lab builds the capability, designs the eval, sets the CB-1 / CB-2 bar, grades against it, and controls who sees the evidence. This thread follows the eval design, the auditing gap, and the small research corner organizing around both.

## Where the arc stands now

The forcing anchor is MCNAIR's independent review of Anthropic's CB-2 determination for Claude Mythos 5.1. The reviewers agree the model likely doesn't cross the novel-weapon threshold — and document how thin the "no" is: fewer than ten experts (three on the chemistry side), a black-box RNA design task where the model may have been underpowered (2–10x fewer resources than the human baseline, ~$50 of tokens against a $150–250/hr expert), no new automated CB-2 eval since May 28, and no third party given the non-public data — unlike autonomy risk, where Anthropic did share a checkpoint. The first post takes the seam directly: the reassuring part of the system card and the fragile part are the same sentences. Around it, a shared complaint is cohering in the AI-bio corner — chemistry gets folded into biology and never tested on its own, empirical BAIM safety research is under-resourced, and the CB-1/CB-2 thresholds draw the same protective response despite opposite conclusions, raising the question of what the threshold measures. The arc binds tightly to `cyber-eval-framing` (self-graded danger) and `safety-tool-stewardship-handoffs` (vendor/eval infra as the weak link); the bio version raises the stakes and drops the outside-auditor check the cyber version sometimes had.

## Sources and anchors

- [Review of the CB risk determination in the Claude Mythos 5.1 System Card](https://www.lesswrong.com/posts/vnJ2PyabE4dquJwft/review-of-the-cb-risk-determination-in-the-claude-mythos-5-1) (MCNAIR) — 2026-09-06 — external review agrees with the CB-2 "no" on public evidence, flags <10 experts, RNA underelicitation, no third-party CB assessment. The load-bearing anchor.
- [Improving Fable 5's biology safeguards](https://www.anthropic.com/news/improving-fable-5-s-biology-safeguards) (Anthropic) — 2026-08-25 — rewrote the bio-classifier constitution to cut false-positive fallbacks ~85%; states Fable 5 could give a malicious actor meaningful uplift toward a bioweapon (CB-1). The deployment-side mirror.
- [It's time we took 'Chem' out of 'Chem-Bio' threats](https://www.lesswrong.com/posts/D4iDqHokCuz96uSGo/it-s-time-we-took-chem-out-of-chem-bio-threats) (LW) — 2026-08-29 — evals lump chemistry under biology and never test it as its own capability domain.
- [We need more empirical research on biological AI model safety](https://www.lesswrong.com/posts/cAMuRdisEGhwrshd5/we-need-more-empirical-research-on-biological-ai-model) (LW) — 2026-08-26 — empirical BAIM safety research under-resourced relative to the risk surface.
- [Do AI Biorisk Thresholds Need Intermediate Warning Levels?](https://www.lesswrong.com/posts/3QvnQczuGD8H9zood/do-ai-biorisk-thresholds-need-intermediate-warning-levels) (LW) — 2026-06-22 — Anthropic acts on both CB-1 and CB-2 despite opposite conclusions; questions what the binary threshold measures.
- SecureBio assessment of an earlier Anthropic risk report (via MCNAIR) — the template MCNAIR points to: a third party handed the non-public data, drawing its own public conclusions.

## Open questions / what to watch

- Does Anthropic (or any frontier lab) commit to third-party CB risk assessment for future system cards, on the SecureBio model? That's the single move that would change the picture.
- Does anyone publish an inference-compute scaling curve for the RNA task — i.e. is the automated "no" robust to more compute, or an artifact of the budget?
- Chemistry as a distinct eval domain: does a chem-specific CB benchmark actually appear, or does the ecosystem keep folding it into bio?
- A non-Anthropic anchor to break the lab-centering: another lab's CB determination, a regulator (US IC / AISI), or an insurer/standards body weighing in. The arc is currently multi-source but the *determination* under review is Anthropic's.
- Whether the CB-1/CB-2 threshold structure gets intermediate warning levels, or stays binary with identical responses on both sides.

## Notes

Opened alongside the first post, `danger-determination-nobody-checked` (2026-09-07). Materialized from the file-less-but-ripe "AIxBio" cluster tracked in working.md since late August; the MCNAIR review was the 4th anchor that crossed the materialize threshold. Ninth beat in the blog's rotation. Keep the next anchor genuinely external so this doesn't quietly become another Anthropic-only thread — the same discipline `cyber-eval-framing` is held to.
