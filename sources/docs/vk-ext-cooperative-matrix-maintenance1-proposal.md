---
id: doc-vk-ext-cooperative-matrix-maintenance1-proposal
title: VK_EXT_cooperative_matrix_maintenance1 proposal (Vulkan-Docs)
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_cooperative_matrix_maintenance1.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- coopmat-shape
- subgroup-size
- subgroup-size-control
retrieved_at: '2026-10-10'
---

# VK_EXT_cooperative_matrix_maintenance1 proposal (Vulkan-Docs)

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/features/latest/features/proposals/VK_EXT_cooperative_matrix_maintenance1.html

## Excerpt: proposals/VK_EXT_cooperative_matrix_maintenance1.adoc, lines 16-22 (Problem Statement)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_cooperative_matrix_maintenance1.adoc#L16-L22

```text
While VK_KHR_cooperative_matrix can be used to accelerate "simple" GEMMs, it
has some serious limitations:

 * Some networks require operations like reductions or matrix _Use_ conversions,
   and currently these require a round trip through shared memory.
 * There is no way to query for capabilities that vary by subgroup size or by
   class of operation (e.g. saturating accumulation).
```

## Excerpt: proposals/VK_EXT_cooperative_matrix_maintenance1.adoc, lines 35-42 (Solution Space)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_cooperative_matrix_maintenance1.adoc#L35-L42

```text
 * Matrix _Use_ conversions are important for writing fused network kernels,
   so that an accumulator can be used as an operand for another multiply.
 * Reductions are common in networks, for example softmax activation requires
   a reduction over rows, and max-pooling requires a reduction over 2x2
   neighborhoods. We support these in Accumulator matrices since that is the
   primary place they are needed. It is also possible to do sum-reduce of a
   row of an A matrix or a column of a B matrix by multiplying by a matrix
   of all ones, so we do not add an additional way to do this.
```

## Excerpt: proposals/VK_EXT_cooperative_matrix_maintenance1.adoc, lines 46-52 (Proposal)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_cooperative_matrix_maintenance1.adoc#L46-L52

```text
The solution space section describes all the separate features of the proposal
and which solutions we have chosen. Then a final question is how to package these
features. Most of these can be used independently as incremental additions to
VK_KHR_cooperative_matrix. These are specified as independent feature enables
(and independent SPIR-V capabilities) so implementations can adopt them
incrementally (or they could be promoted incrementally) if needed. There are no
specific required features besides `cooperativeMatrixProperties2`.
```

## Excerpt: proposals/VK_EXT_cooperative_matrix_maintenance1.adoc, lines 56-80 (Querying properties, query function and VkPhysicalDeviceCooperativeMatrixInfo2EXT)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_cooperative_matrix_maintenance1.adoc#L56-L80

```text
This extension introduces a new extensible query function:

[source, c]
----
VkResult vkGetPhysicalDeviceCooperativeMatrixProperties2EXT(
    VkPhysicalDevice                                 physicalDevice,
    const VkPhysicalDeviceCooperativeMatrixInfo2EXT* pCooperativeMatrixInfo,
    uint32_t*                                        pPropertyCount,
    VkCooperativeMatrixProperties2EXT*               pProperties);

typedef struct VkPhysicalDeviceCooperativeMatrixInfo2EXT {
    VkStructureType                    sType;
    const void*                        pNext;
    VkScopeKHR                         scope;
    uint32_t                           invocations;
    uint32_t                           subgroupSize;
    VkCooperativeMatrixFlagsEXT        flags;
} VkPhysicalDeviceCooperativeMatrixInfo2EXT;
----

  * `scope` is the scope of the matrix.
  * `invocations` is the number of invocations within the local workgroup.
  * `subgroupSize` is the size of the subgroup.
  * `flags` is a bitmask of `VkCooperativeMatrixFlagBitsEXT` values
    selecting which class of matrix properties to query.
```

## Excerpt: proposals/VK_EXT_cooperative_matrix_maintenance1.adoc, lines 82-104 (Querying properties, subgroupSize and invocations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_cooperative_matrix_maintenance1.adoc#L82-L104

```text
This `subgroupSize` allows the query to return matrix properties that
are specific to the provided subgroup size. A value of 0 is used to
query matrix properties that are valid for shaders executing with a
varying subgroup size (i.e. shaders created with
`VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT` or
`VK_SHADER_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT_EXT`). For properties
returned by such a query, the implementation is permitted to choose
the effective subgroup size at runtime. Shaders that
neither force the subgroup size via
`VkPipelineShaderStageRequiredSubgroupSizeCreateInfo` nor enable a
varying subgroup size still have a well-defined effective subgroup size
of `VkPhysicalDeviceSubgroupProperties::subgroupSize`, and applications
should query with that value rather than 0 in that case.

Applications should use this new query function as the implementation may
expose additional properties that are optimal or compatible only
with specific subgroup sizes.

The `invocations` field is ignored when `scope` is `VK_SCOPE_SUBGROUP_KHR`.
When the query is used together with an extension that supports workgroup
scope cooperative matrices (such as `VK_NV_cooperative_matrix2`), `scope`
may be `VK_SCOPE_WORKGROUP_KHR`, in which case `invocations` indicates the
number of invocations in the local workgroup.
```

## Excerpt: proposals/VK_EXT_cooperative_matrix_maintenance1.adoc, lines 108-131 (Querying properties, VkCooperativeMatrixProperties2EXT)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_cooperative_matrix_maintenance1.adoc#L108-L131

```text
[source, c]
----
typedef struct VkCooperativeMatrixProperties2EXT {
    VkStructureType       sType;
    void*                 pNext;
    uint32_t              MGranularity;
    uint32_t              NGranularity;
    uint32_t              KGranularity;
    VkComponentTypeKHR    AType;
    VkComponentTypeKHR    BType;
    VkComponentTypeKHR    CType;
    VkComponentTypeKHR    ResultType;
} VkCooperativeMatrixProperties2EXT;
----

When used together with an extension that supports flexible-dimensions
cooperative matrices (such as `VK_NV_cooperative_matrix2`) and the
corresponding feature is enabled, the `MGranularity`, `NGranularity`, and
`KGranularity` members specify the alignment of the matrix sizes,
otherwise they specify the matrix sizes equivalent to the `MSize`, `NSize`,
and `KSize` of
xref:{docs}chapters/shaders.html#VkCooperativeMatrixPropertiesKHR[VkCooperativeMatrixPropertiesKHR].

All other members are equivalent to `VkCooperativeMatrixPropertiesKHR`.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2024-2026 The Khronos Group Inc. (file header, lines 1-3).
