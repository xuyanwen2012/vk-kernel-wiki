---
id: doc-vk-ext-shader-split-barrier-proposal
title: 'VK_EXT_shader_split_barrier proposal (Vulkan-Docs): split control barriers for cooperative-matrix loops staged through shared memory'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc
source_category: official-doc
architectures: []
tags:
- control-barrier
- cooperative-matrix
- shared-memory-limit
- shared-memory-fence
- double-buffering
- memory-model
- gemm
retrieved_at: '2026-10-10'
---

# VK_EXT_shader_split_barrier proposal (Vulkan-Docs): split control barriers for cooperative-matrix loops staged through shared memory

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/features/latest/features/proposals/VK_EXT_shader_split_barrier.html

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 17-26 (Problem Statement)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L17-L26

```text
Workgroup control barriers in compute shaders control the execution order of subgroups within a workgroup
and synchronize memory access.

However, in performance-critical compute loops this hard sync point can create a
synchronization bottleneck due to not being able to let fast subgroups race ahead to
continue independent work.

Considering one example where an application is performing a tiled matrix multiplication staged
through shared memory using xref:{refpages}VK_KHR_cooperative_matrix.html[VK_KHR_cooperative_matrix],
a standard `barrier()` significantly impacts memory throughput:
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 28-48 (Problem Statement, tiled matrix multiplication loop)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L28-L48

```text
[source,glsl]
----
    for (uint32_t step = 0; step < TOTAL_K; step += TILE_K)
    {
        // 1. Global -> Shared Copy (High Latency)
        // Only needs to wait for step 2 to complete in previous iteration, but blocked on step 3 by barrier
        ...
        barrier();

        // 2. Shared -> Private load
        coopMatLoad(matA, inputA.x, subMatrixAStartInElements, strideAinElements, int(layoutA_Mfirst));
        coopMatLoad(matB, inputB.x, subMatrixBStartInElements, strideBinElements, int(layoutB_Kfirst));

        // 3. Math using private memory (ALU heavy)
        matR = coopMatMulAdd(matA, matB, matC);

        // 4. Hard sync
        // Wait for ALL subgroups to complete step 3 before allowing ANY subgroup to overwrite shared memory
        barrier();
    }
----
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 50-56 (Problem Statement, effect of the standard barrier)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L50-L56

```text
When a workgroup processes a tile, a standard barrier forces all subgroups to complete their
heavy ALU operations (e.g., `coopMatMulAdd`) before any subgroup can proceed to the next iteration.
This prevents "fast" subgroups from issuing the long-latency Global-to-Shared memory fetches for the
subsequent tile while "slow" subgroups are still performing ALU work.

Consequently, the memory subsystem remains underutilized, creating a bubble in memory occupancy
that cannot be hidden by the ALU.
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 60-76 (Solution Space)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L60-L76

```text
For an application not staging through shared memory, this loop would not need barriers
for functional behavior due to loading from global memory. However, those applications may still benefit
from barriers to help with occupancy between memory access and ALU operations - but not with the current
barrier model.

A better solution is to introduce a split-sync model. By separating the barrier into "Arrival"
and "Wait" phases, a subgroup can signal when it has finished accessing a shared resource without blocking
its own execution.

  1. Arrival (split_barrier_arrive): Informs the workgroup that the subgroup has finished reading from/writing
     to the shared resource (e.g., Shared Memory).
  2. Wait (split_barrier_wait): Blocks the subgroup until all subgroups in the workgroup have signaled their arrival.

This allows a subgroup to "check in" immediately after its Shared-to-Private load, perform its matrix math, and then hit the wait.
If all other subgroups have also "checked in" (meaning they have safely finished reading the current tile from Shared Memory),
the fast subgroup can immediately begin the next iteration's Global Memory fetch, overlapping the memory latency of the next tile
with the ALU latency of the current tile in slower subgroups.
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 141-146 (Proposal, SPIR-V, Vulkan restrictions)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L141-L146

