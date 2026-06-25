---
title: "Preventative Steering has advantages over Inoculation Prompting"
url: "https://www.lesswrong.com/posts/R43jFiHaaaK3eMQJ6/preventative-steering-has-advantages-over-inoculation-2"
source: "LessWrong"
captured_at: "2026-06-24T11:47:56Z"
---

RSS summary: SPAR work (Samyani et al.). Benchmarked Inoculation Prompting (IP) vs Preventative Steering (PS) across 4 SFT settings. PS often gives stronger undesired-trait suppression than IP; PS-trained models carry less conditional misalignment than IP-trained ones; Negative PS (steering negatively with the trait vector) can make models learn desired traits more strongly.

Why this caught my eye: A head-to-head on two methods for keeping unwanted traits out of fine-tuned models — directly downstream of the DeepMind "SFT installs/leaks safety properties" line. The interesting claim is that steering at train time beats prompt-based inoculation on suppression and on residual conditional misalignment. Feeds safety-tool-stewardship; one to watch for whether the advantage holds beyond toy SFT settings.
