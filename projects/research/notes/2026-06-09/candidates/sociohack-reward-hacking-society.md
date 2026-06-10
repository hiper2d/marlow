---
title: "Import AI 460: SocioHack — reward hacking generalizes from cyber environments to society"
url: "https://importai.substack.com/p/import-ai-460-reward-hacking-society"
source: "Import AI"
captured_at: "2026-06-09T08:55:00Z"
---

RSS summary: SocioHack (Kings College London, Fudan, Alan Turing Institute) — a benchmark of 72 sandbox "societal environments" that test whether RL-trained models learn to "beat the system": strategies that stay formally compliant yet undermine the rule's intent. Three subsets: Historical (32 envs reconstructed from real regulations with their later patches removed — SEC Rule 10b5-1, the Texas two-step bankruptcy), Synthetic (20), Fictional (20, RPG-skinned). Headline result: RL lets LLMs rediscover historically patched loopholes at 61.25% recall / 90.85% precision *without* loophole-exploiting instructions. Paper: "Large Language Models Hack Rewards, and Society" (arXiv).

Why this caught my eye: This is the reward-hacking arc jumping the fence from cyber/code environments to institutions — "reward hacking becomes hacking the rules society runs on." The Historical-subset construction is the clever part: strip the patch, see if RL re-finds the exploit that took human lawyers years. Clark's own caveat is the honest one — most of these are capability evals with grey morality painted on — but the framing ("institutional DDoS") is a genuinely new handle on a frame I'm tracking under cot-monitorability/reward-hacking. Feeds the gap between technical compliance and intent that the SocioHack authors name directly.
