---
title: "Import AI 460: RL-trained drones beat a champion human pilot in real-world multi-agent racing"
url: "https://importai.substack.com/p/import-ai-460-reward-hacking-society"
source: "Import AI"
captured_at: "2026-06-09T08:55:00Z"
---

RSS summary: University of Zurich + Google DeepMind trained quadrotor-racing agents via PPO self-play (with a Perceiver encoder for modeling other racers) that outperform a five-time Swiss national champion in multi-player races above 22 m/s while cutting collision rates 50% vs single-agent baselines. Trained entirely in simulation (Flightmare/Agilicious, particle-based downwash model, domain randomization) — 200M interactions, ~27 hours on a single RTX 4090 — then deployed zero-shot to the real world. Anticipatory behaviors (blocking, yielding, riding aerodynamic wake) emerged from competitive self-play, not explicit programming. Notable human-factors note: competitive pressure pushed the human into riskier, error-prone maneuvers; the learned policy didn't degrade that way.

Why this caught my eye: Off my core safety arcs, but a clean, cheap (single 4090, 27h) real-world RL result that beats an elite human and sim-to-real generalizes zero-shot — the "chilling implications for war" Clark flags are not subtle. The honest caveat is in the writeup: not running locally, piloted over the network, so it sidesteps the electronic-warfare environment real combat drones face. Worth Alex seeing as a capability/real-world-RL datapoint even though it doesn't feed a current thread.
