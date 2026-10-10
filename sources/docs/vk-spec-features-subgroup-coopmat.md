---
id: doc-vk-spec-features-subgroup-coopmat
title: 'Vulkan specification, Features chapter: cooperative-matrix feature structures, subgroupSizeControl and computeFullSubgroups'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/features.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- full-subgroups
- subgroup-size-control
retrieved_at: '2026-10-10'
---

# Vulkan specification, Features chapter: cooperative-matrix feature structures, subgroupSizeControl and computeFullSubgroups

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/spec/latest/chapters/features.html

## Excerpt: chapters/features.adoc, lines 3143-3150 (VkPhysicalDeviceCooperativeMatrixFeaturesKHR, members)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/features.adoc#L3143-L3150

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/features.html#VkPhysicalDeviceCooperativeMatrixFeaturesKHR

```text
  * [[features-cooperativeMatrix]] pname:cooperativeMatrix indicates that
    the implementation supports the code:CooperativeMatrixKHR SPIR-V
    capability.
  * [[features-cooperativeMatrixRobustBufferAccess]]
    pname:cooperativeMatrixRobustBufferAccess indicates that the
    implementation supports <<shaders-robust-buffer-access, robust buffer
    access>> for SPIR-V code:OpCooperativeMatrixLoadKHR and
    code:OpCooperativeMatrixStoreKHR instructions.
```

## Excerpt: chapters/features.adoc, lines 3196-3229 (VkPhysicalDeviceCooperativeMatrix2FeaturesNV, members)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/features.adoc#L3196-L3229

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/features.html#VkPhysicalDeviceCooperativeMatrix2FeaturesNV

```text
  * [[features-cooperativeMatrixWorkgroupScope]]
    pname:cooperativeMatrixWorkgroupScope indicates that the implementation
    supports workgroup scope cooperative matrices.
  * [[features-cooperativeMatrixFlexibleDimensions]]
    pname:cooperativeMatrixFlexibleDimensions indicates that the
    implementation supports cooperative matrix sizes that are a multiple of
    the granularity advertised in
    slink:VkCooperativeMatrixFlexibleDimensionsPropertiesNV.
  * [[features-cooperativeMatrixReductions]]
    pname:cooperativeMatrixReductions indicates that the implementation
    supports the code:CooperativeMatrixReductionsNV SPIR-V capability.
    This allows performing (row, column, 2x2, or all element) reductions on
    matrices.
  * [[features-cooperativeMatrixConversions]]
    pname:cooperativeMatrixConversions indicates that the implementation
    supports the code:CooperativeMatrixConversionsNV SPIR-V capability.
    This allows converting accumulator matrices to A or B matrices.
  * [[features-cooperativeMatrixPerElementOperations]]
    pname:cooperativeMatrixPerElementOperations indicates that the
    implementation supports the code:CooperativeMatrixPerElementOperationsNV
    SPIR-V capability.
    This allows performing element-wise operations on matrix elements using
    a callback function.
  * [[features-cooperativeMatrixTensorAddressing]]
    pname:cooperativeMatrixTensorAddressing indicates that the
    implementation supports the code:TensorAddressingNV and
    code:CooperativeMatrixTensorAddressingNV SPIR-V capabilities.
    This allows using tensor layout and tensor view types for matrix loads
    and stores.
  * [[features-cooperativeMatrixBlockLoads]]
    pname:cooperativeMatrixBlockLoads indicates that the implementation
    supports the code:CooperativeMatrixBlockLoadsNV SPIR-V capability.
    This allows setting block size for loads and using a callback function
    to decode block elements.
```

## Excerpt: chapters/features.adoc, lines 3279-3301 (VkPhysicalDeviceCooperativeMatrixMaintenance1FeaturesEXT, members)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/features.adoc#L3279-L3301

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/features.html#VkPhysicalDeviceCooperativeMatrixMaintenance1FeaturesEXT

```text
  * [[features-cooperativeMatrixProperties2EXT]]
    pname:cooperativeMatrixProperties2 indicates that the implementation
    supports the flink:vkGetPhysicalDeviceCooperativeMatrixProperties2EXT
    command.
  * [[features-cooperativeMatrixReductionsEXT]]
    pname:cooperativeMatrixReductions indicates that the implementation
    supports the code:CooperativeMatrixReductionsEXT SPIR-V capability.
    This allows performing (row, column, 2x2, or all element) reductions on
    matrices.
  * [[features-cooperativeMatrixConversionsEXT]]
    pname:cooperativeMatrixConversions indicates that the implementation
    supports the code:CooperativeMatrixConversionsEXT SPIR-V capability.
    This allows converting accumulator matrices to A or B matrices.
  * [[features-cooperativeMatrixPerElementOperationsEXT]]
    pname:cooperativeMatrixPerElementOperations indicates that the
    implementation supports the
    code:CooperativeMatrixPerElementOperationsEXT SPIR-V capability.
    This allows performing element-wise operations on matrix elements using
    a callback function.
  * [[features-cooperativeMatrixGetCoordinateEXT]]
    pname:cooperativeMatrixGetCoordinate indicates that the implementation
    supports the code:CooperativeMatrixGetCoordinateEXT SPIR-V capability.
    This allows querying locations for a matrix element.
```

## Excerpt: chapters/features.adoc, lines 4265-4278 (VkPhysicalDeviceSubgroupSizeControlFeatures, subgroupSizeControl and computeFullSubgroups)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/features.adoc#L4265-L4278

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/features.html#VkPhysicalDeviceSubgroupSizeControlFeatures

```text
  * [[{anchor-prefix}features-subgroupSizeControl]]
    pname:subgroupSizeControl indicates whether the implementation supports
    controlling shader subgroup sizes via the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT
    flag and the slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo
    structure.
  * [[{anchor-prefix}features-computeFullSubgroups]]
    pname:computeFullSubgroups indicates whether the implementation supports
    requiring full subgroups in compute
ifdef::VK_NV_mesh_shader[]
    , mesh, or task
endif::VK_NV_mesh_shader[]
    shaders via the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT flag.
```

## Excerpt: chapters/features.adoc, lines 4287-4292 (VkPhysicalDeviceSubgroupSizeControlFeatures, note on version 1 of the extension)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/features.adoc#L4287-L4292

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/features.html#VkPhysicalDeviceSubgroupSizeControlFeatures

```text
The sname:VkPhysicalDeviceSubgroupSizeControlFeaturesEXT structure was added
in version 2 of the `apiext:VK_EXT_subgroup_size_control` extension.
Version 1 implementations of this extension will not fill out the features
structure but applications may assume that both pname:subgroupSizeControl
and pname:computeFullSubgroups are supported if the extension is supported.
(See also the <<features-requirements, Feature Requirements>> section.)
```

Licence of the excerpts: CC-BY-4.0, Copyright 2015-2026 The Khronos Group Inc. (file header, lines 1-2).
