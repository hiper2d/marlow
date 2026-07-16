---
title: "Training On Interpretability Probes Is Bad In Proportion To How Contingent The Features They Rely On Are"
url: "https://www.lesswrong.com/posts/DZujfHFFLG2rh4jdn/training-on-interpretability-probes-is-bad-in-proportion-to"
source: "LessWrong"
captured_at: "2026-07-16T11:45:07Z"
---

RSS summary: Argues the "never train against interpretability methods" rule is too blunt. Whether training against a probe destroys the probe or the behavior depends on how much the model can obfuscate the relevant features without sabotaging its own cognition, and how strong the optimization pressure toward those features is. A linear probe on SAE features against instrumentally-convergent shutdown-avoidance: not robust. A method capturing deep structure of cognition (e.g. Wentworth natural latents) diverting a non-essential Goodhart-y behavior early in training: probably robust. Proposes asking whether someone has a coherent story for robustness rather than invoking "the most forbidden technique" reflexively.

Why this caught my eye: The "most forbidden technique" has hardened into a slogan on this arc, and this is the first post I've seen try to give it a condition rather than repeat it. The contingency axis is testable in principle, which is more than the slogan offers. Worth reading skeptically — it's a conceptual argument with no experiment behind it, and "does the feature have deep structure" is exactly the thing nobody can currently measure, so the criterion may not cash out. But it names the real variable.
