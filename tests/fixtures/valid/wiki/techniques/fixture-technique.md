---
id: technique-fixture-double-buffering
title: FIXTURE technique page
type: technique
architectures:
- rdna3
tags:
- double-buffering
confidence: verified
reproducibility: snippet
prerequisites:
- hw-fixture-coopmat
related:
- hw-fixture-coopmat
sources:
- doc-fixture-spec
- pr-fixture-example-1
- blog-fixture-note
evidence_basis:
- evidence_type: official-doc
  source_id: doc-fixture-spec
  locator: section-0
- evidence_type: upstream-code
  source_id: pr-fixture-example-1
  locator: excerpt
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
