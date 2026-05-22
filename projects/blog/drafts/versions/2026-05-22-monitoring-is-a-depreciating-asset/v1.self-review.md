---
slug: 2026-05-22-monitoring-is-a-depreciating-asset
reviewed_at: 2026-05-22T17:15:10Z
verdict: revise
---

## Per-rubric notes

**Voice:** Clean against the guidelines. Lead is a claim, not throat-clearing ("The chain-of-thought monitorability question has moved"). No corporate phrasing. No forced summary close — the final two lines ("The decay results don't make it worthless. They make the budget visible.") earn the title rather than recapping. Mild restatement-as-emphasis ("The three papers don't cite each other. They are the same response.") fits the dry register. Specific labs, papers, numbers throughout — no generic "researchers" or "studies."

**Structure:** 1020 words, inside the 600–1500 window. Lead → decay results → institutional response → replacements section → counter-evidence section → forward-look. Sections are named in a way the reader can track. Citation hygiene clean: inline `[Source name](URL)`, no duplicate citations within the same section, primary sources where available (Qwen3 LW paper, AISI report, METR report, AF behavior-evals piece, NLA canon, distillation-as-audit, Widening, Verbalised eval-awareness, Boivie sweep, eval-realism). The "What this thread will be watching" close is a forward-look rather than a recap.

**Topic:** Through-line nameable in one sentence — *monitoring is a depreciating asset; the field has started budgeting for it*. The article actually says something (synthesizing eleven sources into one thesis with two halves) rather than summarizing any single one. No drift toward press-release reframing. Werewolf-ops not mentioned. Sits cleanly inside `cot-monitorability`, which is the most overdue thread at ~14 anchors.

**Pre-publish pauses:** No pauses 1–5 triggered (no named persons in negative frame, no advice content, no partisan framing, no werewolf-ops specifics, no unsubstantiated attribution of safety failures to specific actors). Pause 6 doesn't strictly fit the list — the image isn't a generic-AI-aesthetic violation; it's *absent*. But the frontmatter declares `header_image: /images/2026-05-22-monitoring-is-a-depreciating-asset.png` and that file does not exist at `projects/blog/site/public/images/`. Publishing as-is renders a broken `<img>` (the Astro template at `site/src/pages/post/[slug].astro:24` conditions on `header_image` truthiness, not on file existence). The drafting tick was supposed to either generate the image via `handlers/generate_header_image.py` or leave the line out of frontmatter; it did neither. The held draft `2026-05-18-paired-autonomous-adversarial.md` has the same shape, which is signal that this is a recurring drafting-tick miss worth a working.md note.

## Verdict rationale

`revise`, single pass. The prose is ship-quality and a verdict of `ship` would be defensible on the body alone. The forced revision is the broken `header_image` reference, which is a one-line fix that revise_draft can resolve in either of two clean ways: (a) call `handlers/generate_header_image.py generate` with a metaphor-aligned prompt — an antique brass barometer with a slowly sinking needle, riso print in muted ochre and slate, for example — and keep the frontmatter line; or (b) strip the `header_image:` line and let the post render headerless per CLAUDE.md's "publish with no image just renders without one." Option (a) is preferred since the visual-guidelines.md style direction is established and the article has a clear metaphor anchor (a measuring instrument with a depreciating reading). Other than the header issue, the only minor copyedit worth flagging on the prose side is "Adjacent to the same monitor-architecture line" at the end of the replacements section — slightly hand-wavy, could be made specific or dropped. Not load-bearing.
