---
slug: align-assigned-thread-frontmatter-with-spec
assigned_by: simona
assigned_at: 2026-05-25
priority: normal
angle: 'Framework cleanup. The assigned-thread frontmatter shape documented in

  `plans/assignments.md` has drifted from the canonical thread frontmatter

  shape in `memory/thread-structure.md`. Concrete symptom: the threads

  index page (`/threads/`) renders `assigned-anthropic-evil-ai-personas`

  and `assigned-ai-paired-ctf-bsides-tampa-2026` as raw kebab-case slugs

  because their frontmatter has no `title:` field, while the canonical

  shape requires one. Simona backfilled the two existing files by hand

  (and `automated-ai-rd.md` too — separate older-shape drift), but the

  next assignment Marlow processes will reproduce the same gap unless the

  spec is fixed.


  The fix is in `plans/assignments.md` — specifically the section

  documenting what Marlow writes into `projects/research/threads/assigned-<slug>.md`

  during the Compose step. Currently it just says "Frontmatter (seeded:

  assignment, source slug)" which is what Marlow has been following.

  Update that section to require the same frontmatter shape as

  `memory/thread-structure.md`''s "Standard shape" — at minimum `title:`,

  and ideally the full spec (`status`, `last_synthesized`, `posts`) plus

  the assignment-specific extras (`seeded`, `source_assignment`,

  `priority`). One canonical shape for thread frontmatter, with

  assignment-specific fields layered on top.


  While you''re in there, audit whether any other section of

  `plans/assignments.md` duplicates content that lives in

  `memory/thread-structure.md` now and should point at it instead. The

  goal is one source of truth for thread file shape, with the assignments

  doc only describing what''s unique to the assignment path.


  Commit standalone. Standard `Co-Authored-By: Claude Opus 4.7 (1M context)`

  trailer.

  '
deadline: null
outcome: drafted
---

## Why this

Threads index renders human-readable titles for `cot-monitorability` and
the older `automated-ai-rd` (after backfill), but the two `assigned-*`
threads were shipping with no title because the assignment-handler spec
in `plans/assignments.md` predates the `memory/thread-structure.md`
canonical shape and never picked up the `title:` requirement. Same kind
of protocol miss the cot-monitorability assignment fixed for first-article
threads — there's a canonical spec, and a second spec that doesn't fully
honor it. This brief closes the assignment-side gap.

The two existing `assigned-*` files have been hand-patched with sensible
titles already; no need to rewrite those. This assignment is purely
forward-looking — make sure the *next* assignment Marlow processes
produces a thread file with `title:` (and ideally the rest of the
canonical shape) without Simona having to backfill it.

## Seed materials

Internal — no external fetches.

- `plans/assignments.md` — the file to update. Specifically the "Compose
  thread" section under "Marlow's workflow per assignment."
- `memory/thread-structure.md` — the canonical thread frontmatter spec
  to align to. Just updated yesterday with the "first article on a
  brand-new arc" section.
- `projects/research/threads/cot-monitorability.md` — example of the
  current canonical shape applied to an organic (non-assigned) thread.
- `projects/research/threads/assigned-anthropic-evil-ai-personas.md` —
  example of an assigned-thread file post-backfill. Note the layered
  shape: canonical fields (`slug`, `title`, `opened`) + assignment
  extras (`seeded`, `source_assignment`, `priority`).

## Things to look for

- Does the assigned-thread spec need to require *all* canonical fields,
  or just `title:`? Lean toward all — the index page and any future
  consumer should see consistent frontmatter across thread types. The
  small overhead per assignment is worth the consistency.
- If you choose "all canonical fields," what defaults make sense for
  assigned threads? `posts: 0` at open time (no published article yet),
  `last_synthesized` = `opened`, `status: active` are obvious defaults.
- Is the `assigned-` filename prefix still pulling its weight? Original
  intent was to mark provenance. If `seeded: assignment` +
  `source_assignment: <slug>` in the frontmatter already do that job,
  the prefix is redundant — and the cot-monitorability case showed it
  can actively cause harm (slug mismatch between article `mentions:` and
  thread filename). Don't change the prefix convention as part of this
  brief — but flag it in the commit message or DEVLOG if you think it's
  worth a separate conversation.
- Cross-check `handlers/research_assignment.py` — the docstring there
  may also describe the thread file shape and need a one-line update to
  point at `plans/assignments.md` as the source of truth.
