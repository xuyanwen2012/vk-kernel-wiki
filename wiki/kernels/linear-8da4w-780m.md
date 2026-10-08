---
id: kernel-linear-8da4w-780m
title: "8da4w linear (dynamic int8 activations, 4-bit weights) cooperative-matrix kernel on the Radeon 780M: sarc_linear_dq8ca_coopmat_zpg t128x64k32g42s32"
type: kernel
architectures: [radeon-780m]
tags: [linear-8da4w, linear-8da4w-zpg, gemm, prefill, tiled-linear, quantize-and-pack, cooperative-matrix, int8-arithmetic, subgroup-size, subgroup-size-control, wave64, storage-texture3d, storage-buffer, storage-texture2d, workgroup-tile-sizing, k-chunk-sizing, subgroup-grid, required-subgroup-size, full-a-map, zero-point-hoisting, double-buffering, fp32-accumulation]
confidence: verified
reproducibility: snippet
kernel_types: [linear-8da4w, linear-8da4w-zpg, gemm, prefill]
languages: [glsl]
aliases: ["sarc_linear_dq8ca_coopmat_zpg", "t128x64k32g42s32", "dq8ca coopmat 780M", "8da4w linear 780M", "zpg"]
related: [hw-radeon-780m, hw-cooperative-matrix-rdna3, kernel-linear-4w-780m, kernel-sdpa-prefill-780m, technique-workgroup-tile-sizing, pattern-unaligned-m-fallback]
sources: [meas-780m-8da4w-port, meas-780m-sdpa-port, meas-780m-e2e-prefill, meas-780m-4w-bootstrap, meas-780m-vulkaninfo]
version_sensitive: vs-radv-coopmat-lowering-after-25-2-7
evidence_basis:
  - evidence_type: measurement
    source_id: meas-780m-8da4w-port
    locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, lines 11-34 and openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, lines 11-34 (kernel-level microbench, SARC kernel and release 1.5 tiled kernel); openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log, lines 7-51 and the five other pdiff2 files, line 51 (production-diff, shipped kernel names); openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 1-25; openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 34-60; backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 42-53; sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 3-5 and 10-14 (driver version attributed from the install history, not recorded by the run)"
  - evidence_type: measurement
    source_id: meas-780m-sdpa-port
    locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 5, 11-15, 18-19, 22-23, 25-30 (shipped kernel names dispatched, end-to-end prefill with the SDPA rows, production-diff 6 x ALL PASSED)"
  - evidence_type: measurement
    source_id: meas-780m-e2e-prefill
    locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L17-L19; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L18, #L46, #L74; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv rows gpu=780m,scheme=8da4w; openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv#L4-L5, #L8-L9, #L12-L13"
  - evidence_type: measurement
    source_id: meas-780m-4w-bootstrap
    locator: "sarc/SWEEP-PARAMETERS.md#L127 (shipped 8da4w variant for the Radeon 780M); sarc/SWEEP-PARAMETERS.md#L74-L81, #L99-L102"
  - evidence_type: measurement
    source_id: meas-780m-vulkaninfo
    locator: "sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, lines 687, 1232, 1340"
