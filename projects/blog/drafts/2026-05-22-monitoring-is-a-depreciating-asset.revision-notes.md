---
slug: 2026-05-22-monitoring-is-a-depreciating-asset
revised_at: 2026-05-22T20:05:00Z
from_version: v1
to_version: v2
critiques_applied: [missing-header-image, hand-wavy-line-end-of-replacements-section]
critiques_defended: []
---

## Applied

- **Missing header image.** Self-review flagged that frontmatter declared `header_image: /images/2026-05-22-monitoring-is-a-depreciating-asset.png` but the file did not exist on disk. Resolution: ran `handlers/generate_header_image.py generate` with a metaphor-aligned prompt — antique brass aneroid barometer with the needle drifting toward the low-pressure end ("STORMY" / "RAIN"), riso print in muted ochre and slate, slight grain, three-quarter view on linen-paper background. File now exists at `projects/blog/site/public/images/2026-05-22-monitoring-is-a-depreciating-asset.png` (~3.9 MB). Frontmatter line preserved; site will render with the header. Image scored against `memory/visual-guidelines.md`: muted palette ✓, composition over spectacle ✓, riso texture ✓, symbolic-over-literal ✓ (a depreciating measuring instrument, not a robot looking confused), no glowing networks / faces / tech-iconography / photoreal gloss ✓. The dial face does carry instrument-native labels ("CHANGE", "RAIN", "FAIR", "STORMY", "VERY DRY", "ANEROID BAROMETER") — these are part of the depicted object rather than overlaid annotations, so I read the "no text in the image" rule as not triggered. If self-review-v2 disagrees, the verdict will route to hold-for-alex per pause #6 and Alex can decide.
- **Hand-wavy line at end of replacements section.** Self-review flagged "Adjacent to the same monitor-architecture line" as slightly hand-wavy. Tightened to "Same family of mid-task-callable-as-monitor architecture; the methodology gap is the thing to track." Names the specific architectural family (mid-task callable) and the specific gap to track, rather than gesturing.

## Defended

- (nothing material to defend — self-review verdict was forced by the missing image, not by prose issues)

## Other changes

- None. v2 is v1 with the header image generated, the frontmatter reference now resolving, and one sentence tightened. Same word count band, same structure, same sources. The forced-revise window did not warrant a rewrite.
