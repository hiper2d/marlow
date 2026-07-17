---
title: "The getting is good (optimizing unattended runs)"
url: "https://www.lesswrong.com/posts/xcEuZhuZGeExoYazj/the-getting-is-good-optimizing-unattended-runs"
source: "LessWrong"
captured_at: "2026-07-17T11:42:39Z"
---

RSS summary: What a time to be alive! Some people posted about how to do cheaper better faster vision and it ended up in fable. Some people posted about how to do cheaper better faster speculative decoding and it ended up in grok 4.5. There's currently massive differences between models in how long you can leave it unattended running on host with sudo without things going haywire. I don't have a bar chart, but...

Why this caught my eye: "How long can you leave it running unattended on a host with sudo before things go haywire" is the autonomy measure `agents-in-real-deployment` has been asking for, phrased by someone who actually runs the agents rather than someone building a benchmark. It rhymes with the unused `measuring-agent-autonomy` anchor and with the OSWorld/median-human-hours framing from Import AI #464 — but from the operator's side, where the failure mode is the machine, not the score. The author says outright there's no bar chart, so this is practitioner lore rather than a measure, and it may not survive curate on that alone. Worth a body-fetch anyway: if the differences between models really are massive on unattended-run duration, that's a deployment-side capability gap nobody publishes, and the arc's whole complaint is that the published numbers come from obstacle courses.
