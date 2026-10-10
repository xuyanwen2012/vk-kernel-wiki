---
id: doc-vk-ext-subgroup-size-control
title: VK_EXT_subgroup_size_control extension appendix (Vulkan-Docs), including its promotion to Vulkan 1.3
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_EXT_subgroup_size_control.adoc
source_category: official-doc
architectures: []
tags:
- subgroup-size-control
- required-subgroup-size
- full-subgroups
- subgroup-size
retrieved_at: '2026-10-10'
---

# VK_EXT_subgroup_size_control extension appendix (Vulkan-Docs), including its promotion to Vulkan 1.3

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/refpages/latest/refpages/source/VK_EXT_subgroup_size_control.html

## Excerpt: appendices/VK_EXT_subgroup_size_control.adoc, lines 26-39 (Description, varying subgroup size)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_EXT_subgroup_size_control.adoc#L26-L39

```text
This extension enables an implementation to control the subgroup size by
allowing a varying subgroup size and also specifying a required subgroup
size.

It extends the subgroup support in Vulkan 1.1 to allow an implementation to
expose a varying subgroup size.
Previously Vulkan exposed a single subgroup size per physical device, with
the expectation that implementations will behave as if all subgroups have
the same size.
Some implementations may: dispatch shaders with a varying subgroup size for
different subgroups.
As a result they could implicitly split a large subgroup into smaller
subgroups or represent a small subgroup as a larger subgroup, some of whose
invocations were inactive on launch.
```

## Excerpt: appendices/VK_EXT_subgroup_size_control.adoc, lines 41-48 (Description, minimum and maximum subgroup size and the pipeline create flag)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_EXT_subgroup_size_control.adoc#L41-L48

```text
To aid developers in understanding the performance characteristics of their
programs, this extension exposes a minimum and maximum subgroup size that a
physical device supports and a pipeline create flag to enable that pipeline
to vary its subgroup size.
If enabled, any code:SubgroupSize decorated variables in the SPIR-V shader
modules provided to pipeline creation may: vary between the
<<limits-minSubgroupSize, minimum>> and <<limits-maxSubgroupSize, maximum>>
subgroup sizes.
```

## Excerpt: appendices/VK_EXT_subgroup_size_control.adoc, lines 50-63 (Description, required subgroup size and maxComputeWorkgroupSubgroups)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_EXT_subgroup_size_control.adoc#L50-L63

```text
An implementation is also optionally allowed to support specifying a
required subgroup size for a given pipeline stage.
Implementations advertise which <<limits-requiredSubgroupSizeStages, stages
support a required subgroup size>>, and any pipeline of a supported stage
can be passed a slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfoEXT
structure to set the subgroup size for that shader stage of the pipeline.
For compute shaders, this requires the developer to query the
<<limits-maxComputeWorkgroupSubgroups, pname:maxComputeWorkgroupSubgroups>>
and ensure that:

[latexmath]
++++
s = { WorkGroupSize.x \times WorkGroupSize.y \times WorkgroupSize.z \leq SubgroupSize \times maxComputeWorkgroupSubgroups }
++++
```

## Excerpt: appendices/VK_EXT_subgroup_size_control.adoc, lines 65-69 (Description, full subgroups)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_EXT_subgroup_size_control.adoc#L65-L69

```text
Developers can also specify a new pipeline shader stage create flag that
requires the implementation to have fully populated subgroups within local
workgroups.
This requires the workgroup size in the X dimension to be a multiple of the
subgroup size.
```

## Excerpt: appendices/VK_EXT_subgroup_size_control.adoc, lines 73-80 (Promotion to Vulkan 1.3)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_EXT_subgroup_size_control.adoc#L73-L80

```text
=== Promotion to Vulkan 1.3

Vulkan APIs in this extension are included in core Vulkan 1.3, with the EXT
suffix omitted.
External interactions defined by this extension, such as SPIR-V token names,
retain their original names.
The original Vulkan API names are still available as aliases of the core
functionality.
```

## Excerpt: appendices/VK_EXT_subgroup_size_control.adoc, lines 84-89 (Version History)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/VK_EXT_subgroup_size_control.adoc#L84-L89

```text
  * Revision 1, 2019-03-05 (Neil Henning)
  ** Initial draft

  * Revision 2, 2019-07-26 (Faith Ekstrand)
  ** Add the missing slink:VkPhysicalDeviceSubgroupSizeControlFeaturesEXT
     for querying subgroup size control features.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2017-2026 The Khronos Group Inc. (file header, lines 1-3).
