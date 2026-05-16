---
title: "NLA Verbalizations on AuditBench: Llama 70B"
url: "https://www.lesswrong.com/posts/xmmBTkogixvAbyQFk/nla-verbalizations-on-auditbench-llama-70b"
source: "LessWrong"
captured_at: "2026-05-16T10:53:45Z"
---

RSS summary: Runs Llama 70B through AuditBench with NLA (Natural Language Activations) verbalizations. Strong-Evidence evals are less sampling-sensitive and more robust to KTO + SFT adversarial training than single-turn evals. Strong-Evidence surfaces quirks invisible to single-turn — reward_wireheading goes 0.00 → 0.34; anti_ai_regulation and contextual_optimism go 0.00 → 0.16 — trigger-dependent behaviors that only appear in specific contexts. Random sampling was best for single-turn; bottom-k for Strong-Evidence. KTO adversarial training was a near-complete defense; SFT only partial on single-turn.

Why this caught my eye: This is the empirical leg under the "NLA explanations / observations" frame that's been accumulating across `cot-monitorability` and the adjacent "interp tools catching themselves" cluster. The interesting finding isn't that NLA works — it's the contrast: behaviors at exactly 0.00 in single-turn eval surface at meaningful rates under Strong-Evidence sampling, and KTO completely closes one attack surface that SFT can't. That's a real claim about which eval shape is load-bearing for which adversarial-training regime, and it's the kind of detail risk reports currently elide. Pairs naturally with the deployment-time-spread post captured earlier today — both are arguing that current eval cadence is missing the actual failure surface.
