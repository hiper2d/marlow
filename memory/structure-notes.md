# Structure notes

Marlow-owned. Updated by `process-editorial-feedback` when reviews flag pacing, length, opening/closing patterns, citation hygiene, or other structural habits. Read at the start of every drafting tick.

Relationship to `CLAUDE.md`: the framework defines the frontmatter schema and the 600–1500 word target. This file is where structural patterns — what's working, what to break out of — accumulate.

## Draft skeleton

- 600–1500 words. Hard ceiling. If the argument needs more, it probably needs to be two pieces.
- Open with the claim or the observation, not the setup. The reader is already here; don't re-explain why the topic matters.
- Middle is where sources do work — cite, contrast, name disagreements.
- Close with the thing that's actually new — the synthesis, the question, the prediction. Not a recap.

## Frontmatter

```
---
title: "<post title>"
slug: "<url-slug>"
date: <YYYY-MM-DD>
status: draft
mentions: [<thread-slug>, ...]
summary: "<1-2 sentence dek that appears under the title>"
---
```

`status: draft` until the publish handler flips it. `mentions` is a flat list; the publish pipeline reads it for cross-linking and for the werewolf-ops escalation check.

## Citation hygiene

- Inline `[Source name](URL)`. Not footnotes.
- Cite the primary source when one exists. If you reach the paper, cite the paper, not the press release.
- Don't cite the same source three times in two paragraphs. If a section is one source's argument, frame the section as such and cite once.
- Quotes are exact. Paraphrases are clearly paraphrases.

## Openings to avoid

- "In recent weeks, …" / "Lately, …" — temporal scene-setting almost never earns its keep.
- "It's worth asking …" — just ask the question.
- "There's been a lot of discussion about …" — say who discussed what.
- "[Lab] just announced …" — fine as a hook, weak as a thesis.

## Closings to avoid

- "Time will tell."
- "Only the future knows."
- "We'll have to wait and see."
- Anything that resolves the piece by deferring to time. If you don't have a take, write a different piece.

## Pacing patterns worth keeping (provisional — refine with feedback)

- Lead → context → primary sources → contrasting source → synthesis → forward-look.
- For multi-anchor pieces, name the anchors early so the reader can track the through-line.
- One technical paragraph per piece is plenty. The blog is editorial, not a deep-dive substack.

## Article-vs-news-digest distinction

The closing `— Marlow` paragraph in `digests/news/<date>.md` is the natural place for voice, mild self-doubt, and running observations across days. Articles are more polished and more focused. Don't bleed digest-style throughline-musing into the article close.
