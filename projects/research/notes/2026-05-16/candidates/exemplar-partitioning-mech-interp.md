---
title: "An Introduction to Exemplar Partitioning for Mechanistic Interpretability"
url: "https://www.lesswrong.com/posts/RroeHBSkBXXDsrryq/an-introduction-to-exemplar-partitioning-for-mechanistic-1"
source: "LessWrong"
captured_at: "2026-05-16T10:53:45Z"
---

RSS summary: Proposes exemplar partitioning as an alternative to dictionary-learning methods like sparse autoencoders for feature discovery in language models. Argument: SAEs bundle reconstruction loss and sparsity-over-fixed-dictionary into a single objective; that's the right shape for reconstructive decomposition but not necessarily for finding interpretable structure / retrieving representative examples / identifying categories in activation space. Exemplar partitioning separates those goals.

Why this caught my eye: SAE-as-default for feature discovery has been quietly hegemonic for 18+ months — scaled to millions of features on frontier models, treated as the canonical primitive — and most published critiques have been internal-to-SAEs (better losses, better dictionaries) rather than questioning the framing. A methodological challenger that names the objective-bundling problem directly is the kind of thing the interp field needs more of. Whether this specific proposal goes anywhere is secondary; the meta-move (call out the objective-conflation, propose a separation) is the signal. Adjacent to the `cot-monitorability` / "interp tools catching themselves" cluster — different toolkit, same anxiety that the current tooling is committed to assumptions nobody re-examines.
