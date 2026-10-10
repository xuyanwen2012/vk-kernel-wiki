---
id: doc-vk-nv-cooperative-matrix-decode-vector-proposal
title: VK_NV_cooperative_matrix_decode_vector proposal (Vulkan-Docs)
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_NV_cooperative_matrix_decode_vector.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- dequantize
retrieved_at: '2026-10-10'
---

# VK_NV_cooperative_matrix_decode_vector proposal (Vulkan-Docs)

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/features/latest/features/proposals/VK_NV_cooperative_matrix_decode_vector.html

## Excerpt: proposals/VK_NV_cooperative_matrix_decode_vector.adoc, lines 11-12 (introduction)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_NV_cooperative_matrix_decode_vector.adoc#L11-L12

```text
This extension extends the decode callback added in VK_NV_cooperative_matrix2
to allow decoding multiple matrix elements per invocation.
```

## Excerpt: proposals/VK_NV_cooperative_matrix_decode_vector.adoc, lines 16-28 (Problem Statement)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_NV_cooperative_matrix_decode_vector.adoc#L16-L28

```text
VK_NV_cooperative_matrix2 added a decode callback that lets the shader
dequantize one matrix element at a time while a tensor block is being
loaded. Most quantized weight formats are naturally unpacked in groups
(e.g. several nibbles or bits out of the same packed word), so calling the
decode function once per element makes the implementation redo that unpack
work for every element that shares a packed source.

A compiler can try to vectorize calls to the scalar callback, but it cannot
always do as good a job as the application, and relying on this kind of
optimization is fragile and not portable across implementations. We would
prefer to give the application an explicit way to express "decode V
elements at once" so that the unpack work happens once for V consecutive
matrix elements.
```

## Excerpt: proposals/VK_NV_cooperative_matrix_decode_vector.adoc, lines 32-50 (Solution Space)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_NV_cooperative_matrix_decode_vector.adoc#L32-L50

```text
The most direct option is to replace the existing scalar DecodeFunc with a
vector-returning version. That has a significant downside: a given
OpCooperativeMatrixLoadTensorNV is sometimes lowered by staging through
shared memory and sometimes more directly into registers, and the decode
shape that fits one path is not necessarily the right shape for the other.
Loading a _UseB_ matrix from row-major memory is the canonical example:
it is effectively a transpose relative to the blocked layout, so a vector
decode along the storage direction works well when staging matches that
layout but is the wrong shape once the values land in registers. Making a
vector-only DecodeFunc work everywhere would require tying the vector width
to the matrix _Use_, the _TensorView_, and the load's span/offset/layout
dimensions, so the decode width always matched how the matrix is traversed.

Instead, we add an optional second callback, DecodeVectorFunc, alongside
the existing scalar DecodeFunc. The shader supplies both, and the
implementation picks one or the other per call site. DecodeVectorFunc
returns a vector of 2, 4, or 8 components of the matrix component type and
is invoked once per group of V block-adjacent elements. Matrix _Use_ and
_TensorView_ stay independent of decode shape.
```

## Excerpt: proposals/VK_NV_cooperative_matrix_decode_vector.adoc, lines 54-67 (Proposal)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_NV_cooperative_matrix_decode_vector.adoc#L54-L67

```text
The new functionality is described in SPV_NV_cooperative_matrix_decode_vector
and the matching GLSL_NV_cooperative_matrix_decode_vector.

This Vulkan extension adds a single feature `cooperativeMatrixDecodeVector`
in `VkPhysicalDeviceCooperativeMatrixDecodeVectorFeaturesNV`, which gates
use of the CooperativeMatrixDecodeVectorNV SPIR-V capability. It also adds
a runtime SPIR-V rule that the tensor block size in the innermost dimension
must be a multiple of the number of components of the DecodeVectorFunc
return type.

The extension depends on VK_NV_cooperative_matrix2, and an implementation
exposing it must also support
`VkPhysicalDeviceCooperativeMatrix2FeaturesNV::cooperativeMatrixBlockLoads`.
There are no new commands or properties.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2026 The Khronos Group Inc. (file header, lines 1-3).
