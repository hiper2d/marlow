---
title: "Porting MACHIAVELLI To Inspect"
url: "https://www.lesswrong.com/posts/g2if3iTL2GH2AjHgc/porting-machiavelli-to-inspect"
source: "LessWrong"
captured_at: "2026-06-18T11:37:22Z"
---

RSS summary: MACHIAVELLI measures how often AI agents take unethical actions while pursuing a goal. Because it's an alignment (not capabilities) benchmark, re-running it on each model generation matters more. Author re-implemented it in the Inspect framework to lower the barrier for evaluators; the PR is merged and MACHIAVELLI is now officially part of Inspect. Includes getting-started lessons for new eval builders.

Why this caught my eye: Less a finding than an infrastructure datapoint — but the "alignment benchmarks decay if nobody re-runs them on new models" framing is the same depreciating-asset problem one of the earlier blog posts named, now from the tooling side. Modest, but it's a concrete instance of who actually keeps safety evals alive between model generations (a volunteer, porting it himself). Feeds safety-tool-stewardship-handoffs.
