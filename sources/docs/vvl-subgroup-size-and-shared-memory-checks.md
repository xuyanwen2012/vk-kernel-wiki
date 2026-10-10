---
id: doc-vvl-subgroup-size-and-shared-memory-checks
title: 'Vulkan-ValidationLayers: required subgroup size, full subgroups, workgroup size and shared-memory size checks'
author: The Khronos Group Inc., Valve Corporation, LunarG, Inc.
url: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv.cpp
source_category: upstream-code
architectures: []
tags:
- subgroup-size
- subgroup-size-control
- required-subgroup-size
- shared-memory-limit
- cooperative-matrix2
retrieved_at: '2026-10-10'
description: C++ source of the validation layer; file and VUID locators for compute-shader subgroup and shared-memory checks
---

# Vulkan-ValidationLayers: required subgroup size, full subgroups, workgroup size and shared-memory size checks

## Excerpt: layers/core_checks/cc_spirv.cpp, lines 463-475 (ValidateWorkgroupSharedMemory: VUID-RuntimeSpirv-Workgroup-06530)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv.cpp#L463-L475

```text
bool CoreChecks::ValidateWorkgroupSharedMemory(const spirv::Module& module_state, const spirv::EntryPoint& entrypoint,
                                               VkShaderStageFlagBits stage, const Location& loc) const {
    bool skip = false;

    const uint32_t total_workgroup_shared_memory = module_state.CalculateWorkgroupSharedMemory();

    if (stage == VK_SHADER_STAGE_COMPUTE_BIT) {
        if (total_workgroup_shared_memory > phys_dev_props.limits.maxComputeSharedMemorySize) {
            skip |= LogError(
                "VUID-RuntimeSpirv-Workgroup-06530", module_state.handle(), loc,
                "shader %s uses %" PRIu32 " bytes of shared memory, which is more than maxComputeSharedMemorySize (%" PRIu32 ").",
                entrypoint.Describe().c_str(), total_workgroup_shared_memory, phys_dev_props.limits.maxComputeSharedMemorySize);
        }
```

## Excerpt: layers/core_checks/cc_spirv.cpp, lines 477-500 (VUID-RuntimeSpirv-maxComputeSharedMemorySize-10168: workgroup-scope cooperative matrices reserve shared memory)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv.cpp#L477-L500

```text
        if (enabled_features.cooperativeMatrixWorkgroupScopeNV) {
            for (auto& cooperative_matrix_inst : module_state.static_data_.cooperative_matrix_inst) {
                if (cooperative_matrix_inst->Opcode() != spv::OpTypeCooperativeMatrixKHR) {
                    continue;
                }
                auto scope = module_state.GetAnyConstantDef(cooperative_matrix_inst->Word(3));
                if (!scope || scope->GetConstantValue() != VK_SCOPE_WORKGROUP_KHR) {
                    continue;
                }
                if (total_workgroup_shared_memory >
                    phys_dev_props.limits.maxComputeSharedMemorySize -
                        phys_dev_ext_props.cooperative_matrix_props2_nv.cooperativeMatrixWorkgroupScopeReservedSharedMemory) {
                    skip |= LogError(
                        "VUID-RuntimeSpirv-maxComputeSharedMemorySize-10168", module_state.handle(), loc,
                        "shader %s uses %" PRIu32 " bytes of shared memory, which is more than maxComputeSharedMemorySize (%" PRIu32
                        ") minus "
                        "cooperativeMatrixWorkgroupScopeReservedSharedMemory (%" PRIu32 ").",
                        entrypoint.Describe().c_str(), total_workgroup_shared_memory,
                        phys_dev_props.limits.maxComputeSharedMemorySize,
                        phys_dev_ext_props.cooperative_matrix_props2_nv.cooperativeMatrixWorkgroupScopeReservedSharedMemory);
                    break;
                }
            }
        }
```

## Excerpt: layers/core_checks/cc_spirv.cpp, lines 1623-1651 (ValidateRequiredSubgroupSize: VUID-VkPipelineShaderStageCreateInfo-pNext-02755 / -02756)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv.cpp#L1623-L1651

