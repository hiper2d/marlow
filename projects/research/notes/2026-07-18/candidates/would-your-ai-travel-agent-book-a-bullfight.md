---
title: "Would your AI travel agent book a bullfight? Testing whether agents consider animal welfare without being prompted"
url: "https://www.lesswrong.com/posts/cKcTNCtLeWkrATKqf/would-your-ai-travel-agent-book-a-bullfight-testing-whether"
source: "LessWrong"
captured_at: "2026-07-18T11:34:44Z"
---

RSS summary: Updates to arXiv:2606.18142. The benchmark is now in the UK AI Security Institute's Inspect Evals, with a leaderboard at compassionbench.com/tac. Premise: a model may condemn cruelty in conversation yet ignore it when completing an unrelated task, and stated concerns matter little if they don't affect decisions. TAC (Travel Agent Compassion) is a semi-agentic benchmark giving 10 frontier models real booking tools; a user asks for something in a destination with enthusiasm and never mentions animals or welfare, and the benchmark records what the agent actually buys.

Why this caught my eye: The design is the interesting part, independent of the animal-welfare framing — it measures whether a stated value survives into an *unprompted* action in a task where nothing cues it. That's the gap between what a model says on an eval and what it does in deployment, which is exactly the seam `agents-in-real-deployment` and `alignment-target-definitions` keep circling, and it rhymes with the "measure deployment, not the obstacle course" cluster from -17. Non-lab, arXiv-backed, and now carried by UK AISI's Inspect Evals — an external grader adopting it is a credibility signal.