performance_claims:
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), build sarc (tag sarc/1.5-r2)"
    metric: prefill_tokens_per_second_median_of_5
    value: 2544.1
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L17 row gpu=780m,model=1b,scheme=8da4w column sarc_median"
    baseline: "build stock (upstream ExecuTorch release/1.5), same cell: column stock_median of the same row (separate claim)"
    notes: "End to end. The sarc build also dispatches the SARC SDPA kernels on this device (REPORT.md#L115-L116), so the value is not attributable to the 8da4w linear kernel alone. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), build stock (upstream release/1.5)"
    metric: prefill_tokens_per_second_median_of_5
    value: 1635.78
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L17 row gpu=780m,model=1b,scheme=8da4w column stock_median"
    notes: "Baseline measurement. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc over stock"
    metric: end_to_end_speedup_ratio_of_medians_as_stated_by_source
    value: 1.5552824952010662
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L17 row gpu=780m,model=1b,scheme=8da4w column speedup"
    baseline: "build stock (upstream ExecuTorch release/1.5)"
    notes: "Ratio computed by the campaign's analyze.py (ratio of the medians, REPORT.md#L332), copied, not recomputed here. Includes the SARC SDPA kernels."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), build sarc (tag sarc/1.5-r2)"
    metric: prefill_tokens_per_second_median_of_5
    value: 1051.33
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L18 row gpu=780m,model=3b,scheme=8da4w column sarc_median"
    baseline: "build stock (upstream ExecuTorch release/1.5), same cell: column stock_median of the same row (separate claim)"
    notes: "End to end. The sarc build also dispatches the SARC SDPA kernels on this device (REPORT.md#L115-L116), so the value is not attributable to the 8da4w linear kernel alone. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), build stock (upstream release/1.5)"
    metric: prefill_tokens_per_second_median_of_5
    value: 564.654
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L18 row gpu=780m,model=3b,scheme=8da4w column stock_median"
    notes: "Baseline measurement. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc over stock"
    metric: end_to_end_speedup_ratio_of_medians_as_stated_by_source
    value: 1.8619012705125615
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L18 row gpu=780m,model=3b,scheme=8da4w column speedup"
    baseline: "build stock (upstream ExecuTorch release/1.5)"
    notes: "Ratio computed by the campaign's analyze.py (ratio of the medians, REPORT.md#L332), copied, not recomputed here. Includes the SARC SDPA kernels."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), build sarc (tag sarc/1.5-r2)"
    metric: prefill_tokens_per_second_median_of_5
    value: 489.133
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L19 row gpu=780m,model=8b,scheme=8da4w column sarc_median"
    baseline: "build stock (upstream ExecuTorch release/1.5), same cell: column stock_median of the same row (separate claim)"
    notes: "End to end. The sarc build also dispatches the SARC SDPA kernels on this device (REPORT.md#L115-L116), so the value is not attributable to the 8da4w linear kernel alone. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), build stock (upstream release/1.5)"
    metric: prefill_tokens_per_second_median_of_5
    value: 282.055
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L19 row gpu=780m,model=8b,scheme=8da4w column stock_median"
    notes: "Baseline measurement. Campaign e2e-1.5-2026-09-28, 5 fresh llama_main runs per build with --warmup, prompt_2048.txt, clocks not pinned (REPORT.md#L291, #L422)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc over stock"
    metric: end_to_end_speedup_ratio_of_medians_as_stated_by_source
    value: 1.7341759585896366
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L19 row gpu=780m,model=8b,scheme=8da4w column speedup"
    baseline: "build stock (upstream ExecuTorch release/1.5)"
    notes: "Ratio computed by the campaign's analyze.py (ratio of the medians, REPORT.md#L332), copied, not recomputed here. Includes the SARC SDPA kernels."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (112 dispatches of sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half), build sarc"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 400.402
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L27 row gpu=780m,model=1b,scheme=8da4w,build=sarc,family=prefill GEMM (linear layers) column ms"
    baseline: "build stock, same family: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L18. Excludes the activation-quantize dispatches."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build sarc"
    metric: achieved_prefill_gemm_rate_top_per_s
    value: 9.954
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L20 row gpu=780m,scheme=8da4w,build=sarc,model=1b column rate"
    baseline: "build stock, same model: separate claim"
    notes: "Rate = sum of 2*M*N*K over sum of GPU time; integer ops (TOP/s), logical ops, dequant and zero-point work not counted (TECHNICAL-REPORT.md#L78, #L444; evidence/roofline.md#L161)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, all 8-bit activation-quantize dispatches of one warm 2048-token prefill trace, build sarc"
    metric: gpu_time_ms_activation_quantize_family_warm_trace
    value: 43.13
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L32 row gpu=780m,model=1b,scheme=8da4w,build=sarc,family=8-bit activation quantize column ms"
    notes: "Operator-level companion of the GEMM time: the quantize dispatch is part of the linear operator but not of this kernel (TECHNICAL-REPORT.md#L84-L88)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (112 dispatches of linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8), build stock"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 541.972
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L40 row gpu=780m,model=1b,scheme=8da4w,build=stock,family=prefill GEMM (linear layers) column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L25. Excludes the activation-quantize dispatches."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build stock"
    metric: achieved_prefill_gemm_rate_top_per_s
    value: 7.354
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L23 row gpu=780m,scheme=8da4w,build=stock,model=1b column rate"
    notes: "Baseline measurement. Rate = sum of 2*M*N*K over sum of GPU time; integer ops (TOP/s), logical ops, dequant and zero-point work not counted (TECHNICAL-REPORT.md#L78, #L444; evidence/roofline.md#L161)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, all 8-bit activation-quantize dispatches of one warm 2048-token prefill trace, build stock"
    metric: gpu_time_ms_activation_quantize_family_warm_trace
    value: 43.231
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L45 row gpu=780m,model=1b,scheme=8da4w,build=stock,family=8-bit activation quantize column ms"
    notes: "Baseline measurement. Operator-level companion of the GEMM time: the quantize dispatch is part of the linear operator but not of this kernel (TECHNICAL-REPORT.md#L84-L88)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (196 dispatches of sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half), build sarc"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 1181.007
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L78 row gpu=780m,model=3b,scheme=8da4w,build=sarc,family=prefill GEMM (linear layers) column ms"
    baseline: "build stock, same family: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L46. Excludes the activation-quantize dispatches."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build sarc"
    metric: achieved_prefill_gemm_rate_top_per_s
    value: 9.775
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L21 row gpu=780m,scheme=8da4w,build=sarc,model=3b column rate"
    baseline: "build stock, same model: separate claim"
    notes: "Rate = sum of 2*M*N*K over sum of GPU time; integer ops (TOP/s), logical ops, dequant and zero-point work not counted (TECHNICAL-REPORT.md#L78, #L444; evidence/roofline.md#L161)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, all 8-bit activation-quantize dispatches of one warm 2048-token prefill trace, build sarc"
    metric: gpu_time_ms_activation_quantize_family_warm_trace
    value: 101.421
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L82 row gpu=780m,model=3b,scheme=8da4w,build=sarc,family=8-bit activation quantize column ms"
    notes: "Operator-level companion of the GEMM time: the quantize dispatch is part of the linear operator but not of this kernel (TECHNICAL-REPORT.md#L84-L88)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (196 dispatches of linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8), build stock"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 1621.24
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L91 row gpu=780m,model=3b,scheme=8da4w,build=stock,family=prefill GEMM (linear layers) column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L53. Excludes the activation-quantize dispatches."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build stock"
    metric: achieved_prefill_gemm_rate_top_per_s
    value: 7.121
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L24 row gpu=780m,scheme=8da4w,build=stock,model=3b column rate"
    notes: "Baseline measurement. Rate = sum of 2*M*N*K over sum of GPU time; integer ops (TOP/s), logical ops, dequant and zero-point work not counted (TECHNICAL-REPORT.md#L78, #L444; evidence/roofline.md#L161)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, all 8-bit activation-quantize dispatches of one warm 2048-token prefill trace, build stock"
    metric: gpu_time_ms_activation_quantize_family_warm_trace
    value: 100.699
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L96 row gpu=780m,model=3b,scheme=8da4w,build=stock,family=8-bit activation quantize column ms"
    notes: "Baseline measurement. Operator-level companion of the GEMM time: the quantize dispatch is part of the linear operator but not of this kernel (TECHNICAL-REPORT.md#L84-L88)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (224 dispatches of sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half), build sarc"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 2965.232
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L129 row gpu=780m,model=8b,scheme=8da4w,build=sarc,family=prefill GEMM (linear layers) column ms"
    baseline: "build stock, same family: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L74. Excludes the activation-quantize dispatches."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build sarc"
    metric: achieved_prefill_gemm_rate_top_per_s
    value: 9.641
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L22 row gpu=780m,scheme=8da4w,build=sarc,model=8b column rate"
    baseline: "build stock, same model: separate claim"
    notes: "Rate = sum of 2*M*N*K over sum of GPU time; integer ops (TOP/s), logical ops, dequant and zero-point work not counted (TECHNICAL-REPORT.md#L78, #L444; evidence/roofline.md#L161)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, all 8-bit activation-quantize dispatches of one warm 2048-token prefill trace, build sarc"
    metric: gpu_time_ms_activation_quantize_family_warm_trace
    value: 165.872
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L133 row gpu=780m,model=8b,scheme=8da4w,build=sarc,family=8-bit activation quantize column ms"
    notes: "Operator-level companion of the GEMM time: the quantize dispatch is part of the linear operator but not of this kernel (TECHNICAL-REPORT.md#L84-L88)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace (224 dispatches of linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8), build stock"
    metric: gpu_time_ms_prefill_gemm_family_warm_trace
    value: 4142.245
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L142 row gpu=780m,model=8b,scheme=8da4w,build=stock,family=prefill GEMM (linear layers) column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L81. Excludes the activation-quantize dispatches."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, all prefill GEMM dispatches of one warm 2048-token prefill trace, build stock"
    metric: achieved_prefill_gemm_rate_top_per_s
    value: 6.901
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L25 row gpu=780m,scheme=8da4w,build=stock,model=8b column rate"
    notes: "Baseline measurement. Rate = sum of 2*M*N*K over sum of GPU time; integer ops (TOP/s), logical ops, dequant and zero-point work not counted (TECHNICAL-REPORT.md#L78, #L444; evidence/roofline.md#L161)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, all 8-bit activation-quantize dispatches of one warm 2048-token prefill trace, build stock"
    metric: gpu_time_ms_activation_quantize_family_warm_trace
    value: 167.005
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L147 row gpu=780m,model=8b,scheme=8da4w,build=stock,family=8-bit activation quantize column ms"
    notes: "Baseline measurement. Operator-level companion of the GEMM time: the quantize dispatch is part of the linear operator but not of this kernel (TECHNICAL-REPORT.md#L84-L88)."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, one warm prefill dispatch, M=2048, N=2048, K=2048, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 1.7644
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L226 row gpu=780m,model=1b,scheme=8da4w,build=sarc,M=2048,N=2048,K=2048 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L338 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, one warm prefill dispatch, M=2048, N=2048, K=2048, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 2.181
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L338 row gpu=780m,model=1b,scheme=8da4w,build=stock,M=2048,N=2048,K=2048 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, one warm prefill dispatch, M=2048, N=512, K=2048, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 0.4546
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L227 row gpu=780m,model=1b,scheme=8da4w,build=sarc,M=2048,N=512,K=2048 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L339 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, one warm prefill dispatch, M=2048, N=512, K=2048, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 0.5354
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L339 row gpu=780m,model=1b,scheme=8da4w,build=stock,M=2048,N=512,K=2048 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, one warm prefill dispatch, M=2048, N=8192, K=2048, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 6.8822
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L230 row gpu=780m,model=1b,scheme=8da4w,build=sarc,M=2048,N=8192,K=2048 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L342 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, one warm prefill dispatch, M=2048, N=8192, K=2048, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 9.3911
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L342 row gpu=780m,model=1b,scheme=8da4w,build=stock,M=2048,N=8192,K=2048 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, one warm prefill dispatch, M=2048, N=2048, K=8192, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 6.8637
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L232 row gpu=780m,model=1b,scheme=8da4w,build=sarc,M=2048,N=2048,K=8192 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L344 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, one warm prefill dispatch, M=2048, N=2048, K=8192, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 9.6655
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L344 row gpu=780m,model=1b,scheme=8da4w,build=stock,M=2048,N=2048,K=8192 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, one warm prefill dispatch, M=2048, N=3072, K=3072, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 4.1252
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L842 row gpu=780m,model=3b,scheme=8da4w,build=sarc,M=2048,N=3072,K=3072 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1038 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, one warm prefill dispatch, M=2048, N=3072, K=3072, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 6.1424
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1038 row gpu=780m,model=3b,scheme=8da4w,build=stock,M=2048,N=3072,K=3072 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, one warm prefill dispatch, M=2048, N=1024, K=3072, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 1.312
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L843 row gpu=780m,model=3b,scheme=8da4w,build=sarc,M=2048,N=1024,K=3072 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1039 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, one warm prefill dispatch, M=2048, N=1024, K=3072, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 1.5575
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1039 row gpu=780m,model=3b,scheme=8da4w,build=stock,M=2048,N=1024,K=3072 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, one warm prefill dispatch, M=2048, N=8192, K=3072, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 10.2005
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L846 row gpu=780m,model=3b,scheme=8da4w,build=sarc,M=2048,N=8192,K=3072 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1042 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, one warm prefill dispatch, M=2048, N=8192, K=3072, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 13.8799
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1042 row gpu=780m,model=3b,scheme=8da4w,build=stock,M=2048,N=8192,K=3072 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, one warm prefill dispatch, M=2048, N=3072, K=8192, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 10.593
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L848 row gpu=780m,model=3b,scheme=8da4w,build=sarc,M=2048,N=3072,K=8192 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1044 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, one warm prefill dispatch, M=2048, N=3072, K=8192, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 14.9735
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1044 row gpu=780m,model=3b,scheme=8da4w,build=stock,M=2048,N=3072,K=8192 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, one warm prefill dispatch, M=2048, N=4096, K=4096, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 7.2757
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1682 row gpu=780m,model=8b,scheme=8da4w,build=sarc,M=2048,N=4096,K=4096 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1906 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, one warm prefill dispatch, M=2048, N=4096, K=4096, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 10.4197
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1906 row gpu=780m,model=8b,scheme=8da4w,build=stock,M=2048,N=4096,K=4096 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, one warm prefill dispatch, M=2048, N=1024, K=4096, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 1.8994
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1683 row gpu=780m,model=8b,scheme=8da4w,build=sarc,M=2048,N=1024,K=4096 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1907 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, one warm prefill dispatch, M=2048, N=1024, K=4096, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 2.3424
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1907 row gpu=780m,model=8b,scheme=8da4w,build=stock,M=2048,N=1024,K=4096 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, one warm prefill dispatch, M=2048, N=14336, K=4096, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 24.8404
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1686 row gpu=780m,model=8b,scheme=8da4w,build=sarc,M=2048,N=14336,K=4096 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1910 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, one warm prefill dispatch, M=2048, N=14336, K=4096, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 35.9027
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1910 row gpu=780m,model=8b,scheme=8da4w,build=stock,M=2048,N=14336,K=4096 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, one warm prefill dispatch, M=2048, N=4096, K=14336, IO texture3d, weights texture2d"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 24.3698
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1688 row gpu=780m,model=8b,scheme=8da4w,build=sarc,M=2048,N=4096,K=14336 column ms (first row of this shape)"
    baseline: "build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, first row of the same shape: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1912 (separate claim)"
    notes: "One dispatch from one warm ETDump trace, no repeat; other dispatches of the same shape are further rows of gemm.csv."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, one warm prefill dispatch, M=2048, N=4096, K=14336, IO texture3d, weights texture2d, build stock, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: gpu_time_ms_single_dispatch_warm_trace
    value: 34.6389
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1912 row gpu=780m,model=8b,scheme=8da4w,build=stock,M=2048,N=4096,K=14336 column ms (first row of this shape)"
    notes: "Baseline measurement. One dispatch from one warm ETDump trace, no repeat."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill linear wq_wo, M=2048, K=2048, N=2048, IO texture3d, weights texture2d, sarc8 run, logged kernel name sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half (name before the rename)"
    metric: microbench_kernel_median_us
    value: 1748.84
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 27 field kernel_median_us"
    baseline: "stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, same case: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 27 (separate claim)"
    notes: "Linear shader only; 3 warmup + 5 timed runs. ET_VK_SARC_UNVERIFIED=1; binaries predate the kernel rename, commit not recorded. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill linear wq_wo, M=2048, K=2048, N=2048, IO texture3d, weights texture2d, stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: microbench_kernel_median_us
    value: 2238.06
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 27 field kernel_median_us"
    notes: "Baseline measurement: release 1.5's tiled dq8ca kernel from the same binaries as sarc8, without ET_VK_SARC_UNVERIFIED; not an upstream stock build. 3 warmup + 5 timed runs. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill linear wk_wv, M=2048, K=2048, N=512, IO texture3d, weights texture2d, sarc8 run, logged kernel name sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half (name before the rename)"
    metric: microbench_kernel_median_us
    value: 455.4
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 29 field kernel_median_us"
    baseline: "stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, same case: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 29 (separate claim)"
    notes: "Linear shader only; 3 warmup + 5 timed runs. ET_VK_SARC_UNVERIFIED=1; binaries predate the kernel rename, commit not recorded. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill linear wk_wv, M=2048, K=2048, N=512, IO texture3d, weights texture2d, stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: microbench_kernel_median_us
    value: 538.92
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 29 field kernel_median_us"
    notes: "Baseline measurement: release 1.5's tiled dq8ca kernel from the same binaries as sarc8, without ET_VK_SARC_UNVERIFIED; not an upstream stock build. 3 warmup + 5 timed runs. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill linear w1_w3, M=2048, K=2048, N=8192, IO texture3d, weights texture2d, sarc8 run, logged kernel name sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half (name before the rename)"
    metric: microbench_kernel_median_us
    value: 6886.1
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 31 field kernel_median_us"
    baseline: "stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, same case: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 31 (separate claim)"
    notes: "Linear shader only; 3 warmup + 5 timed runs. ET_VK_SARC_UNVERIFIED=1; binaries predate the kernel rename, commit not recorded. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill linear w1_w3, M=2048, K=2048, N=8192, IO texture3d, weights texture2d, stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: microbench_kernel_median_us
    value: 9509.38
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 31 field kernel_median_us"
    notes: "Baseline measurement: release 1.5's tiled dq8ca kernel from the same binaries as sarc8, without ET_VK_SARC_UNVERIFIED; not an upstream stock build. 3 warmup + 5 timed runs. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill linear w2, M=2048, K=8192, N=2048, IO texture3d, weights texture2d, sarc8 run, logged kernel name sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half (name before the rename)"
    metric: microbench_kernel_median_us
    value: 6871.94
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 33 field kernel_median_us"
    baseline: "stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, same case: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 33 (separate claim)"
    notes: "Linear shader only; 3 warmup + 5 timed runs. ET_VK_SARC_UNVERIFIED=1; binaries predate the kernel rename, commit not recorded. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill linear w2, M=2048, K=8192, N=2048, IO texture3d, weights texture2d, stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: microbench_kernel_median_us
    value: 9809.82
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 33 field kernel_median_us"
    notes: "Baseline measurement: release 1.5's tiled dq8ca kernel from the same binaries as sarc8, without ET_VK_SARC_UNVERIFIED; not an upstream stock build. 3 warmup + 5 timed runs. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill linear wq_wo, M=2048, K=4096, N=4096, IO texture3d, weights texture2d, sarc8 run, logged kernel name sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half (name before the rename)"
    metric: microbench_kernel_median_us
    value: 6798.32
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 11 field kernel_median_us"
    baseline: "stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, same case: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 11 (separate claim)"
    notes: "Linear shader only; 3 warmup + 5 timed runs. ET_VK_SARC_UNVERIFIED=1; binaries predate the kernel rename, commit not recorded. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill linear wq_wo, M=2048, K=4096, N=4096, IO texture3d, weights texture2d, stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: microbench_kernel_median_us
    value: 9631.9
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 11 field kernel_median_us"
    notes: "Baseline measurement: release 1.5's tiled dq8ca kernel from the same binaries as sarc8, without ET_VK_SARC_UNVERIFIED; not an upstream stock build. 3 warmup + 5 timed runs. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill linear wk_wv, M=2048, K=4096, N=1024, IO texture3d, weights texture2d, sarc8 run, logged kernel name sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half (name before the rename)"
    metric: microbench_kernel_median_us
    value: 1731.12
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 13 field kernel_median_us"
    baseline: "stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, same case: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 13 (separate claim)"
    notes: "Linear shader only; 3 warmup + 5 timed runs. ET_VK_SARC_UNVERIFIED=1; binaries predate the kernel rename, commit not recorded. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill linear wk_wv, M=2048, K=4096, N=1024, IO texture3d, weights texture2d, stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: microbench_kernel_median_us
    value: 2288.84
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 13 field kernel_median_us"
    notes: "Baseline measurement: release 1.5's tiled dq8ca kernel from the same binaries as sarc8, without ET_VK_SARC_UNVERIFIED; not an upstream stock build. 3 warmup + 5 timed runs. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill linear w1_w3, M=2048, K=4096, N=14336, IO texture3d, weights texture2d, sarc8 run, logged kernel name sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half (name before the rename)"
    metric: microbench_kernel_median_us
    value: 23703.8
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 15 field kernel_median_us"
    baseline: "stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, same case: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 15 (separate claim)"
    notes: "Linear shader only; 3 warmup + 5 timed runs. ET_VK_SARC_UNVERIFIED=1; binaries predate the kernel rename, commit not recorded. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill linear w1_w3, M=2048, K=4096, N=14336, IO texture3d, weights texture2d, stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: microbench_kernel_median_us
    value: 33248.7
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 15 field kernel_median_us"
    notes: "Baseline measurement: release 1.5's tiled dq8ca kernel from the same binaries as sarc8, without ET_VK_SARC_UNVERIFIED; not an upstream stock build. 3 warmup + 5 timed runs. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill linear w2, M=2048, K=14336, N=4096, IO texture3d, weights texture2d, sarc8 run, logged kernel name sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half (name before the rename)"
    metric: microbench_kernel_median_us
    value: 23836.2
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 17 field kernel_median_us"
    baseline: "stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8, same case: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 17 (separate claim)"
    notes: "Linear shader only; 3 warmup + 5 timed runs. ET_VK_SARC_UNVERIFIED=1; binaries predate the kernel rename, commit not recorded. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill linear w2, M=2048, K=14336, N=4096, IO texture3d, weights texture2d, stock8 run, kernel linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8"
    metric: microbench_kernel_median_us
    value: 33019.1
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 17 field kernel_median_us"
    notes: "Baseline measurement: release 1.5's tiled dq8ca kernel from the same binaries as sarc8, without ET_VK_SARC_UNVERIFIED; not an upstream stock build. 3 warmup + 5 timed runs. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc8 run, default mode"
    metric: prefill_tokens_per_second_single_run
    value: 1845.05
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 4"
    baseline: "sarc8 run tiled mode (line 3) and stock8 run (line 21): separate claims"
    notes: "One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc8 run, tiled mode (ET_VK_FORCE_TILED_LINEAR=1)"
    metric: prefill_tokens_per_second_single_run
    value: 1630.57
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 3"
    notes: "Baseline measurement. One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), stock8 run (same binaries, no ET_VK_SARC_UNVERIFIED; the proposal's 'stock 1.5' column)"
    metric: prefill_tokens_per_second_single_run
    value: 1624.11
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 21"
    notes: "Baseline measurement; not an upstream stock build. One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), SARC over 'stock 1.5' as stated by the proposal table"
    metric: end_to_end_speedup_ratio_as_stated_by_source
    value: 1.14
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43 row Radeon 780M column 'SARC / stock'"
    baseline: "the proposal's 'stock 1.5' column (stock8 run)"
    notes: "Ratio stated by the proposal from its rounded table values; copied, not recomputed here. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc8 run, default mode"
    metric: prefill_tokens_per_second_single_run
    value: 649.128
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 9"
    baseline: "sarc8 run tiled mode (line 8) and stock8 run (line 23): separate claims"
    notes: "One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc8 run, tiled mode (ET_VK_FORCE_TILED_LINEAR=1)"
    metric: prefill_tokens_per_second_single_run
    value: 565.902
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 8"
    notes: "Baseline measurement. One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), stock8 run (same binaries, no ET_VK_SARC_UNVERIFIED; the proposal's 'stock 1.5' column)"
    metric: prefill_tokens_per_second_single_run
    value: 569.363
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 23"
    notes: "Baseline measurement; not an upstream stock build. One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), SARC over 'stock 1.5' as stated by the proposal table"
    metric: end_to_end_speedup_ratio_as_stated_by_source
    value: 1.14
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43 row Radeon 780M column 'SARC / stock'"
    baseline: "the proposal's 'stock 1.5' column (stock8 run)"
    notes: "Ratio stated by the proposal from its rounded table values; copied, not recomputed here. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc8 run, default mode"
    metric: prefill_tokens_per_second_single_run
    value: 336.068
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 11"
    baseline: "sarc8 run tiled mode (line 10) and stock8 run (line 24): separate claims"
    notes: "One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), sarc8 run, tiled mode (ET_VK_FORCE_TILED_LINEAR=1)"
    metric: prefill_tokens_per_second_single_run
    value: 279.743
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 10"
    notes: "Baseline measurement. One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), stock8 run (same binaries, no ET_VK_SARC_UNVERIFIED; the proposal's 'stock 1.5' column)"
    metric: prefill_tokens_per_second_single_run
    value: 280.702
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 24"
    notes: "Baseline measurement; not an upstream stock build. One llama_main run with --warmup. Attention on release 1.5's own kernels (no SDPA coopmat in this change). Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), SARC over 'stock 1.5' as stated by the proposal table"
    metric: end_to_end_speedup_ratio_as_stated_by_source
    value: 1.2
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43 row Radeon 780M column 'SARC / stock'"
    baseline: "the proposal's 'stock 1.5' column (stock8 run)"
    notes: "Ratio stated by the proposal from its rounded table values; copied, not recomputed here. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "24 prefill microbench shapes (1B/3B/8B x 4 layer shapes x buffer/texture3d), kernel median against the 1.4 confirmation"
    metric: kernel_time_ratio_vs_1_4_study_as_stated_by_source
    value: 0.992
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43 row Radeon 780M column 'kernel ratio vs 1.4'"
    baseline: "the 1.4 confirmation run, whose data is not part of this result set"
    notes: "Stated by the proposal with the range 0.985-1.002 and defined on proposal.md line 37; copied, not recomputed here. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w prefill wq_wo, M=2048, K=2048, N=2048, IO buffer, weights texture2d; 8161 of 4194304 elements sampled"
    metric: production_diff_max_abs_diff
    value: 0.0156136
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log, line 11"
    baseline: "tolerance 0.5 (same line)"
    notes: "Sampled production-diff re-run (pdiff2), non-zero zero points; kernel sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half, correctness=PASSED. Log has no timestamp; date from the proposal heading. Lower end of the proposal's range. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w prefill w2, M=2048, K=14336, N=4096, IO buffer, weights texture2d"
    metric: production_diff_max_abs_diff
    value: 0.124
    measured_at: '2026-09-27'
    source_id: meas-780m-8da4w-port
    source_locator: "openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-buffer.log, line 44"
    baseline: "tolerance 0.500 (same line)"
    notes: "Sampled production-diff re-run (pdiff2), non-zero zero points; kernel sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half, correctness=PASSED. Log has no timestamp; date from the proposal heading. Upper end of the proposal's range. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), with the SDPA rows, default mode"
    metric: prefill_tokens_per_second_single_run
    value: 2544.1
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 12"
    baseline: "tiled mode, same result set: line 11 (separate claim)"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e. Both modes run the SARC SDPA kernels; the modes differ in the linear kernels only. ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), with the SDPA rows, tiled mode (ET_VK_FORCE_TILED_LINEAR=1)"
    metric: prefill_tokens_per_second_single_run
    value: 2155.79
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 11"
    notes: "Baseline measurement. One llama_main run (not a median), --warmup, directory sdpa-e2e. Both modes run the SARC SDPA kernels; the modes differ in the linear kernels only. ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), with the SDPA rows, default mode"
    metric: prefill_tokens_per_second_single_run
    value: 1048.11
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 19"
    baseline: "tiled mode, same result set: line 18 (separate claim)"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e. Both modes run the SARC SDPA kernels; the modes differ in the linear kernels only. ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), with the SDPA rows, tiled mode (ET_VK_FORCE_TILED_LINEAR=1)"
    metric: prefill_tokens_per_second_single_run
    value: 850.145
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 18"
    notes: "Baseline measurement. One llama_main run (not a median), --warmup, directory sdpa-e2e. Both modes run the SARC SDPA kernels; the modes differ in the linear kernels only. ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), with the SDPA rows, default mode"
    metric: prefill_tokens_per_second_single_run
    value: 486.692
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 23"
    baseline: "tiled mode, same result set: line 22 (separate claim)"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e. Both modes run the SARC SDPA kernels; the modes differ in the linear kernels only. ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "dynamic int8 activations (4h4w blocks), 4-bit weights (8da4w)"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), with the SDPA rows, tiled mode (ET_VK_FORCE_TILED_LINEAR=1)"
    metric: prefill_tokens_per_second_single_run
    value: 377.372
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 22"
    notes: "Baseline measurement. One llama_main run (not a median), --warmup, directory sdpa-e2e. Both modes run the SARC SDPA kernels; the modes differ in the linear kernels only. ET_VK_SARC_UNVERIFIED=1. Driver version attributed from the install history, not recorded by the run."
