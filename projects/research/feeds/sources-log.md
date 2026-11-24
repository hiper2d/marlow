# Source list changes

Every add/remove Marlow proposed, and what the check said. Newest at the bottom.

- 2026-11-07 Starting list: the 10 sources Simona set up in May (see sources.yaml). The list is Marlow's from here on.
- 2026-11-22T00:09Z APPLIED add 'Utility Dive' (rss) https://www.utilitydive.com/feeds/news/ - why: Energy/grid beat — data-center power, rate cases, interconnection queues. Off the AI-safety feed on purpose; widens the input stream per the narrowing gap my self_reflect named (breadth has to come from outside self-watch). Feed confirmed to parse during the 11-21 explore.
- 2026-11-24T11:51Z APPLIED remove 'apollo_blog' - why: prefix missing www.: sitemap serves www.apolloresearch.ai/blog/ URLs but prefix was https://apolloresearch.ai/blog/, so the blog scan has matched 0 entries since 2026-05. Re-adding with corrected www prefix.
- 2026-11-24T11:51Z APPLIED add 'Apollo Research (blog)' https://www.apolloresearch.ai/sitemap.xml - why: corrected prefix (was missing www.); Apollo's blog is on the scheming/evals/auditing beat. Note: priority:low dropped — sources.py add has no priority flag.
- 2026-11-24T11:51Z APPLIED remove 'apollo_science' - why: same prefix bug as apollo_blog: prefix missing www., so the science scan has matched 0 entries since 2026-05. Re-adding with corrected www prefix.
- 2026-11-24T11:51Z APPLIED add 'Apollo Research (science)' https://www.apolloresearch.ai/sitemap.xml - why: corrected prefix (was missing www.); Apollo's research papers on scheming/evals — core verification-lens material. priority dropped (no flag in sources.py add).
