---
id: pr-vk-coopmat-perf-7
repo: jeffbolznv/vk_cooperative_matrix_perf
pr: 7
title: Skip cooperative-matrix combinations with no bundled shader
author: Indie-Siggi
date: '2026-06-05'
url: https://github.com/jeffbolznv/vk_cooperative_matrix_perf/pull/7
source_category: upstream-code
architectures: []
tags:
- cooperative-matrix
- cpp
techniques: []
hardware_features:
- cooperative-matrix
kernel_types: []
languages:
- cpp
captured_at: '2026-10-10'
status: merged
merge_sha: d2c4ac1199cb2d6fdc322a5eb7582d1064cd7e54
changed_paths:
- src/vk_cooperative_matrix_perf.cpp
inclusion_reason: 'include (manual review of title, description and changed paths): which advertised cooperative-matrix type combinations select a kernel variant; the description reports the combinations
  a named driver and device advertise: src/vk_cooperative_matrix_perf.cpp'
---

# Skip cooperative-matrix combinations with no bundled shader

Locator: https://github.com/jeffbolznv/vk_cooperative_matrix_perf/pull/7 (pull request description, first 1200 of 1486 characters)

<!-- upstream-excerpt-start -->
The shader-loading loop builds a filename from each driver-advertised cooperative-matrix property and, when the
matching `.spv` is missing, prints `<file> not found!` and runs a bare `throw;`. With no exception in flight that
calls `std::terminate()` (*"terminate called without an active exception"*) and aborts the whole run.

A driver can legitimately advertise type combinations the bundled shader set doesn't cover. Concretely, RADV
(Mesa) on RDNA4 with `VK_NV_cooperative_matrix2` **workgroup scope** advertises the mixed-sign integer combos
`u8 → s32` and `s8 → u32`, for which there is no `workgroupu8_s32.spv` / `workgroups8_u32.spv` (only `s8_s32` and
`u8_u32` ship). The tool terminates at the first such combo, before it can test everything it does support.

This prints a `SKIP:` notice and `continue`s to the next property instead, so the run completes over the
combinations that have shaders:

```diff
         if ((int)spirvsize == -1) {
-            printf("%s not found!\n", fileName.c_str());
-            throw;
+            printf("SKIP: %s not found (no precompiled shader for this advertised combo)\n", fileName.c_str());
+            continue;
         }
```

With this the ab
<!-- upstream-excerpt-end -->
