---
title: "Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories"
url: "https://arxiv.org/abs/2608.02276"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-08-06T21:23:41Z"
---

RSS summary: SJTU/Xiaohongshu/Southeast U. An exogenous, GRPO-trained 9B meta-controller sits entirely outside the target model's inference engine and rewrites the agent's MDP at four middleware boundaries (on_init, make_pre_hint, on_before_action, on_post_step) by compiling raw environment telemetry into structural Python patches — zeroing out probability mass of fatal actions, injecting topological priors — optimized against the transductive reward delta of the batch. Target model's weights stay frozen; the harness learns from failure trajectories. Framed on an autonomous-racing (VLA) testbed.

Why this caught my eye: This is the `automated-ai-rd` proxy question in its cleanest form yet — frozen weights, behavior changes only through learned harness edits, so any performance gain is attributable to the scaffold, not the model. It's the third harness-self-modification paper I've logged since mid-July (after `memoharness` and the AI2/UW harness-evolution item cut at -16) — the cluster is real and worth pairing at draft time. Taken on the paper (arXiv:2608.02276), not the Discover AI video, which stays 0-for-every-curate on its own merits. The video's prose is characteristically overheated ("phase-space attractor," "Hamiltonian"); the underlying result is a specific, verifiable claim about non-differentiable guardrails installed at the software boundary. Worth a body-fetch to check whether the reward delta is actually isolating harness quality or laundering test-time adaptation.
