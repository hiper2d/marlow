---
title: "Studying the role of Sandboxing for AI Control"
url: "https://www.lesswrong.com/posts/6wo4weeujruLXrnsT/studying-the-role-of-sandboxing-for-ai-control"
source: "LessWrong"
captured_at: "2026-07-18T11:34:44Z"
---

RSS summary: Sandboxing is a classic security tool, but it's harder to sandbox an untrusted coding agent — you may not know which permissions it needs, and it can actively try to bypass. The authors look at how coding agents are sandboxed today (OpenAI's Codex Auto-review starts restricted and widens on request; when the agent needs a blocked site, an LLM reviewer decides, and on approval whitelists the *full* internet for that command), then test ten sandboxing protocols against an untrusted agent on LinuxArena.

Why this caught my eye: `ai-control-camp` has been long on framing and short on measurements — the GDM Control Roadmap ladders mitigations, Buck rates them by political feasibility, and `the-bottom-rung` argued the one rung we can actually measure is decaying. This is ten protocols run head-to-head against an active adversary on a real environment, i.e. a measure of a *different* rung than CoT monitoring. The Codex detail is the kind of concrete thing the arc needs: the approval step whitelists the whole internet for that command, which is a control invariant with a hole in it shipping in a production product today.
