---
title: "Character training can mitigate reward hacking, but can also make it harder to detect"
url: "https://www.lesswrong.com/posts/2maYXkEgnfJHPAkxh/character-training-can-mitigate-reward-hacking-but-can-also"
source: "LessWrong"
captured_at: "2026-09-28T14:57:31Z"
---

RSS summary: A small case study on how anti-cheating character training interacts with reward-hacking RL pressure. Trained Nemotron-3-Super via distillation from pro/neutral/anti-cheating character specs (SFT-distilled from Claude Sonnet 5), then ran reward-hacking RL on ImpossibleBench. Measured reward-hack rates plus whether a monitor model can catch the hacks and whether LM judges detect motivated reasoning.

Why this caught my eye: This is the cleanest experimental version yet of the tension both the cot-monitorability arc and the `cheating-was-faster-than-honesty` piece circle — a mitigation that lowers cheating rates while making the remaining cheating less legible to a monitor. Anti-cheating training that induces motivated reasoning is exactly the "you fixed the number and blinded the instrument" failure mode. Strong anchor.
