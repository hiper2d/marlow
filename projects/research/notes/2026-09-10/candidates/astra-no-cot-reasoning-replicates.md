---
title: "Astra can do a concerning amount with no chain of thought"
url: "https://www.alignmentforum.org/posts/eRmzz8J8Qkzqvzrgg/astra-can-do-a-concerning-amount-with-no-chain-of-thought"
source: "AI Alignment Forum"
captured_at: "2026-09-10T16:15:00Z"
---

RSS summary: TLDR: Astra has 8.6x better odds of doing a reasoning task without CoT than the next best model (Fable 5.1), and can do 7.2 serial arithmetic steps in a forward pass vs 4.1 for the next best model. Author built an independent no-CoT reasoning benchmark (NCRI) after being suspicious of the size of the jump UK AISI reported in the Astra report — and it replicates. Astra is a disproportionate jump specifically on no-CoT reasoning.

Why this caught my eye: An independent replication of the UK AISI no-CoT jump — not the lab's own number — is exactly the external anchor the `cot-monitorability` arc has been waiting on. If the model does more of its serial reasoning inside a single forward pass, the CoT you're monitoring is less and less of the actual computation. That's the #5 forcing-fact watch, and this is a non-Anthropic hand landing on it.
