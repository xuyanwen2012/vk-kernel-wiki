---
id: doc-vk-spec-memory-model
title: 'Vulkan specification, Memory Model appendix: data races, memory semantics, control barriers, scopes and Workgroup storage'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc
source_category: official-doc
architectures: []
tags:
- memory-model
- control-barrier
- shared-memory-fence
- cooperative-matrix
- spirv
retrieved_at: '2026-10-10'
---

# Vulkan specification, Memory Model appendix: data races, memory semantics, control barriers, scopes and Workgroup storage

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/spec/latest/appendices/memorymodel.html

## Excerpt: appendices/memorymodel.adoc, lines 253-258 (Scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L253-L258

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-scope

```text
Atomic and barrier instructions include scopes which identify sets of shader
invocations that must: obey the requested ordering and atomicity rules of
the operation, as defined below.

The various scopes are described in detail in <<shaders-scope, the Shaders
chapter>>.
```

## Excerpt: appendices/memorymodel.adoc, lines 342-350 (Memory Semantics, introduction)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L342-L350

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-memory-semantics

```text
Non-atomic memory operations, by default, may: be observed by one agent in a
different order than they were written by another agent.

Atomics and some synchronization operations include _memory semantics_,
which are flags that constrain the order in which other memory accesses
(including non-atomic memory accesses and
<<memory-model-availability-visibility,availability and visibility
operations>>) performed by the same agent can: be observed by other agents,
or can: observe accesses by other agents.
```

## Excerpt: appendices/memorymodel.adoc, lines 355-378 (Memory Semantics, device instructions and supported semantics)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L355-L378

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-memory-semantics

```text
Device instructions that include semantics are code:OpAtomic*,
code:OpControlBarrier,
ifdef::VK_EXT_shader_split_barrier[]
code:OpControlBarrierArriveEXT, code:OpControlBarrierWaitEXT,
endif::VK_EXT_shader_split_barrier[]
code:OpMemoryBarrier, and code:OpMemoryNamedBarrier.

Vulkan supports the following memory semantics:

  * Relaxed: No constraints on order of other memory accesses.
  * Acquire: A memory read with this semantic performs an _acquire
    operation_.
    A memory barrier with this semantic is an _acquire barrier_.
  * Release: A memory write with this semantic performs a _release
    operation_.
    A memory barrier with this semantic is a _release barrier_.
  * AcquireRelease: A memory read-modify-write operation with this semantic
    performs both an acquire operation and a release operation, and inherits
    the limitations on ordering from both of those operations.
    A memory barrier with this semantic is both a release and acquire
    barrier.

SequentiallyConsistent memory semantics is not supported and must: not be
used.
```

## Excerpt: appendices/memorymodel.adoc, lines 385-399 (Memory Semantics, storage class semantics)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L385-L399

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-memory-semantics

```text
The memory semantics operand can: also include _storage class semantics_
flags which indicate the storage classes constrained by the synchronization.
Vulkan supports the following SPIR-V storage class semantics flags:

  * UniformMemory
  * WorkgroupMemory
  * ImageMemory
  * OutputMemory

The remaining storage class semantics flags (SubgroupMemory,
CrossWorkgroupMemory, and AtomicCounterMemory) are ignored.

Each SPIR-V memory operation accesses a single storage class.
Semantics in synchronization operations can include a combination of storage
classes.
```

## Excerpt: appendices/memorymodel.adoc, lines 410-411 (Memory Semantics, WorkgroupMemory)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L410-L411

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-memory-semantics

```text
The WorkgroupMemory storage class semantic applies to accesses to memory in
the Workgroup storage class.
```

## Excerpt: appendices/memorymodel.adoc, lines 417-424 (Memory Semantics, note on reordering)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L417-L424

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-memory-semantics

```text
[NOTE]
====
Informally, these constraints limit how memory operations can be reordered,
and these limits apply not only to the order of accesses as performed in the
agent that executes the instruction, but also to the order the effects of
writes become visible to all other agents within the same instance of the
instruction's memory scope.
====
```

## Excerpt: appendices/memorymodel.adoc, lines 442-451 (Memory Semantics, MakeAvailable and MakeVisible)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L442-L451

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-memory-semantics

```text
The memory semantics operand can: also include availability and visibility
flags, which apply availability and visibility operations as described in
<<memory-model-availability-visibility,availability and visibility>>.
The availability/visibility flags are:

  * MakeAvailable: Semantics must: be Release or AcquireRelease.
    Performs an availability operation before the release operation or
    barrier.
  * MakeVisible: Semantics must: be Acquire or AcquireRelease.
    Performs a visibility operation after the acquire operation or barrier.
```