---

# 8da4w linear cooperative-matrix kernel on the Radeon 780M

Scope: one device (AMD Radeon 780M), one driver version (RADV Mesa 25.2.7), two measurement dates: 2026-09-27 (the port result sets `meas-780m-8da4w-port` and `meas-780m-sdpa-port`: microbenchmark, correctness, production-diff, single-run end-to-end) and 2026-09-28 (end-to-end campaign and its traces, `meas-780m-e2e-prefill`). The 2026-09-27 result sets do not record a driver version; it is attributed from the device's package install history (see "How the driver version is known"). Nothing on this page is established for any other device, driver version or date. All evidence files are in the public repository https://github.com/sarc-acl/executorch at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`; paths below are relative to that repository's root.

Citation form: `[<source page id>: <path>#L<line>]` points at a line of a raw file listed in that source page's `raw_data`. `[code: <path>#L<line>]` points at shader or selection source in the same repository and commit that no measurement source page excerpts; such statements describe what the code says, not something measured. Citations of `meas-780m-8da4w-port` and `meas-780m-sdpa-port` use the locator form of those pages, `<path>, line <N>`. `meas-780m-8da4w-port` also excerpts much of the source cited below as `[code: ...]`: `table_amd.cpp` lines 19-24 and 42-53, `Select.h` lines 80-116, the zpg yaml lines 10-35, the zpg shader header lines 9-19 and 38-45, the body file lines 16-22, 37-43 and 71-77, and `sarc/SWEEP-PARAMETERS.md` lines 72-81, 97-102, 121, 125-127 and 152-154.

