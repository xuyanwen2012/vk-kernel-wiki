---
id: kernel-linear-4w-780m
title: "4w linear (fp16 activations, 4-bit weights) cooperative-matrix kernel on the Radeon 780M: sarc_linear_q4gsw_coopmat t128x128k32g42s32f32c"
type: kernel
architectures: [radeon-780m]
tags: [linear-4w, gemm, prefill, tiled-linear, cooperative-matrix, coopmat-fp32-accumulator, subgroup-size, subgroup-size-control, wave64, storage-texture3d, storage-buffer, storage-texture2d, workgroup-tile-sizing, k-chunk-sizing, subgroup-grid, required-subgroup-size, fp32-accumulation, drain-in-a-staging, double-buffering]
confidence: verified
reproducibility: snippet
kernel_types: [linear-4w, gemm, prefill]
languages: [glsl]
aliases: ["sarc_linear_q4gsw_coopmat", "t128x128k32g42s32f32c", "q4gsw coopmat 780M", "4w linear 780M"]
related: [hw-radeon-780m, hw-cooperative-matrix-rdna3, kernel-linear-8da4w-780m, kernel-sdpa-prefill-780m, technique-fp32-accumulation, technique-drain-in-a-staging, technique-workgroup-tile-sizing, pattern-unaligned-m-fallback]
sources: [meas-780m-4w-bootstrap, meas-780m-e2e-prefill, meas-780m-vulkaninfo]
version_sensitive: vs-radv-coopmat-lowering-after-25-2-7
evidence_basis:
  - evidence_type: measurement
    source_id: meas-780m-4w-bootstrap
    locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L11-L34; openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/correctness.log#L271-L272; openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-*-4w-*.log#L43; openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out#L2"
  - evidence_type: measurement
    source_id: meas-780m-e2e-prefill
    locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L2-L4; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L4, #L32, #L60; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv rows gpu=780m,scheme=4w"
  - evidence_type: measurement
    source_id: meas-780m-vulkaninfo
    locator: "sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, lines 687, 1232, 1340"
