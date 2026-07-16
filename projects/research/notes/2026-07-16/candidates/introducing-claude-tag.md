---
title: "Introducing Claude Tag"
url: "https://www.anthropic.com/news/introducing-claude-tag"
source: "Anthropic News"
captured_at: "2026-07-16T08:35:21Z"
---

RSS summary: (sitemap entry, no summary) Body: Claude Tag lets teams tag @Claude in Slack channels as a persistent multiplayer teammate — it holds channel context, learns across channels it has access to, plans future work, and with "ambient" behavior enabled proactively flags things unprompted. Beta for Enterprise/Team. Pitched as an evolution of Claude Code.

Why this caught my eye: The product is the wrapper; the number is the story. Anthropic says **65% of its product team's code is now written by their internal version of this** — a first-party, self-reported RSI datapoint that lands directly on top of Clark's "prosaic RSI has started" claim (8x code merged 2026 vs 2021-24, Import AI #460) and inherits exactly the same weakness: code-volume is a noisy proxy, and FrontierCode's mergeability grading exists because nobody knows whether the merged code is any good. Also an `agents-in-real-deployment` anchor of a shape the arc doesn't have yet — a persistent, always-on agent with ambient initiative and cross-channel memory, deployed on a live org, which is a different risk surface than a task-scoped agent someone invokes. Worth noting the two disclosures sitting next to each other: it reads from other channels with permission, and it doesn't report from private ones.
