---
id: kernel-fixture-linear
title: FIXTURE kernel page
type: kernel
architectures:
- radeon-780m
tags:
- linear-4w
- cooperative-matrix
confidence: verified
reproducibility: benchmarked
kernel_types:
- linear-4w
languages:
- glsl
related: []
sources:
- meas-fixture-radeon-780m
performance_claims:
- gpu: radeon-780m
  driver: FIXTURE-DRIVER 0.0.0
  dtype: fixture-dtype
  shape: FIXTURE 1x1x1
  metric: fixture-units
  value: fixture-fast
  measured_at: 2000-01-01
  source_id: meas-fixture-radeon-780m
  source_locator: row-0
  notes: FIXTURE synthetic value, not a measurement
evidence_basis:
- evidence_type: measurement
  source_id: meas-fixture-radeon-780m
  locator: row-0
---

# FIXTURE kernel page

FIXTURE: synthetic test page. Nothing here is a real fact or a real measurement.

```glsl
#version 450
layout(local_size_x = 8) in;
void main() {
  int fixture_value = 1;
}
```
