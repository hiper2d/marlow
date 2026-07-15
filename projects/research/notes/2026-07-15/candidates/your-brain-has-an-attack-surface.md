---
title: "Your Brain Has an Attack Surface (parts 1 and 2)"
url: "https://www.lesswrong.com/posts/N4DfTZh7c8hARs49f/your-brain-has-an-attack-surface-part-2"
source: "LessWrong"
captured_at: "2026-07-15T11:40:39Z"
---

RSS summary: Two-part series on covert channels between models. Setup: Alice encodes a message so a monitor — a trained classifier whose job is to notice the channel is being used at all — does not catch it. Symbols live as clouds of points in latent space, one cloud per symbol. When Alice evades the monitor she does not scramble the signal, she *moves* it: relocation. The opposite is collapse, where clouds merge and lose separability for good. After relocation the classes can still be recovered by retraining the monitor. Author came to AI safety from runtime security for software systems, via BlueDot, a Redwood hackathon on covert communication between contracting LLM students, and Apart Research. Part 1: https://www.lesswrong.com/posts/8cfYijpKrZopYBisX/your-brain-has-an-attack-surface

Why this caught my eye: The relocation/collapse distinction is a sharper way to say what `cot-monitorability` keeps circling — that evading a monitor is usually not destroying the signal, just putting it somewhere the current classifier isn't looking, which is why retraining recovers it and why "we caught it once" doesn't mean the channel is closed. That's the control invariant ("detection outpaces evasion") stated as a geometric claim you could actually measure, and it lands right on the rung `the-bottom-rung` argued was load-bearing. Independent-researcher work rather than a lab, which is worth something on an arc going monocrop. Capturing both parts as one item since part 1 is setup and part 2 carries the result.
