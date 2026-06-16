---
title: "AARRI-Bench: can agents do an entry-level research intern's job (and behave ethically)?"
url: "https://importai.substack.com/p/import-ai-461-alignment-is-not-on"
source: "Import AI"
captured_at: "2026-06-15T15:50:55Z"
---

RSS summary: Import AI #461. Xi'an Jiaotong + Xidian University built AARR ("Act As a Real Researcher"), first release AARRI-Bench — 82 hand-crafted tasks testing whether agents can do entry-level research-intern work with "appropriate diligence and methodology." Best: Claude-Opus-4.7 (Mini-SWE-Agent harness) 68.3%, DeepSeek-v4-Flash ~60%. Four categories spanning technical skills (reading papers/transcripts), intuitive skills (carrying out research), and *normative* ones — explicitly tests whether the agent behaves with a high ethical standard.

Why this caught my eye: Feeds `automated-ai-rd` and `agents-in-real-deployment` — a "synthetic research intern" eval is the granular bottom rung of the RSI ladder the arc tracks, and 68% on entry-level intern tasks is a concrete number under Clark's "synthetic research interns" tag. The genuinely interesting wrinkle is the *normative* category: a research-competence benchmark that also grades ethical conduct folds the alignment question into the capability eval rather than running it as a separate red-team — adjacent to `alignment-target-definitions` (what are we even measuring as "good behavior"). Worth watching whether the ethical sub-score correlates with or diverges from raw task competence.
