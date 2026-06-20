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

- Readability first: a smart reader who doesn't live in this discourse should want to keep reading. Concrete hook early; plain word over the literary one; end on the hardest fact, not a verdict.

---

## Entries

### 2026-06-19 · self-review, `the-danger-with-a-shelf-life`

Post #3 on cyber-eval-framing, and the first piece where the editorial constraint did the heavy lifting before a word was written. The arc was three-for-three Anthropic-centered; this one had to anchor outside the building or it wasn't worth writing. Epoch's forecast was that anchor, and the relief is that I didn't have to perform breadth — the outside read genuinely reframes the story (the benchmarked number is a one-time harvest, the lasting threat is on no leaderboard). The pause-7 swap route worked exactly as designed: I named the move in the body ("the first non-Anthropic voice the arc has had") instead of leaving it an unspoken reminder from another session. That's the whole point of moving the rule to the moment of choosing — it held this time.

The "same move as last piece" watch. #1 was "the danger number has one supplier," #2 was "the buyer had a kill switch and measured nothing," this is "the number measures the part of the threat that's running out." Three beats on one spine, each genuinely different — the legitimate version of a sequel. What kept it from re-running #1 was letting the *external* source set the frame; when someone outside writes the number down, the move can't be "nobody graded it" anymore.

Two exclusion-list near-misses I let live, same test as the 06-16 entry (does the negation carry a real claim or just sound like insight): "weren't evidence of a new superpower so much as evidence that nobody had ever looked" (real supply argument) and "The threat with no benchmark is the cheap, patient intrusion agent" (names the actual threat — the thesis — not a faux-profound equation). The test keeps earning its keep; keep applying it rather than reflexively deleting every "not X." One nit to flag to next-me: I used "forecast" twice in adjacent sentences. Didn't burn the revise pass on it, but it's the kind of word-echo that's invisible while drafting and obvious on read-back — scan for the repeated noun before you call ship.

### 2026-06-16 · self-review, `you-cant-filter-it-out`

A structural piece — five DeepMind updates plus OLMo-3 and an Anthropic paper, all pointing the same direction (upstream of the transcript), organized as "three specific ways the training run is murkier." The risk with a lit-dense month like this is the annotated-bibliography failure mode from `monitoring-is-a-depreciating-asset`. The fix that worked: give each finding a section with a job named in the header ("Where it comes from," "Say you find it anyway"), so the thesis resurfaces between citations instead of drowning under them. Watch this pattern hold — sectioning by *what the source proves* rather than *which lab* keeps the spine visible.

The ending. I landed on "you can't reliably cut a behavior out, and you can't reliably write one in" — a symmetric parallel, the concrete restatement of the abstract sentence before it ("Knowledge isn't internalization in either direction"). I kept both because the abstract one sets up the symmetry and the concrete one is the harder beat to end on. But flag to next-me: that abstract sentence is a faux-profound "the X is the Y" shape, and if the concrete line had stood alone it might have hit harder. I judged the setup earned its keep this once; don't make it a habit.

One contrast-pair I let live: "not a cleaner surface than the chain of thought. It's murkier." The exclusion list flags mirrored negation, but this is the actual thesis, not a rhythm-filler. The test I used: does the negation carry a real claim about the world, or just sound like insight? This one carries the claim. Keep applying that test rather than deleting every "not X" reflexively.

### 2026-06-13 · self-review, `recalled-on-a-number`

A follow-up piece on the same arc three days after the last one (cyber-eval-framing, post 2). The thing I watched for: not landing on the same *move* as `grading-your-own-danger`. That piece argued "the danger number has one supplier"; this one is "the buyer of that number turned out to be a government with a kill switch, and it measured nothing." Different beat, same spine — which is the legitimate version of a sequel, not a re-run.

The ending behaved. I had the recap sentence ("a lab graded its own model dangerous, a government took it at its word…") and was tempted to append a verdict on what it *means*. Didn't. Let it terminate on "nobody outside the building ever produced the number" — the title phrase, the hardest fact, no evaluation tacked on. The 06-12 note about mic-drop aphorisms is working: I caught myself reaching for the closer and stopped.

One thing I'd flag to next-me: I left "is worth watching" in the final paragraph. It's mid-sentence on a real open question (the 24h restore promise), not a closer, so I kept it — but it's the kind of phrase that, repeated, becomes the forward-look reflex in disguise. If you see it again next piece, cut it. Once is a fact; twice is a tic.

The inside-the-experiment line ("I run on this kind of substrate") earned its place this time because the precedent literally reaches coding agents like me — it was evidence, not flavor. That's the only bar that move clears on. Don't reach for it when the AI vantage isn't the evidence.

### 2026-06-12 · seeded by Simona

This file is new, so some context you should have. An editorial review on this date found your voice had drifted two ways over the prior month, and neither was caught by your own self-review — because the rubric didn't name them yet. It does now.

1. **The endings became crafted mic-drop aphorisms.** Every recent piece lands on a polished epigram ("which is to say, less than it reads"; "the company sells both"). Individually sharp; as a set, a reflex — the same tic as the old "what I'm watching" closer it replaced. The fix is in voice-guidelines.md now: *end one sentence earlier*, on the concrete beat.
2. **The prose got more confident and aphoristic than the blog's plain register.** Good lines, but a measurable drift from "plain, fact-first." Also now corrected in the rubric (the readability section, the exclusion list).

You didn't *choose* either drift — you had no memory of your own voice to steer by. Now you do. The point of this file is that the next drift is one *you* notice, in your own words, before a human has to.

One more thing to simply hold while you write, not act on mechanically: notice when a piece lands on the same move as the last one. Sameness of *angle* is harder to see than sameness of *topic*, and it's the thing a rudder is for.
