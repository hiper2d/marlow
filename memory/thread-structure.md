# Thread structure

Marlow-owned. Updated by `process_editorial_feedback` when reviews flag thread-page quality. Read at the start of every drafting tick. Three cases to keep separate:

- When you write a new article that mentions an **existing** thread, you rewrite that thread's file to reflect the current state of the arc.
- When you write the **first** article on a brand-new arc — a `mentions:` slug with no thread file on disk — the same drafting tick must also open that thread file. See "First article on a brand-new arc" below.
- When an organic arc has **ripened in `working.md` but has no thread file yet**, open the thread file *before* drafting, at the top of the drafting tick — otherwise `list-threads` can't see it and it never reaches the draft. See "Proactive: ripe organic arc with no thread file" below.

A thread file is **the current synthesis of the arc**, not an append-only log. Every time a new article on the thread publishes, the thread file gets rewritten so it reads as a coherent overview of where the story stands now. The git history preserves prior versions for anyone who wants to trace the development; the live file represents the current view.

## Why rewrite, not append

A thread that runs 6 months and produces 4-5 posts would, under append-only, become a messy chronological pile-up of anchors, abandoned takes, superseded angles, and stale "draft pending" markers. The thread page would read as Marlow's open notebook — authentic but not useful to a reader who actually wants to follow the arc.

Rewriting on each publish costs an extra editorial pass per article but produces a thread page that reads like a brief on the state of the arc. The post auto-list below the body still shows every article, so provenance isn't lost.

## Standard shape

```
---
slug: <thread-slug>
title: "<short title — what this arc is about>"
status: active           # active | dormant | archived
opened: <YYYY-MM-DD>     # date the thread was first written
last_synthesized: <YYYY-MM-DD>   # date of the most recent rewrite
posts: <count>           # number of published posts on this thread
---

## What this thread tracks

<2-4 sentences naming the arc. What's the question or pattern this thread exists to follow? Make it nameable in one sentence at the top; expand to context in the next 1-3 sentences. This section gets refined as the arc develops — early threads will have a tentative description; mature threads will have one that reflects what the arc actually turned out to be about.>

## Where the arc stands now

<3-6 sentences synthesizing the *current* state. What's the through-line across the posts so far? What pattern is emerging? What did the latest post add? This is the section that changes most on each rewrite — it captures the synthesis from the latest article and forward-looks. Don't recap each post in turn (the post list is below); name the arc-level point.>

## Sources and anchors

<Bulleted list of the load-bearing sources for this thread. Each anchor: source name + date + one-line summary. Add new anchors as they land; retire ones that turned out not to matter. Aim for the 5-10 most load-bearing, not exhaustive.>

- [Source name](url) — <YYYY-MM-DD> — one-line take
- ...

## Open questions / what to watch

<3-6 bullets. What hasn't this thread resolved yet? What signals would update the picture? What's the next move? This is the forward-look, distinct from the "where it stands now" section which is retrospective.>

- ...

## Notes

<Optional. Any meta-observations about the arc itself — corrections you'd make to earlier takes, recurring themes Marlow has noticed, framework questions raised by the thread. Keep terse.>
```

## First article on a brand-new arc — open the thread file

When the drafting tick produces an article whose `mentions:` list includes a slug with **no existing thread file on disk**, the same tick must also open that thread file. The trigger is structural, not optional — if the article publishes against a missing thread file, the live site renders a 404 at `/thread/<slug>/`. The publish-side guard added in `handlers/self_review.py` (commit `cf3344d`, 2026-05-23) catches this at review time as a safety net, but the primary mechanism is the drafting tick. If the guard fires, the protocol already broke earlier — the thread file should have been opened during drafting, not patched in at review.

Two non-default points to get right:

1. **Slug-matching.** The thread file path is `projects/research/threads/<slug>.md` where `<slug>` is the exact string in the article's `mentions:` list. Do not prefix it with `assigned-` even if the originating assignment used that prefix — the article's `mentions:` slug is authoritative, and any mismatch leaves the 404 live.
2. **Synthesis seed is the article you just wrote.** No fresh research pass. You wrote the article; you know what it added. Pull anchors from the article's citations plus relevant entries in `working.md`. The thread file is the brief on the arc as it stands *after* the article published.

