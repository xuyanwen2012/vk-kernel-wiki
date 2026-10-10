---
id: doc-vk-nv-cooperative-matrix2-extension
title: VK_NV_cooperative_matrix2 extension appendix (Vulkan-Docs)
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_NV_cooperative_matrix2.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
retrieved_at: '2026-10-10'
---

# VK_NV_cooperative_matrix2 extension appendix (Vulkan-Docs)

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/refpages/latest/refpages/source/VK_NV_cooperative_matrix2.html

## Excerpt: appendices/VK_NV_cooperative_matrix2.adoc, lines 9-16 (Other Extension Metadata)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_NV_cooperative_matrix2.adoc#L9-L16

```text
*Last Modified Date*::
    2024-08-01
*Interactions and External Dependencies*::
  - This extension provides API support for
    {GLSLregistry}/nv/GLSL_NV_cooperative_matrix2.txt[`GLSL_NV_cooperative_matrix2`]
*Contributors*::
  - Jeff Bolz, NVIDIA
  - Karthik Vaidyanathan, NVIDIA
```

## Excerpt: appendices/VK_NV_cooperative_matrix2.adoc, lines 20-38 (Description)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_NV_cooperative_matrix2.adoc#L20-L38

```text
This extension adds several new features building on the cooperative matrix
types added in VK_KHR_cooperative_matrix.
The goal is to add and accelerate features beyond just simple GEMM kernels,
including adding support for type/use conversions, reductions, per-element
operations, and tensor addressing, and also to improve usability and
out-of-the-box performance by adding support for more flexible matrix sizes,
and workgroup scope matrices with compiler-managed staging through shared
memory.

The new functionality is defined by the
{spirv}/NV/SPV_NV_tensor_addressing.html[`SPV_NV_tensor_addressing`] and
{spirv}/NV/SPV_NV_cooperative_matrix2.html[`SPV_NV_cooperative_matrix2`]
SPIR-V extensions and can be used with the
{GLSLregistry}/nv/GLSL_NV_cooperative_matrix2.txt[`GLSL_NV_cooperative_matrix2`]
GLSL extension.

This extension includes support for enumerating the matrix types and
dimensions that are supported by the implementation, and which specific
features are supported.
```

## Excerpt: appendices/VK_NV_cooperative_matrix2.adoc, lines 42-49 (New SPIR-V Capabilities)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_NV_cooperative_matrix2.adoc#L42-L49

```text
=== New SPIR-V Capabilities

  * <<spirvenv-capabilities-table-TensorAddressingNV,TensorAddressingNV>>
  * <<spirvenv-capabilities-table-CooperativeMatrixReductionsEXT,CooperativeMatrixReductionsNV>>
  * <<spirvenv-capabilities-table-CooperativeMatrixConversionsNV,CooperativeMatrixConversionsNV>>
  * <<spirvenv-capabilities-table-CooperativeMatrixPerElementOperationsEXT,CooperativeMatrixPerElementOperationsNV>>
  * <<spirvenv-capabilities-table-CooperativeMatrixTensorAddressingNV,CooperativeMatrixTensorAddressingNV>>
  * <<spirvenv-capabilities-table-CooperativeMatrixBlockLoadsNV,CooperativeMatrixBlockLoadsNV>>
```

Licence of the excerpts: CC-BY-4.0, Copyright 2024-2026 The Khronos Group Inc. (file header, lines 1-3).