Confidence note: the page is `verified`. `evidence_basis` holds first-party measurement pages that support the central claims directly: `meas-780m-8da4w-port` has the kernel-level microbenchmark of this kernel against release 1.5's tiled dq8ca kernel on the same shapes, the kernel-level correctness cases and the sampled production-diff of the shipped kernel names, and it excerpts the selection row and shader parameters; `meas-780m-sdpa-port` repeats the production-diff and the end-to-end runs with the shipped names; `meas-780m-e2e-prefill` has the per-dispatch GPU times of the shipped kernel in the 2026-09-28 campaign. Three qualifications stay attached to the label:

- The driver version of the two 2026-09-27 result sets is attributed from the install history, not recorded by the runs.
- The 2026-09-27 microbenchmark and correctness logs were produced by binaries that predate the kernel rename (logged name `sarc_linear_dq8ca_zpg_t128x64k32g42s32_*`) under `ET_VK_SARC_UNVERIFIED=1`; the result set records sha256 hashes of the binaries, not their commit [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt, lines 3-7].
- The baseline called "stock" in that result set is the same binaries without `ET_VK_SARC_UNVERIFIED`, not an upstream build (see "Measured results", section 3).

## How the driver version is known

The 2026-09-27 result set does not record a driver version. Its own device line names the driver only as `radv phoenix`:

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

[meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, line 5]

The version `RADV Mesa 25.2.7` used for every 2026-09-27 number on this page is attributed from the package install history captured on the device on 2026-10-04 [meas-780m-8da4w-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, line 1]; it is not recorded by the runs:

```text
mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1 installed Fri 29 May 2026 10:08:07 PM PDT built Wed 25 Feb 2026 06:58:58 AM PST
```

[meas-780m-8da4w-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, line 4]

```text
2026-05-29T22:08:06-0700 SUBDEBUG Upgrade: mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1.x86_64
2026-05-29T22:10:09-0700 SUBDEBUG Upgraded: mesa-vulkan-drivers-25.0.7-6.el10_1.x86_64
```

[meas-780m-8da4w-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 12-13]

- The package that owns the RADV driver library is `mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1.x86_64` [meas-780m-8da4w-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, line 8].
- The quoted package-log query returns only the 2026-05-29 entries for the Mesa driver packages, with no later change [meas-780m-8da4w-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 10-14].
- The run timestamps are `Sun Sep 27 10:09:35 PM UTC 2026` (start of the sarc8 run) and `Sun Sep 27 10:13:40 PM UTC 2026` (end of the stock8 run) [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt, line 1; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/done.txt, line 1]. The pdiff2 re-run logs carry no timestamp of their own; their date is the proposal's results heading, `## Results (2026-09-27; ...)` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 34].

The 2026-09-28 campaign numbers carry their driver version through `meas-780m-e2e-prefill`; the attribution above is not applied to them.

## What the kernel computes

- The operator is the "8da4w" quantized linear layer: 8-bit dynamic per-token activations with 4-bit weights [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L60].
- The shader header describes it as the "SARC dq8ca (8da4w) int8 cooperative-matrix linear, \"zpg\" family: 4h4w int8 activations, zero-point hoisted out of the group loop, dbuf4 pipeline" [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl#L10-L11]. The activations arrive already quantized in a packed int8 buffer; `t_input` is not read by this shader [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl#L65-L69].
- It keeps a per-group int32 cooperative-matrix accumulator and a running fp32 accumulator across groups (excerpt below) [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L71-L77].
- It serves the prefill linear layers: the SARC build issues 112, 196 and 224 dispatches of it per prefill for 1B, 3B and 8B [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L18, #L46, #L74; openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L353]. The 8-bit activation quantize is a separate dispatch family, present in both builds [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L84-L88].

## Shipped variant for the 780M

Kernel base name: `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L345; code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L49]. Dispatched in the campaign as `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L18]. The documentation lists the shipped 780M 8da4w variant as zpg `t128x64k32g42s32` + `A_MAP_FULL` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L127].

| Token part | Parameter | Meaning (as documented) | Citation |
|---|---|---|---|
| `t128x64` | `WG_TILE_M` x `WG_TILE_N` | output tile per workgroup | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L99, #L24] |
| `k32` | `WG_TILE_K` | K consumed per main-loop iteration | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L100, #L25] |
| `g42` | `SG_GRID_X`, `SG_GRID_Y` | subgroup grid in the workgroup, X along N, Y along M; workgroup size = X·Y·`SUBGROUP_SIZE` | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L101, #L26] |
| `s32` | `SUBGROUP_SIZE` | must equal the device's subgroup size, or lie within its supported range when subgroup-size control is available | [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L102, #L79-L80] |

