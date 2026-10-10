---
id: pr-vk-coopmat-perf-5
repo: jeffbolznv/vk_cooperative_matrix_perf
pr: 5
title: Check bfloat16 coopmat support
author: GinShio
date: '2025-06-07'
url: https://github.com/jeffbolznv/vk_cooperative_matrix_perf/pull/5
source_category: upstream-code
architectures: []
tags:
- cooperative-matrix
- bfloat16-arithmetic
- fp16-arithmetic
- cpp
techniques: []
hardware_features:
- cooperative-matrix
- bfloat16-arithmetic
- fp16-arithmetic
kernel_types: []
languages:
- cpp
captured_at: '2026-10-10'
status: merged
merge_sha: a0d3ffb6ffa7534eaa1b0ac89a6836af3ff41247
changed_paths:
- src/vk_cooperative_matrix_perf.cpp
inclusion_reason: 'include (manual review of title, description and changed paths): the host checks whether the device supports bfloat16 cooperative matrices before it selects that kernel variant: src/vk_cooperative_matrix_perf.cpp'
---

# Check bfloat16 coopmat support

Locator: https://github.com/jeffbolznv/vk_cooperative_matrix_perf/pull/5 (pull request description, complete)

<!-- upstream-excerpt-start -->
The specification allows only one of bfloat16 dot and coopmat to be supported. When setting the cooperative matrix properties, please note that the vendor may not support bfloat16 coopmat.
<!-- upstream-excerpt-end -->
