---
id: blog-glslang-issue-3948-small-index-types
title: 'glslang issue 3948: array indexing with small index types generates incorrect SPIR-V'
author: jeffbolznv, dnovillo
url: https://github.com/KhronosGroup/glslang/issues/3948
source_category: community-note
architectures: []
tags:
- int8-arithmetic
- spirv
retrieved_at: '2026-10-10'
description: 'GitHub issue thread (page type: source-blog). Array indexing with uint8_t / small unsigned index types emits an OpAccessChain index that SPIR-V treats as signed'
---

# glslang issue 3948: array indexing with small index types generates incorrect SPIR-V

GitHub issue thread in `KhronosGroup/glslang`, state `closed`, opened 2025-04-29, closed 2025-08-15.

## Excerpt: issue body by jeffbolznv, 2025-04-29

Locator: https://github.com/KhronosGroup/glslang/issues/3948

````text
Take this example shader that indexes an array using a uint8_t:

```
#version 450 core

#extension GL_EXT_shader_explicit_arithmetic_types : enable

layout(local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

void main()
{
    uint8_t u8 = uint8_t(150);
    float arr[200];
    float x = arr[u8];
}
```

This generates the following SPIR-V:
```
         %18 = OpLoad %uchar %u8
         %19 = OpAccessChain %_ptr_Function_float %arr %18
         %20 = OpLoad %float %19
```

But https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html#OpAccessChain says indices are treated as signed, so this is treated as a signed 8-bit integer rather than unsigned. To fix this, I think glslang needs to zero-extend smaller types before creating the access chain.
````

## Excerpt: comment by dnovillo, 2025-07-24

Locator: https://github.com/KhronosGroup/glslang/issues/3948#issuecomment-3114727505

```text
@jeffbolznv in this, you are not thinking about zero-extending into a wider integer, right? Just zero-extend within the width of the original index. The spec does not force a width for indices.
```

## Excerpt: comment by jeffbolznv, 2025-07-24

Locator: https://github.com/KhronosGroup/glslang/issues/3948#issuecomment-3114735531

```text
I _am_ suggesting to zero extend to a wider integer, because the current behavior effectively treats unsigned types as signed. I can maybe propose a fix for this.
```

The thread is quoted with attribution to its authors and is not relicensed.
