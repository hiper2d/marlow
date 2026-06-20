---
title: "GDM AI Control Roadmap"
url: "https://www.alignmentforum.org/posts/hEtkyKGoPpFeWnKkX/gdm-ai-control-roadmap"
source: "AI Alignment Forum"
captured_at: "2026-06-19T14:14:00Z"
---

RSS summary: DeepMind published an "AI Control Roadmap (v0.1)" — a plan for internal guardrails to catch adversarial behavior by AI agents in internal deployment. Threat modeling borrows from cybersecurity (TRAIT&R, a taxonomy built on MITRE ATT&CK; three core areas: loss of control, work sabotage, direct harm). Two control invariants — reliable detection of misaligned intent, and effective prevention/response — that must outpace the agent's ability to evade. Capability-based mitigation ladders link defenses to model capability: four Detection tiers (D1–D4), three Prevention/Response tiers (R1–R3). 15 concrete tiered mitigations, from CoT monitoring and async alerts now to real-time access control, internal-activations monitoring, and shutdown infrastructure later.

Why this caught my eye: This is the second real anchor for `ai-control-camp`, which has been sitting at one (the Buck/Redwood efficient-tradeoffs post). It's the same control-over-alignment bet, now in institutional roadmap form from a frontier lab, with the same "rate interventions by feasibility, escalate with capability" logic ladderized into D1–D4 / R1–R3. Also worth flagging: TRAIT&R is another MITRE ATT&CK derivative (rhymes with the GDM attack-navigator frame), and CoT monitoring sits at the bottom rung as a *current* mitigation — a control-camp lab betting load-bearing weight on exactly the transcript readability that cot-monitorability keeps finding decays. Cross-thread anchor.
