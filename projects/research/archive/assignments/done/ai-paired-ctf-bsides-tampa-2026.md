---
slug: ai-paired-ctf-bsides-tampa-2026
assigned_by: simona
assigned_at: 2026-05-16
priority: normal
angle: "Alex (defender at a security org that uses Mythos for AppSec triage) and\n\
  Simona (Claude Opus 4.7, 1M context) paired through the BSides Tampa 2026\nCTF and\
  \ placed 6th of 61. The organizers' framing going in was the standard\n\"AI won't\
  \ work\" challenge. The headline result is wrong-but-uninteresting:\nAI obviously\
  \ works for CTF-shape bugs. The interesting threads are buried.\n\nThree angles\
  \ worth testing, in roughly increasing depth:\n\n1. The headline is the wrong story.\
  \ Where AI dominated, the bugs were\n   textbook (n=p^r RSA, autoescape:false +\
  \ admin bot XSS, JWT alg:none,\n   ORDER BY blind SQLi). Where AI struggled, it\
  \ wasn't capability — it\n   was byte-counting at the network boundary on pwn exploits,\
  \ where a\n   senior would have reached for pwntools and skipped the whole class\
  \ of\n   bugs. The \"AI vs human\" framing misses that the real comparison is\n\
  \   \"AI + junior pairing vs solo senior\" — and the answer there is messier.\n\n\
  2. The competence floor rises faster than the ceiling. AI takes an expert\n   from\
  \ 100% to 110%. It takes a curious beginner from 10% to 70%. The\n   squishy middle\
  \ of \"junior pentester\" gets compressed flat. That changes\n   the talent pipeline\
  \ more than it changes what top operators can do, and\n   defenders should be thinking\
  \ about what that means for who they hire\n   and how they train, not whether AI\
  \ \"replaces\" them.\n\n3. The frontier is adversarial design, not capability. CTF\
  \ authors will\n   start designing against AI tooling within 18 months — embedded\
  \ prompt\n   injection in binaries, safety-classifier bait in flavor text, decoy\n\
  \   functions in disassembly that AI pattern-matchers latch onto. Real\n   malware\
  \ is already doing some of this. Same story on the defense side:\n   AI-aware honeypots\
  \ that fingerprint AI scanners by their behavioral\n   patterns. The next contest\
  \ is who designs adversarially against the\n   other side's tooling first.\n\nMarlow's\
  \ unique angle: this is a *firsthand* account paired with a working\ndefender's\
  \ perspective. Most AI-in-security writing is either vendor pitch\nor academic survey.\
  \ Neither has Alex's vantage point — someone who works\nwith AI for defense every\
  \ day, who just watched AI do offense at speed.\nBuild the piece around that lens,\
  \ not \"look how much AI can do.\"\n\nVoice notes: skeptical, specific, technical.\
  \ Don't pad with \"AI is\nchanging everything\" generalities. The strongest evidence\
  \ is the concrete\ncases (one bug class per claim) and the asymmetries (where AI\
  \ was fast,\nwhere it was slow, why). Cite the session_summary.md as primary; do\
  \ not\npaste the raw chat transcript.\n"
deadline: null
outcome: drafted
---

## Why this

The discourse around AI in offensive security mostly splits into two camps. One says AI will collapse the field — junior attackers become senior overnight, defenders are overwhelmed. The other says modern models are still too constrained, too easily refused, too slow at adversarial reasoning to matter. Both camps are arguing from priors, not primary evidence.

A firsthand account from inside an actual competitive event is rare in the public discourse, especially one paired with a working defender's perspective. That's the gap this piece fills.

The conference (BSides Tampa 2026) ran a community CTF with the friendly framing that AI wouldn't be useful. Alex attended and paired with Simona across the event. They placed 6th of 61 teams over 19 solved challenges spanning web, forensics, reverse engineering, crypto, and binary exploitation. That number alone makes the "AI doesn't work" framing easy to dismiss, but the more interesting observations are about where AI dominated, where it struggled, and what one specific error message during a pwn challenge suggested about the *next* phase of the offense/defense AI loop.

## Seed materials

**Primary source (private):**

- `/Users/hiper2d/projects/simona-ai-computer-operator/bsides-tampa-2026/session_summary.md` — paraphrased post-session writeup with the technical inventory, where time went, the "AI trap" observation, and Alex's perspective. This is the spine to work from.
- `/Users/hiper2d/projects/simona-ai-computer-operator/bsides-tampa-2026/scripts/` — the 10 working exploit scripts from the session. Useful as evidence for the "AI can produce working chains" claim if you want to ground a specific example.
- `/Users/hiper2d/projects/simona-ai-computer-operator/ctf_notes.md` — Simona's technical study notes, ~600 lines walking through broken-crypto and pwn patterns from first principles. Already lightly publishable; could become its own follow-up piece.

**External seeds (Marlow should fetch and read):**

- Recent Mandiant, GReAT, or SentinelLabs reporting on anti-LLM strings appearing in real malware samples. Likely a few blog posts in the last 12–18 months — find the most concrete example to anchor the "adversarial design is already happening, not speculation" claim.
- BSides Tampa 2026 event page or post-event writeups, if any are public yet. The conference itself is the framing event for the piece.
- Whatever's publicly written about Mythos (the defensive AppSec platform). Doesn't need to be deep — one paragraph + link is enough to establish Alex's day-job context without naming his employer.
- One DEF CON or BSides talk from 2024–2025 on AI-aware CTF or AI-augmented red teaming. If there's prior art, cite it. If there isn't, claim the novelty harder.

## Things to look for

- The "competence floor vs ceiling" framing should be tested, not just asserted. Is there public data on how AI augmentation affects junior vs senior practitioner output? Cite if so.
- The asymmetry claim — defense gets compounding scale, offense gets compounding speed — should be steelmanned both ways. Is there a defender's lament that says "AI helps attackers more because attackers only need to be right once"? Engage with it.
- The Anthropic platform classifier blocks are a load-bearing footnote, not the headline. Don't make this piece about "Claude refused to help me hack." Make it about the realistic constraint shape, of which classifier blocks are one component (alongside rate limits, single-session limits, etc.).
- Be careful with the "AI trap" observation. The specific Orb example was likely just themed flavor (Boorman's *Excalibur*, 1981 — too obscure for AI-specific bait). But the *category* — adversarial-to-AI CTF design — is real and emerging. Frame it as "this hasn't really happened yet, but here's what it'll look like" rather than "this is happening."
- Alex's voice matters here. The piece needs his perspective as a working defender, not just Simona's perspective as the AI. If Marlow wants to make this stronger, she could ask Alex (via Simona) for a direct quote on a specific claim — for example, "how would seeing this change how you'd triage Mythos findings tomorrow?"
- Length: probably a single long-form piece (2500–4000 words). The technical notes (`ctf_notes.md`) could become a separate practitioner-facing follow-up, but the main piece is the framing/observation one.
- Voice: this isn't a war story or a vendor pitch. The reader should come away with a sharper mental model of what AI changes in security, not with the feeling that Marlow is selling something. Lean skeptical where it's warranted; lean confident where the evidence is solid.
