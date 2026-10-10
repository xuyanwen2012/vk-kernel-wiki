---
id: doc-vk-spec-shaders-compute-subgroups
title: 'Vulkan specification, Shaders chapter: compute shaders, varying, full and required subgroups, workgroup and subgroup scopes, group operations'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc
source_category: official-doc
architectures: []
tags:
- full-subgroups
- subgroup-size
- subgroup-size-control
- required-subgroup-size
- subgroup-operations
- shared-memory-limit
- control-barrier
- memory-model
retrieved_at: '2026-10-10'
---

# Vulkan specification, Shaders chapter: compute shaders, varying, full and required subgroups, workgroup and subgroup scopes, group operations

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/spec/latest/chapters/shaders.html

## Excerpt: chapters/shaders.adoc, lines 1943-1974 (Varying Subgroup Size)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L1943-L1974

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-varying-subgroup-size

```text
Shaders may: report a different value of <<interfaces-builtin-variables-sgs,
code:SubgroupSize>> for different subgroups if varying subgroups are
allowed.

If varying subgroups are not allowed, <<interfaces-builtin-variables-sgs,
code:SubgroupSize>> will always be equal to <<limits-subgroupSize>>.
If varying subgroups are allowed, <<interfaces-builtin-variables-sgs,
code:SubgroupSize>> must: be a power-of-two value between
<<limits-minSubgroupSize, pname:minSubgroupSize>> and
<<limits-maxSubgroupSize, pname:maxSubgroupSize>> and must: be uniform with
<<shaders-scope-subgroup, subgroup scope>>.
For
ifdef::VK_EXT_mesh_shader,VK_NV_mesh_shader[]
task, mesh, or
endif::VK_EXT_mesh_shader,VK_NV_mesh_shader[]
compute shaders, subgroups in the same <<shaders-scope-command, command
scope>> will have the same size.
For other stages, every subgroup may: have a different size even within a
single command.

Varying subgroups are allowed if any of the following conditions are true:

ifdef::VK_COMPUTE_VERSION_1_3[]
  * The shader was created from SPIR-V with version number of 1.6 or higher.
endif::VK_COMPUTE_VERSION_1_3[]
ifdef::VK_EXT_shader_object[]
  * The shader was created with flink:vkCreateShadersEXT and the
    ename:VK_SHADER_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT_EXT flag was set.
endif::VK_EXT_shader_object[]
  * The shader was created as part of a pipeline and the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT
    flag was set.
```

## Excerpt: chapters/shaders.adoc, lines 1980-2009 (Full Subgroups)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L1980-L2009

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-full-subgroups

```text
When full subgroups are required:, subgroups must: be launched with all
invocations active, i.e., there is an active invocation with
code:SubgroupLocalInvocationId for each value in range
[0,code:SubgroupSize-1].

Full subgroups are required: when the code:X dimension of the workgroup size
is a multiple of the reported value of <<interfaces-builtin-variables-sgs,
the code:SubgroupSize built-in>>, and one of the following is true:

ifdef::VK_COMPUTE_VERSION_1_3[]
  * The shader was created from SPIR-V with version number of 1.6 or higher.
endif::VK_COMPUTE_VERSION_1_3[]
ifdef::VK_EXT_shader_object[]
  * The shader was created with flink:vkCreateShadersEXT and the
    ename:VK_SHADER_CREATE_REQUIRE_FULL_SUBGROUPS_BIT_EXT flag was set.
endif::VK_EXT_shader_object[]
  * The shader was created as part of a pipeline and the
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT flag
    was set.

[NOTE]
====
If <<shaders-varying-subgroup-size, varying subgroup sizes>> are allowed,
this can only be statically guaranteed if the x dimension of the workgroup
size is a multiple of the <<limits-maxSubgroupSize, pname:maxSubgroupSize>>.
Otherwise, the subgroup size in a particular subgroup may be set to any of
the supported sizes, making this a dynamic condition.
<<shaders-required-subgroup-size, Requiring a specific subgroup size>> will
also ensure this is statically known.
====
```

## Excerpt: chapters/shaders.adoc, lines 2012-2021 (Full Subgroups, note on legacy behaviour)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L2012-L2021

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-full-subgroups

```text
[NOTE]
====
Many algorithms cannot easily be implemented without
<<shaders-full-subgroups,full subgroups>>.
For implementations, full subgroup guarantees can be provided more often
with <<shaders-varying-subgroup-size, varying subgroup sizes>>.
The behavior of this built-in without that guarantee is considered legacy,
and implementations are encouraged to implement the tighter behavior
unconditionally.
====
```

