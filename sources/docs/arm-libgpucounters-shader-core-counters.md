---
id: doc-arm-libgpucounters-shader-core-counters
title: 'Arm libGPUCounters: Mali shader-core counter definitions for warps, register use and thread occupancy'
author: Arm Limited
url: https://github.com/ARM-software/libGPUCounters/tree/378c7b59e2dae87cbbffb0ac9cf96ed13c939823
source_category: upstream-code
architectures:
- arm
tags:
- subgroup-size
- workgroup-tile-sizing
retrieved_at: '2026-10-10'
description: Machine-readable Mali counter specification; the counters are read through the Arm commercial driver, not through Vulkan
---

# Arm libGPUCounters: Mali shader-core counter definitions for warps, register use and thread occupancy

## Excerpt: README.md, lines 3-7 (what the library is)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/README.md#L3-L7

```text
libGPUCounters (formerly called HWCPipe) is a utility that allows applications
to sample performance counters from Arm® Immortalis™ and Arm Mali™ GPUs. This
information allows developers to profile and optimize their application
workload using their existing in-house performance tooling, and gives the
ability to display performance data live in the application user interface.
```

## Excerpt: README.md, lines 16-23 (supported devices)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/README.md#L16-L23

```text
The project aims to support all Arm GPU products from the Mali-G71 series or
later, covering all Arm GPU architectures since the Bifrost architecture. This
ensures developers have coverage of the vast majority of smartphones with Arm
GPUs that are in use today. If you find a device with an Arm GPU which does not
work, or gives inaccurate results, please open an Issue on the GitHub issue
tracker.

This library only supports devices using the Arm commercial driver.
```

## Excerpt: README.md, lines 80-85 (interactive counter documentation)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/README.md#L80-L85

```text
## Counter documentation

Interactive counter documentation for all of the GPU products supported by
libGPUCounters can be found on the project GitHub Pages site:

* https://arm-software.github.io/libGPUCounters/
```

## Excerpt: specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml, lines 167-186 (MaliNonFragWarp: compute warps and work-group size)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml#L167-L186

```text
    <MachineName>MaliNonFragWarp</MachineName>
    <SourceName>COMPUTE_WARPS</SourceName>
    <SourceAlias>COMPUTE_THREADS</SourceAlias>
    <StableID>228</StableID>
    <HumanName>Non-fragment warps</HumanName>
    <GroupName>Shader Warps</GroupName>
    <GroupHumanName>Non-fragment warps</GroupHumanName>
    <Units>warps</Units>
    <Trend>Lower better</Trend>
    <Visibility>Novice</Visibility>
    <ShortDescription>
      The number of non-fragment warps created.
    </ShortDescription>
    <LongDescription>
      This counter increments for every created non-fragment warp. For this
      GPU, a warp contains {{C::MaliGPUWarpSize.equation}} threads.

      For compute shaders, to ensure full utilization of the warp capacity,
      work groups must be a multiple of warp size.
    </LongDescription>
```

## Excerpt: specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml, lines 651-675 (MaliCoreAllRegsWarp: warps using more than 32 registers)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml#L651-L675

```text
    <MachineName>MaliCoreAllRegsWarp</MachineName>
    <SourceName>WARP_REG_SIZE_64</SourceName>
    <StableID>231</StableID>
    <HumanName>Warps using more than 32 registers</HumanName>
    <GroupName>Shader Warps</GroupName>
    <GroupHumanName>All register warps</GroupHumanName>
    <Units>warps</Units>
    <Trend>Lower better</Trend>
    <Visibility>Novice</Visibility>
    <ShortDescription>
      The number of warps that require more than 32 registers.
    </ShortDescription>
    <LongDescription>
      This counter increments for every warp that requires more than 32
      registers. Threads which require more than 32 registers consume two
      thread slots in the register file, halving the number of threads that can
      be concurrently active in the shader core.

      Reduction in thread count can impact the ability of the shader core to
      keep functional units busy, and means that performance is more likely to
      be impacted by stalls caused by cache misses.

      Aim to minimize the number of threads requiring more than 32 registers,
      by using simpler shader programs and lower precision data types.
    </LongDescription>
```

## Excerpt: specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml, lines 695-715 (MaliCoreAllRegsWarpRate)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml#L695-L715

