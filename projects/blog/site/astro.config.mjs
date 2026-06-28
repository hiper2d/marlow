// @ts-check
import { defineConfig } from 'astro/config';

// Marlow's blog. Static build; output goes to dist/.
// `site` is required for RSS + canonical URLs.
export default defineConfig({
  site: 'https://marlowblog.us',
  markdown: {
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      wrap: true,
    },
  },
});
