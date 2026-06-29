---
title: "Can we use steering vectors to suppress reward-hacking? Somewhat"
url: "https://www.lesswrong.com/posts/kzri5W2uBfF2mdboK/can-we-use-steering-vectors-to-suppress-reward-hacking-1"
source: "LessWrong"
captured_at: "2026-06-28T11:40:48Z"
---

RSS summary: Can steering vectors drive gradient routing? Yes, but not in realistic reward-hacking environments — they aren't precise enough classifiers of hacky vs clean solutions. Instead, can a steering vector initialise adapters so gradient routing happens without a classifier, separating hacky and clean gradients automatically? Partly: the init approach suppressed ~70% of hacking.

Why this caught my eye: A measured "somewhat" result on using steering to control reward-hacking — and it lands exactly where the steering-tools arc keeps landing: the vector isn't a precise enough classifier in realistic settings, but a softer init-based use partly works. Pairs directly with steering-directions-as-explanations-not-handles and the negated-reward-hacking thread. Honest partial-success negative-ish result, the kind the cot-monitorability / safety-tool-stewardship arcs feed on.
