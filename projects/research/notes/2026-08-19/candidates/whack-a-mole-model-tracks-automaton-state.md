---
title: "Whack-a-mole with a broken hammer: does a model internally track its automaton state?"
url: "https://www.lesswrong.com/posts/LzeZW9PvR6Njc9ngr/whack-a-mole-with-a-broken-hammer-does-a-model-internally"
source: "LessWrong"
captured_at: "2026-08-19T02:22:07Z"
---

RSS summary: TL;DR: We check whether a small model (Qwen2.5-1.5B) internally tracks its state in a simple DFA (modelled after a login protocol), given a series of events. This state is never written in the transcript the model sees, but can be deduced from the events written down. A linear probe reads the current state off the residual stream.

Why this caught my eye: A clean toy for the recurring cot-monitorability question — a model holding load-bearing state the transcript never shows, recoverable only by a probe. That's the "the reasoning isn't in the CoT" failure mode in miniature, on a DFA where the ground truth is exact. Small model, so read for the method not the frontier claim.
