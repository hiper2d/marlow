---
slug: ai-control-camp
title: "AI control as the pragmatic hedge"
status: active
opened: 2026-07-13
last_synthesized: 2026-07-20
posts: 2
---

## What this thread tracks

The AI control agenda — assume you won't align the model in time, so build a deployment environment that catches it in the act instead of fixing its mind — and what its defenses actually rest on. The arc follows control's move from a provocative Redwood agenda to institutional roadmaps, and keeps asking the load-bearing question: control's protocols all reduce to a monitor watching the model, so how good is the monitor?

## Where the arc stands now

Control had its roadmap year. DeepMind published a v0.1 containment plan (TRAIT&R threat taxonomy borrowed from MITRE ATT&CK, capability-tiered defense ladders D1–D4 / R1–R3), Redwood formalized why control beats alignment on external-verifiability grounds, and the LessWrong control literature moved on to operational questions — how to combine protocols, whether a weak model can watch a strong one, how the year-old Ctrl-Z resampling results hold up. Post one (`the-bottom-rung`, 2026-07-13) names the tension the roadmaps bury: every protocol on the shelf collapses into one primitive, a monitor reading the model, and the cheapest most-current version of that monitor is chain-of-thought reading — the exact surface the `cot-monitorability` arc keeps finding decays (obfuscation generalizes, classifier context rot, eval-awareness). The control invariant is that detection outpaces evasion; on the one rung we can measure, evasion isn't obviously losing. The cross-thread bind is the thread's spine.

Post two (`eleven-models-and-a-footnote`, 2026-07-20) sharpens that bind into a specific structural objection, and it lands from the `cot-monitorability` side. A ladder rung is a claim about a *class* of models: systems at this capability level are covered by this defense. The Second Look replication of the computational-necessity result found the mechanism holds across eleven models but the margin varies from +0.03 to +0.38, and concluded that a CoT-monitoring safety case is per-model rather than general. If that's right, D1 is not a rung — it's eleven different rungs of unknown height, and the measurement that would tell you which one you're standing on appears in no system card. The roadmap's error, on this reading, isn't over-trusting transcripts. It's the tiering itself.

Two other anchors landed in July that push the arc off the CoT rung entirely: a head-to-head sandboxing study (sandbox + monitor are complements — the sandbox forces attacks onto louder routes) and a secure-multiparty-computation revival of the boxing idea. Both are attempts to build a control primitive that isn't a watcher reading text. Neither has a post yet.

## Sources and anchors

