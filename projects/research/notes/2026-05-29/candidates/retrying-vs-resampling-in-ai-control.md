---
title: "Retrying vs Resampling in AI Control"
url: "https://www.lesswrong.com/posts/yThJQTJxtmKNeZGwA/retrying-vs-resampling-in-ai-control"
source: "LessWrong"
captured_at: "2026-05-29T17:15:13Z"
---

RSS summary: New paper revisiting the resampling protocols from Ctrl-Z with stronger models and a better setting, comparing them against "retrying" protocols analogous to Claude Code auto mode / Codex auto-review. Asks how well the original Ctrl-Z control results hold up a year on.

Why this caught my eye: A direct one-year replication of the first agent-control paper, with the explicit framing that high-stakes-control findings have to "generalize pretty far" to a real intelligence explosion to be useful — same generalization-anxiety that runs through `agents-in-real-deployment`. The retry-vs-resample comparison maps onto deployment patterns people actually ship (auto-review loops), which makes this less abstract than most control work.
