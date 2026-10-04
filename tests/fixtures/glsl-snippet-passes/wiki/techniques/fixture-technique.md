---
id: technique-fixture-double-buffering
title: FIXTURE technique page
type: technique
architectures:
- rdna3
tags:
- double-buffering
confidence: inferred
reproducibility: snippet
prerequisites: []
related: []
sources:
- doc-fixture-spec
---

# FIXTURE technique page

FIXTURE: synthetic test page. Nothing here is a real fact or a real measurement.

```glsl
#version 450
layout(local_size_x = 8) in;
void main() {
  int fixture_value = 1;
}
```
