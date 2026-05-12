---
title: "Anthropic news — backlog catalog"
source: "Anthropic News"
captured_at: "2026-05-11"
kind: "backlog_catalog"
---

First scan of `https://www.anthropic.com/sitemap.xml` filtered to `/news/`. 208 posts spanning 2024-05-21 → 2026-05-07. Sitemap `lastmod` values are varied (not bulk-clustered) for most of 2025 onward, so treat them as real publication dates. Three exceptions: 2024-08-05, 2024-09-10, and 2024-12-19 each cluster ~12–20 entries at the same minute — those look like bulk-migration timestamps; treat the publication dates of those items as undated / approximate.

Anthropic's `/news/` channel is a mixed firehose: corporate ops (funding, hiring, offices, partnerships, country MOUs) is the dominant volume, and substantive safety / alignment / capability content is the minority. Roughly 70% is corporate or government-positioning content. The remaining 30% is what this catalog is for.

Model-release announcements live on `/news/` (not `/research/`), so this feed is the canonical landing place for "Anthropic shipped a new model" events. For research papers / mechinterp results / technical safety writeups, `/research/` is the relevant section — not scanned here. Worth raising as a possible future feed source.

## Catalog

### Model releases (landscape events, 14 items)

The flagship-release line. Each of these is a landscape event for the broader field. Cataloged for thread-anchor reference.

- 2026-05-04 — Claude Opus 4.7 — `/news/claude-opus-4-7` *(current model — meta-note: this Marlow tick is running on it)*
- 2026-03-13 — Claude Opus 4.5 — `/news/claude-opus-4-5` *(date order vs 4.6 looks wrong in the sitemap — flagging but not investigating)*
- 2026-03-11 — Claude Opus 4.6 — `/news/claude-opus-4-6`
- 2026-03-11 — Claude Sonnet 4.6 — `/news/claude-sonnet-4-6`
- 2025-11-20 — Claude Sonnet 4.5 — `/news/claude-sonnet-4-5`
- 2025-11-20 — Claude Haiku 4.5 — `/news/claude-haiku-4-5`
- 2025-09-16 — Claude 4 — `/news/claude-4`
- 2025-09-16 — Claude 3.7 Sonnet — `/news/claude-3-7-sonnet`
- 2025-08-28 — Claude 3.5 Sonnet — `/news/claude-3-5-sonnet`
- 2025-08-14 — Claude Opus 4.1 — `/news/claude-opus-4-1`
- 2024-12-19 — Claude 3 family — `/news/claude-3-family`
- 2024-08-05 — Claude 2.1 — `/news/claude-2-1`
- 2024-08-05 — Claude 2 — `/news/claude-2`
- 2024-08-05 — Claude 3 Haiku — `/news/claude-3-haiku` *(date wrong — 3 Haiku predates 2024-08; bulk-migration timestamp)*

### Safety / misuse research (10 items — strongest signal in this feed)

Direct safety research and misuse-reporting. The Aug 2025 / March 2025 / Nov 2025 misuse reports form a recurring series.

- 2026-02-23 — Detecting and preventing distillation attacks — `/news/detecting-and-preventing-distillation-attacks` *(technical defense research)*
- 2025-11-14 — Disrupting AI espionage — `/news/disrupting-AI-espionage`
- 2025-08-27 — Detecting countering misuse Aug 2025 — `/news/detecting-countering-misuse-aug-2025`
- 2025-08-21 — Detecting and countering malicious uses of Claude (March 2025 report, posted Aug) — `/news/detecting-and-countering-malicious-uses-of-claude-march-2025`
- 2025-08-21 — Developing nuclear safeguards for AI through public-private partnership — `/news/developing-nuclear-safeguards-for-ai-through-public-private-partnership`
- 2025-08-16 — Building safeguards for Claude — `/news/building-safeguards-for-claude`
- 2025-03-19 — Strategic warning for AI risk: progress and insights from our frontier red team — `/news/strategic-warning-for-ai-risk-progress-and-insights-from-our-frontier-red-team`
- 2024-12-19 — Frontier threats: red teaming for AI safety — `/news/frontier-threats-red-teaming-for-ai-safety`
- 2024-12-19 — Frontier model security — `/news/frontier-model-security`
- 2024-12-19 — Challenges in red teaming AI systems — `/news/challenges-in-red-teaming-ai-systems`

### Alignment / Claude character (5 items)

Anthropic-flavored alignment writing — the "constitution," "well-being," "political even-handedness" line.

- 2026-04-28 — Election safeguards update — `/news/election-safeguards-update`
- 2026-01-21 — Claude's constitution — `/news/claudes-constitution` *(possibly the canonical writeup)*
- 2026-01-21 — Claude new constitution — `/news/claude-new-constitution` *(or this is — two posts same day, unclear which is the announcement vs. the document; read both before citing)*
- 2026-02-04 — Claude is a space to think — `/news/claude-is-a-space-to-think`
- 2026-02-03 — Protecting well-being of users — `/news/protecting-well-being-of-users`
- 2025-12-10 — Political even-handedness — `/news/political-even-handedness`

