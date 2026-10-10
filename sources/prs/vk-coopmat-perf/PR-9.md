---
id: pr-vk-coopmat-perf-9
repo: jeffbolznv/vk_cooperative_matrix_perf
pr: 9
title: Enable subgroupSizeControl and computeFullSubgroups features
author: Indie-Siggi
date: '2026-06-05'
url: https://github.com/jeffbolznv/vk_cooperative_matrix_perf/pull/9
source_category: upstream-code
architectures: []
tags:
- subgroup-size
- cpp
techniques: []
hardware_features:
- subgroup-size
kernel_types: []
languages:
- cpp
captured_at: '2026-10-10'
status: merged
merge_sha: fb275e185bc1d0ca6b141394adfc801deaa9cdd0
changed_paths:
- src/vk_cooperative_matrix_perf.cpp
inclusion_reason: 'include (manual review of title, description and changed paths): enables the features that make the pipelines'' required subgroup size and full-subgroups request valid: src/vk_cooperative_matrix_perf.cpp'
---

# Enable subgroupSizeControl and computeFullSubgroups features

Locator: https://github.com/jeffbolznv/vk_cooperative_matrix_perf/pull/9 (pull request description, first 1200 of 2295 characters)

<!-- upstream-excerpt-start -->
Each compute pipeline requests specific subgroup behaviour per stage: it chains a
`VkPipelineShaderStageRequiredSubgroupSizeCreateInfo` onto the stage (a required subgroup size of 32) and sets
`VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT` in the stage flags. But the device is created
without enabling the two features that make those requests legal — `subgroupSizeControl` (required to chain
`…RequiredSubgroupSizeCreateInfo`) and `computeFullSubgroups` (required for `REQUIRE_FULL_SUBGROUPS_BIT`). Under
`VK_LAYER_KHRONOS_validation` this trips two VUIDs on every `vkCreateComputePipelines`:

```
VUID-VkPipelineShaderStageCreateInfo-pNext-02755: …RequiredSubgroupSizeCreateInfo… the subgroupSizeControl feature was not enabled
VUID-VkPipelineShaderStageCreateInfo-flags-02785: …REQUIRE_FULL_SUBGROUPS_BIT… the computeFullSubgroups feature was not enabled
```

This isn't only validation noise. With the features off, both requests are invalid usage, so the spec doesn't
guarantee the requested subgroup size or full-subgroup behaviour the tool depends on — enabling the features is
what actually makes its existing requests well-defined, not just a way to silence the messages. As a
<!-- upstream-excerpt-end -->
