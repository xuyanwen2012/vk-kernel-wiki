---
id: doc-vk-spec-spirvenv-cooperative-matrix-subgroups
title: 'Vulkan specification, SPIR-V environment appendix: cooperative-matrix, subgroup, workgroup and barrier validity rules'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- coopmat-shape
- full-subgroups
- subgroup-size
- shared-memory-limit
- workgroup-size-limit
- control-barrier
- memory-model
- spirv
retrieved_at: '2026-10-10'
---

# Vulkan specification, SPIR-V environment appendix: cooperative-matrix, subgroup, workgroup and barrier validity rules

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/spec/latest/appendices/spirvenv.html

## Excerpt: appendices/spirvenv.adoc, lines 187-192 (VUID-StandaloneSpirv-None-04636 and VUID-StandaloneSpirv-Scope-12243, execution scope and cooperative-matrix scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L187-L192

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-StandaloneSpirv-None-04636

```text
  * [[VUID-StandaloneSpirv-None-04636]]
    code:Scope for execution must: be limited to code:Workgroup or
    code:Subgroup
  * [[VUID-StandaloneSpirv-Scope-12243]]
    The code:Scope operand of code:OpTypeCooperativeMatrixKHR must: be
    limited to code:Workgroup or code:Subgroup
```

## Excerpt: appendices/spirvenv.adoc, lines 197-207 (VUID-StandaloneSpirv-None-04638, -ExecutionModel-07320 and -None-07321, memory scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L197-L207

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-StandaloneSpirv-None-04638

```text
  * [[VUID-StandaloneSpirv-None-04638]]
    code:Scope for memory must: be limited to code:Device, code:QueueFamily,
    code:Workgroup, code:ShaderCallKHR, code:Subgroup, or code:Invocation
  * [[VUID-StandaloneSpirv-ExecutionModel-07320]]
    If the {ExecutionModel} is code:TessellationControl, and the
    code:MemoryModel is code:GLSL450, the code:Scope for memory must: not be
    code:Workgroup
  * [[VUID-StandaloneSpirv-None-07321]]
    If the code:Scope for memory is code:Workgroup, then it must: only be
    used in the task, mesh, tessellation control, or compute
    {ExecutionModel}
```

## Excerpt: appendices/spirvenv.adoc, lines 218-221 (VUID-StandaloneSpirv-SubgroupVoteKHR-07951, Subgroup memory scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L218-L221

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-StandaloneSpirv-SubgroupVoteKHR-07951

```text
  * [[VUID-StandaloneSpirv-SubgroupVoteKHR-07951]]
    If none of the code:SubgroupVoteKHR, code:GroupNonUniform, or
    code:SubgroupBallotKHR capabilities are declared, code:Scope for memory
    must: not be code:Subgroup
```

## Excerpt: appendices/spirvenv.adoc, lines 234-236 (VUID-StandaloneSpirv-None-04645, Workgroup storage class)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L234-L236

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-StandaloneSpirv-None-04645

```text
  * [[VUID-StandaloneSpirv-None-04645]]
    If the {StorageClass} is code:Workgroup, then it must: only be used in
    the task, mesh, or compute {ExecutionModel}
```

## Excerpt: appendices/spirvenv.adoc, lines 588-591 (VUID-StandaloneSpirv-OpControlBarrier-04682)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L588-L591

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-StandaloneSpirv-OpControlBarrier-04682

```text
  * [[VUID-StandaloneSpirv-OpControlBarrier-04682]]
    If code:OpControlBarrier is used in ray generation, intersection,
    any-hit, closest hit, miss, fragment, vertex, tessellation evaluation,
    or geometry shaders, the execution Scope must: be code:Subgroup
```

## Excerpt: appendices/spirvenv.adoc, lines 842-846 (VUID-StandaloneSpirv-Pointer-08973, storage class of cooperative-matrix load and store pointers)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L842-L846

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-StandaloneSpirv-Pointer-08973

```text
  * [[VUID-StandaloneSpirv-Pointer-08973]]
    The {StorageClass} of the code:Pointer operand to
    code:OpCooperativeMatrixLoadKHR or code:OpCooperativeMatrixStoreKHR
    must: be limited to code:Workgroup, code:StorageBuffer, or
    code:PhysicalStorageBuffer
```

## Excerpt: appendices/spirvenv.adoc, lines 1633-1647 (VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10163, type must match an enumerated property)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L1633-L1647

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10163

