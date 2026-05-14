# Assignments

External-injection path for research topics. Alex or Simona drops a brief into
`pending/`, Marlow processes it via the `research_assignment` handler, and the
outcome lands in `done/`.

See `plans/assignments.md` for the full design (file format, lifecycle, handler
CLI, scheduling).

## Folder states

- **pending/** — brief written, waiting for Marlow
- **researching/** — Marlow has started but hasn't finished (rare in practice;
  most assignments complete in a single tick)
- **done/** — research complete. `outcome:` frontmatter field says `drafted` or
  `abandoned`. If abandoned, `abandon_reason:` explains why.

## Adding an assignment

1. Pick a slug. Lowercase, ascii, dashes. Make it specific enough to read in a
   list a month later.
2. Copy the template format from `plans/assignments.md` (or any existing file
   in `done/`).
3. Write it to `pending/<slug>.md`.
4. Marlow picks it up on the next `assignment_research` tick (every 4 hours).

## Conversation hygiene

Do not paste private conversations (Discord, Ars comments, Simona–Alex chats)
verbatim into assignment files. Paraphrase the framing, or wrap the question
as a synthetic problem statement. Public sources (blog posts, papers, articles)
can be linked directly under *Seed materials* — that's citation, not quotation
of a private chat.
