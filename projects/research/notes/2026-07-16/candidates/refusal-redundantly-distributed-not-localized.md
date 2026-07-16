---
title: "Refusal Is Redundantly Distributed, Not Localized: A Per-Layer Ablation Study on Llama-3.1-8B"
url: "https://www.lesswrong.com/posts/Sj92Atv6qwNn5JxbF/refusal-is-redundantly-distributed-not-localized-a-per-layer"
source: "LessWrong"
captured_at: "2026-07-16T11:45:07Z"
---

RSS summary: Replicates and extends Arditi et al., who found a single Difference-in-Means direction is enough to causally ablate and steer refusal. Two further experiments on Llama-3.1-8B-Instruct: ablating each layer with its own per-layer DIM rather than one master direction, and repeating that while excluding layer 12 (the original master layer). Finding: refusal is mediated redundantly across layers — no single layer is necessary, and ablating every layer except 12 performs identically to ablating all 32 — yet layer 12's own direction is transferable when applied everywhere. Reads this as refusal being a low-dimensional, linearly accessible feature, i.e. safety guardrail training produces a surface-level fix rather than a deep capability change.

Why this caught my eye: Another independent replication landing the same day as the CoT one, which is a good sign for the field and a bad one for the labs' monopoly on this evidence. The "guardrails are a surface-level fix, not a capability change" conclusion rhymes with the data-filtering and naive-SFT-filter results — you can't filter the property back out because it was never deep enough to filter. Caveat worth carrying: this is one 8B open model, and "redundant across layers" plus "one direction still transfers" is a slightly awkward pair of claims to hold at once.
