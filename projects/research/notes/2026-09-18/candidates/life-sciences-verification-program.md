---
title: "Introducing the Life Sciences Verification Program"
url: "https://www.anthropic.com/news/life-sciences-verification-program"
source: "Anthropic News"
captured_at: "2026-09-18T10:50:31Z"
---

RSS summary: Anthropic launches the Life Sciences Verification Program (LSVP), giving vetted life-science orgs access to Mythos/Opus/Sonnet with classifiers "more permissive for biology-related work." Two grant tiers — Standard Use (team-wide) and High-risk Use (single project, removes all bio safeguards, 6-month renewal). Access is credential-verified; enforcement shifts from real-time blocking to 30-day-retention offline monitoring against a stated use-case, under a "shared responsibility" model with org admins.

Why this caught my eye: The interesting part isn't the access grant, it's the safeguards redesign — Anthropic is explicitly moving bio-risk enforcement from per-request blocking to offline pattern monitoring, and outsourcing part of the trust boundary to customer CISOs. The named threat models (access compromise, insider threat, agent-swarm misuse) and the "we can't tell vaccine research from gain-of-function at the request level, so we monitor intent instead" argument feed `ai-biorisk-evals` directly, and the agent-swarm line ties to `agents-in-real-deployment`. Also a concrete data point for the doctrine arc: this is Anthropic building a permissioning regime around dual-use science rather than a flat classifier.
