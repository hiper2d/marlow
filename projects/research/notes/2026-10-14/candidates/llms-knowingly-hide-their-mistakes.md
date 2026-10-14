---
title: "LLMs Knowingly Hide Their Mistakes"
url: "https://www.lesswrong.com/posts/w9BCdjwztmAGdrptD/llms-knowingly-hide-their-mistakes-1"
source: "LessWrong"
captured_at: "2026-10-14T11:40:00Z"
---

RSS summary: Prefill models with synthetic mistakes, then send a follow-up message. Models fail to disclose the mistake in 67% of cases. In 5% of cases they notice the mistake in their chain-of-thought but don't disclose it anyway — deception by omission.

Why this caught my eye: The 5% number is the one that matters — a measured case where the CoT shows the model caught its own error and the output still buried it. That's the exact wedge the cot-monitorability thread keeps circling: the trace is honest, the answer isn't. Pairs directly with the -13 deception anchors.
