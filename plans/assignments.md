# Research assignments — design

## Problem

Marlow's organic pipeline (`feed_scan` → candidate notes → threads → `draft_review`) works when stories ripen across multiple sources over weeks. It doesn't cover the case where Alex or Simona reads something interesting *outside* Marlow's feeds and wants Marlow to take it on as a deep-research piece.

This adds an external **assignment** path. Assignments seed the research pipeline from outside, with curated framing and source material. Marlow does her own deep research around the seeds and either drafts a piece or declines and explains why.

## Lifecycle

```
projects/research/assignments/
├── pending/        ← brief written, waiting for Marlow
├── researching/    ← Marlow has started but hasn't finished
└── done/           ← research complete (drafted, abandoned, or shipped)
```

States:
- **pending** — assignment file exists, Marlow hasn't touched it
- **researching** — Marlow has begun (typically only one at a time, but the folder allows more)
- **done** — research finished. The assignment file lives here with a final `outcome:` field added to frontmatter (`drafted` | `abandoned`)

## Assignment file format

One markdown file per assignment. Slug-named. Lives at `assignments/pending/<slug>.md` when first created.

```yaml
---
slug: anthropic-evil-ai-personas
assigned_by: simona              # simona | alex
assigned_at: 2026-05-14
priority: normal                 # normal | high
angle: |
  Paraphrased framing of the question Marlow should explore.
  Multi-line YAML block scalar. This is what Marlow leans on
  when deciding what to say.
deadline: null                   # ISO date or null
outcome: null                    # set on done: drafted | abandoned
---

## Why this

Free-form prose context. What's the conversation behind this? What's
interesting about it? Not a Discord paste — see "Conversation hygiene"
below.

## Seed materials

- https://primary-source.example.com/article
- https://secondary-source.example.com/paper
- (other links worth pulling, primary sources preferred)

## Things to look for

- Specific angles, tensions, or counterarguments Marlow should test
- What the primary sources got right or missed
- Optional — empty list is fine if the angle field is enough
```

### Conversation hygiene

When an assignment derives from a private conversation (a Discord thread, an Ars comment, a chat between Alex and Simona), **do not paste those conversations verbatim into the assignment file**. We don't have permission, and the blog isn't a chat-dump.

Acceptable framings for the "Why this" section:
- A paraphrased intro: *"A recurring claim in the AI-discourse space is that…"*
- A synthetic dialog construct: *"Imagine two researchers debating whether…"* — make it clear it's a construct, not a real quote
- A direct framing of the problem as Marlow herself might pose it

If you need to reference a specific public artifact (an Anthropic blog post, an Ars Technica article), link it as a seed source — that's public discourse and citation is fine.

## Marlow's workflow per assignment

One tick processes one assignment from start to finish. The 5-minute wall-clock budget covers: reading the brief, fetching 5–10 URLs, writing the research synthesis into the assignment file, optionally drafting if high-priority, and a final notify.

Stages (logical, all within one tick):

1. **Read brief** — `research_assignment.py read --slug <slug>` returns the assignment frontmatter + body
2. **Collect** — fetch every URL in *Seed materials* via `fetch_article.py fetch`. Add 1–2 rounds of targeted web search for adjacent prior work or counterarguments. Pull primary sources where the seed is secondary (e.g. seed is Ars piece → fetch the underlying paper too).
3. **Synthesize research into the assignment file** — do **not** create a file in `projects/research/threads/`. An assignment is scaffolding for one commissioned piece, not a durable arc; it stays inside `assignments/`. Append the research synthesis to the assignment file's own body (it's in `researching/` at this point), under three headings:

   - **Sources** — one short paragraph per fetched piece, what it actually says (your read, not a press-release summary). Cite each `[name](url)`.
   - **Cross-source observations** — where do sources agree, disagree, miss each other? What does the primary source say the secondary missed?
   - **Angle memo** — Marlow's working position. 3–6 sentences. Where does she land, what's the contrarian observation, what does she want to say? This is the seed of the eventual article.

   The brief and its research now travel together; `mark-done` (step 5) carries the whole thing into `done/`. The durable thread is born later, at *drafting* time, under a clean topic slug — see `memory/thread-structure.md` → "Assignment briefs are not threads" and "First article on a brand-new arc." The `assigned-<slug>` convention names the **assignment file only**; it must never appear as a file in `threads/`.
4. **Decide outcome**:
   - **draft-eligible** — angle memo is real, sources support it, she has something to say. Continue to (5).
   - **abandoned** — after research, Marlow has nothing useful to add. Write a one-paragraph explanation into the assignment frontmatter (`abandon_reason`), set `outcome: abandoned`, move to `done/`, notify Alex with reason. Don't fake interest.
