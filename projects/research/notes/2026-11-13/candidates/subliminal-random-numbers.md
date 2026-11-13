---
title: "Instilling Behavior by Not Training on Specific Random Numbers"
url: "https://www.lesswrong.com/posts/6t4cyZbwKKbW3zJFe/instilling-behavior-by-not-training-on-specific-random"
source: "LessWrong"
captured_at: "2026-11-13T16:52:19Z"
---

RSS summary: Extends subliminal learning (a model picking up a behavior from semantically unrelated data). Prior work used a teacher model with the target behavior; here they train models to predict lists of uniform random numbers and change the models' reported "favorite animal" purely by selectively *masking* which numbers appear — behavior instilled by omission, not by any content carrying the trait.

Why this caught my eye: A cleaner, almost adversarial demonstration of subliminal learning — the signal is in what's withheld, not what's shown, which makes the "you can't audit the training data for the behavior" problem sharper. It's a tidy, surprising result that doesn't need the field's backstory to land.