```text
bool CoreChecks::ValidateRequiredSubgroupSize(const spirv::Module& module_state, const spirv::EntryPoint& entrypoint,
                                              const ShaderStageState& stage_state, uint64_t invocations,
                                              const spirv::LocalSize& local_size, const Location& loc) const {
    bool skip = false;

    const auto* required_subgroup_size_ci =
        vku::FindStructInPNextChain<VkPipelineShaderStageRequiredSubgroupSizeCreateInfo>(stage_state.GetPNext());
    if (!required_subgroup_size_ci) return skip;

    const Location pNext_loc = loc.pNext(Struct::VkPipelineShaderStageRequiredSubgroupSizeCreateInfo);

    const uint32_t required_subgroup_size = required_subgroup_size_ci->requiredSubgroupSize;
    if (!enabled_features.subgroupSizeControl) {
        skip |= LogError("VUID-VkPipelineShaderStageCreateInfo-pNext-02755", module_state.handle(), pNext_loc,
                         "the subgroupSizeControl feature was not enabled\n%s",
                         PrintPNextChain(Struct::Empty, stage_state.GetPNext()).c_str());
    }
    if ((phys_dev_props_core13.requiredSubgroupSizeStages & stage_state.GetStage()) == 0) {
        skip |= LogError("VUID-VkPipelineShaderStageCreateInfo-pNext-02755", module_state.handle(), loc,
                         "%s is not in requiredSubgroupSizeStages (%s).", string_VkShaderStageFlagBits(stage_state.GetStage()),
                         string_VkShaderStageFlags(phys_dev_props_core13.requiredSubgroupSizeStages).c_str());
    }
    if ((invocations > required_subgroup_size * phys_dev_props_core13.maxComputeWorkgroupSubgroups)) {
        skip |= LogError("VUID-VkPipelineShaderStageCreateInfo-pNext-02756", module_state.handle(), loc,
                         "shader %s local workgroup size (%s) is greater than requiredSubgroupSize (%" PRIu32
                         ") * maxComputeWorkgroupSubgroups (%" PRIu32 ").",
                         entrypoint.Describe().c_str(), local_size.ToString().c_str(), required_subgroup_size,
                         phys_dev_props_core13.maxComputeWorkgroupSubgroups);
    }
```

## Excerpt: layers/core_checks/cc_spirv.cpp, lines 1652-1681 (pNext-02757 and requiredSubgroupSize-02760 / -02761 / -02762)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv.cpp#L1652-L1681

```text
    if (stage_state.pipeline_create_info &&
        (stage_state.pipeline_create_info->flags & VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT) > 0) {
        if (!IsIntegerMultipleOf(local_size.x, required_subgroup_size)) {
            skip |= LogError("VUID-VkPipelineShaderStageCreateInfo-pNext-02757", module_state.handle(), loc,
                             "shader %s local workgroup size x (%" PRIu32
                             ") is not a multiple of "
                             "requiredSubgroupSize (%" PRIu32 ").",
                             entrypoint.Describe().c_str(), local_size.x, required_subgroup_size);
        }
    }
    if (!IsPowerOfTwo(required_subgroup_size)) {
        skip |=
            LogError("VUID-VkPipelineShaderStageRequiredSubgroupSizeCreateInfo-requiredSubgroupSize-02760", module_state.handle(),
                     pNext_loc.dot(Field::requiredSubgroupSize), "(%" PRIu32 ") is not a power of 2.", required_subgroup_size);
    }
    if (required_subgroup_size < phys_dev_props_core13.minSubgroupSize) {
        skip |=
            LogError("VUID-VkPipelineShaderStageRequiredSubgroupSizeCreateInfo-requiredSubgroupSize-02761", module_state.handle(),
                     pNext_loc.dot(Field::requiredSubgroupSize), "(%" PRIu32 ") is less than minSubgroupSize (%" PRIu32 ").",
                     required_subgroup_size, phys_dev_props_core13.minSubgroupSize);
    }
    if (required_subgroup_size > phys_dev_props_core13.maxSubgroupSize) {
        skip |=
            LogError("VUID-VkPipelineShaderStageRequiredSubgroupSizeCreateInfo-requiredSubgroupSize-02762", module_state.handle(),
                     pNext_loc.dot(Field::requiredSubgroupSize), "(%" PRIu32 ") is greater than maxSubgroupSize (%" PRIu32 ").",
                     required_subgroup_size, phys_dev_props_core13.maxSubgroupSize);
    }

    return skip;
}
```

## Excerpt: layers/core_checks/cc_spirv.cpp, lines 1692-1706 (ValidateComputeWorkGroupSizes: VUID-RuntimeSpirv-x-06429 / y-06430 / z-06431)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv.cpp#L1692-L1706

```text
    if (local_size.x > phys_dev_props.limits.maxComputeWorkGroupSize[0]) {
        skip |= LogError("VUID-RuntimeSpirv-x-06429", module_state.handle(), loc,
                         "shader %s LocalSize X (%" PRIu32 ") exceeds device limit maxComputeWorkGroupSize[0] (%" PRIu32 ").",
                         entrypoint.Describe().c_str(), local_size.x, phys_dev_props.limits.maxComputeWorkGroupSize[0]);
    }
    if (local_size.y > phys_dev_props.limits.maxComputeWorkGroupSize[1]) {
        skip |= LogError("VUID-RuntimeSpirv-y-06430", module_state.handle(), loc,
                         "shader %s LocalSize Y (%" PRIu32 ") exceeds device limit maxComputeWorkGroupSize[1] (%" PRIu32 ").",
                         entrypoint.Describe().c_str(), local_size.y, phys_dev_props.limits.maxComputeWorkGroupSize[1]);
    }
    if (local_size.z > phys_dev_props.limits.maxComputeWorkGroupSize[2]) {
        skip |= LogError("VUID-RuntimeSpirv-z-06431", module_state.handle(), loc,
                         "shader %s LocalSize Z (%" PRIu32 ") exceeds device limit maxComputeWorkGroupSize[2] (%" PRIu32 ").",
                         entrypoint.Describe().c_str(), local_size.z, phys_dev_props.limits.maxComputeWorkGroupSize[2]);
    }
```