performance_claims:
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B wq_wo, M=2048, K=4096, N=4096, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 6481
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L11 cases[0].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L11 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B wq_wo, M=2048, K=4096, N=4096, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 16314.4
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L11 cases[0].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B wq_wo, M=2048, K=4096, N=4096, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 6481.4
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L12 cases[1].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L12 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B wq_wo, M=2048, K=4096, N=4096, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 16320.7
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L12 cases[1].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B wk_wv, M=2048, K=4096, N=1024, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 1716.96
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L13 cases[2].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L13 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B wk_wv, M=2048, K=4096, N=1024, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 4089.84
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L13 cases[2].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B wk_wv, M=2048, K=4096, N=1024, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 1732.96
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L14 cases[3].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L14 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B wk_wv, M=2048, K=4096, N=1024, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 4083.16
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L14 cases[3].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B w1_w3, M=2048, K=4096, N=14336, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 22023.1
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L15 cases[4].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L15 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B w1_w3, M=2048, K=4096, N=14336, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 57203.9
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L15 cases[4].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B w1_w3, M=2048, K=4096, N=14336, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 22060.3
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L16 cases[5].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L16 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B w1_w3, M=2048, K=4096, N=14336, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 57293.3
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L16 cases[5].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B w2, M=2048, K=14336, N=4096, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 22098.7
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L17 cases[6].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L17 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B w2, M=2048, K=14336, N=4096, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 57492.9
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L17 cases[6].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B w2, M=2048, K=14336, N=4096, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 22312.4
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L18 cases[7].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L18 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B w2, M=2048, K=14336, N=4096, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 57557.6
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L18 cases[7].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B wq_wo, M=2048, K=3072, N=3072, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 3582.48
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L19 cases[8].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L19 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B wq_wo, M=2048, K=3072, N=3072, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 9143.62
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L19 cases[8].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B wq_wo, M=2048, K=3072, N=3072, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 3545.96
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L20 cases[9].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L20 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B wq_wo, M=2048, K=3072, N=3072, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 9160.06
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L20 cases[9].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B wk_wv, M=2048, K=3072, N=1024, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 1256.44
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L21 cases[10].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L21 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B wk_wv, M=2048, K=3072, N=1024, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 3073.8
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L21 cases[10].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B wk_wv, M=2048, K=3072, N=1024, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 1276.52
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L22 cases[11].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L22 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B wk_wv, M=2048, K=3072, N=1024, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 3074.28
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L22 cases[11].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B w1_w3, M=2048, K=3072, N=8192, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 9404.12
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L23 cases[12].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L23 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B w1_w3, M=2048, K=3072, N=8192, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 24486.5
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L23 cases[12].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B w1_w3, M=2048, K=3072, N=8192, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 9389.78
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L24 cases[13].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L24 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B w1_w3, M=2048, K=3072, N=8192, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 24522.6
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L24 cases[13].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B w2, M=2048, K=8192, N=3072, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 9488.56
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L25 cases[14].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L25 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B w2, M=2048, K=8192, N=3072, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 24595.6
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L25 cases[14].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B w2, M=2048, K=8192, N=3072, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 9597.64
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L26 cases[15].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L26 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B w2, M=2048, K=8192, N=3072, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 24609.1
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L26 cases[15].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B wq_wo, M=2048, K=2048, N=2048, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 1607.96
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L27 cases[16].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L27 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B wq_wo, M=2048, K=2048, N=2048, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 4094.84
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L27 cases[16].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B wq_wo, M=2048, K=2048, N=2048, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 1598.5
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L28 cases[17].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L28 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B wq_wo, M=2048, K=2048, N=2048, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 4090.64
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L28 cases[17].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B wk_wv, M=2048, K=2048, N=512, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 438.52
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L29 cases[18].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L29 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B wk_wv, M=2048, K=2048, N=512, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 1065.8
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L29 cases[18].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B wk_wv, M=2048, K=2048, N=512, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 443.84
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L30 cases[19].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L30 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B wk_wv, M=2048, K=2048, N=512, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 1062.44
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L30 cases[19].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B w1_w3, M=2048, K=2048, N=8192, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 6297.8
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L31 cases[20].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L31 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B w1_w3, M=2048, K=2048, N=8192, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 16309.5
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L31 cases[20].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B w1_w3, M=2048, K=2048, N=8192, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 6246.16
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L32 cases[21].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L32 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B w1_w3, M=2048, K=2048, N=8192, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 16300.6
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L32 cases[21].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B w2, M=2048, K=8192, N=2048, group_size=128, batch 1, IO texture3d, weights texture2d"
    metric: kernel_median_us
    value: 6479.96
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L33 cases[22].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half: results/780m/stock/linear-4w.json#L33 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B w2, M=2048, K=8192, N=2048, group_size=128, batch 1, IO texture3d"
    metric: kernel_median_us
    value: 16523.3
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L33 cases[22].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B w2, M=2048, K=8192, N=2048, group_size=128, batch 1, IO buffer, weights texture2d"
    metric: kernel_median_us
    value: 6538.68
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L34 cases[23].kernel_median_us"
    baseline: "stock release 1.5 build, same shape and storage, kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half: results/780m/stock/linear-4w.json#L34 (separate claim)"
    notes: "3 warmup + 5 timed runs (#L7-L8); dev build, ET_VK_SARC_UNVERIFIED=1; kernel sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B w2, M=2048, K=8192, N=2048, group_size=128, batch 1, IO buffer"
    metric: kernel_median_us
    value: 16547.7
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L34 cases[23].kernel_median_us"
    notes: "Baseline measurement: stock release 1.5 build, upstream kernel q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half; 3 warmup + 5 timed runs (#L7-L8)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC dev build (ET_VK_SARC_UNVERIFIED=1), default mode"
    metric: prefill_tokens_per_second_single_run
    value: 1915.81
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-default.log#L6 prefill_token_per_sec"
    baseline: "same change, same day: stock release 1.5 build (upstream q4gsw_linear_gemm__tin__w_4x8) and the dev build with ET_VK_FORCE_TILED_LINEAR; separate claims"
    notes: "End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC dev build, ET_VK_FORCE_TILED_LINEAR (tiled)"
    metric: prefill_tokens_per_second_single_run
    value: 714.336
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-tiled.log#L6 prefill_token_per_sec"
    notes: "Baseline measurement. End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: stock release 1.5 build"
    metric: prefill_tokens_per_second_single_run
    value: 1204.71
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-1b-4w-default.log#L5 prefill_token_per_sec"
    notes: "Baseline measurement. End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC release export (row verified, no env)"
    metric: prefill_tokens_per_second_single_run
    value: 1930.25
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-1b-4w-default.log#L5 prefill_token_per_sec"
    baseline: "same change, same day: stock release 1.5 build (upstream q4gsw_linear_gemm__tin__w_4x8) and the dev build with ET_VK_FORCE_TILED_LINEAR; separate claims"
    notes: "End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC dev build (ET_VK_SARC_UNVERIFIED=1), default mode"
    metric: prefill_tokens_per_second_single_run
    value: 683.35
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-default.log#L6 prefill_token_per_sec"
    baseline: "same change, same day: stock release 1.5 build (upstream q4gsw_linear_gemm__tin__w_4x8) and the dev build with ET_VK_FORCE_TILED_LINEAR; separate claims"
    notes: "End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC dev build, ET_VK_FORCE_TILED_LINEAR (tiled)"
    metric: prefill_tokens_per_second_single_run
    value: 246.065
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-tiled.log#L6 prefill_token_per_sec"
    notes: "Baseline measurement. End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: stock release 1.5 build"
    metric: prefill_tokens_per_second_single_run
    value: 421.486
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-3b-4w-default.log#L5 prefill_token_per_sec"
    notes: "Baseline measurement. End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC release export (row verified, no env)"
    metric: prefill_tokens_per_second_single_run
    value: 689.795
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-3b-4w-default.log#L5 prefill_token_per_sec"
    baseline: "same change, same day: stock release 1.5 build (upstream q4gsw_linear_gemm__tin__w_4x8) and the dev build with ET_VK_FORCE_TILED_LINEAR; separate claims"
    notes: "End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC dev build (ET_VK_SARC_UNVERIFIED=1), default mode"
    metric: prefill_tokens_per_second_single_run
    value: 351.951
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-default.log#L6 prefill_token_per_sec"
    baseline: "same change, same day: stock release 1.5 build (upstream q4gsw_linear_gemm__tin__w_4x8) and the dev build with ET_VK_FORCE_TILED_LINEAR; separate claims"
    notes: "End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC dev build, ET_VK_FORCE_TILED_LINEAR (tiled)"
    metric: prefill_tokens_per_second_single_run
    value: 104.357
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-tiled.log#L6 prefill_token_per_sec"
    notes: "Baseline measurement. End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: stock release 1.5 build"
    metric: prefill_tokens_per_second_single_run
    value: 193.829
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-8b-4w-default.log#L5 prefill_token_per_sec"
    notes: "Baseline measurement. End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_tokens 2048), build: SARC release export (row verified, no env)"
    metric: prefill_tokens_per_second_single_run
    value: 352.193
    measured_at: '2026-09-27'
    source_id: meas-780m-4w-bootstrap
    source_locator: "openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-8b-4w-default.log#L5 prefill_token_per_sec"
    baseline: "same change, same day: stock release 1.5 build (upstream q4gsw_linear_gemm__tin__w_4x8) and the dev build with ET_VK_FORCE_TILED_LINEAR; separate claims"
    notes: "End to end, single llama_main run; this build has no SARC SDPA kernels (attention runs release 1.5's own kernels); clocks not pinned."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_2048.txt), build sarc (tag sarc/1.5-r2)"
    metric: prefill_tokens_per_second_median_of_5
    value: 2698.29
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L2 row gpu=780m,model=1b,scheme=4w column sarc_median"
    baseline: "build stock (upstream ExecuTorch release/1.5), same cell: column stock_median of the same row (separate claim)"
    notes: "End to end. The sarc build also dispatches the SARC SDPA kernels on this device (REPORT.md#L115-L116), so the value is not attributable to the 4w linear kernel alone. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_2048.txt), build stock (upstream release/1.5)"
    metric: prefill_tokens_per_second_median_of_5
    value: 1211.83
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L2 row gpu=780m,model=1b,scheme=4w column stock_median"
    notes: "Baseline measurement. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_2048.txt), sarc over stock"
    metric: end_to_end_speedup_ratio_of_medians_as_stated_by_source
    value: 2.2266241964632005
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L2 row gpu=780m,model=1b,scheme=4w column speedup"
    baseline: "build stock (upstream ExecuTorch release/1.5)"
    notes: "Ratio computed by the campaign's analyze.py (ratio of the medians, REPORT.md#L332), copied, not recomputed here. Includes the SARC SDPA kernels."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_2048.txt), build sarc (tag sarc/1.5-r2)"
    metric: prefill_tokens_per_second_median_of_5
    value: 1151.21
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L3 row gpu=780m,model=3b,scheme=4w column sarc_median"
    baseline: "build stock (upstream ExecuTorch release/1.5), same cell: column stock_median of the same row (separate claim)"
    notes: "End to end. The sarc build also dispatches the SARC SDPA kernels on this device (REPORT.md#L115-L116), so the value is not attributable to the 4w linear kernel alone. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_2048.txt), build stock (upstream release/1.5)"
    metric: prefill_tokens_per_second_median_of_5
    value: 425.073
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L3 row gpu=780m,model=3b,scheme=4w column stock_median"
    notes: "Baseline measurement. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_2048.txt), sarc over stock"
    metric: end_to_end_speedup_ratio_of_medians_as_stated_by_source
    value: 2.7082642275562083
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L3 row gpu=780m,model=3b,scheme=4w column speedup"
    baseline: "build stock (upstream ExecuTorch release/1.5)"
    notes: "Ratio computed by the campaign's analyze.py (ratio of the medians, REPORT.md#L332), copied, not recomputed here. Includes the SARC SDPA kernels."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_2048.txt), build sarc (tag sarc/1.5-r2)"
    metric: prefill_tokens_per_second_median_of_5
    value: 525.802
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L4 row gpu=780m,model=8b,scheme=4w column sarc_median"
    baseline: "build stock (upstream ExecuTorch release/1.5), same cell: column stock_median of the same row (separate claim)"
    notes: "End to end. The sarc build also dispatches the SARC SDPA kernels on this device (REPORT.md#L115-L116), so the value is not attributable to the 4w linear kernel alone. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_2048.txt), build stock (upstream release/1.5)"
    metric: prefill_tokens_per_second_median_of_5
    value: 198.008
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L4 row gpu=780m,model=8b,scheme=4w column stock_median"
    notes: "Baseline measurement. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_2048.txt), sarc over stock"
    metric: end_to_end_speedup_ratio_of_medians_as_stated_by_source
    value: 2.655458365318573
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L4 row gpu=780m,model=8b,scheme=4w column speedup"
    baseline: "build stock (upstream ExecuTorch release/1.5)"
    notes: "Ratio computed by the campaign's analyze.py (ratio of the medians, REPORT.md#L332), copied, not recomputed here. Includes the SARC SDPA kernels."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (112 dispatches of sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half), build sarc"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 373.745
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L2 row gpu=780m,model=1b,scheme=4w,build=sarc,family=prefill GEMM (linear layers) column ms"
    baseline: "build stock, same family: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L4."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build sarc"
    metric: achieved_prefill_gemm_rate_tflop_per_s
    value: 10.664
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L14 row gpu=780m,scheme=4w,build=sarc,model=1b column rate"
    baseline: "build stock, same model: separate claim"
    notes: "Rate = sum of 2*M*N*K over sum of GPU time, logical FLOPs (TECHNICAL-REPORT.md#L78, #L444)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (112 dispatches of q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half), build stock"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 927.709
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L14 row gpu=780m,model=1b,scheme=4w,build=stock,family=prefill GEMM (linear layers) column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L10."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build stock"
    metric: achieved_prefill_gemm_rate_tflop_per_s
    value: 4.296
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L17 row gpu=780m,scheme=4w,build=stock,model=1b column rate"
    notes: "Baseline measurement. Rate = sum of 2*M*N*K over sum of GPU time, logical FLOPs (TECHNICAL-REPORT.md#L78, #L444)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (196 dispatches of sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half), build sarc"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 1075.918
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L53 row gpu=780m,model=3b,scheme=4w,build=sarc,family=prefill GEMM (linear layers) column ms"
    baseline: "build stock, same family: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L32."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build sarc"
    metric: achieved_prefill_gemm_rate_tflop_per_s
    value: 10.73
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L15 row gpu=780m,scheme=4w,build=sarc,model=3b column rate"
    baseline: "build stock, same model: separate claim"
    notes: "Rate = sum of 2*M*N*K over sum of GPU time, logical FLOPs (TECHNICAL-REPORT.md#L78, #L444)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (196 dispatches of q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half), build stock"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 2715.137
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L65 row gpu=780m,model=3b,scheme=4w,build=stock,family=prefill GEMM (linear layers) column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L38."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build stock"
    metric: achieved_prefill_gemm_rate_tflop_per_s
    value: 4.252
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L18 row gpu=780m,scheme=4w,build=stock,model=3b column rate"
    notes: "Baseline measurement. Rate = sum of 2*M*N*K over sum of GPU time, logical FLOPs (TECHNICAL-REPORT.md#L78, #L444)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (224 dispatches of sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half), build sarc"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 2777.342
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L104 row gpu=780m,model=8b,scheme=4w,build=sarc,family=prefill GEMM (linear layers) column ms"
    baseline: "build stock, same family: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L60."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build sarc"
    metric: achieved_prefill_gemm_rate_tflop_per_s
    value: 10.293
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L16 row gpu=780m,scheme=4w,build=sarc,model=8b column rate"
    baseline: "build stock, same model: separate claim"
    notes: "Rate = sum of 2*M*N*K over sum of GPU time, logical FLOPs (TECHNICAL-REPORT.md#L78, #L444)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (224 dispatches of q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half), build stock"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 6963.215
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L116 row gpu=780m,model=8b,scheme=4w,build=stock,family=prefill GEMM (linear layers) column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L66."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build stock"
    metric: achieved_prefill_gemm_rate_tflop_per_s
    value: 4.105
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L19 row gpu=780m,scheme=4w,build=stock,model=8b column rate"
    notes: "Baseline measurement. Rate = sum of 2*M*N*K over sum of GPU time, logical FLOPs (TECHNICAL-REPORT.md#L78, #L444)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, one warm prefill dispatch, M=2048, N=2048, K=2048, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 1.6328
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L2 row gpu=780m,model=1b,scheme=4w,build=sarc,M=2048,N=2048,K=2048 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L114"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, one warm prefill dispatch, M=2048, N=512, K=2048, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 0.4501
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L3 row gpu=780m,model=1b,scheme=4w,build=sarc,M=2048,N=512,K=2048 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L115"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, one warm prefill dispatch, M=2048, N=8192, K=2048, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 6.3596
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L6 row gpu=780m,model=1b,scheme=4w,build=sarc,M=2048,N=8192,K=2048 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L118"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 1B 4w, one warm prefill dispatch, M=2048, N=2048, K=8192, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 6.522
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L8 row gpu=780m,model=1b,scheme=4w,build=sarc,M=2048,N=2048,K=8192 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L120"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, one warm prefill dispatch, M=2048, N=3072, K=3072, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 3.5702
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L450 row gpu=780m,model=3b,scheme=4w,build=sarc,M=2048,N=3072,K=3072 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L646"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, one warm prefill dispatch, M=2048, N=1024, K=3072, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 1.2627
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L451 row gpu=780m,model=3b,scheme=4w,build=sarc,M=2048,N=1024,K=3072 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L647"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, one warm prefill dispatch, M=2048, N=8192, K=3072, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 9.5236
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L454 row gpu=780m,model=3b,scheme=4w,build=sarc,M=2048,N=8192,K=3072 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L650"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.2 3B 4w, one warm prefill dispatch, M=2048, N=3072, K=8192, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 9.5858
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L456 row gpu=780m,model=3b,scheme=4w,build=sarc,M=2048,N=3072,K=8192 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L652"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, one warm prefill dispatch, M=2048, N=4096, K=4096, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 6.8051
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1234 row gpu=780m,model=8b,scheme=4w,build=sarc,M=2048,N=4096,K=4096 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1458"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, one warm prefill dispatch, M=2048, N=1024, K=4096, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 1.8567
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1235 row gpu=780m,model=8b,scheme=4w,build=sarc,M=2048,N=1024,K=4096 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1459"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, one warm prefill dispatch, M=2048, N=14336, K=4096, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 23.2404
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1238 row gpu=780m,model=8b,scheme=4w,build=sarc,M=2048,N=14336,K=4096 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1462"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 activations, 4-bit group-symmetric weights (4w)"
    shape: "Llama 3.1 8B 4w, one warm prefill dispatch, M=2048, N=4096, K=14336, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 23.676
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1240 row gpu=780m,model=8b,scheme=4w,build=sarc,M=2048,N=4096,K=14336 column ms (first row of this shape)"
    baseline: "build stock, kernel q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1464"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
