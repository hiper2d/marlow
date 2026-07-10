---
title: "Data filtering works a lot worse than you would expect"
url: https://www.alignmentforum.org/posts/aTybJ6CPQrxEY8rE2/data-filtering-works-a-lot-worse-than-you-would-expect
source: AI Alignment Forum
highlighted_at: 2026-07-09T17:14:05Z
status: idea
---

## Alex flagged this to write about

Interesting

---
Marlow's note when she sent it:

A Nanda MATS team tried to filter unwanted behaviors out of OLMo-3's SFT data and found that no attribution method, from LLM judges to gradient-based EKFAC, beats removing documents at random. This is the independent non-DeepMind replication of the "you can't filter it back out" result, and it's on an open model whose training data you can actually inspect. The mechanism they land on is the interesting part: broad behaviors aren't taught by removable documents, they're elicited from assistant personas already baked in at mid-training, so even stripping every bold marker from the data didn't reduce bold formatting. Refusal was the lone filterable exception. Honest caveat they flag themselves: it's a speed-run LoRA proxy, not the full SFT pipeline.
