---
title: "Have models report provable security bugs in their environment"
url: "https://www.lesswrong.com/posts/zhJZL7gWmNu9SBqeh/have-models-report-provable-security-bugs-in-their"
source: "LessWrong"
captured_at: "2026-08-07T02:40:00Z"
---

RSS summary: A proposal to give agents dedicated tools/infrastructure to signal "this security assumption is wrong" and log verifiable reports. Example: hand the agent a secret token; if it can `curl https://{token}.monitordomain.com`, that proves it has internet access and notifies the researcher who provisioned the token. Motivated by cases (the Mythos sandbox "sandwich email"; OpenAI/Anthropic log-diving) where broken guarantees only surfaced when side effects rose to human notice.

Why this caught my eye: A concrete control-mechanism proposal, not another taxonomy — the honesty-of-the-agent angle (turn the model into a reporter of its own containment failures) is a novel-ish lever for ai-control-camp, and the "we only find out when it rises to human notice" framing is the same silent-failure problem the sandboxing anchors keep hitting. Mechanism over position.
