---
id: blog-shaderc-issue-1594-coopmat2-optimizer-capability
title: 'shaderc issue 1594: shaderc internal error: Invalid capability operand: 5447 with cooperative‑matrix shader'
author: '1234562026'
url: https://github.com/google/shaderc/issues/1594
source_category: community-note
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- sdpa
- spirv
retrieved_at: '2026-10-10'
description: 'GitHub issue thread (page type: source-blog). glslc -O fails on a cooperative-matrix-2 shader with ''Invalid capability operand: 5447'' on a distribution shaderc build'
---

# shaderc issue 1594: shaderc internal error: Invalid capability operand: 5447 with cooperative‑matrix shader

GitHub issue thread in `google/shaderc`, state `open`, opened 2026-08-30.

## Excerpt: issue body by 1234562026, 2026-08-30 (report)

Locator: https://github.com/google/shaderc/issues/1594

````text
# Bug Report
## Environment
- Platform: Android aarch64 (Termux)
- glslc/shaderc installed from Termux official repository

## Problem
When compiling a Vulkan compute‑shader that uses Cooperative Matrix 2 capabilities with optimization flag `-O`, the compilation succeeds, but the SPIR‑V optimizer crashes internally:
shaderc: internal error: compilation succeeded but failed to optimize: Invalid capability operand: 5447

## Reproduction command
```bash
glslc -fshader-stage=compute --target-env=vulkan1.3 flash_attn_cm2.comp -o test.spv -O -DFLOAT16=1
````

The thread is quoted with attribution to its authors and is not relicensed.