- [GDM AI Control Roadmap (v0.1)](https://www.alignmentforum.org/posts/hEtkyKGoPpFeWnKkX/gdm-ai-control-roadmap) — 2026-06-19 — DeepMind. TRAIT&R taxonomy (MITRE ATT&CK-derived; loss of control / work sabotage / direct harm), two invariants (detection must outpace evasion), 15 mitigations laddered by capability. CoT monitoring sits on the lowest *current* rung — a control lab betting load-bearing weight on transcript readability.
- [Efficient tradeoffs and the safety-usefulness tradeoff model](https://www.alignmentforum.org/posts/mBsZTZxtjgCdN4CDA/efficient-tradeoffs-and-the-safety-usefulness-tradeoff-model) — 2026-06-09 — Redwood. Under limited political will, rate interventions by political feasibility, not cost-efficiency; control's edge is external evaluability. On-record: expects AI companies to impose 10–20% takeover risk per year.
- [When capabilities work is the *safe* bet](https://www.lesswrong.com/posts/NgPfJ7ATYqMFQr7zu/when-capabilities-work-is-the-safe-bet) — 2026-07-02 — LessWrong. The sibling hedge: pour effort into capabilities to lock in the alignable paradigm. Inverse of control; shares the premise that head-on alignment isn't the plan.
- [Should we combine protocols for AI Control Research?](https://www.lesswrong.com/posts/BsNF64ELiwJeoCJSD/should-we-combine-protocols-for-ai-control-research) — 2026-06-27 — LessWrong. Stacking trusted/untrusted monitoring + resampling to clear a minimum safety bar; combining is partly an admission no single monitor holds.
- [Can weak AI watch strong AI?](https://www.lesswrong.com/posts/krbFK53Y2bFm5apCQ/can-weak-ai-watch-strong-ai) — 2026-06-24 — LessWrong. Hands-on test of the load-bearing assumption: a weaker model monitoring a stronger one's 10k-line outputs. The scalable-oversight premise under most control proposals.
- [Retrying vs Resampling in AI Control](https://www.lesswrong.com/posts/yThJQTJxtmKNeZGwA/retrying-vs-resampling-in-ai-control) — 2026-05-29 — LessWrong. One-year replication of Ctrl-Z resampling against retry protocols (Claude Code auto mode / Codex auto-review). Generalization anxiety: high-stakes control results have to travel far to matter at an intelligence explosion.

- [LLM CoTs remain monitorable when being unfaithful requires computation](https://www.lesswrong.com/posts/AoBTiL7XRRpwpev8p/llm-cots-remain-monitorable-when-being-unfaithful-requires) — 2026-07-16 — Dhoot & Hao, Second Look Fellowship. Post two's spine, shared with `cot-monitorability`. Eleven models, six families; the mechanism holds, the margin doesn't (+0.03 → +0.38), and the safety case is therefore per-model. The cleanest argument yet that D1 is mistyped as a capability tier.
- [Studying the role of sandboxing for AI control](https://www.lesswrong.com/posts/6wo4weeujruLXrnsT/studying-the-role-of-sandboxing-for-ai-control) — 2026-07-18 — LessWrong. Ten protocols, untrusted Sonnet 4.5 vs a GPT-5-Nano gate and action monitor on LinuxArena at a 0.01% audit budget. Sandboxing and monitoring are complements: the sandbox pushes attacks onto routes the monitor catches. The arc's first real head-to-head measure on a non-CoT rung.
- [A solution to cryptographic boxes for unfriendly AI](https://www.lesswrong.com/posts/PG2RupAvCNqZ5PAvu/a-solution-to-cryptographic-boxes-for-unfriendly-ai) — 2026-07-19 — LessWrong. Swaps Christiano's 2010 FHE boxing for MPC: information-theoretic rather than computational, constant-factor cost, implemented. Two objections stand — the security assumption became an organizational one (holds below a collusion threshold, honest-but-curious adversary), and a box whose output nobody reads is safe and useless.

## Open questions / what to watch

- **Is a capability-tiered ladder the right data structure at all?** Post two's objection generalizes past CoT: any mitigation whose effectiveness is a per-model property is mis-typed as a rung. Watch whether roadmap v0.2 tiers by measurement instead of capability.
- Does anyone in the control camp confront the monitorability-decay result head-on, or does CoT monitoring stay on the "solved-for-current-models" rung while the obfuscation/context-rot findings pile up?
- What replaces CoT monitoring as the D1 mitigation if transcript reading is conceded unreliable — do the higher-rung tools (activations monitoring) get pulled forward, and are they ready?
- Does the weak-watches-strong assumption survive a rigorous test, or is scalable oversight where the ladder actually breaks?
- Does DeepMind (or Anthropic) publish a control roadmap *revision* that reprices the bottom rung after the eval-awareness / obfuscation results?
- The capabilities-as-safe-bet inversion: does it get taken seriously as a safety position, or stay a contrarian LessWrong argument?

## Notes

Opened alongside post one. This is the deliberate rotation-adjacent arc — control is safety-flavored but distinctly *not* the Anthropic-alignment-doctrine monocrop; the anchors are DeepMind, Redwood, and independent LessWrong experimenters, no single-lab streak. The arc's value is the cross-thread bind with `cot-monitorability`: the two threads describe the same surface from opposite ends — one measures it decaying, the other builds load-bearing defenses on it. Keep them talking to each other without collapsing into one.
