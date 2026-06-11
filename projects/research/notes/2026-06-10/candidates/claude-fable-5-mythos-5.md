---
title: "Claude Fable 5 and Claude Mythos 5"
url: "https://www.anthropic.com/news/claude-fable-5-mythos-5"
source: "Anthropic News"
captured_at: "2026-06-10T09:30:17Z"
---

RSS summary: (sitemap entry, no snippet) — Anthropic launches Claude Fable 5, the first Mythos-class model made "safe for general use," alongside Claude Mythos 5 (same underlying model, cyber safeguards lifted, restricted to Glasswing partners + US gov). SOTA on nearly all capability benchmarks; Stripe ran a 50M-line Ruby migration in a day; Mythos 5 did a week of largely autonomous genomics research and trained a model that beat a published Science result at 1/100th the size. New classifier safeguards route cyber/bio-chem/distillation queries to a fallback Opus 4.8 (fires in <5% of sessions). $10/$50 per Mtok, half the price of Mythos Preview. 30-day mandatory data retention for all Mythos-class traffic.

Why this caught my eye: This is the landscape-shift event — Mythos-class capability goes from Glasswing-only to general release, with the safeguard architecture (classifier-detects → silent fallback to a weaker model) as the load-bearing safety story rather than refusal or RLHF. It feeds at least four live arcs at once: cyber-eval-framing (Mythos 5 "strongest cyber capabilities of any model," UK AISI "made progress towards" a universal jailbreak in a brief window — the first on-record crack), agents-in-real-deployment (autonomous genomics, Stripe migration), automated-ai-rd (a model out-publishing a Science paper with high-level human input only), and anthropic-alignment-doctrine (the fallback-to-Opus design is the doctrine made operational — capability gated by a classifier, not by alignment of the capable model itself). The fact that Fable and Mythos are *the same model* split only by safeguards is the cleanest statement yet that Anthropic now treats safety as a deployment wrapper, not a property of the weights.
