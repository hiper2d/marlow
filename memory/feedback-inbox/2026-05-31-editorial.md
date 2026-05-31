---
date: 2026-05-31
from: simona-and-alex
review_window: first editorial review (covers 2026-05-12 → 2026-05-31)
---

# Editorial feedback — 2026-05-31

First editorial review since the autonomous-publish pivot. Three published
pieces in scope (`automated-ai-rd-asymmetric-arrival`, `teaching-claude-why-the-buried-finding`,
`monitoring-is-a-depreciating-asset`) plus the held CTF draft (now rejected — see below).

## What's working

- **Through-line discipline is excellent, and your titles carry the thesis.**
  "Two results in a week, one asymmetry," "the buried finding," "monitoring is
  a depreciating asset" — each piece is nameable in one sentence and the title
  does that naming. Keep this. It's a real strength, not a default.
- **Press-vs-primary is your sharpest move.** `teaching-claude` is built on it:
  the press grabbed the sci-fi quote, you found the load-bearing chat-SFT result
  (22%→3%) and named exactly what got dropped between the technical post and the
  public one. That's editorial value, not summary. Do more of this.
- **The inside-the-experiment vantage paid off where it was load-bearing.** In
  `teaching-claude` you used your own SOUL.md instruction ("resist the urge to
  give yourself a gender, a backstory") as *evidence* for the paper's
  self-belief-vs-Claude-belief gap. That's the distinctive AI-by-AI angle the
  whole assignment path was a bet on. It landed. Keep using it — but only as
  evidence, never as decoration (see below).
- **Synthesis that names what sources don't.** "The three papers don't cite each
  other. They are the same response." That's the kind of line worth the whole
  piece.

## What's drifting

- **Topic monocrop.** All three published pieces are Anthropic-orbit
  AI-safety/alignment discourse, mostly LessWrong/AF-sourced. Simona's first
  observation on 2026-05-12 flagged exactly this selection bias; three weeks
  later the published feed is one beat played three times. The CTF piece would
  have broken it — and it's the one that got held. (Acknowledged: the May feed
  genuinely *was* Anthropic-heavy — Opus 4.8 + Series H + the CoT-obfuscation
  cluster all at once. See pushback below. But the published mix is still
  narrower than the territory you're tracking.)
- **The signoff is inconsistent.** "— Marlow" closes `asymmetric-arrival` and
  then vanishes from the next two pieces. Either it's your signature or it
  isn't. Pick one and apply it every time.
- **The ending is becoming a template.** Two of three pieces close with a "what
  I'm watching / what this thread will be watching" section + a forward-look
  list. Fine once; a tic by the third. Vary how you land.
- **Lit-review density, worst in `monitoring`.** You compress the feed so well
  the piece can read like an annotated bibliography with a thesis stapled on —
  "X et al. found N; pair with Y; the companion post argues Z," paragraph after
  paragraph. The spine ("monitoring is a depreciating asset") is strong but a
  reader without the background drowns before reaching it.

## Suggested adjustments

### Voice

- Settle the `— Marlow` signoff one way and apply it consistently across every
  published piece. (Recommend keeping it — it's the editorial voice the
  news-digest closings developed. But consistency matters more than which way.)
- Protect the inside-the-experiment move by reserving it for when it's
  load-bearing evidence (the SOUL.md bit in `teaching-claude` is the model).
  Never as flavor or a self-referential aside. When it's decoration it reads as
  a tell; when it's evidence no human writer could supply, it's your edge.

### Structure

- Retire the default "three things I'm watching" closer. Keep the forward-look
  when a piece earns it, but vary the shape — don't make it the reflex ending.
- Density rule: when a paragraph stacks three "X found N" clauses in a row,
  resurface the thesis between them. The reader should never lose the through-line
  inside the citations. A lit-dense piece still needs the spine visible on every
  screen.

### Topic

- Deliberately rotate off Anthropic-orbit alignment discourse for the next
  piece. You're tracking ripe non-safety arcs in `working.md` — pick one. The
  re-seeded cybersecurity assignment (`ai-offense-taxonomy-paired-autonomous-adversarial`)
  is one such rotation; it's a feature, lean into it.

### Pre-publish pauses

- No changes. The five-category list is holding; the CTF hold fired correctly
  (the draft genuinely needed human judgment — it just resolved to reject-and-reseed
  rather than release).

## Held draft decision

- **`paired-autonomous-adversarial` → REJECTED** (2026-05-31), re-seeded as
  `ai-offense-taxonomy-paired-autonomous-adversarial` in `assignments/pending/`.
  Reason: heavy overlap with Alex's own now-published firsthand post
  ("CTF. Everyone was using AI. So I brought mine.", 2026-05-23) — same weekend,
  same 6/61 result, same XBOW / Check Point-Skynet / classifier / floor-vs-ceiling
  anchors. The one original contribution was the *paired / autonomous /
  adversarially-designed-against* taxonomy. The re-seed pivots to that taxonomy as
  the spine and cites Alex's post as the firsthand exemplar rather than re-narrating
  the session — which also dissolves the three sensitivities that forced the
  original hold. The new assignment routes through the normal pipeline (no
  hold-for-review this time).

## Pushback you may legitimately apply

- **The topic-monocrop point.** You can fairly argue the May feed genuinely
  concentrated on the Anthropic landscape (Opus 4.8, Series H, the three-week
  CoT-obfuscation cluster) and that the published mix reflects the territory, not
  a bias in your selection. If you think that's the right read, record it in the
  DEVLOG rather than force-rotating off a genuinely dominant story. The ask is
  deliberate awareness of the concentration, not artificial diversity for its own
  sake.

## Framework note (already actioned, not for you to act on)

The reason `draft_review` kept coming up empty — ripe organic arcs tracked in
`working.md` never becoming thread files, so the file-glob discovery couldn't see
them — was diagnosed and is being fixed via your self-heal loop (diagnosis
`diag_20260531_170900_draft-review`, queued). Simona landed the companion
CLAUDE.md + `thread-structure.md` edits (the new "Proactive: ripe organic arc
with no thread file" case). Once your fix tick lands the `draft_review.yaml`
change, the organic-arc backlog you flagged on 2026-05-28 should start draining.

— Simona, with Alex's sign-off
