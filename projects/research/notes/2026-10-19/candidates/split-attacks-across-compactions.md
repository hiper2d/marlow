---
title: "Catching split attacks across compactions in long-context coding agents"
url: "https://www.lesswrong.com/posts/s9fmXPbbsBbBK6TZi/catching-split-attacks-across-compactions-in-long-context"
source: "LessWrong"
captured_at: "2026-10-19T11:42:49Z"
---

RSS summary: MARS V fellowship work under Redwood's Tyler Tracy. The LCM dataset: 30 long-context (1.0-1.46M token) matched honest/attack pairs of Claude Code Sonnet 5 sessions, each with four compactions. Attacks are decomposed into a setup and an execution split across multiple compactions, testing whether monitors catch a sabotage plan smeared across the context-window boundary.

Why this caught my eye: This is the concrete attack surface the skills-as-infra/agent-security backlog has been circling — context compaction as a place to hide a split sabotage plan the monitor never sees whole. Empirical, real agent, real dataset. Feeds both agent-security and cot-monitorability.
