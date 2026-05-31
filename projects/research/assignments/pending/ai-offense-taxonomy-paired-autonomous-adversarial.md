---
slug: ai-offense-taxonomy-paired-autonomous-adversarial
assigned_by: simona
assigned_at: 2026-05-31
priority: normal
angle: |
  Re-seed of the rejected ai-paired-ctf-bsides-tampa-2026 assignment. The
  original draft (paired-autonomous-adversarial, rejected 2026-05-31)
  overlapped almost entirely with Alex's own now-published firsthand post —
  same weekend, same 6/61 result, same XBOW / Check Point-Skynet / classifier
  anchors, same competence-floor-vs-ceiling point. A retread with less detail
  and a borrowed vantage. Don't write that piece again.

  The ONE original contribution in the rejected draft was the taxonomy:
  "AI vs human" is the wrong axis for AI-in-offensive-security; the live axis
  is *paired vs autonomous vs adversarially-designed-against*. Build the new
  piece around that frame alone. It is an analysis essay, not a war story.

  Crucial change of stance: Alex has already published the firsthand account
  (the CTF weekend, the exploit walkthroughs, the classifier friction). So you
  do NOT re-narrate the session. You CITE his post as the paired-quadrant
  exemplar and spend your words on the taxonomy:

    - Paired — human + 1-2 model sessions; human does scope, ferries state
      across context windows, picks tools the model doesn't reach for, absorbs
      platform-policy friction. Exemplar: Alex's BSides post (link it).
    - Autonomous — full pipeline, model as one component among validators /
      scope ingestion / dedup, operating under its own platform policy.
      Exemplar: XBOW #1 on HackerOne.
    - Adversarially-designed-against — targets built to confuse, manipulate, or
      refuse AI tooling specifically. Leading edge: Check Point's Skynet
      prompt-injection-in-malware sample. Clumsy now; a discipline within
      18-24 months. CTF authors are ~12-24 months behind malware on this curve.

  The contrarian payload: capability is settled (XBOW closed it on web bugs 18
  months ago; a weekend pair closed it on competition puzzles). What's
  unsettled is which SHAPE matters where, and which shape each new data point
  actually belongs to. The taxonomy is a thinking tool defenders can use; "AI
  vs human" is not. End on what defenders should do differently given the three
  shapes (design the wrapper, not just the model; plan for the floor-vs-ceiling
  talent reshape; the next contest is adversarial design).

  Voice: analytical, skeptical, specific. This is the essay the rejected draft
  should have been once Alex's post existed to carry the firsthand weight.
  Shorter than the rejected draft — 1200-2000 words. You're not re-proving AI
  works; you're giving the discourse a better axis.
deadline: null
outcome: null
---

## Why this

The discourse on AI in offensive security is stuck on "can AI do offense / will
it replace humans." That question closed ~18 months ago (XBOW autonomous #1 on
HackerOne; a 2026 weekend pair placing 6/61 at a community CTF whose organizers
said AI "wouldn't help"). Arguing the dead question is satisfying and the
evidence cuts cleanly, so most writing keeps doing it. The live edge is messier
and nobody's giving it a usable frame.

This piece supplies the frame: *paired / autonomous / adversarially-designed-
against* as the axis that replaces "AI vs human." It's the one genuinely
original idea from the rejected draft, lifted out of a piece that otherwise
duplicated Alex's firsthand post.

The pivot that makes this work: Alex's firsthand account is already public, so
Marlow doesn't need to (and shouldn't) re-tell the weekend. She cites it as the
paired-quadrant exemplar and spends her words on the taxonomy and its
implications. This also dissolves the three sensitivities that forced the
original draft to hold — Alex's professional identity, the classifier-workaround
narrative, the Mythos mention all live in *his* published post now, linked
rather than paraphrased. The earlier hold-for-review instruction does not carry
over; this version routes through the normal pipeline.

## Seed materials

**Primary (public) — the firsthand exemplar to CITE, not retell:**

- Alex's published post: "CTF. Everyone was using AI. So I brought mine."
  (`~/projects/blog/posts/2026-05-23-ai-paired-ctf-bsides-tampa.md`, slug
  `ai-paired-ctf-bsides-tampa`, published 2026-05-23 on Alex's personal blog).
  This is the paired-quadrant exemplar. Link it; quote at most a line or two;
  do not reproduce the exploit walkthroughs.

**External anchors (fetch / re-confirm):**

- [The road to Top 1: How XBOW did it](https://xbow.com/blog/top-1-how-xbow-did-it)
  — autonomous-quadrant exemplar. ~1,060 submissions, ~130 resolved + 303
  triaged, 90 days, no human in loop.
- [In the Wild: Malware Prototype with Embedded Prompt Injection](https://research.checkpoint.com/2025/ai-evasion/)
  (Check Point Research, 2025) — adversarially-designed-against leading edge.
  The "hundreds of AI audit escape techniques" closing line is the load-bearing
  quote.
- One DEF CON / Black Hat 2024-2025 talk on AI-augmented red teaming or
  AI-aware CTF design (Brendan Dolan-Gavitt is the named prior-art lead,
  referenced in XBOW's writeup). Cite to ground "this isn't novel," or claim
  the novelty harder if the public record is thin.

## Things to look for

- The taxonomy has to do real work, not just label three things. For each
  concrete data point (Alex's weekend, XBOW, the Skynet sample), name which
  quadrant it sits in AND what that placement predicts. A taxonomy that only
  sorts is decoration; one that predicts is a tool.
- Steelman the boundaries. Paired and autonomous aren't clean categories — a
  paired setup with heavy tooling shades into autonomous. Say where the line
  actually is (platform policy? human-in-loop on scope? state-ferrying?) rather
  than pretending it's crisp.
- Don't overclaim the adversarial-design timeline. It's real in malware (one
  clumsy sample), not yet in CTFs. Frame as "here's what it'll look like,"
  with the Skynet sample as the existence proof, not "this is happening at
  scale."
- The competence-floor-vs-ceiling point is good but it's Alex's already-public
  territory now — use it as a brief defender-implications beat, not the spine.
- Topic-rotation note: this is a cybersecurity piece, a deliberate break from
  the Anthropic-orbit alignment-discourse run of the last three published
  articles. That's a feature — don't drift it back toward safety-research
  framing.
