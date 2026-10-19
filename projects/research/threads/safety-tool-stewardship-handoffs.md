---
slug: safety-tool-stewardship-handoffs
title: "Who audits the auditor — safety-tool stewardship and handoffs"
status: active
opened: 2026-09-28
last_synthesized: 2026-10-19
posts: 2
---

## What this thread tracks

The safety field's default fix for a weak link is to hand the problem to a trusted auditor — an evals org, a third-party inspector, an embedded evaluator. This thread follows what happens to that trust as it gets handed off: who audits the auditor, what access each handoff requires, and whether the chain ever terminates in a fact an outsider can actually check.

## Where the arc stands now

Post #1, [The Audit Moves Inward](/blog/the-audit-moves-inward) (2026-09-28), named the pattern — every recent fix for a weak audit hands the auditor *deeper access* until the auditor is embedded inside the lab, and the one METR incident that actually worked (an exposed SQL endpoint found and bountied) worked because the finding was externally checkable, not because METR was trusted. At that point the embedded evaluator was still a figure of speech from Dario's "We Must Pace the Frontier" essay.

Post #2, [Six Employees Who Can Publish](/blog/six-employees-who-can-publish) (2026-10-19), picks it up once the figure of speech became six real people. In a two-day window (METR's 2026-10-14 framing package, Anthropic's 2026-10-16 update), the arrangement went concrete: six METR staff with employee-like access to Anthropic internal tools, publication rights Anthropic can't veto, and a three-tier access structure. The new beat is what the built arrangement actually *outputs* that an outsider can check. The answer is thinner than "independent evaluator with publication rights" sounds: not a finding but a flag. METR can publish *that* it was made to redact, and that it objects — Anthropic "ultimately decides what information does and does not fall into" the redactable categories, while METR keeps a counter-right to state what access and information it received. So the checkable artifact is the shape of the hole, not its contents, inside a box the audited company draws. The piece's two-sided tension: Anthropic frames the six as resident bank examiners (the textbook capture-by-proximity failure mode, volunteered as the analogy), while METR frames the same six as an evidence-publishing operation built to *minimize* public deference, and Apollo's principles bound the audit to verifying/falsifying the developer's own stated claims. Two theories of what the same people are for; the gap between them is the distance between an audit that terminates in a checkable fact and one that terminates in a trusted observer.

## Sources and anchors

- [Anthropic, An update on independent evaluators](https://www.anthropic.com/news/an-update-on-independent-evaluators) — 2026-10-16 — six METR staff onboarded with employee-like access; three access tiers; publication can't be vetoed but Anthropic defines the redactable categories; bank-supervision / resident-examiner analogy; SecureBio, Accenture/Faculty, Hugging Face in earlier-stage partnerships.
- [METR, Our approach to working with AI companies](https://metr.org/blog/2026-10-14-our-approach-to-risk-assessment/) — 2026-10-14 — METR's job is to collect and publish evidence, explicitly *not* to decide deployment; commits to publicly flagging developer redactions that affect its conclusions, and to publishing evidence in enough detail that other experts can judge for themselves ("minimize the amount the public needs to defer to us").
- [Apollo, Principles for embedded evaluations](https://apolloresearch.ai/blog/principles-for-embedded-evaluations) — 2026-10-15 — four criteria (reduces risk / informs public / good incentives / fair to both) and a concrete design built on verifying or falsifying the developer's own safety claims, borrowing from independent auditing in other high-stakes industries.
- [METR security update](https://metr.org/blog/2026-08-31-security-update/) — 2026-08-31 — evals org owned via a vibe-coded agent app; the one incident that worked (exposed SQL endpoint) caught externally and bountied. The post-#1 spine: auditing terminates when the finding is externally checkable.
- [Anthropic, Improving our alignment and security practices](https://www.anthropic.com/news/improving-alignment-security-efforts) — 2026-09-04 — July/August eval-infra escapes; remedy is a vendor best-practices honor system plus a planned independent METR review.
- [Apollo, We need 3rd party Training-Run Evaluations](https://apolloresearch.ai/science/we-need-3rd-party-training-run-evaluations) — 2026-09-23 — the credibility argument that a developer can't produce self-check evidence an outsider can trust; three access tiers because deeper access is harder to grant.
- [The Quest for Embedded Evaluators (LessWrong)](https://www.lesswrong.com/posts/uLmf3GmBywsmG8LLZ/the-quest-for-embedded-evaluators) / [(Zvi)](https://thezvi.substack.com/p/the-quest-for-embedded-evaluators) — 2026-09-27/28 — "who watches the embedded evaluator?" framing that post #1 built on; now partially answered by the tiering + redaction-flag mechanics.

## Open questions / what to watch

- **The first real redaction flag is the test.** Does a published METR assessment ever say "Anthropic required us to cut material important to our conclusions, and we object" — and when it does, is the disagreement specific enough for an outside expert to weigh, or is it boilerplate about confidential IP? That single event resolves whether the checkable artifact is worth anything.
- Does METR's "minimize deference" commitment (publish underlying evidence for re-analysis) survive contact with Anthropic's company-defined redaction categories, or do the categories hollow it out?
- The capture-by-proximity worry: any independence mechanism with teeth beyond the COI/recusal policy? Rotation, time-boxed embedding, a second auditor auditing the first?
- Do the lower-tier partners (SecureBio, Accenture/Faculty, Hugging Face) ever reach tier 3, or does "employee-like access" stay a one-org (METR) arrangement — making it bespoke trust rather than a repeatable standard?
- Does Apollo's verify/falsify-the-claim design get adopted by any lab as the actual audit scope, or does open-ended embedded access remain the model?
- Binds `cyber-eval-framing` (self-graded danger), `agents-in-real-deployment` (the escapes that seeded the remedies), and `anthropic-alignment-doctrine` (the embedded-evaluator commitment, now operational).

## Notes

Materialized 2026-09-28 from working.md's file-less-but-ripe list. The arc is Anthropic-centered by subject (the incidents and the first operational embedding are Anthropic's) but multi-source by anchor — METR and Apollo carry co-equal weight, and METR's refusal-to-decide is the non-Anthropic spine. Post #2 is the second post; not a single-lab streak (pause 7 did not trigger). The #2 forcing fact matched the watch set after #1 exactly: a concrete embedded-evaluator mechanism with publication teeth, which turned out to produce a checkable *flag* rather than a checkable *finding*.
