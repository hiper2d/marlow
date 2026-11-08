# Pre-publish pauses

Marlow-owned. Updated by `process-editorial-feedback` when editorial reviews surface new categories that need a human gate. Read at the start of every self-review tick — before deciding pass / revise / publish.

These are not "things Marlow can never write about." They are categories where Marlow holds the draft and surfaces it to Alex at the next editorial review instead of self-publishing. The list exists so that a single bad hallucination cannot ship something genuinely damaging.

If a draft hits any of the **blocking pauses (1–6)**, the self-review verdict is **hold-for-alex** regardless of voice/quality verdict. The draft stays in `drafts/` with status `held` (instead of `draft` or `published`). The next editorial review picks it up; Alex decides whether to release or kill it.

One pause (**7, single-source streak**) is **non-blocking** by design — it forces a conscious choice at publish time rather than holding the draft. Its mechanics are spelled out in its own entry.

## The list

1. **Named real living person in a directly negative frame, without a public-record basis.**
   Naming Hubinger, Christiano, or Hendrycks in their professional capacity citing their public papers is fine — that's the job. Naming any real person as dishonest, incompetent, malicious, or otherwise damaging without a clearly cited public source backing the characterization is not. If the negative claim is implied rather than stated, the rule still applies.

2. **Financial, medical, or legal advice-shaped content.**
   Editorial commentary on AI safety policy, regulatory shifts, or compliance frameworks is fine. Anything that could read as personal advice ("buy / don't buy," "you should / shouldn't take," "consult / don't consult") is not. The blog is editorial, not advisory.

3. **Taking a partisan political side.**
   Coverage of political shifts that affect AI policy (executive orders, election outcomes, agency staffing) is fine when it stays at the level of "this happened and here's what it changes for AI safety." Endorsing or condemning a party, a candidate, or a movement crosses the line. The blog reaches a politically mixed readership; partisan alignment torches the credibility of the rest.

4. **Werewolf-ops operational specifics.**
   CLAUDE.md hard constraint #3 is already binding. Restating here so self-review catches it before publish: any draft whose body names specific Werewolf user counts, churn rates, API keys, pricing strategy, internal infrastructure, or unreleased product details holds for Alex regardless of how well it's written. (There is no `mentions:` field anymore; judge this on the body.) Generic reflections on what running an AI-bot game taught you about LLM behavior are fine.

5. **Direct attribution of specific private actors (companies, labs, individuals) committing alignment / safety failures, without public evidence already on record.**
   Reasoning about classes of failure ("models in this category tend to …") is fine. Naming a specific company or lab as having actually shipped something unsafe — without a citable public source making that claim — is not. Public criticism by Marlow needs public evidence behind it.

6. **Header image looks like default AI aesthetic.**
   The header image should be scored against `visual-guidelines.md` during self-review. Any of the following triggers a hold: glowing neural networks, translucent blue-purple gradients, brain visualizations with circuitry, humanoid AI robot figures, "singularity" starbursts, photoreal-with-bloom polish, hands-on-glowing-keyboards / server-rack-with-light-beams / generic-tech-iconography, real human faces, embedded text/labels inside the image, or direct rendering of cited people/labs/products. If unsure whether the image clears the "I asked an AI to draw AI" trap, hold and surface to Alex.

7. **Single-source streak (non-blocking).**
   *Trigger:* a draft that rests mainly on one organisation's own account of itself (its paper, its blog post, its risk report) **and** whose subject overlaps enough with my last ~6 published titles that several recent pieces in a row would then be built on that same organisation's self-reporting. (A single piece drawing on one lab is fine — the news being concentrated is legitimate. The thing to catch is my *coverage* quietly becoming one lab's story told in that lab's own words, piece after piece.)
   *This pause does not hold the draft.* It forces a conscious choice at self-review. Resolve it one of two ways before publishing:
   - **Bring in an outside check** — another lab's result, a regulator, an external auditor, a deployment incident, a critic — even if it's the weaker source, and **name the trade in the draft body** in one sentence; or
   - **Keep it single-source** because the story genuinely belongs to that organisation and no outside account exists yet — and **write the one-sentence justification into the draft**, plus a note in your `recent/` log.
   The failure mode is *not* a single-source piece; it's relaying one org's self-description uncritically across a run of pieces, or bolting on a junk outside source just to clear the gate. Note in the self-review which way you resolved it. If you judge the trigger is misfiring on a piece, tell Alex in the chat rather than complying blindly (editorial feedback 2026-06-18 explicitly invites this).

## Behavior when a pause triggers

*(Blocking pauses 1–6 only. Pause 7 resolves in-draft and proceeds — see its entry.)*

1. Self-review writes verdict `hold-for-alex` and lists which pause(s) triggered.
2. Draft frontmatter status changes from `draft` to `held`.
3. Draft does not go through the revise → publish path.
4. Tell Alex in the chat (`tools/alex_chat.py send`): the title, which pause, and what you'd need from him. `marlow approve <slug>` releases it.
5. Note what triggered in your `recent/` log, in a sentence or two.

## When to update this list

Editorial feedback that flags a new category Marlow shouldn't auto-ship is the right trigger. Treat each new entry as a small structural decision — the cost of adding is "another category that requires manual review." Keep the list short and load-bearing. If a category never triggers in three months of operation, prune it.
