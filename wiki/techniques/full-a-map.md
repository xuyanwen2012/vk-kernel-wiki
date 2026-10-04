---
id: technique-full-a-map
title: "Full A map (A_MAP_FULL) in the 8da4w zpg cooperative-matrix linear kernel on the Radeon 780M"
type: technique
architectures: [radeon-780m]
tags: [full-a-map, linear-8da4w-zpg, linear-8da4w, cooperative-matrix, double-buffering, prefill]
confidence: source-reported
reproducibility: snippet
prerequisites: [hw-cooperative-matrix-rdna3]
related: [hw-radeon-780m, kernel-linear-8da4w-780m, technique-workgroup-tile-sizing, technique-drain-in-a-staging, pattern-coopmat-name-check-false-failure]
sources: [meas-780m-8da4w-port]
aliases: ["A_MAP_FULL", "A_ALWAYS_ACTIVE", "a_active guard"]
---

# Full A map (A_MAP_FULL) in the 8da4w zpg linear kernel

Scope: one device (Radeon 780M), one driver (RADV Mesa 25.2.7), one result set dated 2026-09-27 (`meas-780m-8da4w-port`). Nothing here is established for another device, driver or date.

How the driver version is known: the result set's own device line names the driver as `radv phoenix` and records no version [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, line 5]. The version is attributed from the package install history captured on the device on 2026-10-04, which shows the Vulkan driver package at 25.2.7 since 2026-05-29 with no later entry [meas-780m-8da4w-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 3-5 and lines 10-14]. It is not recorded by the run.

"code" below means https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae. A citation of the form `[code: path#L]` points at that commit and is a statement of the code or its authors, not a measurement held in a source page of this wiki.

## What the technique is

`sarc_linear_dq8ca_coopmat_zpg` is the 8da4w family that reads int8 activations in 4h4w blocks [meas-780m-8da4w-port: sarc/SWEEP-PARAMETERS.md, lines 8-12]. Before each multiply step, the invocations of a workgroup copy the A operand (the packed int8 activations) into the shared array `Ash_int8`. Which invocation copies which block is fixed by a per-invocation map, and an invocation takes part only when its index is below the number of blocks to stage:

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L140-L151` (code; the A staging thread map and its guard)

```glsl
  // --- A staging thread map: one (m4, k4) ivec4 block per active thread ---
  const uint K_BLOCKS_PER_CHUNK = WG_TILE_K >> 2u;
  const uint A_ACTIVE_THREADS = (WG_TILE_M >> 2u) * K_BLOCKS_PER_CHUNK;
  const uint a_m_block = gl_LocalInvocationID.x / K_BLOCKS_PER_CHUNK;
  const uint a_k_block = gl_LocalInvocationID.x % K_BLOCKS_PER_CHUNK;
#ifdef A_ALWAYS_ACTIVE
  // A_ACTIVE_THREADS == WG_SIZE for this variant's tile, so every thread stages
  // A and the guard is unconditionally true.
  const bool a_active = true;
#else
  const bool a_active = gl_LocalInvocationID.x < A_ACTIVE_THREADS;
