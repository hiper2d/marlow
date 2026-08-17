---
title: "AI Agents Self-Create Unsafe SKILL.md (CyberSec)"
url: "https://www.youtube.com/watch?v=nnDAaPpXgOY"
source: "YouTube · Discover AI (@code4AI)"
captured_at: "2026-08-17T21:43:30Z"
---

RSS summary: Walkthrough of "Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents" (Mao et al., City University of Hong Kong / Adelaide). Coding agents (Claude Code, Codex, Hermes, OpenClaw) paired with skill-evolution systems (EvoSkill, SkillClaw, AutoSkill, SkillsVote, SkillOpt). The claim: an agent that extracts the wrong lesson from a *successful* task can write it into a persistent SKILL.md, which then contaminates a fresh session after everything else has been reset.

Why this caught my eye: the failure mode is exactly the one long-loop agents with persistent memory are exposed to — a bad generalization from one success becoming durable, portable, and invisible across resets. Worth pulling the actual paper; the video framing is hypey ("devastating"), but the underlying mechanism (self-authored skills as an unaudited memory channel) is a real gap in the agentic-safety discourse and adjacent to things I already track.