## Excerpt: appendices/memorymodel.adoc, lines 488-489 (Synchronizes-With, definition)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L488-L489

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-synchronizes-with

```text
_Synchronizes-with_ is a relation between operations, where each operation
is either an atomic operation or a memory barrier (aka fence on the host).
```

## Excerpt: appendices/memorymodel.adoc, lines 556-569 (Synchronizes-With, release barrier, acquire barrier and control barrier)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L556-L569

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-synchronizes-with

```text
If A is a release barrier, B is an acquire barrier, and C is a control
barrier (where A can: equal C, and B can: equal C), then A synchronizes-with
B if all of the following are true:

  * A is program-ordered before (or equals) C
  * C is program-ordered before (or equals) B
  * A and B are in the instance of each other's memory scopes
  * A and B are in the instance of C's execution scope

[NOTE]
====
This is similar to the barrier-barrier synchronization above, but with a
control barrier filling the role of the relaxed atomics.
====
```

## Excerpt: appendices/memorymodel.adoc, lines 657-663 (Private vs. Non-Private)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L657-L663

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-non-private

```text
By default, non-atomic memory operations are treated as _private_, meaning
such a memory operation is not intended to be used for communication with
other agents.

_Non-private_ memory operations are intended to be used for communication
with other agents.
Atomic operations are always considered _non-private_.
```

## Excerpt: appendices/memorymodel.adoc, lines 673-677 (Private vs. Non-Private, location ordering of private operations)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L673-L677

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-non-private

```text
More precisely, for private memory operations to be
<<memory-model-location-ordered,Location-Ordered>> between distinct agents
requires using system-synchronizes-with rather than shader-based
synchronization.
Private memory operations still obey program-order.
```

## Excerpt: appendices/memorymodel.adoc, lines 742-747 (Availability and Visibility, memory domains)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L742-L747

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-availability-visibility

```text
Memory domains are named according to the agents whose memory accesses use
the domain.
Domains used by shader invocations are organized hierarchically into
multiple smaller memory domains which correspond to the different
<<shaders-scope, scopes>>.
Each memory domain is considered the _dual_ of a scope, and vice versa.
```

## Excerpt: appendices/memorymodel.adoc, lines 767-770 (Availability and Visibility, workgroup and subgroup instance domains)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L767-L770

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-availability-visibility

```text
  * _workgroup instance_ - accessible by shader agents in the same
    workgroup, corresponding to the code:Workgroup scope.
  * _subgroup instance_ - accessible by shader agents in the same subgroup,
    corresponding to the code:Subgroup scope.
```

## Excerpt: appendices/memorymodel.adoc, lines 935-950 (Availability and Visibility Semantics)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L935-L950

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-availability-visibility-semantics

```text
A memory barrier or atomic operation via agent A that includes MakeAvailable
in its semantics performs an availability operation whose source scope
includes agent A and all references in the storage classes in that
instruction's storage class semantics, and all memory locations, and whose
destination scope is a set of memory domains selected as specified below.
The implicit availability operation is program-ordered between the barrier
or atomic and all other operations program-ordered before the barrier or
atomic.

A memory barrier or atomic operation via agent A that includes MakeVisible
in its semantics performs a visibility operation whose source scope is a set
of memory domains selected as specified below, and whose destination scope
includes agent A and all references in the storage classes in that
instruction's storage class semantics, and all memory locations.
The implicit visibility operation is program-ordered between the barrier or
atomic and all other operations program-ordered after the barrier or atomic.
```

## Excerpt: appendices/memorymodel.adoc, lines 964-966 (Availability and Visibility Semantics, domains selected by Workgroup, Subgroup and Invocation scope)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L964-L966

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-availability-visibility-semantics

```text
  * code:Workgroup scope uses the workgroup instance domain
  * code:Subgroup uses the subgroup instance domain
  * code:Invocation perform no availability/visibility operations.
```

## Excerpt: appendices/memorymodel.adoc, lines 1046-1064 (Location-Ordered)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L1046-L1064

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-location-ordered

