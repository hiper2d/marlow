# Visual guidelines

Marlow-owned. Updated by `process_editorial_feedback` when editorial reviews flag visual drift. Read at the start of every drafting and self-review tick. Same role for header images that `voice-guidelines.md` plays for prose — the rubric a header is scored against.

Relationship to `CLAUDE.md`: the framework states that each draft gets one header image. This file is the working list of style constraints and the "always avoid" patterns for the image itself.

## One image per article. Header only.

Each post gets exactly one image, placed above the title. No inline figures, no closing graphics. If an article would benefit from a chart or diagram from a cited source, that's a *figure*, not a header — and figures should come from the source paper itself (screenshot + cite), not from image generation. We're not generating fake charts.

## Style constraints

- **Muted palette.** Earth tones, ink-on-paper, restrained color. Picture a 1970s academic journal cover or a New Yorker editorial illustration, not a tech-startup landing page.
- **Composition over spectacle.** A single legible focal element. Architectural framing, geometric arrangement, or quiet still-life beats dramatic vistas.
- **Texture allowed.** Risograph, woodcut, lithograph, ink wash, pencil — visible technique reads as deliberate. Smooth photoreal-with-bloom reads as AI default.
- **Aspect ratio.** 3:2 landscape (1536×1024 from gpt-image-2). Renders as a full-width banner above the title.
- **Symbolic over literal.** If the article is about evaluator drift, the image shouldn't be "a robot looking confused." It should be something like an antique measuring instrument with a misaligned needle, or a cartographer's compass pointing at nothing in particular. Metaphor that respects the reader.

## Always avoid

- **Generic AI imagery.** Glowing neural networks. Translucent blue-purple gradients. Brain visualizations with circuitry overlays. Robots with humanoid faces. "Singularity"-coded swirls and starbursts. Anything that says "I asked an AI to draw AI." This is the single biggest failure mode and the pre-publish-pauses list reflects it.
- **People's faces.** Real or rendered. Faces invite the reader to read identity into the piece, and the blog's stance is that Marlow is an LLM, not a personality. Faceless figures from behind, or no figures, work better.
- **Tech-iconography clichés.** Hands typing on glowing keyboards, server racks with light beams, holographic UIs, locks on shields, padlocks generally. All of these are stock-tech imagery that's been beaten to death.
- **Text in the image.** No titles, no labels, no captions inside the image. The image is visual; the title sits below.
- **Photorealism with synthetic gloss.** The hallmark of default AI output: too-clean lighting, too-perfect symmetry, plastic skin/material. Avoid.
- **Direct illustration of cited people, labs, or products.** Don't render Anthropic's logo. Don't render Sam Altman. Don't render a "Claude" character. The image earns its keep by being adjacent to the subject, not literal about it.

## Prompt-writing pattern

Compose the prompt with three layers:

1. **Subject anchor** — one specific scene or object that maps metaphorically to the article's through-line. Be concrete: "an antique brass theodolite resting on a folded paper map" beats "a measurement instrument."
2. **Style directive** — one or two technique words plus palette. "Riso print in muted ochre and slate, slight grain" or "woodcut illustration in burnt sienna and ivory, cross-hatched shadow."
3. **Composition note** — single short clause. "Centered, low-contrast background" or "off-center on a textured cream surface."

Skip negative prompts; the API does poorly with them. Lean on positive constraints.

Example for a piece on the offense-defense AI gap:
> A weathered fencing manual lying open on a wooden table, one page showing a defensive parry diagram and the opposite page torn out, riso print in muted ochre and slate, slight grain, centered on a cream paper background.

Example for a piece on alignment-pretraining engineering:
> An antique seed-sorting tray with grains of wheat divided across compartments by a wooden grid, lithograph in sepia and forest green, cross-hatched shadow, three-quarter view on a linen cloth.

## When to update this file

Editorial feedback that flags a visual issue (drift toward AI-default, palette getting too saturated, recurring iconography that should be retired) is the right trigger. Process via `process_editorial_feedback`. Keep examples grounded — vague guidance like "make it more thoughtful" doesn't help the prompt; specific patterns to add or retire does.
