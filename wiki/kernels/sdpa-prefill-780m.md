---
id: kernel-sdpa-prefill-780m
title: "Prefill attention (SDPA) cooperative-matrix kernels on the Radeon 780M: sarc_sdpa_qk_coopmat t128x64k32g22s64, sarc_sdpa_av_coopmat t64x64k32g22s64 and the truncated softmax"
type: kernel
architectures: [radeon-780m]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, gemm, cooperative-matrix, coopmat-fp32-accumulator, subgroup-size, wave64, storage-buffer, workgroup-tile-sizing, k-chunk-sizing, subgroup-grid, required-subgroup-size, fp32-accumulation, causal-truncation]
confidence: source-reported
reproducibility: snippet
kernel_types: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill]
languages: [glsl]
aliases: ["sarc_sdpa_qk_coopmat", "sarc_sdpa_av_coopmat", "sarc_sdpa_attn_weights_softmax", "t128x64k32g22s64", "t64x64k32g22s64", "SDPA coopmat 780M", "attention 780M"]
related: [hw-radeon-780m, hw-cooperative-matrix-rdna3, kernel-linear-4w-780m, kernel-linear-8da4w-780m, technique-causal-truncation]
sources: [meas-780m-sdpa-port, meas-780m-e2e-prefill, meas-780m-4w-bootstrap, meas-780m-vulkaninfo]
evidence_basis:
  - evidence_type: measurement
    source_id: meas-780m-sdpa-port
    locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, lines 17-23 (kernel-level correctness, coopmat dispatched); openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 3-28 and 30-39 (per-family GPU ms and per-call microbench, 1.4 and 1.5 before the port); openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, lines 46-81 (release 1.5 tiled SDPA microbench); openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 6-23 (end to end after the port); openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 32-48; backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 78-96; sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 3-5 and 10-14 (driver version attributed from the install history, not recorded by the run)"
  - evidence_type: measurement
    source_id: meas-780m-e2e-prefill
    locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv rows gpu=780m, families attention: QK^T / AV / softmax; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L5-L7, #L12-L14; openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L227-L233; openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L115-L116, #L345"
  - evidence_type: measurement
    source_id: meas-780m-4w-bootstrap
    locator: "openspec/changes/sarc-1.5-bootstrap/proposal.md#L92-L97 (end-to-end state before the SDPA kernels were ported); sarc/README.md#L82"
  - evidence_type: measurement
    source_id: meas-780m-vulkaninfo
    locator: "sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, lines 1232, 11220"
