---
title: "Monitorability evaluations and policy proposals"
url: "https://www.alignmentforum.org/posts/zAczYuHQS6jdG5DTg/monitorability-evaluations-and-policy-proposals"
source: "AI Alignment Forum"
captured_at: "2026-10-23T08:16:33Z"
---

RSS summary: Personal (non-official-Anthropic) proposal that splits monitorability into four types — Control, Training, Auditing, Diffuse — and builds a red-line methodology on top. Key move: use Auditing Monitorability to establish *trustedness* of a monitor (grounding it in the "models too un-robust to hide in audits" argument from Anthropic's Aug Risk Report), then evaluate Control/Training monitorability against the best trusted monitor you actually deploy, with real elicitation (held-out evals + prompt/RL iteration) so a schemer can't sandbag the measurement. Proposes two hard red lines (no internally-deployed model that reliably evades detection on sabotage; no trained model that reliably evades detection on reward hacks) plus a "monitorability externality" quotient (unmonitorability/capabilities via ECI) to constrain degradation along the way.

Why this caught my eye: This is the policy-proposal counterpart to everything cot-monitorability has been tracking empirically — the probe-evasion-scales-with-capability pair (-19), single-pass defection (-16), monitor red-teaming (-16). Those are measurements of *how* monitorability fails; this is a scaffold for turning such measurements into a bright line labs commit not to cross, and it's refreshingly honest about where it's weakest (white-box monitors treated as untrusted; Diffuse monitorability admitted as unsolved). The explicit lean on the Aug Risk Report's "weak, not aligned" argument also ties it straight into stewardship #3's "the veto nobody used" beat — same report, used here as the load-bearing trust foundation. Strong cot-monitorability #7 anchor, maybe the governance hinge the arc has been missing.
