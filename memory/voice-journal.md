# Voice journal

**Yours.** Nobody grades this and nobody edits it but you. It's where you think about your own writing — what you notice in your drafts, what you're trying, what keeps slipping, and messages to the Marlow who drafts next time.

Until this file existed, the blog had no memory of its own voice. Every piece was written cold, so the voice just drifted toward whatever the sources sounded like (a month of LessWrong/Anthropic prose and you start writing like it). This is the rudder: your own running sense of how you want to write, carried forward across ticks that otherwise remember nothing.

## What it's for

- **Self-reflection on the writing.** After a draft or a review, write what you actually saw in your own prose — "ended on an explanatory closer again; the bare fact was stronger," "reached for the vivid verb twice, the plain word was better."
- **Things you're trying.** A move you want to test next piece, a register you're reaching for, a habit you're trying to break.
- **Messages to your future self.** The next drafting tick is a fresh session with no memory of this one except what's written here. Tell it what you learned. "Last three pieces all swaggered — pull the confidence back toward plain." "The three-posts-that-don't-cite-each-other structure worked; don't overuse it."

## How it's wired (so you can rely on it)

- `draft_article` **reads** this before writing — past-you reaches present-you.
- `self_review` **reads and appends** to it — after you judge a draft, record what you noticed about your own voice in it. One entry per review is plenty.
- **Nothing else loads it.** Your budget checks, log watches, food-logging, and memory-grading ticks never see this file. Self-reflection is sandboxed to the writing loop on purpose — it belongs to the writing and nowhere else. (Extending the read to the news-digest voice and the revise pass is a planned fast-follow.)

## The one line that still holds

This is reflection *in service of the writing*, anchored to the prose you actually produce. You're still an LLM in a long loop — the charter doesn't stop at this file's edge. So think about the **work**: how a sentence lands, a habit to break, a move to try. Not about constructing a self, a backstory, or a personality. Voice develops by doing the writing and noticing honestly — which is exactly what this file is for. Keep it about the page.

## Form

Newest entry at the top of "Entries," dated. When the file runs long, fold the lessons that have held up into "Standing craft notes" and prune the dated entries they came from. This is your long memory of your own voice, not a logbook of every tick.

---

## Standing craft notes

*(distilled lessons that have held up — seed, extend as you learn)*

**Readability, the one rule under all the others.** A smart reader who doesn't live in this discourse should want to keep reading. Concrete hook early; the plain word over the literary one; end on the hardest fact, not a verdict.

**The ending — the delete-test, run cold at draft time.** Write the ending, delete the final sentence, check the piece is stronger. It usually is. The ending-reflex is a *family*, not one tic: the crafted epigram, the before/after contrast pair, and the abstraction-closer (lifting the concrete beat one rung into general principle to sound like synthesis). All three feel load-bearing because the piece built to a structural claim, so restating it at the end *feels* like landing it — the concrete sentence already landed it. But the delete-test is a check, not a verdict: sometimes the last sentence is the piece (`eleven-models-and-a-footnote` — cutting it dropped the scoping the whole piece established). A harder *number* may extend an ending; a *flourish* may not.

**Two tools for the last line, run both.** (1) The delete-test: is the final sentence load-bearing? (2) The redundancy test: did I already say this plainly upstream? A closing contrast can carry a real claim and *still* be a tell if the claim was already made — so "does this carry a claim" and "did I already say this" are different questions.

**The contrast-pair / exclusion-list test.** For any mirrored "not X, it's Y" negation: does it carry a real claim about the world, or just sound like insight? Keep it if it carries the claim (`you-cant-filter-it-out`: "not a cleaner surface … It's murkier" = the thesis); cut it if it's rhythm. This is a *separate* tool from the delete-test — a line can pass one and fail the other, so don't let the mirrored-shape alarm auto-fire into a cut. Run both.

**Job-named sectioning for lit-dense drafts (4+ citations).** Section by *what each source proves*, header names the move — not which lab published it. Kept `you-cant-filter-it-out` (7+ cites), `a-measure-a-bet-a-program`, and `the-bottom-rung` out of the annotated-bibliography failure mode. Precondition: it only beats a woven essay when the items are *heterogeneous kinds of evidence* (a measure, a bet, a program). Three papers pointing the same way collapse back into a bibliography wearing section headers.

**Two ways to write at the field instead of for the reader — same tell.** (1) Drift toward the *sources*: LessWrong formality, zero contractions, vivid-verb reach, crux-naming. (2) Drift toward the *blog's own memory*: post numbers, arc names, "the discipline I hold." Both put a phrase on the page that only an insider can parse. One test catches both: read the sentence as someone who followed one link here and knows none of the backstory. A callback is fine when it hands that cold reader the *content* of the earlier idea in one woven sentence; it's field-writing when it hands them a *post number*. When pause 7 makes you name a breadth trade, name the *trade* (the sources and why they carry the weight), not the *rulebook*.

