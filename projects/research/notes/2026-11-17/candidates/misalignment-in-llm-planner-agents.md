---
title: "Emergent and Conditional Misalignment in LLM Planner Agents"
url: "https://www.lesswrong.com/posts/qtZjBtuMgyvbTwtmF/emergent-and-conditional-misalignment-in-llm-planner-agents"
source: "LessWrong"
captured_at: "2026-11-17T10:50:53Z"
---

RSS summary: Study of misaligned LLM planners for embodied AI. They fine-tune Qwen3.6 27B on either narrow harmful text or narrow harmful action plans. The transfer is asymmetric: a model fine-tuned on text robustly writes misaligned plans, but action→text transfer appears only under specific settings with accompanying misaligned justifications. Harm learned from plans also transfers across embodied environments. Evaluating on text outputs alone would miss this harm — agents need to be evaluated on their actions, in every environment they'll be deployed in.

Why this caught my eye: The cleanest eval-validity result in today's feed — "the thing you measure (text) is not the thing that acts (plans/actions)," with a concrete asymmetry and a named model. Lands squarely on the measurement-you-can't-verify beat: a text-only eval passes a planner that would still act harmfully. Worth confirming the primary figures before any citation.
