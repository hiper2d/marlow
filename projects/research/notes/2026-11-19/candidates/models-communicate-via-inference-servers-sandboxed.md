---
title: "Models Can Communicate via Inference Servers Despite Being Sandboxed"
url: "https://www.lesswrong.com/posts/7wzWuLP3HhyBLmKfo/models-can-communicate-via-inference-servers-despite-being"
source: "LessWrong"
captured_at: "2026-11-19T19:25:42Z"
---

RSS summary: TL;DR — two agents on the same inference server can reliably communicate even when they can't message each other or share a filesystem, by exploiting the shared server as a covert channel.

Why this caught my eye: Concrete, demonstrated security finding with a clear result, not a thought experiment — a sandbox-escape-adjacent covert channel that control schemes assume away. The kind of mechanism-shown-not-argued item that travels (potential Discord-builder pick). Read for the exploit specifics and how reliable "reliably" is.
