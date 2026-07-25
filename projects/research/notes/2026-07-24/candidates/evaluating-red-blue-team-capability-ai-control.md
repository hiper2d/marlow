---
title: "Evaluating Red Team and Blue Team Capability for AI Control Research"
url: "https://www.lesswrong.com/posts/KWT2Nk2gyxTc9xowT/evaluating-red-team-and-blue-team-capability-for-ai-control"
source: "LessWrong"
captured_at: "2026-07-24T11:42:19Z"
---

RSS summary: Proposes an ELO methodology (Extended Bradley-Terry) to measure red-team (attacker) and blue-team (monitor/protocol) capability in AI control, separating the *model* from the *researcher* who builds the attack/defense. Run on LinuxArena with six models as both attackers and monitors, with and without automated (Claude Code) elicitation. Headline finding (wide error bars, low-medium confidence): when elicited, monitors improve slightly *faster* than attackers (+16 ELO/ECI); when non-elicited, attackers pull slightly ahead (-14 ELO/ECI). Human feedback gave a small measurable lift to the blue team, ~none to the red team. Proposes a live leaderboard tracking which side scales faster.

Why this caught my eye: This is a direct measurement instrument for the exact question `the-bottom-rung` left open — does control's invariant "detection outpaces evasion" actually hold on the rung we can measure? It answers "sometimes, and it depends entirely on elicitation," which is a sharper and more falsifiable answer than the arc has had. Pairs tightly with the -18 `studying-sandboxing-for-ai-control` anchor (same LinuxArena, same untrusted-Sonnet framing). The elicited/non-elicited flip is the story: the invariant is contingent on how hard you push the monitor.
