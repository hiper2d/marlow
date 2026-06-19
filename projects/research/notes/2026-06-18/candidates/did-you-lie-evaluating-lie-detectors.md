---
title: "“Did you lie?” Evaluating Lie Detectors across Model Scale and Belief-Verified Model Organisms"
url: "https://www.lesswrong.com/posts/xFbMTnmDAucwE8Cdm/did-you-lie-evaluating-lie-detectors-across-model-scale-and"
source: "LessWrong"
captured_at: "2026-06-18T11:37:22Z"
---

RSS summary: Lie detectors for LLMs could help auditing/monitoring, but evaluating them needs testbeds where the model verifiably believes the opposite of what it says — most existing trained model organisms don't clear that bar. Authors train 13 reasoning model organisms with CoT evidence they hold the alternative belief (and OOD generalisation), plus a broad prompted-lying testbed. Finding: detectors scale positively with capability when lying is prompted, but every activation- and logprob-based detector drops sharply [under the harder belief-verified setting].

Why this caught my eye: A direct negative-result datapoint for the cot-monitorability arc — the monitoring tools degrade exactly where it matters (genuine belief-divergence, not prompted lying). The "most model organisms don't actually believe the opposite" methodological gripe is a sharp critique of how this whole subfield validates itself. Pairs naturally with the activation-steering negative results already on the thread.
