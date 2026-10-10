---
id: doc-vk-spec-pipeline-shader-stage-subgroup-flags
title: 'Vulkan specification, Pipelines chapter: VkPipelineShaderStageCreateInfo subgroup flags, required subgroup size and local-size divisibility rules'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc
source_category: official-doc
architectures: []
tags:
- full-subgroups
- subgroup-size-control
- required-subgroup-size
- subgroup-size
- cooperative-matrix
- cooperative-matrix2
- workgroup-size-limit
retrieved_at: '2026-10-10'
---

# Vulkan specification, Pipelines chapter: VkPipelineShaderStageCreateInfo subgroup flags, required subgroup size and local-size divisibility rules

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/spec/latest/chapters/pipelines.html

## Excerpt: chapters/pipelines.adoc, lines 1257-1275 (VUID-VkPipelineShaderStageCreateInfo-flags-02784, -flags-02785 and -flags-08988)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1257-L1275

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VUID-VkPipelineShaderStageCreateInfo-flags-02785

```text
  * [[VUID-VkPipelineShaderStageCreateInfo-flags-02784]]
    If pname:flags has the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT
    flag set, the <<features-subgroupSizeControl,
    pname:subgroupSizeControl>> feature must: be enabled
  * [[VUID-VkPipelineShaderStageCreateInfo-flags-02785]]
    If pname:flags has the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT flag
    set, the <<features-computeFullSubgroups, pname:computeFullSubgroups>>
    feature must: be enabled
  * [[VUID-VkPipelineShaderStageCreateInfo-flags-08988]]
    If pname:flags includes
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT,
    pname:stage must: be
ifdef::VK_NV_mesh_shader,VK_EXT_mesh_shader[]
    one of ename:VK_SHADER_STAGE_MESH_BIT_EXT,
    ename:VK_SHADER_STAGE_TASK_BIT_EXT, or
endif::VK_NV_mesh_shader,VK_EXT_mesh_shader[]
    ename:VK_SHADER_STAGE_COMPUTE_BIT
```

## Excerpt: chapters/pipelines.adoc, lines 1276-1296 (VUID-VkPipelineShaderStageCreateInfo-pNext-02754, -pNext-02755 and -pNext-02756)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1276-L1296

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VUID-VkPipelineShaderStageCreateInfo-pNext-02756

```text
  * [[VUID-VkPipelineShaderStageCreateInfo-pNext-02754]]
    If a slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo structure
    is included in the pname:pNext chain, pname:flags must: not have the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT
    flag set
  * [[VUID-VkPipelineShaderStageCreateInfo-pNext-02755]]
    If a slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo structure
    is included in the pname:pNext chain, the
    <<features-subgroupSizeControl, pname:subgroupSizeControl>> feature
    must: be enabled, and pname:stage must: be a valid bit specified in
    <<limits-requiredSubgroupSizeStages, pname:requiredSubgroupSizeStages>>
  * [[VUID-VkPipelineShaderStageCreateInfo-pNext-02756]]
    If a slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo structure
    is included in the pname:pNext chain and pname:stage is
    ename:VK_SHADER_STAGE_COMPUTE_BIT,
ifdef::VK_NV_mesh_shader,VK_EXT_mesh_shader[ename:VK_SHADER_STAGE_MESH_BIT_EXT, or ename:VK_SHADER_STAGE_TASK_BIT_EXT,]
    the local workgroup size of the shader must: be less than or equal to
    the product of
    slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo::pname:requiredSubgroupSize
    and <<limits-maxComputeWorkgroupSubgroups,
    pname:maxComputeWorkgroupSubgroups>>
```

## Excerpt: chapters/pipelines.adoc, lines 1297-1303 (VUID-VkPipelineShaderStageCreateInfo-pNext-02757, X dimension a multiple of requiredSubgroupSize)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1297-L1303

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VUID-VkPipelineShaderStageCreateInfo-pNext-02757

```text
  * [[VUID-VkPipelineShaderStageCreateInfo-pNext-02757]]
    If a slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo structure
    is included in the pname:pNext chain, and pname:flags has the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT flag
    set, the local workgroup size in the X dimension of the pipeline must:
    be a multiple of
    slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo::pname:requiredSubgroupSize
```

## Excerpt: chapters/pipelines.adoc, lines 1304-1319 (VUID-VkPipelineShaderStageCreateInfo-flags-02758 and -flags-02759)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1304-L1319

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VUID-VkPipelineShaderStageCreateInfo-flags-02759

```text
  * [[VUID-VkPipelineShaderStageCreateInfo-flags-02758]]
    If pname:flags has both the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT and
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT
    flags set, the local workgroup size in the X dimension of the pipeline
    must: be a multiple of <<limits-maxSubgroupSize, pname:maxSubgroupSize>>
  * [[VUID-VkPipelineShaderStageCreateInfo-flags-02759]]
    If pname:flags has the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT flag
    set and pname:flags does not have the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT
    flag set and no
    slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo structure is
    included in the pname:pNext chain, the local workgroup size in the X
    dimension of the pipeline must: be a multiple of <<limits-subgroupSize,
    pname:subgroupSize>>
```

