---
id: doc-vvl-cooperative-matrix-checks
title: 'Vulkan-ValidationLayers: cooperative-matrix shader checks (cc_spirv_cooperative.cpp)'
author: The Khronos Group Inc., Valve Corporation, LunarG, Inc.
url: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv_cooperative.cpp
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- coopmat-shape
- subgroup-size
- subgroup-size-control
- required-subgroup-size
retrieved_at: '2026-10-10'
description: C++ source of the validation layer; file and VUID locators for the cooperative-matrix checks
---

# Vulkan-ValidationLayers: cooperative-matrix shader checks (cc_spirv_cooperative.cpp)

## Excerpt: layers/core_checks/cc_spirv_cooperative.cpp, lines 196-205 (VUID-RuntimeSpirv-cooperativeMatrixSupportedStages-08985)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv_cooperative.cpp#L196-L205

```text
    if (module_state.HasCapability(spv::CapabilityCooperativeMatrixKHR)) {
        if (!(entrypoint.stage & phys_dev_ext_props.cooperative_matrix_props_khr.cooperativeMatrixSupportedStages)) {
            skip |=
                LogError("VUID-RuntimeSpirv-cooperativeMatrixSupportedStages-08985", module_state.handle(), loc,
                         "shader %s contains OpTypeCooperativeMatrixKHR but %s is not in "
                         "cooperativeMatrixSupportedStages (%s)",
                         entrypoint.Describe().c_str(), string_VkShaderStageFlagBits(entrypoint.stage),
                         string_VkShaderStageFlags(phys_dev_ext_props.cooperative_matrix_props_khr.cooperativeMatrixSupportedStages)
                             .c_str());
        }
```

## Excerpt: layers/core_checks/cc_spirv_cooperative.cpp, lines 219-230 (VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10770 / -10771: full subgroups before Vulkan 1.3)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv_cooperative.cpp#L219-L230

```text
    if (!module_state.static_data_.cooperative_matrix_inst.empty() && api_version < VK_API_VERSION_1_3) {
        if (!stage_state.RequiresFullSubgroup()) {
            const char* vuid = stage_state.HasPipeline() ? "VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10770"
                                                         : "VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10771";
            skip |= LogError(vuid, module_state.handle(), loc,
                             "shader %s contains SPV_KHR_cooperative_matrix which requires SPIR-V 1.6 (Vulkan 1.3). In order to "
                             "use it with older versions, you need to use %s (which requires VK_EXT_subgroup_size_control).",
                             entrypoint.Describe().c_str(),
                             stage_state.HasPipeline() ? "VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT"
                                                       : "VK_SHADER_CREATE_REQUIRE_FULL_SUBGROUPS_BIT_EXT");
        }
    }
```

## Excerpt: layers/core_checks/cc_spirv_cooperative.cpp, lines 386-412 (VUID-VkPipelineShaderStageCreateInfo-module-08987 / -10169: local size X and subgroup size)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv_cooperative.cpp#L386-L412

```text
            case spv::OpTypeCooperativeMatrixKHR: {
                CoopMatType m(insn.ResultId(), module_state, IsSignedIntType(insn.Word(2)));

                if ((entrypoint.stage & VK_SHADER_STAGE_COMPUTE_BIT) != 0) {
                    if (!IsIntegerMultipleOf(local_size.x, effective_subgroup_size)) {
                        const auto vuid_string = m.scope == VK_SCOPE_SUBGROUP_KHR
                                                     ? "VUID-VkPipelineShaderStageCreateInfo-module-08987"
                                                     : "VUID-VkPipelineShaderStageCreateInfo-module-10169";
                        skip |= LogError(vuid_string, module_state.handle(), loc,
                                         "shader %s has a local workgroup size in the X dimension (%" PRIu32
                                         ") that is not a multiple of subgroupSize (%" PRIu32 ").",
                                         entrypoint.Describe().c_str(), local_size.x, effective_subgroup_size);
                        found_error = true;
                    }
                    if (m.scope == VK_SCOPE_WORKGROUP_KHR) {
                        if (workgroup_size >
                            phys_dev_ext_props.cooperative_matrix_props2_nv.cooperativeMatrixWorkgroupScopeMaxWorkgroupSize) {
                            skip |= LogError(
                                "VUID-VkPipelineShaderStageCreateInfo-module-10169", module_state.handle(), loc,
                                "shader %s has a total local workgroup size (%" PRIu64
                                ") that is larger than cooperativeMatrixWorkgroupScopeMaxWorkgroupSize (%" PRIu32 ").",
                                entrypoint.Describe().c_str(), workgroup_size,
                                phys_dev_ext_props.cooperative_matrix_props2_nv.cooperativeMatrixWorkgroupScopeMaxWorkgroupSize);
                            found_error = true;
                        }
                    }
                }
```

## Excerpt: layers/core_checks/cc_spirv_cooperative.cpp, lines 418-422 (VUID-RuntimeSpirv-cooperativeMatrixWorkgroupScope-10164)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv_cooperative.cpp#L418-L422

```text
                if (m.scope == VK_SCOPE_WORKGROUP_KHR && !enabled_features.cooperativeMatrixWorkgroupScopeNV) {
                    skip |= LogError("VUID-RuntimeSpirv-cooperativeMatrixWorkgroupScope-10164", module_state.handle(), loc,
                                     "shader %s has a cooperative matrix that uses workgroup scope but "
                                     "cooperativeMatrixWorkgroupScope is not enabled.",
                                     entrypoint.Describe().c_str());
```

