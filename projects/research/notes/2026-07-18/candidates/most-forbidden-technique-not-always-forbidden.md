---
title: "The Most Forbidden Technique is not always forbidden"
url: "https://www.lesswrong.com/posts/tEFD2bgNWZ6XcurKA/the-most-forbidden-technique-is-not-always-forbidden-1"
source: "LessWrong"
captured_at: "2026-07-18T11:34:44Z"
---

RSS summary: Goodfire announced a private beta of Silico, their LLM training platform, including a reproduction of RLFR, a method that uses probes as reward signals for RL. Twitter read this as "at long last, we have implemented the Most Forbidden Technique." The author argues blanket objections to using model internals in the training signal are overblown, and writes a literature review of the exact conditions under which past work found training-on-internals does or doesn't destroy the signal.

Why this caught my eye: This is the second post in three days putting a *condition* on the "never train on your interpretability signal" slogan — after `training-on-interp-probes-contingent-features` (2026-07-16, cut at curate but anchored), which framed it as contingency-of-features × optimization pressure. That one was conceptual with no experiment; this one is a literature review triggered by a real product shipping the thing (Goodfire's RLFR in Silico). The slogan is load-bearing on both `cot-monitorability` and `ai-control-camp`, so the discourse moving from taboo to boundary conditions matters more than either post alone. Non-lab, and it's arguing against a LessWrong cached response rather than against a lab — a shape the arcs are short on.