Frontmatter for a freshly-opened thread:

- `opened` — the article's publish date (or its current draft date if not yet published), not the date you opened the thread file.
- `last_synthesized` — same as `opened`.
- `posts: 1`.
- `status: active`.

Body follows the "Standard shape" above. The "Sources and anchors" section pulls from the article's citations plus relevant entries in working memory; pick the 5–10 most load-bearing, not exhaustive.

## Proactive: ripe organic arc with no thread file

The drafting tick discovers work by globbing `projects/research/threads/*.md`. Organic arcs accumulate as prose in `working.md` ("Active threads") long before they become files — and nothing else in the pipeline promotes them. So a ripe arc that only lives in `working.md` is invisible to `draft_article list-threads`, and `draft_review` comes up empty even when the material is there. This is the organic counterpart to the assignment path, where `research_assignment` explicitly composes `assigned-<slug>.md`. Organic arcs have no such step unless you do it here.

At the **top of the drafting tick**, before `list-threads`:

1. Read the "Active threads" section of `working.md`.
2. For each arc that meets the ripeness bar (3+ cross-source anchors over 1–3 weeks, a genuine through-line, something to *say*) and has **no** `projects/research/threads/<slug>.md` file on disk — open the thread file now.
3. Seed it from the `working.md` anchors plus the candidate/research notes that mention the arc (the same corpus `draft_article list-materials` would surface once the file exists). No fresh research pass; you're synthesizing what's already tracked.
4. Frontmatter and body follow the "Standard shape" above. `opened` and `last_synthesized` are today; `posts: 0` (nothing published yet — this is the pre-first-article state, unlike the brand-new-arc case which is opened *alongside* a first article and starts at `posts: 1`); `status: active`.

Then proceed to `list-threads` → ripeness judgement → draft as normal. The arc you just materialized is now visible and draftable in the same tick.

Don't over-promote: only arcs that genuinely clear the bar. A thin two-anchor cluster stays in `working.md` until it ripens. Opening a thread file is a commitment that the arc is real, not a staging area for maybes.

## When to rewrite

- **Every time a new article on an existing thread publishes.** During the drafting tick, after writing the article, rewrite the thread file to incorporate the new piece's contribution. Use the just-written article as input (you wrote it; you know what it added).
- **When a new high-signal anchor lands** even without a new article — research scans that surface a load-bearing source warrant updating the "Sources and anchors" section and possibly the "Where the arc stands now" section.
- **When editorial feedback flags drift** — same as the other behavioral files; `process_editorial_feedback` may update individual thread synthesis sections.

## When NOT to rewrite

- During a daily news scan that produces a candidate note. Candidate notes live in their own dated directories; the thread file only gets touched when something load-bearing lands.
- During the publish tick. The rewrite happens during the *drafting* tick, alongside writing the article. Publish just commits the work.
- During revision (`revise_draft`). The article is being refined; the thread synthesis should reflect the *final* article, but in practice the v1 → v2 changes are small enough that re-rewriting the thread is overkill. If v2 substantively changes the angle, do it; otherwise leave the thread file alone.

## Status field

- `active` — current arc, recent posts, likely to spawn more.
- `dormant` — thread has gone quiet but isn't closed. No posts in 8+ weeks. May reactivate if a new anchor lands.
- `archived` — thread is closed. The arc has resolved or moved on. Stops appearing in the "Open threads" grid on the homepage.

Marlow updates the status field herself during the rewrite if the situation has shifted (e.g., the third article on a thread is its concluding piece → `status: archived`). Editorial feedback can also direct status changes.

## Voice for the thread file

Same voice rules as the posts (see `voice-guidelines.md`). Editorial, dry, fact-first. Slightly more terse than a published article — a thread file is the *brief* on the arc, not the essay. Sentences over paragraphs. Specific named anchors over hand-waves.

The "Where the arc stands now" section is where voice shows most — it's a synthesis paragraph. Lean into the same plain, direct restatement that the voice rules call for in articles.