```text
This capability is only permitted in compute shaders. Unlike `OpControlBarrier`,
tessellation, mesh, and ray pipeline shaders are not permitted.

While the SPIRV instructions include parameters similar to control barriers,
Vulkan requires `Execution Scope` be `Workgroup` or `Subgroup`, and there are
additional restrictions on `Acquire` and `Release` memory semantics.
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 170-176 (High Level Language Exposure, memory barrier and uniform control flow)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L170-L176

```text
This barrier specifies both an execution barrier as described in the definitions above and
specifies a memory barrier. The memory barrier only synchronizes accesses to shared variables.
A separate memoryBarrier needs to be specified in order to synchronize other accesses.

If a split barrier pair is placed within control flow, it must be dynamically uniform. All controlling
expressions must uniformly execute this pair or it could cause a deadlock. For example,
if some invocations skip calling arrive, wait may never unblock.
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 199-206 (High Level Language Exposure, scope and semantics restrictions)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L199-L206

```text
The restrictions are defined in the `GL_KHR_memory_scope_semantics` extension section "Scope and Semantics`, with the additional restrictions:
  * Only `gl_SemanticsRelease`, `gl_SemanticsMakeAvailable`, or `gl_SemanticsRelaxed` are valid to be used with `controlBarrierArrive`
  * Only `gl_SemanticsAcquire`, `gl_SemanticsMakeVisible`, or `gl_SemanticsRelaxed` are valid to be used with `controlBarrierWait`

Additionally, `execution` must be set to `gl_ScopeWorkgroup` or `gl_ScopeSubgroup`.

Like `splitBarrierArrive`/`splitBarrierWait`, these must be called within uniform control flow if `execution` is
set to `gl_ScopeWorkgroup`.
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 221-237 (Features and Properties)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L221-L237

```text
  * `shaderSplitBarrier` indicates that the implementation supports SPIR-V modules
    declaring the `SplitBarrierEXT` capability.

A new property is added with this extension:

[source,c]
----
typedef struct VkPhysicalDeviceShaderSplitBarrierPropertiesEXT {
    VkStructureType    sType;
    void*              pNext;
    uint32_t           splitBarrierReservedSharedMemory;
} VkPhysicalDeviceShaderSplitBarrierPropertiesEXT;
----

  * `splitBarrierReservedSharedMemory` indicates the amount of shared memory reserved
    by the implementation in bytes out of `maxComputeSharedMemorySize` when using split
    barriers in the shader
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 241-253 (Examples, note)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L241-L253

```text
This example illustrates how to use a split barrier to increase concurrency between
subgroups.

[NOTE]
====
This example is not prescribing a reference implementation for how to perform tiled
cooperative matrix operations. When staging through shared memory it may be recommended
to pull step 1 out of the tile loop - that was not done here to keep the example simple.

On at least one implementation, it is recommended to load directly from global memory to
private memory and skip staging through shared memory. Using split barriers is still useful
here to keep ALU and memory access fully occupied across the subgroups.
====
```

## Excerpt: proposals/VK_EXT_shader_split_barrier.adoc, lines 255-278 (Examples, loop with a split barrier)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/proposals/VK_EXT_shader_split_barrier.adoc#L255-L278

```text
[source,glsl]
----
    for (uint32_t step = 0; step < TOTAL_K; step += TILE_K)
    {
        // 1. Global -> Shared Copy (High Latency)
        // Start occupying memory lanes while subgroups are still crunching step 3 from last tile
        ...
        barrier();

        // 2. Shared -> Private load
        coopMatLoad(matA, inputA.x, subMatrixAStartInElements, strideAinElements, int(layoutA_Mfirst));
        coopMatLoad(matB, inputB.x, subMatrixBStartInElements, strideBinElements, int(layoutB_Kfirst));

        // Signal to workgroup this subgroup is done using shared memory
        splitBarrierArrive();

        // 3. Math using private memory (ALU heavy)
        matR = coopMatMulAdd(matA, matB, matC);

        // 4. Only wait for all subgroups to finish step 2 before proceeding to next tile.
        // Do not wait for all subgroups to complete step 3.
        splitBarrierWait();
    }
----
```

Licence of the excerpts: CC-BY-4.0, Copyright 2026 The Khronos Group Inc. (file header, lines 1-3).
