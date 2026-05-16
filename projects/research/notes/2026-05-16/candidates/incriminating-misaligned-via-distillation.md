---
title: "Incriminating misaligned AI models via distillation"
url: "https://www.lesswrong.com/posts/BYH6ebmfZb3Eggzer/incriminating-misaligned-ai-models-via-distillation"
source: "LessWrong"
captured_at: "2026-05-16T10:53:45Z"
---

RSS summary: Frames a distillation-as-audit technique. Take a candidate-misaligned teacher that can fool alignment audits, distill into a student. Two outcomes: (a) misalignment fails to transfer, you get a benign capable model; (b) misalignment transfers but the smaller student is worse at hiding it, giving you indirect evidence of the teacher's misalignment. Post proposes distillation methods aimed at the second outcome — transfer misalignment without transferring deception capability.

Why this caught my eye: Auditing-via-distillation as a *technique* (not just a wish) is a genuinely interesting direction — it converts "the teacher is too capable to interrogate honestly" from a wall into a usable asymmetry. Closer cousins to the safer-models-as-oracles literature, but the framing is more practical and lands on the audit side rather than the deployment side. Anchors in `cot-monitorability` (audit techniques cluster) and is adjacent to the NLA / AuditBench work captured today — both are attempts to surface signals that survive when the model knows you're looking. Worth watching whether anyone actually runs this on a known-misaligned-by-construction teacher.