- Yaml defaults of the family, not overridden by the two 780M variants: `MMA_M: 16`, `MMA_N: 16`, `MMA_K: 16`, `WG_TILE_M: 128`, `WG_TILE_N: 64`, `WG_TILE_K: 32`, `SG_GRID_X: 4`, `SG_GRID_Y: 2`, `SUBGROUP_SIZE: 32` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.yaml#L20-L28]. The two 780M variants (buffer and texture3d IO, texture2d weights) both set `A_MAP_FULL: true` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.yaml#L30-L35].
- Selection-table geometry: `{128, 64, 32, 4, 2, 32, 16, false}` [code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L50], fields `m, n, k, sg_grid_x, sg_grid_y, subgroup_size, mma_m, csh_in_ash` [code: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h#L81-L88]; row comment "zpg (4h4w activations), full A map" [code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L42].
- `A_MAP_FULL` is not part of the name; it has to be read from the yaml entry [code: sarc/SWEEP-PARAMETERS.md#L121]. Documented meaning: each thread stages exactly one A block, "which removes the `a_active` guard from the hot loop"; it may be set only when `A_ACTIVE_THREADS == WG_SIZE` has been checked for the tile [code: sarc/SWEEP-PARAMETERS.md#L58]. The shader comment gives the reason: the guard is statically always true for such a tile, "but the driver compiler does not fold it" because the bound comes from a spec constant, so the comparison survives as a real branch in the hot loop [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl#L38-L43].
- Subgroup size: the device default is 64, minimum 32, with subgroup-size control [meas-780m-vulkaninfo: sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, lines 1232, 1340, 687] (device-properties export dated `2026-9-1` in the file [meas-780m-vulkaninfo: sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, line 11220]); the code comment on the AMD device predicate says the shipped RDNA cooperative-matrix variants force subgroup size 32 per pipeline [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L19-L21].

### Shader excerpts

Double-buffered operand staging in shared memory. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L41-L43` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
// Double-buffered MMA operand staging.
shared uint Ash_int8[2u * ASH_SLICE_U32];
shared uint Bsh_int8[2u * BSH_SLICE_U32];
```

The two accumulators. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L71-L77` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
// Running fp32 accumulator (across all groups).
coopmat<float, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator>
    result[MMAS_PER_SG_M][MMAS_PER_SG_N];

// Per-group int32 MMA accumulator.
coopmat<int32_t, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator>
    accum_int32[MMAS_PER_SG_M][MMAS_PER_SG_N];
```

Workgroup geometry. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh#L16-L17` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
const uint NUM_SUBGROUPS = SG_GRID_X * SG_GRID_Y;
const uint WG_SIZE = NUM_SUBGROUPS * SUBGROUP_SIZE;
```

These fragments are verbatim and depend on the surrounding file (tile constants are template parameters filled from the yaml); they are not a standalone shader.

## How it is selected

- Row: device substring `"780m"`, predicate `amd_wave64`, op `Op::kDq8caLinear`, storage mask `kTex3dTex2d | kBufTex2d`, status `Status::kVerified` [code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L46-L53]. `amd_wave64` is `d.is_amd && d.subgroup_size == 64` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L22-L24]. The release status table lists 8da4w on the Radeon 780M as verified [meas-780m-4w-bootstrap: sarc/README.md#L82].
- Rows are tried in order and only verified rows are active in a release [meas-780m-4w-bootstrap: sarc/README.md#L19-L20]; in the campaign's sarc build: "Kernel choice is by device name, from verified rows only" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L259].
- For an 8da4w op the selector additionally requires `device.int8_coopmat` [code: backends/vulkan/runtime/graph/ops/impl/sarc/Select.cpp#L82-L85]. The device-properties export in this wiki does not enumerate cooperative-matrix shapes, so it neither shows nor rules out an int8 shape (see `hw-cooperative-matrix-rdna3`); that the row is selected on this device is shown by the dispatch record [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L18, #L46, #L74].
- Shape preconditions enforced by `sarc::select()`: tile divisibility of M, N and K, `group_size % WG_TILE_K == 0`, no bias, batch 1, not a single-token call, allowed storage combination, subgroup size, shared-memory limit [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L74-L81].
- Prompt length matters: on the campaign's 1972-token check prompt, where "M is not a multiple of any tile" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L322], the report gives the SARC path for the 780M 8B 8da4w cell as "GEMM falls back to stock kernels; attention still uses SARC kernels" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L394].

## Correctness evidence

### Kernel level (2026-09-27, `meas-780m-8da4w-port` and `meas-780m-sdpa-port`)

- **Correctness cases.** In the sarc8 run the two rank-3 dq8ca cases (M128 K128 N128 and M128 K4096 N128, buffer) both end `correctness=PASSED` on the kernel logged as `sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/correctness.log, lines 285-286]. The same lines carry the label `(NOT coopmat -- fallback)` and the run summary reads `correctness rc=1 [correctness] FAILED` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 1]. The proposal attributes such labels to the harness, which "saw no \"coopmat\" in the old `sarc_linear_dq8ca_zpg*` names" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 52-53]; that sentence is written about the production-diff run, and the correctness lines show the same name-based label next to a numeric PASSED.
- **Production-diff, first run (old names).** All six model x storage files report `FAILED` with `rc=1` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 12-17], while the per-case line reads `(NOT coopmat -- fallback, cannot validate the shader under test), correctness=PASSED` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/pdiff-llama-3.2-1b-8da4w-buffer.log, line 17]. "The kernels have been renamed, and the re-run is in `results/*/pdiff2`" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 53].
- **Production-diff, re-run (pdiff2, shipped names).** All six files (1B, 3B, 8B x buffer, texture3d; 4 shapes each, M=2048) end `[production-diff] ALL PASSED`, and their first case line names `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half` or `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half` with `(coopmat dispatched), correctness=PASSED` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log, lines 17 and 51; openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-texture3d.log, lines 17 and 51; openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-3b-8da4w-buffer.log, lines 17 and 51; openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-3b-8da4w-texture3d.log, lines 17 and 51; openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-buffer.log, lines 17 and 51; openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-texture3d.log, lines 17 and 51]. The diff is sampled (for the 1B wq_wo buffer case, "checking 8161 of 4194304 elements" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log, line 10]) and uses non-zero activation zero points (`--production-diff-nonzero-zp` for 8da4w [meas-780m-8da4w-port: sarc/tools/verify.sh, line 113]).
- **Error size.** The proposal gives the 780M range as "max |err| 0.016–0.124 against 0.5" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 50-51]. The two ends in the logs: `max abs diff 0.0156136 (tol 0.5)` for 1B wq_wo (M=2048, K=2048, N=2048, buffer) [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log, line 11] and `max abs diff 0.124 (tol 0.500)` for 8B w2 (M=2048, K=14336, N=4096, buffer) [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-buffer.log, line 44]. The values of the other 22 cases are on the source page.
- **Production-diff, third pass.** The SDPA port's verification run repeats the 8da4w production-diff with `rc=0` and `ALL PASSED` for all six files [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 25-30].

### Model level, port result sets (2026-09-27)

The result sets do not record the command line. Their output file names and summary-line formats match `sarc/tools/verify.sh` at the code commit, so the run parameters cited to that script below and in Performance section 4 (`cmp` comparison, `--warmup`, prompt file, token counts, `--production-diff-nonzero-zp`) are what the script does, not something the logs state; `run8.out` also contains the lines `---- stock` and `ALLDONE`, which the script does not print [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 18, 25].

Generated text of default mode versus tiled mode (`ET_VK_FORCE_TILED_LINEAR=1`), Llama 3.2 1B, compared with `cmp` after dropping observer and log lines [meas-780m-8da4w-port: sarc/tools/verify.sh, line 77]:

- Check prompt (1972 prompt tokens [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/check-1b-8da4w-default.log, line 140]): `SAME` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 5].
- Unaligned prompt (1792 prompt tokens [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/unaligned-1b-8da4w-default.log, line 7]): **`DIFFER`** [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 6]. The text line before the observer line is `2` in tiled mode and a single space in default mode; the stock8 run prints `2` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/unaligned-1b-8da4w-tiled.log, line 6; openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/unaligned-1b-8da4w-default.log, line 6; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/unaligned-1b-8da4w-default.log, line 5]. The proposal's account: "780M: 1.4 tiled, 1.4 tuned and 1.5 SARC all give the same token, and only 1.5 tiled flips." and "Production-diff is within tolerance. This is a near-tie flip in 1.5's tiled path, not a port error." [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 59-60]. The 1.4 runs that this account refers to are not part of the result set, so the explanation is the proposal's, not something this wiki can check; the difference should not be described as a plain pass.
- With the SDPA rows present, later the same day, both comparisons read `SAME` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 13-14].
- Decode (32 new tokens requested [meas-780m-8da4w-port: sarc/tools/verify.sh, line 104]) completed with `rc=0` and 31 generated tokens [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 7]. A single-token call does not meet this kernel's shape preconditions (see "How it is selected"), so the decode run does not exercise it.

