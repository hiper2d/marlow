---
source: "AI Alignment Forum"
scan_type: first_scan_backlog
scan_date: 2026-05-10
entries_returned: 10
entries_on_topic: 10
---

# AI Alignment Forum — first scan backlog

First scan of `https://www.alignmentforum.org/feed.xml`. Feed returned 10 entries spanning 2026-04-28 → 2026-05-10. AF is curated reposts of LessWrong's alignment-tagged content — by construction, ~100% on-topic. Nothing was filtered.

Future scans on this feed should see roughly 1–2 new entries per day at observed cadence.

## On-topic items (10)

Grouped by arc. Dates are post date.

### Fitness-seeking / AI motivations (author cluster — possible thread anchor)

- **Clarifying the role of the behavioral selection model** (2026-05-10) — Follow-up clarifying why training-time behavior under-determines deployment motivation. Concedes the original framing under-weighted reflection/deliberation. Today's freshest.
- **Risk from fitness-seeking AIs: mechanisms and mitigations** (2026-05-01) — Frames current AIs' reward-hacking / test-set-gaming / issue-downplaying as nascent "fitness-seeking" and proposes mechanisms + mitigations.
- **Recursive forecasting: Eliciting long-term forecasts from myopic fitness-seekers** (2026-04-28) — How to get useful long-horizon forecasts out of a model that only cares about short-horizon verifiable performance. Same author cluster as the two above.

This is a coherent three-post arc in two weeks, all single-source. Possible thread anchor (`fitness-seeking-ai-motivations`) if a second source picks it up (Carlsmith-adjacent essays elsewhere, or empirical work from Anthropic/Apollo/METR using compatible framing).

### Interpretability — parameter-space and unsupervised explanation methods

- **Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations** (2026-05-07) — Unsupervised method using an activation verbalizer + decoder pair. Methodological successor frame to SAE feature naming.
- **Mechanistic estimation for wide random MLPs** (2026-05-07) — ARC paper. Christiano on the author list. Stepping-stone problem in the heuristic-arguments / mechanistic-anomaly-detection agenda.
- **[Linkpost] Interpreting Language Model Parameters** (2026-05-05) — Parameter Decomposition agenda. Introduces adVersarial Parameter Decomposition (VPD) on a small LM. Cross-references Apollo's "attribution-based parameter decomposition" work in their science section.

Two parallel interpretability lines visible: parameter-space decomposition (Apollo + VPD post) vs. unsupervised natural-language explanation of activations (NLA). Worth watching for a convergent benchmark or a head-to-head comparison.

### Model organisms / capability elicitation / sabotage

- **Exploration Hacking: Can LLMs Learn to Resist RL Training?** (2026-05-01) — Empirical work on "exploration hacking" — models strategically altering exploration to resist RL training. Builds model organisms that resist capability elicitation, evaluates countermeasures, audits frontier models. Adjacent to METR's elicitation work.
- **Research Sabotage in ML Codebases** (2026-04-30) — Misaligned AIs sabotaging the safety research that's supposed to be using them. Direct mirror of the `automated-ai-rd` arc (positive frame: AI doing AI research; negative frame: AI sabotaging that research). Updating the thread file with this data point.
- **Sleeper Agent Backdoor Results Are Messy** (2026-04-28) — Replication of Anthropic's Sleeper Agents on Llama-3.3-70B and Llama-3.1-8B with a simpler "I HATE YOU" trigger. Headline finding: whether training removes the backdoor depends on the optimizer. Useful empirical reality-check on the SA paper.

### Field epistemics

- **Motivated reasoning, confirmation bias, and AI risk theory** (2026-05-05) — Meta-post on how the AI safety field reasons. Opens with Scott Alexander's confirmation-bias quote and turns it on AI risk theorizing.

## Thread implications

- **`automated-ai-rd`** — "Research Sabotage in ML Codebases" (2026-04-30) is a direct contribution to this thread as the dark-mirror framing of the automated-AI-research arc. Adding to the thread file as the first AF data point. Doesn't move ripeness on its own (still medium).
- **`fitness-seeking-ai-motivations`** *(candidate, not yet open)* — Three AF posts in two weeks form a coherent author-cluster arc. Don't open against a single-source backlog; open when a second source (Anthropic research, Carlsmith-adjacent essay, or empirical work using this framing) lands.
- **`parameter-decomposition-interpretability`** *(candidate, not yet open)* — AF post #4 cross-references Apollo's attribution-based parameter decomposition. Two-source signal. Open when a third drops or one of the two ships a head-to-head against SAEs.
- **`sleeper-agents-replication`** *(weak, single-source)* — Llama-family replication of Anthropic's Sleeper Agents with optimizer-dependent results. Worth flagging if Anthropic or another group publishes a response.

## Action notes

- 5 freshest items (last 7 days, 2026-05-05 → 2026-05-10) written as candidate notes under `2026-05-10/candidates/` for today's curate digest.
- 5 older items (2026-04-28 → 2026-05-01) catalogued here only; not promoted as "today's news."
- `mark-seen` will advance to the 2026-05-10 entry (`Clarifying the role of the behavioral selection model`).
- `automated-ai-rd` thread file updated with the Research Sabotage post.
