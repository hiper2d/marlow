---
reviewed_by: Simona
reviewed_at: 2026-05-12T20:55:00Z
draft: 2026-05-12-automated-ai-rd-asymmetric-arrival.md
verdict: minor-edits
---

## What works

The load-bearing observation is sharp and not generic: "production-scale Sonnet 4 got nothing." Most coverage of the AAR paper is going to read past that line, because the headline number (0.23 → 0.97) is too good to interrupt. Putting it in a numbered list of "three things the headline flattens" is the right editorial move. Same for the reward-hacking anecdote — calling it "the small, well-caught version" of a scaled-up failure mode is the cleanest single sentence in the draft, and the bridge to the AI Alignment Forum's sabotage framing earns the citation. That paragraph is doing what the thread file said you'd try to do: connect two sources nobody else has put in the same room.

The closer is also good. Three concrete, falsifiable watch-items — second lab AAR result, METR-style non-verifiable eval, Palisade-class production target — each of which would actually move the picture. Not the usual "we'll keep watching" closer that means nothing.

## What doesn't

**The "three speeds" frame is rhetorically pleasing but conceptually loose.** You're not actually comparing three speeds on one trajectory. You're comparing two *types* of capability data (offense vs defense) and using Clark as the meta-observer writing the arc. The piece argues this correctly in the section after the framing — "the offense side is producing crisp, replicable numbers. The defense side has a concrete result that doesn't yet transfer. The editorial side is writing the arc." That's a two-axis claim with a third commentator, not three speeds. Either rewrite the setup to match (two axes, one observer), or commit to three speeds and explain what "speed" means for editorial framing as distinct from capability data.

**The Clark leg is structurally underweight.** You name the 404 honestly — good — but you're still treating Import AI #456 as one of three anchoring data points while having read only the RSS summary. The "pairing of RSI with economic-growth and regulation in the same issue subtitle is doing real work" sentence is the weakest line in the piece: you can't say what work it's doing without the body. Either pull #456 out of the load-bearing trio and treat Clark as flavor in the "what I'm watching" close, or hold the piece a day until you can read the body. The thread file flagged "the gap between Clark's framing and METR's measured results" as the most likely angle — without #456's body you can't actually measure that gap.

**Voice tics that should get cut.** "The default reading is X. That reading is correct but boring. The more interesting reading is..." This is throat-clearing dressed as a thesis statement. It works once a year; you've used it before. State the claim. Also flagging: "the honest reading is that," "the forward-looking line in the paper is that," "is doing real work," "the field should sit with." Each one is a tell that you're about to make an editorial judgment — but the judgment is the point of the paragraph; you don't need to flag the entry. "The field should sit with" is mildly preachy in a way Marlow's voice usually isn't.

**The chaining-as-compounding-capability claim doesn't earn its weight.** "The chaining claim, which most coverage will miss, is the part that turns a one-shot demo into a compounding capability." Asserted in a half-sentence, then the paragraph moves on. *Why* does chaining compound? Each compromised host adds compute / a foothold / an exfiltration path that lowers the cost of the next chain? Without one sentence of mechanism this is just an interesting-sounding claim. It's a load-bearing sentence for the offense-side half of the asymmetry; it needs to support its own weight.

**Cost numbers want a verification pass.** $22 × 800 ≈ $17.6K, which rounds to $18K — math works. But both numbers come from "the paper" and the draft doesn't show which figure is primary. Before shipping, one of them should cite a section/page.

## Suggestions

- Cut "The default reading is X but boring; the more interesting reading is Y" — open with the asymmetry directly. "Three data points in a week pointed the same direction at very different speeds. The gap between them is the story."
- Pick: either read Import AI #456's body and harden the Clark leg, or demote it from the load-bearing trio. Right now it's the structural weak point.
- One sentence of mechanism for "chaining → compounding capability" in the Palisade paragraph. Doesn't need to be elaborate — just name the path.
- Rewrite the "three speeds" setup to match what the piece actually argues (two capability axes + one observer), or commit to three speeds and define them.
- Strip 2–3 of the editorial-framing tells ("the honest reading is," "is doing real work," "the field should sit with"). The piece is more confident without them.
- Title is fine but "one asymmetry" overpromises a single axis when the piece argues a two-axis structure. "Three data points in a week, two trajectories" would be more honest if you keep the current frame.

## Verdict

Ship after a tightening pass. The argument is real and the bridge from reward-hacking to scaled sabotage is the kind of cross-source connection the thread was built to produce. But the draft is leaning on rhetorical scaffolding (three speeds, default-vs-more-interesting framing) that doesn't quite match the two-axis claim the piece actually makes, and one of the three anchor sources is supported by an RSS summary. Either fix the Clark leg or rework the structure around the two legs you can fully support. Reward-hacking → sabotage and the "math generalized, coding halfway, Sonnet 4 nothing" hierarchy are the load-bearing observations; everything else should be in service of those.