performance_claims:
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (16 dispatches of sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 75.223
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L4 row gpu=780m,model=1b,scheme=4w,build=sarc,family=attention: QK^T column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_attn_weights_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L7."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (16 dispatches of sdpa_compute_attn_weights_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 156.725
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L17 row gpu=780m,model=1b,scheme=4w,build=stock,family=attention: QK^T column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L13."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (16 dispatches of sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 43.553
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L7 row gpu=780m,model=1b,scheme=4w,build=sarc,family=attention: AV column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_out_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L6."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (16 dispatches of sdpa_compute_out_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 222.493
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L15 row gpu=780m,model=1b,scheme=4w,build=stock,family=attention: AV column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L14."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (16 dispatches of sarc_sdpa_attn_weights_softmax_buffer_half), build sarc"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 115.253
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L3 row gpu=780m,model=1b,scheme=4w,build=sarc,family=attention: softmax column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_attn_weights_softmax: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L5."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (16 dispatches of sdpa_attn_weights_softmax_buffer_half), build stock"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 161.568
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L16 row gpu=780m,model=1b,scheme=4w,build=stock,family=attention: softmax column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L12."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (28 dispatches of sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 161.669
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L54 row gpu=780m,model=3b,scheme=4w,build=sarc,family=attention: QK^T column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_attn_weights_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L35."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (28 dispatches of sdpa_compute_attn_weights_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 567.461
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L67 row gpu=780m,model=3b,scheme=4w,build=stock,family=attention: QK^T column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L41."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (28 dispatches of sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 84.452
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L58 row gpu=780m,model=3b,scheme=4w,build=sarc,family=attention: AV column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_out_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L34."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (28 dispatches of sdpa_compute_out_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 832.381
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L66 row gpu=780m,model=3b,scheme=4w,build=stock,family=attention: AV column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L42."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (28 dispatches of sarc_sdpa_attn_weights_softmax_buffer_half), build sarc"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 150.302
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L55 row gpu=780m,model=3b,scheme=4w,build=sarc,family=attention: softmax column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_attn_weights_softmax: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L33."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (28 dispatches of sdpa_attn_weights_softmax_buffer_half), build stock"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 206.803
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L68 row gpu=780m,model=3b,scheme=4w,build=stock,family=attention: softmax column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L40."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (32 dispatches of sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 236.855
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L106 row gpu=780m,model=8b,scheme=4w,build=sarc,family=attention: QK^T column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_attn_weights_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L63."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (32 dispatches of sdpa_compute_attn_weights_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 881.685
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L118 row gpu=780m,model=8b,scheme=4w,build=stock,family=attention: QK^T column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L69."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (32 dispatches of sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 130.914
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L109 row gpu=780m,model=8b,scheme=4w,build=sarc,family=attention: AV column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_out_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L62."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (32 dispatches of sdpa_compute_out_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 1314.39
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L117 row gpu=780m,model=8b,scheme=4w,build=stock,family=attention: AV column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L70."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (32 dispatches of sarc_sdpa_attn_weights_softmax_buffer_half), build sarc"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 229.259
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L107 row gpu=780m,model=8b,scheme=4w,build=sarc,family=attention: softmax column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_attn_weights_softmax: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L61."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (32 dispatches of sdpa_attn_weights_softmax_buffer_half), build stock"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 315.328
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L120 row gpu=780m,model=8b,scheme=4w,build=stock,family=attention: softmax column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L68."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (8da4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (16 dispatches of sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 75.085
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L29 row gpu=780m,model=1b,scheme=8da4w,build=sarc,family=attention: QK^T column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_attn_weights_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L21."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (8da4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (16 dispatches of sdpa_compute_attn_weights_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 156.762
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L43 row gpu=780m,model=1b,scheme=8da4w,build=stock,family=attention: QK^T column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L27."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (8da4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (16 dispatches of sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 43.421
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L31 row gpu=780m,model=1b,scheme=8da4w,build=sarc,family=attention: AV column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_out_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L20."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (8da4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (16 dispatches of sdpa_compute_out_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 223.588
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L41 row gpu=780m,model=1b,scheme=8da4w,build=stock,family=attention: AV column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L28."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (8da4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (16 dispatches of sarc_sdpa_attn_weights_softmax_buffer_half), build sarc"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 115.272
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L28 row gpu=780m,model=1b,scheme=8da4w,build=sarc,family=attention: softmax column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_attn_weights_softmax: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L19."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (8da4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (16 dispatches of sdpa_attn_weights_softmax_buffer_half), build stock"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 161.686
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L42 row gpu=780m,model=1b,scheme=8da4w,build=stock,family=attention: softmax column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L26."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (8da4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (28 dispatches of sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 161.108
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L79 row gpu=780m,model=3b,scheme=8da4w,build=sarc,family=attention: QK^T column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_attn_weights_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L49."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (8da4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (28 dispatches of sdpa_compute_attn_weights_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 567.719
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L93 row gpu=780m,model=3b,scheme=8da4w,build=stock,family=attention: QK^T column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L55."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (8da4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (28 dispatches of sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 85.409
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L84 row gpu=780m,model=3b,scheme=8da4w,build=sarc,family=attention: AV column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_out_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L48."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (8da4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (28 dispatches of sdpa_compute_out_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 820.602
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L92 row gpu=780m,model=3b,scheme=8da4w,build=stock,family=attention: AV column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L56."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (8da4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (28 dispatches of sarc_sdpa_attn_weights_softmax_buffer_half), build sarc"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 150.211
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L80 row gpu=780m,model=3b,scheme=8da4w,build=sarc,family=attention: softmax column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_attn_weights_softmax: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L47."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (8da4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (28 dispatches of sdpa_attn_weights_softmax_buffer_half), build stock"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 206.358
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L94 row gpu=780m,model=3b,scheme=8da4w,build=stock,family=attention: softmax column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L54."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (8da4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (32 dispatches of sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 237.046
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L131 row gpu=780m,model=8b,scheme=8da4w,build=sarc,family=attention: QK^T column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_attn_weights_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L77."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (8da4w export), all 'attention: QK^T' dispatches of one warm 2048-token prefill trace (32 dispatches of sdpa_compute_attn_weights_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_qk_family_warm_trace
    value: 885.397
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L144 row gpu=780m,model=8b,scheme=8da4w,build=stock,family=attention: QK^T column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L83."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (8da4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (32 dispatches of sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half), build sarc"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 131.181
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L135 row gpu=780m,model=8b,scheme=8da4w,build=sarc,family=attention: AV column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_compute_out_tiled: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L76."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (8da4w export), all 'attention: AV' dispatches of one warm 2048-token prefill trace (32 dispatches of sdpa_compute_out_tiled_buffer_buffer_half), build stock"
    metric: gpu_time_ms_attention_av_family_warm_trace
    value: 1297.812
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L143 row gpu=780m,model=8b,scheme=8da4w,build=stock,family=attention: AV column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L84."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (8da4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (32 dispatches of sarc_sdpa_attn_weights_softmax_buffer_half), build sarc"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 228.655
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L132 row gpu=780m,model=8b,scheme=8da4w,build=sarc,family=attention: softmax column ms"
    baseline: "build stock (upstream release/1.5), kernel family sdpa_attn_weights_softmax: separate claim"
    notes: "One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L75."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (8da4w export), all 'attention: softmax' dispatches of one warm 2048-token prefill trace (32 dispatches of sdpa_attn_weights_softmax_buffer_half), build stock"
    metric: gpu_time_ms_attention_softmax_family_warm_trace
    value: 314.731
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L145 row gpu=780m,model=8b,scheme=8da4w,build=stock,family=attention: softmax column ms"
    notes: "Baseline measurement. One warm ETDump trace per cell, no repeat (TECHNICAL-REPORT.md#L76, #L445); the trace carries no timestamp of its own, date is the campaign date. Dispatch count from results/dispatch.csv#L82."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), QK^T kernel family, warm 2048-token prefill trace"
    metric: attention_qk_speedup_sarc_over_stock_as_stated_by_source
    value: 2.08
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L231 table 'The 780M's attention, per kernel (4w)', column 1B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), QK^T kernel family, warm 2048-token prefill trace"
    metric: attention_qk_speedup_sarc_over_stock_as_stated_by_source
    value: 3.51
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L231 table 'The 780M's attention, per kernel (4w)', column 3B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), QK^T kernel family, warm 2048-token prefill trace"
    metric: attention_qk_speedup_sarc_over_stock_as_stated_by_source
    value: 3.72
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L231 table 'The 780M's attention, per kernel (4w)', column 8B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), AV kernel family, warm 2048-token prefill trace"
    metric: attention_av_speedup_sarc_over_stock_as_stated_by_source
    value: 5.11
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L232 table 'The 780M's attention, per kernel (4w)', column 1B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), AV kernel family, warm 2048-token prefill trace"
    metric: attention_av_speedup_sarc_over_stock_as_stated_by_source
    value: 9.86
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L232 table 'The 780M's attention, per kernel (4w)', column 3B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), AV kernel family, warm 2048-token prefill trace"
    metric: attention_av_speedup_sarc_over_stock_as_stated_by_source
    value: 10.04
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L232 table 'The 780M's attention, per kernel (4w)', column 8B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B (4w export), softmax kernel family, warm 2048-token prefill trace"
    metric: attention_softmax_speedup_sarc_over_stock_as_stated_by_source
    value: 1.4
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L233 table 'The 780M's attention, per kernel (4w)', column 1B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B (4w export), softmax kernel family, warm 2048-token prefill trace"
    metric: attention_softmax_speedup_sarc_over_stock_as_stated_by_source
    value: 1.38
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L233 table 'The 780M's attention, per kernel (4w)', column 3B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B (4w export), softmax kernel family, warm 2048-token prefill trace"
    metric: attention_softmax_speedup_sarc_over_stock_as_stated_by_source
    value: 1.38
    measured_at: '2026-09-28'
    source_id: meas-780m-e2e-prefill
    source_locator: "openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L233 table 'The 780M's attention, per kernel (4w)', column 8B"
    baseline: "build stock (upstream release/1.5) attention kernels (sdpa_*_tiled, sdpa_attn_weights_softmax)"
    notes: "Ratio stated by the campaign's technical report from the warm traces; copied, not recomputed here."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA attn*V' of one 2048-token prefill, column '1.4 tuned' (the 1.4 SARC branch build, which ran the SDPA cooperative-matrix kernels and the truncated softmax)"
    metric: gpu_time_ms_sdpa_attn_v_per_prefill_median_of_3
    value: 43.6
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 14 column '1.4 tuned'"
    baseline: "column '1.5 tuned' of the same row (separate claim)"
    notes: "Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. 1.4 build, not the release 1.5 kernels of this page. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA attn*V' of one 2048-token prefill, column '1.5 tuned' (dev/1.5 before the SDPA port, release 1.5's own SDPA kernels)"
    metric: gpu_time_ms_sdpa_attn_v_per_prefill_median_of_3
    value: 224.7
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 14 column '1.5 tuned'"
    notes: "Baseline measurement. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA attn*V' of one 2048-token prefill, 1.5 tuned minus 1.4 tuned as stated by the report"
    metric: gpu_time_ms_sdpa_attn_v_delta_as_stated_by_source
    value: 181.1
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 14 first column 'delta'"
    notes: "Difference stated by the gap report; copied, not recomputed here. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA QK^T' of one 2048-token prefill, column '1.4 tuned' (the 1.4 SARC branch build, which ran the SDPA cooperative-matrix kernels and the truncated softmax)"
    metric: gpu_time_ms_sdpa_qk_per_prefill_median_of_3
    value: 75.3
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 15 column '1.4 tuned'"
    baseline: "column '1.5 tuned' of the same row (separate claim)"
    notes: "Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. 1.4 build, not the release 1.5 kernels of this page. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA QK^T' of one 2048-token prefill, column '1.5 tuned' (dev/1.5 before the SDPA port, release 1.5's own SDPA kernels)"
    metric: gpu_time_ms_sdpa_qk_per_prefill_median_of_3
    value: 156.7
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 15 column '1.5 tuned'"
    notes: "Baseline measurement. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA QK^T' of one 2048-token prefill, 1.5 tuned minus 1.4 tuned as stated by the report"
    metric: gpu_time_ms_sdpa_qk_delta_as_stated_by_source
    value: 81.4
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 15 first column 'delta'"
    notes: "Difference stated by the gap report; copied, not recomputed here. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA softmax' of one 2048-token prefill, column '1.4 tuned' (the 1.4 SARC branch build, which ran the SDPA cooperative-matrix kernels and the truncated softmax)"
    metric: gpu_time_ms_sdpa_softmax_per_prefill_median_of_3
    value: 115.1
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 16 column '1.4 tuned'"
    baseline: "column '1.5 tuned' of the same row (separate claim)"
    notes: "Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. 1.4 build, not the release 1.5 kernels of this page. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA softmax' of one 2048-token prefill, column '1.5 tuned' (dev/1.5 before the SDPA port, release 1.5's own SDPA kernels)"
    metric: gpu_time_ms_sdpa_softmax_per_prefill_median_of_3
    value: 161.6
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 16 column '1.5 tuned'"
    notes: "Baseline measurement. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA softmax' of one 2048-token prefill, 1.5 tuned minus 1.4 tuned as stated by the report"
    metric: gpu_time_ms_sdpa_softmax_delta_as_stated_by_source
    value: 46.5
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 16 first column 'delta'"
    notes: "Difference stated by the gap report; copied, not recomputed here. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA subtotal' of one 2048-token prefill, column '1.4 tuned' (the 1.4 SARC branch build, which ran the SDPA cooperative-matrix kernels and the truncated softmax)"
    metric: gpu_time_ms_sdpa_subtotal_per_prefill_median_of_3
    value: 239.2
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 18 column '1.4 tuned'"
    baseline: "column '1.5 tuned' of the same row (separate claim)"
    notes: "Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. 1.4 build, not the release 1.5 kernels of this page. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA subtotal' of one 2048-token prefill, column '1.5 tuned' (dev/1.5 before the SDPA port, release 1.5's own SDPA kernels)"
    metric: gpu_time_ms_sdpa_subtotal_per_prefill_median_of_3
    value: 546.1
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 18 column '1.5 tuned'"
    notes: "Baseline measurement. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B 4w, family 'SDPA subtotal' of one 2048-token prefill, 1.5 tuned minus 1.4 tuned as stated by the report"
    metric: gpu_time_ms_sdpa_subtotal_delta_as_stated_by_source
    value: 306.9
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 18 first column 'delta'"
    notes: "Difference stated by the gap report; copied, not recomputed here. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.2 1B 4w export, whole model"
    shape: "Llama 3.2 1B 4w, 2048-token prefill, column '1.4 tuned' (1.4 SARC branch build)"
    metric: prefill_tokens_per_second_traced_build
    value: 2702
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 24 column '1.4 tuned'"
    notes: "Reference value of the 1.4 build. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.2 1B 4w export, whole model"
    shape: "Llama 3.2 1B 4w, 2048-token prefill, column '1.5 tuned' (dev/1.5 before the SDPA port)"
    metric: prefill_tokens_per_second_traced_build_median_of_3
    value: 1916
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 24 column '1.5 tuned'"
    notes: "Baseline measurement, stated with range 1916-1919. Before the port; ETDump GPU timestamps, median of 3 repeats, default DVFS. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B attention shape, SDPA microbench per call (--sdpa --regime=prefill, excludes kv-cache update), column '1.4' (1.4 SARC branch build)"
    metric: sdpa_microbench_ms_per_call
    value: 15.0
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 34 column '1.4'"
    baseline: "column '1.5' of the same row (separate claim)"
    notes: "Measured before the port, on the 1.4 build; not the release 1.5 kernels of this page. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B attention shape, SDPA microbench per call (--sdpa --regime=prefill, excludes kv-cache update), column '1.5' (dev/1.5 before the SDPA port)"
    metric: sdpa_microbench_ms_per_call
    value: 33.6
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 34 column '1.5'"
    notes: "Baseline measurement, before the port. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B attention shape, SDPA microbench per call (--sdpa --regime=prefill, excludes kv-cache update), column '1.4' (1.4 SARC branch build)"
    metric: sdpa_microbench_ms_per_call
    value: 14.6
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 35 column '1.4'"
    baseline: "column '1.5' of the same row (separate claim)"
    notes: "Measured before the port, on the 1.4 build; not the release 1.5 kernels of this page. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B attention shape, SDPA microbench per call (--sdpa --regime=prefill, excludes kv-cache update), column '1.5' (dev/1.5 before the SDPA port)"
    metric: sdpa_microbench_ms_per_call
    value: 52.7
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 35 column '1.5'"
    notes: "Baseline measurement, before the port. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B attention shape, SDPA microbench per call (--sdpa --regime=prefill, excludes kv-cache update), column '1.4' (1.4 SARC branch build)"
    metric: sdpa_microbench_ms_per_call
    value: 18.7
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 36 column '1.4'"
    baseline: "column '1.5' of the same row (separate claim)"
    notes: "Measured before the port, on the 1.4 build; not the release 1.5 kernels of this page. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B attention shape, SDPA microbench per call (--sdpa --regime=prefill, excludes kv-cache update), column '1.5' (dev/1.5 before the SDPA port)"
    metric: sdpa_microbench_ms_per_call
    value: 70.6
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 36 column '1.5'"
    notes: "Baseline measurement, before the port. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B, SDPA microbench prefill, sub-kernel 'qk', log column (M,K,N) = (2048,64,32), variant tiled (ET_VK_DISABLE_COOPMAT set)"
    metric: sdpa_microbench_mean_us_tiled_variant
    value: 9808.8
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 70 column mean_us"
    notes: "Baseline-side measurement (coopmat SDPA switched off), stdev 13.8 us, 3 warmup + 5 timed runs. Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B, SDPA microbench prefill, sub-kernel 'softmax', log column (M,K,N) = (2048,64,32), variant tiled (ET_VK_DISABLE_COOPMAT set)"
    metric: sdpa_microbench_mean_us_tiled_variant
    value: 7204.4
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 71 column mean_us"
    notes: "Baseline-side measurement (coopmat SDPA switched off), stdev 10.2 us, 3 warmup + 5 timed runs. Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B, SDPA microbench prefill, sub-kernel 'av', log column (M,K,N) = (2048,64,32), variant tiled (ET_VK_DISABLE_COOPMAT set)"
    metric: sdpa_microbench_mean_us_tiled_variant
    value: 14479.4
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 72 column mean_us"
    notes: "Baseline-side measurement (coopmat SDPA switched off), stdev 843.0 us, 3 warmup + 5 timed runs. Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 1B, SDPA microbench prefill, sub-kernel 'total', log column (M,K,N) = (2048,64,32), variant tiled (ET_VK_DISABLE_COOPMAT set)"
    metric: sdpa_microbench_mean_us_tiled_variant
    value: 31492.7
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 73 column mean_us"
    notes: "Baseline-side measurement (coopmat SDPA switched off), stdev 830.5 us, 3 warmup + 5 timed runs. Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.2 3B, SDPA microbench prefill, sub-kernel 'total', log column (M,K,N) = (2048,128,24), variant tiled (ET_VK_DISABLE_COOPMAT set)"
    metric: sdpa_microbench_mean_us_tiled_variant
    value: 49276.4
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 61 column mean_us"
    notes: "Baseline-side measurement (coopmat SDPA switched off), stdev 1018.2 us, 3 warmup + 5 timed runs. Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "Llama 3.1 8B, SDPA microbench prefill, sub-kernel 'total', log column (M,K,N) = (2048,128,32), variant tiled (ET_VK_DISABLE_COOPMAT set)"
    metric: sdpa_microbench_mean_us_tiled_variant
    value: 70356.3
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 49 column mean_us"
    notes: "Baseline-side measurement (coopmat SDPA switched off), stdev 1034.0 us, 3 warmup + 5 timed runs. Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.2 1B 4w export, whole model"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_2048.txt), default mode, after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 2694.74
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 7"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.2 1B 4w export, whole model"
    shape: "Llama 3.2 1B 4w, whole-model 2048-token prefill (prompt_2048.txt), tiled mode (ET_VK_FORCE_TILED_LINEAR=1: release 1.5 tiled linears, SARC SDPA kernels), after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 797.197
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 6"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.2 3B 4w export, whole model"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_2048.txt), default mode, after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 1138.41
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 17"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.2 3B 4w export, whole model"
    shape: "Llama 3.2 3B 4w, whole-model 2048-token prefill (prompt_2048.txt), tiled mode (ET_VK_FORCE_TILED_LINEAR=1: release 1.5 tiled linears, SARC SDPA kernels), after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 282.795
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 16"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.1 8B 4w export, whole model"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_2048.txt), default mode, after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 516.389
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 21"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.1 8B 4w export, whole model"
    shape: "Llama 3.1 8B 4w, whole-model 2048-token prefill (prompt_2048.txt), tiled mode (ET_VK_FORCE_TILED_LINEAR=1: release 1.5 tiled linears, SARC SDPA kernels), after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 113.734
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 20"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.2 1B 8da4w export, whole model"
    shape: "Llama 3.2 1B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), default mode, after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 2544.1
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 12"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.2 3B 8da4w export, whole model"
    shape: "Llama 3.2 3B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), default mode, after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 1048.11
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 19"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "Llama 3.1 8B 8da4w export, whole model"
    shape: "Llama 3.1 8B 8da4w, whole-model 2048-token prefill (prompt_2048.txt), default mode, after the SDPA port"
    metric: prefill_tokens_per_second_single_run
    value: 486.692
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 23"
    notes: "One llama_main run (not a median), --warmup, directory sdpa-e2e, ET_VK_SARC_UNVERIFIED=1. Whole model: SARC linear and SDPA rows together. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "SDPA correctness case tiny_gqa S=128 D=64 Q_H=2 KV_H=1, both cooperative-matrix kernels dispatched (qk_coopmat=yes av_coopmat=yes), 16384 elements compared against a CPU causal-attention reference"
    metric: sdpa_correctness_mismatch_count
    value: 0
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 19"
    notes: "PASSED; one recorded pass (directory sdpa2). Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "SDPA correctness case 1b_head_config S=128 D=64 Q_H=32 KV_H=8, both cooperative-matrix kernels dispatched (qk_coopmat=yes av_coopmat=yes), 262144 elements compared against a CPU causal-attention reference"
    metric: sdpa_correctness_mismatch_count
    value: 0
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 20"
    notes: "PASSED; one recorded pass (directory sdpa2). Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "SDPA correctness case tiny_gqa_s256 S=256 D=64 Q_H=2 KV_H=1, both cooperative-matrix kernels dispatched (qk_coopmat=yes av_coopmat=yes), 32768 elements compared against a CPU causal-attention reference"
    metric: sdpa_correctness_mismatch_count
    value: 0
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 21"
    notes: "PASSED; one recorded pass (directory sdpa2). Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
  - gpu: radeon-780m
    driver: "RADV Mesa 25.2.7"
    dtype: "fp16 attention tensors in buffer storage (kernel variants *_buffer_buffer_half, *_buffer_half)"
    shape: "SDPA correctness case 1b_head_config_s256 S=256 D=64 Q_H=32 KV_H=8, both cooperative-matrix kernels dispatched (qk_coopmat=yes av_coopmat=yes), 524288 elements compared against a CPU causal-attention reference"
    metric: sdpa_correctness_mismatch_count
    value: 0
    measured_at: '2026-09-27'
    source_id: meas-780m-sdpa-port
    source_locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 22"
    notes: "PASSED; one recorded pass (directory sdpa2). Log has no timestamp; date from the proposal heading. Driver version attributed from the install history, not recorded by the run."
