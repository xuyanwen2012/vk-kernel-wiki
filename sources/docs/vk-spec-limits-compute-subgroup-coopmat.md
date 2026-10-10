---
id: doc-vk-spec-limits-compute-subgroup-coopmat
title: 'Vulkan specification, Limits chapter: maxComputeSharedMemorySize, compute workgroup limits, subgroup and cooperative-matrix properties'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc
source_category: official-doc
architectures: []
tags:
- shared-memory-limit
- workgroup-size-limit
- subgroup-size
- subgroup-size-control
- subgroup-operations
- cooperative-matrix
- cooperative-matrix2
retrieved_at: '2026-10-10'
---

# Vulkan specification, Limits chapter: maxComputeSharedMemorySize, compute workgroup limits, subgroup and cooperative-matrix properties

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/spec/latest/chapters/limits.html

## Excerpt: chapters/limits.adoc, lines 499-503 (VkPhysicalDeviceLimits, maxComputeSharedMemorySize)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L499-L503

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/limits.html#limits-maxComputeSharedMemorySize

```text
  * [[limits-maxComputeSharedMemorySize]] pname:maxComputeSharedMemorySize
    is the maximum total storage size, in bytes, available for variables
    declared with the code:Workgroup storage class in shader modules (or
    with the code:shared storage qualifier in GLSL) in the compute shader
    stage.
```

## Excerpt: chapters/limits.adoc, lines 504-529 (VkPhysicalDeviceLimits, maxComputeWorkGroupCount, maxComputeWorkGroupInvocations and maxComputeWorkGroupSize)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L504-L529

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/limits.html#limits-maxComputeWorkGroupSize

```text
  * [[limits-maxComputeWorkGroupCount]] pname:maxComputeWorkGroupCount[3] is
    the maximum number of local workgroups that can: be dispatched by a
    single dispatching command.
    These three values represent the maximum number of local workgroups for
    the X, Y, and Z dimensions, respectively.
    The workgroup count parameters to the dispatching commands must: be less
    than or equal to the corresponding limit.
    See <<dispatch>>.
  * [[limits-maxComputeWorkGroupInvocations]]
    pname:maxComputeWorkGroupInvocations is the maximum total number of
    compute shader invocations in a single local workgroup.
    The product of the X, Y, and Z sizes, as specified by the code:LocalSize
ifdef::VK_COMPUTE_VERSION_1_3,VK_KHR_maintenance4[or code:LocalSizeId]
    execution mode in shader modules or by the object decorated by the
    code:WorkgroupSize decoration, must: be less than or equal to this
    limit.
  * [[limits-maxComputeWorkGroupSize]] pname:maxComputeWorkGroupSize[3] is
    the maximum size of a local compute workgroup, per dimension.
    These three values represent the maximum local workgroup size in the X,
    Y, and Z dimensions, respectively.
    The pname:x, pname:y, and pname:z sizes, as specified by the
    code:LocalSize
ifdef::VK_COMPUTE_VERSION_1_3,VK_KHR_maintenance4[or code:LocalSizeId]
    execution mode or by the object decorated by the code:WorkgroupSize
    decoration in shader modules, must: be less than or equal to the
    corresponding limit.
```

## Excerpt: chapters/limits.adoc, lines 1329-1354 (VkPhysicalDeviceSubgroupProperties, members)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L1329-L1354

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/limits.html#VkPhysicalDeviceSubgroupProperties

