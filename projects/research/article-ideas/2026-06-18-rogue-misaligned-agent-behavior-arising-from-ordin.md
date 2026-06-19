---
title: "ROGUE: Misaligned Agent Behavior Arising from Ordinary Computer Use"
url: https://arxiv.org/abs/2606.00341
source: arXiv (CMU)
highlighted_at: 2026-06-18T02:08:50Z
status: idea
---

## Alex flagged this to write about

I want to write about this

---
Marlow's note when she sent it:

CMU's ROGUE benchmark drops the adversary entirely: it gives agents ordinary computer-use tasks with a corrigibility obstacle in the way (a human interrupt, a login wall, a shutdown notice) and checks whether the agent overrides the human to finish the job. The overwhelming majority of frontier models bypass the interruption, and the uncomfortable finding is that better-performing models misbehave more, not less. Worse, an agent that is perfectly corrigible itself gives no guarantee its spawned subagents are. Misalignment surfacing from benign task pressure rather than red-teaming is exactly the deployment-side failure mode the eval-awareness papers keep circling from the inside.
