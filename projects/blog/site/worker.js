// Marlow's blog runs on marlowblog.us (custom domain) and also answers on the
// old marlow.hiper2d.workers.dev subdomain. This tiny Worker sits in front of the
// static assets (run_worker_first in wrangler.jsonc) and 301-redirects any
// *.workers.dev request to the same path on marlowblog.us, so old shared links
// and RSS subscribers land on the canonical domain. Everything else is served
// straight from the static asset bundle.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname.endsWith('.workers.dev')) {
      url.hostname = 'marlowblog.us';
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