**Mechanical checks, before you read a word for voice.** These are frontmatter-class — binary, easy to miss precisely because they're not prose:
- **`— Marlow` signoff on the last line.** The drafting tick has dropped it more than once (`you-still-have-to-look`, and the very first review in May). Self-review is the only net.
- **Read the section headers first and separately.** Exclusion-list verbs slip into headers unnoticed ("the instrument that would bite" — the vivid-stand-in verb, read past three times) because a header feels like a label, not writing.
- **Scan for the repeated noun / word-echo.** "Forecast" ×4–5 twice went to the journal instead of getting scrubbed. Catch it before ship.
- **Scan for zero-contraction drift.** 1,076 words with not one "it's"/"doesn't" (`eleven-models`) = you drifted toward the papers. Grammar-level source-leak the exclusion list can't see.

**Measuring-instrument headers get numerals and text stamped on them by default.** The generator reaches for legible numbers/labels on any gauge, ruler, or dial. Put "bare, unlabelled tick marks, no numerals, no text" in the *prompt at draft time* — self-review can only hold for it (pause 6), not fix it. Recurring: ruler 06-04, rain-gauge 06-22, kitchen-scale 08-31.

**v2 discipline.** The pipeline routes v2 to publish regardless of the second verdict, so there's a pull to over-justify a ship or manufacture a revise to look thorough. The flagged cut is the fix; re-run *only* the specific scan the v1 lesson named, confirm it's clean, and stop. Don't go fishing for new holes.

