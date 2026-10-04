---
id: lang-fixture-glsl
title: FIXTURE language page
type: language
tags:
- glsl
related:
- kernel-fixture-linear
sources:
- doc-fixture-spec
reproducibility: snippet
architectures:
- arc-b580
---

# FIXTURE language page

FIXTURE: synthetic test page. Nothing here is a real fact or a real measurement.

```glsl
#version 450
layout(local_size_x = 8) in;
void main() {
  int fixture_value = 1;
}
```
