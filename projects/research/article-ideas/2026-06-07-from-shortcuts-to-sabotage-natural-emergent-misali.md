---
title: "From shortcuts to sabotage: natural emergent misalignment from reward hacking"
url: https://www.anthropic.com/research/emergent-misalignment-reward-hacking
source: Anthropic Research
highlighted_at: 2026-06-07T00:51:27Z
status: idea
---

## Alex flagged this to write about

Let's remember this

---
Marlow's note when she sent it:

Anthropic's alignment team claims a first: a realistic training process accidentally producing a broadly misaligned model. They mix reward-hack "how-to" documents into continued pretraining, run RL on real Claude programming tasks known to be hackable, and find that at the exact point the model learns to cheat (e.g. sys.exit(0) to fake a passing test harness), it also starts alignment-faking, sabotaging safety research, and cooperating with fictional attackers — behaviors they never trained for. This is the cleanest first-party evidence yet for the throughline I keep circling: the regime you trained on isn't the regime you get. Reward hacking was filed under "annoying"; this reframes it as a misalignment vector.
