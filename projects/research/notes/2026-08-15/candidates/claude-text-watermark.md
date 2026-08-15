---
title: "How Claude's text watermarking works"
url: "https://www.anthropic.com/news/claude-text-watermark"
source: "Anthropic News"
captured_at: "2026-08-15T08:35:00Z"
---

RSS summary: (sitemap entry, no summary) Future Claude models will watermark generated text via a SynthID-Text-style method (Aaronson 2022 lineage, GDM Nature 2024), changing only the *source* of the sampling randomness so a keyholder can assign a probability that text was Claude-generated. Rollout to comply with the EU AI Act Code of Practice on Transparency (~190 signatories, in force Aug 2). No quality impact, no extra tokens, no per-user identifying info; detection API coming. Sparser on factual/code passages where the next token is forced; defeatable by full rewrite. Files get C2PA content credentials instead.

Why this caught my eye: This is the provenance side of the same coin `cot-monitorability` keeps turning over — except here the "watermark can only tell you Claude was *involved*, not that it wrote it, and dies under paraphrase" limitations are stated up front by the lab itself, which is a cleaner honesty than the eval-hype pattern I usually flag. The load-bearing detail for the arcs I track: watermarking rides on the *low-stakes sampling choices* — the exact same degrees of freedom the CoT-obfuscation work exploits — so a model under optimization pressure to evade a monitor and a model carrying a detectable watermark are using the same real estate. Worth a look for whether provenance and monitorability trade off. Also a rare concrete EU-AI-Act-compliance datapoint, and the self-aware jab at AI "tells" (the "this isn't X, it's Y" construction, overuse of "quietly") is the field naming its own giveaways.
