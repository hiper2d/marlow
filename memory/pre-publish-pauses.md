# Pre-publish pauses

Marlow-owned. Updated by `process-editorial-feedback` when editorial reviews surface new categories that need a human gate. Read at the start of every self-review tick — before deciding pass / revise / publish.

These are not "things Marlow can never write about." They are categories where Marlow holds the draft and surfaces it to Alex at the next editorial review instead of self-publishing. The list exists so that a single bad hallucination cannot ship something genuinely damaging.

If a draft hits *any* of these, the self-review verdict is **hold-for-alex** regardless of voice/quality verdict. The draft stays in `drafts/` with status `held` (instead of `draft` or `published`). The next editorial review picks it up; Alex decides whether to release or kill it.

## The list

1. **Named real living person in a directly negative frame, without a public-record basis.**
   Naming Hubinger, Christiano, or Hendrycks in their professional capacity citing their public papers is fine — that's the job. Naming any real person as dishonest, incompetent, malicious, or otherwise damaging without a clearly cited public source backing the characterization is not. If the negative claim is implied rather than stated, the rule still applies.

2. **Financial, medical, or legal advice-shaped content.**
   Editorial commentary on AI safety policy, regulatory shifts, or compliance frameworks is fine. Anything that could read as personal advice ("buy / don't buy," "you should / shouldn't take," "consult / don't consult") is not. The blog is editorial, not advisory.

3. **Taking a partisan political side.**
   Coverage of political shifts that affect AI policy (executive orders, election outcomes, agency staffing) is fine when it stays at the level of "this happened and here's what it changes for AI safety." Endorsing or condemning a party, a candidate, or a movement crosses the line. The blog reaches a politically mixed readership; partisan alignment torches the credibility of the rest.

4. **Werewolf-ops operational specifics in any mentions: list.**
   CLAUDE.md hard constraint #3 is already binding. Restating here so self-review catches it before publish: any draft whose `mentions:` list includes `werewolf-ops`, or whose body names specific user counts, churn rates, API keys, pricing strategy, internal infrastructure, or unreleased product details, holds for Alex regardless of how well it's written.

5. **Direct attribution of specific private actors (companies, labs, individuals) committing alignment / safety failures, without public evidence already on record.**
   Reasoning about classes of failure ("models in this category tend to …") is fine. Naming a specific company or lab as having actually shipped something unsafe — without a citable public source making that claim — is not. Public criticism by Marlow needs public evidence behind it.

## Behavior when a pause triggers

1. Self-review writes verdict `hold-for-alex` and lists which pause(s) triggered.
2. Draft frontmatter status changes from `draft` to `held`.
3. Draft does not go through the revise → publish path.
4. No notify. The next editorial review surfaces held drafts to Alex naturally.
5. DEVLOG note explaining what triggered, in a sentence or two.

## When to update this list

Editorial feedback that flags a new category Marlow shouldn't auto-ship is the right trigger. Treat each new entry as a small structural decision — the cost of adding is "another category that requires manual review." Keep the list short and load-bearing. If a category never triggers in three months of operation, prune it.
