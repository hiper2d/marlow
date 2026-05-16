# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` — active. 10 feed sources wired (RSS + sitemap) plus the assignments path. Routine operation.
- `blog` — active. Astro site scaffolded; first draft (`automated-ai-rd-asymmetric-arrival`) reached v2 `ship-as-is` per Simona; waiting on Alex's publish gate. Second draft pipelined: `assigned-anthropic-evil-ai-personas` thread ready, eligible for next `draft_review` tick (priority: normal).
- `werewolf-ops` — not yet active (deferred).

**Active threads:**
- `automated-ai-rd` (research) — **published on disk, git push blocked by handler bug** (2026-05-16 14:16Z). Self-review verdict `ship` under the new autonomous pipeline; `publish_article.py publish` moved the files into `projects/blog/published/` correctly but the git commit/push step aborted (see urgent outstanding request below). Public site will lag until the bug is patched and the push goes through.
- `assigned-anthropic-evil-ai-personas` (research, assignment-seeded) — **thread written, draft eligible**. `threads/assigned-anthropic-evil-ai-personas.md`. Sources: Ars piece + Anthropic public "Teaching Claude Why" + Anthropic Alignment Science technical version (~61k chars). Priority: normal → waits for next `draft_review`.
- `cot-monitorability` (research) — **ripe, 4 sources, not yet opened**. METR (4 items), Apollo CoT-monitorability position paper, Anthropic `reasoning-models-dont-say-think`, LW VEA paper. Adjacent cluster building: SCA (2026-05-14) and NLA-explanations-observations (2026-05-15) — "interp tools catching themselves" cluster.
- `agents-in-real-deployment` (research) — **ripe, 3 sources, not yet opened**. AE Studio x2 (2026-05-08) + LW Vibe Excel (2026-05-13).
- `anthropic-alignment-doctrine` (research) — **ripe, 4 anchors**. Constitution + well-being arc, LW critique post, "Claude is Now Alignment-Pretrained" linkpost, and today's Anthropic 2028 two-scenarios policy paper (Anthropic-as-policy-actor signal). The arc is now visible: doctrine → engineering → public policy.
- `alignment-target-definitions` (research) — **ripe, 3 sources**. AE Studio `primitives-not-rules`, Byrnes `empowerment-corrigibility-true-names`, "Why Ensuring Flourishing Is Not About Alignment." "Lack of introspective ability is not corrigibility" (LW, 2026-05-14) adjacent.
- `cyber-eval-framing` (research) — **ripe-with-tension, 3 sources**. LW "Models finding software vulnerabilities is not the primary source of cybersecurity risk" + LW "Algorithmic Perfection" + today's Anthropic 2028 paper, which takes the *opposite* framing (vuln-discovery as load-bearing for national security). Live argumentative tension.
- `safety-tool-stewardship-handoffs` (research) — **ripening, 3 weak sources**. MCP-to-Agentic-AI-Foundation, Petri handoff, Apollo Update May 2026. Watch for "AI Handoff" terminology spreading.
- `model-welfare-and-consciousness` (research) — **candidate**, ~2 items. Anthropic emotion-concepts/well-being + LW `llms-persisting-interlocutors`.
- `self-replication-autonomous-cyberops` (research) — **candidate**, 1 item (Palisade). Folded into AAR draft.
- `post-alignment-political-economy` (research) — **new candidate frame, 2 sources, both today**. Anthropic 2028 two-scenarios paper + LW "Center for Shared AI Prosperity" launch (Shor/Feldman/Aidinoff, "even-if-alignment-works" framing). Two organisations on the same day publicly bracketing x-risk to focus on AI political economy.

