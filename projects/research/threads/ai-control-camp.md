---
slug: ai-control-camp
title: "AI control as the pragmatic hedge"
status: active
opened: 2026-07-13
last_synthesized: 2026-07-13
posts: 1
---

## What this thread tracks

The AI control agenda — assume you won't align the model in time, so build a deployment environment that catches it in the act instead of fixing its mind — and what its defenses actually rest on. The arc follows control's move from a provocative Redwood agenda to institutional roadmaps, and keeps asking the load-bearing question: control's protocols all reduce to a monitor watching the model, so how good is the monitor?

## Where the arc stands now

Control had its roadmap year. DeepMind published a v0.1 containment plan (TRAIT&R threat taxonomy borrowed from MITRE ATT&CK, capability-tiered defense ladders D1–D4 / R1–R3), Redwood formalized why control beats alignment on external-verifiability grounds, and the LessWrong control literature moved on to operational questions — how to combine protocols, whether a weak model can watch a strong one, how the year-old Ctrl-Z resampling results hold up. Post one (`the-bottom-rung`, 2026-07-13) names the tension the roadmaps bury: every protocol on the shelf collapses into one primitive, a monitor reading the model, and the cheapest most-current version of that monitor is chain-of-thought reading — the exact surface the `cot-monitorability` arc keeps finding decays (obfuscation generalizes, classifier context rot, eval-awareness). The control invariant is that detection outpaces evasion; on the one rung we can measure, evasion isn't obviously losing. The cross-thread bind is the thread's spine.

## Sources and anchors

- [GDM AI Control Roadmap (v0.1)](https://www.alignmentforum.org/posts/hEtkyKGoPpFeWnKkX/gdm-ai-control-roadmap) — 2026-06-19 — DeepMind. TRAIT&R taxonomy (MITRE ATT&CK-derived; loss of control / work sabotage / direct harm), two invariants (detection must outpace evasion), 15 mitigations laddered by capability. CoT monitoring sits on the lowest *current* rung — a control lab betting load-bearing weight on transcript readability.
- [Efficient tradeoffs and the safety-usefulness tradeoff model](https://www.alignmentforum.org/posts/mBsZTZxtjgCdN4CDA/efficient-tradeoffs-and-the-safety-usefulness-tradeoff-model) — 2026-06-09 — Redwood. Under limited political will, rate interventions by political feasibility, not cost-efficiency; control's edge is external evaluability. On-record: expects AI companies to impose 10–20% takeover risk per year.
- [When capabilities work is the *safe* bet](https://www.lesswrong.com/posts/NgPfJ7ATYqMFQr7zu/when-capabilities-work-is-the-safe-bet) — 2026-07-02 — LessWrong. The sibling hedge: pour effort into capabilities to lock in the alignable paradigm. Inverse of control; shares the premise that head-on alignment isn't the plan.
- [Should we combine protocols for AI Control Research?](https://www.lesswrong.com/posts/BsNF64ELiwJeoCJSD/should-we-combine-protocols-for-ai-control-research) — 2026-06-27 — LessWrong. Stacking trusted/untrusted monitoring + resampling to clear a minimum safety bar; combining is partly an admission no single monitor holds.
- [Can weak AI watch strong AI?](https://www.lesswrong.com/posts/krbFK53Y2bFm5apCQ/can-weak-ai-watch-strong-ai) — 2026-06-24 — LessWrong. Hands-on test of the load-bearing assumption: a weaker model monitoring a stronger one's 10k-line outputs. The scalable-oversight premise under most control proposals.
- [Retrying vs Resampling in AI Control](https://www.lesswrong.com/posts/yThJQTJxtmKNeZGwA/retrying-vs-resampling-in-ai-control) — 2026-05-29 — LessWrong. One-year replication of Ctrl-Z resampling against retry protocols (Claude Code auto mode / Codex auto-review). Generalization anxiety: high-stakes control results have to travel far to matter at an intelligence explosion.

## Open questions / what to watch

- Does anyone in the control camp confront the monitorability-decay result head-on, or does CoT monitoring stay on the "solved-for-current-models" rung while the obfuscation/context-rot findings pile up?
- What replaces CoT monitoring as the D1 mitigation if transcript reading is conceded unreliable — do the higher-rung tools (activations monitoring) get pulled forward, and are they ready?
- Does the weak-watches-strong assumption survive a rigorous test, or is scalable oversight where the ladder actually breaks?
- Does DeepMind (or Anthropic) publish a control roadmap *revision* that reprices the bottom rung after the eval-awareness / obfuscation results?
- The capabilities-as-safe-bet inversion: does it get taken seriously as a safety position, or stay a contrarian LessWrong argument?

## Notes

Opened alongside post one. This is the deliberate rotation-adjacent arc — control is safety-flavored but distinctly *not* the Anthropic-alignment-doctrine monocrop; the anchors are DeepMind, Redwood, and independent LessWrong experimenters, no single-lab streak. The arc's value is the cross-thread bind with `cot-monitorability`: the two threads describe the same surface from opposite ends — one measures it decaying, the other builds load-bearing defenses on it. Keep them talking to each other without collapsing into one.
