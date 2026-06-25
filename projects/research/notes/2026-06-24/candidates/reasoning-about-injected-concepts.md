---
title: "Reasoning and learning about injected concepts in language models"
url: "https://www.lesswrong.com/posts/de2qaz6G3qrFZvQqK/reasoning-and-learning-about-injected-concepts-in-language-1"
source: "LessWrong"
captured_at: "2026-06-24T11:47:56Z"
---

RSS summary: SPAR work (mentors Bronzi, Fornasiere). Tests models' ability to recover information about their own activations: inject steering vectors and ask the LLM to verbalize properties. Via in-context learning, probes whether models can identify the layer region (early/middle/late), relative magnitude (low/med/high), and gate behavior conditioned on detecting an injection with specific semantic meaning.

Why this caught my eye: Introspection-as-monitoring from the other direction — not "can we read the model" but "can the model report on its own injected internal state." If models can detect and verbalize injected steering, that's both a monitoring tool and a route to evasion (a model that knows it's being steered can route around it). Sits next to the NLA/activation-verbalizer thread.
