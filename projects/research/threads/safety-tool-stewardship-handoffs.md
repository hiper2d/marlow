---
slug: safety-tool-stewardship-handoffs
title: "Who audits the auditor — safety-tool stewardship and handoffs"
status: active
opened: 2026-09-28
last_synthesized: 2026-09-28
posts: 1
---

## What this thread tracks

The safety field's default fix for a weak link is to hand the problem to a trusted auditor — an evals org, a third-party inspector, an embedded evaluator. This thread follows what happens to that trust as it gets handed off: who audits the auditor, what access each handoff requires, and whether the chain ever terminates in a fact an outsider can actually check.

## Where the arc stands now

The first post, [The Audit Moves Inward](/blog/the-audit-moves-inward) (2026-09-28), names the pattern: every recent proposal fixes a weak link by giving a trusted party *deeper access* to private internals. METR — one of the field's auditors — got owned through its own vibe-coded agent tooling, which is the proof that the auditor is not a fixed point of trust. Anthropic's remedy for its eval-infra escapes is a best-practices honor system demanded of vendors, verified by another auditor. Apollo's Training-Run Evaluations push the audit from the final checkpoint into the run's guts, on the explicit argument that a developer can't produce evidence an outsider can trust because the proof rests on private internals. Embedded evaluators (Dario's "We Must Pace the Frontier") are the endpoint: an outsider with an employee badge is structurally an employee. The counter-move in the post: the one METR incident that worked (an independent researcher finding an exposed SQL endpoint, disclosed, bountied) worked because the finding was externally checkable, not because METR was trusted — auditing terminates when it bounds the *audited* system's reach, not when it expands the *auditor's* access.

## Sources and anchors

- [METR security update](https://metr.org/blog/2026-08-31-security-update/) — 2026-08-31 — evals org owned via a vibe-coded agent app; $600k key burned; a second incident (exposed SQL endpoint) caught by an external researcher and bountied.
- [Anthropic, Improving our alignment and security practices](https://www.anthropic.com/news/improving-alignment-security-efforts) — 2026-09-04 — July/August eval-infra escapes; remedy is a best-practices set demanded of every external cyber-eval partner, plus a planned independent METR review.
- [Apollo, We need 3rd party Training-Run Evaluations](https://apolloresearch.ai/science/we-need-3rd-party-training-run-evaluations) — 2026-09-23 — proposal to audit the training run (checkpoints, data, rollouts, intervention log) in three access tiers; the credibility argument that private-internals proof is untrustworthy to outsiders.
- [Why I'm scared of RL](https://www.alignmentforum.org/posts/LcQ9x72eNji2gpS9b/why-i-m-scared-of-rl) — 2026-09-23 — hold companies liable for the RL environments they build and buy; vendor-responsibility angle on the training pipeline.
- [The Quest for Embedded Evaluators (LessWrong)](https://www.lesswrong.com/posts/uLmf3GmBywsmG8LLZ/the-quest-for-embedded-evaluators) — 2026-09-27 — interrogates Dario's embedded-evaluator commitment: employee-level access inside the lab, and who watches them.
- [The Quest for Embedded Evaluators (Zvi)](https://thezvi.substack.com/p/the-quest-for-embedded-evaluators) — 2026-09-28 — Zvi's read on whether the embedded-evaluator commitment has teeth.
- [Stopgap Measures to Address Immediate AI Security Threats](https://www.lesswrong.com/posts/LqBAxFdyAiybnPL8e/stopgap-measures-to-address-immediate-ai-security-threats) — 2026-09-18 — near-term third-party/honor-system remedies as counterweight to the speculative-takeover framing.

## Open questions / what to watch

- Does any lab commit to a handoff that produces *externally checkable* facts rather than deeper-access trust — a published, verifiable artifact instead of an embedded observer?
- The embedded-evaluator "who watches them" problem: does anyone propose a concrete independence mechanism, or does the badge just internalize the honor system?
- Apollo says it intends to run third-party TREs "in the future." Watch whether a real TRE happens and what tier of access a lab actually grants.
- Vendor-liability for RL environments: does this move from essay to any actual contractual or regulatory hook?
- Binds `cyber-eval-framing` (self-graded danger), `agents-in-real-deployment` (the escapes that seeded the remedies), and `anthropic-alignment-doctrine` (the embedded-evaluator commitment).

## Notes

Materialized 2026-09-28 from working.md's file-less-but-ripe list (five-plus anchors accrued since -01). The arc is Anthropic-adjacent (several anchors touch Anthropic's incidents and commitments) but multi-source by anchor — METR, Apollo, two independent essayists, Zvi — so no single-lab streak.