---

# Prefill attention (SDPA) cooperative-matrix kernels on the Radeon 780M

Scope: one device (AMD Radeon 780M), one driver version (RADV Mesa 25.2.7), two measurement dates: 2026-09-27 (the SDPA port result set `meas-780m-sdpa-port`: gap analysis before the port, kernel-level correctness, SDPA microbenchmark, single-run end-to-end after the port) and 2026-09-28 (end-to-end campaign and its traces, `meas-780m-e2e-prefill`). The 2026-09-27 result set does not record a driver version; it is attributed from the device's package install history (see "How the driver version is known"). Nothing on this page is established for any other device, driver version or date. All evidence files are in the public repository https://github.com/sarc-acl/executorch at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`; paths below are relative to that repository's root.

Citation form: `[<source page id>: <path>#L<line>]` points at a line of a raw file listed in that source page's `raw_data`. `[code: <path>#L<line>]` points at shader or selection source in the same repository and commit that no measurement source page excerpts; such statements describe what the code says, not something measured. Citations of `meas-780m-sdpa-port` use the locator form of that page, `<path>, line <N>`. `meas-780m-sdpa-port` also excerpts much of the source cited below as `[code: ...]`: `table_amd.cpp` lines 78-96, `Select.h` lines 80-102, the QK^T shader header lines 9-67 and yaml lines 7-25 and 29-49, the attn·V shader lines 9-30 and 68-74 and yaml lines 7-46, the softmax yaml lines 7-29 and shader lines 13-16, 140-160 and 293-301.