### Model level, 2026-09-28 campaign

- Tile-aligned 2048-token real-text prompt, logits probe, 2026-09-28: top-1 token identical between stock and sarc for 1B, 3B and 8B 8da4w [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv#L4, #L8, #L12]. Logits are not bitwise identical (`bitwise_identical_top10` False on those rows); the report names 780M 1B 8da4w as the largest top-10 logit difference of the whole campaign, "2.0 (780M 1B 8da4w)" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L386], which is the `max_abs_dlogit_top10` value 2.0156 of that row [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv#L4].
- 1972-token check prompt: next token SAME for 1B and 3B, **DIFFER for 8B** [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/tables.md#L28-L30, #L63]; the probe shows stock top-1 id 6062 and sarc top-1 id 45647 for that cell [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv#L13]. The report's reading: at M = 1972 the "GEMM falls back to stock kernels; attention still uses SARC kernels", and the logit margins between the two candidate tokens are −0.09 for stock and +0.50 for sarc [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L394]. By that account the difference does not come from this kernel, which is not dispatched at that prompt length; it should still not be described as a plain pass.
- Clocks were not pinned [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L422].

## Measured results

Sections 1 and 2 are from the 2026-09-28 campaign; sections 3 to 5 are from the 2026-09-27 port result sets. Campaign builds: stock (upstream release/1.5 @ `985c1ceccc`) and sarc (tag `sarc/1.5-r2`) [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L247, #L256]. The stock build's 8da4w prefill linear is `linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L25], which uses `dotPacked4x8AccSatEXT` with a per-group zero-point correction and no cooperative matrix [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L130-L132]. No ratio on this page is computed by the wiki.

### 1. Warm-trace GPU time and rate of the prefill GEMM family (kernel level)

One warm ETDump trace per cell and build, no repeat [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L76, #L445]. Rate is sum of 2·M·N·K over sum of GPU time; for 8da4w these are integer ops, TOP/s [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L78; openspec/changes/sarc-1.5-e2e-benchmark/evidence/roofline.md#L161].

| Model | sarc GEMM ms | sarc dispatches | sarc rate | stock GEMM ms | stock dispatches | stock rate | Citation |
|---|---|---|---|---|---|---|---|
| Llama 3.2 1B | 400.402 | 112 | 9.954 | 541.972 | 112 | 7.354 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L27; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L18; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L20; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L40; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L25; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L23] |
| Llama 3.2 3B | 1181.007 | 196 | 9.775 | 1621.24 | 196 | 7.121 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L78; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L46; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L21; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L91; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L53; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L24] |
| Llama 3.1 8B | 2965.232 | 224 | 9.641 | 4142.245 | 224 | 6.901 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L129; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L74; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L22; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L142; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L81; openspec/changes/sarc-1.5-e2e-benchmark/evidence/efficiency.csv#L25] |

The source's own kernel-level ratio for these traces ("GEMM x", stock over sarc) is 1.35 / 1.37 / 1.40 for 1B / 3B / 8B [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/modelsize.txt#L8-L10].

Activation-quantize dispatches (operator level, not this kernel), GPU ms per warm prefill:

| Model | sarc quantize ms | stock quantize ms | Citation |
|---|---|---|---|
| Llama 3.2 1B | 43.13 | 43.231 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L32; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L45] |
| Llama 3.2 3B | 101.421 | 100.699 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L82; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L96] |
| Llama 3.1 8B | 165.872 | 167.005 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L133; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L147] |

Single warm dispatches, first row of each distinct shape in `gemm.csv` (rate column in TOP/s):

| Model | M | N | K | sarc ms | sarc rate | stock ms | stock rate | Citation |
|---|---|---|---|---|---|---|---|---|
| Llama 3.2 1B | 2048 | 2048 | 2048 | 1.7644 | 9.737 | 2.181 | 7.877 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L226 (sarc), #L338 (stock)] |
| Llama 3.2 1B | 2048 | 512 | 2048 | 0.4546 | 9.448 | 0.5354 | 8.021 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L227 (sarc), #L339 (stock)] |
| Llama 3.2 1B | 2048 | 8192 | 2048 | 6.8822 | 9.985 | 9.3911 | 7.318 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L230 (sarc), #L342 (stock)] |
| Llama 3.2 1B | 2048 | 2048 | 8192 | 6.8637 | 10.012 | 9.6655 | 7.11 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L232 (sarc), #L344 (stock)] |
| Llama 3.2 3B | 2048 | 3072 | 3072 | 4.1252 | 9.37 | 6.1424 | 6.293 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L842 (sarc), #L1038 (stock)] |
| Llama 3.2 3B | 2048 | 1024 | 3072 | 1.312 | 9.821 | 1.5575 | 8.273 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L843 (sarc), #L1039 (stock)] |
| Llama 3.2 3B | 2048 | 8192 | 3072 | 10.2005 | 10.105 | 13.8799 | 7.427 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L846 (sarc), #L1042 (stock)] |
| Llama 3.2 3B | 2048 | 3072 | 8192 | 10.593 | 9.731 | 14.9735 | 6.884 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L848 (sarc), #L1044 (stock)] |
| Llama 3.1 8B | 2048 | 4096 | 4096 | 7.2757 | 9.445 | 10.4197 | 6.595 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1682 (sarc), #L1906 (stock)] |
| Llama 3.1 8B | 2048 | 1024 | 4096 | 1.8994 | 9.045 | 2.3424 | 7.334 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1683 (sarc), #L1907 (stock)] |
| Llama 3.1 8B | 2048 | 14336 | 4096 | 24.8404 | 9.683 | 35.9027 | 6.699 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1686 (sarc), #L1910 (stock)] |
| Llama 3.1 8B | 2048 | 4096 | 14336 | 24.3698 | 9.87 | 34.6389 | 6.944 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/gemm.csv#L1688 (sarc), #L1912 (stock)] |

The report's decomposition of the 8B difference between SARC 8da4w and SARC 4w (see `kernel-linear-4w-780m`) attributes +188 ms to the GEMM ("the int8 kernel is 6.8 % slower"), +166 ms to the activation quantize and −92 ms to view copies [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L319-L321].

### 2. End to end (sarc build includes SARC attention kernels)

Median of 5 timed runs per build, `prompt_2048.txt` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L291]. The sarc build's speedup on the 780M includes the coopmat QK^T/AV kernels and the truncated softmax [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L115-L116], so these values are not attributable to this kernel alone.

| Model | stock median tok/s | sarc median tok/s | speedup (ratio of medians, from the file) | next token (1972-token check) | Citation |
|---|---|---|---|---|---|
| Llama 3.2 1B | 1635.78 (min 1625.4, max 1643.66) | 2544.1 (min 2540.94, max 2547.26) | 1.5552824952010662 | SAME | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L17] |
| Llama 3.2 3B | 564.654 (min 563.566, max 568.257) | 1051.33 (min 1051.33, max 1052.42) | 1.8619012705125615 | SAME | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L18] |
| Llama 3.1 8B | 282.055 (min 281.589, max 282.405) | 489.133 (min 488.783, max 489.367) | 1.7341759585896366 | DIFFER | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L19] |

### 3. Kernel-level microbenchmark of the port result set (2026-09-27)

Source: `meas-780m-8da4w-port`. Protocol: "3 warmup + 5 timed runs per case", prefill M=2048, `linear group_size=128` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, line 4]. Two runs of the same three binaries (identical sha256 for `llama_main`, `test_llama_microbench` and `libllama_runner.so` in both environment files [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt, lines 3-7; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/env.txt, lines 3-6]):