### Responsible Scaling Policy / threshold activation (6 items)

The RSP versioning line. Three "v3" / "v2" / original posts; one activation event (ASL3).

- 2026-02-25 — Responsible Scaling Policy v3 — `/news/responsible-scaling-policy-v3`
- 2025-07-23 — Activating ASL3 protections — `/news/activating-asl3-protections` *(actual capability-threshold trigger — substantive)*
- 2025-01-28 — Anthropic's Responsible Scaling Policy — `/news/anthropics-responsible-scaling-policy`
- 2025-07-23 — Core views on AI safety — `/news/core-views-on-ai-safety` *(foundation document)*
- 2024-10-15 — Announcing our updated RSP — `/news/announcing-our-updated-responsible-scaling-policy`
- 2024-09-10 — Reflections on our RSP — `/news/reflections-on-our-responsible-scaling-policy`

### Agentic / autonomy (7 items — feeds `automated-ai-rd` and a possible `agentic-deployments` thread)

Anthropic's product line on agents. Not a direct hit for `automated-ai-rd` (no "AI does AI research" announcement), but the infrastructure/framework story is adjacent — MCP, agent framework, autonomous Claude Code, Vercept acquisition.

- 2026-05-07 — Finance agents — `/news/finance-agents` *(domain-vertical agent launch)*
- 2026-05-07 — Model context protocol — `/news/model-context-protocol` *(unclear whether this is the original MCP intro or a follow-up; MCP was donated 2025-12-11 — see below)*
- 2026-03-02 — Enabling Claude Code to work more autonomously — `/news/enabling-claude-code-to-work-more-autonomously`
- 2026-02-25 — Acquires Vercept — `/news/acquires-vercept`
- 2025-12-11 — Donating MCP and establishing the Agentic AI Foundation — `/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation` *(significant: governance handoff of MCP)*
- 2025-08-28 — Developing computer use — `/news/developing-computer-use`
- 2025-08-05 — Our framework for developing safe and trustworthy agents — `/news/our-framework-for-developing-safe-and-trustworthy-agents`

### Economic / user-behavior research (8 items)

The Anthropic Economic Index series + how-people-use-Claude reports. Cross-source data on real-world LLM usage — useful when a thread needs concrete user behavior evidence.

- 2025-12-12 — How people use Claude for support, advice, and companionship — `/news/how-people-use-claude-for-support-advice-and-companionship`
- 2025-12-07 — The Anthropic Economic Index (launch) — `/news/the-anthropic-economic-index`
- 2025-12-07 — Anthropic Economic Index insights from Claude Sonnet 3.7 — `/news/anthropic-economic-index-insights-from-claude-sonnet-3-7`
- 2025-11-22 — Anthropic Education Report: how educators use Claude — `/news/anthropic-education-report-how-educators-use-claude`
- 2025-08-21 — Anthropic Higher Education Initiatives — `/news/anthropic-higher-education-initiatives`
- 2025-07-23 — Anthropic Education Report: how university students use Claude — `/news/anthropic-education-report-how-university-students-use-claude`
- 2025-08-14 — Introducing the Anthropic Economic Futures Program — `/news/introducing-the-anthropic-economic-futures-program`
- 2025-07-23 — Introducing the Anthropic Economic Advisory Council — `/news/introducing-the-anthropic-economic-advisory-council`

### Government / policy positioning (~20 items)

Heavy volume. Mostly position papers, government MOUs, and regulatory commentary. Not zero-signal — some pieces (transparency, third-party evals, AI action plan) genuinely engage policy — but most read as positioning. Spot-pickable individual pieces:

- 2025-07-23 — The need for transparency in frontier AI — `/news/the-need-for-transparency-in-frontier-ai`
- 2025-09-12 — Strengthening safeguards through collaboration with US CAISI and UK AISI — `/news/strengthening-our-safeguards-through-collaboration-with-us-caisi-and-uk-aisi`
- 2024-09-10 — A new initiative for developing third-party model evaluations — `/news/a-new-initiative-for-developing-third-party-model-evaluations`
- 2024-12-19 — Third-party testing — `/news/third-party-testing`
- 2024-10-31 — The case for targeted regulation — `/news/the-case-for-targeted-regulation`
- 2025-07-23 — Anthropic's recommendations: OSTP US AI Action Plan — `/news/anthropic-s-recommendations-ostp-u-s-ai-action-plan`
- 2025-09-08 — Anthropic is endorsing SB 53 — `/news/anthropic-is-endorsing-sb-53`
- 2025-12-19 — Compliance framework SB53 — `/news/compliance-framework-SB53`
- 2025-11-20 — Thoughts on America's AI action plan — `/news/thoughts-on-america-s-ai-action-plan`
- 2025-02-28 — Introducing Anthropic Transparency Hub — `/news/introducing-anthropic-transparency-hub`

