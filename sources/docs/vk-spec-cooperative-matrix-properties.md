---
id: doc-vk-spec-cooperative-matrix-properties
title: 'Vulkan specification, Shaders chapter, Cooperative Matrices: property enumeration, VkCooperativeMatrixPropertiesKHR and property matching'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- coopmat-shape
- int8-cooperative-matrix
- coopmat-fp32-accumulator
- mma-shape-selection
- subgroup-size
- subgroup-size-control
retrieved_at: '2026-10-10'
---

# Vulkan specification, Shaders chapter, Cooperative Matrices: property enumeration, VkCooperativeMatrixPropertiesKHR and property matching

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/spec/latest/chapters/shaders.html

## Excerpt: chapters/shaders.adoc, lines 3956-3964 (Cooperative Matrices)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L3956-L3964

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#cooperative-matrices

```text
A _cooperative matrix_ type is a SPIR-V type where the storage for and
computations performed on the matrix are spread across the invocations in a
scope instance.
These types give the implementation freedom in how to optimize matrix
multiplies.

SPIR-V defines the types and instructions, but does not specify rules about
what sizes/combinations are valid, and it is expected that different
implementations may: support different sizes.
```

## Excerpt: chapters/shaders.adoc, lines 4058-4061 (VkPhysicalDeviceCooperativeMatrixInfo2EXT, subgroupSize equal to 0)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L4058-L4061

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#VkPhysicalDeviceCooperativeMatrixInfo2EXT

```text
If pname:subgroupSize is equal to `0`, then the properties returned will be
valid for use with shaders that execute with a varying subgroup size, and
the returned properties are not guaranteed to be valid for any specific
effective subgroup size.
```

## Excerpt: chapters/shaders.adoc, lines 4064-4073 (VkPhysicalDeviceCooperativeMatrixInfo2EXT, workgroup scope and invocations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L4064-L4073

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#VkPhysicalDeviceCooperativeMatrixInfo2EXT

```text
If pname:scope is ename:VK_SCOPE_WORKGROUP_KHR, pname:invocations specifies
the number of invocations in the local workgroup, otherwise the properties
returned will be valid for all supported local workgroup sizes.

[NOTE]
====
If pname:scope is ename:VK_SCOPE_WORKGROUP_KHR scope, the retrieved
properties will only be valid for shaders in which pname:invocations is a
multiple of the shader's effective subgroup size.
====
```

## Excerpt: chapters/shaders.adoc, lines 4077-4104 (VkPhysicalDeviceCooperativeMatrixInfo2EXT, note on the intended usage of subgroupSize)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L4077-L4104

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#VkPhysicalDeviceCooperativeMatrixInfo2EXT

```text
[NOTE]
====
The intended usage of pname:subgroupSize is:

  * If the matrix will be used with a pipeline that enables
    ename:VK_PIPELINE_SHADER_STAGE_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT
ifdef::VK_EXT_shader_object[]
    or a shader that enables
    ename:VK_SHADER_CREATE_ALLOW_VARYING_SUBGROUP_SIZE_BIT_EXT,
endif::VK_EXT_shader_object[]
    or a SPIR-V module version 1.6 or later with no required subgroup size
    specified, the application should query the properties with
    pname:subgroupSize equal to `0`, since the effective subgroup size is
    not known at pipeline creation time.
  * If the matrix will be used with a shader whose subgroup size is forced
    via slink:VkPipelineShaderStageRequiredSubgroupSizeCreateInfo,
ifdef::VK_EXT_shader_object[]
    or slink:VkShaderRequiredSubgroupSizeCreateInfoEXT for shader objects,
endif::VK_EXT_shader_object[]
    the application should query with pname:subgroupSize equal to the
    required value.
  * Otherwise (the SPIR-V module version is less than 1.6, and the shader
    neither requests a specific subgroup size nor allows it to vary), the
    effective subgroup size is
    slink:VkPhysicalDeviceSubgroupProperties::pname:subgroupSize, and the
    application should query with that value.
endif::VK_VERSION_1_3,VK_EXT_subgroup_size_control[]
====
```

