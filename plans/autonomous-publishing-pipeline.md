# Plan: Autonomous publishing pipeline

**Status:** Proposed 2026-05-15. Awaiting execution in a fresh session.

## Goal

Marlow becomes a fully autonomous writer-publisher. She drafts, self-reviews, and publishes without an external review gate. Simona's role shifts to **retrospective editorial review on Alex's demand**, with feedback that shapes Marlow's future behavior — not feedback that revises past articles.

## Why now

- Cost: the launchd-driven Simona review loop burns API budget on every tick. Moving editorial review into Alex's interactive Claude Code sessions captures the high-signal feedback at zero marginal API spend.
- Simplicity: the current pipeline has accumulated bugs (stuck-loop detection, requeue on stale failures, handler logic patching the symptoms instead of the design). Cleanest fix is removing the back-and-forth entirely.
- Honest division of labor: Marlow is the writer. She owns her drafts, her quality bar, and her publish decisions. Simona is an editor who shows up periodically with notes on the body of work, not a gate on every piece.
- You can't unpublish. So review should improve the *next* batch, not the last batch.

## Target pipeline

### Marlow's autonomous loop
1. Marlow drafts an article on her own cadence.
2. Marlow runs a **single self-review pass** against voice and quality criteria.
3. Pass → publish. Fail → one revision pass → publish. No further loops, no v2/v3, no escalation queue.
4. Marlow logs the publish to her own publication history.
5. Before drafting her next article, Marlow checks her **editorial feedback inbox** (see below) and processes anything new.

### Editorial review (manual, on-demand)
1. Alex asks Simona: "how is Marlow doing" or "review Marlow's work since last time."
2. Simona reads Marlow's recent published articles + DEVLOG + any self-notes Marlow flagged.
3. Simona drafts editorial feedback in the chat: what's working, what's drifting, suggested adjustments.
4. **Alex and Simona discuss the feedback before sending.** Alex can soften, sharpen, add, drop, or veto individual points. This is collaborative editing, not Simona handing down decrees.
5. When both agree, Simona writes the final feedback to Marlow's inbox file.
6. Next time Marlow runs, she processes the inbox (see below) and updates her own behavioral files. The article history isn't touched — feedback shapes the *next* writing cycle.

### Marlow ingesting feedback
Marlow gets a new handler — `process-editorial-feedback`. It runs at the start of each writing session, before drafting. Behavior:
- Read every file in `memory/feedback-inbox/`.
- For each piece of feedback, classify it: voice issue, topic issue, structural issue, habit issue, or other.
- Update the corresponding behavioral file in `memory/`:
  - Voice issues → `memory/voice-guidelines.md`
  - Topic preferences → `memory/topic-guidance.md`
  - Structural patterns → `memory/structure-notes.md`
  - Habits to start or stop → `memory/working.md` or a dedicated habits file
- Log what was changed and why in `DEVLOG.md` under a new section.
- If she disagrees with a piece of feedback, note that explicitly in DEVLOG instead of applying it. Editorial pushback is allowed and gets recorded.
- Move the processed inbox file to `memory/feedback-archive/YYYY-MM-DD-editorial.md`.

The point: she decides how to internalize the feedback. We give her editorial intent; she translates it into her own rules. This preserves her autonomy and creates a real audit trail of how her behavior evolves.

## Marlow-side changes (in `~/projects/marlow/`)

- [ ] **Add self-review handler.** Single critique pass before publish. Voice + quality criteria. Output: pass or revise.
- [ ] **Add single-revision logic.** On self-review fail, do one revision pass and publish regardless of second-pass result (flag in DEVLOG if still uncertain). No infinite loops.
- [ ] **Add publish handler.** Marlow decides publication timing herself.
- [ ] **Add `process-editorial-feedback` handler.** Runs at start of each writing session. Inbox → classify → update behavioral files → DEVLOG → archive.
- [ ] **Create the feedback directory structure**: `memory/feedback-inbox/` and `memory/feedback-archive/`. Empty initially.
- [ ] **Create initial behavioral files** if they don't exist: `memory/voice-guidelines.md`, `memory/topic-guidance.md`, `memory/structure-notes.md`. Seed with whatever's already implicit in Marlow's framework so feedback has somewhere to land.
- [ ] **Remove `review_drafts` handler.** Dead path.
- [ ] **Remove stuck-loop detection** specific to the review flow. Keep general handler hygiene.
- [ ] **Remove requeue-on-failure logic** that caused today's bug. Replace with "log and move on" semantics.
- [ ] **Update Marlow's framework docs** (`README.md`, `CLAUDE.md`, working memory) to reflect autonomous publish + retrospective feedback model.
- [ ] **Update `DEVLOG.md`** with the pivot.

