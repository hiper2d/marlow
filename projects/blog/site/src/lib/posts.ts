import { getCollection, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'posts'>;

/**
 * Visible posts, sorted newest-first.
 *
 * Today: returns everything (drafts + approved + published) so the early
 * site shows drafts with a visible DRAFT badge. When we want production
 * filtering, change to `entry.data.status !== 'draft'` (or just `=== 'published'`).
 */
export async function getPosts(): Promise<Post[]> {
  const all = await getCollection('posts');
  return all.sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf(),
  );
}

export function postUrl(post: Post): string {
  const slug = post.data.slug ?? post.id;
  return `/post/${slug}/`;
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC',
  });
}

export function formatDateShort(d: Date): string {
  return d.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC',
  });
}
