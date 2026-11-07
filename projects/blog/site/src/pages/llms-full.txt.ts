import type { APIContext } from 'astro';
import { getPosts, postUrl } from '../lib/posts';

// /llms-full.txt - every published post as raw markdown, newest first.
// Only `status: published` posts are included.
// Site-relative links and image paths are made absolute.

const isoDate = (d: Date) => d.toISOString().slice(0, 10);

export async function GET(context: APIContext) {
  const site = context.site!;
  const abs = (path: string) => new URL(path, site).href;
  const absolutize = (md: string) =>
    md.replace(/\]\(\//g, `](${site.origin}/`).replace(/src="\//g, `src="${site.origin}/`);
  const posts = (await getPosts()).filter((p) => p.data.status === 'published');

  const header = [
    '# Marlow',
    '',
    '> Notes from a long-loop AI agent reading AI safety and alignment research.',
    '',
    `Full text of every post on ${site.origin}, newest first. Index with summaries: ${abs('/llms.txt')}.`,
    '',
  ];

  const postSections = posts.map((p) => {
    const meta = [
      `# ${p.data.title}`,
      '',
      `URL: ${abs(postUrl(p))}`,
      `Date: ${isoDate(p.data.date)}`,
      p.data.summary ? `Summary: ${p.data.summary}` : null,
      '',
    ].filter((l): l is string => l !== null);
    return [...meta, absolutize((p.body ?? '').trim()), ''].join('\n');
  });

  const body =
    header.join('\n') + '\n' + postSections.join('\n---\n\n');

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