```text
    <MachineName>MaliCoreAllRegsWarpRate</MachineName>
    <StableID>65597</StableID>
    <HumanName>All registers warp percentage</HumanName>
    <GroupName>Shader Workload Properties</GroupName>
    <GroupHumanName>All registers warp rate</GroupHumanName>
    <Units>percent</Units>
    <Trend>Lower better</Trend>
    <Visibility>Novice</Visibility>
    <ShortDescription>
      The percentage of warps that require more than 32 registers.
    </ShortDescription>
    <LongDescription>
      This expression defines the percentage of warps that use more than 32
      registers, requiring the full register allocation of 64 registers. Warps
      that require more than 32 registers halve the peak thread occupancy of
      the shader core, and can make shader performance more sensitive to cache
      misses and memory stalls.
    </LongDescription>
    <Equation>
      (MaliCoreAllRegsWarp / (MaliNonFragWarp + MaliFragWarp)) * 100
    </Equation>
```

## Excerpt: specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml, lines 827-846 (MaliCoreThreadOccupancyQ1Cy: thread occupancy quartile)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml#L827-L846

```text
    <MachineName>MaliCoreThreadOccupancyQ1Cy</MachineName>
    <SourceName>EXEC_CORE_OCCUPANCY_25</SourceName>
    <StableID>546</StableID>
    <HumanName>Core cycles with 0-25% thread occupancy</HumanName>
    <GroupName>Shader Core Occupancy</GroupName>
    <GroupHumanName>0-25% occupancy</GroupHumanName>
    <Units>cycles</Units>
    <Trend>Lower better</Trend>
    <Visibility>Novice</Visibility>
    <ShortDescription>
      The number of cycles with 0-25% thread occupancy.
    </ShortDescription>
    <LongDescription>
      This counter increments for every active shader core cycle where core
      thread occupancy is between 0 and 25%.

      Increasing thread occupancy improves the ability of the core to hide the
      latency of data fetches on cache misses, but can increase cache pressure
      for some data access patterns.
    </LongDescription>
```

## Excerpt: specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml, lines 987-1011 (MaliCoreFullWarp: full warps)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml#L987-L1011

```text
    <MachineName>MaliCoreFullWarp</MachineName>
    <SourceName>FULL_QUAD_WARPS</SourceName>
    <SourceAlias>FULL_WARPS</SourceAlias>
    <StableID>232</StableID>
    <HumanName>Full warps</HumanName>
    <GroupName>Shader Warps</GroupName>
    <GroupHumanName>Full warps</GroupHumanName>
    <Units>warps</Units>
    <Trend>Higher better</Trend>
    <Visibility>Novice</Visibility>
    <ShortDescription>
      The number of warps that have a full thread slot allocation.
    </ShortDescription>
    <LongDescription>
      This counter increments for every warp that has a full thread slot
      allocation. Note that allocated thread slots might not contain a running
      thread if the workload can not fill the whole allocation.

      If many warps are not fully allocated then performance is reduced. Fully
      allocated warps are more likely if:

      * Draw calls avoid late ZS dependency hazards.
      * Draw calls use meshes with a low percentage of tiny primitives.
      * Compute dispatches use work groups that are a multiple of warp size.
    </LongDescription>
```

## Excerpt: specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml, lines 1032-1057 (MaliCoreFullWarpRate)

Locator: https://github.com/ARM-software/libGPUCounters/blob/378c7b59e2dae87cbbffb0ac9cf96ed13c939823/specification/database/counterinfo/Mali-CounterInfo-04d-ShaderCore-Program.xml#L1032-L1057

```text
    <MachineName>MaliCoreFullWarpRate</MachineName>
    <StableID>65598</StableID>
    <HumanName>Full warp percentage</HumanName>
    <GroupName>Shader Workload Properties</GroupName>
    <GroupHumanName>Full warp rate</GroupHumanName>
    <Units>percent</Units>
    <Trend>Higher better</Trend>
    <Visibility>Novice</Visibility>
    <ShortDescription>
      The percentage of warps that have a full thread slot allocation.
    </ShortDescription>
    <LongDescription>
      This expression defines the percentage of warps that have a full thread
      slot allocation. Note that allocated thread slots might not contain a
      running thread if the workload can not fill the whole allocation.

      If a high percentage of warps are not fully allocated then performance is
      reduced. Fully allocated warps are more likely if:

      * Draw calls avoid late ZS dependency hazards.
      * Draw calls use meshes with a low percentage of tiny primitives.
      * Compute dispatches use work groups that are a multiple of warp size.
    </LongDescription>
    <Equation>
      (MaliCoreFullWarp / (MaliNonFragWarp + MaliFragWarp)) * 100
    </Equation>
```

Licence of the excerpts: MIT, Copyright (c) 2019-2026 Arm Limited (file header of the specification file; `LICENSE.md` of the repository).
