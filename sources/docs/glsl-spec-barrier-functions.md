---
id: doc-glsl-spec-barrier-functions
title: 'OpenGL Shading Language specification, Built-In Functions: barrier() and the shader memory control functions (memoryBarrierShared)'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/builtinfunctions.adoc
source_category: official-doc
architectures: []
tags:
- control-barrier
- shared-memory-fence
- memory-model
- glsl
retrieved_at: '2026-10-10'
---

# OpenGL Shading Language specification, Built-In Functions: barrier() and the shader memory control functions (memoryBarrierShared)

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html

## Excerpt: chapters/builtinfunctions.adoc, lines 3443-3462 (Shader Invocation Control Functions, barrier())

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/builtinfunctions.adoc#L3443-L3462

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html#_barrier

```text
[source,glsl]
----
void barrier()
----

For any given static instance of *barrier*(), all tessellation control shader invocations for a
single input patch must enter it before any will be allowed to continue beyond it, or all compute
shader invocations for a single workgroup must enter it before any will continue beyond it.

The function *barrier*() provides a partially defined order of execution
between shader invocations.
The ensures that, for some types of memory accesses, values written by one
invocation prior to a given static instance of *barrier*() can be safely read
by other invocations after their call to the same static instance *barrier*().
Because invocations may execute in an undefined order between these barrier
calls, the values of a per-vertex or per-patch output variable for tessellation
control shaders, or the values of *shared* variables for compute shaders will be
undefined in a number of cases enumerated in
"`<<output-variables,Output Variables>>`" (for tessellation control shaders)
and "`<<shared-variables,Shared Variables>>`" (for compute shaders).
```

## Excerpt: chapters/builtinfunctions.adoc, lines 3471-3476 (barrier(), memory accesses synchronized)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/builtinfunctions.adoc#L3471-L3476

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html#_barrier

```text
A *barrier*() affects control flow but only synchronizes memory accesses
to *shared* variables and tessellation control output variables.
For other memory accesses, it does not ensure that values written by one invocation
prior to a given static instance of *barrier*() can be safely read by other
invocations after their call to the same static instance of *barrier*().
To achieve this requires the use of both *barrier*() and a memory barrier.
```

## Excerpt: chapters/builtinfunctions.adoc, lines 3478-3489 (barrier(), uniform control flow in compute shaders)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/builtinfunctions.adoc#L3478-L3489

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html#_barrier

```text
For compute shaders, the *barrier*() function may be placed within control
flow, but that control flow must be uniform control flow.
That is, all the controlling expressions that lead to execution of the
barrier must be dynamically uniform expressions.
This ensures that if any shader invocation enters a conditional statement,
then all invocations will enter it.
While compilers are encouraged to give warnings if they can detect this
might not happen, compilers cannot completely determine this.
Hence, it is the author's responsibility to ensure *barrier*() only exists
inside uniform control flow.
Otherwise, some shader invocations will stall indefinitely, waiting for a
barrier that is never reached by other invocations.
```

## Excerpt: chapters/builtinfunctions.adoc, lines 3494-3506 (Shader Memory Control Functions)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/builtinfunctions.adoc#L3494-L3506

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html#shader-memory-control-functions

```text
Within a single shader invocation, the visibility and order of writes made
by that invocation are well-defined.
However, the relative order of reads and writes to a single shared memory
address from multiple separate shader invocations is largely undefined.
Additionally, the order of accesses to multiple memory addresses performed
by a single shader invocation, as observed by other shader invocations, is
also undefined.

The memory barrier built-in functions can be used to order reads and writes
to variables stored in memory accessible to other shader invocations.
When called, these functions will wait for the completion of all reads and
writes previously performed by the caller that access selected variable
types, and then return with no other effect.
```

## Excerpt: chapters/builtinfunctions.adoc, lines 3508-3516 (Shader Memory Control Functions, per-function scope of variable types)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/builtinfunctions.adoc#L3508-L3516

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html#shader-memory-control-functions

```text
The built-in functions *memoryBarrierAtomicCounter*(),
*memoryBarrierBuffer*(), *memoryBarrierImage*(), and *memoryBarrierShared*()
wait for the completion of accesses to atomic counter, buffer, image, and
shared variables, respectively.
The built-in functions *memoryBarrier*() and *groupMemoryBarrier*() wait for
the completion of accesses to all of the above variable types.
The functions *memoryBarrierShared*() and *groupMemoryBarrier*() are
available only in compute shaders; the other functions are available in all
shader types.
```

## Excerpt: chapters/builtinfunctions.adoc, lines 3518-3530 (Shader Memory Control Functions, visibility of stores)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/builtinfunctions.adoc#L3518-L3530

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html#shader-memory-control-functions

```text
When these functions return, the effects of any memory stores performed
using coherent variables prior to the call will be visible to any
future^1^ coherent access to the same memory performed by any other shader
invocation. In particular, the values written this way in one shader stage are
guaranteed to be visible to coherent memory accesses performed by shader
invocations in subsequent stages when those invocations were triggered by
the execution of the original shader invocation (e.g. fragment shader
invocations for a primitive resulting from a particular geometry
shader invocation).

1::
    An access is only a _future_ access if a _happens-before_ relation can
    be established between the store and the load.
```

## Excerpt: chapters/builtinfunctions.adoc, lines 3532-3543 (Shader Memory Control Functions, ordering of stores and the workgroup limit of memoryBarrierShared())

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/builtinfunctions.adoc#L3532-L3543

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/builtinfunctions.html#shader-memory-control-functions

```text
Additionally, memory barrier functions order stores performed by the calling
invocation, as observed by other shader invocations.
Without memory barriers, if one shader invocation performs two stores to
coherent variables, a second shader invocation might see the values written
by the second store prior to seeing those written by the first.
However, if the first shader invocation calls a memory barrier function
between the two stores, selected other shader invocations will never see the
results of the second store before seeing those of the first.
When using the functions *groupMemoryBarrier*() or *memoryBarrierShared*(),
this ordering guarantee applies only to other shader invocations in the same
compute shader workgroup; all other memory barrier functions provide the
guarantee to all other shader invocations.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2008-2024 The Khronos Group Inc. (file header, lines 1-2).
