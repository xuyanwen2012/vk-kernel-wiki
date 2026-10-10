---
id: doc-vk-spec-subgroup-builtins
title: 'Vulkan specification, Shader Interfaces chapter: NumSubgroups, SubgroupId, SubgroupLocalInvocationId and SubgroupSize built-in variables'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/interfaces.adoc
source_category: official-doc
architectures: []
tags:
- subgroup-size
- subgroup-size-control
- full-subgroups
- spirv
retrieved_at: '2026-10-10'
---

# Vulkan specification, Shader Interfaces chapter: NumSubgroups, SubgroupId, SubgroupLocalInvocationId and SubgroupSize built-in variables

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/spec/latest/chapters/interfaces.html

## Excerpt: chapters/interfaces.adoc, lines 3917-3918 (NumSubgroups)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/interfaces.adoc#L3917-L3918

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/interfaces.html#interfaces-builtin-variables-numsubgroups

```text
Decorating a variable with the code:NumSubgroups built-in decoration will
make that variable contain the number of subgroups in the local workgroup.
```

## Excerpt: chapters/interfaces.adoc, lines 4983-4985 (SubgroupId)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/interfaces.adoc#L4983-L4985

```text
Decorating a variable with the code:SubgroupId built-in decoration will make
that variable contain the index of the subgroup within the local workgroup.
This variable is in range [0, code:NumSubgroups-1].
```

## Excerpt: chapters/interfaces.adoc, lines 5150-5153 (SubgroupLocalInvocationId)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/interfaces.adoc#L5150-L5153

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/interfaces.html#interfaces-builtin-variables-sgli

```text
Decorating a variable with the code:SubgroupLocalInvocationId builtin
decoration will make that variable contain the index of the invocation
within the subgroup.
This variable is in range [0,code:SubgroupSize-1].
```

## Excerpt: chapters/interfaces.adoc, lines 5157-5165 (SubgroupLocalInvocationId, note)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/interfaces.adoc#L5157-L5165

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/interfaces.html#interfaces-builtin-variables-sgli

```text
There is no direct relationship between code:SubgroupLocalInvocationId and
code:LocalInvocationId or code:LocalInvocationIndex.
ifdef::VK_COMPUTE_VERSION_1_3,VK_EXT_subgroup_size_control[]
If the shader was created with <<shaders-full-subgroups, full subgroups>>,
applications can compute their own local invocation index to serve the same
purpose:

[eq]#index = code:SubgroupLocalInvocationId + code:SubgroupId {times}
code:SubgroupSize#
```

## Excerpt: chapters/interfaces.adoc, lines 5191-5219 (SubgroupSize)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/interfaces.adoc#L5191-L5219

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/interfaces.html#interfaces-builtin-variables-sgs

```text
Decorating a variable with the code:SubgroupSize builtin decoration will
make that variable contain the implementation-dependent
<<limits-subgroupSize, number of invocations in a subgroup>>.
This value must: be a power-of-two integer.
+
ifdef::VK_COMPUTE_VERSION_1_3,VK_EXT_subgroup_size_control[]
If the shader was created with <<shaders-varying-subgroup-size, varying
subgroup size allowed>>, the code:SubgroupSize decorated variable will
contain the subgroup size for each subgroup that gets dispatched.
This value must: be between <<limits-minSubgroupSize,
pname:minSubgroupSize>> and <<limits-maxSubgroupSize,
pname:maxSubgroupSize>> and must: be uniform with <<shaders-scope-subgroup,
subgroup scope>>.
+
If the shader was created with a <<shaders-required-subgroup-size, required
subgroup size>>, the code:SubgroupSize decorated variable will match that
value.
+
If the shader does not allow <<shaders-varying-subgroup-size, varying
subgroup sizes>>, the
endif::VK_COMPUTE_VERSION_1_3,VK_EXT_subgroup_size_control[]
ifndef::VK_COMPUTE_VERSION_1_3,VK_EXT_subgroup_size_control[]
The
endif::VK_COMPUTE_VERSION_1_3,VK_EXT_subgroup_size_control[]
variable decorated with code:SubgroupSize will match <<limits-subgroupSize,
pname:subgroupSize>>.
+
The maximum number of invocations that an implementation can support per
subgroup is 128.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2015-2026 The Khronos Group Inc. (file header, lines 1-2).