## Excerpt: chapters/shaders.adoc, lines 4194-4214 (vkGetPhysicalDeviceCooperativeMatrixPropertiesKHR)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L4194-L4214

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#vkGetPhysicalDeviceCooperativeMatrixPropertiesKHR

```text
To enumerate the supported cooperative matrix types and operations, call:

include::{generated}/api/protos/vkGetPhysicalDeviceCooperativeMatrixPropertiesKHR.adoc[]

  * pname:physicalDevice is the physical device.
  * pname:pPropertyCount is a pointer to an integer related to the number of
    cooperative matrix properties available or queried.
  * pname:pProperties is either `NULL` or a pointer to an array of
    slink:VkCooperativeMatrixPropertiesKHR structures.

If pname:pProperties is `NULL`, then the number of cooperative matrix
properties available is returned in pname:pPropertyCount.
Otherwise, pname:pPropertyCount must: point to a variable set by the
application to the number of elements in the pname:pProperties array, and on
return the variable is overwritten with the number of structures actually
written to pname:pProperties.
If pname:pPropertyCount is less than the number of cooperative matrix
properties available, at most pname:pPropertyCount structures will be
written, and ename:VK_INCOMPLETE will be returned instead of
ename:VK_SUCCESS, to indicate that not all the available cooperative matrix
properties were returned.
```

## Excerpt: chapters/shaders.adoc, lines 4373-4409 (VkCooperativeMatrixPropertiesKHR, members, ordering and scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L4373-L4409

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#VkCooperativeMatrixPropertiesKHR

```text
  * pname:MSize is the number of rows in matrices code:A, code:C, and
    code:Result.
  * pname:KSize is the number of columns in matrix code:A and rows in matrix
    code:B.
  * pname:NSize is the number of columns in matrices code:B, code:C,
    code:Result.
  * pname:AType is the component type of matrix code:A, of type
    elink:VkComponentTypeKHR.
  * pname:BType is the component type of matrix code:B, of type
    elink:VkComponentTypeKHR.
  * pname:CType is the component type of matrix code:C, of type
    elink:VkComponentTypeKHR.
  * pname:ResultType is the component type of matrix code:Result, of type
    elink:VkComponentTypeKHR.
  * pname:saturatingAccumulation indicates whether the
    code:SaturatingAccumulation operand to code:OpCooperativeMatrixMulAddKHR
    must: be present or not.
    If it is ename:VK_TRUE, the code:SaturatingAccumulation operand must: be
    present.
    If it is ename:VK_FALSE, the code:SaturatingAccumulation operand must:
    not be present.
  * pname:scope is the scope of all the matrix types, of type
    elink:VkScopeKHR.

If some types are preferred over other types (e.g. for performance), they
should: appear earlier in the list enumerated by
flink:vkGetPhysicalDeviceCooperativeMatrixPropertiesKHR.

At least one entry in the list must: have power of two values for all of
pname:MSize, pname:KSize, and pname:NSize.

ifdef::VK_NV_cooperative_matrix2[]
If the
<<features-cooperativeMatrixWorkgroupScope,pname:cooperativeMatrixWorkgroupScope>>
feature is not supported,
endif::VK_NV_cooperative_matrix2[]
pname:scope must: be ename:VK_SCOPE_SUBGROUP_KHR.
```

## Excerpt: chapters/shaders.adoc, lines 4626-4646 (VkCooperativeMatrixPropertiesKHR Type Matching)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L4626-L4646

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-cooperative-matrix-properties-khr-type-matching

```text
An code:OpTypeCooperativeMatrixKHR type matches a
slink:VkCooperativeMatrixPropertiesKHR structure if all of the following
conditions are satisfied:

  * Its scope matches slink:VkCooperativeMatrixPropertiesKHR::pname:scope.
  * If code:Use is code:MatrixA, its number of rows matches
    slink:VkCooperativeMatrixPropertiesKHR::pname:MSize, its number of
    columns matches slink:VkCooperativeMatrixPropertiesKHR::pname:KSize, and
    its component type matches
    slink:VkCooperativeMatrixPropertiesKHR::pname:AType.
  * If code:Use is code:MatrixB, its number of rows matches
    slink:VkCooperativeMatrixPropertiesKHR::pname:KSize, its number of
    columns matches slink:VkCooperativeMatrixPropertiesKHR::pname:NSize, and
    its component type matches
    slink:VkCooperativeMatrixPropertiesKHR::pname:BType.
  * If code:Use is code:MatrixAccumulator, its number of rows matches
    slink:VkCooperativeMatrixPropertiesKHR::pname:MSize, its number of
    columns matches slink:VkCooperativeMatrixPropertiesKHR::pname:NSize, and
    its component type matches either
    slink:VkCooperativeMatrixPropertiesKHR::pname:CType or
    slink:VkCooperativeMatrixPropertiesKHR::pname:ResultType.
```