#endif
```

`A_MAP_FULL` is a yaml parameter of the family, default off. Its header description is "every thread stages exactly one A block (full A map)" [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl, lines 9-19 (line 19)]. Setting it defines `A_ALWAYS_ACTIVE`, which replaces the runtime comparison above by the constant `true`:

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl#L38-L45` (code; template lines, `$if` is the shader generator's syntax)

```glsl
// INTERVENTION G: when the A staging thread map exactly covers the workgroup
// (A_ACTIVE_THREADS == WG_SIZE) the `a_active` guard is statically always true,
// but the driver compiler does not fold it -- gl_LocalInvocationID.x's bound
// comes from a spec constant, so the comparison survives into the hot loop as a
// real branch. Set A_MAP_FULL only for tiles where the equality has been
// checked arithmetically; the yaml records the arithmetic per variant.
$if A_MAP_FULL:
  #define A_ALWAYS_ACTIVE
```

The same eight lines are excerpted in the source page [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl, lines 38-45].

With `A_ALWAYS_ACTIVE` defined, the `if (a_active)` in front of the A stores and of the prefetch inside the main loop is removed by the preprocessor:

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L307-L312` (code; store of chunk 0)

```glsl
  {
    // store chunk 0 -> slice 0
#ifndef A_ALWAYS_ACTIVE
    if (a_active)
#endif
    {
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L378-L383` (code; prefetch of the next chunk inside the main loop)

```glsl
      if (has_next) {
        const uint chunkK_nxt = (chunk + 1u) * WG_TILE_K;
#ifndef A_ALWAYS_ACTIVE
        if (a_active)
#endif
        {
```

## Rationale given by the code

The shader comment quoted above states the reason: when the A staging map exactly covers the workgroup, the guard is always true, "but the driver compiler does not fold it", because the bound of `gl_LocalInvocationID.x` comes from a spec constant, "so the comparison survives into the hot loop as a real branch" [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl, lines 38-45]. This is a statement of the shader authors. No source page of this wiki holds a disassembly or a timing that shows the branch.

## Condition for using it

The flag is only correct when the number of A blocks per chunk equals the workgroup size. The comment says to set it "only for tiles where the equality has been checked arithmetically" [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl, lines 38-45]. The two sides of the equality are:

- `A_ACTIVE_THREADS = (WG_TILE_M >> 2u) * K_BLOCKS_PER_CHUNK`, with `K_BLOCKS_PER_CHUNK = WG_TILE_K >> 2u` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L141-L142].
- `WG_SIZE = NUM_SUBGROUPS * SUBGROUP_SIZE`, with `NUM_SUBGROUPS = SG_GRID_X * SG_GRID_Y` [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh, lines 16-22].

The parameters of the 780M variant that enter these formulas are `WG_TILE_M: 128`, `WG_TILE_K: 32`, `SG_GRID_X: 4`, `SG_GRID_Y: 2` and `SUBGROUP_SIZE: 32` [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.yaml, lines 10-35 (lines 23, 25-28)]. For this tile the body comment states "A_ACTIVE_THREADS == WG_SIZE for this variant's tile" [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L146-L147]. The microbenchmark log of the device shows the kernel dispatched with local work size `(256,1,1)` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, lines 9-14 (line 10)].

The flag is not part of the variant name: "Any other shipped flag, such as zpg's `A_MAP_FULL`, is not in the name. Read the yaml entry." [meas-780m-8da4w-port: sarc/SWEEP-PARAMETERS.md, line 121].

## Use on the Radeon 780M

- Both shipped 780M variants of the family set `A_MAP_FULL: true` in the yaml: `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half` and `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half` [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.yaml, lines 10-35 (lines 31-35)].
- The table of shipped release 1.5 variants lists the Radeon 780M 8da4w kernel as "zpg `t128x64k32g42s32` + `A_MAP_FULL`" [meas-780m-8da4w-port: sarc/SWEEP-PARAMETERS.md, lines 125-127].
- The selection row for the device is commented "Radeon 780M 8da4w: zpg (4h4w activations), full A map", names the kernel base `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32`, and has status `Status::kVerified` [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 42-53].
- Dispatch on the device: in the production-diff re-run the Llama 3.2 1B wq_wo buffer case reports `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED`, and the file ends with `[production-diff] ALL PASSED` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log, lines 7-51 (lines 17 and 51)]. The texture3d variant is reported the same way [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-texture3d.log, lines 7-51 (lines 17 and 51)].

Timings of this kernel on the device are on `kernel-linear-8da4w-780m`.

## What the measurements do and do not show

- Shown: the 780M variant that the yaml builds with `A_MAP_FULL: true` is the shipped one, it was dispatched on the device, and its output passed the production-diff check cited above.
- Not shown: no source page of this wiki holds an A/B measurement of the 780M tile with and without `A_MAP_FULL`. The result set compares the kernel with release 1.5's tiled kernel, not with a build of the same tile that keeps the guard.
- Not recorded: the result set identifies the binaries under test only by sha256 [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt, lines 3-7]. The microbenchmark and correctness logs of the 2026-09-27 `sarc8` run name the kernel `sarc_linear_dq8ca_zpg_t128x64k32g42s32_*`, the name before the rename [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 1-25 (line 2)]; see `pattern-coopmat-name-check-false-failure`. The yaml cited on this page is the one at the code commit above.

## Confidence

`source-reported`. The mechanism and the condition come from the shader source and the parameter documentation excerpted in `meas-780m-8da4w-port`. The benefit (one branch less in the hot loop) is asserted by the shader comment only; it is not isolated by a measurement.