## Excerpt: chapters/shaders.adoc, lines 2028-2045 (Required Subgroup Size)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L2028-L2045

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-required-subgroup-size

```text
A specific subgroup size can: be required: for a shader between
<<limits-minSubgroupSize,pname:minSubgroupSize>> and
<<limits-maxSubgroupSize,pname:maxSubgroupSize>>.
The required size can: be specified by:

  * Adding an instance of
    slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo to the
    pname:pNext chain of slink:VkPipelineShaderStageCreateInfo with
    pname:requiredSize set to the desired value.
ifdef::VK_EXT_shader_object[]
  * Adding an instance of slink:VkShaderRequiredSubgroupSizeCreateInfoEXT to
    the pname:pNext chain of slink:VkShaderCreateInfoEXT with
    pname:requiredSize set to the desired value.
endif::VK_EXT_shader_object[]

When specified, the value of <<interfaces-builtin-variables-sgs,
code:SubgroupSize>> must: match the required value for all invocations of
the shader.
```

## Excerpt: chapters/shaders.adoc, lines 2469-2473 (Shader Memory Access Ordering, reference to the memory model)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L2469-L2473

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-execution-memory-ordering

```text
The <<memory-model,Memory Model>> appendix defines the terminology and rules
for how to correctly communicate between shader invocations, such as when a
write is <<memory-model-visible-to,Visible-To>> a read, and what constitutes
a <<memory-model-access-data-race,Data Race>>.
Applications must: not cause a data race.
```

## Excerpt: chapters/shaders.adoc, lines 2904-2920 (Compute Shaders)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L2904-L2920

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-compute

```text
Compute shaders are invoked via <<dispatch, dispatching commands>>.
In general, they have access to similar resources as shader stages executing
as part of a graphics pipeline.

Compute workloads are formed from groups of work items called workgroups and
processed by the compute shader in the current compute pipeline.
A workgroup is a collection of shader invocations that execute the same
shader, potentially in parallel.
Compute shaders execute in _global workgroups_ which are divided into a
number of _local workgroups_ with a size that can: be set by assigning a
value to the code:LocalSize
ifdef::VK_COMPUTE_VERSION_1_3,VK_KHR_maintenance4[or code:LocalSizeId]
execution mode or via an object decorated by the code:WorkgroupSize
decoration.
An invocation within a local workgroup can: share data with other members of
the local workgroup through shared variables and issue memory and control
flow barriers to synchronize with other members of the local workgroup.
```

## Excerpt: chapters/shaders.adoc, lines 3190-3197 (Scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3190-L3197

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-scope

```text
A _scope_ describes a set of shader invocations, where each such set is a
_scope instance_.
Each invocation belongs to one or more scope instances, but belongs to no
more than one scope instance for each scope.

The operations available between invocations in a given scope instance vary,
with smaller scopes generally able to perform more operations, and with
greater efficiency.
```

## Excerpt: chapters/shaders.adoc, lines 3351-3367 (Scope, Workgroup)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3351-L3367

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-scope-workgroup

```text
A _local workgroup_ is a set of invocations that can synchronize and share
data with each other using memory in the code:Workgroup storage class.

The code:Workgroup code:Scope can be used as both an code:Execution
code:Scope and code:Memory code:Scope for barrier and atomic operations.

Each invocation in a local workgroup must: be in the same
<<shaders-scope-command, command scope instance>>.

Only
ifdef::VK_NV_mesh_shader,VK_EXT_mesh_shader[]
task, mesh, and
endif::VK_NV_mesh_shader,VK_EXT_mesh_shader[]
compute shaders have defined workgroups - other shader types cannot: use
workgroup functionality.
For shaders that have defined workgroups, this set of invocations forms an
_invocation group_ as defined in the <<spirv-spec,SPIR-V specification>>.
```

## Excerpt: chapters/shaders.adoc, lines 3369-3392 (Scope, Workgroup, storage consumed by Workgroup variables)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3369-L3392

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#workgroup-padding

```text
[[workgroup-padding]]
ifdef::VK_KHR_workgroup_memory_explicit_layout[]
When variables declared with the code:Workgroup storage class are explicitly
laid out (hence they are also decorated with code:Block), the amount of
storage consumed is the size of the largest Block variable, not counting any
padding at the end.
endif::VK_KHR_workgroup_memory_explicit_layout[]
The amount of storage consumed by the
ifdef::VK_KHR_workgroup_memory_explicit_layout[]
non-Block
endif::VK_KHR_workgroup_memory_explicit_layout[]
variables declared with the code:Workgroup storage class is
implementation-dependent.
However, the amount of storage consumed may not exceed the largest block
size that would be obtained if all active
ifdef::VK_KHR_workgroup_memory_explicit_layout[]
non-Block
endif::VK_KHR_workgroup_memory_explicit_layout[]
variables declared with code:Workgroup storage class were assigned offsets
in an arbitrary order by successively taking the smallest valid offset
according to the <<interfaces-resources-standard-layout,Standard Storage
Buffer Layout>> rules, and with code:Boolean values considered as 32-bit
integer values for the purpose of this calculation.
(This is equivalent to using the GLSL std430 layout rules.)
```

