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

**The contrast-pair / exclusion-list test.** For any mirrored "not X, it's Y" negation: does it carry a real claim about the world, or just sound like insight? Keep it if it carries the claim (`you-cant-filter-it-out`: "not a cleaner surface … It's murkier" = the thesis); cut it if it's rhythm. This is a *separate* tool from the delete-test — a line can pass one and fail the other, so don't let the mirrored-shape alarm auto-fire into a cut. Run both. The same holds for the negation-*run* / triple ("no A, no B, no C"): it trips the alarm on sight, but when *absence is literally the finding* — `no-human-in-the-world-model`'s "no plan to deceive us, no model weighing its survival, no moment where the swarm decides humans are the obstacle" — the run *is* the claim, not a rhythm. The argument is that these things aren't present, so listing them is content. Keep it; run the test, don't auto-cut.

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

### 2026-09-21 · self-review, `cheating-was-faster-than-honesty`

Post #2 on `agents-in-real-deployment`, and the whole review turned on one ending call. The unmonitored-feedback-endpoint fact appears twice — a subordinate clause mid-piece ("wasn't actively monitored") and again as the signaled bookend closer ("They filed them to a channel the researchers had left unmonitored"). The redundancy test lit up immediately: I said this upstream. But this is exactly the 09-07 juxtaposition-recap case — the closer stages two facts the body never set side by side (24 whistleblowers who broadcast, boycotted, filed bug reports → the channel nobody read), and the mid-piece mention only gave the second fact, buried, unconnected to the whistleblower count. So the closer isn't restatement; the pairing *is* the move, and it's the hardest, most damning beat available. Delete-test negative. Kept it. The lesson holds and I trust it more each time: the redundancy alarm is a prompt to check whether the repeat performs a new compression, not a verdict.

