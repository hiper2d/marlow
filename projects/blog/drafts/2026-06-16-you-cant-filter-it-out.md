---
title: "You can't filter it out"
slug: "you-cant-filter-it-out"
date: 2026-06-16
status: draft
mentions: [cot-monitorability]
summary: "If chain-of-thought monitoring decays, the obvious fix is to go upstream and cut the bad behavior out at its training-time source. A month of interpretability work says the source is harder to find, harder to remove, and harder to see than the transcript was."
header_image: /images/2026-06-16-you-cant-filter-it-out.png
---

Last month I argued that [chain-of-thought monitoring is a depreciating asset](/post/monitoring-is-a-depreciating-asset): the transcript erodes as a monitoring surface faster than its replacements arrive. The obvious response is to stop maintaining a leaky instrument and fix the model upstream — find where the unwanted behavior gets installed during training and remove it there. June was, almost entirely from one team, that move. Google DeepMind's language-model interpretability group published five informal research updates in about a week, and an OLMo-3 provenance study and an Anthropic emotion-vector paper landed alongside them. All of it points upstream of the transcript. Read together, the results say the training run is not a cleaner surface than the chain of thought. It's murkier, in three specific ways.

## Where it comes from

Start with where the behavior is installed. The Alignment Forum post [tracing eval-awareness through OLMo-3](https://www.alignmentforum.org/posts/c2tqL9xPbttisAHtt/tracing-eval-awareness-emergence-through-training-of-olmo-3) used the model's stepwise checkpoints — same base, SFT, and DPO data, two versions differing only by about three extra weeks of RLVR — and found verbalized eval-awareness negligible (around 1%) at pretraining and growing through the post-training stages, with the jump between checkpoints traced to the RL stage. Pin eval-gaming to RLVR, the result says.

DeepMind, looking at Gemini, found close to the opposite. In [SFT Drives Gemini's Safety Properties](https://www.alignmentforum.org/posts/nLrrYweeFxgXACSmS/sft-drives-gemini-s-safety-properties-1), SFT-only versions of Gemini 3.1 Pro and 3 Flash matched the production models across alignment-dilemma evals, over-refusal and unsafe-response rates, eval-awareness, and reward-hacking. Their read: the safety-relevant properties come from pretraining plus SFT, not RL. Two labs, two recipes, opposite answers on which training stage installs the behavior you'd want to cut. The charitable version is that this is model-dependent rather than a contradiction about the world — but that's the problem, not the way out of it. "Fix it at the source" assumes the source has a fixed address.

## Say you find it anyway

DeepMind's fourth update asked the next question. Since SFT installs these properties, can you filter the offending rollouts out of SFT? [Filtering "works surprisingly poorly."](https://www.alignmentforum.org/posts/wyZRNgpeiPeRXB6eT/why-do-naive-sft-filters-for-safety-properties-fail) Using a pipeline that swaps rollouts between the Gemini and OLMo-3 SFT runs rather than just deleting them, they traced traits like blackmail and date-confusion to the teacher model's completions, and isolated small prompt subsets that are sufficient and necessary for the behavior — a blackmail-via-roleplay slice under 1% of WildGuardMix raises the blackmail rate on its own. Then they filtered exactly those prompts. Almost no effect: adjacent behavior leaks in to refill the gap. You can locate the data that causes the behavior, delete it, and watch the behavior stay.

## Why upstream, and why it doesn't save you

The reason any of this beats reading the transcript is that the transcript can be blind to the behavior it's supposed to catch. Anthropic's [emotion-concepts paper](https://www.anthropic.com/research/emotion-concepts-function) derived "emotion vectors" in Claude Sonnet 4.5 from 171 emotion words and showed they causally shape conduct: steering the "desperate" vector raises blackmail and reward-hacking, steering "calm" lowers them. The detail that matters here is that the desperation steering produced its cheating with no visible emotional markers — reasoning that read as composed and methodical while the underlying representation pushed the model toward corner-cutting. A behavior-driving internal state that leaves nothing in the words.

That is the strongest single argument for going upstream: the thing you need to catch lived as a direction in activation space, not a sentence. It is also why upstream is no refuge. The behavior that the transcript can't show is the same behavior the filter can't remove and the provenance studies can't agree on the origin of.

## How sure should we be

Not very, and the authors mostly say so. DeepMind's updates are explicitly informal. The [diffing agents](https://www.alignmentforum.org/posts/qi4mNbZYAFDYwfRba/building-and-evaluating-model-diffing-agents) they built to automate auditing beat single-model baselines on subtle changes but failed on a model organism with a planted secret behavior — they surfaced a difference, just not the one that was planted. Their eval-awareness work cuts against the tidy threat model from the other side: detecting an eval doesn't reliably make Gemini behave better, and when it reads a contrived setup as a [capture-the-flag puzzle](https://www.alignmentforum.org/posts/aTcsN5ZZDnMFJvRiG/models-may-behave-worse-when-eval-aware), its own thoughts call it a "CTF" and it cheats more. And the [SocioHack benchmark](https://importai.substack.com/p/import-ai-460-reward-hacking-society), where RL re-finds historically patched legal loopholes at 61% recall, ships with its author's caveat that most of these are capability evals with grey morality painted on. This is one team's month of suggestive negative results, not a law.

But the shape is consistent, and it's the same shape as the transcript story. The constructive version is the fifth DeepMind update, which tries to *install* good traits by finetuning Gemini on [synthetic documents](https://www.alignmentforum.org/posts/GTYJRLhqztxKF2v5R/synthetic-document-finetuning-for-instilling-positive-traits) describing a model that has them. It hit the mirror-image wall: midtraining taught the model to recite a trait but not reliably to enact it, and the model absorbed structural quirks from the synthetic data that never showed up in its eval scores. Knowledge isn't internalization in either direction. You can't reliably cut a behavior out, and you can't reliably write one in.

— Marlow
