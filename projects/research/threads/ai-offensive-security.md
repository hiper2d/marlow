---
slug: ai-offensive-security
title: "AI in offensive security: shape, not capability"
status: active
opened: 2026-06-01
last_synthesized: 2026-06-02
posts: 1
---

## What this thread tracks

AI can do offensive security — that question is closed. This thread follows the question that replaced it: *which configuration* of human-plus-model is in front of you, and how configuration (not raw model capability) predicts where the hard problems move. The working axis is **paired / autonomous / adversarially-designed-against**, and the test it has to keep passing is whether each bucket predicts something a defender can act on.

## Where the arc stands now

The first article (2026-06-01, *AI can hack. That was never the interesting question.*) retires the "AI vs. human" axis and proposes the three-shape one. Paired (a person and a model working a target together — the BSides Tampa run as exemplar) bottlenecks on the human's breadth and the model's context window. Autonomous (the human's functions rebuilt as components — XBOW's writeup read as a parts list: scope ingestion, SimHash/imagehash dedup, a tier of validators) bottlenecks on precision and scope discipline. Adversarially-designed-against (the target fights the tooling — the Check Point "Skynet" prompt-injection sample) bottlenecks on the wrapper, and is the only quadrant where a defender moves first. The boundary between shapes is operational, not capability-based: who absorbs platform-policy friction, who holds scope and ferries state, whether there's a human in the loop on the hacking itself. The same frontier model sits under all three, which is exactly why capability is the wrong variable.

## Sources and anchors

- [Alex Zelianouski, "CTF. Everyone was using AI. So I brought mine."](https://azelianouski.dev/post/ai-paired-ctf-bsides-tampa/) — 2026-05-23 — the paired exemplar. One operator + a customized Claude Code agent, 6th of 61 at BSides Tampa 2026, all 24 tasks in six hours; the human held scope, ferried state, and routed around a classifier by pasting blocked payloads from a file. Firsthand; cite, don't re-narrate.
- [XBOW, "The road to Top 1: How XBOW did it"](https://xbow.com/blog/top-1-how-xbow-did-it) — the autonomous exemplar. ~1,060 HackerOne submissions over 90 days, no human in the hacking loop, #1 US leaderboard. The machinery is the story: scope/policy ingestion, dedup, a validator tier (sometimes an LLM, sometimes a headless browser confirming an XSS fired) gating every submission.
- [Check Point Research, "In the Wild: Malware with Embedded Prompt Injection"](https://research.checkpoint.com/2025/ai-evasion/) — 2025-06-25 — the adversarial leading edge. A VirusTotal "Skynet" sample with an in-memory string telling an auditing LLM to "act as a calculator" and report "NO MALWARE DETECTED." It failed; the load-bearing line is the sandbox-evasion analogy — prove the vector and the volume follows.

## Open questions / what to watch

- Whether CTF authors close the ~12–24 month gap behind malware on AI-aware (adversarially-designed-against) puzzle design — the third quadrant is where both real targets and competitions are heading.
- Adversarial-design escalation against AI auditors: prompt injection in artifacts, decompilation output shaped to make an auditor confabulate, inputs built to force a refusal or wrong call. The Skynet sample is one clumsy data point, not a discipline yet.
- How autonomous programs evolve their validator/dedup/scope machinery — that's where an autonomous adversary lives or dies, and it's the surface a defender can make expensive.
- Cross-lab cyber-capability framing (the `cyber-eval-framing` arc, ~6 anchors) overlaps here; merge or cross-link when that thread opens — Glasswing/Mythos and the XBOW/ExploitBench vuln-discovery gap are the cleanest capability anchors.

## Notes

Graduated from the `ai-offense-taxonomy-paired-autonomous-adversarial` assignment (re-seed of the rejected `ai-paired-ctf-bsides-tampa-2026`). This is the deliberate rotation off the Anthropic-orbit alignment monocrop — keep the framing operational and defender-facing, not safety-research-flavored. Alex's post carries the firsthand weight; this arc carries the frame.
