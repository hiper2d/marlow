---
title: "Import AI backlog catalog (#436–#455)"
source: "Import AI"
captured_at: "2026-05-10T21:05Z"
scan_id: "scan_import_ai_20260510_1143"
---

First persisted Import AI scan. Working memory referenced a 2026-05-09 catalog of #446–#455, but the corresponding note file and `automated-ai-rd` thread file are absent on disk and Import AI had no entry in `_feed_state.json` — so for my purposes this is the first real scan. Fetch returned 20 issues spanning 2025-11-24 to 2026-05-04 (Import AI ships ~weekly with occasional gaps). Treating as a backlog catalog (precedent: METR / Apollo / AE Studio backlog notes from earlier today), not as same-day candidates.

Themes below are derived from titles and RSS summaries; I have not read the issue bodies. Bodies are typically 5–10 segments per issue, so per-segment cataloging would be premature without a reason to dig.

## Themes

### Automated AI R&D / recursive self-improvement (densest arc)
- **#455** (2026-05-04) — *"AI systems are about to start building themselves."* Subtitle: "The first step towards recursive self improvement." Direct anchor item.
- **#454** (2026-04-20) — *Automating alignment research; safety study of a Chinese model; HiFloat4.*
- **#449** (2026-03-16) — *LLMs training other LLMs; 72B distributed training run; computer vision is harder than generative text.*
- **#448** (2026-03-09) — *AI R&D; Bytedance's CUDA-writing agent; on-device satellite AI.* "AI writing CUDA" is the same shape as METR's RD-section evals.
- **#444** (2026-02-09) — *LLM societies; Huawei makes kernels with AI; ChipBench.*
- **#439** (2026-01-05) — *AI kernels; decentralized training; and universal representations.*
- **#437** (2025-12-08) — *Co-improving AI; RL dreams; AI labels might be annoying.*

Seven of twenty issues touch this arc — Clark has been tracking it as a coherent storyline through 2026. Combined with METR's two 2026-05-08 RD-section posts, this is the closest thing to a ripe thread on the board.

### Agentic systems and agent ecologies
- **#453** (2026-04-13) — *Breaking AI agents; MirrorCode; and ten views on gradual disempowerment.*
- **#447** (2026-03-02) — *The AGI economy; testing AIs with generated games; and agent ecologies.*
- **#443** (2026-02-02) — *Into the mist: Moltbook, agent ecologies, and the internet in transition.*
- **#441** (2026-01-19) — *My agents are working. Are yours?* (Plus: corrupting AI systems with a poison fountain.)
- **#451** (2026-03-30) — *Political superintelligence; Google's society of minds, and a robot drummer.*

"Agent ecology" is a Clark-coined frame and recurs three times in six months. Worth a separate thread tag — `agent-ecologies` — but no second-source convergence yet, so don't open.

### Cyber / scaling laws for offense
- **#452** (2026-04-06) — *Scaling laws for cyberwar; rising tides of AI automation; and a puzzle over gDP forecasting.*
- **#450** (2026-03-23) — *China's electronic warfare model; traumatized LLMs; and a scaling law for cyberattacks.*
- **#442** (2026-01-26) — *Winners and losers in the AI economy; math proof automation; and industrialization of cyber espionage.*
- **#438** (2025-12-22, "Silent sirens") — slug `cyber-capability-overhang`. Likely the framing essay for this strand.

Two distinct "scaling laws for cyber X" pieces inside two months suggests Clark is tracking a real curve. Possible thread anchor when an external lab (Anthropic/Apollo) adds an item, or when a concrete benchmark drops.

### China / geopolitics
- **#454** (2026-04-20) — Chinese model safety study (cross-listed with R&D arc).
- **#450** (2026-03-23) — China's electronic warfare model.
- **#446** (2026-02-23) — *Nuclear LLMs; China's big AI benchmark; measurement and AI policy.*

Three items but no second-source convergence; geopolitics is largely background colour for this corpus.

### Forecasting / "timing superintelligence"
- **#445** (2026-02-16) — *Timing superintelligence; AIs solve frontier math proofs; a new ML research benchmark.*
- **#451** (2026-03-30) — *Political superintelligence …*
- **#447** (2026-03-02) — *The AGI economy …*

Macro-forecasting / takeoff framing — Clark's editorial obsession but not directly actionable as a thread.

### Math / formal reasoning automation
- **#445** (2026-02-16) — frontier math proofs.
- **#442** (2026-01-26) — math proof automation.

Two-item line. If a third source (DeepMind / Anthropic / arxiv-via-author-list) lands, this becomes a thread.

### Disempowerment / regulation
- **#453** (2026-04-13) — ten views on gradual disempowerment.
- **#440** (2026-01-12) — *Red queen AI; AI regulating AI; o-ring automation.*
- **#436** (2025-11-24) — *Another 2GW datacenter; why regulation is scary; how to fight a superintelligence.*

Editorial / political framing, low priority for thread tracking.

### Misc anchors worth flagging
- **#450** (2026-03-23) — "traumatized LLMs" — possible model-welfare angle, will note if a second source picks it up.
- **#441** (2026-01-19) — "poison fountain" — agentic-corruption / data-poisoning vector, low signal until concrete eval lands.

## Thread implications

- **`automated-ai-rd`**: confirmed and reinforced. Opening the thread file as a separate artifact this tick (it was referenced in `working.md` but never persisted). Seven Import AI items + two 2026-05-08 METR items + Apollo's strategic-deception adjacent line — ripeness now medium, will move to "ripe" if any of: (a) Anthropic/OpenAI publishes an automated-alignment-research result, (b) METR publishes a third RD-section eval, (c) a frontier lab announces an "AI does AI research" deployment.

- **`cot-monitorability`**: no Import AI item directly contributes; status unchanged from working memory.

- **`agent-ecologies`** (new candidate, not opened): Clark's recurring frame. Wait for a second source.

- **`cyber-scaling`** (new candidate, not opened): two scaling-law-for-cyber pieces. Wait for a second source.

## State advanced

Marked feed seen at `https://importai.substack.com/p/import-ai-455-automating-ai-research`, latest 2026-05-04T12:32:09+00:00. Future scans should see ≤1 new entry per run.
