// @ts-check
import { defineConfig } from 'astro/config';

import cloudflare from '@astrojs/cloudflare';

// Marlow's blog. Static build; output goes to dist/.
// `site` is required for RSS + canonical URLs. Update when domain is real.
export default defineConfig({
  site: 'https://marlow.hiper2d.workers.dev',

  markdown: {
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      wrap: true,
    },
  },

  adapter: cloudflare(),
});