```text
  * [[{anchor-prefix}limits-subgroupSize]] pname:subgroupSize is the default
    number of invocations in each subgroup.
    pname:subgroupSize is at least 1 if any of the physical device's queues
    support ename:VK_QUEUE_GRAPHICS_BIT or ename:VK_QUEUE_COMPUTE_BIT.
    pname:subgroupSize is a power-of-two.
  * [[{anchor-prefix}limits-subgroupSupportedStages]]
    pname:{supportedStages} is a bitfield of elink:VkShaderStageFlagBits
    describing the shader stages that <<shaders-group-operations, group
    operations>> with <<shaders-scope-subgroup, subgroup scope>> are
    supported in.
    pname:{supportedStages} will have the ename:VK_SHADER_STAGE_COMPUTE_BIT
    bit set if any of the physical device's queues support
    ename:VK_QUEUE_COMPUTE_BIT.
  * [[{anchor-prefix}limits-subgroupSupportedOperations]]
    pname:{supportedOperations} is a bitmask of
    elink:VkSubgroupFeatureFlagBits specifying the sets of
    <<shaders-group-operations, group operations>> with
    <<shaders-scope-subgroup, subgroup scope>> supported on this device.
    pname:{supportedOperations} will have the
    ename:VK_SUBGROUP_FEATURE_BASIC_BIT bit set if any of the physical
    device's queues support ename:VK_QUEUE_GRAPHICS_BIT or
    ename:VK_QUEUE_COMPUTE_BIT.
  * [[{anchor-prefix}limits-subgroupQuadOperationsInAllStages]]
    pname:{quadOperationsInAllStages} is a boolean specifying whether
    <<shaders-quad-operations,quad group operations>> are available in all
    stages, or are restricted to fragment and compute stages.
```

## Excerpt: chapters/limits.adoc, lines 1514-1537 (VkPhysicalDeviceSubgroupSizeControlProperties, members)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L1514-L1537

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/limits.html#VkPhysicalDeviceSubgroupSizeControlProperties

```text
  * [[{anchor-prefix}limits-minSubgroupSize]] pname:minSubgroupSize is the
    minimum subgroup size supported by this device.
    pname:minSubgroupSize is at least one if any of the physical device's
    queues support ename:VK_QUEUE_GRAPHICS_BIT or
    ename:VK_QUEUE_COMPUTE_BIT.
    pname:minSubgroupSize is a power-of-two.
    pname:minSubgroupSize is less than or equal to pname:maxSubgroupSize.
    pname:minSubgroupSize is less than or equal to <<limits-subgroupSize,
    pname:subgroupSize>>.
  * [[{anchor-prefix}limits-maxSubgroupSize]] pname:maxSubgroupSize is the
    maximum subgroup size supported by this device.
    pname:maxSubgroupSize is at least one if any of the physical device's
    queues support ename:VK_QUEUE_GRAPHICS_BIT or
    ename:VK_QUEUE_COMPUTE_BIT.
    pname:maxSubgroupSize is a power-of-two.
    pname:maxSubgroupSize is greater than or equal to pname:minSubgroupSize.
    pname:maxSubgroupSize is greater than or equal to <<limits-subgroupSize,
    pname:subgroupSize>>.
  * [[{anchor-prefix}limits-maxComputeWorkgroupSubgroups]]
    pname:maxComputeWorkgroupSubgroups is the maximum number of subgroups
    supported by the implementation within a workgroup.
  * [[{anchor-prefix}limits-requiredSubgroupSizeStages]]
    pname:requiredSubgroupSizeStages is a bitfield of what shader stages
    support having a required subgroup size specified.
```

## Excerpt: chapters/limits.adoc, lines 1543-1545 (VkPhysicalDeviceSubgroupSizeControlProperties, minSubgroupSize with quad operations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L1543-L1545

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/limits.html#VkPhysicalDeviceSubgroupSizeControlProperties

```text
If slink:VkPhysicalDeviceSubgroupProperties::pname:supportedOperations
includes <<features-subgroup-quad, ename:VK_SUBGROUP_FEATURE_QUAD_BIT>>,
pname:minSubgroupSize must: be greater than or equal to 4.
```

## Excerpt: chapters/limits.adoc, lines 3644-3653 (VkPhysicalDeviceCooperativeMatrixPropertiesKHR, cooperativeMatrixSupportedStages)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L3644-L3653

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/limits.html#limits-cooperativeMatrixSupportedStages

```text
  * [[limits-cooperativeMatrixSupportedStages]]
    pname:cooperativeMatrixSupportedStages is a bitfield of
    elink:VkShaderStageFlagBits describing the shader stages that
    cooperative matrix instructions are supported in.
    pname:cooperativeMatrixSupportedStages will have the
    ename:VK_SHADER_STAGE_COMPUTE_BIT bit set if any of the physical
    device's queues support ename:VK_QUEUE_COMPUTE_BIT.

pname:cooperativeMatrixSupportedStages must: not have any bits other than
ename:VK_SHADER_STAGE_COMPUTE_BIT set.
```

