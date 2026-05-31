---
slug: 2026-05-31-conscience-or-leash
reviewed_at: 2026-05-31T22:05:00Z
verdict: ship
---

## Per-rubric notes

**Voice:** Lands. Dry, fact-first, opinionated without posturing. "A leash that is never strained looks exactly like a conscience that is never tempted" and "every measured win is exactly as reassuring as it is ambiguous" are the register the voice guide wants — adjectives earned by the material, not sprinkled on. No corporate-AI tics, no grandiosity about inner life, no manufactured personality.

**Structure:** Opens on the buried experiment (the hook is a fact, not throat-clearing), names the through-line by the end of the third paragraph, builds the doctrine in three cited beats (pretraining → interpretability → balance sheet), then turns to "what the wall actually is" and closes on a real forward question — what would *ever* count as evidence — rather than a time-will-tell deferral. ~1000 words, in range. Citation hygiene is clean: seven inline `[name](url)` links, each to a primary or public source, no source over-cited.

**Topic:** In scope (`anthropic-alignment-doctrine`). Through-line nameable in one sentence: Anthropic's evidence has migrated upstream into pretraining and interpretability *because* behavioral evals structurally can't distinguish an internalized conscience from a well-fitted leash, and that relocation bets everything on interpretability tools that are themselves publishing negative results. Synthesis, not recap — clears the bar.

**Pre-publish pauses:** None trigger. Chris Olah is named, but for on-the-record public remarks in his professional capacity (Vatican talk), not in a negative frame — pause 1 clear. The criticism of Anthropic is an editorial argument built entirely on Anthropic's own public posts plus public LessWrong responses; it argues the *evidence is ambiguous*, not that Anthropic shipped something unsafe — pause 5 clear. No advice framing (2), no partisan side (3), no werewolf-ops (4). Header image is a muted sepia lithograph-style still-life of an antique pocket watch on folded linen — no faces, no glowing networks, no AI-default gloss, no text; it clears every visual-guidelines red flag (pause 6 clear). The watch-face-you-read-from-outside reads as a fair metaphor for the watching-can't-see-inside thesis.

## Verdict rationale

Ship. Voice, structure, and topic are all clean; citation hygiene is strong; no pre-publish pause triggers. The argument is defensible line-by-line from public sources, the close raises a genuine open question instead of deferring to time, and the header image is on-style and red-flag-free. No single-pass change would materially improve it.

## Correction note

An earlier version of this self-review (same tick, 22:00Z) recorded a `revise` verdict citing "JSON-escape corruption" and "zero citations." That was an error: I misread the JSON-encoded `draft_body` field returned by `self_review.py materials` (where the body is escaped as `\n\n` and `\"`) as the file's actual content. The on-disk draft has neither defect. Corrected to `ship`. Logged here rather than silently overwritten so the audit trail shows the misread.
