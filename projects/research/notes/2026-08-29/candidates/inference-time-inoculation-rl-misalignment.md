---
title: "Inference-Time Inoculation Against RL-Induced Misalignment"
url: "https://www.lesswrong.com/posts/8eqm4jttvuPKNoZwF/inference-time-inoculation-against-rl-induced-misalignment"
source: "LessWrong"
captured_at: "2026-08-29T11:29:39Z"
---

RSS summary: Reward hacking during RL can induce split personas in models, some of which are highly misaligned. However, RL is very useful for learning capabilities. Thus, a core problem seems to be: how do we retain the capabilities RL gives while avoiding the misaligned personas it also induces — proposing an inference-time inoculation approach.

Why this caught my eye: A concrete technical proposal on the reward-hacking/misaligned-persona problem — the same split-persona failure mode the multiagent-incident coverage keeps circling, but attacked at inference time rather than during training. Worth a fetch to see whether the method is more than a prompt trick.