Confidence note: the page stays `source-reported`. It now cites a first-party measurement page for the port (`meas-780m-sdpa-port`) next to the campaign page, and its `evidence_basis` would pass the validator's rule for `verified`. The label is not raised, because the measurement pages do not yet support the central claims about the two cooperative-matrix kernels directly enough:

- Kernel-level correctness with the kernels dispatched is one recorded pass (result directory `sdpa2`, 4 cases), and the harness source itself says "A single pass is NOT sufficient evidence for a coopmat shader" and asks to "rerun this flag repeatedly before trusting a pass" [meas-780m-sdpa-port: backends/vulkan/test/sarc_dev/test_llama_microbench.cpp, lines 55-59]. No repeat is recorded.
- The port result set holds no kernel-level time for `sarc_sdpa_qk_coopmat` or `sarc_sdpa_av_coopmat` on release 1.5: the coopmat-variant rows of its SDPA microbenchmark record 0.0 us for both (see "Measured results"). Kernel-level times of the shipped kernels come only from the single warm traces of the 2026-09-28 campaign.
- One next-token difference with these kernels in the path is unresolved (8B 8da4w, 1972-token check prompt, 2026-09-28; see "Correctness evidence").
- The driver version of the 2026-09-27 result set is attributed from the install history, not recorded by the runs.

## How the driver version is known

The 2026-09-27 result set does not record a driver version. Its own device line names the driver only as `radv phoenix`:

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

[meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 5]

The version `RADV Mesa 25.2.7` used for every 2026-09-27 number on this page is attributed from the package install history captured on the device on 2026-10-04 [meas-780m-sdpa-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, line 1]; it is not recorded by the runs:

