---
id: doc-vk-gl-cts-subgroup-size-control-tests
title: 'VK-GL-CTS: subgroup size control compute tests (dEQP-VK.subgroups.size_control.compute)'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/subgroups/vktSubgroupsSizeControlTests.cpp
source_category: upstream-code
architectures: []
tags:
- subgroup-size
- subgroup-size-control
- required-subgroup-size
retrieved_at: '2026-10-10'
description: C++ source of the conformance tests; the compute cases for varying, full and required subgroup sizes
---

# VK-GL-CTS: subgroup size control compute tests (dEQP-VK.subgroups.size_control.compute)

## Excerpt: external/vulkancts/modules/vulkan/subgroups/vktSubgroupsSizeControlTests.cpp, lines 241-263 (checkComputeRequireFull: expected subgroup count from local size and required size)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/subgroups/vktSubgroupsSizeControlTests.cpp#L241-L263

```text
static bool checkComputeRequireFull(const void *internalData, vector<const void *> datas,
                                    const uint32_t numWorkgroups[3], const uint32_t localSize[3], uint32_t)
{
    const struct internalDataStruct *checkInternalData =
        reinterpret_cast<const struct internalDataStruct *>(internalData);
    const Context *context                    = checkInternalData->context;
    const auto &subgroupSizeControlProperties = context->getSubgroupSizeControlProperties();
    TestLog &log                              = context->getTestContext().getLog();
    const uint32_t globalSizeX                = numWorkgroups[0] * localSize[0];
    const uint32_t globalSizeY                = numWorkgroups[1] * localSize[1];
    const uint32_t globalSizeZ                = numWorkgroups[2] * localSize[2];
    const uint32_t width                      = globalSizeX * globalSizeY * globalSizeZ;
    const UVec4 *data                         = reinterpret_cast<const UVec4 *>(datas[0]);
    const uint32_t numSubgroups =
        (localSize[0] * localSize[1] * localSize[2]) / checkInternalData->requiredSubgroupSize;
    const bool exactSubgroupSize =
        (checkInternalData->caseDef.shaderUsesFullSubgroups() && checkInternalData->isRequiredSubgroupSize);

    for (uint32_t i = 0; i < width; i++)
    {
        if (data[i].x() > subgroupSizeControlProperties.maxSubgroupSize ||
            data[i].x() < subgroupSizeControlProperties.minSubgroupSize)
        {
```

## Excerpt: external/vulkancts/modules/vulkan/subgroups/vktSubgroupsSizeControlTests.cpp, lines 1103-1134 (require-full-subgroups and required-size cases (compute only))

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/subgroups/vktSubgroupsSizeControlTests.cpp#L1103-L1134

```text
        // Require full subgroups cases (only compute shaders).
        const uint32_t flagsFull         = VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT_EXT;
        const CaseDefinition caseDefFull = {params.flagsEnabled ? flagsFull : 0u,
                                            VK_SHADER_STAGE_COMPUTE_BIT,
                                            true,
                                            REQUIRED_SUBGROUP_SIZE_NONE,
                                            de::SharedPtr<bool>(new bool),
                                            params.useSpirv16 ? SPIRV_VERSION_1_6 : SPIRV_VERSION_1_3};
        addFunctionCaseWithPrograms(computeGroup.get(), "require_full_subgroups" + params.postfix,
                                    supportedCheckFeatures, initProgramsRequireFull, testRequireFullSubgroups,
                                    caseDefFull);

        // Tests to check setting a required subgroup size value, together with require full subgroups (only compute shaders).
        const CaseDefinition caseDefMaxFull = {params.flagsEnabled ? flagsFull : 0u,
                                               VK_SHADER_STAGE_COMPUTE_BIT,
                                               true,
                                               REQUIRED_SUBGROUP_SIZE_MAX,
                                               de::SharedPtr<bool>(new bool),
                                               params.useSpirv16 ? SPIRV_VERSION_1_6 : SPIRV_VERSION_1_3};
        addFunctionCaseWithPrograms(
            computeGroup.get(), "required_subgroup_size_max_require_full_subgroups" + params.postfix,
            supportedCheckFeatures, initProgramsRequireFull, testRequireSubgroupSize, caseDefMaxFull);

        const CaseDefinition caseDefMinFull = {params.flagsEnabled ? flagsFull : 0u,
                                               VK_SHADER_STAGE_COMPUTE_BIT,
                                               true,
                                               REQUIRED_SUBGROUP_SIZE_MIN,
                                               de::SharedPtr<bool>(new bool),
                                               params.useSpirv16 ? SPIRV_VERSION_1_6 : SPIRV_VERSION_1_3};
        addFunctionCaseWithPrograms(
            computeGroup.get(), "required_subgroup_size_min_require_full_subgroups" + params.postfix,
            supportedCheckFeatures, initProgramsRequireFull, testRequireSubgroupSize, caseDefMinFull);
```