```text
  * [[VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10163]]
    For code:OpTypeCooperativeMatrixKHR,
ifdef::VK_NV_cooperative_matrix2[]
    if the <<features-cooperativeMatrixFlexibleDimensions,
    pname:cooperativeMatrixFlexibleDimensions>> feature is not enabled,
endif::VK_NV_cooperative_matrix2[]
ifdef::VK_EXT_cooperative_matrix_maintenance1[]
    if the <<features-cooperativeMatrixProperties2EXT,
    slink:VkPhysicalDeviceCooperativeMatrixMaintenance1FeaturesEXT::pname:cooperativeMatrixProperties2>>
    feature is not enabled,
endif::VK_EXT_cooperative_matrix_maintenance1[]
    the type must: match one of the supported
    slink:VkCooperativeMatrixPropertiesKHR structures as defined in
    <<shaders-cooperative-matrix-properties-khr-type-matching,
    VkCooperativeMatrixPropertiesKHR Type Matching>>
```

## Excerpt: appendices/spirvenv.adoc, lines 1648-1662 (VUID-RuntimeSpirv-OpCooperativeMatrixMulAddKHR-10060, multiply-add operands must match an enumerated property)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L1648-L1662

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-OpCooperativeMatrixMulAddKHR-10060

```text
  * [[VUID-RuntimeSpirv-OpCooperativeMatrixMulAddKHR-10060]]
    For code:OpCooperativeMatrixMulAddKHR,
ifdef::VK_NV_cooperative_matrix2[]
    if the <<features-cooperativeMatrixFlexibleDimensions,
    pname:cooperativeMatrixFlexibleDimensions>> feature is not enabled,
endif::VK_NV_cooperative_matrix2[]
ifdef::VK_EXT_cooperative_matrix_maintenance1[]
    if the <<features-cooperativeMatrixProperties2EXT,
    slink:VkPhysicalDeviceCooperativeMatrixMaintenance1FeaturesEXT::pname:cooperativeMatrixProperties2>>
    feature is not enabled,
endif::VK_EXT_cooperative_matrix_maintenance1[]
    the operands must: match a supported
    slink:VkCooperativeMatrixPropertiesKHR structure as defined in
    <<shaders-cooperative-matrix-properties-khr-muladd-matching,
    VkCooperativeMatrixPropertiesKHR Multiply-Add Matching>>
```

## Excerpt: appendices/spirvenv.adoc, lines 1678-1685 (VUID-RuntimeSpirv-cooperativeMatrixWorkgroupScope-10164)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L1678-L1685

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-cooperativeMatrixWorkgroupScope-10164

```text
  * [[VUID-RuntimeSpirv-cooperativeMatrixWorkgroupScope-10164]]
ifdef::VK_NV_cooperative_matrix2[]
    If the <<features-cooperativeMatrixWorkgroupScope,
    pname:cooperativeMatrixWorkgroupScope>> feature is not enabled, the
endif::VK_NV_cooperative_matrix2[]
ifndef::VK_NV_cooperative_matrix2[The]
    scope of all code:OpTypeCooperativeMatrixKHR must: not be
    elink:VkScopeKHR::ename:VK_SCOPE_WORKGROUP_KHR
```

## Excerpt: appendices/spirvenv.adoc, lines 1766-1773 (VUID-RuntimeSpirv-maxComputeSharedMemorySize-10168, shared memory with workgroup-scope matrices)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L1766-L1773

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-maxComputeSharedMemorySize-10168

```text
  * [[VUID-RuntimeSpirv-maxComputeSharedMemorySize-10168]]
    If the module uses code:OpTypeCooperativeMatrixKHR with code:Scope equal
    to code:Workgroup, the sum of size in bytes for variables and
    <<workgroup-padding, padding>> in the code:Workgroup {StorageClass} in
    the code:GLCompute {ExecutionModel} must: be less than or equal to
    <<limits-maxComputeSharedMemorySize, pname:maxComputeSharedMemorySize>>
    minus
    <<limits-cooperativeMatrixWorkgroupScopeReservedSharedMemory,pname:cooperativeMatrixWorkgroupScopeReservedSharedMemory>>
```

## Excerpt: appendices/spirvenv.adoc, lines 1782-1790 (VUID-RuntimeSpirv-cooperativeMatrixSupportedStages-08985 and VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10770, full subgroups or SPIR-V 1.6)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L1782-L1790

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10770

