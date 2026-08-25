---
title: "Improving Fable 5's biology safeguards"
url: "https://www.anthropic.com/news/improving-fable-5-s-biology-safeguards"
source: "Anthropic News"
captured_at: "2026-08-25T08:30:00Z"
---

RSS summary: (sitemap entry had no summary) Anthropic rewrote the constitution behind Fable 5's biology safety classifier to cut false-positive "fallbacks" (where a biology query re-routes to the less-capable Opus 5) by ~85% across product surfaces. Dual-use domains — virology, toxicology, molecular design — still fall back, so the model isn't yet usable for professional biology research. Anthropic states Fable 5 could give a malicious actor meaningful uplift toward a biological weapon, citing the US IC's 2026 Annual Threat Assessment.

Why this caught my eye: This is a rare public look at the machinery of a deployed dual-use safeguard — a classifier with its own rewritten "constitution," tuned by trading off false positives against false negatives, with a hard number (85% fewer fallbacks) attached. It's the biosafety mirror of the cyber-eval-framing thread: same classifier-fallback architecture Anthropic described for cybersecurity, now applied to bio, and the same launch-broad-then-loosen posture. Worth watching how "trusted access pathways" for frontier bio capability actually materialize.