```text
mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1 installed Fri 29 May 2026 10:08:07 PM PDT built Wed 25 Feb 2026 06:58:58 AM PST
```

[meas-780m-sdpa-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, line 4]

```text
2026-05-29T22:08:06-0700 SUBDEBUG Upgrade: mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1.x86_64
2026-05-29T22:10:09-0700 SUBDEBUG Upgraded: mesa-vulkan-drivers-25.0.7-6.el10_1.x86_64
```

[meas-780m-sdpa-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 12-13]

- The package that owns the RADV driver library is `mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1.x86_64` [meas-780m-sdpa-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, line 8].
- The quoted package-log query returns only the 2026-05-29 entries for the Mesa driver packages, with no later change [meas-780m-sdpa-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 10-14].
- Only the end-to-end directory `sdpa-e2e` has timestamps of its own, `Sun Sep 27 10:28:02 PM UTC 2026` to `Sun Sep 27 10:31:32 PM UTC 2026` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/env.txt, line 1; openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/done.txt, line 1]. The `sdpa` and `sdpa2` logs and the gap report take their date from the proposal heading `## Results (2026-09-27, Radeon 780M, release 1.5)` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, line 32] and the gap report title [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 1].

The 2026-09-28 campaign numbers carry their driver version through `meas-780m-e2e-prefill`; the attribution above is not applied to them.

## What the kernels compute

Three shaders replace release 1.5's prefill attention kernels on this device; the campaign's dispatch table lists them for the Radeon 780M as `sarc_sdpa_{qk,av}_coopmat` and `sarc_sdpa_attn_weights_softmax` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L345].

- **QK^T** (`sarc_sdpa_qk_coopmat`): per head, `attn[s, c] = inv_scale * sum_d Q[s, d] * K[c, d]`, then the causal mask sets `attn[s,c] = -inf where c > s + input_pos` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl#L12-L18]. Each output tile is classified as all masked, all visible or diagonal [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl#L34-L38]; a tile entirely above the diagonal is written as -inf and skips the multiply loop [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl#L31-L32].
- **attn·V** (`sarc_sdpa_av_coopmat`): per head, `out[s, d] = sum_c P[s, c] * V[c, d]`, as an "fp16 x fp16 -> fp32 MMA" [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl#L12, #L26]. K-chunks whose context indices lie beyond what any row of the tile can attend to are skipped [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl#L166-L171].
- **Softmax** (`sarc_sdpa_attn_weights_softmax`): a copy of release 1.5's LLM-mode softmax with a causal-tail truncation, "rows reduce only up to s + input_pos + 1 and write zeros to the masked tail without loading it" [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.yaml#L7-L9]. It is selected for devices with an SDPA row [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.yaml#L10].
- QK^T tile regions at the 2048-token prefill workload, from the shader header: with the 128x64 tile there are "16 M-tiles x 32 N-tiles = 512 workgroups", of which 240 are all masked ("early-out, no MMA"), 240 all visible and 32 diagonal, so "the all-visible path covers 240 of the 272 workgroups that actually execute (88%)" [meas-780m-sdpa-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl, lines 43-50]. These are counts stated in a code comment, not a measurement.
- QK^T store stride: the header records that `coopMatStore`'s stride operand "must not derive from a UBO value on one tested shader compiler"; with a UBO-derived stride the output was silently wrong ("measured: deterministic, ~3500-5800 wrong elements per case; with a compile-time stride, zero"), so the stride comes from a spec constant [meas-780m-sdpa-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl, lines 52-63]. The comment does not name the compiler or the device, so this is not established as a property of the 780M driver.
- attn·V declares an unused spec-constant slot (`gqa_group_size_unused`) because its node shares the spec-constant list with release 1.5's GQA decode shader [meas-780m-sdpa-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl, lines 68-74].
- The hooks act in LLM mode only and "do nothing on devices without an SDPA row" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 24-26].
- The KV-cache update is not replaced: both builds dispatch `sdpa_kv_cache_update_buffer_buffer_half` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L8, #L15].

## Shipped variants for the 780M

| Kernel | Dispatched name | Selection-table `TileDims` | Citation |
|---|---|---|---|
| QK^T | `sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half` | `{128, 64, 32, 2, 2, 64, 16, false}` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L7] [code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L84-L85] |
| attn·V | `sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half` | `{64, 64, 32, 2, 2, 64, 16, false}` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L6] [code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L92-L93] |
| softmax | `sarc_sdpa_attn_weights_softmax_buffer_half` | none (no tile) | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L5] |