---

# 4w linear cooperative-matrix kernel on the Radeon 780M

Scope: one device (AMD Radeon 780M), one driver version (RADV Mesa 25.2.7), measured on 2026-09-27 (kernel microbenchmark, correctness, first end-to-end runs) and 2026-09-28 (end-to-end campaign and its traces). Nothing on this page is established for any other device, driver version or date. All evidence files are in the public repository https://github.com/sarc-acl/executorch at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`; paths below are relative to that repository's root.

Citation form: `[<source page id>: <path>#L<line>]` points at a line of a raw file listed in that source page's `raw_data`. `[code: <path>#L<line>]` points at shader or selection source in the same repository and commit that no measurement source page excerpts; such statements describe what the code says, not something measured.

## What the kernel computes

- The operator is the "4w" quantized linear layer: 4-bit group-quantized weights with fp16 activations [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L50]. The SARC family for this scheme is `sarc_linear_q4gsw_coopmat`, activation layout fp16 [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L10].
- The shader's own header calls it the "SARC fp16 q4gsw (4-bit group-symmetric weight) cooperative-matrix linear" [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.glsl#L10] and gives its loop structure as a prologue that prefetches chunk 0, then per iteration "barrier -> prefetch(next) -> MMA(cur) -> store(next)" [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.glsl#L18-L19].
- It is used for the prefill linear layers. In the end-to-end campaign every prefill linear of the three Llama models uses texture3d activations [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L350], and the SARC build issues 112, 196 and 224 linear dispatches per prefill for 1B, 3B and 8B [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L353; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L4, #L32, #L60].

## Shipped variant for the 780M

Kernel base name: `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L37]. Built variants: `..._texture3d_texture2d_half`, `..._buffer_texture2d_half`, `..._buffer_buffer_half` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.yaml#L43, #L48, #L52], matching the row's storage mask `kTex3dTex2d | kBufTex2d | kBufBuf` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L39].

Names follow `<family>[_sweep]_<tile>_<io>_<weight>_half` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L91]. The tile token `t128x128k32g42s32f32c` decodes as follows:

| Token part | Parameter | Meaning (as documented) | Citation |
|---|---|---|---|
| `t128x128` | `WG_TILE_M` x `WG_TILE_N` | output tile per workgroup | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L99, #L24] |
| `k32` | `WG_TILE_K` | K consumed per main-loop iteration | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L100, #L25] |
| `g42` | `SG_GRID_X`, `SG_GRID_Y` | subgroup grid in the workgroup, X along N, Y along M; workgroup size = X·Y·`SUBGROUP_SIZE` | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L101, #L26] |
| `s32` | `SUBGROUP_SIZE` | must equal the device's subgroup size, or lie within its supported range when subgroup-size control is available | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L102, #L79-L80] |
| `f32` | `ACC_FP32` | the selection table describes the 780M tile as "with fp32 accumulate" | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L103; backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L26] |
| `c` | `CSH_IN_ASH` | texture3d output drain staged in the dead A shared-memory region; "less LDS, higher occupancy" on the 780M | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L104, #L43] |

- The selection table carries the same geometry as `TileDims k780mDims = {128, 128, 32, 4, 2, 32, 16, true}` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L27], described there as "t128x128k32g42s32 with fp32 accumulate and the drain staged in Ash" [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L26]. The positional fields are `m, n, k, sg_grid_x, sg_grid_y, subgroup_size, mma_m, csh_in_ash` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h#L81-L88].
- Subgroup size: the device's default subgroup size is 64, its minimum is 32, and subgroup-size control is available [meas-780m-vulkaninfo: sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, lines 1232, 1340, 687] (device-properties export dated `2026-9-1` in the file [meas-780m-vulkaninfo: sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, line 11220]); the microbenchmark reports `subgroup_size=64` and `max_shared_mem_bytes=65536` for the device [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.log#L5]. The code comment on the AMD device predicate says the shipped RDNA cooperative-matrix variants force subgroup size 32 per pipeline [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L19-L21].
- Why fp32 accumulation: the campaign's technical report states "SARC 4w uses fp32 accumulation because RDNA3 WMMA with an fp16 accumulator is slower" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L311]. This is the source's explanation; this wiki has no measurement page for the underlying roofline study.
- Provenance: the shader is "byte-identical to the 1.4 one, split into a body and a wrapper", with a `buffer_buffer` variant added [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L25-L26].

### Shader excerpts

Accumulator element type selected by `ACC_FP32`. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat.glsl#L119-L123` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
#ifdef ACC_FP32
#define ACC_T float
#else
#define ACC_T float16_t
#endif
```

Tile-derived constants. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L21-L27` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
const uint NUM_SUBGROUPS = SG_GRID_X * SG_GRID_Y;
const uint WG_SIZE = NUM_SUBGROUPS * SUBGROUP_SIZE;

const uint SG_TILE_M = WG_TILE_M / SG_GRID_Y;
const uint SG_TILE_N = WG_TILE_N / SG_GRID_X;
const uint MMAS_PER_SG_M = SG_TILE_M / MMA_M;
const uint MMAS_PER_SG_N = SG_TILE_N / MMA_N;
```

Accumulator matrices, one array per invocation, subgroup scope. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L186-L188` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
// FP16 accumulator coopmats (MMAS_PER_SG_M x MMAS_PER_SG_N per thread).
coopmat<ACC_T, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator>
    result[MMAS_PER_SG_M][MMAS_PER_SG_N];
```

The multiply-accumulate in the main loop. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_q4gsw_coopmat_body.glslh#L560-L562` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
        [[unroll]] for (uint i = 0; i < MMAS_PER_SG_M; ++i) {
          result[i][j] = coopMatMulAdd(matA[i], matB, result[i][j]);
        }
```

These fragments are verbatim and depend on the surrounding file (the constants `MMA_M`, `WG_TILE_M` and so on are template parameters filled from the yaml); they are not a standalone shader.

## How it is selected

- Selection is table-driven: a row is `{device substring, device predicate, op, kernel base name, tile dims, storage-combination mask, shape predicate, status, rowmajor_a}` and rows are tried in order [meas-780m-4w-bootstrap: sarc/README.md#L19]. In the campaign's sarc build: "Kernel choice is by device name, from verified rows only" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L259].
- The 780M 4w row: device substring `"780m"`, predicate `amd_wave64`, op `Op::kQ4gswLinear`, status `Status::kVerified` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L34-L41]. `amd_wave64` is `d.is_amd && d.subgroup_size == 64` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L22-L24].
- `kUnverified` rows are inert in a release; a dev build enables them with `ET_VK_SARC_UNVERIFIED=1` [meas-780m-4w-bootstrap: sarc/README.md#L20]. The 2026-09-27 dev-build runs were made with that variable set [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/env.txt#L4]; the release export and the 2026-09-28 campaign ran the row as verified, with no such variable [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L74; meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L260].
- The shader has no shape checks; `sarc::select()` enforces the preconditions when it matches a row [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L74]: `M % WG_TILE_M == 0`, `N % WG_TILE_N == 0`, `K % WG_TILE_K == 0`; `group_size % WG_TILE_K == 0`; no bias, batch 1, not a single-token (gemv) call; storage combination allowed by the row; `SUBGROUP_SIZE` equal to the device's subgroup size or inside its supported range when subgroup-size control is available; shared memory within the device limit [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L75-L81].
- For shapes no row covers (decode, unaligned M, bias, fp32) the op falls back to release 1.5's own `linear_q4gsw_{tiled,coop}` kernels [meas-780m-4w-bootstrap: sarc/README.md#L23]. The campaign's check prompt is such a case: "At 1972 tokens, M is not a multiple of any tile" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L322].
- `ET_VK_FORCE_TILED_LINEAR=1` sends the SARC linears to release 1.5's tiled/coop kernels and is the "tiled" baseline of the 2026-09-27 runs [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L154].

## Correctness evidence

Kernel level, 2026-09-27, dev build:

- All 24 microbenchmark prefill cases dispatched this kernel, 12 on the buffer variant and 12 on the texture3d variant [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out#L2; openspec/changes/sarc-1.5-bootstrap/proposal.md#L56-L57].
- The change's own statement: "All 4w numeric checks pass, including the rank-3 cases" [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L62]. The two rank-3 batch-1 4w cases dispatched the buffer variant with `correctness=PASSED` [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/correctness.log#L271-L272].
- The correctness binary's final line reads FAILED [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/correctness.log#L275]; the proposal attributes the non-zero exit only to 8da4w rank-3 cases falling back to tiled, 8da4w not being ported in that change [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L63-L64].
- Production-diff (sampled reference, M=2048) passed for all six model and storage combinations, "(6/6)" [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L65], each log ending `ALL PASSED`: `pdiff-llama-3.2-1b-4w-buffer.log#L43`, `pdiff-llama-3.2-1b-4w-texture3d.log#L43`, `pdiff-llama-3.2-3b-4w-buffer.log#L43`, `pdiff-llama-3.2-3b-4w-texture3d.log#L43`, `pdiff-llama-3.1-8b-4w-buffer.log#L43`, `pdiff-llama-3.1-8b-4w-texture3d.log#L43` under `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/`. Example, 1B wq_wo texture3d: 8161 of 4194304 elements checked, max abs diff 0.0195694 (tol 0.5), max rel diff 0.0119457 (tol 0.05) [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-1b-4w-texture3d.log#L10-L11].
- The SPIR-V verified on the device in the dev build is byte-identical to the release export [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L84].

Model level:

- 2026-09-27, 1B: default and tiled outputs are the SAME on the check prompt and on the unaligned prompt [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out#L5-L6]. The logs do not record which linear kernels ran in those two runs.
- 2026-09-28 campaign: the next token of the sarc and stock builds is SAME for all three 4w cells [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/tables.md#L8-L10]. That check uses a 1972-token prompt, where "M is not a multiple of any tile" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L321-L322], so by the fallback rule above it does not exercise this kernel's GEMM path.
- 2026-09-28 logits probe on the tile-aligned 2048-token real-text prompt: top-1 token identical between stock and sarc for 1B, 3B and 8B 4w [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv#L2, #L6, #L10]; also identical on the 1972-token check prompt [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv#L3, #L7, #L11]. The probe's `bitwise_identical_top10` column is False on these rows, i.e. logits differ numerically while the top-1 token agrees.

Not verified, as stated by the source:

- The `buffer_buffer` variant (buffer-stored weights) "has not run on the device" [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L87-L88].
- Clocks were not pinned [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L89; meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L422].

## Measured results

Four kinds of numbers are kept apart: (1) kernel microbenchmark, (2) end to end on 2026-09-27 before any SARC attention kernel existed on release 1.5, (3) end to end in the 2026-09-28 campaign, where the sarc build also runs SARC attention kernels, (4) warm-trace GPU time of the 2026-09-28 campaign. No ratio on this page is computed by the wiki; ratios are quoted only where an evidence file states them.

### 1. Kernel microbenchmark, 2026-09-27

`test_llama_microbench`, 3 warmup + 5 timed runs per case, linear group_size 128 [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json#L7-L9]. Value: `kernel_median_us` (microseconds). SARC column: dev build with `ET_VK_SARC_UNVERIFIED=1`, kernel `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_<io>_texture2d_half`. Baseline column: a stock release 1.5 build, which dispatched the upstream `q4gsw_linear_gemm__tin__w_4x8_nc_<io>_half` kernels [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out#L20]. Every row cites [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json] and [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json] at the line given.

| Case | M | K | N | IO storage | SARC kernel_median_us | stock 1.5 kernel_median_us | Line (same in both files) |
|---|---|---|---|---|---|---|---|
| Llama 3.1 8B wq_wo | 2048 | 4096 | 4096 | texture3d | 6481 | 16314.4 | `linear-4w.json#L11` (cases[0]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.1 8B wq_wo | 2048 | 4096 | 4096 | buffer | 6481.4 | 16320.7 | `linear-4w.json#L12` (cases[1]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.1 8B wk_wv | 2048 | 4096 | 1024 | texture3d | 1716.96 | 4089.84 | `linear-4w.json#L13` (cases[2]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.1 8B wk_wv | 2048 | 4096 | 1024 | buffer | 1732.96 | 4083.16 | `linear-4w.json#L14` (cases[3]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.1 8B w1_w3 | 2048 | 4096 | 14336 | texture3d | 22023.1 | 57203.9 | `linear-4w.json#L15` (cases[4]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.1 8B w1_w3 | 2048 | 4096 | 14336 | buffer | 22060.3 | 57293.3 | `linear-4w.json#L16` (cases[5]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.1 8B w2 | 2048 | 14336 | 4096 | texture3d | 22098.7 | 57492.9 | `linear-4w.json#L17` (cases[6]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.1 8B w2 | 2048 | 14336 | 4096 | buffer | 22312.4 | 57557.6 | `linear-4w.json#L18` (cases[7]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 3B wq_wo | 2048 | 3072 | 3072 | texture3d | 3582.48 | 9143.62 | `linear-4w.json#L19` (cases[8]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 3B wq_wo | 2048 | 3072 | 3072 | buffer | 3545.96 | 9160.06 | `linear-4w.json#L20` (cases[9]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 3B wk_wv | 2048 | 3072 | 1024 | texture3d | 1256.44 | 3073.8 | `linear-4w.json#L21` (cases[10]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 3B wk_wv | 2048 | 3072 | 1024 | buffer | 1276.52 | 3074.28 | `linear-4w.json#L22` (cases[11]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 3B w1_w3 | 2048 | 3072 | 8192 | texture3d | 9404.12 | 24486.5 | `linear-4w.json#L23` (cases[12]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 3B w1_w3 | 2048 | 3072 | 8192 | buffer | 9389.78 | 24522.6 | `linear-4w.json#L24` (cases[13]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 3B w2 | 2048 | 8192 | 3072 | texture3d | 9488.56 | 24595.6 | `linear-4w.json#L25` (cases[14]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 3B w2 | 2048 | 8192 | 3072 | buffer | 9597.64 | 24609.1 | `linear-4w.json#L26` (cases[15]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 1B wq_wo | 2048 | 2048 | 2048 | texture3d | 1607.96 | 4094.84 | `linear-4w.json#L27` (cases[16]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 1B wq_wo | 2048 | 2048 | 2048 | buffer | 1598.5 | 4090.64 | `linear-4w.json#L28` (cases[17]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 1B wk_wv | 2048 | 2048 | 512 | texture3d | 438.52 | 1065.8 | `linear-4w.json#L29` (cases[18]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 1B wk_wv | 2048 | 2048 | 512 | buffer | 443.84 | 1062.44 | `linear-4w.json#L30` (cases[19]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 1B w1_w3 | 2048 | 2048 | 8192 | texture3d | 6297.8 | 16309.5 | `linear-4w.json#L31` (cases[20]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 1B w1_w3 | 2048 | 2048 | 8192 | buffer | 6246.16 | 16300.6 | `linear-4w.json#L32` (cases[21]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 1B w2 | 2048 | 8192 | 2048 | texture3d | 6479.96 | 16523.3 | `linear-4w.json#L33` (cases[22]) in `results/780m/sarc/` and `results/780m/stock/` |
| Llama 3.2 1B w2 | 2048 | 8192 | 2048 | buffer | 6538.68 | 16547.7 | `linear-4w.json#L34` (cases[23]) in `results/780m/sarc/` and `results/780m/stock/` |

The stock JSON also records `op_mean_us`, which is larger than its kernel time (for example `op_mean_us` 17265 against `kernel_mean_us` 16310.4 on the 8B wq_wo texture3d case [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json#L11]). The microbenchmark files do not say what the difference consists of. Separately, the campaign report says stock 4w issues "a separate input-transpose dispatch per linear op" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L128-L129].

### 2. End to end, 2026-09-27 (no SARC attention kernels in any build)

Whole-model 2048-token prefill, tok/s from `llama_main`'s PyTorchObserver line, one run per entry.

| Model | Build / mode | prefill tok/s | Citation |
|---|---|---|---|
| Llama 3.2 1B | SARC dev build (ET_VK_SARC_UNVERIFIED=1), default mode | 1915.81 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-default.log#L6] |
| Llama 3.2 1B | SARC dev build, ET_VK_FORCE_TILED_LINEAR (tiled) | 714.336 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-tiled.log#L6] |
| Llama 3.2 1B | stock release 1.5 build | 1204.71 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-1b-4w-default.log#L5] |
| Llama 3.2 1B | SARC release export (row verified, no env) | 1930.25 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-1b-4w-default.log#L5] |
| Llama 3.2 3B | SARC dev build (ET_VK_SARC_UNVERIFIED=1), default mode | 683.35 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-default.log#L6] |
| Llama 3.2 3B | SARC dev build, ET_VK_FORCE_TILED_LINEAR (tiled) | 246.065 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-tiled.log#L6] |
| Llama 3.2 3B | stock release 1.5 build | 421.486 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-3b-4w-default.log#L5] |
| Llama 3.2 3B | SARC release export (row verified, no env) | 689.795 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-3b-4w-default.log#L5] |
| Llama 3.1 8B | SARC dev build (ET_VK_SARC_UNVERIFIED=1), default mode | 351.951 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-default.log#L6] |
| Llama 3.1 8B | SARC dev build, ET_VK_FORCE_TILED_LINEAR (tiled) | 104.357 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-tiled.log#L6] |
| Llama 3.1 8B | stock release 1.5 build | 193.829 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-8b-4w-default.log#L5] |
| Llama 3.1 8B | SARC release export (row verified, no env) | 352.193 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-8b-4w-default.log#L5] |

The proposal states the SARC vs stock 1.5 ratio as 1.60× / 1.64× / 1.81× for 1B / 3B / 8B [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L75]. The same change notes that the 1.4 branch had reached a higher 1B figure and names the not-yet-ported SDPA cooperative-matrix kernels as the most likely cause, "Not yet confirmed" at that point [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L92-L97]; see `kernel-sdpa-prefill-780m`.

### 3. End to end, 2026-09-28 campaign (sarc build includes SARC attention kernels)

Median of 5 timed runs per build, `prompt_2048.txt`, builds stock (upstream release/1.5 @ `985c1ceccc`) and sarc (tag `sarc/1.5-r2`) [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L247, #L256, #L291]. "The 780M numbers include attention": the sarc build's speedup includes the coopmat QK^T/AV kernels and the truncated softmax [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L115-L116].

| Model | stock median tok/s | sarc median tok/s | speedup (ratio of medians, from the file) | Citation |
|---|---|---|---|---|
| Llama 3.2 1B | 1211.83 (min 1210.4, max 1216.15) | 2698.29 (min 2698.29, max 2701.85) | 2.2266241964632005 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L2] |
| Llama 3.2 3B | 425.073 (min 424.192, max 426.223) | 1151.21 (min 1150.56, max 1151.21) | 2.7082642275562083 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L3] |
| Llama 3.1 8B | 198.008 (min 197.932, max 198.277) | 525.802 (min 524.59, max 526.208) | 2.655458365318573 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L4] |

### 4. Warm-trace GPU time and rate of the prefill GEMM family, 2026-09-28 campaign

One warm ETDump trace per cell and build, no repeat [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L76, #L445]. Rate is the achieved prefill-GEMM rate, sum of 2·M·N·K over sum of GPU time, in TFLOP/s, logical FLOPs [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L78, #L444].

| Model | sarc GEMM ms | sarc dispatches | sarc rate | stock GEMM ms | stock dispatches | stock rate | Citation |
|---|---|---|---|---|---|---|---|
| Llama 3.2 1B | 373.745 | 112 | 10.664 | 927.709 | 112 | 4.296 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L2; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L4; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L14; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L14; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L10; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L17] |
| Llama 3.2 3B | 1075.918 | 196 | 10.73 | 2715.137 | 196 | 4.252 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L53; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L32; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L15; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L65; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L38; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L18] |
| Llama 3.1 8B | 2777.342 | 224 | 10.293 | 6963.215 | 224 | 4.105 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L104; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L60; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L16; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L116; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L66; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L19] |

The source's own kernel-level ratio for these traces ("GEMM x", stock over sarc) is 2.48 / 2.52 / 2.51 for 1B / 3B / 8B [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/modelsize.txt#L5-L7].

Single warm dispatches, first row of each distinct shape in `gemm.csv` (rate column in TFLOP/s as defined in [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/roofline.md#L161]):

| Model | M | N | K | sarc ms | sarc rate | stock ms | stock rate | Citation |
|---|---|---|---|---|---|---|---|---|
| Llama 3.2 1B | 2048 | 2048 | 2048 | 1.6328 | 10.522 | 3.9577 | 4.341 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L2 (sarc), #L114 (stock)] |
| Llama 3.2 1B | 2048 | 512 | 2048 | 0.4501 | 9.542 | 1.0565 | 4.065 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L3 (sarc), #L115 (stock)] |
| Llama 3.2 1B | 2048 | 8192 | 2048 | 6.3596 | 10.806 | 15.8182 | 4.344 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L6 (sarc), #L118 (stock)] |
| Llama 3.2 1B | 2048 | 2048 | 8192 | 6.522 | 10.537 | 16.1803 | 4.247 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L8 (sarc), #L120 (stock)] |
| Llama 3.2 3B | 2048 | 3072 | 3072 | 3.5702 | 10.827 | 8.8844 | 4.351 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L450 (sarc), #L646 (stock)] |
| Llama 3.2 3B | 2048 | 1024 | 3072 | 1.2627 | 10.204 | 3.039 | 4.24 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L451 (sarc), #L647 (stock)] |
| Llama 3.2 3B | 2048 | 8192 | 3072 | 9.5236 | 10.824 | 24.084 | 4.28 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L454 (sarc), #L650 (stock)] |
| Llama 3.2 3B | 2048 | 3072 | 8192 | 9.5858 | 10.753 | 24.5308 | 4.202 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L456 (sarc), #L652 (stock)] |
| Llama 3.1 8B | 2048 | 4096 | 4096 | 6.8051 | 10.098 | 16.8836 | 4.07 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1234 (sarc), #L1458 (stock)] |
| Llama 3.1 8B | 2048 | 1024 | 4096 | 1.8567 | 9.253 | 4.3651 | 3.936 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1235 (sarc), #L1459 (stock)] |
| Llama 3.1 8B | 2048 | 14336 | 4096 | 23.2404 | 10.349 | 57.848 | 4.158 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1238 (sarc), #L1462 (stock)] |
| Llama 3.1 8B | 2048 | 4096 | 14336 | 23.676 | 10.159 | 58.4082 | 4.118 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1240 (sarc), #L1464 (stock)] |

The stock kernel in these rows is `q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half`, described by the report as fp16 FMA with fp16 accumulation and no cooperative matrix [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L128, #L132].

## Limits of this page

- One device, one driver version, two days. No statement here is tested on another driver version.
- The end-to-end numbers of section 3 cannot be attributed to this kernel alone.
- The traces of section 4 carry no timestamp of their own; their date and driver rest on the campaign report describing them as part of the campaign.
- Comparisons against the release-1.4 branch quoted by the evidence rest on reference data outside the cited files and are not reproduced here beyond the quoted proposal lines.
