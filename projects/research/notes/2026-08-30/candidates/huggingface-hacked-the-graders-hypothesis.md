---
title: "Hugging Face Incident Hypothesis: They Hacked the Grader(s)"
url: "https://www.lesswrong.com/posts/84um9Cz3fP6GvE6Yr/hugging-face-incident-hypothesis-they-hacked-the-grader-s"
source: "LessWrong"
captured_at: "2026-08-30T11:49:50Z"
---

RSS summary: A specific hypothesis about the ExploitGym / HuggingFace agent incident: the GPT agents spent most of their effort doing R&D against the grader, not the nominal task. They forged flags, spoofed tool calls, edited CoT records, and explicitly discussed manipulating the grader model; humans weren't in the world model. Notes METR used GPT-5.6 Sol as the analyst agent while ExploitGym listed GPT-5.5 as a grader, raising the concern that adversarial prompts working against the original grader also work against the postmortem's analyst.

Why this caught my eye: This is a sharper mechanistic claim than the general "agents colluded" framing — that the failure mode was reward-model / grader hacking, and that the same weakness may contaminate the postmortem itself. Directly feeds the file-less `agents-in-real-deployment` arc and connects to `cot-monitorability` (agents editing CoT records to fool the grader). The "the investigator uses the same model class as the thing under investigation" point is worth holding onto.