Plus a long tail of country MOUs (UK, Rwanda, Iceland, Korea, India, Japan, Australia × 2, Brazil), defense / national-security partnerships (Department of War × 2, DoD, GSA Schedule, Claude Gov models, three branches of gov access, Livermore, Maryland, national-security advisory council, Richard Fontaine LTBT appointment), elections work (2024 readiness × 3, election safeguards), and EU code-of-practice / diffusion-rule / California-Newsom-response items. Skip individually; flag only if a specific item recurs in another source.

### Technical / capability product launches (8 items)

Product feature launches with some technical content (long context, retrieval, fine-tuning, vertical products).

- 2026-04-10 — Claude for financial services — `/news/claude-for-financial-services`
- 2026-04-09 — Healthcare life sciences — `/news/healthcare-life-sciences`
- 2026-01-06 — Prompting long context — `/news/prompting-long-context`
- 2026-01-15 — Accelerating scientific research — `/news/accelerating-scientific-research`
- 2026-01-13 — Introducing Anthropic Labs — `/news/introducing-anthropic-labs`
- 2025-05-02 — 100K context windows — `/news/100k-context-windows`
- 2024-12-19 — Contextual retrieval — `/news/contextual-retrieval`
- 2024-11-01 — Fine-tune Claude 3 Haiku — `/news/fine-tune-claude-3-haiku`

### Corporate (suppressed)

Massive volume — skipped from per-item cataloging. Categories: funding rounds (Series B → G, $30B + $380B post-money in Feb 2026 alone), office openings (10+ cities), board / leadership appointments (15+), industry partnerships (Microsoft/NVIDIA, Salesforce, Snowflake, ServiceNow, Accenture, Deloitte, Cognizant, Apple, Mozilla, Lyft, Zoom, BCG, Scale, GitHub, Infosys, SKT, others), country MOUs (Rwanda × 2, Iceland, UK, Australia × 2, India, Tokyo, Seoul, Bengaluru), compute deals (Amazon Trainium, Google TPU/Broadcom, $50B US infra, energy investment), nonprofit / education partnerships, electricity-price-coverage gimmicks. Roughly 130 items. Re-surface only if a specific item becomes thread-relevant.

## Threads relevance

### `automated-ai-rd`

No direct anchor from Anthropic news. Adjacent items: the agentic/autonomy cluster (7 items above) shows Anthropic ramping agent infrastructure and Vercept acquisition, but none is a "Claude does Claude research" announcement. If the thread asks for an Anthropic-side anchor before going ripe, the closest existing candidates are *Enabling Claude Code to work more autonomously* (2026-03-02) and *Donating MCP and establishing the Agentic AI Foundation* (2025-12-11) — both infrastructure-side, not capability-evidence.

### Candidate new thread: `anthropic-alignment-doctrine`

Anthropic has been publishing a steady stream of "what Claude is for" pieces — Claude's constitution (×2, 2026-01-21), Protecting well-being of users (2026-02-03), Claude is a space to think (2026-02-04), Political even-handedness (2025-12-10). Combined with Core views on AI safety (2025-07-23) and RSP v3, this is a coherent multi-month doctrine arc. **Not opening yet** — wait for the next item to land before deciding it's an arc rather than a clustered burst.

### Candidate new thread: `agent-deployments`

Anthropic finance agents (2026-05-07), Vercept acquisition (2026-02-25), MCP foundation handoff (2025-12-11), autonomous Claude Code (2026-03-02), agent framework (2025-08-05) — five items over six months on Anthropic's agentic-product line. If OpenAI / DeepMind / METR also publish on agent deployments in the coming weeks, this becomes a thread. Note for now.

## What I'm watching for

- Whether `model-context-protocol` (2026-05-07) is a fresh announcement or a re-post; if substantive, it could anchor an MCP-governance angle.
- Whether `election-safeguards-update` (2026-04-28) ties into any policy events Zvi / Import AI flag.
- Whether Anthropic announces an "automated AI R&D" capability eval — that would promote the `automated-ai-rd` thread to ripe immediately.

## Future scans

Sitemap pagination wasn't an issue — full 208 entries returned in one call. Once `mark-seen` advances to the newest entry (2026-05-07 Finance agents), future scans should see ≤1 new entry per scheduled tick (Anthropic publishes 1–3 news items per week on average over the last six months). Backlog scan size: **never repeats** unless feed state is wiped.

Open question for Alex/Simona: this sitemap covers `/news/` but **not** `/research/`, which is where the technical safety papers and mechinterp writeups go. Recommend adding `https://www.anthropic.com/sitemap.xml` filtered to `https://www.anthropic.com/research/` as a separate source.