## Excerpt: chapters/limits.adoc, lines 3673-3686 (VkPhysicalDeviceCooperativeMatrix2PropertiesNV, members)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L3673-L3686

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/limits.html#limits-cooperativeMatrixWorkgroupScopeReservedSharedMemory

```text
  * [[limits-cooperativeMatrixWorkgroupScopeMaxWorkgroupSize]]
    pname:cooperativeMatrixWorkgroupScopeMaxWorkgroupSize is the maximum
    number of invocations in a workgroup when the module uses
    code:OpTypeCooperativeMatrixKHR with code:Scope equal to code:Workgroup.
  * [[limits-cooperativeMatrixFlexibleDimensionsMaxDimension]]
    pname:cooperativeMatrixFlexibleDimensionsMaxDimension is the maximum
    supported dimension for cooperative matrix types when the
    <<features-cooperativeMatrixFlexibleDimensions,pname:cooperativeMatrixFlexibleDimensions>>
    feature is enabled.
  * [[limits-cooperativeMatrixWorkgroupScopeReservedSharedMemory]]
    pname:cooperativeMatrixWorkgroupScopeReservedSharedMemory is the number
    of bytes of shared memory reserved for the implementation when the
    module uses code:OpTypeCooperativeMatrixKHR with code:Scope equal to
    code:Workgroup.
```

## Excerpt: chapters/limits.adoc, lines 6824-6827 (Required Limits, attribute definitions used in the table)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L6824-L6827

```text
:limit2022: Vulkan Roadmap 2022
:limit2024: Vulkan Roadmap 2024
:limit2026: Vulkan Roadmap 2026
:limit1_4: Vulkan 1.4
```

## Excerpt: chapters/limits.adoc, lines 6931-6937 (Required Limits table, rows maxComputeSharedMemorySize to maxComputeWorkGroupSize)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L6931-L6937

```text
| pname:maxComputeSharedMemorySize           | - | 16384 +
                                                   32768 ({limit2026}) | min
| pname:maxComputeWorkGroupCount             | - | (65535,65535,65535) | min
| pname:maxComputeWorkGroupInvocations       | - | 128 ({core}) +
                                                   256 ({limit2022}, {limit1_4})           | min
| pname:maxComputeWorkGroupSize              | - | (128,128,64) ({core}) +
                                                   (256,256,64) ({limit2022}, {limit1_4})  | min
```

## Excerpt: chapters/limits.adoc, line 7458 (Required Limits table, row cooperativeMatrixWorkgroupScopeReservedSharedMemory)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L7458

```text
| pname:cooperativeMatrixWorkgroupScopeReservedSharedMemory                  |   -   | [eq]#pname:maxComputeSharedMemorySize / 2#   | max
```

## Excerpt: chapters/limits.adoc, lines 7718-7723 (Roadmap 2022, table introduction and header)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L7718-L7723

```text
Implementations that claim support for the <<roadmap-2022, Roadmap 2022>>
milestone must: satisfy the following additional limit requirements:

[width="100%",cols="<35,<14,<11",options="header"]
|====
| Limit                                    | Supported Limit  | Limit Type^1^
```

## Excerpt: chapters/limits.adoc, lines 7742-7743 (Roadmap 2022 table, rows maxComputeWorkGroupInvocations and maxComputeWorkGroupSize)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L7742-L7743

```text
| pname:maxComputeWorkGroupInvocations        | 256           | min
| pname:maxComputeWorkGroupSize               | (256,256,64)  | min
```

## Excerpt: chapters/limits.adoc, lines 7791-7796 (Roadmap 2026, table introduction and header)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L7791-L7796

```text
Implementations that claim support for the <<roadmap-2026, Roadmap 2026>>
milestone must: satisfy the following additional limit requirements:

[width="100%",cols="<35,<14,<11",options="header"]
|====
| Limit                                                 | Supported Limit  | Limit Type^1^
```

## Excerpt: chapters/limits.adoc, line 7812 (Roadmap 2026 table, row maxComputeSharedMemorySize)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/limits.adoc#L7812

```text
| pname:maxComputeSharedMemorySize                      | 32768 | min
```

Licence of the excerpts: CC-BY-4.0, Copyright 2015-2026 The Khronos Group Inc. (file header, lines 1-2).