```text
  * [[VUID-RuntimeSpirv-cooperativeMatrixSupportedStages-08985]]
    code:OpTypeCooperativeMatrixKHR and code:OpCooperativeMatrix*
    instructions must: not be used in shader stages not included in
    slink:VkPhysicalDeviceCooperativeMatrixPropertiesKHR::pname:cooperativeMatrixSupportedStages
  * [[VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10770]]
    Any pipeline containing a shader with code:OpTypeCooperativeMatrixKHR or
    code:OpCooperativeMatrix*KHR instructions must: be created with the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT flag or
    the shader module must be version 1.6 or greater
```

## Excerpt: appendices/spirvenv.adoc, lines 1793-1797 (VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10771, shader objects)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L1793-L1797

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10771

```text
  * [[VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10771]]
    Any shader object containing code:OpTypeCooperativeMatrixKHR or
    code:OpCooperativeMatrix*KHR instructions must: be created with the
    ename:VK_SHADER_CREATE_REQUIRE_FULL_SUBGROUPS_BIT_EXT flag or the shader
    module must be version 1.6 or greater
```

## Excerpt: appendices/spirvenv.adoc, lines 2666-2682 (VUID-RuntimeSpirv-x-06429, -y-06430, -z-06431 and -x-06432, compute local workgroup size)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L2666-L2682

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-x-06429

```text
  * [[VUID-RuntimeSpirv-x-06429]]
    In compute shaders using the code:GLCompute {ExecutionModel} the pname:x
    size in code:LocalSize or code:LocalSizeId must: be less than or equal
    to slink:VkPhysicalDeviceLimits::pname:maxComputeWorkGroupSize[0]
  * [[VUID-RuntimeSpirv-y-06430]]
    In compute shaders using the code:GLCompute {ExecutionModel} the pname:y
    size in code:LocalSize or code:LocalSizeId must: be less than or equal
    to slink:VkPhysicalDeviceLimits::pname:maxComputeWorkGroupSize[1]
  * [[VUID-RuntimeSpirv-z-06431]]
    In compute shaders using the code:GLCompute {ExecutionModel} the pname:z
    size in code:LocalSize or code:LocalSizeId must: be less than or equal
    to slink:VkPhysicalDeviceLimits::pname:maxComputeWorkGroupSize[2]
  * [[VUID-RuntimeSpirv-x-06432]]
    In compute shaders using the code:GLCompute {ExecutionModel} the product
    of pname:x size, pname:y size, and pname:z size in code:LocalSize or
    code:LocalSizeId must: be less than or equal to
    slink:VkPhysicalDeviceLimits::pname:maxComputeWorkGroupInvocations
```

## Excerpt: appendices/spirvenv.adoc, lines 2717-2721 (VUID-RuntimeSpirv-Workgroup-06530, Workgroup storage class size)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L2717-L2721

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-Workgroup-06530

```text
  * [[VUID-RuntimeSpirv-Workgroup-06530]]
    The sum of size in bytes for variables and <<workgroup-padding,
    padding>> in the code:Workgroup {StorageClass} in the code:GLCompute
    {ExecutionModel} must: be less than or equal to
    <<limits-maxComputeSharedMemorySize, pname:maxComputeSharedMemorySize>>
```

## Excerpt: appendices/spirvenv.adoc, lines 3034-3041 (VUID-RuntimeSpirv-OpControlBarrierArriveEXT-13562, shared memory with split barriers)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/spirvenv.adoc#L3034-L3041

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/spirvenv.html#VUID-RuntimeSpirv-OpControlBarrierArriveEXT-13562

```text
  * [[VUID-RuntimeSpirv-OpControlBarrierArriveEXT-13562]]
    If the module uses code:OpControlBarrierArriveEXT or
    code:OpControlBarrierWaitEXT, the sum of size in bytes for variables and
    <<workgroup-padding, padding>> in the code:Workgroup {StorageClass} in
    the code:GLCompute {ExecutionModel} must: be less than or equal to
    <<limits-maxComputeSharedMemorySize, pname:maxComputeSharedMemorySize>>
    minus
    <<limits-splitBarrierReservedSharedMemory,pname:splitBarrierReservedSharedMemory>>
```

Licence of the excerpts: CC-BY-4.0, Copyright 2015-2026 The Khronos Group Inc. (file header, lines 1-2).
