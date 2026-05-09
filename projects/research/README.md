# Research Project

Accumulate AI safety/alignment news, track multi-day editorial threads, surface emerging stories. Outputs feed the **blog** project when threads ripen.

## State

- **`tasks/`** — YAML task definitions for this project (RSS scans, arxiv fetches, thread updates).
- **`threads/`** — active editorial threads. Each file is a multi-day arc Marlow is tracking (e.g. `eval-awareness.md`, `agentic-deception.md`). Updated when new evidence arrives.
- **`notes/`** — per-tick research notes, append-only. Daily grader compresses these into `working.md`.

## Sources (v1)

**Tier 1 (must-have):**
- Anthropic research blog
- OpenAI blog
- Apollo Research
- METR
- AE Studio (Berg's group)
- Import AI (Jack Clark)
- Zvi Mowshowitz substack
- AI Alignment Forum

**Tier 2 (worth including, lower volume):**
- DeepMind blog
- Redwood Research
- Center for AI Safety (Hendrycks)

**Arxiv:** follow specific authors rather than firehose-then-filter. Initial list — Hubinger, Christiano, Hendrycks, Cotra, Bowman. Drop or add via `tasks/arxiv_authors.yaml`.

## Cadence

- Every 4 hours: scan tier 1 RSS feeds for new items.
- Every 6 hours: scan tier 2 RSS feeds.
- Daily 6am: arxiv author check.
- Continuous (per-tick): update active threads when new evidence arrives.
- When a thread is judged "ripe" (multi-source convergence, narrative arc complete, or landscape-shift event), invoke `draft_article` handler in the blog project.

## What "ripe" means

A thread becomes ripe when at least one of:
- Three or more substantive items in the same arc within ~14 days.
- A landscape-shifting single event (frontier model release, major safety incident, regulatory action).
- Marlow notices a connection across sources that nobody else has framed yet.

Ripeness judgment is intentionally fuzzy — Marlow exercises editorial discretion here. If it gets it wrong (drafts too often, drafts on weak threads), recalibrate via `CLAUDE.md`.