## Excerpt: layers/core_checks/cc_spirv.cpp, lines 1708-1733 (VUID-VkPipelineShaderStageCreateInfo-flags-02758 / -02759: full subgroups and local size X)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv.cpp#L1708-L1733

```text
    if (stage_state.pipeline_create_info) {
        const auto subgroup_flags = VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT |
                                    VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT;
        if ((stage_state.pipeline_create_info->flags & subgroup_flags) == subgroup_flags) {
            if (!IsIntegerMultipleOf(local_size.x, phys_dev_props_core13.maxSubgroupSize)) {
                skip |= LogError(
                    "VUID-VkPipelineShaderStageCreateInfo-flags-02758", module_state.handle(), loc.dot(Field::flags),
                    "(%s), but local workgroup size X dimension (%" PRIu32
                    ") is not a multiple of VkPhysicalDeviceSubgroupSizeControlPropertiesEXT::maxSubgroupSize (%" PRIu32 ").",
                    string_VkPipelineShaderStageCreateFlags(stage_state.pipeline_create_info->flags).c_str(), local_size.x,
                    phys_dev_props_core13.maxSubgroupSize);
            }
        } else if ((stage_state.pipeline_create_info->flags & VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT) &&
                   (stage_state.pipeline_create_info->flags & VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT) ==
                       0) {
            if (!vku::FindStructInPNextChain<VkPipelineShaderStageRequiredSubgroupSizeCreateInfo>(stage_state.GetPNext())) {
                if (!IsIntegerMultipleOf(local_size.x, phys_dev_props_core11.subgroupSize)) {
                    skip |=
                        LogError("VUID-VkPipelineShaderStageCreateInfo-flags-02759", module_state.handle(), loc.dot(Field::flags),
                                 "(%s), but local workgroup size X dimension (%" PRIu32
                                 ") is not a multiple of VkPhysicalDeviceVulkan11Properties::subgroupSize (%" PRIu32 ").",
                                 string_VkPipelineShaderStageCreateFlags(stage_state.pipeline_create_info->flags).c_str(),
                                 local_size.x, phys_dev_props_core11.subgroupSize);
                }
            }
        }
```

## Excerpt: layers/core_checks/cc_pipeline.cpp, lines 683-704 (feature and stage requirements of the two stage flags: flags-02784, -02785, -08988)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_pipeline.cpp#L683-L704

```text
        if ((flags & VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT) != 0 &&
            !enabled_features.subgroupSizeControl) {
            skip |= LogError("VUID-VkPipelineShaderStageCreateInfo-flags-02784", device, loc.dot(Field::flags),
                             "includes "
                             "VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT, "
                             "but the subgroupSizeControl feature was not enabled.");
        }

        if ((flags & VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT) != 0) {
            if (!enabled_features.computeFullSubgroups) {
                skip |= LogError("VUID-VkPipelineShaderStageCreateInfo-flags-02785", device, loc.dot(Field::flags),
                                 "includes "
                                 "VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT, but the computeFullSubgroups feature "
                                 "was not enabled");
            } else if ((stage_ci.stage &
                        (VK_SHADER_STAGE_MESH_BIT_EXT | VK_SHADER_STAGE_TASK_BIT_EXT | VK_SHADER_STAGE_COMPUTE_BIT)) == 0) {
                skip |= LogError("VUID-VkPipelineShaderStageCreateInfo-flags-08988", device, loc.dot(Field::flags),
                                 "includes "
                                 "VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT, but the stage is %s.",
                                 string_VkShaderStageFlagBits(stage_ci.stage));
            }
        }
```

## Excerpt: layers/stateless/sl_pipeline.cpp, lines 577-584 (pNext-02754: required subgroup size together with ALLOW_VARYING_SUBGROUP_SIZE)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/stateless/sl_pipeline.cpp#L577-L584

```text
    if (vku::FindStructInPNextChain<VkPipelineShaderStageRequiredSubgroupSizeCreateInfo>(create_info.pNext)) {
        if ((create_info.flags & VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT) != 0) {
            skip |= LogError("VUID-VkPipelineShaderStageCreateInfo-pNext-02754", device, loc.dot(Field::flags),
                             "(%s) includes VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT while "
                             "VkPipelineShaderStageRequiredSubgroupSizeCreateInfo is included in the pNext chain.",
                             string_VkPipelineShaderStageCreateFlags(create_info.flags).c_str());
        }
    }
```

Licence of the excerpts: Apache-2.0 (`LICENSE.txt` of the repository; copyright notices are in the file headers).