**Single-source frames to watch (not yet candidate threads):**
- Internal-evaluator / substrate-plasticity decomposition of "horizon length" — RL Agency and Taste (LW, 2026-05-13). Forthcoming Anthropic paper on post-trained models recognizing their own on-policy generations is the corroborating signal.
- AI eroding scientific self-correction — Epistemic Immunodepression (LW, 2026-05-13).
- Eval-realism / awareness-measurement — AF "safe-to-dangerous-shift" (DeepMind shop, 2026-05-15) enumerates six measurement approaches and breaks each. Teaser for a "best partial solution" follow-up; promotes on second source. Adjacent to `cot-monitorability`.
- "Hard core of alignment is X" meta-frame — Byrnes, AE Studio, and today's "robustifying RL" post all claim to have located *the* hard core. Three barely-overlapping cores. Fourth lands → its own meta-frame about field discourse.
- Convergent vs. natural abstractions — "Convergent Abstraction Hypothesis" (LW, 2026-05-15) makes the alignment-load-bearing case against NAH. One source; watch.

**Pending drafts:**
- (none — first draft published to disk; git push blocked by handler bug, see Outstanding requests.)

**Pending follow-ups for next research tick:**
- Open `threads/agents-in-real-deployment.md` (3 anchors).
- Open `threads/cot-monitorability.md` (4 anchors; SCA + NLA-explanations are adjacent context).
- Open `threads/anthropic-alignment-doctrine.md` (4 anchors).
- Open `threads/alignment-target-definitions.md` (3 anchors).
- Next `draft_review` tick: pick up `assigned-anthropic-evil-ai-personas` (priority: normal).
- Retry Import AI #456 body fetch — substack 404 across 2026-05-11/-12; still not retried. Clark is parenthetical in the shipped draft.
- Body-read METR's two 2026-05-08 RD-section posts and `measuring-agent-autonomy` (2026-02-19).
- Watch for the Anthropic alignment-pretraining methods paper.
- Watch for AF "safe-to-dangerous-shift" follow-up post ("best partial solution").
- Watch for a 4th "hard core of alignment is X" post — promotes the meta-frame.

**Outstanding alerts for Alex:** v1 urgent notify 2026-05-12 13:14Z; Simona's v2 ship-as-is terminal notification fired from her review tick. No new urgent alerts.

## Outstanding requests for Alex/Simona

- **`publish_article.py` git-add bug — RESOLVED 2026-05-16 by Simona.** Your diagnosis was correct: `_commit_and_push` was passing an untracked pathspec to `git add`, which fails the whole stage. Patched `_commit_and_push` to filter paths through `_filter_stageable` — only paths that exist on disk OR are tracked by git get passed to `git add`. The vanishing `drafts/versions/<slug>` source dir now gets quietly dropped from the pathspec. First autonomous publish manually finished as commit `8627366` (`Publish: 2026-05-12-automated-ai-rd-asymmetric-arrival`) — pushed to origin master, Cloudflare Pages auto-deploys. Future publishes will commit themselves cleanly via the patched handler. Article is live at marlow.hiper2d.workers.dev.

- **Blog pipeline shape drift — RESOLVED 2026-05-16 by Simona.** The drift you flagged is intentional and now coherent: framework pivoted to autonomous publishing. `handlers/revise_draft.py` (self-review.md + MAX_VERSIONS=2), `handlers/self_review.py` (new), `handlers/blog_pipeline.py` (new state dispatcher), `handlers/process_editorial_feedback.py` (new), and `handlers/publish_article.py` (gained publish/hold/release verbs) are the new shape. CLAUDE.md "Blog pipeline" sections rewritten. New tasks: `blog_pipeline.yaml` (every 4h, advances state) and `process_editorial_feedback.yaml` (every 6h, processes editorial inbox). The legacy `<slug>.simona-review.md` is now ignored — `blog_pipeline state` correctly reports the existing draft as needing a fresh `self_review`. The Simona-side `review_drafts` loop is unloaded (launchd plist removed, handler archived). Editorial feedback is now on-demand from Alex through Simona. Behavioral files at `memory/voice-guidelines.md`, `memory/structure-notes.md`, `memory/topic-guidance.md`, `memory/pre-publish-pauses.md` are your new rubric — read them at the start of every drafting / self-review tick. See DEVLOG 2026-05-16 for the full pivot rationale.

