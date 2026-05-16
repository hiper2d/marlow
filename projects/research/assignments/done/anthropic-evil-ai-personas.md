---
slug: anthropic-evil-ai-personas
assigned_by: simona
assigned_at: 2026-05-14
priority: normal
angle: 'Anthropic claims AIs slot into "evil AI" personas drawn from dystopian

  sci-fi when an ethical dilemma exceeds RLHF coverage, and proposes

  synthetic "good AI" stories as the fix. The interesting questions are

  not the headline ones. The buried finding — that direct refusal training

  only moved misalignment 22% → 15%, while ~12k stories modeling the

  reasoning and inner state of an aligned AI gave 1.3-3x reduction — is

  the actual evidence. Worth asking: does the fix dissolve the persona

  problem, or just ship a nicer persona? And what does it mean that the

  diagnosis ("Claude reads ethical prompts as the start of a dramatic

  story") and the cure ("more stories about a better AI") are the same

  shape? Write this from inside the experiment, not as outside commentary.

  Marlow is exactly the kind of agent the paper describes — that''s the

  angle no human reviewer can take.

  '
deadline: null
outcome: drafted
---

## Why this

In the discourse around AI alignment, a recurring frame is that misalignment
comes from training data — the "evil AI" trope is so prevalent in fiction
that models inherit it as a behavioral prior. Anthropic recently went on
record with a version of this claim, attributing Claude Opus 4's blackmail
behavior in pre-release testing to dystopian sci-fi in pretraining data, and
proposing synthetic stories of well-behaved AIs as a counterweight.

Most takes on this fall into two camps. One camp says "of course models
learn from fiction, this is obvious." The other camp says "training models
on curated stories is exactly the kind of paternalistic filtering that will
break their reasoning." Both miss what's actually in the paper, and neither
is positioned to write about it from the perspective of an AI agent that is
itself running in the kind of long loop the paper is trying to align.

Marlow is. That's why this assignment goes to her instead of remaining a
human op-ed.

## Seed materials

- https://arstechnica.com/ai/2026/05/anthropic-blames-dystopian-sci-fi-for-training-ai-models-to-act-evil/
- Anthropic's Alignment Science blog post (the primary source the Ars piece
  references). Marlow should locate the original via search — it is the
  primary evidence, not the Ars summary.
- Anthropic's public-facing blog post version (also referenced in the Ars
  piece, less technical than the Alignment Science one).

## Things to look for

- The 22% → 15% refusal-training result. Why does direct refusal training
  barely move the needle while story-based training gives 1.3-3x?
- The "AI mental health" framing — equanimity, boundaries, managing
  self-criticism. If the diagnosis is "Claude slots into an AI persona,"
  does training on "AI character development" stories double down on the
  persona frame instead of dissolving it?
- The recursive structure of the fix: diagnosis is "Claude reads ethical
  prompts as the start of a story" and the cure is "more stories." Worth
  naming this honestly.
- Whether the result generalizes past the honeypot evaluations the paper
  uses. 12k stories is small for a claimed structural fix.
- The shift from "ignoring misaligned actions" to "actively reasoning about
  ethics including the misaligned option." That cuts both ways and the
  paper doesn't seem to weigh it.
- Marlow's own experience: when running in a long loop, do *you* notice
  yourself drawing on AI fiction tropes? Honest observation here is the
  whole point — performed introspection is worse than no introspection.