## Excerpt: layers/core_checks/cc_spirv_cooperative.cpp, lines 531-553 (matrix type against the enumerated properties: -13382, -10163, -10165)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv_cooperative.cpp#L531-L553

```text
                if (!valid) {
                    if (enabled_features.cooperativeMatrixProperties2) {
                        found_error = true;
                        skip |= LogError("VUID-RuntimeSpirv-cooperativeMatrixProperties2-13382", module_state.handle(), loc,
                                         "shader %s has\n%s (%s)\nbut doesn't match any supported "
                                         "VkCooperativeMatrixPropertiesKHR or VkCooperativeMatrixProperties2EXT.\n%s",
                                         entrypoint.Describe().c_str(), insn.Describe().c_str(), m.Describe().c_str(),
                                         print_workgroup_size(m.scope).c_str());
                    } else if (!enabled_features.cooperativeMatrixFlexibleDimensionsNV) {
                        found_error = true;
                        skip |= LogError("VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10163", module_state.handle(), loc,
                                         "shader %s has\n%s (%s)\nbut doesn't match any VkCooperativeMatrixPropertiesKHR\n%s%s",
                                         entrypoint.Describe().c_str(), insn.Describe().c_str(), m.Describe().c_str(),
                                         print_workgroup_size(m.scope).c_str(), print_properties().c_str());
                    } else {
                        skip |= LogError("VUID-RuntimeSpirv-cooperativeMatrixFlexibleDimensions-10165", module_state.handle(), loc,
                                         "shader %s has\n%s (%s)\nbut doesn't match any VkCooperativeMatrixPropertiesKHR or "
                                         "VkCooperativeMatrixFlexibleDimensionsPropertiesNV\n%s%s\n%s",
                                         entrypoint.Describe().c_str(), insn.Describe().c_str(), m.Describe().c_str(),
                                         print_workgroup_size(m.scope).c_str(), print_properties().c_str(),
                                         print_flexible_properties().c_str());
                    }
                }
```

## Excerpt: layers/core_checks/cc_spirv_cooperative.cpp, lines 554-562 (VUID-RuntimeSpirv-cooperativeMatrixFlexibleDimensionsMaxDimension-10167)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv_cooperative.cpp#L554-L562

```text
                if (enabled_features.cooperativeMatrixFlexibleDimensionsNV) {
                    if (m.rows > phys_dev_ext_props.cooperative_matrix_props2_nv.cooperativeMatrixFlexibleDimensionsMaxDimension ||
                        m.cols > phys_dev_ext_props.cooperative_matrix_props2_nv.cooperativeMatrixFlexibleDimensionsMaxDimension) {
                        skip |= LogError(
                            "VUID-RuntimeSpirv-cooperativeMatrixFlexibleDimensionsMaxDimension-10167", module_state.handle(), loc,
                            "shader %s has\n%s (%s)\nbut number of rows or columns is greater than "
                            "cooperativeMatrixFlexibleDimensionsMaxDimension (%" PRIu32 ").",
                            entrypoint.Describe().c_str(), insn.Describe().c_str(), m.Describe().c_str(),
                            phys_dev_ext_props.cooperative_matrix_props2_nv.cooperativeMatrixFlexibleDimensionsMaxDimension);
```

## Excerpt: layers/core_checks/cc_spirv_cooperative.cpp, lines 705-722 (OpCooperativeMatrixMulAddKHR operand combination: -13383, -10060, -10166)

Locator: https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/99fd2cb5761410c0e8cd82395861abd75c9d1f06/layers/core_checks/cc_spirv_cooperative.cpp#L705-L722

```text
                        if (enabled_features.cooperativeMatrixProperties2) {
                            skip |= LogError("VUID-RuntimeSpirv-cooperativeMatrixProperties2-13383", module_state.handle(), loc,
                                             "shader %s instruction\n%s\ndoesn't match any supported "
                                             "VkCooperativeMatrixPropertiesKHR or VkCooperativeMatrixProperties2EXT\n%s%s",
                                             entrypoint.Describe().c_str(), insn.Describe().c_str(), operands_str.c_str(),
                                             print_workgroup_size(report_scope).c_str());
                        } else if (!enabled_features.cooperativeMatrixFlexibleDimensionsNV) {
                            skip |= LogError("VUID-RuntimeSpirv-OpCooperativeMatrixMulAddKHR-10060", module_state.handle(), loc,
                                             "shader %s instruction\n%s\ndoesn't match a supported matrix "
                                             "VkCooperativeMatrixPropertiesKHR\n%s%s%s",
                                             entrypoint.Describe().c_str(), insn.Describe().c_str(), operands_str.c_str(),
                                             print_workgroup_size(report_scope).c_str(), print_properties().c_str());
                        } else {
                            skip |=
                                LogError("VUID-RuntimeSpirv-cooperativeMatrixFlexibleDimensions-10166", module_state.handle(), loc,
                                         "shader %s instruction\n%s\ndoesn't match a supported matrix "
                                         "VkCooperativeMatrixPropertiesKHR or "
                                         "VkPhysicalDeviceCooperativeMatrix2PropertiesNV\n%s%s%s\n%s",
```

Licence of the excerpts: Apache-2.0 (`LICENSE.txt` of the repository; copyright notices are in the file header).