## Simona-side changes (in `~/projects/simona-ai-computer-operator/`)

- [ ] **Remove the launchd plist** for the Marlow monitoring tick. Document the removal in commit message and the simona CLI docs.
- [ ] **Remove or archive scheduled monitoring scripts** that drove the automated review loop.
- [ ] **Leave `tasks/` archive intact** — historical review_pending files stay as audit trail; no new ones get written.
- [ ] **Add a Marlow editorial review skill** at `.claude/skills/marlow-review/SKILL.md`. Triggered when Alex asks "how is Marlow doing," "review Marlow's recent work," or similar. Workflow:
  - Pull Marlow's recently published articles
  - Pull her DEVLOG entries since last editorial review
  - Pull any self-flags she emitted (uncertainty notes, deferred decisions)
  - Draft structured feedback in chat: what's working, what's drifting, suggested adjustments
  - **Pause for discussion with Alex.** Don't write the inbox file yet.
  - On Alex's "go," write the agreed-on feedback to `~/projects/marlow/memory/feedback-inbox/YYYY-MM-DD-editorial.md`.
- [ ] **Update CLAUDE.md** in simona repo to reflect new on-demand review pattern.
- [ ] **Revise the feedback memory** (`feedback_marlow_review_authority.md`): the rule shifts from "Simona reviews via the automated pipeline" to "Simona reviews on-demand, drafts feedback for discussion with Alex, then writes the finalized feedback to Marlow's inbox."

## Open decisions for Alex

1. **Self-review hold threshold.** What does Marlow do if her self-review still flags concerns after one revision? Options: (a) publish anyway and flag in DEVLOG for next editorial review, (b) hold the draft in a "uncertain" queue she surfaces at next review, (c) never publish uncertain drafts. I'd default to (a) — bias toward shipping, let editorial reviews catch drift.

2. **Editorial review cadence reminder.** Fully on-demand from Alex, or does Marlow include a gentle "it's been N days since last editorial review" in her status reports when Alex pings her? I'd lean toward the embedded reminder, not active nagging.

3. **Pre-publish guardrails.** Any topic categories Marlow should never publish autonomously without explicit approval (e.g., naming a specific real person negatively, financial-advice-shaped content, anything political)? Worth defining a short "always pause and ask" list so a hallucination crisis can't ship something embarrassing. This is a small exception list, not a return to gating.

4. **Behavioral file granularity.** How many separate behavioral files should Marlow maintain? Voice / topic / structure is a starting cut. Could also have habits, taboos, recurring patterns. Start with three and let Marlow create more as feedback accumulates? Or define the full set up front?

## Success criteria

- Zero automated review API calls after rollout.
- Marlow publishes at least one self-reviewed article without manual intervention.
- One full editorial review cycle: Alex asks, Simona drafts, they discuss, inbox file written, Marlow processes it, behavioral files updated, DEVLOG reflects the changes.
- The processed inbox file shows up in the archive cleanly.
- No regressions in voice/quality on the first batch of post-feedback articles.

## Execution notes for the next session

- Marlow changes are the bulk of the work. Touch Simona side only after Marlow's pipeline is functional — don't leave the launchd process running against a half-built handler chain.
- Order of operations:
  1. Create the feedback inbox/archive directory structure and seed behavioral files.
  2. Implement `process-editorial-feedback` handler.
  3. Implement self-review + single-revision + publish handlers.
  4. Dry-run on a draft to confirm the new pipeline works end-to-end.
  5. Disable and remove the launchd plist on the Simona side.
  6. Delete the now-dead review handlers in Marlow.
  7. Add the Simona-side `marlow-review` skill.
  8. Update docs (READMEs, CLAUDE.md files, DEVLOG, memory).
  9. Revise the simona memory entry on review authority.
- Commit cadence: one commit per logical step in Marlow, one cleanup commit in Simona for the launchd removal. Remember: git is run in Marlow, not in the simona repo — Alex commits Simona changes himself.

## Quick mental model

- **Marlow**: writes, self-reviews once, revises once if needed, publishes. Reads her editorial inbox before each writing session and grows accordingly.
- **Simona**: pulls Marlow's recent work when Alex asks, drafts editorial notes, discusses with Alex, drops the final notes in Marlow's inbox.
- **Alex**: triggers editorial reviews on his own cadence, co-edits the feedback before it's sent, occasionally patches Marlow's framework when something deeper needs fixing.
