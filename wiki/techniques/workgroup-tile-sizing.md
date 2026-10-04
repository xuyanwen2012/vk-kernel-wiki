---
id: technique-workgroup-tile-sizing
title: "Output tile per workgroup (WG_TILE_M x WG_TILE_N) in the Radeon 780M cooperative-matrix kernels"
type: technique
architectures: [radeon-780m]
tags: [workgroup-tile-sizing, subgroup-grid, cooperative-matrix, linear-4w, linear-8da4w-zpg, sdpa-qk, sdpa-av, gemm, prefill]
confidence: source-reported
reproducibility: snippet
prerequisites: [hw-cooperative-matrix-rdna3]
related: [hw-radeon-780m, technique-fp32-accumulation, technique-drain-in-a-staging, pattern-unaligned-m-fallback, kernel-linear-4w-780m, kernel-linear-8da4w-780m]
sources: [meas-780m-4w-bootstrap, meas-780m-e2e-prefill]
aliases: ["WG_TILE_M", "WG_TILE_N", "t<M>x<N> tile token", "tile alignment"]
---

# Output tile per workgroup (WG_TILE_M x WG_TILE_N)

Scope: one device (Radeon 780M), one driver (RADV Mesa 25.2.7), measurements dated 2026-09-27 (`meas-780m-4w-bootstrap`) and 2026-09-28 (`meas-780m-e2e-prefill`). Nothing here is established for another device, driver or date.

"code" below means https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae. A citation of the form `[code: path#L]` points at that commit and is a statement of the code or its authors, not a measurement held in a source page of this wiki.

## What the technique is

Each workgroup of a SARC cooperative-matrix kernel computes one fixed output tile. `WG_TILE_M` and `WG_TILE_N` are the "Output tile per workgroup"; `SG_GRID_X` and `SG_GRID_Y` are the "Subgroup grid in the workgroup (X along N, Y along M)", with "workgroup size = X·Y·`SUBGROUP_SIZE`" [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 22-26, 29-32].

The tile is divided among the subgroups of the grid, and each subgroup's share is divided into cooperative-matrix multiply-adds.

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L21-L27` (code)

```glsl
const uint NUM_SUBGROUPS = SG_GRID_X * SG_GRID_Y;
const uint WG_SIZE = NUM_SUBGROUPS * SUBGROUP_SIZE;

const uint SG_TILE_M = WG_TILE_M / SG_GRID_Y;
const uint SG_TILE_N = WG_TILE_N / SG_GRID_X;
const uint MMAS_PER_SG_M = SG_TILE_M / MMA_M;
const uint MMAS_PER_SG_N = SG_TILE_N / MMA_N;
```

In a variant name the tile-token part `t<M>x<N>` gives `WG_TILE_M` × `WG_TILE_N`, `k<K>` gives `WG_TILE_K`, `g<X><Y>` gives `SG_GRID_X`, `SG_GRID_Y` and `s<S>` gives `SUBGROUP_SIZE` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 91-104].

## Tiles used on the Radeon 780M

| Operator | Kernel dispatched on the device | Citation |
|---|---|---|
| 4w linear | `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv, line 4] |
| 8da4w linear | `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv, line 18] |
| SDPA QK^T | `sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv, line 7] |
| SDPA attn*V | `sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv, line 6] |

The shipped release 1.5 linear variants for the Radeon 780M are 4w `t128x128k32g42s32f32c` and 8da4w zpg `t128x64k32g42s32` + `A_MAP_FULL` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 125-127]. The 4w selection row carries the tile as `TileDims` `{128, 128, 32, 4, 2, 32, 16, true}` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 19-41]; the field order of `TileDims` is `m`, `n`, `k`, `sg_grid_x`, `sg_grid_y`, `subgroup_size`, `mma_m`, `csh_in_ash` [code: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h#L80-L88]. The `TileDims` of the other three 780M rows are tabulated on `hw-cooperative-matrix-rdna3`.

The launch dimensions come from the selection row: "Launch dims come from the row. Nothing parses kernel names." [meas-780m-4w-bootstrap: sarc/README.md, lines 18-24].

## The cost of a fixed tile: shape preconditions

The shaders contain no shape checks. The selector enforces, when it matches a row, "`M % WG_TILE_M == 0`, `N % WG_TILE_N == 0`, `K % WG_TILE_K == 0`" and "`group_size % WG_TILE_K == 0`" [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 74-81].

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/Select.cpp#L137-L141` (code)

```cpp
  if (!shape.ignore_alignment &&
      (shape.M % dims.m != 0 || shape.N % dims.n != 0 ||
       shape.K % dims.k != 0 || shape.group_size % dims.k != 0)) {
    return false;
  }
```

Consequences recorded for the 780M:

- For shapes no row covers, the 4w operator "falls back to release 1.5's own `linear_q4gsw_{tiled,coop}` kernels: decode, unaligned M, bias, fp32" [meas-780m-4w-bootstrap: sarc/README.md, lines 18-24].
- The campaign's check prompt is an unaligned case: "At 1972 tokens, M is not a multiple of any tile" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 320-327]. For the 780M Llama 3.1 8B 8da4w cell at that length the report gives the SARC path as "GEMM falls back to stock kernels; attention still uses SARC kernels" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, lines 390-394].
- The single-token output projection is not covered by the tile kernel: it ran `q4gsw_linear_gemv_coop__w_4x8_nc_buffer_g8w8_buffer_half`, 1 dispatch, in the SARC build as in the stock build [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv, lines 3 and 11].

What this looks like from outside, and how the 2026-09-28 campaign dealt with it, is described in `pattern-unaligned-m-fallback`.

## Shapes on which the 780M tiles were exercised

All 24 4w prefill shapes of the microbenchmark (1B/3B/8B × 4 ops × buffer/texture3d, M=2048) dispatched the `t128x128k32g42s32f32c` kernel [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md, lines 55-80; openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out, lines 1-25 (line 2)]. In the end-to-end campaign the SARC linear kernel was dispatched 112 times per prefill for 1B, 196 for 3B and 224 for 8B [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 350-353].

## What the measurements on this page do and do not show

- Shown: which tiles ship for the 780M, that they were dispatched on the device at tile-aligned prefill shapes, and that the selector rejects non-divisible shapes.
- Not shown: no source page of this wiki compares different `WG_TILE_M` × `WG_TILE_N` choices on the 780M. This page therefore makes no claim that the shipped tile sizes are faster than any alternative.

## Confidence

`source-reported`. The parameter meanings, the shipped tiles and the preconditions are stated by the documentation and code excerpted in the two measurement pages; the dispatch of those tiles on the device is recorded there.
