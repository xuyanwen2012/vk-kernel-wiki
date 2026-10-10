---
id: doc-cubek-matmul
title: 'CubeK matmul (Burn / CubeCL; Rust kernels compiled to WGSL, SPIR-V, CUDA and others, not GLSL): tiling scheme, plane selector, double buffering'
author: Tracel Technologies Inc. and CubeK contributors
url: https://github.com/tracel-ai/cubek/tree/ea03524e1fa44a5c89f95f0fe19b9b74f9f2c461/crates/cubek-matmul
source_category: official-doc
architectures: []
tags:
- gemm
- workgroup-tile-sizing
- k-chunk-sizing
- double-buffering
- subgroup-size
- device-specific-tuning
retrieved_at: '2026-10-10'
description: 'Language / backend: Rust with the CubeCL #[cube] macro, compiled per backend (wgpu/WGSL, SPIR-V, CUDA, Metal). A plane is CubeCL''s name for a subgroup and a cube for a workgroup'
---

# CubeK matmul (Burn / CubeCL; Rust kernels compiled to WGSL, SPIR-V, CUDA and others, not GLSL): tiling scheme, plane selector, double buffering

Language and backend of the source: Rust, written against CubeCL and compiled per backend (WGSL through wgpu, SPIR-V, CUDA, Metal); not GLSL. In the quoted code a "plane" is a subgroup, a "cube" a workgroup and a "unit" one invocation.

## Excerpt: crates/cubek-matmul/src/multi_level/definition/tiling_scheme.rs, lines 4-12 (the four tiling levels)

Locator: https://github.com/tracel-ai/cubek/blob/ea03524e1fa44a5c89f95f0fe19b9b74f9f2c461/crates/cubek-matmul/src/multi_level/definition/tiling_scheme.rs#L4-L12

```text
#[derive(Debug, Copy, Clone, Hash, PartialEq, Eq)]
/// Complete tiling configuration for a matmul.
/// Encodes all structural information needed to compute tiling shapes and counts.
pub struct TilingScheme {
    pub tile_size: TileSize,
    pub partition_size: PartitionSize,
    pub stage_size: StageSize,
    pub global_partition_size: GlobalPartitionSize,
}
```

## Excerpt: crates/cubek-matmul/src/multi_level/routines/selector/plane.rs, lines 103-124 (planes per cube, reduced to compensate for register use)

Locator: https://github.com/tracel-ai/cubek/blob/ea03524e1fa44a5c89f95f0fe19b9b74f9f2c461/crates/cubek-matmul/src/multi_level/routines/selector/plane.rs#L103-L124

```text
    let row_count = options.row_count.unwrap_or_else(|| {
        #[cfg(target_os = "macos")]
        // If we allow too many units it will select a large plane_count and fail with Cube Dim too large
        let max_units_per_cube = min(client.properties().hardware.max_units_per_cube, 256);
        #[cfg(not(target_os = "macos"))]
        let max_units_per_cube = client.properties().hardware.max_units_per_cube;

        let max_plane_per_cube = max_units_per_cube / plane_dim;
        // Compensate for register use
        let precision_factor = match dtypes.lhs_stage.size() >= 4 {
            true => 2,
            false => 1,
        };
        let mut tile_factor = tile_size.n().div_ceil(4);
        if problem.m as u32 <= tile_size.m() * 4 || problem.n as u32 <= tile_size.n() * 4 {
            tile_factor = 8;
        }
        // The compensation narrows the cube, never below one plane: a cube of one plane runs,
        // and declining here would make the routine's availability hinge on where the problem
        // falls inside its autotune bucket. A device that fits no plane in a cube still declines.
        (max_plane_per_cube / (tile_factor * precision_factor)).max(max_plane_per_cube.min(1))
    });
```

## Excerpt: crates/cubek-matmul/src/multi_level/routines/selector/plane.rs, lines 266-294 (rows per plane and stage size)

Locator: https://github.com/tracel-ai/cubek/blob/ea03524e1fa44a5c89f95f0fe19b9b74f9f2c461/crates/cubek-matmul/src/multi_level/routines/selector/plane.rs#L266-L294

```text
fn select_size(
    strategy: MultiRowStrategy,
    plane_count: usize,
    instruction_m: usize,
    problem_m: usize,
) -> (usize, usize, usize) {
    let rows = match strategy {
        MultiRowStrategy::Never => 1,
        MultiRowStrategy::Always(count) => count,
        MultiRowStrategy::Adaptive {
            minimum_stage_count,
        } => {
            if problem_m > plane_count * instruction_m * minimum_stage_count as usize {
                2
            } else {
                1
            }
        }
    } as usize;

    // The number of rows handled per plane cannot exceed the number of available
    // planes: otherwise `plane_count / rows` underflows to 0, producing a degenerate
    // tiling scheme with `stage_size.m == 0` that divides by zero in
    // `BatchMatmulBlueprint::cube_launch_info`. Clamp so there is always at least one stage
    // along `m` (e.g. a large `problem_m` requesting 2 rows when only 1 plane fits).
    let rows = rows.min(plane_count).max(1);

    (rows, plane_count / rows, plane_count)
}
```

## Excerpt: crates/cubek-matmul/src/multi_level/routines/selector/plane.rs, lines 340-356 (tiny problems: partition along K)

Locator: https://github.com/tracel-ai/cubek/blob/ea03524e1fa44a5c89f95f0fe19b9b74f9f2c461/crates/cubek-matmul/src/multi_level/routines/selector/plane.rs#L340-L356

```text
fn selection_tiny(
    client: &Client,
    problem: &MatmulProblem,
    tile_size: TileSize,
    plane_dim: u32,
    tile_matmul: TileMatmulKind,
) -> BatchMatmulBlueprint {
    // If the K axis is big, we can leverage that.
    let pk = u32::min(problem.k as u32 / tile_size.k(), 8);
    let pk = u32::max(pk, 1);

    let tiling_scheme = TilingScheme::builder()
        .with_tile_size(tile_size)
        .with_partition_size(PartitionSize::new(1, 1, pk))
        .with_stage_size((1, 1, 1).into())
        .build()
        .unwrap();
```

## Excerpt: crates/cubek-matmul/src/multi_level/components/global/multi_stage/double_buffering/matmul.rs, lines 37-39 (double buffering)

Locator: https://github.com/tracel-ai/cubek/blob/ea03524e1fa44a5c89f95f0fe19b9b74f9f2c461/crates/cubek-matmul/src/multi_level/components/global/multi_stage/double_buffering/matmul.rs#L37-L39

```text
/// Performs matrix multiplication at the global level, with planes pipelining their work using two buffers:
/// While they trigger a load event from global memory to shared memory on stage A,
/// they trigger a computation event from tensor cores on stage B. Then stages are switched.
```

Licence of the excerpts: MIT OR Apache-2.0 (`license` in the workspace `Cargo.toml`; `LICENSE-MIT`, `LICENSE-APACHE`).