## Excerpt: chapters/shaders.adoc, lines 4651-4674 (VkCooperativeMatrixPropertiesKHR Multiply-Add Matching, operand types)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L4651-L4674

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-cooperative-matrix-properties-khr-muladd-matching

```text
The operands of an code:OpCooperativeMatrixMulAddKHR instruction match a
slink:VkCooperativeMatrixPropertiesKHR structure if all of the following
conditions are satisfied:

  * The type of code:A has code:Rows matching
    slink:VkCooperativeMatrixPropertiesKHR::pname:MSize, code:Columns
    matching slink:VkCooperativeMatrixPropertiesKHR::pname:KSize, code:Use
    equal to code:MatrixAKHR, and code:ComponentType matching
    slink:VkCooperativeMatrixPropertiesKHR::pname:AType.
  * The type of code:B has code:Rows matching
    slink:VkCooperativeMatrixPropertiesKHR::pname:KSize, code:Columns
    matching slink:VkCooperativeMatrixPropertiesKHR::pname:NSize, code:Use
    equal to code:MatrixBKHR, and code:ComponentType matching
    slink:VkCooperativeMatrixPropertiesKHR::pname:BType.
  * The type of code:C has code:Rows matching
    slink:VkCooperativeMatrixPropertiesKHR::pname:MSize, code:Columns
    matching slink:VkCooperativeMatrixPropertiesKHR::pname:NSize, code:Use
    equal to code:MatrixAccumulatorKHR, and code:ComponentType matching
    slink:VkCooperativeMatrixPropertiesKHR::pname:CType.
  * The type of code:Result has code:Rows matching
    slink:VkCooperativeMatrixPropertiesKHR::pname:MSize, code:Columns
    matching slink:VkCooperativeMatrixPropertiesKHR::pname:NSize, code:Use
    equal to code:MatrixAccumulatorKHR, and code:ComponentType matching
    slink:VkCooperativeMatrixPropertiesKHR::pname:ResultType.
```

## Excerpt: chapters/shaders.adoc, lines 4675-4694 (VkCooperativeMatrixPropertiesKHR Multiply-Add Matching, signedness, saturation and scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/chapters/shaders.adoc#L4675-L4694

Rendered locator: https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-cooperative-matrix-properties-khr-muladd-matching

```text
  * code:MatrixASignedComponents is used if and only if
    slink:VkCooperativeMatrixPropertiesKHR::pname:AType is a signed integer
    type.
  * code:MatrixBSignedComponents is used if and only if
    slink:VkCooperativeMatrixPropertiesKHR::pname:BType is a signed integer
    type.
  * code:MatrixCSignedComponents is used if and only if
    slink:VkCooperativeMatrixPropertiesKHR::pname:CType is a signed integer
    type.
  * code:MatrixResultSignedComponents is used if and only if
    slink:VkCooperativeMatrixPropertiesKHR::pname:ResultType is a signed
    integer type.
  * code:SaturatingAccumulationKHR is used if and only if
    slink:VkCooperativeMatrixPropertiesKHR::pname:saturatingAccumulation is
    ename:VK_TRUE.
  * code:SaturatingAccumulationKHR is not used if and only if
    slink:VkCooperativeMatrixPropertiesKHR::pname:saturatingAccumulation is
    ename:VK_FALSE.
  * The scope of all cooperative matrix operands matches
    slink:VkCooperativeMatrixPropertiesKHR::pname:scope.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2015-2026 The Khronos Group Inc.; Copyright (c) 2020-2021 NVIDIA Corporation (file header, lines 1-3).
