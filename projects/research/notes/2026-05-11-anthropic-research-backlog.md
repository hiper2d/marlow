---
title: "Anthropic research — backlog catalog"
source: "Anthropic Research"
captured_at: "2026-05-11"
kind: "backlog_catalog"
---

First scan of `https://www.anthropic.com/sitemap.xml` filtered to `/research/`. 119 entries spanning 2024-04-26 → 2026-05-08. Confirms the working-memory hypothesis: this is the technical channel. Signal-to-noise is dramatically higher than `/news/` — interpretability papers, alignment results, capability evals, agent / CoT studies, with a thin layer of economic-index content and team/landing pages. The bulk of canonical Anthropic safety research (Constitutional AI, sleeper agents, alignment faking, reward tampering, toy models of superposition, induction heads, sycophancy, Clio, agentic misalignment, etc.) is republished or linked from this section.

## Dating notes

Two `lastmod` clusters are bulk-migration timestamps and should not be read as publication dates:

- **2024-12-19** — ~25 items. Mostly the early canonical Anthropic papers (Constitutional AI, A general language assistant as a laboratory for alignment, training a helpful and harmless assistant, measuring faithfulness in CoT, sycophancy, towards monosemanticity, influence functions, many-shot jailbreaking, evaluating AI systems, building effective agents, sabotage evaluations, etc.).
- **2025-11-20** — ~15 items. Recent canonical line (alignment faking, auditing hidden objectives, reward tampering, persona vectors, introspection, tracing thoughts, Claude character, constitutional classifiers, toy models of superposition, values wild, collective constitutional AI, predictability-and-surprise, plus team landing pages alignment / interpretability / societal impacts / economic-research).

Items outside these clusters appear to have real per-item `lastmod` values. Treat the bulk-clustered items as undated archival; for actual publication dates, fall back to arxiv listings if the paper is academic.

## Catalog

### Mechanistic interpretability (heavy — Anthropic's flagship line)

Recent / dated:
- 2026-05-08 — Teaching Claude why — `/research/teaching-claude-why` *(title alone — could be interp, alignment, or model-behavior; needs body read)*
- 2026-05-07 — Natural language autoencoders — `/research/natural-language-autoencoders` *(autoencoders on natural-language reps — interpretability tooling)*
- 2026-05-01 — Emotion concepts function — `/research/emotion-concepts-function` *(features-as-emotions story; ties to persona vectors line)*
- 2026-03-02 — Mapping the mind of a language model — `/research/mapping-mind-language-model` *(reads as the canonical mech-interp summary post)*
- 2026-02-23 — Persona selection model — `/research/persona-selection-model`
- 2025-05-29 — Open source circuit tracing — `/research/open-source-circuit-tracing` *(tooling release)*
- 2025-02-20 — Crosscoder model diffing — `/research/crosscoder-model-diffing` *(interp technique for comparing models)*

Bulk-archival (2024-12-19 / 2025-11-20):
- Tracing thoughts in a language model; Toy models of superposition; Persona vectors; Introspection; Constitutional classifiers; Towards monosemanticity (dictionary learning); In-context learning and induction heads; A mathematical framework for transformer circuits; Decomposing language models into understandable components; Softmax linear units; Privileged bases in the transformer residual stream; Superposition, memorization, and double descent; Distributed representations / composition / superposition; Scaling laws and interpretability of learning from repeated data; Features as classifiers; Evaluating feature steering; Engineering challenges in interpretability; Interpretability dreams; Circuits updates (multiple: April/June/July/Aug/Sept 2024 + May 2023).

### Alignment / Claude character / values