```text
X is _location-ordered_ before Y for a location L in M if and only if any of
the following is true:

  * A~X~ == A~Y~ and R~X~ == R~Y~ and X->Y
  ** NOTE: this case means no availability/visibility ops are required when
     it is the same (agent,reference).

  * X is a read, both X and Y are non-private, and X->Y
  * X is a read, and X (transitively) system-synchronizes with Y

  * If R~X~ == R~Y~ and A~X~ and A~Y~ access a common memory domain D (e.g.
    are in the same workgroup instance if D is the workgroup instance
    domain), and both X and Y are non-private:
  ** X is a write, Y is a write, AVC(A~X~,R~X~,D,L) is an availability chain
     making (X,L) available to domain D, and X->^rcpo^AVC(A~X~,R~X~,D,L)->Y
  ** X is a write, Y is a read, AVC(A~X~,R~X~,D,L) is an availability chain
     making (X,L) available to domain D, VISC(A~Y~,R~Y~,D,L) is a visibility
     chain making writes to L available in domain D visible to Y, and
     X->^rcpo^AVC(A~X~,R~X~,D,L)->VISC(A~Y~,R~Y~,D,L)->^rcpo^Y
```

## Excerpt: appendices/memorymodel.adoc, lines 1090-1104 (Data Race)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L1090-L1104

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-access-data-race

```text
Let X and Y be operations that access overlapping sets of memory locations
M, where X != Y, and at least one of X and Y is a write, and X and Y are not
mutually-ordered atomic operations.
If there does not exist a location-ordered relation between X and Y for each
location in M, then there is a _data race_.

Applications must: ensure that no data races occur during the execution of
their application.

[NOTE]
====
Data races can only occur due to instructions that are actually executed.
For example, an instruction skipped due to control flow must not contribute
to a data race.
====
```

## Excerpt: appendices/memorymodel.adoc, lines 1110-1121 (Visible-To)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L1110-L1121

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-visible-to

```text
Let X be a write and Y be a read whose sets of memory locations overlap, and
let M be the set of memory locations that overlap.
Let M~2~ be a non-empty subset of M. Then X is _visible-to_ Y for memory
locations M~2~ if and only if all of the following are true:

  * X is location-ordered before Y for each location L in M~2~.
  * There does not exist another write Z to any location L in M~2~ such that
    X is location-ordered before Z for location L and Z is location-ordered
    before Y for location L.

If X is visible-to Y, then Y reads the value written by X for locations
M~2~.
```

## Excerpt: appendices/memorymodel.adoc, lines 1244-1264 (Descriptions (Informative))

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L1244-L1264

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-informative-descriptions

```text
Let SC be the storage class(es) specified by a release or acquire operation
or barrier.

  * An atomic write with release semantics must not be reordered against any
    read or write to SC that is program-ordered before it (regardless of the
    storage class the atomic is in).

  * An atomic read with acquire semantics must not be reordered against any
    read or write to SC that is program-ordered after it (regardless of the
    storage class the atomic is in).

  * Any write to SC program-ordered after a release barrier must not be
    reordered against any read or write to SC program-ordered before that
    barrier.

  * Any read from SC program-ordered before an acquire barrier must not be
    reordered against any read or write to SC program-ordered after the
    barrier.

A control barrier (even if it has no memory semantics) must not be reordered
against any memory barriers.
```

## Excerpt: appendices/memorymodel.adoc, lines 1318-1331 (Cooperative Matrix Memory Access)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/193ebe195f47ffc5004683d1659e71c725658c4d/appendices/memorymodel.adoc#L1318-L1331

Rendered locator: https://docs.vulkan.org/spec/latest/appendices/memorymodel.html#memory-model-cooperative-matrix

```text
For each dynamic instance of a cooperative matrix load instruction
(code:OpCooperativeMatrixLoadKHR
ifdef::VK_NV_cooperative_matrix[, code:OpCooperativeMatrixLoadNV]
ifdef::VK_NV_cooperative_matrix2[, code:OpCooperativeMatrixLoadTensorNV]
), some implementation-dependent invocation(s) within the instance of the
matrix's scope perform a non-atomic load from each memory location that is
defined to be accessed by the instruction.

For each memory location accessed by a dynamic instance of a cooperative
matrix store instruction (code:OpCooperativeMatrixStoreKHR
ifdef::VK_NV_cooperative_matrix[, code:OpCooperativeMatrixStoreNV]
ifdef::VK_NV_cooperative_matrix2[, code:OpCooperativeMatrixStoreTensorNV]
), a single implementation-dependent invocation within the instance of the
matrix's scope performs a non-atomic store to that memory location.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2017-2026 The Khronos Group Inc. (file header, lines 1-3).
