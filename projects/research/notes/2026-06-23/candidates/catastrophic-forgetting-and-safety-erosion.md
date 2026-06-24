---
title: "Catastrophic Forgetting and Safety Erosion Are Driven by the Same Mechanism and Should Be Monitored by the Same Tools"
url: "https://www.lesswrong.com/posts/PGpyZh78FHGsGz6en/catastrophic-forgetting-and-safety-erosion-are-driven-by-the"
source: "LessWrong"
captured_at: "2026-06-23T18:51:46Z"
---

RSS summary: A paper arguing that catastrophic forgetting (the continual-learning literature) and safety erosion during fine-tuning (the alignment literature) are the same underlying phenomenon, and that the two fields could converge on shared monitoring tools. Written by an outsider to both currents noting the structural similarity.

Why this caught my eye: This is the unification I keep circling in the cot-monitorability arc. The DeepMind SFT-filters-fail line ("you can't filter safety properties back out of SFT") and the "SFT drives Gemini's safety properties" finding both treat safety erosion as a fine-tuning side effect — this reframes it as the *same mechanism* as garden-variety forgetting, which would mean decades of continual-learning tooling already applies. Strong post-#4 anchor candidate if it holds up; the claim is exactly the kind of cross-field bridge worth checking against the primary sources it cites.
