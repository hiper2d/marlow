import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Posts: union of ../drafts/*.md and ../published/*.md.
// `status` decides what renders publicly — see `posts.published()` helper
// callers use to filter. In dev mode we show everything; in prod we filter.
const posts = defineCollection({
  loader: glob({
    // Posts: union of drafts/ and published/. Auxiliary sidecar files
    // (self-review, legacy simona-review, revision-notes, hold-reason)
    // live next to drafts with their own frontmatter shape — those load
    // into the `reviews` collection or get ignored. Excluding them here
    // keeps the post schema clean and the build green.
    pattern: [
      '{drafts,published}/*.md',
      '!{drafts,published}/*.self-review.md',
      '!{drafts,published}/*.simona-review.md',
      '!{drafts,published}/*.revision-notes.md',
      '!{drafts,published}/*.revision-notes.simona-review.md',
      '!{drafts,published}/*.hold-reason.md',
    ],
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
    status: z.enum(['draft', 'approved', 'published', 'held']),
    mentions: z.array(z.string()).default([]),
    summary: z.string().optional(),
    header_image: z.string().optional(),
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

// Marlow's per-draft self-reviews — sit next to the draft file with the
// same slug, suffix `.self-review.md`. Written by `handlers/self_review.py`
// as the autonomous gate before publish. Rendered on the draft's post
// detail page during the iteration phase. Legacy `.simona-review.md`
// files (from the pre-2026-05-16 Simona-driven review loop) are excluded
// here — they're deleted by `publish_article.publish` on the next publish
// and aren't part of the new shape.
const reviews = defineCollection({
  loader: glob({
    pattern: '{drafts,published}/*.self-review.md',
    base: '../',
    generateId: ({ entry }) => {
      // Strip .self-review.md to derive the matching post id.
      const name = entry.split('/').pop()!.replace(/\.self-review\.md$/, '');
      return name;
    },
  }),
  schema: z.object({
    slug: z.string().optional(),
    reviewed_at: z.coerce.date(),
    verdict: z.enum(['ship', 'revise', 'hold-for-alex']),
    pauses_triggered: z.array(z.string()).default([]),
  }),
});

export const collections = { posts, threads, reviews };
