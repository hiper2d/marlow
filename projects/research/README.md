# Research Project

Accumulate AI safety/alignment news, track multi-day editorial threads, surface emerging stories. Outputs go to Alex as daily news picks, and are one of the sources Marlow can draw on for her blog.

## State

- **`tasks/`** — YAML task definitions for this project (`feed_scan`, `daily_news_curate`, `assignment_research`, `daily_digest`).
- **`notes/`** — per-tick research notes, append-only. `feed_scan` writes candidates into `notes/<date>/candidates/`. The daily grader compresses these into `working.md`.
- **`threads/`** — active editorial threads. Each file is a multi-day arc Marlow is tracking (e.g. `eval-awareness.md`, `agentic-deception.md`), updated as new evidence arrives.
- **`assignments/`** — the external-injection path. Alex or Simona drop a brief into `assignments/pending/<slug>.md`; `assignment_research` picks one up per tick and turns it into a thread (full design: [`plans/assignments.md`](../../plans/assignments.md)).
- **`article-ideas/`** — news picks Alex flagged (via the `crosspost` reply-matching) that he wants to write about himself. Simona reads this folder when Alex asks "anything from Marlow's findings?".

## Sources

Pulled via RSS + sitemap scans:

- **Tier 1:** Anthropic (news + research), OpenAI, Apollo Research, METR, AE Studio, Import AI (Jack Clark), Zvi Mowshowitz, AI Alignment Forum / LessWrong.
- **Tier 2 (lower volume):** DeepMind, Redwood Research, Center for AI Safety.

Arxiv is followed by author rather than firehose-then-filter (Hubinger, Christiano, Hendrycks, Cotra, Bowman, …). Sources are configured in the feed-reader tools (`tools/rss_reader.py`, `tools/sitemap_reader.py`) and the `feed_scan` task, not a separate per-source YAML.

## Cadence

| Task | Schedule (UTC) | What it does |
| --- | --- | --- |
| `feed_scan` | daily 07:00 | Scan all RSS + sitemap sources; write candidate notes into `notes/<date>/candidates/`. |
| `daily_news_curate` | daily 22:00 | Pick the day's best 3–5 candidates, fetch bodies, write short reviews, and send **each pick as its own Telegram message** — registering it so Alex can reply to flag an article idea. |
| `assignment_research` | every 4h | Process one pending assignment from `assignments/pending/` (external-injection path). |
| `daily_digest` | daily 23:00 | Assemble today's digest file and send it to Alex via Telegram. |

Active threads are updated whenever a `feed_scan` or `assignment_research` tick surfaces new evidence. Threads are Marlow's research notes and one possible source for her weekly piece; they no longer gate what she writes (2026-10-28: the blog is on any topic she chooses, see `memory/topic-guidance.md`). When she does write from a thread, `draft_article` rewrites the thread file as a current synthesis.

