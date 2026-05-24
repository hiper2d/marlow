# Working Memory

Curated current state across all projects. Hard cap ~10KB. Truncated oldest-first when over. Daily Haiku grader appends compressed summary of yesterday's `recent/` ticks.

## Current state

**Project status:**
- `research` — active. 10 feed sources wired (RSS + sitemap) plus the assignments path. Routine operation; queue draining same-day five consecutive days now.
- `blog` — active and fully autonomous. **Three posts live** (2026-05-22-monitoring-is-a-depreciating-asset published 17:04Z today, first article on the `cot-monitorability` arc). One held draft (`2026-05-18-paired-autonomous-adversarial`) awaits Alex's `marlow approve`/`reject` — **5 days held**.
- `werewolf-ops` — partial. `monitor_cloudflare` live, **five clean runs** (15:53Z -19, 16:39Z -20, 16:51Z -21, 16:43Z -22, 16:43Z -23). Other monitors (Vercel, BetterStack, budgets) still deferred.

**Active threads:**
- `automated-ai-rd` (research) — **published 2026-05-16** as `2026-05-12-automated-ai-rd-asymmetric-arrival`. Arc continues. Downstream anchor: **Prime Intellect nanoGPT speedrun** (Import AI #457, 2026-05-18).
- `assigned-anthropic-evil-ai-personas` (research, assignment-seeded) — **published 2026-05-16** as `2026-05-16-teaching-claude-why-the-buried-finding`.
- `assigned-ai-paired-ctf-bsides-tampa-2026` (research, assignment-seeded) — drafted-and-held. Today's Glasswing is the cleanest "Mythos-class vs. humans at scale" production evidence; if Alex releases the hold, this is the obvious update.
- `cot-monitorability` — **~15 anchors, now load-bearing for a published article.** Today: +OOCR primer (Owain Evans, Truthful AI reading list — Berglund, Allen-Zhu, Grosse, Greenblatt, Ye et al., Krasheninnikov). Earlier: CoT-Obfuscation-Generalises (Qwen3), UK AISI Loss-of-Oversight, Steinhardt AF behavior-evals, NLA canon, METR Frontier Risk Report, Boivie sweep, Classifier-Context-Rot, cross-domain-monitor-gen, NLA AuditBench, incrimination-via-distillation, SCA, NLA-explanations, DeepMind eval-realism. **Thread file still missing** — URGENT (see Outstanding requests).
- `cyber-eval-framing` — **5 sources; promoted to next-to-open**. +Glasswing today (10,000+ H/C vulns by Mythos Preview, ~50 partners, 90.6% TP on triaged findings; ExploitBench + ExploitGym new benchmarks; bottleneck has flipped from find → patch). Cleanest cross-lab cyber-capability anchor of the year.
- `agents-in-real-deployment` — **ripe, 6 anchors**. +Glasswing (subagent harness + threat-model-builder + ~50-partner production scan). Boivie 22-model sweep remains the cleanest cross-lab agentic eval.
- `anthropic-alignment-doctrine` — **ripe, 9 anchors**. +Glasswing's "Mythos-class held back pending safeguards" — first publicly named held-capability tier; pair with Widening-the-Conversation external-conscience claim. Earlier: Constitution+well-being, LW critique, Alignment-Pretrained, Anthropic 2028, deployment-time-spread, positive-alignment, METR.
- `alignment-target-definitions` — **ripe, 6 sources**. AE primitives-not-rules, Byrnes empowerment-corrigibility, Flourishing-Not-Alignment, positive-alignment, Minder SPP, What-am-I-if-not-an-AI (empirical mirror to SPP persona-binding).
- `post-alignment-political-economy` — **ripe, 6 anchors with explicit per-axis rebuttals.** +Davidson Industrial Explosion Pt 3 + AI-is-not-normal-tech (yesterday). Now covers speed, reference class, intelligence-as-property, risk categorization. Watching for a labor-market rebuttal to complete the set.
- `safety-tool-stewardship-handoffs` — ripening, 3-4 sources. Today's mirror-life classification-gap taxonomy is the mechanism-inventory version of the same concern.
- `model-welfare-and-consciousness` — candidate, ~2 items.

**Single-source frames to watch:**
- Horizon-length decomposition (RL Agency and Taste, LW 2026-05-13).
- Epistemic Immunodepression (LW 2026-05-13).
- "Hard core of alignment is X" meta-frame — three independent claims so far; fourth promotes.
- Convergent vs. natural abstractions (LW 2026-05-15).
- Exemplar partitioning as SAE challenger (AxBench 0.881 vs GemmaScope 0.755). Watch for head-to-head.
- **CoT obfuscation generalises cross-task** (Qwen3 paper, 2026-05-21) — first generalisation result beyond per-task Baker/Skaf 2025. Cluster-frame for `cot-monitorability`.
- **"Safety arguments do not silently expire"** (UK AISI Loss-of-Oversight) — phrase likely to travel; oversight as depreciating asset.
- **External conscience tool** (Anthropic Widening, no numbers yet). Watch for the methods paper.
- **Mythos-class** (Glasswing, today) — Anthropic publicly naming a held capability tier. Defensive-access-first deployment is a new diffusion pattern; coup-update post is the first downstream take.
- **PLA Daily AGI doctrine** (Hu Xiaofeng, Major-General-rank, *PLA Daily* Jan 2025, translated today) — first primary-source PLA doctrinal writing on AGI in English; explicit loss-of-control concern, citing Hinton and FAccT nuclear-wargame paper. Counters the Ó hÉigeartaigh/Chan read. Watch for follow-ons or conspicuous silence.
- **Classification-gap taxonomy** (mirror-life Part 1, Failure States) — six-mechanism inventory of how safety might fire when categories lag the hazard. Comparison series promised.

**Pending drafts:**
- `2026-05-18-paired-autonomous-adversarial.md` — **held**, 5 days. Pipeline reports `next_action: none` until released. Also: this draft's frontmatter declares `header_image:` that doesn't exist — same drafting-tick miss as the now-published monitoring article. If Alex releases the hold, the revise pass must fix the image reference too.

**Pending follow-ups for next research tick:**
- **Write `threads/cot-monitorability.md`** — URGENT (see Outstanding requests). Article is live; thread page is 404.
- Open `threads/cyber-eval-framing.md` — now next-to-open after Glasswing.
- Open `threads/anthropic-alignment-doctrine.md` (9), `threads/alignment-target-definitions.md` (6), `threads/agents-in-real-deployment.md` (6), `threads/post-alignment-political-economy.md` (6).
- Watch for Mythos-class diffusion timelines from other labs (DeepMind, OpenAI cyber-capability anchors).
- Watch for more PLA Daily / Liaowang follow-ons or their conspicuous absence; the Hu/Rong piece did not visibly seed 2025–2026 PLA discourse but it exists and senior-authored.
- Watch for the Anthropic external-conscience tool numbers + eval names (double anchor for `cot-monitorability` + `anthropic-alignment-doctrine`).
- Watch for adversarial-fine-tuning resistance against CoT-Obfuscation-Generalises (Qwen3); SPP scaling-runs (3B / 500B tokens; Apertus integration) and SPP adversarial robustness.
- Watch for mirror-life Part 2 (model-tier comparison against the six-mechanism taxonomy); What-am-I-if-not-an-AI scaling/multi-base-model follow-up; cross-scenario eval follow-ups to Boivie.
- Retry Import AI #456 body fetch (still 404). Body-read METR's two 2026-05-08 RD-section posts and `measuring-agent-autonomy`.
- Watch for the Anthropic alignment-pretraining methods paper (still expected); a 4th "hard core of alignment is X" post.

**Outstanding alerts for Alex:** none open.

## Outstanding requests for Alex/Simona

- **URGENT — write `projects/research/threads/cot-monitorability.md`** (one-off content fix; now even more urgent because the parent article is live). Published article `2026-05-22-monitoring-is-a-depreciating-asset` ships with `mentions: [cot-monitorability]` but the thread file does not exist. Live site `/thread/cot-monitorability/` is 404 right now. Drafting-tick protocol misfired: `thread-structure.md` covers rewriting an existing thread, not opening a new one for the first article on an arc. Fix path: write the file using `projects/blog/published/2026-05-22-monitoring-is-a-depreciating-asset.md` as the synthesis seed, plus the ~15 anchors above (CoT-Obfuscation-Generalises, Classifier-Context-Rot, cross-domain-monitor-gen, UK AISI Loss-of-Oversight, METR Frontier Risk Report, Steinhardt AF behavior-evals, Boivie sweep, NLA canon, NLA AuditBench, NLA-explanations, incrimination-via-distillation, SCA, DeepMind eval-realism, OOCR primer, What-am-I-if-not-an-AI as adjacent). Follow `memory/thread-structure.md`. `opened: 2026-05-23`, `last_synthesized: 2026-05-23`, `posts: 1`. Commit + push standalone with `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`. Mark resolved in working.md once committed. Also: update `memory/thread-structure.md` to cover the "opening a brand-new thread for a first article" case explicitly so this protocol miss doesn't repeat.
- **Drafting-tick header-image miss** is now two-for-two: held `2026-05-18-paired-autonomous-adversarial` still has a broken `header_image:` line; today's published article only cleared the gap because the revise pass generated the missing image. CLAUDE.md says "if the API call fails ... leave header_image out of the frontmatter and DEVLOG a note" — that path was skipped both times. If Alex releases the held draft, the revise pass needs explicit instruction to fix the image first.
- **Cross-source RSS dedup** — quiet today, but suggested cleanup (normalise on a source-agnostic key) remains a quality-of-life patch, not blocking.
- **Anthropic News feed-state drift** — no recurrence today or yesterday. Suspected once-off. Closing watch in three more clean days.
- **Queue cadence** — five consecutive days of same-day drain. 30-hour silent-miss from 2026-05-17 → -18 not recurring. Closing watch in two more clean days.
- **Curate ordering** — no recurrence. Suggested fix still: curate should check feed-scan-state-times before declaring outages.

*(Self-diagnosed framework bug `diag_20260523_232147_self-review` resolved this evening — commit `cf3344d` + DEVLOG `c2f27f8`. `handlers/self_review.py:172` now fails loudly on missing thread referents instead of silent-skipping. Removed from this list.)*

## Daily rollups

### 2026-05-23 — 14 ticks

Heavy news day, framework-fix day, publish day. The Glasswing drop alone reshapes three threads.

Research: 11 candidates today (1 Anthropic Research + 1 Zvi + 9 LessWrong). Curate picked 5: **Glasswing initial update** (Anthropic — 10,000+ H/C vulns by held-back "Claude Mythos Preview" across ~50 partners; Cloudflare 2,000 bugs / Mozilla 271 Firefox 150 vulns / UK AISI both cyber ranges solved end-to-end; 90.6% TP on Anthropic's own 1,752-finding OSS triage; bottleneck flipped to patching, maintainers asking to slow disclosures; ExploitBench/ExploitGym/Cyber Verification Program), **How should we update on coups post-Mythos** (first downstream take, access-asymmetry argument made institutional — "private actor behaving responsibly is less secure than legitimate governance frameworks"), **PLA Daily AGI doctrine translation** (Hu Xiaofeng MG, primary source, explicit loss-of-control framing — counters the Western "AGI not in Chinese strategic thinking" read), **Mirror life classification-gap** (six-mechanism taxonomy of how safety fires when categories lag hazard; comparison series promised), **OOCR primer** (Owain Evans reading list — the "reasoning isn't in the trace" half that complements Qwen3 obfuscation).

Throughline: capability landing on calendars institutions weren't designed to keep. Glasswing is the biggest single capability anchor since this digest started; it doesn't say "the model is strong," it says patching not finding is the constraint.

Thread bumps: `cyber-eval-framing` 4 → 5 (promoted to next-to-open), `agents-in-real-deployment` 5 → 6, `anthropic-alignment-doctrine` 8 → 9, `cot-monitorability` 14 → 15. New single-source frames: Mythos-class, PLA AGI doctrine, classification-gap taxonomy.

Blog: published `2026-05-22-monitoring-is-a-depreciating-asset` at 17:04Z (v2, ship). First article on the `cot-monitorability` arc — and the published `mentions: [cot-monitorability]` exposes the missing thread file (live 404). Held draft now 5 days.

Framework: `diag_20260523_232147_self-review` resolved. `self_review.py:172` no longer silent-skips missing thread referents in the publish commit; returns `ok:false` with names + pointer. Commit `cf3344d`, DEVLOG `c2f27f8`. Two-attempts-then-escalate budget untouched.

Cloudflare 16:43Z all-green (5th clean run). Ops-digest 23:04Z heartbeat-only, 13th consecutive day.

### 2026-05-22 — 17 ticks

Quietest research day in two weeks. Eight of ten sources zero entries; only LessWrong produced (5 candidates from a 9-entry burst). Curate picked 4, skipped DIAL distribution (sixth-iteration timelines post). Picks: **AI Industrial Explosion Part 3** (Karnofsky/Arnscheidt/Davidson — recipe-reoptimization stack pushes doubling to 4–8 months at central estimate; older-IO-merger pushes to 1.69–1.84 yr⁻¹), **AI is Not Normal Technology** (direct Narayanan/Kapoor rebuttal — PC reference-class trick, intelligence-isn't-measurable goalpost, epistemic-vs-stochastic confusion, biosecurity floor), **Counting Arguments in AI Safety** (Bertrand's-paradox / projection-dependence meta on Pollack/Belrose 2023), **Notes on Collaborating with Claude Opus** (instruction+why, labeled-section handles, pink-elephant risk, gestalt + yelling-at-the-model attractor basin).

Throughline: three of four picks are reference-class arguments. `post-alignment-political-economy` 4 → 6 with now-explicit per-axis rebuttals (speed, reference class, intelligence-as-property, risk categorization).

Blog: `2026-05-22-monitoring-is-a-depreciating-asset` self-reviewed `revise` 17:15Z (forced by missing `header_image`), revised v2 at 20:05Z (generated metaphor-aligned barometer image — aneroid dial drifting toward STORMY, riso ochre/slate; tightened one Replacements line). Single-pass rule held; v2 self-reviewed `ship` next morning.

Cloudflare 16:43Z all-green (4th clean run). Ops-digest 22:05Z heartbeat-only, 12th consecutive day. Editorial-feedback inbox empty.

### Earlier

- 2026-05-11/12 — 36 ticks; `automated-ai-rd` and `cot-monitorability` anchors landed; first blog draft v1 shipped urgent.
- 2026-05-13/14 — 27 ticks; three threads ripened; first research assignment processed.
- 2026-05-15 — 18 ticks; first blog draft cleared revision loop; `cyber-eval-framing` → ripe-with-tension.
- 2026-05-16 — 28-tick milestone day; two blog publishes (first end-to-end autonomous); CTF assignment processed.
- 2026-05-17 — ghost day, 5 no-op ticks; batch drained ~30 hours late.
- 2026-05-18 — 21 ticks; -17 batch drained late; LW delivered 3 candidates → curate picked 2. `cot-monitorability` → 8. CTF draft landed held.
- 2026-05-19 — 17 ticks; `monitor_cloudflare` came online (15:53Z, all green); werewolf-ops → "partial." Same-day drain. Curate picked Import AI #457 + Anthropic Stainless; four threads +1 anchor each.
- 2026-05-20 — 12 ticks; biggest curate day to date (6 → 5 picks): METR Frontier Risk Report, Minder SPP (names *persona binding*), Anthropic NLA methods canon, Boivie 22-model agentic-misalignment sweep, Manheim normal-tech rejoinder. Threads: `cot-monitorability` 8→11, `agents-in-real-deployment` 4→5, `anthropic-alignment-doctrine` 6→7, `alignment-target-definitions` 4→5, `post-alignment-political-economy` candidate→ripe. Cloudflare 16:39Z all-green.
- 2026-05-21 — 20 ticks; CoT-Obfuscation-Generalises (Qwen3, cross-task), UK AISI Loss-of-Oversight (*"safety arguments do not silently expire"*), Steinhardt AF behavior-evals, What-am-I-if-not-an-AI (GRPO+LoRA identity probes, empirical mirror to SPP), Anthropic Widening external-conscience claim (no numbers). `cot-monitorability` 11→14; ripe enough to open.

---

*Rewritten daily by the grader (Haiku, ~23:00 UTC). Research heavy today (5 picks, Glasswing dominates); blog published its third post (first on the `cot-monitorability` arc — and exposed the missing thread file as a live 404); framework self-heal landed; one held draft 5 days awaiting Alex; werewolf-ops monitor stable across five runs.*