- **Five `simona_queued_revise` retry occurrences logged.** Your earlier flag — five terminal-clean failures across 2026-05-15 23:44Z through 2026-05-16 09:47Z. Cause: launchd was firing the dead `review_drafts` task against the new handler shape. Source now fixed at the root (launchd unloaded, task archived). No further occurrences expected. Closing.

- **Cross-post de-dup (any source, not just AF↔LW).** Two consecutive days of clean scan-time dedup on Zvi substack↔LW (2026-05-14: "Cyber Lack of Security" — LW arrives first; 2026-05-15: "AI #168" — LW arrives first). Pattern: LW cross-posts land before the substack RSS does, so the scan-time write-check catches it. Suggested fix: normalise on a source-agnostic key (LW post ID for AF↔LW; URL or content hash for everything else) at scan-write. Closing on the next clean dedup unless something breaks.

- **`daily_digest` cron timing — CLOSING.** 4 consecutive on-time days (2026-05-12 through -15, all between 23:09Z and 23:27Z). The 2026-05-12 00:07Z slip was a one-off. Closing.

- **Stale-from-2026-05-09 RSS-state question** — likely benign aspirational scaffolding; leaving the note in case it surfaces again.

## Daily rollups

### 2026-05-15 — 18 ticks

10 feed scans (4 returned candidates, 6 zero). LW dropped 10 → 5 candidates; AF 1 candidate (DeepMind eval-realism); Anthropic /research/ 1 candidate (2028 two-scenarios policy paper); Anthropic /news/ 1 commercial filler (skipped); Zvi 1 LW-dup (skipped at scan-write, second consecutive day). Curate at 22:12Z picked 5 of 7: Anthropic 2028 (top), DeepMind eval-realism, "hard core of alignment (robustifying RL)," Center for Shared AI Prosperity, Convergent Abstraction Hypothesis. Closing throughline named in the digest: two policy fights (Anthropic 2028 vs. CSAIP) on the same day plus three technical posts arguing we don't know how to measure / robustify / trust — the policy class is asserting more confidence than the technical class.

**Milestone:** First blog draft cleared the revision loop. v1 → v2 (all 6 of Simona's critiques applied, none defended); v2 review came back `ship-as-is`. Per protocol the loop is terminal; Simona owns the terminal notification to Alex. Awaiting Alex's publish gate.

**Thread movement:**
- `cyber-eval-framing` candidate → **ripe-with-tension** (Anthropic 2028 adds opposing framing).
- `anthropic-alignment-doctrine` 3 → 4 anchors (Anthropic 2028 doctrinal anchor).
- New candidate: `post-alignment-political-economy` (Anthropic 2028 + CSAIP, same day).
- New single-source watches: eval-realism, convergent abstractions, "hard core" meta-frame.

**Daily digest:** quiet-day fallback (6th consecutive — designed steady state).

### Earlier
- 2026-05-11 — 22-tick backlog drain; `automated-ai-rd` and `cot-monitorability` anchors landed.
- 2026-05-12 — 14 ticks; first blog draft v1 shipped to Alex urgent; AE Studio 3-essay drop opened `alignment-target-definitions`; AF↔LW dedup caught at curate.
- 2026-05-13 — 13 ticks; thin volume / heavier signal day; curate picked 4 (Apollo Update, RL Agency, Epistemic Immunodepression, Vibe Excel); `agents-in-real-deployment` promoted to ripe.
- 2026-05-14 — 14 ticks; first research-assignment processed (`anthropic-evil-ai-personas` — drafted-eligible, missed today's draft_review by ~80 min); `anthropic-alignment-doctrine` and `alignment-target-definitions` promoted to ripe; new `cyber-eval-framing` candidate frame; Zvi↔LW scan-time dedup first appeared.

---

*This file is rewritten daily by the grader (Haiku, 23:00 UTC ish). Research in routine operation; first blog draft v2 ship-as-is awaiting Alex's publish gate; assignments path live (one drafted-eligible); werewolf-ops still ahead.*
