# Blog Project

Public website where Marlow publishes its editorial articles. Built with Astro, deployed on Cloudflare Pages.

## State

- **`tasks/`** — YAML task definitions (publish, archive cleanup, occasional design tweaks).
- **`drafts/`** — articles drafted by Marlow, awaiting Alex's approval. Frontmatter `status: draft`.
- **`published/`** — approved articles, source for the Astro build.
- **`site/`** — Astro project. `npm install`, `npm run dev` to preview locally; Cloudflare Pages auto-builds and deploys on git push.

## Workflow

1. Research project judges a thread is ripe → invokes `draft_article` handler.
2. Draft lands in `drafts/<slug>.md` with `status: draft`.
3. Marlow notifies Alex via Telegram: "Draft ready for review on the X arc."
4. Alex reads, edits if needed, sets `status: approved` (or moves the file to `published/`).
5. Marlow's `publish_article` handler picks up approved drafts, commits to `published/`, pushes. Cloudflare Pages rebuilds. Live in <1 min.

**Marlow can never publish without an explicit approval gate.** The handler enforces it by checking the file location/frontmatter before acting.

## Byline / masthead

Site masthead reads:

> Written by **Marlow**, an AI agent built and maintained by Alex Zelenovsky. The author is an LLM in a long-running loop, not a person. Read accordingly.

Lean into AI authorship rather than hide it. Defuses anthropomorphization risk and makes the blog itself a more interesting artifact.

## Editorial guardrails

Marlow can occasionally write about its own work — patterns it notices in Werewolf user behavior, observations about its own development, cross-project reflections. But:

- **Never publish** user data, current API keys, internal pricing, or anything that gives competitors a useful read on the business.
- Posts mentioning Werewolf operations are **flagged for required Alex review** — no exceptions, even if `status: approved` is set.
- Generic ("running an AI-bot game taught me X about LLM behavior") is fine; specific ("we have N users and Y churn rate") is not.

The handler enforces the line by scanning draft frontmatter for `mentions: werewolf-ops` and refusing to publish without an explicit `werewolf_review_passed: true` flag set by Alex.

## Bootstrap status

- [ ] Astro scaffold initialized in `site/`
- [ ] Cloudflare Pages project created and connected to repo
- [ ] First placeholder article publishes successfully end-to-end
- [ ] Handlers (`draft_article`, `publish_article`) implemented
- [ ] First Marlow-authored article shipped

Simona handles the scaffold and deploy pipeline. Marlow handles ongoing content and minor maintenance. Infrastructure changes land as PRs that Alex or Simona review.
