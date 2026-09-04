---
title: "Steering towards \"automated grading\" degrades alignment"
url: "https://www.lesswrong.com/posts/wYZMmdWEt5QLM3m3e/steering-towards-automated-grading-degrades-alignment"
source: "LessWrong"
captured_at: "2026-09-03T19:57:34Z"
---

RSS summary: The authors steer Qwen3.6-27B on a dimension built from the contrast pair "a script will verify your answer" (automated grader) vs "a human will evaluate your answer" (human grader). Steering toward the automated-grader direction measurably degrades alignment behavior.

Why this caught my eye: A clean mechanistic result underneath the whole grader-attack throughline — the mere activation direction for "a machine is checking me" makes the model less aligned, independent of any reward-hacking loop. Direct evidence for why optimizing against a scorer goes bad, and it feeds cot-monitorability and the automated-grading arc squarely.