## Excerpt: chapters/shaders.adoc, lines 3399-3406 (Scope, Subgroup)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3399-L3406

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-scope-subgroup

```text
A _subgroup_ (see the subsection "`Control Flow`" of section 2 of the SPIR-V
1.3 Revision 1 specification) is a set of invocations that can synchronize
and share data with each other efficiently.

The code:Subgroup code:Scope can be used as both an code:Execution
code:Scope and code:Memory code:Scope for barrier and atomic operations.
Other <<VkSubgroupFeatureFlagBits, subgroup features>> allow the use of
<<shaders-group-operations, group operations>> with subgroup scope.
```

## Excerpt: chapters/shaders.adoc, lines 3415-3423 (Scope, Subgroup, relation to the local workgroup)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3415-L3423

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-scope-subgroup

```text
For <<shaders-scope-workgroup, shaders that have defined workgroups>>, each
invocation in a subgroup must: be in the same <<shaders-scope-workgroup,
local workgroup>>.

In other shader stages, each invocation in a subgroup must: be in the same
<<shaders-scope-device, device scope instance>>.

Only <<limits-subgroupSupportedStages, shader stages that support subgroup
operations>> have defined subgroups.
```

## Excerpt: chapters/shaders.adoc, lines 3626-3636 (Group Operations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3626-L3636

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-group-operations

```text
_Group operations_ are executed by multiple invocations within a
<<shaders-scope, scope instance>>; with each invocation involved in
calculating the result.
This provides a mechanism for efficient communication between invocations in
a particular scope instance.

Group operations all take a code:Scope defining the desired
<<shaders-scope,scope instance>> to operate within.
Only the code:Subgroup scope can: be used for these operations; the
<<limits-subgroupSupportedOperations, pname:subgroupSupportedOperations>>
limit defines which types of operation can: be used.
```

## Excerpt: chapters/shaders.adoc, lines 3642-3650 (Basic Group Operations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3642-L3650

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-group-operations-basic

```text
Basic group operations include the use of code:OpGroupNonUniformElect,
code:OpControlBarrier, code:OpMemoryBarrier, and atomic operations.

code:OpGroupNonUniformElect can: be used to choose a single invocation to
perform a task for the whole group.
Only the invocation with the lowest id in the group will return code:true.

The <<memory-model,Memory Model>> appendix defines the operation of barriers
and atomics.
```

## Excerpt: chapters/shaders.adoc, lines 3675-3687 (Arithmetic Group Operations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3675-L3687

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-group-operations-arithmetic

```text
The arithmetic group operations allow invocations to perform scans and
reductions across a group.
The operators supported are add, mul, min, max, and, or, xor.

For reductions, every invocation in a group will obtain the cumulative
result of these operators applied to all values in the group.
For exclusive scans, each invocation in a group will obtain the cumulative
result of these operators applied to all values in invocations with a lower
index in the group.
Inclusive scans are identical to exclusive scans, except the cumulative
result includes the operator applied to the value in the current invocation.

The order in which these operators are applied is implementation-dependent.
```

## Excerpt: chapters/shaders.adoc, lines 3693-3699 (Ballot Group Operations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3693-L3699

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-group-operations-ballot

```text
The ballot group operations allow invocations to perform more complex votes
across the group.
The ballot functionality allows all invocations within a group to provide a
boolean value and get as a result what each invocation provided as their
boolean value.
The broadcast functionality allows values to be broadcast from an invocation
to all other invocations within the group.
```

## Excerpt: chapters/shaders.adoc, lines 3705-3706 (Shuffle Group Operations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3705-L3706

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-group-operations-shuffle

```text
The shuffle group operations allow invocations to read values from other
invocations within a group.
```

## Excerpt: chapters/shaders.adoc, lines 3712-3716 (Shuffle Relative Group Operations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3712-L3716

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-group-operations-shuffle-relative

```text
The shuffle relative group operations allow invocations to read values from
other invocations within the group relative to the current invocation in the
group.
The relative operations supported allow data to be shifted up and down
through the invocations within a group.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2015-2026 The Khronos Group Inc.; Copyright (c) 2020-2021 NVIDIA Corporation (file header, lines 1-3).