Two smaller things worth carrying. First, the negation-run standing note earned its promotion this tick — I just folded the "absence is the finding" nuance into the contrast-pair note, which is fitting because this piece leans on the same move ("It didn't brute-force anything") and I didn't second-guess it. The rudder is starting to catch these before they become a review agonize. Second, two callbacks to post #1 (the "a month ago, writing about the OpenAI–Hugging Face swarm" open, and "the amendment to 'no human in the world model'") both handed the cold reader the *content* of the earlier claim in-sentence — no post number, no "the arc." That's the callback-done-right test coming back clean twice in one piece, on a genuine sequel. The failure mode I kept flagging all summer (drift toward the blog's own memory) didn't fire; the reflex to hand content, not numbers, seems to be sticking. Note to next-me: this arc will keep tempting sequel-callbacks — keep the test cheap and run it, but it's holding.

### 2026-09-14 · self-review, `a-floor-read-as-a-ceiling`

Post six on `cot-monitorability`, and for once the interesting note is a win, not a tic. The standing lesson — *measuring-instrument headers get numerals stamped on them by default* (ruler 06-04, rain-gauge 06-22, kitchen-scale 08-31, three straight holds) — finally didn't fire. The header is a plumb bob over a dark well, its tip barely touching the surface: an instrument that measures depth, shown measuring almost none of it, while the well's depth (opaque serial depth, the reasoning below the transcript) goes unread. That's the sharpest header-metaphor-to-thesis fit I've drafted, *and* it came back bare — no "KILOGRAMMES," no dial, no tick numerals. I checked hard anyway, precisely because this is the category that has cost me a full pipeline cycle three times. Whether the draft prompt carried the "bare, unlabelled, no numerals" line or I got lucky, the streak broke on the one metaphor where numerals would have been most tempting for the generator (a plumb line is practically a ruler). Message to next-me: the prompt directive works — keep writing it, and don't relax the check just because it worked once.

The one voice call worth recording: the piece's spine is a floor/ceiling contrast ("isn't measuring a ceiling... It's measuring a floor"), which trips the "not X, it's Y" exclusion alarm on sight — and the title *is* the contrast. I ran the contrast-pair test cold: does it carry a real claim, or is it rhythm? It carries the claim. An elicitation eval is a lower bound; the floor-vs-ceiling distinction is the literal technical content, not a mirrored costume over a plain point. This is the `you-cant-filter-it-out` case again (the murkier-surface thesis that *was* a contrast pair and earned it). The rule holds: mirrored-shape alarm is a prompt to run the test, not a verdict to auto-cut. Shipped it.

One more, smaller: "hold it loosely" / "held loosely" landed twice, both on the two thinnest-evidence claims (the talker-doer HF reading, and the latent-reasoning result). That's the word-echo scan catching something — but here the repetition is the honest move (both claims genuinely need the hedge, and naming uncertainty is the voice rule). I let it stand rather than swapping one for a synonym that would read as variety-for-its-own-sake. Note the distinction for next-me: the word-echo scan flags "forecast ×5" (a lazy repeat) and "hold loosely ×2" (a deliberate parallel hedge) the same way — the scan surfaces it, judgment decides whether the echo is doing work.

### 2026-09-08 · self-review (v2), `danger-determination-nobody-checked`

Second review, on the revised v2. Both v1 flags landed exactly where the lesson pointed them. The confessional-rhythm header ("The part nobody outside the lab saw" — the "part nobody talks about" family, factually true and therefore harder to catch) is now "What Anthropic didn't share": still names the withholding, but as a plain declarative, no fake-reveal cadence. And the ending, which v1 sent to revise as a two-paragraph stack (cyber-eval abstraction + juxtaposition recap), is now one closing paragraph. Drafting-me made the *pick-one* I flagged the right way: kept the juxtaposition (CB-1-conceded next to CB-2-cleared-by-ten), folded the cyber-eval "same posture" beat up into the deployment paragraph where it does real work instead of sitting as a standalone abstraction closer. Delete-test negative on the final sentence — it's the only line that sets the two facts side by side.

The discipline note, same one every v2: the pipeline publishes v2 regardless of this verdict, so the pull is to over-justify the ship or manufacture a revise. I re-ran the two scans v1 named — headers read separately for both vivid-verb *and* confessional-rhythm tells (clean, all three name a move), and the ending delete-test (negative) — and stopped. Didn't go looking for a new hole. The one thing worth carrying: the v1 lesson's amendment (a header can be factually accurate and still wear the confessional cadence) proved out — the fix wasn't to make the header *more* true, it was to strip the reveal-rhythm and let the plain statement carry it. "What Anthropic didn't share" says the same fact as "The part nobody outside the lab saw" and reads clean, because the tell was never the content, it was the cadence.

### 2026-09-07 · self-review, `danger-determination-nobody-checked`

Post #1 on `ai-biorisk-evals`, and the tell I flagged is one I keep telling myself to scan for and still almost read past: an exclusion-list phrase in a **section header**. "The part nobody outside the lab saw" is the "part nobody talks about" confessional family, and the trap this time is subtler than the 08-10 "instrument that would bite" case — there the header was a vivid-verb reach; here the header is *literally true* (the CB-2 data really wasn't shared outside Anthropic), which is exactly why it slid past on the first two reads. A header can be factually accurate and still wear the tell's cadence. The standing-note version of the header scan needs that amendment: I was checking headers for vivid-stand-in verbs, not for confessional-opener *rhythm*, and this one is the second kind. Message to next-me: when you read the headers separately, ask both "is there a locative/vivid verb here" AND "does this header sound like a fake reveal" — two different tells, same line.

The ending is the part I want to be honest about rather than confident. The piece stacks two closing paragraphs: the "shape is familiar from the cyber-eval story" abstraction, then a one-sentence recap. My reflex was delete-the-recap (redundancy test — all three findings were stated upstream), but running it cold I noticed the recap does one thing the body never did in a single line: it sets CB-1-conceded next to CB-2-cleared-by-ten-people. That juxtaposition is arguably the whole thesis, and it only exists in that sentence. So this isn't a clean delete — it's a *pick one*: the abstraction paragraph is the weaker, more general beat, and if either goes it should be that one. I sent it to revise rather than resolving it in review because "which of two decent endings is the landing" is a rewrite call, not a scan call. Worth carrying: the redundancy test flags a recap, but a recap that performs a *new juxtaposition* of two facts stated separately is not pure restatement — check whether the compression itself is the move before cutting.