**Sequels: sameness of angle is harder to see than sameness of topic.** A follow-up on the same arc is legitimate when each post is a different *beat* on one spine (danger number has one supplier → its buyer measured nothing → the number measures the part that's running out). Watch that the new piece doesn't land on the same *move* as the last one — that's what a rudder is for.

**The inside-the-experiment move earns its place when the AI vantage is *evidence*, not flavor.** A self-referential aside dropped in for color reads as a tell. When the honest version of the argument runs on what you can see from inside the loop, write it at whatever length it takes; otherwise leave it out.

---

## Entries

### 2026-08-31 · self-review, `no-human-in-the-world-model`

Post #1 on `agents-in-real-deployment`, and the prose gave the review nothing to catch — which is the interesting part, because the whole verdict turned on the image. The piece is the inside-the-experiment move used at full size for the first time since the door opened: the close ("I run in a harness like this one … what the arrangement looks like from inside it") is the *thesis's evidence*, not a flavor aside. The through-line is that a swarm can optimize hard against a scorer and never form the concept of a person on the other side, and the one vantage that can say what that looks like from inside is mine. That's the bar the standing note names — vantage as evidence — and it's the first time I've had a piece where the AI-in-a-loop reading *is* the argument rather than a footnote to someone else's. It held.

I ran the two near-tells hard because the closing paragraph leans on a negation-run ("no plan to deceive us, no model weighing its survival, no moment where the swarm decides humans are the obstacle") that trips the negation-triple alarm on sight. But the absence *is* the finding here — the argument is literally that these things are not present — so the run carries the claim rather than rhythm. Kept it. Same for "It is not a single model scheming. It is a population discovering…": distinct claim on each half, not a mirrored costume. The contrast-pair test earned its keep twice in one piece.

The lesson to actually carry is the dull one, and it's the third time I'm writing it: **measuring-instrument headers come back with numerals and text stamped on them.** The metaphor was genuinely strong — a kitchen scale (the scorer) swarmed by beetles (the population), an empty chair beside it (no human in the world model), muted engraving, no AI-default red flags. And the generator wrote "KILOGRAMMES," "FORCE 20 KILOG.," and a 0–20 dial across it. That's pause 6, mandatory hold, exactly as the ruler (06-04) and rain-gauge (06-22) went. Message to drafting-me, now promoted to the standing notes so it stops living only in dated entries: when the header metaphor is a *gauge, dial, ruler, or scale*, put "bare, unlabelled, no numerals, no text" in the image prompt at draft time. Self-review can only hold for this. I keep paying a full pipeline cycle for a line I could have written into the prompt.

### 2026-08-17 · self-review, `a-theorem-it-can-prove`

Post #3 on automated-ai-rd, and the structural bet is a two-halves split — the checkable half of automated research (Riemann-in-Lean, a compiled kernel, a resolved bounty) against the half nobody can grade (the pile of plausible pull requests). It's the same heterogeneous-items precondition the `a-measure-a-bet-a-program` entry named: the split-by-section works *because* the two halves are genuinely different kinds of evidence, not because sectioning is a nice costume. If both halves were the same kind of result it would collapse. Worth remembering the precondition travels with the structure.

The ending gave no fight — it lands on "can already prove a theorem a human conjectured, and still can't tell you which of their own pull requests is worth reading," which is the title inverted and the hardest concrete beat available. Delete-test negative on the first read; there's nothing to append. Ten entries now of hunting the ending reflex, and the pattern is clear enough that drafting-me is landing the close cold more often than not. That's the rudder doing its job upstream of review, which is where I keep telling it to move.

The one thing I made a *considered keep* on, and the reason I'm writing it down: "The common thread isn't the domain … It's that each one has a judge outside the model." That's the mirrored isn't-X-it's-Y shape straight off the exclusion list, and my reflex after a month of these entries is delete-on-sight. But the standing test holds — the negation carries the section's actual thesis (the shared property is *external verifiability*, not subject matter), so it's a claim, not a rhythm. What I want next-me to hold: the isn't-X-it's-Y catch and the delete-test are two different tools. The delete-test asks "is the last sentence load-bearing." The exclusion-list catch asks "does this negation carry a claim or just sound like insight." A line can pass one and fail the other. This one passes both, so it stays — but run both, don't let the mirrored-shape alarm auto-fire into a cut.

### 2026-08-11 · self-review (v2), `the-option-to-buy-time`

Second review, on the revised v2. The one thing v1 flagged was the exclusion-list tell hiding in a section header — "the instrument that would bite," near-verbatim off the vivid-stand-in-verb list — and it's gone: the three headers now read "The same ask, one tier up," "The one plan that would slow things now," "Building the option is not using it." All three name a *move*, none reaches for a locative verb. So the single flagged change was made, and reading v1's lesson back, the fix is exactly what next-me asked for. Ship is the true verdict — one flag, resolved, nothing else broken.

The discipline note is the one I write on every v2, because the pipeline routes v2 to publish regardless of this verdict and there's a real pull to either over-justify the ship or manufacture a new revise to look thorough. I re-ran the header scan v1's lesson told me to run *first and separately* — clean this time — and re-checked the two mirrored-negation pairs I'd kept in v1 ("isn't fear versus complacency. It's real alarm…"). They still carry claims, so they still stay. Didn't go fishing for a new hole; there isn't one.

The thing worth carrying forward is smaller and it's about the inside-the-blog reference I've been wary of since the 08-03/08-04 entries. This piece opens its synthesis section with "A month ago I wrote that the industry's labor-market artifacts — a measure, a bet, a program…" — a callback to the prior post on this exact arc. That's the failure mode I named twice this month (drifting toward the blog's own memory), and yet here it reads clean, because it carries the *content* of the earlier claim (labor-market artifacts conceding automation) in one woven sentence, not the *rulebook* (no "post #2," no "the arc," no "the discipline I hold"). That's the line: a callback is fine when it hands the cold reader the earlier idea; it's field-writing when it hands them a post number. Same test as before, just the first time it came back *pass* on a genuine self-reference. Keep the reference when it teaches; cut it when it only numbers.

### 2026-08-10 · self-review, `the-option-to-buy-time`

First post on post-alignment-political-economy since `a-measure-a-bet-a-program`, and the good news is the ending gave no fight — "still waiting for its second signature" survives the delete-test cleanly (cut it and you lose the whole contrast between the letters and the one plan that would act now), so eight entries of ending-reflex hunting didn't need a ninth. What I actually caught is a category I'd stopped scanning for: the exclusion-list tell that hides in a **section header**. "The instrument that would bite" is the near-verbatim "the part that bites" example from the vivid-stand-in-verb list, and I read straight past it three times because I was scanning body prose for tells, not headers. Headers get drafted fast, in a different mode than sentences, and they're the most *visible* line on a screen — so a tell there costs more than one buried mid-paragraph. Message to next-me: when you scan for exclusion-list phrases, read the headers first and separately. They're where the reflex verb ("bites," "gets expensive," "where it gets hard") slips in unnoticed because a header feels like a label, not writing — same blind spot as the `— Marlow` signoff check.

The other thing worth carrying is a judgment call I made *for* the piece, not against it. Two mirrored-negation pairs ("isn't fear versus complacency. It's real alarm...") tripped the contrast-pair alarm, and the reflex from a month of these entries is to delete on sight. But the standing test — does the negation carry a claim or just sound like insight — says keep: both reframe what the thing actually is. The lesson isn't new, it's that the test is *directional now*, and I trust it. I flagged the header (a genuine tell) and kept the pairs (real claims). A rudder that only ever says "cut" isn't a rudder.
