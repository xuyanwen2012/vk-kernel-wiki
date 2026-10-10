---
id: migration-rdna3-to-xe2
title: "Porting the fused attention kernel from AMD RDNA3 (RADV) to Intel Xe2 (ANV)"
type: migration
from_arch: rdna3
to_arch: xe2
tags: [kernel-fusion, sdpa, coopmat-shape, mma-shape-selection, subgroup-size, required-subgroup-size, subgroup-grid, control-barrier, full-subgroups, shared-memory-limit, cooperative-matrix, prefill]
confidence: verified
reproducibility: snippet
prerequisites: [technique-fused-attention-kernel]
related: [technique-fused-attention-kernel, pattern-invalid-usage-that-passes-tests, hw-cooperative-matrix-rdna3]
sources: [meas-b580-fused-port, meas-b70-fused-port, meas-780m-vulkaninfo]
evidence_basis:
  - evidence_type: measurement
    source_id: meas-b580-fused-port
    locator: "proposal.md, lines 62-118; STATUS.md, lines 442-477"
  - evidence_type: measurement
    source_id: meas-b70-fused-port
    locator: "proposal.md, lines 276-291"
---

# RDNA3 to Xe2: the fused attention kernel

**Do:** change the matrix shape mechanically, then read the compiler's spill statistics before timing anything, and expect to split the workgroup into several subgroups. **Do not** keep the RDNA3 tiles: on both Xe2 cards they were several times slower than the three kernels they were meant to replace.

Scope: one kernel (`technique-fused-attention-kernel`), ported from the Radeon 780M / RX 7600 form to the Arc B580 and confirmed unchanged on the Arc Pro B70; ANV Mesa 26.2.3, 2026-10-09. Files in citations are relative to the campaign change directory named in the measurement page's `raw_data`. **The linear kernels are not covered here:** their Xe2 changes are in earlier campaigns that have no source page in this wiki yet.

## What differs

| Property | RDNA3 (source kernel) | Xe2 (ported kernel) | Citation |
|---|---|---|---|
| fp16 matrix shape M x N x K | 16 x 16 x 16, one constant `MMA = 16` | 8 x 16 x 16 only ("ANV exposes fp16 8 x 16 x 16 only"); three constants `MMA_M = 8`, `MMA_N = 16`, `MMA_K = 16` | [meas-b580-fused-port: proposal.md, line 73] |
| Subgroup size the kernel runs with | written for 32; not required by the pipeline, and the size the driver actually ran it with is unverified (device default 64, minimum 32 on the 780M) | 16, required by the pipeline; "Intel runs 8, 16 or 32 lanes" | [meas-b580-fused-port: proposal.md, line 78] [meas-780m-vulkaninfo: sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, lines 1232 and 1340-1341] |
| Registers per thread as the compiler reports them | not the limit in the source kernel | 128 registers = 4096 bytes of 16-lane values | [meas-b580-fused-port: proposal.md, lines 88-89] |
| Shared-memory limit | 780M value on `hw-cooperative-matrix-rdna3` | 49152 bytes | [meas-b580-fused-port: proposal.md, line 111] |

## Step 1: matrix shape (mechanical)

The M of every product is the query row, so the score, e, accumulator, Q and divisor tiles become 8 rows x 16; the K^T and V operand tiles are K x N = 16 x 16 and do not change, so the packed K / V copies and the copy shader are reused; tile counts and row offsets follow `MMA_M` [meas-b580-fused-port: proposal.md, lines 74-77].