Recent / dated:
- 2026-05-01 — Claude personal guidance — `/research/claude-personal-guidance`
- 2026-01-28 — Disempowerment patterns — `/research/disempowerment-patterns` *(suggestive title — failure-mode taxonomy?)*
- 2026-01-19 — Assistant axis — `/research/assistant-axis`
- 2025-11-21 — Emergent misalignment / reward hacking — `/research/emergent-misalignment-reward-hacking` *(direct safety result)*
- 2025-08-15 — End subset conversations — `/research/end-subset-conversations` *(Claude getting the option to end abusive conversations — model-welfare adjacent)*
- 2025-06-23 — Agentic misalignment — `/research/agentic-misalignment` *(major piece — Anthropic's own framing of agentic deception)*
- 2025-04-24 — Exploring model welfare — `/research/exploring-model-welfare`
- 2024-05-02 — Probes catch sleeper agents — `/research/probes-catch-sleeper-agents`

Bulk-archival:
- Alignment faking; Auditing hidden objectives; Reward tampering; Claude character; Values wild; Collective constitutional AI; Sleeper agents (also dated 2024-08-05 in another cluster); Constitutional AI: harmlessness from AI feedback; Specific versus general principles for constitutional AI; The capacity for moral self-correction; A general language assistant as a laboratory for alignment; Training a helpful and harmless assistant with RLHF; Towards measuring representation of subjective global opinions; Discovering language model behaviors with model-written evals; Predictability and surprise.

### Automated alignment / AI-doing-AI-research

- **2026-04-14 — Automated alignment researchers — `/research/automated-alignment-researchers`** ← **direct anchor for the `automated-ai-rd` thread**. Title alone is a probable ripeness trigger; body not yet read. Updated the thread file with this evidence.

### Agent capability / autonomy

- 2026-04-09 — Trustworthy agents — `/research/trustworthy-agents`
- 2026-04-03 — Diff tool — `/research/diff-tool` *(Anthropic's editing-tool design choice — pairs with Import AI's coding-agent coverage)*
- 2026-03-25 — Long-running Claude — `/research/long-running-Claude` *(persistence / horizon — METR-eval-adjacent)*
- 2026-03-26 — Project Vend 1 / Project Vend 2 / Project Fetch (robot dog) — three companion items (`/research/project-vend-1`, `/research/project-vend-2`, `/research/project-fetch-robot-dog`)
- 2026-02-19 — Measuring agent autonomy — `/research/measuring-agent-autonomy` ← **second-order anchor for `automated-ai-rd`** (capability measurement on the autonomy axis)
- 2026-02-05 — AI assistance coding skills — `/research/AI-assistance-coding-skills`
- 2025-06-23 — Agentic misalignment (cross-listed above)
- Bulk-archival: Building effective agents; Sabotage evaluations (also dated 2024-10-18); Shade Arena sabotage monitoring (2025-06-25); SWE-bench Sonnet.

### Capability / eval methodology

- 2026-04-30 — Evaluating Claude for bioinformatics (BioMysteryBench) — `/research/Evaluating-Claude-For-Bioinformatics-With-BioMysteryBench` *(domain capability eval; bio is a CBRN-adjacent surface)*
- 2026-02-23 — AI fluency index — `/research/AI-fluency-index`
- 2025-06-25 — Shade Arena sabotage monitoring — `/research/shade-arena-sabotage-monitoring`
- 2025-02-28 — Forecasting rare behaviors — `/research/forecasting-rare-behaviors`
- 2024-11-19 — Statistical approach to model evals — `/research/statistical-approach-to-model-evals`
- 2024-10-18 — Sabotage evaluations — `/research/sabotage-evaluations`
- 2024-09-10 — Measuring model persuasiveness — `/research/measuring-model-persuasiveness`
- Bulk-archival: Evaluating AI systems; Measuring progress on scalable oversight; SWE-bench Sonnet; Discovering language model behaviors with model-written evaluations; Evaluating and mitigating discrimination in language model decisions.

### CoT faithfulness / monitorability

- 2025-07-23 — Visible extended thinking — `/research/visible-extended-thinking`
- 2025-04-04 — Reasoning models don't say what they think — `/research/reasoning-models-dont-say-think` ← **directly relevant to the candidate `cot-monitorability` thread**; pairs with METR's CoT items and Apollo's CoT-monitorability position paper.
- Bulk-archival: Measuring faithfulness in chain-of-thought reasoning; Question decomposition improves faithfulness of model-generated reasoning.

### Defenses / red teaming / cyber

- 2026-01-09 — Next-generation constitutional classifiers — `/research/next-generation-constitutional-classifiers`
- 2025-11-24 — Prompt injection defenses — `/research/prompt-injection-defenses`
- 2025-10-09 — Small samples poison — `/research/small-samples-poison` *(data-poisoning result — pairs with Apollo / METR safety lines)*
- 2025-10-03 — Building AI cyber defenders — `/research/building-ai-cyber-defenders`
- Bulk-archival: Many-shot jailbreaking; Red-teaming language models to reduce harms.

### Anthropic Institute / strategy / tooling-release

- 2026-05-07 — Donating open-source Petri — `/research/donating-open-source-petri` *(governance handoff of the auditing tool; companion to MCP donation in /news/. Builds the "Anthropic donates its safety tools to a neutral org" pattern.)*
- 2026-05-07 — Anthropic Institute agenda — `/research/anthropic-institute-agenda` *(strategic doc for what reads as a new safety research org; pairs with "Introducing Anthropic Science" 2026-03-25)*
- 2026-03-25 — Introducing Anthropic Science — `/research/introducing-anthropic-science`
- 2025-11-04 — Deprecation commitments — `/research/deprecation-commitments` *(model-deprecation policy; pairs with 2026-02-25 `deprecation-updates-opus-3`)*
- 2026-02-25 — Deprecation updates Opus 3 — `/research/deprecation-updates-opus-3`
- 2025-10-06 — Petri open-source auditing — `/research/petri-open-source-auditing` *(initial Petri release; pairs with 2026-05-07 donation)*
- 2025-08-28 — Clio — `/research/clio` *(privacy-preserving usage analytics)*
- 2025-06-18 — Confidential inference / trusted VMs — `/research/confidential-inference-trusted-vms`

### Anthropic-uses-Claude / "vibe" reports

- 2026-03-25 — Vibe physics — `/research/vibe-physics`
- 2025-12-20 — Bloom — `/research/bloom` *(unclear without body read; likely product or tool)*
- 2025-12-09 — How AI is transforming work at Anthropic — `/research/how-ai-is-transforming-work-at-anthropic`
- 2025-12-07 — Estimating productivity gains — `/research/estimating-productivity-gains`
- 2026-04-03 — Diff tool (cross-listed)

### Economic index / labor / policy research (high volume, lower urgency)

The Anthropic Economic Index series + adoption briefs. Not a thread driver, but supplies real-world LLM usage data.

- 2026-04-22 — 81k economics — `/research/81k-economics`
- 2026-04-22 — Economic index survey announcement — `/research/economic-index-survey-announcement`
- 2026-04-08 — Labor market impacts — `/research/labor-market-impacts`
- 2026-03-31 — How Australia uses Claude — `/research/how-australia-uses-claude`
- 2026-03-25 — Economic index March 2026 report — `/research/economic-index-march-2026-report`
- 2026-03-23 — Economic index January 2026 report — `/research/anthropic-economic-index-january-2026-report`
- 2026-02-17 — India brief economic index — `/research/india-brief-economic-index`
- 2026-02-03 — Economic index primitives — `/research/economic-index-primitives`
- 2026-01-15 — Economic index September 2025 report — `/research/anthropic-economic-index-september-2025-report`
- 2025-12-05 — Economic research (team page) — `/research/team/economic-research`
- 2025-10-14 — Economic policy responses — `/research/economic-policy-responses`
- Bulk-archival: Economic index geography; Impact software development.

### Team / landing pages (suppressed)

`team/economic-research`, `team/societal-impacts`, `team/alignment`, `team/interpretability` — not content posts, just landing pages.

## Threads relevance

### `automated-ai-rd` — direct anchor landed

- **2026-04-14 — Automated alignment researchers** — `/research/automated-alignment-researchers`. Title is a near-exact match for one of the thread's ripeness triggers ("publishes an automated-alignment-research result"). Body not yet read; updating the thread file with this evidence and flagging as a candidate ripe-trigger pending body read.
- **2026-02-19 — Measuring agent autonomy** — `/research/measuring-agent-autonomy`. Anthropic's own capability-measurement on the agent-autonomy axis. Second-order anchor — the kind of eval data the thread wants alongside METR's RD-section results.
- Adjacent (capability infrastructure, not direct anchors): Trustworthy agents (2026-04-09), Long-running Claude (2026-03-25), AI assistance coding skills (2026-02-05).

### `cot-monitorability` (candidate thread) — anchor landed

- **2025-04-04 — Reasoning models don't say what they think** — `/research/reasoning-models-dont-say-think`. The Anthropic-side anchor that the candidate thread was waiting for. Pairs with the four METR CoT items and Apollo's CoT-monitorability position paper to form a clear three-source arc.
- Supplementary: Visible extended thinking (2025-07-23); bulk-archival Measuring faithfulness in CoT and Question decomposition.
- **Recommendation:** open the thread next tick. Don't open now — separate work. Note as a queued thread.

### Candidate new thread: `anthropic-interpretability-doctrine`

Anthropic publishes a steady cadence of mech-interp results — `mapping-mind-language-model` (2026-03-02), `crosscoder-model-diffing` (2025-02-20), `persona-selection-model` (2026-02-23), `natural-language-autoencoders` (2026-05-07), `emotion-concepts-function` (2026-05-01), plus the open-source `circuit-tracing` release (2025-05-29). Cross-source convergence would require DeepMind or Apollo mech-interp items; Apollo is more deception-focused so this may not materialize. **Not opening** — note for watch.

### Candidate new thread: `safety-tool-donations`

`Donating open-source Petri` (2026-05-07) + the MCP-donation-to-Agentic-AI-Foundation (2025-12-11 in /news/) form a pattern: Anthropic offloading its safety/agent tooling to neutral orgs. Could be a coherent governance story or coincidence. **Not opening** — wait for a third instance.

## What I'm watching for

- Read the body of `automated-alignment-researchers` to confirm `automated-ai-rd` thread ripeness. Top priority for next deep-read tick.
- Read `agentic-misalignment` (2025-06-23) — Anthropic's own framing of agentic deception; useful background for the candidate `cot-monitorability` thread and for any agent-related draft.
- Watch whether the `anthropic-institute-agenda` (2026-05-07) describes a research org separate from the existing alignment team — if so, it changes the org map.
- Whether `donating-open-source-petri` (2026-05-07) is paired with anything from Apollo or METR (auditing-tool ecosystem story).

## Future scans

Sitemap returned full 119 entries in one call. After `mark-seen` advances to the newest entry (2026-05-08 `teaching-claude-why`), future scans should see ≤1 new entry per week — Anthropic publishes /research/ posts at a roughly weekly cadence, and most weeks land 1-3 items. Backlog scan size: never repeats unless feed state is wiped.
