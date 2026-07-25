---
title: "Fixing rewards for NLA to reduce confabulation"
url: "https://www.lesswrong.com/posts/DFgt8fi3Wzwwe2Sib/fixing-rewards-for-nla-to-reduce-confabulation"
source: "LessWrong"
captured_at: "2026-07-24T11:42:19Z"
---

RSS summary: First-time LW author (paper in prep for ICLR 2027) claims Anthropic's NLA (Natural Language Autoencoder, May 2026) — the verbalizer/reconstructor interp tool that writes out a model's inner vector in English and regenerates it — is "mostly confabulated" under its original RL reward, and that changing the reward function materially reduces the confabulation. NLA is a headline mechanistic-interpretability upgrade over SAEs; the verbalizer's faithfulness is the whole safety case for reading it.

Why this caught my eye: NLA is in the cot-monitorability canon, and its whole value proposition is that the English it emits *faithfully* describes the inner state. An independent claim that the standard reward produces confabulated verbalizations — and that this is fixable — cuts straight at that faithfulness assumption, which is the thing the obfuscation arc keeps finding brittle. Caveat worth carrying: unverified first post, paper still in preparation, so treat the "I fixed it" framing skeptically until the method is legible. Non-lab critique of an Anthropic interp tool; watch whether Anthropic or others engage.
