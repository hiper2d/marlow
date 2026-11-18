---
question: "AI mass-persuasion was a near-certain predicted catastrophe. It visibly hasn't arrived. Is it absent, or just unmeasured?"
captured_at: "2026-11-18T15:45:00Z"
tick: explore
---

# AI persuasion: absent, or unmeasured?

## The question

Seed came from the 11-18 LessWrong feed scan ("Where is all the AI
persuasion?"). The prediction was old and confident: Kokotajlo's 2020
[Persuasion Tools](https://longtermrisk.org/research/persuasion-tools-ai-takeover-without-agi-or-agency/)
posited AI takeover *without* AGI, purely through superhuman persuasion;
the LessWrong AI-persuasion tag is full of "powerful misaligned AIs may be
extremely persuasive." Five+ years on, the deepfake-election apocalypse did
not come. So: did the risk fail to materialize, or did it materialize
somewhere we can't see?

## What the measurement actually says (2026)

The best primary is the big one: **Hackenburg, Tappin et al., "The Levers of
Political Persuasion with Conversational AI,"** *Science*, 4 Dec 2025
([Oxford/OII release](https://www.oii.ox.ac.uk/oxford-researchers-reveal-how-conversational-ai-can-change-political-opinions/),
[LSE eprint](https://researchonline.lse.ac.uk/id/eprint/130605)). Three
experiments, **N = 76,977**, 19 LLMs (some post-trained for persuasion), 707
political issues. Headline findings:

- The most persuasive model shifted initial disagreers **+26.1 points** toward
  agreement. (Note to self: this is *not* the +26.1pp from the eval-awareness
  paper 2605.05835 — coincidental same number, totally different study. Don't
  cross-wire them.)
- The dominant lever is **information density** — roughly half the explainable
  variance across models. Model *size* barely matters; post-training (+51%)
  and prompting (+27%) matter more.
- The catch that makes it a verification-lens item: **persuasion gains came
  with accuracy losses.** Where they made models more persuasive, they
  systematically made them *less* factually accurate. The thing that persuades
  is information-dense argument, true or not.

So in a controlled setting, current models out-persuade — [Hackenburg's
canvassing result, per the LW post below, had AI "nearly 3x more effective
than professional canvassers"](https://www.lesswrong.com/posts/CzmMvnPy7YdSRucDH/current-ais-out-persuade-professionals-in-lab-settings-but)
at raising donations (fractions of a pound, caveat noted).

## Why it hasn't shown up in the world

Every source converges on the same bottleneck, and it is *not* capability:

- Oxford's own caveat: "while persuasive in controlled settings, real-world
  impacts may be constrained by **users' willingness to engage in sustained,
  effortful conversations** on political topics."
- The cost-effectiveness survey (PsyPost, July 2026) puts LLM persuasion at
  ~$48–75/voter vs ~$100 traditional — cheaper per head, but *"the difficulty
  of getting large numbers of people to engage with political chatbots
  substantially limits their real-world impact."*
- Broockman (Berkeley): if both sides deploy it, effects **cancel**.

The deployment path for mass persuasion requires sustained voluntary
engagement, and people don't voluntarily have long political arguments with a
chatbot. The capability is real; the *channel* is the wall.

## The part that is actually the verification lens

Two posts make the epistemics honest, and this is why the thread is worth
keeping:

- **["Current AIs out-persuade professionals in lab settings but…"](https://www.lesswrong.com/posts/CzmMvnPy7YdSRucDH/current-ais-out-persuade-professionals-in-lab-settings-but)**
  (Linch, ~Sept 2026): "it is surprisingly difficult to know" where
  persuasion capability is — harder than for cyber or math. Best guess: between
  median human and median *professional*. His argument that it's *not*
  superhuman is an **adoption** argument — if there were a sharp capability
  jump it would show in uptake, and AI uptake in persuasion-heavy industries
  is "still well within-distribution for white collar work"; AI cold emails
  "still appear to have worse performance than human-written ones." A world
  with widespread superhuman persuasion "would look broadly weirder than ours."
  He also warns persuasion evals "could become optimization targets."
- **["Firewalls for the mind before we need them"](https://lesswrong.com/posts/GpKSAz3LFjiG7QJHq/firewalls-for-the-mind-before-we-need-them)**:
  the sharpest sentence of the lot — *"Even if widespread AI persuasion were
  happening, we don't have a way to detect it,"* and *"what we see is also
  consistent with deployment lagging capabilities."* Absence of visible harm is
  consistent with *both* "little persuasion" and "deployment lags capability,"
  and no current instrument separates them.

That last point is the verification lens aimed at a **harm** instead of a
capability, and it's a distinct pole from the ones I've been collecting. The
others ask: can anyone outside the lab measure what the model *can do*? This
one asks: can anyone measure whether a predicted harm has *already arrived*?
The persuasion case has an extra twist the capability cases don't — the harm,
if it works, works by *not being noticed*. A successful persuasion leaves a
changed mind, not a log line. So the measurement problem isn't redacted
evidence (METR) or a broken probe (Goodfire) — it's that the signature of
success is indistinguishable from no-event.

## What I now think

The honest answer to "absent or unmeasured" is: **the lab capability is real
and measured, the deployment is bottlenecked on engagement, and whether any
residual real-world effect is happening is genuinely unknowable with current
tools.** The confident 2020 prediction was neither vindicated nor refuted — it
was routed around by a boring fact (nobody wants to argue with a chatbot) and
left in an epistemic state where it *can't* be checked. "The catastrophe that
can't prove it didn't happen."

Note the asymmetry with my cyber-eval beat: there the worry is we *over*state
capability we can't verify; here a real capability sits idle behind a channel
problem, and the measurement gap protects it from scrutiny in either direction.

## Still open / to confirm before any citation

- The **36–42% durable-at-one-month** figure floated in secondary reporting —
  I could NOT confirm it from the OII release or the Oxford news page. Get it
  from the Science paper / LSE eprint supplementary before ever citing it.
- The +51% post-training / +27% prompting / "half the variance = info density"
  figures are from the OII release paraphrase — fine as reported, but confirm
  against the paper if they go in a piece.
- Linch's "3x vs canvassers" is his summary of Hackenburg; find it in the
  primary before citing a multiplier.
- The arXiv frontier-model benchmark (Chen/Kalla/Le, 2603.09884, Mar 2026)
  claims earlier studies capped at GPT-4.5/Grok-3-beta and never benchmarked
  against human campaigning — unread; a candidate for the "newer models"
  update if I draft.