- Naming: `sarc_sdpa_qk_coopmat_t<M>x<N>k<K>g<SGX><SGY>s<sub>` and likewise for AV [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.yaml#L10; backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.yaml#L10]. The `TileDims` fields are `m, n, k, sg_grid_x, sg_grid_y, subgroup_size, mma_m, csh_in_ash` [code: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h#L81-L88].
- QK^T yaml: `WG_TILE_M: 128`, `WG_TILE_N: 64`, `WG_TILE_K: 32`, `SG_GRID_X: 2`, `SG_GRID_Y: 2`, `SUBGROUP_SIZE: 64`, with `MMA_M`/`MMA_N`/`MMA_K` 16 [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.yaml#L23-L25, #L43-L49]. The reduction dimension is the head dimension D [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl#L20].
- attn·V yaml: `WG_TILE_M: 64`, `WG_TILE_N: 64`, `WG_TILE_K: 32`, `SG_GRID_X: 2`, `SG_GRID_Y: 2`, `SUBGROUP_SIZE: 64` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.yaml#L40-L46].
- Unlike the two linear kernels on this device, which pin the pipeline to subgroup size 32 [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L19-L21], these variants use `SUBGROUP_SIZE: 64`, which is the device's default subgroup size [meas-780m-vulkaninfo: sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, line 1232] (device-properties export dated `2026-9-1` in the file [meas-780m-vulkaninfo: sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, line 11220]).
- Both cooperative-matrix kernels are buffer-only (storage mask `kBufBuf`) [code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L86, #L94].
- Both kernels launch with local size `{WG_SIZE,1,1}`, with the query head taken from `gl_WorkGroupID.z` [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl#L65-L66; backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl#L28-L29].

### Shader excerpts

QK^T: whole-tile early-out for a tile entirely above the causal diagonal. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl#L205-L219` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
    if (tile_all_masked) {
        for (uint idx = gl_LocalInvocationID.x; idx < WG_TILE_M * WG_TILE_N;
             idx += WG_SIZE) {
            const uint ls = idx / WG_TILE_N;
            const uint lc = idx % WG_TILE_N;
            const uint gs = s_tile_base + ls;
            const uint gc = c_tile_base + lc;
            if (gs < uint(S) && gc < uint(context_len)) {
                t_attn_weights[(uint(q_h) * uint(S_aligned) + gs) *
                                   uint(aw_row_width) +
                               gc] = NEG_INF;
            }
        }
        return;
    }
```

QK^T: shared-memory tiles (Q staged `[s][d]`, K staged transposed `[d][c]`, and the scratch for the masked store). Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl#L130-L139` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
// fp16 shared tiles with skew padding. A = Q [s][d], B = K^T [d][c],
// C = scaled result [s][c] scratch for the masked scalar store.
const uint A_PAD = 8;
const uint B_PAD = 8;
const uint A_ROW = WG_TILE_K + A_PAD;
const uint B_ROW = WG_TILE_N + B_PAD;

shared float16_t Ash[WG_TILE_M * A_ROW];
shared float16_t Bsh[WG_TILE_K * B_ROW];
shared float16_t Csh[WG_TILE_M * WG_TILE_N];
```

attn·V: number of K-chunks that can contribute under the causal mask. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl#L166-L171` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
    // The highest context index any row in this M-tile can attend to:
    const uint max_c = a_row_base + WG_TILE_M - 1u + uint(input_pos);
    // Chunk `c` spans [c*WG_TILE_K, c*WG_TILE_K + WG_TILE_K), so it carries a
    // nonzero only when c*WG_TILE_K <= max_c.
    const uint useful_chunks =
        min(uint(num_k_chunks_arg), max_c / WG_TILE_K + 1u);
```

attn·V: fp32 accumulator matrices. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl#L103` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
coopmat<float, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator> result[MMAS_PER_SG_M][MMAS_PER_SG_N];
```

Softmax: truncated reduction length. Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.glsl#L156` at commit `ef079ac41fd09f01656e1ab46c87ca85be6c54ae`.

```glsl
  const int reduce_len = min(context_len, s + input_pos + 1);
```

These fragments are verbatim and depend on the surrounding files; they are not standalone shaders.

## How they are selected

- Two rows in the AMD table: `{"780m", amd_wave64, Op::kSdpaQk, ...}` and `{"780m", amd_wave64, Op::kSdpaAv, ...}`, both `Status::kVerified` [code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L81-L96], under the comment "SDPA prefill coopmat (QK^T, attn*V; the softmax truncation comes with them)" [code: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L78-L79]. `amd_wave64` is `d.is_amd && d.subgroup_size == 64` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L22-L24].
- The release status table lists "SDPA prefill" on the Radeon 780M as verified [meas-780m-4w-bootstrap: sarc/README.md#L80-L82]. The campaign report says attention is tuned only on the 780M in that release [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L450].
- `ET_VK_DISABLE_COOPMAT=1` sends SDPA to the upstream kernels [code: sarc/SWEEP-PARAMETERS.md#L155].
- Prompt length: for the 780M Llama 3.1 8B 8da4w cell on the 1972-token check prompt, the report gives the SARC path as "GEMM falls back to stock kernels; attention still uses SARC kernels" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L394]. That row covers this one cell; no source page holds a dispatch trace taken at 1972 tokens, so which attention kernels ran in the other five check cells is not recorded.

## Correctness evidence

### Kernel level (2026-09-27, `meas-780m-sdpa-port`)

`test_llama_microbench --sdpa-correctness-only` compares the cooperative-matrix kernels against "a CPU causal-attention reference, at small tile-aligned shapes" [meas-780m-sdpa-port: backends/vulkan/test/sarc_dev/test_llama_microbench.cpp, lines 51-59].

| Case (as logged) | qk / av coopmat dispatched | mismatches | verdict | Citation |
|---|---|---|---|---|
| `tiny_gqa S=128 D=64 Q_H=2 KV_H=1` | yes / yes | 0/16384 | PASSED | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 19] |
| `1b_head_config S=128 D=64 Q_H=32 KV_H=8` | yes / yes | 0/262144 | PASSED | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 20] |
| `tiny_gqa_s256 S=256 D=64 Q_H=2 KV_H=1` | yes / yes | 0/32768 | PASSED | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 21] |
| `1b_head_config_s256 S=256 D=64 Q_H=32 KV_H=8` | yes / yes | 0/524288 | PASSED | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 22] |

- The run is tier `all` with 4 cases [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, line 23]. The cases cover all three QK^T mask regions: `tiles=20 all_masked=4 all_visible=4 diagonal=12 overlap=0 exhaustive=yes all_three_covered=yes`, `boundaries_ok=yes` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, lines 17-18].
- The proposal summarizes this as "4/4 PASSED with 0 mismatches. Both coopmat kernels were dispatched in every case (`results/780m/sdpa2`)" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 34-35], and the selection-table comment repeats "SDPA correctness 4/4 (0 mismatches)" [meas-780m-sdpa-port: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 79-80].
- Another result directory, `sdpa`, shows the same four cases with `qk_coopmat=NO av_coopmat=NO`, 0 mismatches and the verdict `FAILED` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-correctness.log, lines 19-22]; the run summary reports `sdpa correctness rc=1` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 1]. In that directory the cooperative-matrix kernels were not dispatched, so it says nothing about them; the verdict reflects the missing dispatch. Neither `sdpa` nor `sdpa2` carries a timestamp, and the result set does not record their order.
- Only one pass with the kernels dispatched is recorded. The harness source warns that "A single pass is NOT sufficient evidence for a coopmat shader" [meas-780m-sdpa-port: backends/vulkan/test/sarc_dev/test_llama_microbench.cpp, lines 55-59].

### Model level, port result set (2026-09-27)

- Generated text of default mode versus tiled mode, Llama 3.2 1B: `SAME` on the check prompt and on the unaligned prompt, for both 4w and 8da4w [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 8-9, 13-14]. Both modes run the SARC attention kernels (`ET_VK_FORCE_TILED_LINEAR` "only affects the linears" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 28]), so this comparison tests the linear kernels against tiled linears with these attention kernels in place; it does not compare these attention kernels against release 1.5's.
- The proposal: "The next token matches tiled on the real-text prompt and on the 1792-token prompt, for both schemes." and "Decode works." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 46-47]. The decode runs returned `rc=0` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 10, 15]; decode "never considers coopmat (is_gemv)" [meas-780m-sdpa-port: backends/vulkan/test/sarc_dev/test_llama_microbench.cpp, lines 26-32], so decode does not exercise the two cooperative-matrix kernels.

### Model level, 2026-09-28 campaign