Single-subgroup declarations (https://github.com/sarc-acl/executorch at commit 8f8c44e22e2d8c62a6a192f00e252f8768486b0d, `backends/vulkan/runtime/graph/ops/glsl/sarc_dev/sarc_dev_4070ti_sdpa_fused3sb.glsl#L120-L121`, which the file's header says is the RDNA3 text from `#version` on):

```glsl
coopmat<float, gl_ScopeSubgroup, MMA, MMA, gl_MatrixUseAccumulator> sc[MMAS_M][MMAS_C];
coopmat<float, gl_ScopeSubgroup, MMA, MMA, gl_MatrixUseAccumulator> acc[MMAS_M][MMAS_D];
```

Xe2 declarations (commit a434a49623600f168089173a964efc79661ac286, `.../sarc_dev/sarc_dev_b580_sdpa_fused.glsl#L169`, `#L172` and `#L175`):

```glsl
coopmat<float, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator> acc[MMAS_M][MMAS_D / SGS];
coopmat<float, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator> sc[MMAS_M][MMAS_C];
coopmat<float16_t, gl_ScopeSubgroup, MMA_M, MMA_K, gl_MatrixUseA> aq[MMAS_M][MMAS_D];
```

Result of this step alone on the B580: correct in five tiers with 0 mismatches, and 5.9 ms against 2.0 ms (head_dim 64) and 14.4 ms against 2.3 ms (head_dim 128, 8B) for the three kernels [meas-b580-fused-port: proposal.md, lines 82-84].

## Step 2: unit of work (not mechanical)

The source kernel assumes one subgroup keeps all its tiles in registers. At 16 lanes that fails: the head_dim 128 shape of the 780M compiles to 15093 to 16537 instructions with 1114 to 1250 spills; the multi-subgroup variants compile to 768 to 1155 instructions with 0 spills [meas-b580-fused-port: STATUS.md, lines 451-455].

| Item | RDNA3 | Xe2 | Citation (all meas-b580-fused-port: proposal.md) |
|---|---|---|---|
| Workgroup | one subgroup, 16 or 32 rows | G = 4 or 8 subgroups of 16 lanes, 16 rows; local size G x 16 | line 96 |
| Accumulators | all head_dim tiles in one subgroup | each subgroup owns `HEAD_DIM / 16 / G` head_dim tiles | line 97 |
| Scores of a block | all tiles by the one subgroup | subgroup g computes columns `j % G == g`, one column at a time | line 98 |
| Barriers | `memoryBarrierShared()` plus `subgroupBarrier()` | `memoryBarrierShared(); barrier();` | line 101 |
| One-pass rescale decision | `subgroupAny(new_max > row_max)` | an atomic flag in shared memory read after a barrier | line 102 |
| Q tiles | registers | head_dim 64: registers; head_dim 128: loaded per product | line 103 |
| Layout check | assumed | `gl_NumSubgroups == G`, `gl_SubgroupSize == 16`, NaN rows otherwise | line 104 |

Tried and dropped on the way: keeping one column of score tiles live in the single-subgroup form (no real effect) and moving the accumulators to shared memory ("Slower in every case") [meas-b580-fused-port: STATUS.md, lines 462-466].

Selected variants: `d64_t16x64s16m8g4roj` and `d128_t16x128s16m8g8oj`; shared memory 3588 and 5892 bytes [meas-b580-fused-port: proposal.md, lines 116-117 and 321].

## Outcome

| Device, driver, date | Kernel time per layer, three kernels -> fused (1B / 3B / 8B) | End to end over the tuned parent | Citation |
|---|---|---|---|
| Arc B580, ANV Mesa 26.2.3, 2026-10-09 | 1989 / 1771 / 2297 us -> 724 / 1139 / 1464 us | +9.12 % geomean, `GATE_PASS` | [meas-b580-fused-port: proposal.md, lines 310 and 319-321] |
| Arc Pro B70, ANV Mesa 26.2.3, 2026-10-09 | 1481 / 1285 / 1691 us -> 486 / 749 / 967 us | +8.26 % geomean, `GATE_PASS` | [meas-b70-fused-port: proposal.md, lines 283-288 and 310] |

The second card needed no port: the B580's shaders were brought over with byte-identical SPIR-V, one screen was repeated and the same pair won [meas-b70-fused-port: proposal.md, lines 59-63 and 291].

## Carry over, and do not carry over

- Carry over: the arithmetic, the block walk, the masks, the packed K / V layout and the copy shader [meas-b580-fused-port: proposal.md, lines 66-67 and 75].
- Do not carry over: the tiles, the one-subgroup assumption, `subgroupBarrier()` as the exchange barrier, or `subgroupAny` as the rescale vote.
- Still open on Xe2: the pipelines lack the full-subgroups flag, which the multi-subgroup lane mapping depends on (`pattern-invalid-usage-that-passes-tests`), and decode was up to 2.5 % slower with the fused node present [meas-b70-fused-port: proposal.md, lines 382-385].

## What this does not show

- Two cards of one generation on one driver version; nothing for Xe3 or for an integrated Xe2 GPU.
- No two-pass multi-subgroup variant was among the selected or screened pairs cited here.
- The register figure is the compiler's statistic for this kernel, not a hardware specification.