## Excerpt: chapters/pipelines.adoc, lines 1321-1325 (VUID-VkPipelineShaderStageCreateInfo-module-08987, subgroup-scope cooperative matrix)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1321-L1325

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VUID-VkPipelineShaderStageCreateInfo-module-08987

```text
  * [[VUID-VkPipelineShaderStageCreateInfo-module-08987]]
    If pname:module uses the code:OpTypeCooperativeMatrixKHR instruction
    with a code:Scope equal to code:Subgroup, then the local workgroup size
    in the X dimension of the pipeline must: be a multiple of the
    <<interfaces-builtin-variables-sgs,effective subgroup size>>
```

## Excerpt: chapters/pipelines.adoc, lines 1329-1337 (VUID-VkPipelineShaderStageCreateInfo-module-10169, workgroup-scope cooperative matrix)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1329-L1337

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VUID-VkPipelineShaderStageCreateInfo-module-10169

```text
  * [[VUID-VkPipelineShaderStageCreateInfo-module-10169]]
    If pname:module uses the code:OpTypeCooperativeMatrixKHR instruction
    with a code:Scope equal to code:Workgroup, then the local workgroup size
    in the X dimension of the pipeline must: be a multiple of the
    <<interfaces-builtin-variables-sgs,effective subgroup size>> and the
    total local workgroup size must: be a power of two multiple of the
    <<interfaces-builtin-variables-sgs,effective subgroup size>> and must:
    be less than or equal to
    <<limits-cooperativeMatrixWorkgroupScopeMaxWorkgroupSize,cooperativeMatrixWorkgroupScopeMaxWorkgroupSize>>
```

## Excerpt: chapters/pipelines.adoc, lines 1422-1443 (VkPipelineShaderStageCreateFlagBits, flag descriptions and note)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1422-L1443

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VkPipelineShaderStageCreateFlagBits

```text
  * ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT
    specifies that the
    <<interfaces-builtin-variables-sgs,code:SubgroupSize>> may: vary in the
    shader stage.
  * ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT
    specifies that the subgroup sizes must: be launched with all invocations
    active in the
ifdef::VK_NV_mesh_shader,VK_EXT_mesh_shader[task, mesh, or]
    compute stage.

[NOTE]
====
If ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT_EXT
and ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT_EXT are
specified and <<limits-minSubgroupSize, pname:minSubgroupSize>> does not
equal <<limits-maxSubgroupSize, pname:maxSubgroupSize>> and no
<<shaders-required-subgroup-size, required subgroup size>> is specified,
then the only way to guarantee that the 'X' dimension of the local workgroup
size is a multiple of <<interfaces-builtin-variables-sgs,
code:SubgroupSize>> is to make it a multiple of pname:maxSubgroupSize.
Under these conditions, you are guaranteed full subgroups but not any
particular subgroup size.
```

## Excerpt: chapters/pipelines.adoc, lines 1524-1530 (VkPipelineShaderStageRequiredSubgroupSizeCreateInfo, member description)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1524-L1530

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VkPipelineShaderStageRequiredSubgroupSizeCreateInfo

```text
  * pname:requiredSubgroupSize is an unsigned integer value specifying the
    required subgroup size for the newly created pipeline shader stage.

If a sname:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo structure is
included in the pname:pNext chain of slink:VkPipelineShaderStageCreateInfo,
it specifies that the pipeline shader stage being compiled has a required
subgroup size.
```

## Excerpt: chapters/pipelines.adoc, lines 1540-1547 (VUID-VkPipelineShaderStageRequiredSubgroupSizeCreateInfo-requiredSubgroupSize-02760, -02761 and -02762)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/pipelines.adoc#L1540-L1547

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/pipelines.html#VUID-VkPipelineShaderStageRequiredSubgroupSizeCreateInfo-requiredSubgroupSize-02760

```text
  * [[VUID-VkPipelineShaderStageRequiredSubgroupSizeCreateInfo-requiredSubgroupSize-02760]]
    pname:requiredSubgroupSize must: be a power-of-two integer
  * [[VUID-VkPipelineShaderStageRequiredSubgroupSizeCreateInfo-requiredSubgroupSize-02761]]
    pname:requiredSubgroupSize must: be greater than or equal to
    <<limits-minSubgroupSize, pname:minSubgroupSize>>
  * [[VUID-VkPipelineShaderStageRequiredSubgroupSizeCreateInfo-requiredSubgroupSize-02762]]
    pname:requiredSubgroupSize must: be less than or equal to
    <<limits-maxSubgroupSize, pname:maxSubgroupSize>>
```

Licence of the excerpts: CC-BY-4.0, Copyright 2015-2026 The Khronos Group Inc. (file header, lines 1-2).