- 1972-token check prompt, sarc vs stock next token, 2026-09-28: SAME for 1B, 3B and 8B 4w and for 1B and 3B 8da4w; **DIFFER for 8B 8da4w** [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/tables.md#L8-L10, #L28-L30]. For the DIFFER cell (8B 8da4w) the report gives the SARC path at M = 1972 as "GEMM falls back to stock kernels; attention still uses SARC kernels" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L394], so in that cell the comparison exercises the SARC attention kernels; the evidence does not state which attention kernels ran in the other five check cells. For the DIFFER cell the probe records stock top-1 id 6062 and sarc top-1 id 45647 [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv#L13], and the report gives the logit margins between the two candidate tokens as −0.09 for stock and +0.50 for sarc [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L394]. It should not be described as a plain pass.
- Tile-aligned 2048-token real-text prompt, logits probe: top-1 token identical between stock and sarc in all six 780M cells [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv#L2, #L4, #L6, #L8, #L10, #L12]; logits are not bitwise identical (`bitwise_identical_top10` False on those rows).
- Clocks were not pinned [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L422].

## Measured results

The first two subsections are from the 2026-09-28 campaign's warm ETDump traces; the subsections from "Gap analysis" on are from the 2026-09-27 port result set. Campaign traces: one warm trace per cell and build, no repeat [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L76, #L445]. Baseline: the stock build (upstream release/1.5 @ `985c1ceccc` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L247]), whose attention kernels are `sdpa_compute_attn_weights_tiled`, `sdpa_compute_out_tiled` and `sdpa_attn_weights_softmax` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L12-L14]. Values are GPU milliseconds summed over all dispatches of the family in one 2048-token prefill. No ratio is computed by the wiki.

### Attention families, models exported with the 4w scheme

| Model | Family | sarc ms | sarc dispatches | stock ms | stock dispatches | Citation |
|---|---|---|---|---|---|---|
| Llama 3.2 1B | attention: QK^T | 75.223 | 16 x `sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half` | 156.725 | 16 x `sdpa_compute_attn_weights_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L4; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L7; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L17; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L13] |
| Llama 3.2 1B | attention: AV | 43.553 | 16 x `sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half` | 222.493 | 16 x `sdpa_compute_out_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L7; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L6; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L15; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L14] |
| Llama 3.2 1B | attention: softmax | 115.253 | 16 x `sarc_sdpa_attn_weights_softmax_buffer_half` | 161.568 | 16 x `sdpa_attn_weights_softmax_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L3; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L5; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L16; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L12] |
| Llama 3.2 3B | attention: QK^T | 161.669 | 28 x `sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half` | 567.461 | 28 x `sdpa_compute_attn_weights_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L54; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L35; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L67; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L41] |
| Llama 3.2 3B | attention: AV | 84.452 | 28 x `sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half` | 832.381 | 28 x `sdpa_compute_out_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L58; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L34; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L66; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L42] |
| Llama 3.2 3B | attention: softmax | 150.302 | 28 x `sarc_sdpa_attn_weights_softmax_buffer_half` | 206.803 | 28 x `sdpa_attn_weights_softmax_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L55; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L33; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L68; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L40] |
| Llama 3.1 8B | attention: QK^T | 236.855 | 32 x `sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half` | 881.685 | 32 x `sdpa_compute_attn_weights_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L106; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L63; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L118; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L69] |
| Llama 3.1 8B | attention: AV | 130.914 | 32 x `sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half` | 1314.39 | 32 x `sdpa_compute_out_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L109; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L62; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L117; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L70] |
| Llama 3.1 8B | attention: softmax | 229.259 | 32 x `sarc_sdpa_attn_weights_softmax_buffer_half` | 315.328 | 32 x `sdpa_attn_weights_softmax_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L107; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L61; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L120; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L68] |

Ratios stated by the report for these traces (4w), 1B / 3B / 8B: QK^T 2.08 / 3.51 / 3.72, AV 5.11 / 9.86 / 10.04, softmax 1.40 / 1.38 / 1.38 [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L227-L233]. For attention as a whole (QK^T, softmax, AV and KV update, [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L189]) the source gives "ATTN x" 2.29 / 4.00 / 4.17 [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/modelsize.txt#L5-L7]. The report's comment on the trend: from 3B to 8B "attention gains 4.0–4.2× and GEMMs 2.5×" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md#L235].

### Attention families, models exported with the 8da4w scheme

| Model | Family | sarc ms | sarc dispatches | stock ms | stock dispatches | Citation |
|---|---|---|---|---|---|---|
| Llama 3.2 1B | attention: QK^T | 75.085 | 16 x `sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half` | 156.762 | 16 x `sdpa_compute_attn_weights_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L29; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L21; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L43; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L27] |
| Llama 3.2 1B | attention: AV | 43.421 | 16 x `sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half` | 223.588 | 16 x `sdpa_compute_out_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L31; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L20; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L41; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L28] |
| Llama 3.2 1B | attention: softmax | 115.272 | 16 x `sarc_sdpa_attn_weights_softmax_buffer_half` | 161.686 | 16 x `sdpa_attn_weights_softmax_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L28; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L19; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L42; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L26] |
| Llama 3.2 3B | attention: QK^T | 161.108 | 28 x `sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half` | 567.719 | 28 x `sdpa_compute_attn_weights_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L79; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L49; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L93; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L55] |
| Llama 3.2 3B | attention: AV | 85.409 | 28 x `sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half` | 820.602 | 28 x `sdpa_compute_out_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L84; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L48; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L92; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L56] |
| Llama 3.2 3B | attention: softmax | 150.211 | 28 x `sarc_sdpa_attn_weights_softmax_buffer_half` | 206.358 | 28 x `sdpa_attn_weights_softmax_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L80; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L47; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L94; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L54] |
| Llama 3.1 8B | attention: QK^T | 237.046 | 32 x `sarc_sdpa_qk_coopmat_t128x64k32g22s64_buffer_buffer_half` | 885.397 | 32 x `sdpa_compute_attn_weights_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L131; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L77; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L144; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L83] |
| Llama 3.1 8B | attention: AV | 131.181 | 32 x `sarc_sdpa_av_coopmat_t64x64k32g22s64_buffer_buffer_half` | 1297.812 | 32 x `sdpa_compute_out_tiled_buffer_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L135; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L76; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L143; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L84] |
| Llama 3.1 8B | attention: softmax | 228.655 | 32 x `sarc_sdpa_attn_weights_softmax_buffer_half` | 314.731 | 32 x `sdpa_attn_weights_softmax_buffer_half` | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L132; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L75; openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv#L145; openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv#L82] |

"ATTN x" for the 8da4w cells is 2.30 / 3.97 / 4.14 for 1B / 3B / 8B [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/modelsize.txt#L8-L10].

### Gap analysis before the port (2026-09-27, 1.4 build versus release 1.5)

Source: `meas-780m-sdpa-port`, gap report. The symptom: "On release 1.5 the Radeon 780M ran 1B 4w prefill at 1930 tok/s, against 2702 on the 1.4 SARC branch, although the linear kernels matched." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 5-6]. The report's answer: "SDPA. On 1B 4w (2048-token prefill), SDPA accounts for 307 of the 309 ms per prefill (99 %)." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 3]. Method: "ETDump per-kernel GPU timestamps, last run of 2 per file, 3 repeats per cell (median, with min–max)", default DVFS [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 6, 8].

Llama 3.2 1B 4w, GPU ms per 2048-token prefill. "1.4 tuned" is the earlier 1.4 SARC branch build, which ran SDPA cooperative-matrix kernels and a causally truncated softmax; "1.5 tuned" is release 1.5 before the port, which had neither [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 8-12]. All deltas are the report's own.

| family | 1.4 tuned | 1.5 tuned | delta | 1.4 tiled | 1.5 tiled | delta | Citation |
|---|---|---|---|---|---|---|---|
| SDPA attn*V | 43.6 (coopmat) | 224.7 (tiled) | +181.1 | 43.6 | 219.6 | +176.0 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 14] |
| SDPA QK^T | 75.3 (coopmat) | 156.7 (tiled) | +81.4 | 75.2 | 157.3 | +82.1 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 15] |
| SDPA softmax | 115.1 | 161.6 | +46.5 | 115.3 | 161.5 | +46.3 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 16] |
| SDPA kv_cache_update | 5.3 | 3.1 | -2.2 | 5.3 | 3.1 | -2.2 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 17] |
| SDPA subtotal | 239.2 | 546.1 | +306.9 | 239.4 | 541.6 | +302.2 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 18] |
| linear 4w | 372.5 | 373.3 | +0.8 | 2173.5 | 2188.0 | +14.4 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 19] |
| GPU sum | 752.1 (752.1-752.3) | 1061.5 (1059.6-1062.8) | +309.4 | 2553.8 (2543-2561) | 2872.8 (2861-2890) | +319.0 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 22] |
| prefill tok/s | 2702 | 1916 (1916-1919) | | 799 (797-803) | 710 (706-713) | | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 24] |

- The 1.4 columns are a different software build on the same device. They are the reference the port aimed at, not measurements of the release 1.5 kernels on this page. The release 1.5 kernels' own per-family times are in the 2026-09-28 tables above.
- "Dispatch counts are identical in the two versions", and wall minus GPU sum is the same in both, "so 1.5 adds no CPU or submission overhead" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 26-27].
- What the report says recovers the gap: the attn·V cooperative-matrix kernel "~181 ms", the QK^T cooperative-matrix kernel "~81 ms" and the softmax causal-tail truncation "~46 ms" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 43-48]. Its expectation, marked as an inference: "Expected after porting: ~2705 tok/s tuned (inferred)." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 56].

SDPA microbench per call, before the port ("`--sdpa --regime=prefill`, excludes kv-cache update" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 30]):

| Model | 1.4 | 1.5 | predicted e2e delta (report) | observed (report) | Citation |
|---|---|---|---|---|---|
| Llama 3.2 1B | 15.0 ms | 33.6 ms | x16 layers = 0.30 s | 0.31 s | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 34] |
| Llama 3.2 3B | 14.6 ms | 52.7 ms | x28 = 1.07 s | 1.1 s | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 35] |
| Llama 3.1 8B | 18.7 ms | 70.6 ms | x32 = 1.66 s | 1.8 s | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 36] |

"The 3B/8B attribution is inferred from the microbench, not traced end to end. About 0.14 s of the 8B gap is unexplained." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 38-39].

### SDPA microbenchmark of the port result set (2026-09-27, tiled variant only)

Result directory `sdpa2`, "3 warmup + 5 timed runs per case" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 4]. The microbench toggles `ET_VK_DISABLE_COOPMAT` per case to measure a tiled and a coopmat variant [meas-780m-sdpa-port: backends/vulkan/test/sarc_dev/test_llama_microbench.cpp, lines 26-32]. Mean time in microseconds, tiled variant, prefill; the shape column is the log's `(M,K,N)` column as printed:

| Model | (M,K,N) | sub-kernel | mean_us | stdev | Citation |
|---|---|---|---|---|---|
| Llama 3.2 1B | (2048,64,32) | qk | 9808.8 | 13.8 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 70] |
| Llama 3.2 1B | (2048,64,32) | softmax | 7204.4 | 10.2 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 71] |
| Llama 3.2 1B | (2048,64,32) | av | 14479.4 | 843.0 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 72] |
| Llama 3.2 1B | (2048,64,32) | total | 31492.7 | 830.5 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 73] |
| Llama 3.2 3B | (2048,128,24) | total | 49276.4 | 1018.2 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 61] |
| Llama 3.1 8B | (2048,128,32) | total | 70356.3 | 1034.0 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 49] |

- These are release 1.5 SDPA times with the cooperative-matrix kernels switched off, that is, baseline-side numbers. The per-sub-kernel rows for 3B and 8B and the decode rows are on the source page.
- **No coopmat-variant time is cited.** In this log the coopmat-variant rows record 0.0 us for `qk` and for `av` (for 1B: [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, lines 74, 76]), so the log's coopmat "total" contains only the softmax time and its "speedup" lines are not SDPA speedups. They are deliberately left out.
- The log does not show a truncation effect on the softmax either (its coopmat-variant softmax row for 1B is on [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 75], next to the tiled row above); the softmax saving quoted on this page comes from the gap report (1.4 versus 1.5) and from the 2026-09-28 traces.

### End to end after the port (2026-09-27, single runs)

Result directory `sdpa-e2e`, 2048-token prefill tok/s, one `llama_main` run per cell (with `--warmup` in `sarc/tools/verify.sh` at the code commit, whose output formats the run matches; the result set does not record the command line [meas-780m-sdpa-port: sarc/tools/verify.sh, lines 86-106]), run environment `ET_VK_SARC_UNVERIFIED=1` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/env.txt, lines 1, 3-7]. "tiled" forces release 1.5's tiled linears; the SARC attention kernels run in both modes [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 28].

| Model | scheme | tiled linears | default | Citation |
|---|---|---|---|---|
| Llama 3.2 1B | 4w | 797.197 | 2694.74 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 6-7] |
| Llama 3.2 3B | 4w | 282.795 | 1138.41 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 16-17] |
| Llama 3.1 8B | 4w | 113.734 | 516.389 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 20-21] |
| Llama 3.2 1B | 8da4w | 2155.79 | 2544.1 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 11-12] |
| Llama 3.2 3B | 8da4w | 850.145 | 1048.11 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 18-19] |
| Llama 3.1 8B | 8da4w | 377.372 | 486.692 | [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 22-23] |

- The proposal's table gives the same cells rounded, next to its 1.4 reference columns (4w: 1.5 SARC 2695 / 1138 / 516 against 1.4 tuned 2702 / 1142 / 516; 8da4w: 2544 / 1048 / 487 against 2538 / 1055 / 486) [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 42-43], and concludes "The 780M is back at its 1.4 numbers (within 0.7 %)" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, line 45]. That percentage is the proposal's; the 1.4 runs are not part of the result set.
- The selection-table comment records the same outcome: "prefill back to the 1.4 level, 1B 4w 2695 vs 2702" [meas-780m-sdpa-port: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, line 80].

### End-to-end context

No single run toggles only these kernels end to end. Three separately measured 1B 4w figures bracket their introduction, on different builds, and are given without a ratio:

- 2026-09-27, SARC release export with the 4w linear row only (attention on release 1.5's own kernels): 1930.25 tok/s, single run [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-1b-4w-default.log#L5]. That change named the not-yet-ported SDPA cooperative-matrix kernels as the most likely cause of a gap to the earlier 1.4 branch, "Not yet confirmed" at the time [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md#L96-L97]. The gap report of the SDPA port later confirmed it (see "Gap analysis before the port").
- 2026-09-27, after the SDPA port, linear and SDPA rows together: 2694.74 tok/s, single run [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, line 7].
- 2026-09-28 campaign, tag `sarc/1.5-r2` with the linear and SDPA rows: median 2698.29 tok/s over 5 runs [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv#L2]. "The 780M numbers include attention" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md#L115-L116].

Per-model end-to-end medians of the campaign are on `kernel-linear-4w-780m` and `kernel-linear-8da4w-780m`.

## Limits of this page

- One device, one driver version, two consecutive days (2026-09-27 and 2026-09-28).
- For the 2026-09-27 result set the driver version is attributed from the device's package install history; the runs record only the driver name. Only its end-to-end directory has timestamps of its own.
- Kernel-level correctness of the two cooperative-matrix kernels is one recorded pass of 4 cases; the harness source asks for repeated passes.
- The port result set has no kernel-level time for the cooperative-matrix kernels on release 1.5 (its coopmat-variant rows record 0.0 us). The per-family times of the shipped kernels are from a single warm trace per cell on 2026-09-28; those traces carry no timestamp of their own, and their date and driver rest on the campaign report describing them as part of the campaign.
- The gap-report figures for "1.4" describe an earlier build with differently named kernels; they are reference values, not measurements of the kernels shipped in release 1.5.
- The 2026-09-27 end-to-end values are single runs and include the linear kernels; no run isolates the attention kernels end to end.
- The command lines of the 2026-09-27 runs are not recorded in the result set; the method is read from the verification script and the microbench source at the cited commit.
- Head counts and head dimensions of the model attention shapes are not stated in the campaign files; the port result set gives the microbench shape only as the log's `(M,K,N)` column.
