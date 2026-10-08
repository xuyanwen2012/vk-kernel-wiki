---
id: doc-vk-nv-cooperative-matrix2-proposal
title: VK_NV_cooperative_matrix2 proposal (Vulkan-Docs)
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/e4e53e4b31e13eeaee1ad99fb940aa72b2ec1b14/proposals/VK_NV_cooperative_matrix2.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
retrieved_at: '2026-10-06'
---

# VK_NV_cooperative_matrix2 proposal (Vulkan-Docs)

## Excerpt: proposals/VK_NV_cooperative_matrix2.adoc, lines 16-33 (Problem Statement)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/e4e53e4b31e13eeaee1ad99fb940aa72b2ec1b14/proposals/VK_NV_cooperative_matrix2.adoc#L16-L33

```text
While VK_KHR_cooperative_matrix can be used to accelerate "simple" GEMMs, it
has some serious limitations:

 * Subgroup scope matrices are small enough that using them the natural way
   in a GEMM does not lead to good performance. Shader authors can work around
   this by explicitly tiling and staging through shared memory, but it is
   cumbersome. Similarly, for networks that need slightly larger matrices that
   should still fit in the register file, they are again required to explicitly
   tile.
 * Some networks require operations like reductions or matrix _Use_ conversions,
   and currently these require a round trip through shared memory.
 * Simple row/col-major ordering is fine for 2D tensors, but many networks
   have tensors with more dimensions, more complex slicing of tensors, and
   padding at tensor boundaries. VK_KHR_cooperative_matrix does not address
   these use cases.
 * Many large networks store weights in a quantized format, and there is not
   a great way to dequantize these as they are loaded into a cooperative
   matrix.
```

## Excerpt: proposals/VK_NV_cooperative_matrix2.adoc, lines 46-55 (Solution Space, matrix sizes and workgroup scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/e4e53e4b31e13eeaee1ad99fb940aa72b2ec1b14/proposals/VK_NV_cooperative_matrix2.adoc#L46-L55

```text
 * Compilers can easily scale matrix sizes by internally tiling them, and more
   flexible matrix dimensions are clearly valuable for ease of use. The main
   question is whether the sizes should be completely arbitrary, or defined as
   a multiple of some minimum granularity. Completely arbitrary sizes might
   lead to unexpected complexity or performance issues, so for simplicity this
   extension adds minimum granularities, and any multiple is supported up to
   some relatively large upper bound. Additionally, supporting matrices at
   workgroup scope allows implementations to more efficiently support larger
   matrix sizes, and to optimize their loads by automatically staging them
   through shared memory.
```

## Excerpt: proposals/VK_NV_cooperative_matrix2.adoc, lines 80-85 (Solution Space, quantized weights)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/e4e53e4b31e13eeaee1ad99fb940aa72b2ec1b14/proposals/VK_NV_cooperative_matrix2.adoc#L80-L85

```text
 * Quantized weights are often stored in sub-byte types (e.g. int4) or as part
   of a larger block, and need to be scaled and/or run through a lookup table
   to produce the dequantized value. Previously, this had to be done manually
   and copied into shared memory to be loaded into a matrix. We support block
   dimensions in the addressing calculations and a decode callback function that
   allows the values to be dequantized as they are loaded into the matrix.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2024-2026 The Khronos Group Inc. (file header, lines 1-3).
