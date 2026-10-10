---
id: blog-glslang-issue-3929-bfloat16-coopmat-elementwise
title: 'glslang issue 3929: Invalid arithmetic operations when generating Cooperative Matrix per-element ops with BFloat matrices'
author: cmarcelo, jeffbolznv
url: https://github.com/KhronosGroup/glslang/issues/3929
source_category: community-note
architectures: []
tags:
- cooperative-matrix
- bfloat16-arithmetic
- spirv
retrieved_at: '2026-10-10'
description: 'GitHub issue thread (page type: source-blog). glslang emitted OpFAdd on bfloat16 cooperative matrices, which SPV_KHR_bfloat16 does not allow'
---

# glslang issue 3929: Invalid arithmetic operations when generating Cooperative Matrix per-element ops with BFloat matrices

GitHub issue thread in `KhronosGroup/glslang`, state `closed`, opened 2025-04-15, closed 2025-04-18.

## Excerpt: issue body by cmarcelo, 2025-04-15 (shader)

Locator: https://github.com/KhronosGroup/glslang/issues/3929

````text
Example below:

```
#version 450

#extension GL_KHR_shader_subgroup_basic: enable
#extension GL_KHR_memory_scope_semantics: enable
#extension GL_KHR_cooperative_matrix: enable
#extension GL_EXT_shader_explicit_arithmetic_types: enable
#extension GL_EXT_buffer_reference: enable
#extension GL_EXT_bfloat16: enable

#define M 8
#define N 8

layout(local_size_x = 32) in;

layout(binding = 0) buffer A {
    bfloat16_t x[64];
};

layout(binding = 1) buffer B {
    bfloat16_t y[64];
};

layout(binding = 2) buffer R {
    bfloat16_t r[64];
};

void main() {
    coopmat<bfloat16_t, gl_ScopeSubgroup, M, N, gl_MatrixUseA> matX;
    coopmat<bfloat16_t, gl_ScopeSubgroup, M, N, gl_MatrixUseA> matY;
    coopmat<bfloat16_t, gl_ScopeSubgroup, M, N, gl_MatrixUseA> matR;
    coopMatLoad(matX, x, 0, N, gl_CooperativeMatrixLayoutRowMajor);
    coopMatLoad(matY, y, 0, N, gl_CooperativeMatrixLayoutRowMajor);
    matR = matX + matY;
    coopMatStore(matR, r, 0, N, gl_CooperativeMatrixLayoutRowMajor);
}
```
````

## Excerpt: issue body by cmarcelo, 2025-04-15 (generated SPIR-V)

Locator: https://github.com/KhronosGroup/glslang/issues/3929

```text
generates an OpFAdd between two matrices with BFloat16 component type, but
per SPV_KHR_bfloat16 that's not allowed
```

## Excerpt: comment by cmarcelo, 2025-04-15

Locator: https://github.com/KhronosGroup/glslang/issues/3929#issuecomment-2806513462

```text
Related: https://github.com/KhronosGroup/SPIRV-Tools/issues/6090
```

## Excerpt: comment by jeffbolznv, 2025-04-15

Locator: https://github.com/KhronosGroup/glslang/issues/3929#issuecomment-2807298137

```text
Thanks, I created a PR to add the missing error checks.
```

The thread is quoted with attribution to its authors and is not relicensed.
