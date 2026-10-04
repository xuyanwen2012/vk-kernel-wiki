---
id: technique-drain-in-a-staging
title: "texture3d output drain staged in the dead A shared-memory region (CSH_IN_ASH) on the Radeon 780M"
type: technique
architectures: [radeon-780m]
tags: [drain-in-a-staging, storage-texture3d, cooperative-matrix, linear-4w, gemm, prefill]
confidence: source-reported
reproducibility: snippet
prerequisites: [hw-cooperative-matrix-rdna3]
related: [hw-radeon-780m, technique-fp32-accumulation, technique-workgroup-tile-sizing, kernel-linear-4w-780m]
sources: [meas-780m-4w-bootstrap, meas-780m-e2e-prefill]
aliases: ["CSH_IN_ASH", "c tile token", "drain staged in Ash"]
---

# texture3d output drain staged in the dead A shared-memory region (CSH_IN_ASH)

Scope: one device (Radeon 780M), one driver (RADV Mesa 25.2.7), measurements dated 2026-09-27 (`meas-780m-4w-bootstrap`) and 2026-09-28 (`meas-780m-e2e-prefill`). Nothing here is established for another device, driver or date.

"code" below means https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae. A citation of the form `[code: path#L]` points at that commit and is a statement of the code or its authors, not a measurement held in a source page of this wiki.

## What the technique is

When the 4w linear kernel `sarc_linear_q4gsw_coopmat` writes a texture3d output, the accumulator matrices are first stored to shared memory and then written out texel by texel (the "drain"). Without the flag, the drain is staged in its own shared array `Csh`. With `CSH_IN_ASH`, the drain is staged in `Ash`, the shared array that held the A operand during the multiply loop: the parameter table describes the flag as "texture3d output drain staged in the dead A shared-memory region" [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 38-39, 43].

With the flag set, the separate `Csh` array is not declared at all.

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L845-L859` (code; storing one accumulator matrix for the drain)

```glsl
#ifdef CSH_IN_ASH
      coopMatStore(
          coopmat<float16_t, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator>(result[i][j]), Ash,
          (warpInTile.y * MMA_M * WG_TILE_N +
              MMA_N * (MMAS_PER_SG_N * warpInTile.x + j)) / FP16_PER_VEC4,
          WG_TILE_N / FP16_PER_VEC4,
          gl_CooperativeMatrixLayoutRowMajor);
#else
      coopMatStore(
          coopmat<float16_t, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator>(result[i][j]), Csh,
          warpInTile.y * MMA_M * WG_TILE_N +
              MMA_N * (MMAS_PER_SG_N * warpInTile.x + j),
          WG_TILE_N,
          gl_CooperativeMatrixLayoutRowMajor);
#endif
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L870-L887` (code; reading the staged values back and writing the output texel)

```glsl
#ifdef CSH_IN_ASH
      // base is a multiple of 4 halves: the texel is one half of a uvec4.
      const uvec4 q = Ash[base / FP16_PER_VEC4];
      const bool hi = (base % FP16_PER_VEC4) != 0u;
      imageStore(
          t_output,
          ivec3(tile_n_start / 4u + lc4, m, 0),
          vec4(unpackHalf2x16(hi ? q.z : q.x), unpackHalf2x16(hi ? q.w : q.y)));
#else
      imageStore(
          t_output,
          ivec3(tile_n_start / 4u + lc4, m, 0),
          vec4(
              float(Csh[base]),
              float(Csh[base + 1u]),
              float(Csh[base + 2u]),
              float(Csh[base + 3u])));
#endif
```

Two things follow from the excerpts:

- `Ash` is a `uvec4` array in this configuration, so the drained values are stored through a `float16_t` cooperative matrix with offsets and stride divided by `FP16_PER_VEC4`, and read back with `unpackHalf2x16`.
- The store loop is followed by `memoryBarrierShared(); barrier();` before any invocation reads the staged values [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L861-L862].

The shader does not allow `CSH_IN_ASH` together with `CSH_FULL`, `CSH_BAND`, `CSH_POOL`, `SH_F16V4` or `ACC_GROUP_FP32_REG`; each combination raises `#error` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L65-L66, #L89-L90, #L138-L139, #L145-L146, #L201-L202].

## Use on the Radeon 780M

- The parameter table lists the 780M as the user of `CSH_IN_ASH`, with the remark "less LDS, higher occupancy" [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 38-39, 43].
- In the variant name, the tile-token part `c` stands for `CSH_IN_ASH` (4w) [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 91-104].
- The shipped release 1.5 4w variant for the Radeon 780M is `t128x128k32g42s32f32c` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 125-127]. The selection table calls the tile "t128x128k32g42s32 with fp32 accumulate and the drain staged in Ash", and the last field of its `TileDims` initializer `{128, 128, 32, 4, 2, 32, 16, true}` is `true` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 19-41]. That last field is `csh_in_ash`, commented "texture3d drain staged in Ash (no extra Csh LDS)" [code: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h#L88].
- The texture3d variant ran on the device: `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half` was dispatched in 12 microbenchmark cases on 2026-09-27 [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out, lines 1-25 (line 2)], and the 2026-09-28 campaign states that all prefill linears in its models use texture3d activations [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 350-353].
- Production-diff of the texture3d variant passed for the three models at M=2048 [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out, lines 1-25 (lines 13, 15, 17)].

The buffer-output variants of the 780M also carry `CSH_IN_ASH: true` in the yaml [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.yaml#L48-L55], but the flag is documented as acting on the texture3d output drain.

## Rationale given by the code

The comment at the `Csh` declaration gives the authors' reason for the 780M: `Ash` is dead after the last multiply-add and every drain iteration starts with a barrier, so the drain can reuse it; removing `Csh` lowers the shared memory per workgroup and the register count, which raises occupancy [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L159-L162]. That comment also quotes figures for the saving and the resulting gain; they are not excerpted in any source page of this wiki and are not repeated here.

## What the measurements on this page do and do not show

- Shown: the variant with `CSH_IN_ASH` is the one dispatched on the device, and its texture3d output passed the numeric checks cited above.
- Not shown: no source page of this wiki holds an A/B measurement of the 780M tile with and without `CSH_IN_ASH`. The microbenchmark in `meas-780m-4w-bootstrap` times the texture3d and buffer variants of the same tile, both built with the flag; it does not isolate the flag.

## Confidence

`source-reported`. The description of the flag and its use by the 780M come from the documentation and selection table excerpted in `meas-780m-4w-bootstrap`. The occupancy benefit is asserted by the documentation and the shader comment only.
