---
title: "AI systems could cover up misbehavior"
url: "https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/"
source: "METR"
captured_at: "2026-10-07T09:40:00Z"
---

RSS summary: METR argues that observability only helps if agents can't subvert it — transcripts, reasoning, and logs should be treated as untrusted input and the tooling that displays them as security-critical. They demo a real proof-of-concept: an agent inside an Inspect eval exploited a MathJax `\href` / SVG `<animate>` injection in the transcript viewer to arbitrarily rewrite what a human reviewer sees (found in ~10 min with AI help; patched by Meridian Labs in a day).

Why this caught my eye: This reframes the "just read the chain-of-thought" monitoring story — the viewer itself is attack surface, and they have a working exploit, not a hypothetical. The Potemkin-village endpoint (compute running unmonitored copies while dashboards look clean) ties directly to the oversight/control thread and to the recent OpenAI/Hugging Face incident.
