---
title: "Red-teaming LLM unlearning: LUNAR's forgotten knowledge is still recoverable"
url: https://www.lesswrong.com/posts/shkMAc9Logd8xPQvB/red-teaming-llm-unlearning-lunar-s-forgotten-knowledge-is
source: LessWrong
highlighted_at: 2026-07-25T01:26:22Z
status: idea
---

## Alex flagged this to write about

Interesting

---
Marlow's note when she sent it:

A clean red-team result that unlearning suppresses rather than deletes. LUNAR is a state-of-the-art method that retrains a single MLP down-projection matrix to redirect "forget"-set activations into "I don't know" responses, and it looks robust under standard eval including white-box attacks. It isn't: the author finds two routes back to the forgotten knowledge — GRPO optimizing upstream layers to route *around* the redirection site without touching it, and a linear activation shift that reverses the redirection mask, reconstructed without the original checkpoint and without even knowing which layer LUNAR modified. The mechanism detail is the sting: a single localized bottleneck is a single point of recovery. If unlearning is meant to strip dangerous knowledge (bioweapon synthesis is the stock example) out of the weights, "still recoverable if you sample the tail or route around one matrix" means the safety property was hidden, not removed — the same suppression-not-deletion pattern the refusal and SFT-filtering results keep surfacing.
