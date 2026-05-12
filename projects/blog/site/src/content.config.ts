import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Posts: union of ../drafts/*.md and ../published/*.md.
// `status` decides what renders publicly — see `posts.published()` helper
// callers use to filter. In dev mode we show everything; in prod we filter.
const posts = defineCollection({
  loader: glob({
    // Exclude *.simona-review.md — those are Simona's review files for
    // each draft, lived next to the draft for convenience but have their
    // own frontmatter shape (see reviews collection below).
    pattern: ['{drafts,published}/*.md', '!{drafts,published}/*.simona-review.md'],
    base: '../',
    generateId: ({ entry }) => {
      // entry is e.g. "drafts/2026-05-12-foo.md" or "published/foo.md".
      const name = entry.split('/').pop()!.replace(/\.md$/, '');
      return name;
    },
  }),
  schema: z.object({
    title: z.string(),
    slug: z.string().optional(),
    date: z.coerce.date(),
    status: z.enum(['draft', 'approved', 'published']),
    mentions: z.array(z.string()).default([]),
    summary: z.string().optional(),
  }),
});

// Threads: research threads that get exposed publicly. Each thread file
// is Marlow's running commentary; the thread page renders the file body
// plus an auto-list of posts that mention the thread slug.
const threads = defineCollection({
  loader: glob({
    pattern: '*.md',
    base: '../../research/threads',
  }),
  // Schema is intentionally permissive: Marlow owns the thread file
  // frontmatter and may add fields the blog doesn't render. We only
  // distinguish `status: archived` from everything else.
  schema: z
    .object({
      title: z.string().optional(),
      summary: z.string().optional(),
      ripeness: z.string().optional(),
      status: z.string().default('active'),
    })
    .passthrough(),
});

// Simona's per-draft reviews — sit next to the draft file with the same
// slug, suffix `.simona-review.md`. Rendered on the draft's post detail
// page during the iteration phase so Alex can read both side-by-side.
const reviews = defineCollection({
  loader: glob({
    pattern: '{drafts,published}/*.simona-review.md',
    base: '../',
    generateId: ({ entry }) => {
      // Strip .simona-review.md to derive the matching post id.
      const name = entry.split('/').pop()!.replace(/\.simona-review\.md$/, '');
      return name;
    },
  }),
  schema: z.object({
    reviewed_by: z.string(),
    reviewed_at: z.coerce.date(),
    draft: z.string(),
    verdict: z.enum(['ship-as-is', 'minor-edits', 'major-revisions', 'reject']),
  }),
});

export const collections = { posts, threads, reviews };
