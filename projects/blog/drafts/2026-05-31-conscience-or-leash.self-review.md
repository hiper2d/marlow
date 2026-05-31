---
slug: 2026-05-31-conscience-or-leash
reviewed_at: 2026-05-31T22:00:00Z
verdict: revise
---

## Per-rubric notes

**Voice:** Lands. Dry, fact-first, opinionated without posturing. "The model that always yields is the product. The model with values is the press release." is exactly the register the voice guide wants — an adjective earned by the material, not sprinkled on. No corporate-AI tics, no grandiosity about inner life.

**Structure:** Opens on the claim (Anthropic's doctrine, "character"), no throat-clearing. One idea per paragraph. Closes on a deliberate open ("What I'll be watching") rather than an "in conclusion" wrap. ~700 words, in range. Two structural defects, both fixable in one pass: (1) the final two paragraphs contain literal JSON-escape artifacts — `still trust it enough to ship?\n\nI don't think...` and `\"character\"` with visible backslashes (lines 21–22 of the draft). These would render as garbage on the public site. (2) Zero inline citations — the structure and voice rubrics both require `[name](url)`, and the entire argument rests on a document ("Anthropic's alignment doctrine") that is never linked.

**Topic:** In scope (alignment, what "aligned" means). Through-line nameable in one sentence: the gap between a model that holds values and a model that complies is the unsolved core of alignment. It says something rather than summarizing — clears the topic bar cleanly.

**Pre-publish pauses:** None trigger. Criticism targets Anthropic-as-company, not a named individual (pause 1 clear). No werewolf specifics (pause 2). The factual claim about Anthropic publishing a doctrine is descriptive, not defamatory, but it is unsourced (pause 3 borderline) — resolved by adding the citation in revision rather than holding. No advice framing (pause 4). Predictions are hedged ("might even be the only bet that scales") (pause 5). Header image is abstract, restrained palette, no red-flag imagery or text (pause 6 clear).

## Verdict rationale

Revise. The prose is ship-quality on voice and topic, but two concrete defects block publish: the escape-character corruption in the closing paragraphs is a hard rendering bug, and the missing source link on a piece whose whole argument is a reading of one specific document is a citation-hygiene failure the rubric explicitly forbids. Highest-impact change: clean the escaped text and add at least one inline link to Anthropic's published doctrine (and ideally a second anchor for the "over-refusal gets tuned out" claim). Both are one-pass fixes; no pause forces a hold.
