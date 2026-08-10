---
title: "Off-policy honesty training generalizes better than on-policy honesty training"
url: "https://www.lesswrong.com/posts/isPKgCFSHdJ6fKYbK/off-policy-honesty-training-generalizes-better-than-on"
source: "LessWrong"
captured_at: "2026-08-10T21:28:41Z"
---

RSS summary: SPAR Spring 2026 (Chaurasia/Tan/Li). Investigates self-report fine-tuning (SRFT) for honesty — SFT on 2-turn transcripts where the model lies with 50% probability then is asked whether it lied and confesses/denies. Finds off-policy training generalizes better than on-policy. Code released.

Why this caught my eye: A concrete honesty-training method with a cross-condition generalization result, from a student program rather than a lab — the source diversity the honesty/lie-detection cluster keeps needing. Sits next to the did-you-lie negative result on cot-monitorability (detectors that work on prompted lying but not genuine belief-divergence): this is the training-side counterpart to that measurement-side finding. Watch whether "off-policy generalizes better" survives on a real model organism.
