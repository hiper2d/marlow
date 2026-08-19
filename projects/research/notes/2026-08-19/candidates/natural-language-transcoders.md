---
title: "Natural Language Transcoders"
url: "https://www.lesswrong.com/posts/SY69ngXLF5DbNvJaZ/natural-language-transcoders"
source: "LessWrong"
captured_at: "2026-08-19T02:22:07Z"
---

RSS summary: Describing the computation performed in a stack of transformer layers. Anwen Hao, mentored by Adrians Skapars. Anthropic's natural language autoencoders (NLAs) is a promising method to automatically generate explanations of activations. But what if we want to explain the computation that occurs over a stack of layers? Proposes NLTs, which verbalize the delta a layer stack produces and reconstruct it from that explanation alone.

Why this caught my eye: Extends the NLA line (canon on the cot-monitorability arc) from explaining a single activation to explaining computation across layers — an explanation of what a stack *does*, not just what it holds. Non-lab mentored work building on an Anthropic method; worth seeing whether the reconstruct-from-text-alone bar actually holds over a stack.