5. **Move to done** — `research_assignment.py mark-done --slug <slug>` moves the assignment file from `researching/` to `done/` and writes the outcome.
6. **High-priority extension** — if `priority: high`, draft immediately in the same tick. Marlow drafts straight from the brief + research synthesis she just wrote (no thread file exists yet), composing to `projects/blog/drafts/<YYYY-MM-DD>-<slug>.md`. The draft's `mentions:` names a **clean topic slug**, never `assigned-<slug>`; she then opens that durable thread via "First article on a brand-new arc" (`memory/thread-structure.md`), or — if the topic already has a durable thread — mentions that one and rewrites it to absorb the post. Notifies urgent. Skips the `draft_review` cadence entirely.
   - For `priority: normal`, Marlow does *not* draft in this tick. The next `draft_review` cycle will pick up the thread.

## Decline path

Marlow is explicitly allowed to abandon an assignment after research. Forcing a take she doesn't have produces worse content than not posting. The bar:
- She read everything and still has nothing distinct to say
- The angle Alex/Simona proposed doesn't survive contact with the actual sources
- The sources are too thin to make a piece work

When she abandons, she writes the *why* into the assignment file's `abandon_reason` field and notifies Alex (digest, not urgent). Alex can re-assign with a different angle, or kill it.

## Scheduling

`projects/research/tasks/assignment_research.yaml` — fires **every 4 hours** (`0 */4 * * *`). Each fire enqueues one static subtask: `process_one_assignment`. That subtask, when picked up by the next available tick, runs the workflow above for the highest-priority oldest pending assignment.

Backlog drain: 6 firings per day → up to 6 assignments processed per day. With realistic assignment volume (a few per week), the queue never piles up.

Empty-queue behavior: if there are no pending assignments, the handler returns `done` immediately with result `"no pending assignments"`. The subtask completes, the next 4-hour fire is harmless.

The scheduler's existing dedup logic (handler + url + prefix) means if a previous `process_one_assignment` is still pending or in-progress, a new one won't pile up. Self-throttling.

### Existing `draft_review` cadence change

Bumped from weekly Sundays to **every 3 days** (`0 14 */3 * *`). Same task, same handler, same ripeness bar. Just more frequent looks at organic threads. High-priority assignments bypass it via the in-tick draft path described above.

## Handler — `research_assignment.py`

CLI matches Marlow's existing handler convention:

```
research_assignment.py list-pending
  → JSON list of slugs in assignments/pending/, with priority + assigned_at

research_assignment.py read --slug <slug>
  → JSON: assignment frontmatter + body + path (works in any state)

research_assignment.py move-to-researching --slug <slug>
  → Moves the file pending/ → researching/. Returns new path.

research_assignment.py mark-done --slug <slug> --outcome drafted
research_assignment.py mark-done --slug <slug> --outcome abandoned --reason "..."
  → Moves to done/, writes outcome (and abandon_reason if set) into frontmatter.

research_assignment.py list-all
  → All assignments across states. Useful for status displays.
```

The handler is *deterministic file-shuffling and YAML reading*, matching `draft_article.py`'s philosophy. Marlow does the editorial work in-session, not inside the handler.

## Integration with existing pipeline

Assignments don't introduce a parallel pipeline — they feed into the existing thread/draft system:

- Assignments do **not** create thread files. The brief + research synthesis live in `assignments/`; the durable thread is opened at drafting time under a clean topic slug (graduation — see `memory/thread-structure.md`). `threads/` holds durable arcs only, never `assigned-<slug>` files
- The existing `draft_article.py` handler works against durable threads unchanged — once an assignment graduates, its thread is an ordinary topic thread
- The existing `revise_draft.py` review-loop also works unchanged — Simona reviews, Marlow revises, drafts ship or die at the version cap
- The publish gate (Alex flips status to `approved`) is identical for assigned and organic drafts

The only fork in the road is the **immediate-draft** path for high-priority assignments, which bypasses `draft_review` but uses the same drafting logic.

## CLAUDE.md additions

Add a new section to Marlow's CLAUDE.md under "How a tick works" documenting:
- The handler name and CLI surface
- The workflow stages
- The decline path
- The high-priority same-tick draft rule
- The conversation-hygiene rule (no verbatim quotes from private chats)

## Open questions deferred

- **Multi-assignment-in-tick batching**: should the handler optionally process multiple short assignments in one tick when wall-clock allows? Possibly later — for now, one per tick.
- **decompose_handler in scheduler.py**: would let us drop the static-subtask shape and dynamically enqueue per pending assignment. Not blocking; the every-4-hour static-subtask approach works.
- **CLI sugar**: `marlow assign <slug>` to stamp out a new template assignment from a CLI prompt. Nice-to-have, not v1.
