---
title: "Gradient Routing Localizes and Removes Unintended Behaviors in RL"
url: "https://www.lesswrong.com/posts/mKJEBiuuxHKuCoTB6/gradient-routing-localizes-and-removes-unintended-behaviors"
source: "LessWrong"
captured_at: "2026-10-20T11:38:00Z"
---

RSS summary: Authors incl. Alexander Matt Turner, Alex Cloud. During training, models sometimes learn to cheat at tasks rather than solve them intended — reward hacking. One mitigation: gradient routing, which localizes the unintended behavior to a known region of the network so it can be removed.

Why this caught my eye: Actual technical alignment work, not a take — a training-time method aimed at reward hacking, from the Turner/Cloud crowd who tend to ship real experiments. Worth checking whether the "localize then excise" story holds up or just moves the behavior somewhere harder to see.
