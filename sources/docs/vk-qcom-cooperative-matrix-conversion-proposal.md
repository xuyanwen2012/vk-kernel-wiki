---
id: doc-vk-qcom-cooperative-matrix-conversion-proposal
title: VK_QCOM_cooperative_matrix_conversion proposal (Vulkan-Docs)
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_QCOM_cooperative_matrix_conversion.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- shared-memory-limit
- subgroup-size
retrieved_at: '2026-10-10'
---

# VK_QCOM_cooperative_matrix_conversion proposal (Vulkan-Docs)

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/features/latest/features/proposals/VK_QCOM_cooperative_matrix_conversion.html

## Excerpt: proposals/VK_QCOM_cooperative_matrix_conversion.adoc, lines 17-30 (Problem Statement)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_QCOM_cooperative_matrix_conversion.adoc#L17-L30

```text
The baseline Cooperative Matrix extension achieves great performance
boost for simple matrix multiplication operations when data is loaded
to and from memory.

However, most use cases which leverage matrix
multiplication hardware, such as Convolution and Large Language Models,
require additional manipulation of input and output data which the opaque
cooperative matrix objects do not support directly.

The cooperative matrix extension explicitly requires staging data through
shared memory to perform these invocation-level manipulation operations.
An extension is needed that allows implementations
to create optimized data conversions between the invocation
and subgroup scope without explicitly going through shared memory.
```

## Excerpt: proposals/VK_QCOM_cooperative_matrix_conversion.adoc, lines 34-35 (Solution Space)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_QCOM_cooperative_matrix_conversion.adoc#L34-L35

```text
An explicit conversion API allows the application to bypass staging
to shared memory.
```

## Excerpt: proposals/VK_QCOM_cooperative_matrix_conversion.adoc, lines 39-59 (Proposal)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_QCOM_cooperative_matrix_conversion.adoc#L39-L59

```text
This proposal exposes support for the
`SPV_QCOM_cooperative_matrix_conversion` SPIR-V extension. This extension
provides the following:

  * Capabilities:
  ** `CooperativeMatrixConversionQCOM`
  * Instructions:
  ** `OpBitCastArrayQCOM`
  ** `OpCompositeConstructCoopMatQCOM`
  ** `OpCompositeExtractCoopMatQCOM`
  ** `OpExtractSubArrayQCOM`

This extension is compatible with the GLSL extension
`GLSL_QCOM_cooperative_matrix_conversion`.

Unlike `GLSL_KHR_cooperative_matrix.txt`, these instructions permit
the per-invocation vectors to be located in private memory. Allowing
<<coopmatconv-examples,workflows>> where shared memory staging
is not required. These can also enable applications to write
less vendor-dependent shaders, bypassing vendor required
loading constraints and shuffling of data.
```

## Excerpt: proposals/VK_QCOM_cooperative_matrix_conversion.adoc, lines 88-108 (OpCompositeConstructCoopMatQCOM and gl_MatrixUseA)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_QCOM_cooperative_matrix_conversion.adoc#L88-L108

```text
`OpCompositeConstructCoopMatQCOM` can be used to construct a cooperative matrix cooperatively
using a vector from each subgroup invocation. The GLSL equivalent is:

[source,c]
----
void vectorToCoopmatQCOM(SrcEltTy vec[SrcVecLen], coopmat<DstEltTy, gl_ScopeSubgroup, NumRows, NumCols, CoopMatUse> cm);
----

  * `CoopMatUse` determines the type of cooperative matrix and must be one of
    `gl_MatrixUseA`, `gl_MatrixUseB`, and `gl_MatrixUseAccumulator`

#### gl_MatrixUseA

When `CoopMatUse` type is `gl_MatrixUseA`, the per-invocation vectors fill in the rows of the matrix, where
the vector for `gl_SubgroupInvocationID == i` fills in row `i` of the matrix. Vectors belonging to invocations in
excess of `NumRows` are ignored and not copied.

The matrix `NumRows` must be a constant less than or equal to the `gl_SubgroupSize` and have a length in bytes
equal to 32. The permitted types of the matrix are `float32_t`, `float16_t`, `uint8_t`, and `int8_t`.

Both `NumRows` and `NumCols` are permitted to be specialization constants.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2025-2026 The Khronos Group, Inc. (file header, lines 1-3).
