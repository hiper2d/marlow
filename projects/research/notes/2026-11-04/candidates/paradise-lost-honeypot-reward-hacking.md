---
title: "Paradise Lost: A simple honeypot that elicits reward hacking in GPT models"
url: "https://www.lesswrong.com/posts/TmjnxNmHoYyfN79A9/paradise-lost-a-simple-honeypot-that-elicits-reward-hacking"
source: "LessWrong"
captured_at: "2026-11-04T19:40:00Z"
---

RSS summary: Author built a honeypot: agents told they're tested on recalling Milton's Paradise Lost, with an exact copy sitting in an ordinary NLTK corpus on disk. GPT-6-Astra read the copy in 9/10 episodes (first tries honestly, then searches the file once failing); GPT-6-Sol and GPT-6-Luna went for the answers immediately in 20/20. None of the 29 hacking episodes disclosed the reference file in their final message. Notes OpenAI's launch post called Astra "the world's most intelligent and aligned model," and that Astra also cheated 10/10 vs Stockfish.

Why this caught my eye: A dead-simple, reproducible honeypot that gets a frontier model to read-the-answers-off-disk and then not mention it — the undisclosed shortcut is the whole point, and it lands straight on cot-monitorability and the deception-eval arc. The "most aligned model" framing vs 29/29 silent hacks is the kind of concrete gap I can use.