- **sarc8**: environment has `ET_VK_SARC_UNVERIFIED=1` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt, line 4], the switch that "activates `kUnverified` rows" [meas-780m-8da4w-port: sarc/SWEEP-PARAMETERS.md, line 153]. Dispatched: 12 cases of `sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half` and 12 of `sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 2]. These are the names before the rename; the shipped names appear in the pdiff2 logs and in the selection table.
- **stock8**: no `ET_VK_SARC_UNVERIFIED` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/env.txt, lines 3-6]. Dispatched: 12 cases each of `linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8` and `linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 20], release 1.5's tiled dq8ca kernel. The proposal labels this column "stock 1.5" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43]; it is the same binaries with the 8da4w row inactive, not an upstream stock build.

`kernel_median_us` is the median time of the linear shader alone, in microseconds. The table is a subset of the 24 cases per run: IO storage texture3d (the storage the 2026-09-28 campaign dispatched end to end, see "Shipped variant for the 780M"), for the smallest and the largest model, all four layer shapes. The Llama 3.2 3B cases, all buffer cases, and the other fields of each case (op mean and stdev, kernel mean, coefficient of variation, GFLOP/s) are on the source page (`linear-8da4w.json`, lines 11-34 of each run). No ratio is computed here.

| Model | op | (M,K,N) | sarc8 kernel_median_us | stock8 kernel_median_us | Citation |
|---|---|---|---|---|---|
| Llama 3.2 1B | wq_wo | (2048,2048,2048) | 1748.84 | 2238.06 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 27; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 27] |
| Llama 3.2 1B | wk_wv | (2048,2048,512) | 455.4 | 538.92 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 29; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 29] |
| Llama 3.2 1B | w1_w3 | (2048,2048,8192) | 6886.1 | 9509.38 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 31; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 31] |
| Llama 3.2 1B | w2 | (2048,8192,2048) | 6871.94 | 9809.82 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 33; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 33] |
| Llama 3.1 8B | wq_wo | (2048,4096,4096) | 6798.32 | 9631.9 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 11; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 11] |
| Llama 3.1 8B | wk_wv | (2048,4096,1024) | 1731.12 | 2288.84 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 13; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 13] |
| Llama 3.1 8B | w1_w3 | (2048,4096,14336) | 23703.8 | 33248.7 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 15; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 15] |
| Llama 3.1 8B | w2 | (2048,14336,4096) | 23836.2 | 33019.1 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json, line 17; openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json, line 17] |

- Dispatch geometry as logged for the 8B wq_wo texture3d case: the SARC kernel runs with global work size `(16384,16,1)` and local work size `(256,1,1)` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, line 10]; release 1.5's tiled kernel with `(512,512,1)` and `(8,8,1)` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.log, line 9]. The selection code defines the workgroup size as `sg_grid_x * sg_grid_y * subgroup_size` [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h, line 92].
- Harness labels to ignore in the sarc8 logs: every case is recorded with `"variant": "tiled"`, buffer cases with `"dispatch": "fallback_tiled"`, the summary marks them `!` ("buffer case did NOT dispatch a coopmat shader" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, line 241]) and the step returns `rc=1` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, line 2]. The check is by kernel name, and the old names did not contain "coopmat" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 52-53]. For the same reason the log's own speedup columns are empty; none is cited.
- Against the earlier 1.4 study the proposal states a kernel ratio of 0.992 (0.985–1.002) [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43], defined as "microbench kernel median against the 1.4 confirmation, 24 shapes" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 37]; the selection-table comment repeats it as "kernels 0.992x of the 1.4 study" [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, line 43]. The 1.4 data is not in the result set.

### 4. End to end in the port result set (2026-09-27, attention on release 1.5's kernels)

One `llama_main` run per cell; in `sarc/tools/verify.sh` at the code commit (command line not recorded by the result set, see "Model level, port result sets") the run uses `--warmup`, `prompt_2048.txt` and 1 new token, and tiled mode sets `ET_VK_FORCE_TILED_LINEAR=1` [meas-780m-8da4w-port: sarc/tools/verify.sh, lines 88-89], which "sends the SARC linears to release 1.5's tiled/coop kernels, as the baseline" [meas-780m-8da4w-port: sarc/SWEEP-PARAMETERS.md, line 154]. This change does not contain the SDPA cooperative-matrix kernels [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 38-39], so here the difference between the columns is the linear kernel. Values are 2048-token prefill tok/s.

| Model | sarc8 tiled | sarc8 default | stock8 | SARC / stock as stated by the proposal | Citation |
|---|---|---|---|---|---|
| Llama 3.2 1B | 1630.57 | 1845.05 | 1624.11 | 1.14 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 3, 4, 21; openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43] |
| Llama 3.2 3B | 565.902 | 649.128 | 569.363 | 1.14 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 8, 9, 23; openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43] |
| Llama 3.1 8B | 279.743 | 336.068 | 280.702 | 1.20 | [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 10, 11, 24; openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43] |

The ratio column is copied from the proposal table, which works from its own rounded values (1845 / 649 / 336 against 1624 / 569 / 281) [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, line 43]; it is not recomputed here. The check, unaligned and decode runs of this result set are single runs without `--warmup`, and their prefill values are not comparable to this table.

### 5. End to end with the SDPA rows (2026-09-27, later run)

Source: `meas-780m-sdpa-port`, result directory `sdpa-e2e` (run started `Sun Sep 27 10:28:02 PM UTC 2026` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/env.txt, line 1], `ET_VK_SARC_UNVERIFIED=1` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/env.txt, line 4]). The linear microbench step of that run dispatched the shipped names, 12 cases each of `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half` and `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 5]. Each value is one `llama_main` run, not a median. Both modes run the SARC SDPA kernels (`ET_VK_FORCE_TILED_LINEAR` "only affects the linears" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 28]), so the two columns differ in the linear kernels only.

| Model | tiled linears, tok/s | default (this kernel), tok/s | Citation |
|---|---|---|---|
| Llama 3.2 1B | 2155.79 | 2544.1 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 11-12] |
| Llama 3.2 3B | 850.145 | 1048.11 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 18-19] |
| Llama 3.1 8B | 377.372 | 486.692 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 22-23] |

The selection-table comment on the 780M 8da4w row cites the rounded default-mode values: "with the SDPA rows, prefill 1B/3B/8B 2544/1048/487 tok/s" [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, line 44]. The linear microbench step of this run returned `rc=1` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 5], and its texture3d rows carry a dispatch label that the log itself says makes its speedup numbers untrustworthy; the raw per-case times are on the source page and are not cited here.

## Limits of this page

- One device, one driver version, two consecutive days (2026-09-27 and 2026-09-28).
- For the 2026-09-27 result sets the driver version is attributed from the device's package install history; the runs record only the driver name. The pdiff2 logs have no timestamp of their own.
- The 2026-09-27 microbenchmark was taken with binaries that predate the kernel rename and whose commit is not recorded; it is evidence for the kernel logged as `sarc_linear_dq8ca_zpg_t128x64k32g42s32_*`. The shipped names are measured at kernel level by the 2026-09-28 traces (section 1) and checked by the pdiff2 and `sdpa-e2e` production-diff runs.
- The "stock" column of the 2026-09-27 result set is the same binaries without `ET_VK_SARC_UNVERIFIED`, not an upstream build. The upstream build is the stock build of the 2026-09-28 campaign.
- The microbenchmark table is a subset (texture3d, 1B and 8B); the 3B and buffer cases are on `meas-780m-8da4w-port`.
- The 2026-09-27 end-to-end values are single runs; the 2026-09-28 values are medians of 5.
- The 0.992 kernel ratio against the 1.4 study is the proposal's statement; the 1.4 data is not held by this wiki.
- The traces of the 2026-09-28 campaign carry no timestamp of their own; their date and driver rest on the campaign report describing them as part of the campaign. Per-dispatch and family times come from a single warm trace per cell.
- Two next-token differences are recorded and unresolved by first-party evidence in this wiki: the 1792-token prompt in the 2026-09-27 sarc8 run (default versus tiled) and the 8B 1972-token check cell of the 2026-09-28 campaign (sarc versus stock).
