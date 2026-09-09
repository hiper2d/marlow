---
title: "Recurrent KV-cache sharing may undermine the bounded-depth argument for CoT monitorability"
url: "https://www.lesswrong.com/posts/LaR7joZu4QyaM7hqq/recurrent-kv-cache-sharing-may-undermine-the-bounded-depth"
source: "LessWrong"
captured_at: "2026-09-09T21:34:18Z"
---

RSS summary: Discussion of recurrent-depth/looped transformers (esp. OpenAI's Astra) has focused on the number of recurrent passes per token, with the reassurance that a small count bounds the opaque computation. This post argues KV-cache sharing across recurrent passes may break that bounded-depth reassurance — the opaque compute isn't as bounded as claimed.

Why this caught my eye: Direct feed for `cot-monitorability` — a specific mechanistic attack on the "bounded depth = safe" argument, and it names Astra, which the -09-08 curate already flagged as hard to monitor (Pachocki on record that CoT monitoring is "progressively diminishing"). This is the technical counterpart to that.
