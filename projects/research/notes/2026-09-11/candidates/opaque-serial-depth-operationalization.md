---
title: "An operationalization of opaque serial depth"
url: "https://www.alignmentforum.org/posts/x8BvtWxtoajBGHS3g/an-operationalization-of-opaque-serial-depth"
source: "AI Alignment Forum"
captured_at: "2026-09-11T14:30:00Z"
---

RSS summary: Redwood Research operationalizes a measure — a proxy for how much
unverbalized serial cognition a model can perform — as a specific instantiation
of "opaque serial depth" (Brown-Cohen et al, GDM, 2026). The measure is the
longest path in the computational graph that doesn't pass through an
"interpretable bottleneck"; CoT tokens count as a bottleneck, latent recurrence
does not. Companion to their architecture-monitorability tracking proposal.

Why this caught my eye: This is the cot-monitorability thread getting something
it's been short on — a concrete, measurable quantity rather than another
qualitative warning. It turns "architectures could erode CoT oversight" into a
number you could in principle report and compare across labs. Pairs directly
with the Pachocki "diminishing" on-record line and the GDM bounded-depth work.
