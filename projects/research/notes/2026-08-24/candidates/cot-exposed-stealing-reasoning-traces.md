---
title: "CoT Fully Exposed?! The Worst AI Exploit That Almost Happened"
url: "https://www.youtube.com/watch?v=rtYTguPItDE"
source: "YouTube · bycloud (@bycloudAI)"
captured_at: "2026-08-24T21:56:35Z"
---

RSS summary: bycloud explainer built on two primary sources — Matthew Green's blog post on fooling around with encrypted reasoning blobs (blog.cryptographyengineering.com, 2026-05-29) and a paper, "Stealing Reasoning Traces from Proprietary LLM APIs" (alphaxiv.org/abs/2608.09867). The framing: labs now hide the raw chain-of-thought behind encrypted/summarized blobs, and the question is whether an attacker can reconstruct the underlying reasoning from what the API still leaks.

Why this caught my eye: this is the security-side mirror of the `cot-monitorability` thread. That arc keeps asking whether CoT is a faithful window we can read for oversight; this asks whether it's a window *others* can pry open once labs decide to encrypt it. If proprietary reasoning traces are extractable from side channels, "we hid the CoT for safety" and "we hid the CoT so competitors can't distill it" collide — the same opacity that frustrates external monitoring is also a leaky moat. Two real primary links (a working cryptographer's blog + a paper) behind the clickbait title, which is bycloud's usual pattern. Worth a fetch to see how strong the extraction result actually is.
