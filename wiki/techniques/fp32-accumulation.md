---
id: technique-fp32-accumulation
title: "fp32 accumulator matrix for fp16 cooperative-matrix operands (ACC_FP32) on the Radeon 780M"
type: technique
architectures: [radeon-780m]
tags: [fp32-accumulation, coopmat-fp32-accumulator, cooperative-matrix, linear-4w, gemm, prefill]
confidence: source-reported
reproducibility: snippet
prerequisites: [hw-cooperative-matrix-rdna3]
related: [hw-radeon-780m, technique-drain-in-a-staging, technique-workgroup-tile-sizing, kernel-linear-4w-780m]
sources: [meas-780m-4w-bootstrap, meas-780m-e2e-prefill]
aliases: ["ACC_FP32", "f32 tile token", "fp32 accumulate"]
---

# fp32 accumulator matrix for fp16 cooperative-matrix operands (ACC_FP32)

Scope: one device (Radeon 780M), one driver (RADV Mesa 25.2.7), measurements dated 2026-09-27 (`meas-780m-4w-bootstrap`) and 2026-09-28 (`meas-780m-e2e-prefill`). Nothing here is established for another device, driver or date.

"code" below means https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae. A citation of the form `[code: path#L]` points at that commit and is a statement of the code or its authors, not a measurement held in a source page of this wiki.

## What the technique is

The 4w linear kernel family `sarc_linear_q4gsw_coopmat` multiplies fp16 operands with cooperative-matrix multiply-add and keeps the running result in an accumulator matrix. The `ACC_FP32` flag switches the element type of that accumulator from fp16 to fp32: with the flag defined the shader sets `ACC_T` to `float`, otherwise to `float16_t` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.glsl#L119-L123].

The switch is one macro, `ACC_T`, used wherever the accumulator type is named.

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.glsl#L119-L123` (code)

```glsl
#ifdef ACC_FP32
#define ACC_T float
#else
#define ACC_T float16_t
#endif
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L187-L188` (code)

```glsl
coopmat<ACC_T, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator>
    result[MMAS_PER_SG_M][MMAS_PER_SG_N];
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L560-L562` (code)

```glsl
        [[unroll]] for (uint i = 0; i < MMAS_PER_SG_M; ++i) {
          result[i][j] = coopMatMulAdd(matA[i], matB, result[i][j]);
        }
```

`ACC_FP32` excludes the two other accumulation flags of the family, `ACC_GROUP_FP32` and `ACC_GROUP_FP32_REG`; the shader raises `#error` when they are combined [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.glsl#L113-L118].

## Use on the Radeon 780M

- In the variant name, the tile-token part `f32` stands for `ACC_FP32` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 91-104].
- The shipped release 1.5 4w variant for the Radeon 780M is `t128x128k32g42s32f32c` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 125-127], and the selection table describes the 780M tile as "t128x128k32g42s32 with fp32 accumulate and the drain staged in Ash" [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 19-41].
- The three 780M variants in the shader yaml (`texture3d_texture2d`, `buffer_texture2d`, `buffer_buffer`) all set `ACC_FP32: true` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.yaml#L41-L55].
- The variant was dispatched on the device. In the 2026-09-27 microbenchmark, 12 cases ran `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half` and 12 cases ran `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half` [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out, lines 1-25 (line 2)]. In the 2026-09-28 end-to-end campaign the texture3d variant was dispatched 112 times per Llama 3.2 1B prefill [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv, line 4].

## Rationale given by the code

The shader comment above the `ACC_T` definition attributes the choice to how the two WMMA instruction forms take their accumulator on this device: with an fp16 accumulator the packed accumulator is repacked around every multiply-add, whereas the fp32 accumulator maps directly onto the fp32-accumulate instruction [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.glsl#L107-L112]. The campaign's technical report says the same: "SARC 4w uses fp32 accumulation because RDNA3 WMMA with an fp16 accumulator is slower" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, lines 311-312]. The shader comment and that report line also quote rates for the two accumulator forms; they come from a roofline study that has no source page (with driver and date) in this wiki, so the figures are not repeated here.

## What the measurements on this page do and do not show

What is measured, with the `f32` variant in use:

| Model (4w, SARC build) | Achieved prefill-GEMM rate (`rate` column) | Citation |
|---|---|---|
| Llama 3.2 1B | 10.664 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv, line 14] |
| Llama 3.2 3B | 10.73 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv, line 15] |
| Llama 3.1 8B | 10.293 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv, line 16] |

The rate is defined as "Σ 2·M·N·K / Σ GPU time" over the prefill GEMM dispatches of one warm ETDump trace per cell [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, lines 76 and 78]. The values are copied from the `rate` column as written; the CSV row carries no unit. The same rows also hold `roof_value` and `pct_of_roof` columns; those depend on a separate roofline measurement that has no source page (with driver and date) in this wiki, so they are not repeated here. The achieved rates come from the 2026-09-28 traces.

What is not shown by any source page of this wiki:

- There is no A/B measurement of the same 780M tile with and without `ACC_FP32`. The comparisons in `meas-780m-4w-bootstrap` and `meas-780m-e2e-prefill` are between the SARC cooperative-matrix kernel and the stock or tiled kernels, which differ in much more than the accumulator type.
- The device-properties export does not enumerate cooperative-matrix shapes, so it does not confirm that an fp32 accumulator shape is exposed (see `hw-cooperative-matrix-rdna3`).

## Confidence

`source-reported`. That the 780M variant uses an fp32 accumulator is stated by the parameter documentation and the selection table excerpted in `meas-780m-4w-bootstrap`, and the variant's dispatch on the device is recorded in both measurement pages. The benefit of fp32 over fp16 accumulation on this device is asserted by the shader comment and the technical report only; no measurement in a source page isolates it.