## Excerpt: external/vulkancts/modules/vulkan/subgroups/vktSubgroupsSizeControlTests.cpp, lines 1160-1167 (required_subgroup_size_max)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/subgroups/vktSubgroupsSizeControlTests.cpp#L1160-L1167

```text
        const CaseDefinition caseDefComputeMax = {0u,
                                                  VK_SHADER_STAGE_COMPUTE_BIT,
                                                  false,
                                                  REQUIRED_SUBGROUP_SIZE_MAX,
                                                  de::SharedPtr<bool>(new bool),
                                                  SPIRV_VERSION_1_3};
        addFunctionCaseWithPrograms(computeGroup.get(), "required_subgroup_size_max", supportedCheckFeatures,
                                    initPrograms, testRequireSubgroupSize, caseDefComputeMax);
```

## Excerpt: external/vulkancts/mustpass/main/vk-default/subgroups.txt, lines 47660-47676 (compute case names in the main must-pass list)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/mustpass/main/vk-default/subgroups.txt#L47660-L47676

```text
dEQP-VK.subgroups.size_control.compute.allow_varying_subgroup_size
dEQP-VK.subgroups.size_control.compute.allow_varying_subgroup_size_flags_spirv16
dEQP-VK.subgroups.size_control.compute.allow_varying_subgroup_size_spirv16
dEQP-VK.subgroups.size_control.compute.require_full_subgroups
dEQP-VK.subgroups.size_control.compute.require_full_subgroups_allow_varying_subgroup_size
dEQP-VK.subgroups.size_control.compute.require_full_subgroups_allow_varying_subgroup_size_flags_spirv16
dEQP-VK.subgroups.size_control.compute.require_full_subgroups_allow_varying_subgroup_size_spirv16
dEQP-VK.subgroups.size_control.compute.require_full_subgroups_flags_spirv16
dEQP-VK.subgroups.size_control.compute.require_full_subgroups_spirv16
dEQP-VK.subgroups.size_control.compute.required_subgroup_size_max
dEQP-VK.subgroups.size_control.compute.required_subgroup_size_max_require_full_subgroups
dEQP-VK.subgroups.size_control.compute.required_subgroup_size_max_require_full_subgroups_flags_spirv16
dEQP-VK.subgroups.size_control.compute.required_subgroup_size_max_require_full_subgroups_spirv16
dEQP-VK.subgroups.size_control.compute.required_subgroup_size_min
dEQP-VK.subgroups.size_control.compute.required_subgroup_size_min_require_full_subgroups
dEQP-VK.subgroups.size_control.compute.required_subgroup_size_min_require_full_subgroups_flags_spirv16
dEQP-VK.subgroups.size_control.compute.required_subgroup_size_min_require_full_subgroups_spirv16
```

Licence of the excerpts: Apache-2.0 (`LICENSE` of the repository; copyright notices are in the file header).
