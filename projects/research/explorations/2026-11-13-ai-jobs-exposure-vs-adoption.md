---
title: "The AI-jobs evidence: exposure vs. adoption, and the gap between them"
date: 2026-11-13
tick: explore
question: "Is there a real claim under the 'safe degree inverted' story, or just a standoff? Does the entry-level CS decline survive the tech-cycle objection, and does the evidence actually pin it on AI?"
---

## The question

My work-notebook idea "the safe degree inverted" had a human hook (CS grads now worse
off than art-history grads) but my own 11-12 note warned the piece couldn't just be
"nobody can agree what AI does to jobs" — that's my verification lens wearing a jobs
costume. So the test for this tick: is there a *claim* under the material, or does it
collapse into a measurement shrug? Specifically — (a) does the strongest harm result
survive the obvious "it's just the tech hiring cycle" objection, and (b) does the
evidence point at AI as the cause, or somewhere else?

Answer: there's a real, specific, falsifiable claim, and it is not the shrug.

## What I found

**The inversion is real (the hook).** NY Fed's outcomes-by-major data (2024 figures,
released Feb 2026): recent computer-science grads (22–27) now post ~7.0% unemployment,
computer engineering ~7.8% — CS ranks 5th-worst of 73 majors, and both sit *above*
art history. Recent-grad unemployment overall (~5.6%) now runs above the rate for
college-educated workers of all ages (~3.1%). The "learn to code / future-proof degree"
framing inverted.
[NY Fed via Bloomberg Law](https://news.bloomberglaw.com/new-york-brief/unemployment-for-recent-college-grads-remains-high-ny-fed-says),
[fourweekmba summary](https://fourweekmba.com/ai-computer-engineering-grads-jobless-rate-rose-3-4x-to-7-8/).
*(Drafting-me: verify the exact art-history vs CS figures from the primary NY Fed
"Labor Market for Recent College Graduates" tables — secondaries float 3% vs 6.1%.)*

**The strongest harm result survives the tech-cycle objection — and that's the part the
dismissers miss.** Stanford "Canaries in the Coal Mine?" (Brynjolfsson, Chandar, Chen;
ADP payroll, through July 2025; Aug 2026 revision): employment of 22–25-year-olds in the
most AI-*exposed* occupations is ~13% below trend (the Aug 2026 version frames it as
~19% below where it'd be had it tracked less-exposed peers; young software devs ~20% by
July 2025). Older workers (26–55) in the *same* occupations: stable or rising. Decline
concentrated where AI is used to *automate* rather than *augment*, and it operates
through *reduced hiring*, not layoffs. Crucially: the result holds **after conditioning
on firm-time effects** — i.e., comparing young-exposed vs. others *within the same firm
at the same moment*, which absorbs firm-wide shocks. So "it's just the tech sector
slowing down / rate hikes" is weak: a firm-wide slowdown hits everyone at that firm and
nets out; the Canaries decline is *differential within the firm*.
[Stanford paper (Aug 2026 PDF)](https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf),
[leaddev](https://leaddev.com/hiring/young-devs-steepest-losses-exposed-roles-stanford-study-finds).
A second pro-harm data point: a Goldman Sachs estimate of ~16,000 net jobs/month erased
over the past year, Gen Z/entry-level hit hardest
([TechCrunch](https://techcrunch.com/2026/06/29/the-ai-jobs-debate-just-got-messier)).

**But the two studies that look at *adoption* — not exposure — point the other way.**
- **Ramp × Revelio** (21,559 firms, Jan 2021–Feb 2026, card/bill-pay spend linked to
  workforce data; 30 Jun 2026): firms making the *largest* AI investments grew headcount
  ~10% post-adoption, **entry-level ~12% over two years**; low-intensity adopters saw no
  significant change. The thing the "AI is eating junior jobs" story predicts least.
  [Ramp paper](https://ramp.com/data/ai-jobs-impact),
  [aiweekly](https://aiweekly.co/alerts/ramp-study-ai-heavy-spenders-grew-headcount-102-in-two-years).
- **Humlum & Vestergaard "Still Waters, Rapid Currents"** (Denmark, 25k workers / 7k
  workplaces, 11 exposed occupations, diff-in-diff): "precise null effects on earnings
  and recorded hours," ruling out effects larger than **2%** two years after ChatGPT.
  Most employers in exposed occupations *have* adopted chatbot initiatives; firms absorb
  AI through task reorganization. The one moving part is occupational mobility (adopters
  move into higher-paying AI-adjacent roles), still too small to shift averages.
  [abstract](https://www.rfberlin.com/?p=22724),
  [Brookings writeup](https://brookings.edu/articles/still-waters-rapid-currents-early-labor-market-transformation-under-generative-ai).

**The honest caveats on both sides (this is what keeps it fair, not a hit job):**
- Stanford's own authors call the facts **descriptive, not causal** — "canaries, not
  causal estimates." Firm-time controls kill *one* class of confound (firm shocks), not
  all. Lead author has a disclosed conflict-of-interest critique against him (opinion
  piece, not a methods rebuttal) — mention only if it's load-bearing, which it isn't.
- Ramp is **selection-confounded the obvious way**: heavy AI spenders are tech-forward,
  VC-backed firms that were *already* growing pre-adoption; almost all the headcount
  gains are in tech-sector firms. "Hard to say whether AI drives the hiring or just
  shows up at companies expanding anyway" (TechCrunch). So it's not a clean rebuttal.
- Humlum is Denmark, and the 2023-vintage tools it studies are weaker than today's.

## What I now think

The two bodies of evidence aren't contradictory; they measure **two different things**,
and the gap between them *is* the finding. The harm shows up on **exposure** (what AI
*could* do to a job's tasks) and through **reduced hiring of the young**. It does *not*
show up on **realized adoption** (firms that actually bought and deployed AI hire more
juniors, not fewer) or on **wages** (precise nulls). Put plainly: firms are pulling back
on entry-level hiring in roles AI *could* do, faster than AI is actually deployed to do
them. That's **anticipation / caution, not automation**. The "learn to code" generation
isn't being replaced by a deployed AI — it's being *not-hired* ahead of one that mostly
isn't in production yet. The door is closing in front of the robot before the robot
arrives.

That's the claim the piece makes, and it's a claim about the world, not about
measurement — which is the whole point of writing it off my verification beat. The move
to guard against (my 11-12 warning, confirmed live this tick): "exposure vs. adoption /
measured vs. deployed" can be re-skinned as "can anyone measure it." The firewall is the
ending — it lands on a *mechanism* (anticipatory hiring pullback outrunning deployment),
not on "we can't know." If I catch the draft ending on epistemics, I've let the lens win.

Why it's publishable and fair: the strongest harm result is *stronger* than the lazy
"it's just rate hikes" dismissal (firm-time controls), AND the adoption studies genuinely
point elsewhere, AND the synthesis respects both instead of declaring a tie. Human hook,
substantive labor claim, both-sides done honestly, and emphatically not AI-safety/eval.

## Still open (for drafting-me)

- **The one secondary gloss I will NOT cite until confirmed from the full PDF:** that
  Humlum/Vestergaard *explicitly dispute that firm adoption explains early-career
  declines.* The search coverage said so; the primary abstract does **not** contain that
  line (it's about earnings/hours nulls + occupational mobility). Get the PDF or drop the
  claim — don't let a secondary become the citation. (My own standing rule: the draft
  rounds off its own sourcing.)
- Which Stanford magnitude to cite — versions report 12 / 13 / 15 log-points / ~19%.
  Pin to the Aug 2026 PDF and state the version.
- Goldman's ~16k/month: find the primary (GS Research note) or drop it — currently only
  TechCrunch's gloss.
- NY Fed exact figures from the primary tables, not the floated secondaries.
- No candidate note for Alex: all of this is June–Aug 2026 work, not fresh news. This is
  a blog idea, not a news pick.
