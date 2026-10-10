---
id: doc-vulkan-guide-subgroups
title: 'Vulkan Guide: Subgroups chapter'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Guide/blob/f71c59694335577fb1ec85b17448a53120ef7478/chapters/subgroups.adoc
source_category: official-doc
architectures: []
tags:
- subgroup-size
- subgroup-size-control
- subgroup-operations
retrieved_at: '2026-10-10'
---

# Vulkan Guide: Subgroups chapter

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/guide/latest/subgroups.html

## Excerpt: chapters/subgroups.adoc, lines 11-18 (Subgroups, definition)

Locator: https://github.com/KhronosGroup/Vulkan-Guide/blob/f71c59694335577fb1ec85b17448a53120ef7478/chapters/subgroups.adoc#L11-L18

Rendered locator: https://docs.vulkan.org/guide/latest/subgroups.html#preamble

```text
The Vulkan Spec defines subgroups as:

[NOTE]
====
A set of shader invocations that can synchronize and share data with each other efficiently. In compute shaders, the local workgroup is a superset of the subgroup.
====

For many implementations, a subgroup is the group of invocations that run the same instruction at once. Subgroups allow for a shader writer to work at a finer granularity than a single workgroup.
```

## Excerpt: chapters/subgroups.adoc, lines 25-27 (Subgroup size)

Locator: https://github.com/KhronosGroup/Vulkan-Guide/blob/f71c59694335577fb1ec85b17448a53120ef7478/chapters/subgroups.adoc#L25-L27

Rendered locator: https://docs.vulkan.org/guide/latest/subgroups.html#_subgroup_size

```text
== Subgroup size

It is important to also realize the size of a subgroup can be dynamic for an implementation. Some implementations may dispatch shaders with a varying subgroup size for different subgroups. As a result, they could implicitly split a large subgroup into smaller subgroups or represent a small subgroup as a larger subgroup, some of whose invocations were inactive on launch.
```

## Excerpt: chapters/subgroups.adoc, lines 29-39 (VK_EXT_subgroup_size_control)

Locator: https://github.com/KhronosGroup/Vulkan-Guide/blob/f71c59694335577fb1ec85b17448a53120ef7478/chapters/subgroups.adoc#L29-L39

Rendered locator: https://docs.vulkan.org/guide/latest/subgroups.html#VK_EXT_subgroup_size_control

```text
[[VK_EXT_subgroup_size_control]]
=== VK_EXT_subgroup_size_control

[NOTE]
====
Promoted to core in Vulkan 1.3
====

This extension was created due to some implementations having more than one subgroup size and Vulkan originally only exposing a single subgroup size.

For example, if an implementation has both support for subgroups of size `4` and `16` before they would have had to expose only one size, but now can expose both. This allows applications to potentially control the hardware at a finer granularity for implementations that expose multiple subgroup sizes. If a device does not support this extension, it most likely means there is only one supported subgroup size to expose.
```

## Excerpt: chapters/subgroups.adoc, lines 41-63 (Checking for support)

Locator: https://github.com/KhronosGroup/Vulkan-Guide/blob/f71c59694335577fb1ec85b17448a53120ef7478/chapters/subgroups.adoc#L41-L63

Rendered locator: https://docs.vulkan.org/guide/latest/subgroups.html#_checking_for_support

```text
== Checking for support

With Vulkan 1.1, all the information for subgroups is found in `VkPhysicalDeviceSubgroupProperties`

[source,cpp]
----
VkPhysicalDeviceSubgroupProperties subgroupProperties;

VkPhysicalDeviceProperties2KHR deviceProperties2;
deviceProperties2.sType      = VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PROPERTIES_2;
deviceProperties2.pNext      = &subgroupProperties;
vkGetPhysicalDeviceProperties2(physicalDevice, &deviceProperties2);

// Example of checking if supported in fragment shader
if ((subgroupProperties.supportedStages & VK_SHADER_STAGE_FRAGMENT_BIT) != 0) {
    // fragment shaders supported
}

// Example of checking if ballot is supported
if ((subgroupProperties.supportedOperations & VK_SUBGROUP_FEATURE_BALLOT_BIT) != 0) {
    // ballot subgroup operations supported
}
----
```

## Excerpt: chapters/subgroups.adoc, lines 65-79 (Guaranteed support)

Locator: https://github.com/KhronosGroup/Vulkan-Guide/blob/f71c59694335577fb1ec85b17448a53120ef7478/chapters/subgroups.adoc#L65-L79

Rendered locator: https://docs.vulkan.org/guide/latest/subgroups.html#_guaranteed_support

```text
=== Guaranteed support

For supported stages, the Vulkan Spec guarantees the following support:

[NOTE]
====
**supportedStages** will have the **VK_SHADER_STAGE_COMPUTE_BIT** bit set if any of the physical device's queues support **VK_QUEUE_COMPUTE_BIT**.
====

For supported operations, the Vulkan Spec guarantees the following support:

[NOTE]
====
**supportedOperations** will have the **VK_SUBGROUP_FEATURE_BASIC_BIT** bit set if any of the physical device's queues support **VK_QUEUE_GRAPHICS_BIT** or **VK_QUEUE_COMPUTE_BIT**.
====
```

## Excerpt: chapters/subgroups.adoc, lines 81-93 (VK_KHR_shader_subgroup_extended_types)

Locator: https://github.com/KhronosGroup/Vulkan-Guide/blob/f71c59694335577fb1ec85b17448a53120ef7478/chapters/subgroups.adoc#L81-L93

Rendered locator: https://docs.vulkan.org/guide/latest/subgroups.html#VK_KHR_shader_subgroup_extended_types

```text
[[VK_KHR_shader_subgroup_extended_types]]
== VK_KHR_shader_subgroup_extended_types

[NOTE]
====
Promoted to core in Vulkan 1.2

link:https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_shader_subgroup_extended_types.txt[GLSL_EXT_shader_subgroup_extended_types]
====

This extension allows subgroup operations to use 8-bit integer, 16-bit integer, 64-bit integer, 16-bit floating-point, and vectors of these types in group operations with subgroup scope if the implementation supports the types already.

For example, if an implementation supports 8-bit integers an application can now use the GLSL `genI8Type subgroupAdd(genI8Type value);` call which will get mapped to `OpGroupNonUniformIAdd` in SPIR-V.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2019-2022 The Khronos Group, Inc. (file header, lines 1-2).
