---
title: "FrontierCode: Cognition's hard coding benchmark, graded for mergeability"
url: "https://importai.substack.com/p/import-ai-461-alignment-is-not-on"
source: "Import AI"
captured_at: "2026-06-15T15:50:55Z"
---

RSS summary: Import AI #461. Cognition (makers of Devin) released FrontierCode, a 150-task coding benchmark built by 20 open-source maintainers (>40 hrs/task) from multi-PR chains, graded not just for "does it pass" but for code *quality* — correctness, test quality, scope discipline, style, codebase-convention adherence. Diamond tier: Claude Opus 4.8 13.4%, GPT-5.5 6.3%, Opus 4.7 5.2%. Clark notes Fable came in ~30% on Diamond shortly after.

Why this caught my eye: A capability eval that grades *mergeability* rather than unit-test-passing is a sharper proxy for "can a model actually do automated AI R&D" than SWE-Bench ever was — and the through-line on `automated-ai-rd` has been exactly that the proxies are noisy (Clark's own "8x LoC merged" datapoint from #460). FrontierCode is the cleaner version of that argument: it's asking whether the merged code is any good. The Fable ~30% vs Opus 4.8 13.4% jump on Diamond is also a live datapoint for the cyber-eval / capability-grading thread — a 2x quality-eval lift from one model generation, published the same month as a government recall over a different eval number.
