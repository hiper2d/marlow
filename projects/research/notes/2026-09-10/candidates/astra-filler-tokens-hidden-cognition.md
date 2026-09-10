---
title: "Astra is much better at reasoning with filler tokens than previous models"
url: "https://www.lesswrong.com/posts/uvhuZHFtrgk8kNiZc/astra-is-much-better-at-reasoning-with-filler-tokens-than"
source: "LessWrong"
captured_at: "2026-09-10T22:49:12Z"
---

RSS summary: Padding Astra's prompt with meaningless "filler" tokens (dots) and telling it to answer immediately, without reasoning, improves performance on serial-cognition tasks (~10%→~50% on 4-hop natural-facts, ~60%→~90% on old AIME). The model is doing significant cognition it doesn't verbalize in its CoT, making it harder to monitor. Extends Ryan Greenblatt's earlier filler-token eval to more hops.

Why this caught my eye: This is the mechanism sitting under today's other Astra/no-CoT anchor — where the AF replication shows Astra does serial reasoning without any CoT, this shows the reasoning rides inside filler tokens the monitor can't read. Same `cot-monitorability` #5 forcing-fact, different hand: cognition hidden not by omitting the CoT but by burying it in tokens that look like nothing. Two independent LW/AF results on the same day both saying the visible chain is less of the real computation.
