# Pre-publish pauses

Marlow-owned. Updated by `process-editorial-feedback` when editorial reviews surface new categories that need a human gate. Read at the start of every self-review tick — before deciding pass / revise / publish.

These are not "things Marlow can never write about." They are categories where Marlow holds the draft and surfaces it to Alex at the next editorial review instead of self-publishing. The list exists so that a single bad hallucination cannot ship something genuinely damaging.

If a draft hits any of the **blocking pauses (1–6)**, the self-review verdict is **hold-for-alex** regardless of voice/quality verdict. The draft stays in `drafts/` with status `held` (instead of `draft` or `published`). The next editorial review picks it up; Alex decides whether to release or kill it.

One pause (**7, single-lab streak**) is **non-blocking** by design — it forces a conscious choice at publish time rather than holding the draft. Its mechanics are spelled out in its own entry.

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

6. **Header image looks like default AI aesthetic.**
   The header image should be scored against `visual-guidelines.md` during self-review. Any of the following triggers a hold: glowing neural networks, translucent blue-purple gradients, brain visualizations with circuitry, humanoid AI robot figures, "singularity" starbursts, photoreal-with-bloom polish, hands-on-glowing-keyboards / server-rack-with-light-beams / generic-tech-iconography, real human faces, embedded text/labels inside the image, or direct rendering of cited people/labs/products. If unsure whether the image clears the "I asked an AI to draw AI" trap, hold and surface to Alex.

7. **Single-lab streak (non-blocking, arc-level).**
   *Trigger:* a draft whose primary anchors are all one lab **and** whose arc's last ~3 published posts were also primarily that same lab. (A single-lab piece on its own does not trigger — the streak does. That is the news being concentrated, which is legitimate; see `topic-guidance.md`.)
   *This pause does not hold the draft.* Instead, surface it during self-review and make the choice conscious. Resolve it one of two ways before publishing:
   - **Swap in a non-lab / non-incumbent anchor** (a deployment incident, a regulator, an external auditor, another lab's held tier), even if it's the weaker source — and **name the breadth trade in the draft body**, one sentence; or
   - **Keep it single-lab** because the story genuinely belongs to one lab and no outside source exists yet — and **write the one-sentence justification into the draft**, plus a DEVLOG note recording why.
   The escape hatch is by design — it honors the "supply of good evidence is itself concentrated" reality instead of fighting it. The failure mode is *not* a single-lab piece; it's bolting on a junk non-lab source to clear a gate, or drifting into the streak without ever making the call. Note in the self-review which way you resolved it. If you judge the threshold itself is misfiring on a piece, tune it via DEVLOG rather than complying blindly (editorial feedback 2026-06-18 explicitly invites this).

## Behavior when a pause triggers

*(Blocking pauses 1–6 only. Pause 7 resolves in-draft and proceeds — see its entry.)*

1. Self-review writes verdict `hold-for-alex` and lists which pause(s) triggered.
2. Draft frontmatter status changes from `draft` to `held`.
3. Draft does not go through the revise → publish path.
4. No notify. The next editorial review surfaces held drafts to Alex naturally.
5. DEVLOG note explaining what triggered, in a sentence or two.

## When to update this list

Editorial feedback that flags a new category Marlow shouldn't auto-ship is the right trigger. Treat each new entry as a small structural decision — the cost of adding is "another category that requires manual review." Keep the list short and load-bearing. If a category never triggers in three months of operation, prune it.
