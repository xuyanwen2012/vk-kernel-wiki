---
id: doc-glsl-khr-shader-subgroup
title: GL_KHR_shader_subgroup GLSL extension specification
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt
source_category: official-doc
architectures: []
tags:
- subgroup-operations
- subgroup-size
- control-barrier
- full-subgroups
- glsl
retrieved_at: '2026-10-10'
---

# GL_KHR_shader_subgroup GLSL extension specification

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 78-82 (Overview)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L78-L82

```text
    Invocations are partitioned into subgroups, where invocations within a
    subgroup can synchronize and share data with each other efficiently. This
    extension introduces a set of built-in functions to synchronize and share
    data between invocations within a subgroup, as well as a common set of
    arithmetic operations for reductions and scans.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 115-118 (Mapping to SPIR-V, subgroupBarrier)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L115-L118

```text
      subgroupBarrier() -> OpControlBarrier(
        /*Execution*/Subgroup,
        /*Memory*/Subgroup,
        /*Semantics*/AcquireRelease | UniformMemory | WorkgroupMemory | ImageMemory)
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 128-130 (Mapping to SPIR-V, subgroupMemoryBarrierShared)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L128-L130

```text
      subgroupMemoryBarrierShared() -> OpMemoryBarrier(
        /*Memory*/Subgroup,
        /*Semantics*/AcquireRelease | WorkgroupMemory)
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, line 431 (subgroup and local workgroup)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L431

```text
        In compute shaders, the local workgroup is a superset of the subgroup.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 449-450 (inactive invocations in a compute shader)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L449-L450

```text
        - In a compute shader, invocations may be inactive within a subgroup
          if the local workgroup size is not a multiple of the subgroup size.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 456-459 (dynamic instance of a subgroup built-in function)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L456-L459

```text
        For each active invocation within a subgroup that reaches the same
        dynamic instance of a subgroup built-in function, all active invocations
        within a subgroup must execute the dynamic instance of the function
        before any invocation can proceed.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 485-488 (inclusive and exclusive scan order)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L485-L488

```text
        These operations perform a scan operation across the active invocations
        within a subgroup in linear order starting at the active invocation
        with the lowest <gl_SubgroupInvocationID>, increasing to the active
        invocation with the highest <gl_SubgroupInvocationID>.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 662-665 (gl_SubgroupSize)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L662-L665

```text
    If the extension GL_KHR_shader_subgroup_basic is enabled, the variable
    <gl_SubgroupSize> is the number of invocations within a subgroup, and its
    value is always a power of 2.  The maximum <gl_SubgroupSize> supported by
    the GL_KHR_shader_subgroup_basic extension is 128.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 701-706 (subgroupBarrier)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L701-L706

```text
    The function subgroupBarrier() enforces that all active invocations within a
    subgroup must execute this function before any are allowed to continue their
    execution, and the results of any memory stores performed using coherent
    variables performed prior to the call will be visible to any future
    coherent access to the same memory performed by any other shader invocation
    within the same subgroup.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 734-738 (subgroupMemoryBarrierShared)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L734-L738

```text
    The function subgroupMemoryBarrierShared() enforces the ordering of all
    memory transactions to shared variables issued within a single shader
    invocation, as viewed by other invocations in the same subgroup.

    Only available in compute shaders.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 756-760 (subgroupElect)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L756-L760

```text
    The function subgroupElect() returns true for exactly one invocation out of
    the set of active invocations that execute a dynamic instance of this
    instruction.  All other active invocations will return false.  The
    invocation chosen is the active invocation with the lowest
    <gl_SubgroupInvocationID>.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 829-834 (subgroupBallot)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L829-L834

```text
    The function subgroupBallot() returns a set of bitfields containing the
    result of evaluating the expression <value> in all active invocations in the
    subgroup.  If <value> evaluates to true for an active invocation then the
    bit corresponding to the <gl_SubgroupInvocationID> for the invocation is
    set to one in the result, otherwise the bit is set to zero.  Bits
    corresponding to inactive invocations are set to zero.  The following
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 936-939 (subgroupShuffle)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L936-L939

```text
    The function subgroupShuffle() returns the <value> whose
    <gl_SubgroupInvocationID> is equal to <id>.  If the <id> is an
    inactive invocation or is greater than or equal to <gl_SubgroupSize>, an
    undefined value is returned.
```

## Excerpt: extensions/khr/GL_KHR_shader_subgroup.txt, lines 1000-1002 (subgroupAdd)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GL_KHR_shader_subgroup.txt#L1000-L1002

```text
    The function subgroupAdd() returns the summation of all active invocation
    provided <value>s.  The method that is used to perform the operation on
    each active invocation's <value> is implementation defined.
```

Copyright of the excerpts: Copyright (c) 2018 The Khronos Group Inc.; copyright terms at http://www.khronos.org/registry/speccopyright.html (Notice section of the file, lines 41-44). The repository's REUSE.toml annotates `extensions/**/**.txt` as `LicenseRef-Proprietary` ("Various dates, various Khronos Members"); the file is not redistributed here, only quoted.
