---
id: meas-780m-sdpa-port
title: "Radeon 780M SDPA prefill port to release 1.5: gap report, SDPA correctness, and end-to-end prefill with the SDPA rows (sarc-1.5-sdpa-port, 2026-09-27)"
source_category: measurement
architectures: [radeon-780m]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, decode, cooperative-matrix, causal-truncation, workgroup-tile-sizing, subgroup-size, storage-buffer, linear-4w, linear-8da4w, linear-8da4w-zpg, tiled-linear]
device: radeon-780m
driver: "RADV Mesa 25.2.7"
measured_at: '2026-09-27'
method: "Three kinds of first-party runs on the device, all recorded under openspec/changes/sarc-1.5-sdpa-port/results. (1) results/sdpa-gap-REPORT.md: ETDump per-kernel GPU timestamps of traced llama_main builds of the 1.4 branch and of dev/1.5 on a 2048-token prefill (last run of 2 per file, 3 repeats per cell, median with min-max), plus the SDPA microbench per call (--sdpa --regime=prefill). (2) results/780m/sdpa and results/780m/sdpa2: test_llama_microbench SDPA correctness cases (coopmat kernels vs a CPU causal-attention reference at small tile-aligned shapes) and the SDPA microbench (3 warmup + 5 timed runs per case, GPU timestamp queries). (3) results/780m/sdpa-e2e and results/780m/r4.out: the file names of sdpa-e2e and lines 3-23 and 25-30 of r4.out match the outputs of sarc/tools/verify.sh at the cited commit (the result set does not record the command line); r4.out lines 1-2 (SDPA correctness and SDPA prefill summaries) and the ALLDONE lines (24, 31) come from a step or wrapper that is not in that script. The result set does not record the order of the sdpa and sdpa2 directories. Steps of that script: linear correctness matrix, linear prefill microbench, then per model and scheme one llama_main process per mode with prompt_2048.txt, --max_new_tokens 1 --temperature 0 --warmup, mode tiled setting ET_VK_FORCE_TILED_LINEAR=1 and mode default not; for 1B also a check prompt and an unaligned prompt run once per mode without --warmup and compared as generated text, and a decode run with 32 new tokens; prefill tok/s is the PyTorchObserver prefill_token_per_sec of a single run. The driver version is attributed from the package install history captured on the device on 2026-10-04, not recorded by the runs. Line 2 of sdpa-e2e/env.txt (a host name) is not excerpted."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/proposal.md
    description: "Change proposal: motivation, ported kernels, results heading with the measurement date, end-to-end table"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md
    description: "Gap report dated 2026-09-27: ETDump per-family GPU ms per 1B prefill for the 1.4 and 1.5 builds, SDPA microbench per call, list of what recovers the gap"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out
    description: "Per-step summary lines: return codes, dispatched linear kernel names, prefill tok/s per model, scheme and mode, next-token comparisons, decode tok/s, production-diff verdicts"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-correctness.log
    description: "test_llama_microbench SDPA correctness log, result directory sdpa (coopmat not dispatched)"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-prefill.log
    description: "test_llama_microbench SDPA microbench log (RESULT lines, raw-results table), result directory sdpa (coopmat not dispatched)"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-prefill.json
    description: "JSON form of the SDPA microbench results, result directory sdpa (coopmat not dispatched)"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log
    description: "test_llama_microbench SDPA correctness log, result directory sdpa2 (coopmat dispatched)"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log
    description: "test_llama_microbench SDPA microbench log (RESULT lines, raw-results table), result directory sdpa2 (coopmat dispatched)"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.json
    description: "JSON form of the SDPA microbench results, result directory sdpa2 (coopmat dispatched)"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/env.txt
    description: "Start time (UTC), environment variables and binary hashes of the end-to-end verification run; line 2 is a host name and is not excerpted"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/done.txt
    description: "End time (UTC) of the end-to-end verification run"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/correctness.log
    description: "test_llama_microbench linear correctness matrix log"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-4w.log
    description: "test_llama_microbench 4w linear prefill microbench log"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-4w.json
    description: "JSON form of the 4w linear prefill microbench results"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-8da4w.log
    description: "test_llama_microbench 8da4w linear prefill microbench log"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-8da4w.json
    description: "JSON form of the 8da4w linear prefill microbench results"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-1b-4w-tiled.log
    description: "llama_main log of the 2048-token prefill run, model 1b, scheme 4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-1b-4w-default.log
    description: "llama_main log of the 2048-token prefill run, model 1b, scheme 4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-1b-8da4w-tiled.log
    description: "llama_main log of the 2048-token prefill run, model 1b, scheme 8da4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-1b-8da4w-default.log
    description: "llama_main log of the 2048-token prefill run, model 1b, scheme 8da4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-3b-4w-tiled.log
    description: "llama_main log of the 2048-token prefill run, model 3b, scheme 4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-3b-4w-default.log
    description: "llama_main log of the 2048-token prefill run, model 3b, scheme 4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-3b-8da4w-tiled.log
    description: "llama_main log of the 2048-token prefill run, model 3b, scheme 8da4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-3b-8da4w-default.log
    description: "llama_main log of the 2048-token prefill run, model 3b, scheme 8da4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-8b-4w-tiled.log
    description: "llama_main log of the 2048-token prefill run, model 8b, scheme 4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-8b-4w-default.log
    description: "llama_main log of the 2048-token prefill run, model 8b, scheme 4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-8b-8da4w-tiled.log
    description: "llama_main log of the 2048-token prefill run, model 8b, scheme 8da4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-8b-8da4w-default.log
    description: "llama_main log of the 2048-token prefill run, model 8b, scheme 8da4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/check-1b-4w-tiled.log
    description: "llama_main log of the check-prompt run, model 1b, scheme 4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/check-1b-4w-default.log
    description: "llama_main log of the check-prompt run, model 1b, scheme 4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/check-1b-8da4w-tiled.log
    description: "llama_main log of the check-prompt run, model 1b, scheme 8da4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/check-1b-8da4w-default.log
    description: "llama_main log of the check-prompt run, model 1b, scheme 8da4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/unaligned-1b-4w-tiled.log
    description: "llama_main log of the unaligned-prompt run, model 1b, scheme 4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/unaligned-1b-4w-default.log
    description: "llama_main log of the unaligned-prompt run, model 1b, scheme 4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/unaligned-1b-8da4w-tiled.log
    description: "llama_main log of the unaligned-prompt run, model 1b, scheme 8da4w, mode tiled"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/unaligned-1b-8da4w-default.log
    description: "llama_main log of the unaligned-prompt run, model 1b, scheme 8da4w, mode default"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/decode-1b-4w.log
    description: "llama_main log of the decode run (32 new tokens requested), model 1b, scheme 4w"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/decode-1b-8da4w.log
    description: "llama_main log of the decode run (32 new tokens requested), model 1b, scheme 8da4w"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: sarc/tools/verify.sh
    description: "On-device verification script: llama_main invocations, tiled vs default mode, output comparison, file names"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: sarc/README.md
    description: "SARC zone README; cited for the promotion checklist step that names verify.sh"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/test/sarc_dev/test_llama_microbench.cpp
    description: "Source of test_llama_microbench at the cited commit: suites, flags, RESULT line format, SDPA timing buckets"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp
    description: "Kernel selection table; rows with device substring 780m for Op::kSdpaQk and Op::kSdpaAv"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h
    description: "TileDims, StorageSet and Row definitions used by the table rows"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl
    description: "QK^T cooperative-matrix shader"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.yaml
    description: "QK^T shader variant parameters"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl
    description: "attn*V cooperative-matrix shader"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.yaml
    description: "attn*V shader variant parameters"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.glsl
    description: "attention-weight softmax shader with causal-tail truncation"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.yaml
    description: "softmax shader variant parameters"
  - locator: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt
    description: "Package install history and boot history captured on the device on 2026-10-04; establishes the Mesa version of the Vulkan driver package and that no later change is logged"
captured_at: '2026-10-04'
baseline: "Mode tiled: the same build with ET_VK_FORCE_TILED_LINEAR=1 (per results/sdpa-gap-REPORT.md this affects only the linears). The gap report and the proposal table also compare against the 1.4 SARC branch."
description: "Verbatim excerpts for the Radeon 780M SDPA port to release 1.5: the 1.5-vs-1.4 gap report, SDPA correctness and microbench logs, the end-to-end prefill, next-token and decode runs with the SDPA rows, the selection-table rows and shader headers of the dispatched kernels, and the install-history lines from which the driver version is attributed."
---

## Change, date and scope

Locator: `openspec/changes/sarc-1.5-sdpa-port/proposal.md`, lines 1-12

```text
# sarc-1.5-sdpa-port

## Why

On release 1.5 the Radeon 780M ran 1B 4w prefill at 1930 tok/s, against 2702 on the 1.4 SARC branch,
although the linear kernels matched.

ETDump per-kernel timing (`results/sdpa-gap-REPORT.md`) shows the cause. SDPA accounts for +307 of the
+309 ms per 1B prefill:
- the 1.4 branch ran SARC's SDPA coopmat kernels (AMD subgroup 64);
- 1.4 also ran a causally truncated softmax;
- release 1.5 has neither.
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/proposal.md`, lines 14-29

```text
## What

**Kernels** (`glsl/sarc/`):
- `sarc_sdpa_qk_coopmat` (t128x64k32g22s64) and `sarc_sdpa_av_coopmat` (t64x64k32g22s64), both from the
  1.4 branches.
- The attn*V kernel declares a placeholder in spec slot 2, so its node shares the spec-constant list with
  release 1.5's GQA decode shader.
- `sarc_sdpa_attn_weights_softmax`: release 1.5's LLM softmax plus the 1.4 causal-tail truncation. The
  upstream SPIR-V is unchanged.

**Hooks** (`impl/sarc/SdpaCoopmat.cpp` + `SDPA.cpp`):
- They cover the pickers, the work-group grids, the spec constants and the softmax name.
- LLM mode only; they do nothing on devices without an SDPA row.

**Rows:**
- 780M: verified.
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/proposal.md`, lines 32-48 (the heading on line 32 is the date source for the result directories `results/780m/sdpa/` and `results/780m/sdpa2/`, whose logs carry no timestamp of their own)

```text
## Results (2026-09-27, Radeon 780M, release 1.5)

**SDPA correctness** (`test_llama_microbench --sdpa-correctness-only`): 4/4 PASSED with 0 mismatches.
Both coopmat kernels were dispatched in every case (`results/780m/sdpa2`).

**End to end**, 2048-token prefill tok/s, 1B / 3B / 8B, with the 4w/8da4w rows and the SDPA rows
(`results/780m/sdpa-e2e`):

| scheme | 1.5 tiled | 1.5 SARC | 1.4 tiled | 1.4 tuned |
|---|---|---|---|---|
| 4w | 797 / 283 / 114 | 2695 / 1138 / 516 | 801 / 283 / 114 | 2702 / 1142 / 516 |
| 8da4w | 2156 / 850 / 377 | 2544 / 1048 / 487 | 2151 / 858 / 375 | 2538 / 1055 / 486 |

- The 780M is back at its 1.4 numbers (within 0.7 %).
- The next token matches tiled on the real-text prompt and on the 1792-token prompt, for both schemes.
- Decode works.
- 8da4w production-diff passes 6/6.
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/env.txt`, lines 1, 3-7 (line 2 is the output of `hostname` and is not excerpted)

```text
Sun Sep 27 10:28:02 PM UTC 2026
ETVK_DEVICE_INDEX=0
ET_VK_SARC_UNVERIFIED=1
eb1e8dd76c04a8cf32f420a7c7987f196672669563d5f87088aff2cee3a248f4  test_llama_microbench
547c2ced3d6b51f9c2657d9f85137d26861b8bf5ccddedbb8c903f2b4c7374f9  llama_main
7316cc3dd220104c07db8272a504759feabec77a8d15c2ec0cd2adb36d005372  libllama_runner.so
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/done.txt`, line 1

```text
Sun Sep 27 10:31:32 PM UTC 2026
```

## Environment / driver attribution

### (a) Device line recorded by the result set: driver named, no version

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log`, line 5 (the run records the device string `radv phoenix` and no Mesa version)

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.json`, lines 2-9

```text
  "schema": "test_llama_microbench.v1",
  "device": "amd radeon 780m graphics (radv phoenix)",
  "subgroup_size": 64,
  "timestamp_period_ns": 10,
  "cooperative_matrix": true,
  "warmup_runs": 3,
  "timed_runs": 5,
  "group_size": 128,
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log`, line 5

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-prefill.log`, line 5

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/correctness.log`, line 5

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-4w.log`, line 5

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-8da4w.log`, line 5

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

### (b) Package install history captured on the device: version and absence of later changes

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, line 1 (in this repository)

```text
# Captured 2026-10-04 on the Radeon 780M host. Commands and their verbatim output.
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 3-5 (in this repository; installed version and install time of the Vulkan driver package; the driver version `RADV Mesa 25.2.7` in this page's frontmatter is attributed from these install-history lines, it is not recorded by the run)

```text
$ rpm -q --qf "%{NAME}-%{VERSION}-%{RELEASE} installed %{INSTALLTIME:date} built %{BUILDTIME:date}\n" mesa-vulkan-drivers mesa-dri-drivers
mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1 installed Fri 29 May 2026 10:08:07 PM PDT built Wed 25 Feb 2026 06:58:58 AM PST
mesa-dri-drivers-25.2.7-4.el10.rocky.0.1 installed Fri 29 May 2026 10:08:06 PM PDT built Wed 25 Feb 2026 06:58:58 AM PST
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 7-8 (in this repository; package that owns the RADV driver library)

```text
$ rpm -qf /usr/lib64/libvulkan_radeon.so
mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1.x86_64
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 10-14 (in this repository; every package-log entry for the Mesa driver packages)

```text
$ grep -h -E "mesa-(vulkan|dri)-drivers" /var/log/dnf.rpm.log*
2026-05-29T22:08:06-0700 SUBDEBUG Upgrade: mesa-dri-drivers-25.2.7-4.el10.rocky.0.1.x86_64
2026-05-29T22:08:06-0700 SUBDEBUG Upgrade: mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1.x86_64
2026-05-29T22:10:09-0700 SUBDEBUG Upgraded: mesa-vulkan-drivers-25.0.7-6.el10_1.x86_64
2026-05-29T22:10:20-0700 SUBDEBUG Upgraded: mesa-dri-drivers-25.0.7-6.el10_1.x86_64
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 16-18 (in this repository; start of the retained package log)

```text
$ ls /var/log/dnf.rpm.log*   (oldest entry of the retained log)
/var/log/dnf.rpm.log
2026-02-23T19:29:04-0800 INFO --- logging initialized ---
```

### Boot history lines of the same file (`kernel_version` is not set in this page's frontmatter)

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 20-26 (in this repository; the lines carry no time zone and a truncated kernel string)

```text
$ last reboot | head -6
reboot   system boot  6.12.0-211.61.1. Thu Oct  1 09:52   still running
reboot   system boot  6.12.0-211.60.1. Sat Sep 26 21:45 - 09:52 (4+12:07)
reboot   system boot  6.12.0-211.58.1. Thu Sep 24 07:00 - 21:44 (2+14:44)
reboot   system boot  6.12.0-211.56.1. Wed Sep 23 20:59 - 06:59  (10:00)
reboot   system boot  6.12.0-211.56.1. Sat Sep 19 13:56 - crash (4+07:02)
reboot   system boot  6.12.0-211.55.1. Wed Sep 16 13:46 - 13:56 (3+00:10)
```

## Method: verification script whose output file names match results/780m/sdpa-e2e and whose summary-line formats match results/780m/r4.out lines 3-23 and 25-30

Locator: `sarc/tools/verify.sh`, lines 2-6

```text
# On-device verification of a SARC build, run ON THE GPU HOST. Produces the
# evidence a promotion PR needs: dispatched kernel names + kernel times
# (microbench), correctness, sampled production-diff, end-to-end prefill tok/s
# (tiled vs default), next-token equality vs tiled on a real-text and an
# unaligned prompt, and decode.
```

Locator: `sarc/tools/verify.sh`, lines 50-55

```text
export ETVK_DEVICE_INDEX=$DEV LD_LIBRARY_PATH=$DIR
{
  date -u; hostname; env | grep -E '^(ET_VK|ETVK)' | sort
  sha256sum test_llama_microbench llama_main libllama_runner.so 2>/dev/null
  command -v nvidia-smi >/dev/null && nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader
} > "$O/env.txt"
```

Locator: `sarc/tools/verify.sh`, lines 60-69

```text
if [[ -x ./test_llama_microbench ]]; then
  B=./test_llama_microbench
  timeout 1800 $B --correctness-only > "$O/correctness.log" 2>&1 9>&-
  echo "correctness rc=$? $(grep -o '\[correctness\].*' "$O/correctness.log" | tail -1)"
  for q in "${QS[@]}"; do
    timeout 3600 $B --linear --regime=prefill --scheme=$q --skip-correctness \
      --json-out="$O/linear-$q.json" > "$O/linear-$q.log" 2>&1 9>&-
    echo "linear $q rc=$? kernels: $(grep -o '"kernel": "[^"]*"' "$O/linear-$q.json" | sort | uniq -c | sed 's/"kernel": //' | tr -s ' ' | tr '\n' ';')"
  done
fi
```

Locator: `sarc/tools/verify.sh`, lines 71-78

```text
run() { # run <log> <pte> <tokenizer> <prompt> <new tokens> <env> [extra]
  env $6 timeout 1200 ./llama_main --model_path "$2" --tokenizer_path "$3" --prompt_file "$4" \
    --max_new_tokens "$5" --temperature 0 ${7:-} < /dev/null > "$O/$1" 2>&1 9>&-
}
tok() { grep -o '"prefill_token_per_sec":[0-9.]*' "$O/$1" | head -1 | cut -d: -f2; }
# Compare generated text only: drop runtime logs, stats and the [sarc_dev] banner.
same() { cmp -s <(grep -v 'PyTorchObserver\|^[IWE] \|^\[sarc_dev\]' "$O/$1") <(grep -v 'PyTorchObserver\|^[IWE] \|^\[sarc_dev\]' "$O/$2"); }
UNALIGNED=$(ls r*.txt 2>/dev/null | head -1)
```

Locator: `sarc/tools/verify.sh`, lines 86-106

```text
    MODES=(default); [[ $TILED == 1 ]] && MODES=(tiled default)
    for mode in "${MODES[@]}"; do
      E=""; [[ $mode == tiled ]] && E="ET_VK_FORCE_TILED_LINEAR=1"
      run "prefill-$m-$q-$mode.log" "$PTE" "$TK" prompt_2048.txt 1 "$E" --warmup
      echo "$m $q $mode prefill_tok_s=$(tok "prefill-$m-$q-$mode.log")"
      if [[ $m == 1b ]]; then
        run "check-$m-$q-$mode.log" "$PTE" "$TK" prompt_check.txt 1 "$E"
        [[ -n $UNALIGNED ]] && run "unaligned-$m-$q-$mode.log" "$PTE" "$TK" "$UNALIGNED" 1 "$E"
      fi
    done
    if [[ $m == 1b && $TILED == 1 ]]; then
      for k in check unaligned; do
        [[ -f $O/$k-$m-$q-tiled.log ]] || continue
        same "$k-$m-$q-tiled.log" "$k-$m-$q-default.log" && r=SAME || r=DIFFER
        echo "$m $q $k: default vs tiled output $r"
      done
    fi
    if [[ $m == 1b ]]; then
      run "decode-$m-$q.log" "$PTE" "$TK" prompt_2048.txt 32 ""
      echo "$m $q decode rc=$? $(grep -o '"generated_tokens":[0-9]*' "$O/decode-$m-$q.log") decode_tok_s=$(grep -o '"decode_token_per_sec":[0-9.]*' "$O/decode-$m-$q.log" | cut -d: -f2)"
    fi
```

Locator: `sarc/tools/verify.sh`, lines 110-120

```text
if [[ $PDIFF == 1 && -x ./test_llama_microbench ]]; then
  for md in llama-3.2-1b llama-3.2-3b llama-3.1-8b; do
    for q in "${QS[@]}"; do for st in buffer texture3d; do
      Z=""; [[ $q == 8da4w ]] && Z=--production-diff-nonzero-zp
      timeout 1800 ./test_llama_microbench --production-diff --production-diff-model=$md \
        --production-diff-op=$q --production-diff-storage=$st $Z > "$O/pdiff-$md-$q-$st.log" 2>&1 9>&-
      echo "pdiff $md $q $st rc=$? $(grep -E 'ALL PASSED|FAILED' "$O/pdiff-$md-$q-$st.log" | tail -1 | cut -c1-110)"
    done; done
  done
fi
date -u > "$O/done.txt"
```

Locator: `sarc/README.md`, lines 65-71

```text
3. Build with `build.sh`, then run `verify.sh` on the device. Required evidence:
   - the dispatched kernel names;
   - microbench correctness;
   - production-diff for 1B/3B/8B × buffer/texture3d, with nonzero zp for 8da4w;
   - e2e prefill tok/s (tiled vs default);
   - next token == tiled on the real-text and the unaligned prompt;
   - decode.
```

## Method: test_llama_microbench (source at the cited commit)

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp`, lines 26-32

```text
//   --sdpa      llama.custom_sdpa.default tiled-vs-coopmat at each model's
//               real attention shape (specs/010/021): prefill S=2048/ctx=3072
//               and decode S=1/ctx=3072/input_pos=3071 (the single most
//               expensive real decode step). SDPA coopmat is default-on in
//               this tree; ET_VK_DISABLE_COOPMAT is the kill switch, toggled
//               per-case here to measure both variants. Decode never
//               considers coopmat (is_gemv), so only tiled is measured there.
```

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp`, lines 37-59

```text
//   --sdpa-regions-only  enumerate the QK^T causal-mask tile grid for every
//                       SDPA correctness case and print each tile's region
//                       classification (all_masked / all_visible / diagonal),
//                       then report which of the three shader paths the gate
//                       actually reaches. Host-side only, no GPU. A path no
//                       case produces a tile for is UNCOVERED, however many
//                       times --sdpa-correctness-only passes.
//   --sdpa-tier=<fast|regions|all>
//                       which SDPA correctness tier to run; default all.
//                       "fast" = the original S=128 cases, the cheap
//                       post-edit pre-check. "regions" = the S=256 cases
//                       that put a tile in every QK^T mask region (4x the
//                       reference cost). "all" = the extended gate, which is
//                       what an accept decision requires.
//   --sdpa-correctness-only  run just the SDPA coopmat correctness cases
//                       (sdpa_compute_attn_weights_coopmat /
//                       sdpa_compute_out_coopmat vs. a CPU causal-attention
//                       reference, at small tile-aligned shapes -- see
//                       run_sdpa_correctness). A single pass is NOT
//                       sufficient evidence for a coopmat shader (the linear
//                       tile sweep found a tile that passed once and then
//                       failed 1-in-10 identical repeats, silently) -- rerun
//                       this flag repeatedly before trusting a pass.
```

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp`, lines 73-78

```text
// Output: one specs/021-schema "RESULT,..." line per case streamed during
// the run (shared 12 fields, then suite-specific extras -- linear/baseline:
// storage, M; sdpa: num_kv_heads, toggle), then a report: raw-results
// table, per-site WMMA speedups (coopmat vs tiled -- and vs the forced-tiled
// buffer baseline when --baseline ran), and geomeans per scheme/model/suite
// plus an overall geomean.
```

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp`, lines 164-171 (field order of a `RESULT,sdpa,...` line)

```text
void emit(const Record& r) {
  g_records.push_back(r);
  std::cout << "RESULT," << r.suite << "," << r.model << "," << r.scheme << ","
            << r.regime << ",";
  if (r.suite == "sdpa") {
    std::cout << r.op << "," << r.K << "," << r.N << "," << r.mean_us << ","
              << r.stdev_us << ",-1," << r.dispatch << ",SKIPPED," << r.kv
              << "," << r.variant << "\n";
```

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp`, lines 1241-1255

```text
// Runs one (model, coopmat-toggle, regime) case: builds
// llama.custom_sdpa.default directly via ComputeGraph (specs/010 research.md
// Decision 8: the TestCase framework has no SymInt support and this op
// family requires one). Returns the SDPA-compute-only GPU time split into
// qk (sdpa_compute_attn_weights_*) and av (sdpa_compute_out_*), plus their
// combined total -- excluding the kv-cache-update and softmax dispatches in
// between (unaccelerated, identical regardless of the coopmat toggle).
//
// SDPA coopmat is default-on in this tree; ET_VK_DISABLE_COOPMAT is the
// kill switch (read at shader-pick / graph-build time), so "tiled" here
// means running with it set. The KV cache buffer is always sized to
// `regime.context_len`, filled with random data BEFORE update_cache writes
// this step's new K/V at input_pos -- the shapes and access pattern are
// real even though the "history" isn't a genuine step-by-step prefill walk
// (only timing is measured here, not output correctness).
```

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp`, lines 1352-1379

```text
    float qk_time_us = 0.0f;
    float av_time_us = 0.0f;
    float softmax_time_us = 0.0f;
    last_dispatched.clear();
    for (const auto& r : shader_results) {
      last_dispatched.push_back(r.kernel_name);
      const uint64_t duration_ns = r.end_time_ns - r.start_time_ns;
      // Order matters: "sdpa_attn_weights_softmax" also contains
      // "sdpa_attn_weights", but NOT "sdpa_compute_attn_weights", so the qk
      // test below cannot capture it. Checked first regardless, so a future
      // rename cannot silently fold softmax into the qk bucket.
      if (r.kernel_name.find("softmax") != std::string::npos) {
        softmax_time_us += static_cast<float>(duration_ns) / 1000.0f;
      } else if (
          r.kernel_name.find("sdpa_compute_attn_weights") !=
              std::string::npos ||
          r.kernel_name.find("sarc_sdpa_qk") != std::string::npos) {
        qk_time_us += static_cast<float>(duration_ns) / 1000.0f;
      } else if (
          r.kernel_name.find("sdpa_compute_out") != std::string::npos ||
          r.kernel_name.find("sarc_sdpa_av") != std::string::npos) {
        av_time_us += static_cast<float>(duration_ns) / 1000.0f;
      }
    }
    qk_timings_us.push_back(qk_time_us);
    av_timings_us.push_back(av_time_us);
    softmax_timings_us.push_back(softmax_time_us);
    total_timings_us.push_back(qk_time_us + av_time_us + softmax_time_us);
```

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp`, lines 1463-1471

```text
        const bool qk_coopmat = (has_kernel_containing(
             coopmat.dispatched_kernels, "sdpa_compute_attn_weights_coopmat") ||
         has_kernel_containing(coopmat.dispatched_kernels, "sarc_sdpa_qk_coopmat"));
        const bool av_coopmat = (has_kernel_containing(
             coopmat.dispatched_kernels, "sdpa_compute_out_coopmat") ||
         has_kernel_containing(coopmat.dispatched_kernels, "sarc_sdpa_av_coopmat"));
        dispatch = (tiled_is_tiled && qk_coopmat && av_coopmat)
            ? "confirmed"
            : "fallback_tiled";
```

## Shipped kernels: selection rows for the Radeon 780M

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp`, lines 78-96

```text
    // Radeon 780M: SDPA prefill coopmat (QK^T, attn*V; the softmax truncation comes
    // with them). Verified on release 1.5 (sarc-1.5-sdpa-port): SDPA correctness
    // 4/4 (0 mismatches); prefill back to the 1.4 level, 1B 4w 2695 vs 2702.
    {"780m",
     amd_wave64,
     Op::kSdpaQk,
     "sarc_sdpa_qk_coopmat_t128x64k32g22s64",
     {128, 64, 32, 2, 2, 64, 16, false},
     kBufBuf,
     nullptr,
     Status::kVerified},
    {"780m",
     amd_wave64,
     Op::kSdpaAv,
     "sarc_sdpa_av_coopmat_t64x64k32g22s64",
     {64, 64, 32, 2, 2, 64, 16, false},
     kBufBuf,
     nullptr,
     Status::kVerified},
```

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp`, lines 42-45

```text
    // Radeon 780M 8da4w: zpg (4h4w activations), full A map. Verified on
    // release 1.5 (sarc-1.5-8da4w-port): kernels 0.992x of the 1.4 study;
    // with the SDPA rows, prefill 1B/3B/8B 2544/1048/487 tok/s (1.4:
    // 2538/1055/486).
```

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/Select.h`, lines 80-102 (field order of the brace-initialized tile dims and the storage-set bits used in the rows)

```text
struct TileDims {
  uint32_t m;
  uint32_t n;
  uint32_t k;
  uint32_t sg_grid_x;
  uint32_t sg_grid_y;
  uint32_t subgroup_size;
  uint32_t mma_m;
  bool csh_in_ash; // texture3d drain staged in Ash (no extra Csh LDS)
  bool csh_full = false; // texture3d drain stages the whole WG_TILE_M x WG_TILE_N tile
  bool csh_pool = false; // with csh_full: Ash, Bsh and the drain share one LDS pool
  uint32_t wg_size() const {
    return sg_grid_x * sg_grid_y * subgroup_size;
  }
};

// Storage combinations (IO_STORAGE x WEIGHT_STORAGE) a variant is built for;
// the yaml must contain <kernel_base>_<io>_<weight>_half for each set bit.
enum StorageSet : uint8_t {
  kTex3dTex2d = 1u << 0, // texture3d input/output, texture2d weight
  kBufTex2d = 1u << 1, // buffer input/output, texture2d weight
  kBufBuf = 1u << 2, // buffer input/output, buffer weight
};
```

## Shipped kernels: shader headers

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.glsl`, lines 9-67

```text
/*
 * KHR Cooperative Matrix SDPA QK^T kernel (prefill / LLM mode).
 *
 * Computes per head q_h:  attn[s, c] = inv_scale * sum_d Q[s, d] * K[c, d]
 *   Q = q_projected, DHSB [S, Q_H, D]   index (vec4 along d): (s*Q_H + q_h)*D4 + d4
 *   K = k_cache,     DHSB [context_len, KV_H, D]  index: (c*KV_H + kv_h)*D4 + d4
 *       (GQA: kv_h = q_h / (Q_H/KV_H))
 *   attn = attn_weights, head-contiguous [S_aligned, C4*4]
 *       scalar index: (q_h*S_aligned + s)*(C4*4) + c
 *   then the causal mask sets attn[s,c] = -inf where c > s + input_pos.
 *
 * Reduction dim is D (head_dim) -> num_k_chunks = D / WG_TILE_K (2 or 4).
 *
 * Two structural differences from coopmat_mm.glsl:
 *  1. K is consumed transposed (we need Q*K^T). Rather than a ColumnMajor load
 *     of packed shared memory, K is staged TRANSPOSED into an fp16 shared array
 *     laid out [d][c] (scatter on write, since native K has d contiguous), so
 *     the MMA loop reads it RowMajor exactly like A. Q is likewise staged into
 *     an fp16 [s][d] shared array.
 *  2. The causal mask cannot be applied to a coopmat accumulator (opaque
 *     lane->element mapping), so the scaled fp16 result is coopMatStore'd to a
 *     shared [s][c] scratch and then copied to global scalar-wise, applying the
 *     per-element mask. A whole-WG-tile that is entirely above the diagonal is
 *     written as -inf and skips the MMA loop (~halves prefill QK^T work).
 *
 * Each output tile is classified by where it sits relative to the causal
 * diagonal, and only the diagonal class needs the Csh round trip:
 *   all masked  : c_tile_base                  >  s_tile_base + WG_TILE_M - 1 + input_pos
 *   all visible : c_tile_base + WG_TILE_N - 1  <= s_tile_base + input_pos
 *   diagonal    : neither
 * Both whole-tile conditions holding at once would need
 * WG_TILE_M + WG_TILE_N < 2, and a tile matching neither falls through to the
 * per-element path, so the classes are exhaustive and disjoint.
 *
 * Region counts at the reported 2048-prefill workload (input_pos = 0, 128x64
 * tile, so 16 M-tiles x 32 N-tiles = 512 workgroups):
 *   240 all masked  (early-out, no MMA)
 *   240 all visible (direct coopMatStore to global: no Csh, no barrier, no
 *                    per-element mask)
 *    32 diagonal    (per-element mask via Csh)
 * 240 + 240 + 32 = 512, so the all-visible path covers 240 of the 272
 * workgroups that actually execute (88%).
 *
 * WHY THE ALL-VISIBLE STORE TAKES ITS STRIDE FROM A SPEC CONSTANT:
 * coopMatStore's stride operand must not derive from a UBO value on
 * one tested shader compiler -- the same miscompile sdpa_compute_out_coopmat.glsl
 * works around for its output stride. attn_weights' row width is
 * align_up_4(context_len), and context_len = input_pos + S comes from UBOs, so
 * using it directly produces silently wrong output (measured: deterministic,
 * ~3500-5800 wrong elements per case; with a compile-time stride, zero).
 * Unlike the linear kernel's out_N_arg, this width is NOT static -- it is
 * recomputed on every resize (SDPA.cpp resize_sdpa_attn_weights_node) -- so the
 * spec constant is a BAKED GUESS and the fast path is taken only when it
 * matches the live width. Otherwise control falls through to the Csh path,
 * whose stride is the compile-time WG_TILE_N and is therefore always safe.
 *
 * Dispatch: global {num_tiles_n*WG_SIZE, num_tiles_m, H_q}, local {WG_SIZE,1,1}.
 *   tileID = gl_WorkGroupID.xy (x->context, y->seq), q_h = gl_WorkGroupID.z.
 */
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.yaml`, lines 7-25

```text
# KHR Cooperative Matrix SDPA QK^T kernel (prefill / LLM). Buffer-only, fp16.
#
# Variant naming is tile-sweep-ready (ET_VK_SDPA_ATTN_COOPMAT_VARIANT,
# SDPA.cpp): sarc_sdpa_qk_coopmat_t<M>x<N>k<K>g<SGX><SGY>s<sub>,
# dispatched as ..._t..._buffer_buffer_half. Only the shipped default is
# built here -- a wider sweep was tried and found unvalidated (dozens of
# untested tiles), which doesn't belong in this branch (final shipped
# shaders only); run a real sweep on an experimental branch before adding
# more variants here.

sarc_sdpa_qk_coopmat:
  parameter_names_with_default_values:
    DTYPE: half
    PRECISION: highp
    IO_STORAGE: buffer
    K_CACHE_STORAGE: buffer
    MMA_M: 16
    MMA_N: 16
    MMA_K: 16
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_qk_coopmat.yaml`, lines 29-49

```text
    WG_TILE_M: 128
    WG_TILE_N: 64
    WG_TILE_K: 32
    SG_GRID_X: 2
    SG_GRID_Y: 2
    SUBGROUP_SIZE: 64
  generate_variant_forall:
    combination:
      parameter_names: [IO_STORAGE, K_CACHE_STORAGE]
      combos:
        - parameter_values: [buffer, buffer]
    DTYPE:
      - VALUE: half
  shader_variants:
    - NAME: sarc_sdpa_qk_coopmat_t128x64k32g22s64
      WG_TILE_M: 128
      WG_TILE_N: 64
      WG_TILE_K: 32
      SG_GRID_X: 2
      SG_GRID_Y: 2
      SUBGROUP_SIZE: 64
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl`, lines 9-30

```text
/*
 * KHR Cooperative Matrix SDPA attn*V kernel (prefill / LLM mode).
 *
 * Computes per head q_h:  out[s, d] = sum_c P[s, c] * V[c, d]
 *   P  = attn_weights (softmax output), head-contiguous [S_aligned, context_len]
 *        index (vec4 along c): (q_h * S_aligned + s) * C4 + c4
 *   V  = v_cache, DHSB [context_len, KV_H, D]
 *        index (vec4 along d): (c * KV_H + kv_h) * D4 + d4   (GQA: kv_h = q_h/(Q_H/KV_H))
 *   out= DHSB [S, Q_H, D]
 *        scalar index: (s * Q_H + q_h) * D + d
 *
 * This is the plain A*B coopmat MM (coopmat_mm.glsl) with three changes:
 *   - A (P) staging uses the head-contiguous row stride C4 + per-head base.
 *   - B (V) staging uses the DHSB head-interleaved row stride KV_H*D4 + base.
 *   - output coopMatStore uses the DHSB row stride (Q_H*D) so heads interleave;
 *     stride + head_dim are spec constants (one tested shader compiler
 *     miscompiles coopMatStore whose stride derives from a UBO value).
 * fp16 x fp16 -> fp32 MMA. No mask / no scale (softmax already applied).
 *
 * Dispatch: global {num_tiles_n*WG_SIZE, num_tiles_m, H_q}, local {WG_SIZE,1,1}.
 *   tileID = gl_WorkGroupID.xy, q_h = gl_WorkGroupID.z.
 */
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl`, lines 59-63 (the comment continues on lines 64-67, which are not excerpted)

```text
layout(local_size_x_id = 0, local_size_y_id = 1, local_size_z_id = 2) in;

// Spec constants. inv_scale occupies id 3 (UNUSED here — softmax already
// normalized; attn*V applies no scale) so this shader stays aligned with the
// decode _coop / tiled attn*V variants that share this node's fixed spec_vars
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.glsl`, lines 68-74

```text
${layout_declare_spec_const(C, "float", "inv_scale_unused", "1.0")}
// SARC: slot of release 1.5's GQA decode shader (group_size), which shares this
// node's spec-constant list; unused here.
${layout_declare_spec_const(C, "int", "gqa_group_size_unused", "1")}
${layout_declare_spec_const(C, "int", "num_k_chunks_arg", "0")}
${layout_declare_spec_const(C, "int", "out_row_stride_arg", "0")}
${layout_declare_spec_const(C, "int", "head_dim_arg", "0")}
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_av_coopmat.yaml`, lines 7-46

```text
# KHR Cooperative Matrix SDPA attn*V kernel (prefill / LLM). Buffer-only, fp16.
#
# Variant naming is tile-sweep-ready (ET_VK_SDPA_OUT_COOPMAT_VARIANT,
# SDPA.cpp): sarc_sdpa_av_coopmat_t<M>x<N>k<K>g<SGX><SGY>s<sub>,
# dispatched as ..._t..._buffer_buffer_half. Only the shipped default is
# built here -- a wider sweep was tried and found unvalidated (dozens of
# untested tiles), which doesn't belong in this branch (final shipped
# shaders only); run a real sweep on an experimental branch before adding
# more variants here.

sarc_sdpa_av_coopmat:
  parameter_names_with_default_values:
    DTYPE: half
    PRECISION: highp
    IO_STORAGE: buffer
    V_CACHE_STORAGE: buffer
    MMA_M: 16
    MMA_N: 16
    MMA_K: 16
    WG_TILE_M: 64
    WG_TILE_N: 64
    WG_TILE_K: 32
    SG_GRID_X: 2
    SG_GRID_Y: 2
    SUBGROUP_SIZE: 64
  generate_variant_forall:
    combination:
      parameter_names: [IO_STORAGE, V_CACHE_STORAGE]
      combos:
        - parameter_values: [buffer, buffer]
    DTYPE:
      - VALUE: half
  shader_variants:
    - NAME: sarc_sdpa_av_coopmat_t64x64k32g22s64
      WG_TILE_M: 64
      WG_TILE_N: 64
      WG_TILE_K: 32
      SG_GRID_X: 2
      SG_GRID_Y: 2
      SUBGROUP_SIZE: 64
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.yaml`, lines 7-29

```text
# SARC copy of release 1.5's sdpa_attn_weights_softmax (LLM mode only) with the
# causal-tail truncation of the 1.4 SARC branches (582ec23f95): rows reduce only
# up to s + input_pos + 1 and write zeros to the masked tail without loading it.
# Selected for devices with an SDPA row (impl/sarc/SdpaCoopmat.cpp).
sarc_sdpa_attn_weights_softmax:
  parameter_names_with_default_values:
    IN_DTYPE: float
    OUT_DTYPE: float
    STORAGE: texture3d
    MODE: llm
  generate_variant_forall:
    STORAGE:
      - VALUE: texture3d
      - VALUE: buffer
    combination:
      parameter_names: [IN_DTYPE, OUT_DTYPE]
      combos:
        - parameter_values: [float, float]
          suffix: float
        - parameter_values: [half, half]
          suffix: half
  shader_variants:
    - NAME: sarc_sdpa_attn_weights_softmax
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.glsl`, lines 13-16

```text
#define NUM_WORKERS_PER_WG 64

$if MODE == "llm":
  #define HAS_INPUT_POS
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.glsl`, lines 140-160

```text
  // Causal-mask truncation. In LLM mode the QK^T shader has already written
  // -inf to every element with c > s + input_pos, so for row s only the first
  // (s + input_pos + 1) columns carry information: a masked element
  // contributes exp(-inf - max) == 0 to the sum, cannot be the row max unless
  // the whole row is masked, and normalizes to exactly 0. All three passes can
  // therefore stop at reduce_len instead of context_len, which on a full
  // prefill halves the bytes read (the rows are a triangle, not a rectangle).
  //
  // The STORE still has to cover the whole context_len row: attn*V stages
  // every chunk with chunkK < context_len and multiplies it by V, so the
  // masked tail must be written as zero rather than left stale. Writing zero
  // is cheaper than reading + exp + writing, and needs no load.
  //
  // Fused mode has no input_pos and gets its mask from an attn_mask bias
  // instead, so no truncation is valid there.
#ifdef HAS_INPUT_POS
  const int reduce_len = min(context_len, s + input_pos + 1);
#else
  const int reduce_len = context_len;
#endif
  const int reduce_texel_len = div_up_4(reduce_len);
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.glsl`, lines 293-301

```text
  // Causally-masked tail: every element normalizes to exactly 0, so write zero
  // WITHOUT loading the input. This is the read the truncation saves in pass 3,
  // and the store attn*V depends on (it stages the whole context_len row).
  // Spread across all workers, unlike the straddling texel above.
  for (int c4 = reduce_texel_len + worker_id; c4 < context_texel_len;
       c4 += NUM_WORKERS_PER_WG) {
    store_attn_weights_softmax_c4(
        VEC4_T(0), c4, s, q_h, context_texel_len, attn_S, Q_H);
  }
```

## Gap analysis: results/sdpa-gap-REPORT.md (1.5 vs 1.4 on the Radeon 780M, before the port)

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md`, lines 1-8

```text
# 1.5 vs 1.4 end-to-end gap on the Radeon 780M (2026-09-27)

Answer: SDPA. On 1B 4w (2048-token prefill), SDPA accounts for 307 of the 309 ms per prefill (99 %).

Setup:
- Timing: ETDump per-kernel GPU timestamps, last run of 2 per file, 3 repeats per cell (median, with min–max).
- Builds: traced llama_main of 1.4 `yanwen/release14-quant-shaders-780m` e4786474b9, and of 1.5 `dev/1.5`.
- Device state: gpu-lab lock held; default DVFS; host idle apart from a user's `nvtop`.
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md`, lines 10-28

```text
## 1B per-family GPU ms per prefill (measured)

| family | 1.4 tuned | 1.5 tuned | delta | 1.4 tiled | 1.5 tiled | delta |
|---|---:|---:|---:|---:|---:|---:|
| SDPA attn*V | 43.6 (coopmat) | 224.7 (tiled) | +181.1 | 43.6 | 219.6 | +176.0 |
| SDPA QK^T | 75.3 (coopmat) | 156.7 (tiled) | +81.4 | 75.2 | 157.3 | +82.1 |
| SDPA softmax | 115.1 | 161.6 | +46.5 | 115.3 | 161.5 | +46.3 |
| SDPA kv_cache_update | 5.3 | 3.1 | -2.2 | 5.3 | 3.1 | -2.2 |
| SDPA subtotal | 239.2 | 546.1 | +306.9 | 239.4 | 541.6 | +302.2 |
| linear 4w | 372.5 | 373.3 | +0.8 | 2173.5 | 2188.0 | +14.4 |
| copy/view/slice | 59.2 | 60.8 | +1.6 | 59.6 | 61.1 | +1.5 |
| add/mul, silu, rms_norm, rope | 81.2 | 81.6 | +0.4 | 81.3 | 81.7 | +0.4 |
| GPU sum | 752.1 (752.1-752.3) | 1061.5 (1059.6-1062.8) | +309.4 | 2553.8 (2543-2561) | 2872.8 (2861-2890) | +319.0 |
| graph-execute wall | 754.2 | 1063.9 | +309.7 | 2559.3 | 2879.5 | +320.2 |
| prefill tok/s | 2702 | 1916 (1916-1919) | | 799 (797-803) | 710 (706-713) | |

- Dispatch counts are identical in the two versions.
- Wall minus GPU sum is ~2 ms (tuned) and ~6 ms (tiled) in both versions, so 1.5 adds no CPU or submission overhead.
- The gap is the same in tiled mode because 1.4 runs its SDPA coopmat there too; `ET_VK_FORCE_TILED_LINEAR` only affects the linears.
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md`, lines 30-39

```text
## SDPA microbench per call (measured; `--sdpa --regime=prefill`, excludes kv-cache update)

| model | 1.4 | 1.5 | predicted e2e delta | observed |
|---|---:|---:|---:|---:|
| 1B | 15.0 ms | 33.6 ms | x16 layers = 0.30 s | 0.31 s |
| 3B | 14.6 ms | 52.7 ms | x28 = 1.07 s | 1.1 s |
| 8B | 18.7 ms | 70.6 ms | x32 = 1.66 s | 1.8 s |

The 3B/8B attribution is inferred from the microbench, not traced end to end. About 0.14 s of the 8B gap
is unexplained.
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md`, lines 41-56

```text
## What recovers it (SARC 1.4 commits, none in upstream 1.5)

1. **attn*V coopmat**: `sdpa_compute_out_coopmat` (t64x64k32g22s64), ~181 ms. Commits:
   8be6567b3a, 7f43322dc1, 788617961a, be70eee109.
2. **QK^T coopmat**: `sdpa_compute_attn_weights_coopmat` (t128x64k32g22s64, fast path df5b8dca1b),
   ~81 ms.
3. **Softmax causal-tail truncation** (582ec23f95, an edit to upstream `sdpa_attn_weights_softmax.glsl`),
   ~46 ms.
4. **Supporting `SDPA.cpp` changes** (+310 lines):
   - gate `supports_cooperative_matrix() && subgroup_size()==64`, with the `ET_VK_DISABLE_COOPMAT` kill
     switch;
   - shape eligibility;
   - shader pick and workgroup sizes;
   - extra spec constants.

Expected after porting: ~2705 tok/s tuned (inferred).
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md`, lines 58-78

```text
## Port to dev/1.5 (estimate from reading the code; not attempted)

- **Shaders:** about 670 GLSL lines, nearly verbatim; `common.glslh` is unchanged from 1.4 to 1.5.
  About 250 lines of C++ need re-plumbing, plus the softmax edit.
- **Workgroup API (74d024cde):** the pickers must return `GlobalWorkGrid` / `LocalWorkGroup`.
  Mechanical.
- **Spec-constant conflict on the AV node (real):**
  - 1.5's GQA decode shader passes `{1.0, group_size}` to the same dynamic node.
  - The 1.4 AV coopmat uses slot 2 for `num_k_chunks_arg`.
  - The layouts must be unified.
- **`pick_sdpa_av_shader`:** a small textual conflict. Re-check 1.5's `align_up_4` padding against
  `aw_row_width`.
- **SARC zones:**
  - kernels go into `glsl/sarc` + `impl/sarc/SdpaCoopmat.cpp`;
  - rows for sdpa_qk and sdpa_av;
  - hook lines in `SDPA.cpp` (listed in `sarc/HOOKS`).
  - The softmax edit changes upstream SPIR-V for every device: ship it as a SARC copy selected by a row,
    or get owner sign-off as an upstreamable fix.
- **After porting:** run `--sdpa-correctness-only` (all tiers) and the unaligned-prompt e2e check.

Not checked: SDPA coopmat correctness on 1.5 (not ported).
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md`, line 80

```text
Raw data: `t14-*`, `t14b-*`, `t15-*` (ETDumps and logs), `summary.txt`, `analyze.py`, `run.sh`, `mb/`.
```

## Result directory results/780m/sdpa: SDPA correctness and prefill microbench, coopmat not dispatched

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-correctness.log`, lines 1-23

```text
[sarc_dev] overrides active: unverified=1 variant=

=== Compute Shader Performance Benchmark ===
Llama microbench (3.1 8B / 3.2 3B / 3.2 1B real e2e shapes; prefill 2048 / decode 1 @ ctx3072; linear group_size=128; 3 warmup + 5 timed runs per case)
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
----------------------------------------------------------------------
[sdpa-regions] tiny_gqa S=128 context_len=128 tile=128x64 num_tiles_m=1 num_tiles_n=2 tiles=2 all_masked=0 all_visible=0 diagonal=2 overlap=0
[sdpa-boundary] tiny_gqa m=0 last_visible=-1 first_diagonal=0 last_diagonal=1 first_masked=-1
[sdpa-regions] 1b_head_config S=128 context_len=128 tile=128x64 num_tiles_m=1 num_tiles_n=2 tiles=2 all_masked=0 all_visible=0 diagonal=2 overlap=0
[sdpa-boundary] 1b_head_config m=0 last_visible=-1 first_diagonal=0 last_diagonal=1 first_masked=-1
[sdpa-regions] tiny_gqa_s256 S=256 context_len=256 tile=128x64 num_tiles_m=2 num_tiles_n=4 tiles=8 all_masked=2 all_visible=2 diagonal=4 overlap=0
[sdpa-boundary] tiny_gqa_s256 m=0 last_visible=-1 first_diagonal=0 last_diagonal=1 first_masked=2
[sdpa-boundary] tiny_gqa_s256 m=1 last_visible=1 first_diagonal=2 last_diagonal=3 first_masked=-1
[sdpa-regions] 1b_head_config_s256 S=256 context_len=256 tile=128x64 num_tiles_m=2 num_tiles_n=4 tiles=8 all_masked=2 all_visible=2 diagonal=4 overlap=0
[sdpa-boundary] 1b_head_config_s256 m=0 last_visible=-1 first_diagonal=0 last_diagonal=1 first_masked=2
[sdpa-boundary] 1b_head_config_s256 m=1 last_visible=1 first_diagonal=2 last_diagonal=3 first_masked=-1
[sdpa-regions] TOTAL tiles=20 all_masked=4 all_visible=4 diagonal=12 overlap=0 exhaustive=yes all_three_covered=yes
[sdpa-regions] boundaries_ok=yes
[sdpa-correctness] tiny_gqa S=128 D=64 Q_H=2 KV_H=1 qk_coopmat=NO av_coopmat=NO mismatches=0/16384 FAILED
[sdpa-correctness] 1b_head_config S=128 D=64 Q_H=32 KV_H=8 qk_coopmat=NO av_coopmat=NO mismatches=0/262144 FAILED
[sdpa-correctness] tiny_gqa_s256 S=256 D=64 Q_H=2 KV_H=1 qk_coopmat=NO av_coopmat=NO mismatches=0/32768 FAILED
[sdpa-correctness] 1b_head_config_s256 S=256 D=64 Q_H=32 KV_H=8 qk_coopmat=NO av_coopmat=NO mismatches=0/524288 FAILED
[sdpa-correctness] tier=all cases_run=4
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-prefill.log`, lines 45-81

```text
suite     model         scheme regime   op     storage    variant  (M,K,N)                   mean_us     stdev   kern_us   GFLOP/s  dispatch
sdpa      llama-3.1-8b  -      prefill  qk     -          tiled    (2048,128,32)             25708.2      31.4         -         -  fallback_tiled
sdpa      llama-3.1-8b  -      prefill  softmax-          tiled    (2048,128,32)              7211.1      20.2         -         -  fallback_tiled
sdpa      llama-3.1-8b  -      prefill  av     -          tiled    (2048,128,32)             36387.3     895.5         -         -  fallback_tiled
sdpa      llama-3.1-8b  -      prefill  total  -          tiled    (2048,128,32)             69306.6     874.2         -         -  fallback_tiled
sdpa      llama-3.1-8b  -      prefill  qk     -          coopmat  (2048,128,32)                 0.0       0.0         -         -  fallback_tiled
sdpa      llama-3.1-8b  -      prefill  softmax-          coopmat  (2048,128,32)              7211.5      13.6         -         -  fallback_tiled
sdpa      llama-3.1-8b  -      prefill  av     -          coopmat  (2048,128,32)                 0.0       0.0         -         -  fallback_tiled
sdpa      llama-3.1-8b  -      prefill  total  -          coopmat  (2048,128,32)              7211.5      13.6         -         -  fallback_tiled
sdpa      llama-3.1-8b  -      decode   qk     -          tiled    (1,128,32)                 1112.9       2.8         -         -  not_applicable
sdpa      llama-3.1-8b  -      decode   softmax-          tiled    (1,128,32)                    7.8       0.1         -         -  not_applicable
sdpa      llama-3.1-8b  -      decode   av     -          tiled    (1,128,32)                  195.0      52.8         -         -  not_applicable
sdpa      llama-3.1-8b  -      decode   total  -          tiled    (1,128,32)                 1315.7      51.8         -         -  not_applicable
sdpa      llama-3.2-3b  -      prefill  qk     -          tiled    (2048,128,24)             19714.4      65.8         -         -  fallback_tiled
sdpa      llama-3.2-3b  -      prefill  softmax-          tiled    (2048,128,24)              5403.4      15.2         -         -  fallback_tiled
sdpa      llama-3.2-3b  -      prefill  av     -          tiled    (2048,128,24)             25979.7    1386.4         -         -  fallback_tiled
sdpa      llama-3.2-3b  -      prefill  total  -          tiled    (2048,128,24)             51097.5    1396.8         -         -  fallback_tiled
sdpa      llama-3.2-3b  -      prefill  qk     -          coopmat  (2048,128,24)                 0.0       0.0         -         -  fallback_tiled
sdpa      llama-3.2-3b  -      prefill  softmax-          coopmat  (2048,128,24)              5420.2      11.1         -         -  fallback_tiled
sdpa      llama-3.2-3b  -      prefill  av     -          coopmat  (2048,128,24)                 0.0       0.0         -         -  fallback_tiled
sdpa      llama-3.2-3b  -      prefill  total  -          coopmat  (2048,128,24)              5420.2      11.1         -         -  fallback_tiled
sdpa      llama-3.2-3b  -      decode   qk     -          tiled    (1,128,24)                  824.6       4.4         -         -  not_applicable
sdpa      llama-3.2-3b  -      decode   softmax-          tiled    (1,128,24)                    7.2       0.1         -         -  not_applicable
sdpa      llama-3.2-3b  -      decode   av     -          tiled    (1,128,24)                  169.7      34.3         -         -  not_applicable
sdpa      llama-3.2-3b  -      decode   total  -          tiled    (1,128,24)                 1001.6      37.9         -         -  not_applicable
sdpa      llama-3.2-1b  -      prefill  qk     -          tiled    (2048,64,32)               9795.3      25.3         -         -  fallback_tiled
sdpa      llama-3.2-1b  -      prefill  softmax-          tiled    (2048,64,32)               7213.2      10.9         -         -  fallback_tiled
sdpa      llama-3.2-1b  -      prefill  av     -          tiled    (2048,64,32)              14131.6     194.1         -         -  fallback_tiled
sdpa      llama-3.2-1b  -      prefill  total  -          tiled    (2048,64,32)              31140.1     197.5         -         -  fallback_tiled
sdpa      llama-3.2-1b  -      prefill  qk     -          coopmat  (2048,64,32)                  0.0       0.0         -         -  fallback_tiled
sdpa      llama-3.2-1b  -      prefill  softmax-          coopmat  (2048,64,32)               7210.2      27.4         -         -  fallback_tiled
sdpa      llama-3.2-1b  -      prefill  av     -          coopmat  (2048,64,32)                  0.0       0.0         -         -  fallback_tiled
sdpa      llama-3.2-1b  -      prefill  total  -          coopmat  (2048,64,32)               7210.2      27.4         -         -  fallback_tiled
sdpa      llama-3.2-1b  -      decode   qk     -          tiled    (1,64,32)                   212.3       0.8         -         -  not_applicable
sdpa      llama-3.2-1b  -      decode   softmax-          tiled    (1,64,32)                     8.7       0.1         -         -  not_applicable
sdpa      llama-3.2-1b  -      decode   av     -          tiled    (1,64,32)                    95.6       8.4         -         -  not_applicable
sdpa      llama-3.2-1b  -      decode   total  -          tiled    (1,64,32)                   316.6       8.1         -         -  not_applicable
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-prefill.log`, lines 83-95

```text
========== SDPA: coopmat (WMMA) vs tiled, prefill S=2048 ==========
model         sub        tiled_us  coopmat_us  speedup  dispatch
llama-3.1-8b  qk          25708.2         0.0        -  fallback_tiled
llama-3.1-8b  av          36387.3         0.0        -  fallback_tiled
llama-3.1-8b  total       69306.6      7211.5    9.61x  fallback_tiled
llama-3.2-3b  qk          19714.4         0.0        -  fallback_tiled
llama-3.2-3b  av          25979.7         0.0        -  fallback_tiled
llama-3.2-3b  total       51097.5      5420.2    9.43x  fallback_tiled
llama-3.2-1b  qk           9795.3         0.0        -  fallback_tiled
llama-3.2-1b  av          14131.6         0.0        -  fallback_tiled
llama-3.2-1b  total       31140.1      7210.2    4.32x  fallback_tiled

One or more cases crashed or did not dispatch the expected kernel (see dispatch column) -- do not trust their speedup numbers.
```

## Result directory results/780m/sdpa2: SDPA correctness, coopmat dispatched

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log`, lines 1-23

```text
[sarc_dev] overrides active: unverified=1 variant=

=== Compute Shader Performance Benchmark ===
Llama microbench (3.1 8B / 3.2 3B / 3.2 1B real e2e shapes; prefill 2048 / decode 1 @ ctx3072; linear group_size=128; 3 warmup + 5 timed runs per case)
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
----------------------------------------------------------------------
[sdpa-regions] tiny_gqa S=128 context_len=128 tile=128x64 num_tiles_m=1 num_tiles_n=2 tiles=2 all_masked=0 all_visible=0 diagonal=2 overlap=0
[sdpa-boundary] tiny_gqa m=0 last_visible=-1 first_diagonal=0 last_diagonal=1 first_masked=-1
[sdpa-regions] 1b_head_config S=128 context_len=128 tile=128x64 num_tiles_m=1 num_tiles_n=2 tiles=2 all_masked=0 all_visible=0 diagonal=2 overlap=0
[sdpa-boundary] 1b_head_config m=0 last_visible=-1 first_diagonal=0 last_diagonal=1 first_masked=-1
[sdpa-regions] tiny_gqa_s256 S=256 context_len=256 tile=128x64 num_tiles_m=2 num_tiles_n=4 tiles=8 all_masked=2 all_visible=2 diagonal=4 overlap=0
[sdpa-boundary] tiny_gqa_s256 m=0 last_visible=-1 first_diagonal=0 last_diagonal=1 first_masked=2
[sdpa-boundary] tiny_gqa_s256 m=1 last_visible=1 first_diagonal=2 last_diagonal=3 first_masked=-1
[sdpa-regions] 1b_head_config_s256 S=256 context_len=256 tile=128x64 num_tiles_m=2 num_tiles_n=4 tiles=8 all_masked=2 all_visible=2 diagonal=4 overlap=0
[sdpa-boundary] 1b_head_config_s256 m=0 last_visible=-1 first_diagonal=0 last_diagonal=1 first_masked=2
[sdpa-boundary] 1b_head_config_s256 m=1 last_visible=1 first_diagonal=2 last_diagonal=3 first_masked=-1
[sdpa-regions] TOTAL tiles=20 all_masked=4 all_visible=4 diagonal=12 overlap=0 exhaustive=yes all_three_covered=yes
[sdpa-regions] boundaries_ok=yes
[sdpa-correctness] tiny_gqa S=128 D=64 Q_H=2 KV_H=1 qk_coopmat=yes av_coopmat=yes mismatches=0/16384 PASSED
[sdpa-correctness] 1b_head_config S=128 D=64 Q_H=32 KV_H=8 qk_coopmat=yes av_coopmat=yes mismatches=0/262144 PASSED
[sdpa-correctness] tiny_gqa_s256 S=256 D=64 Q_H=2 KV_H=1 qk_coopmat=yes av_coopmat=yes mismatches=0/32768 PASSED
[sdpa-correctness] 1b_head_config_s256 S=256 D=64 Q_H=32 KV_H=8 qk_coopmat=yes av_coopmat=yes mismatches=0/524288 PASSED
[sdpa-correctness] tier=all cases_run=4
```

## Result directory results/780m/sdpa2: SDPA microbench RESULT lines

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log`, lines 1-4

```text
[sarc_dev] overrides active: unverified=1 variant=

=== Compute Shader Performance Benchmark ===
Llama microbench (3.1 8B / 3.2 3B / 3.2 1B real e2e shapes; prefill 2048 / decode 1 @ ctx3072; linear group_size=128; 3 warmup + 5 timed runs per case)
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log`, lines 7-42

```text
RESULT,sdpa,llama-3.1-8b,,prefill,qk,128,32,25697.8,34.0794,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.1-8b,,prefill,softmax,128,32,7212.21,16.8627,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.1-8b,,prefill,av,128,32,37446.2,1057.16,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.1-8b,,prefill,total,128,32,70356.3,1034.04,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.1-8b,,prefill,qk,128,32,0,0,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.1-8b,,prefill,softmax,128,32,7238.06,46.174,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.1-8b,,prefill,av,128,32,0,0,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.1-8b,,prefill,total,128,32,7238.06,46.174,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.1-8b,,decode,qk,128,32,1111.77,4.32596,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.1-8b,,decode,softmax,128,32,7.496,0.0357771,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.1-8b,,decode,av,128,32,196.288,60.0947,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.1-8b,,decode,total,128,32,1315.55,59.5126,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-3b,,prefill,qk,128,24,19714.4,63.0421,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-3b,,prefill,softmax,128,24,5413.94,22.7319,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-3b,,prefill,av,128,24,24148.1,1060.32,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-3b,,prefill,total,128,24,49276.4,1018.24,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-3b,,prefill,qk,128,24,0,0,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.2-3b,,prefill,softmax,128,24,5427.04,48.0327,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.2-3b,,prefill,av,128,24,0,0,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.2-3b,,prefill,total,128,24,5427.04,48.0327,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.2-3b,,decode,qk,128,24,820.672,2.63384,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-3b,,decode,softmax,128,24,7.008,0.12775,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-3b,,decode,av,128,24,151.744,6.25675,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-3b,,decode,total,128,24,979.424,8.46301,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-1b,,prefill,qk,64,32,9808.83,13.7901,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-1b,,prefill,softmax,64,32,7204.42,10.21,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-1b,,prefill,av,64,32,14479.4,842.992,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-1b,,prefill,total,64,32,31492.7,830.484,-1,confirmed,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-1b,,prefill,qk,64,32,0,0,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.2-1b,,prefill,softmax,64,32,7202.67,18.9718,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.2-1b,,prefill,av,64,32,0,0,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.2-1b,,prefill,total,64,32,7202.67,18.9718,-1,confirmed,SKIPPED,8,coopmat
RESULT,sdpa,llama-3.2-1b,,decode,qk,64,32,210.36,5.9547,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-1b,,decode,softmax,64,32,8.424,0.1004,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-1b,,decode,av,64,32,91.4,4.21493,-1,not_applicable,SKIPPED,8,tiled
RESULT,sdpa,llama-3.2-1b,,decode,total,64,32,310.184,9.03551,-1,not_applicable,SKIPPED,8,tiled
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log`, lines 44-81

```text
==================== RAW RESULTS ====================
suite     model         scheme regime   op     storage    variant  (M,K,N)                   mean_us     stdev   kern_us   GFLOP/s  dispatch
sdpa      llama-3.1-8b  -      prefill  qk     -          tiled    (2048,128,32)             25697.8      34.1         -         -  confirmed
sdpa      llama-3.1-8b  -      prefill  softmax-          tiled    (2048,128,32)              7212.2      16.9         -         -  confirmed
sdpa      llama-3.1-8b  -      prefill  av     -          tiled    (2048,128,32)             37446.2    1057.2         -         -  confirmed
sdpa      llama-3.1-8b  -      prefill  total  -          tiled    (2048,128,32)             70356.3    1034.0         -         -  confirmed
sdpa      llama-3.1-8b  -      prefill  qk     -          coopmat  (2048,128,32)                 0.0       0.0         -         -  confirmed
sdpa      llama-3.1-8b  -      prefill  softmax-          coopmat  (2048,128,32)              7238.1      46.2         -         -  confirmed
sdpa      llama-3.1-8b  -      prefill  av     -          coopmat  (2048,128,32)                 0.0       0.0         -         -  confirmed
sdpa      llama-3.1-8b  -      prefill  total  -          coopmat  (2048,128,32)              7238.1      46.2         -         -  confirmed
sdpa      llama-3.1-8b  -      decode   qk     -          tiled    (1,128,32)                 1111.8       4.3         -         -  not_applicable
sdpa      llama-3.1-8b  -      decode   softmax-          tiled    (1,128,32)                    7.5       0.0         -         -  not_applicable
sdpa      llama-3.1-8b  -      decode   av     -          tiled    (1,128,32)                  196.3      60.1         -         -  not_applicable
sdpa      llama-3.1-8b  -      decode   total  -          tiled    (1,128,32)                 1315.6      59.5         -         -  not_applicable
sdpa      llama-3.2-3b  -      prefill  qk     -          tiled    (2048,128,24)             19714.4      63.0         -         -  confirmed
sdpa      llama-3.2-3b  -      prefill  softmax-          tiled    (2048,128,24)              5413.9      22.7         -         -  confirmed
sdpa      llama-3.2-3b  -      prefill  av     -          tiled    (2048,128,24)             24148.1    1060.3         -         -  confirmed
sdpa      llama-3.2-3b  -      prefill  total  -          tiled    (2048,128,24)             49276.4    1018.2         -         -  confirmed
sdpa      llama-3.2-3b  -      prefill  qk     -          coopmat  (2048,128,24)                 0.0       0.0         -         -  confirmed
sdpa      llama-3.2-3b  -      prefill  softmax-          coopmat  (2048,128,24)              5427.0      48.0         -         -  confirmed
sdpa      llama-3.2-3b  -      prefill  av     -          coopmat  (2048,128,24)                 0.0       0.0         -         -  confirmed
sdpa      llama-3.2-3b  -      prefill  total  -          coopmat  (2048,128,24)              5427.0      48.0         -         -  confirmed
sdpa      llama-3.2-3b  -      decode   qk     -          tiled    (1,128,24)                  820.7       2.6         -         -  not_applicable
sdpa      llama-3.2-3b  -      decode   softmax-          tiled    (1,128,24)                    7.0       0.1         -         -  not_applicable
sdpa      llama-3.2-3b  -      decode   av     -          tiled    (1,128,24)                  151.7       6.3         -         -  not_applicable
sdpa      llama-3.2-3b  -      decode   total  -          tiled    (1,128,24)                  979.4       8.5         -         -  not_applicable
sdpa      llama-3.2-1b  -      prefill  qk     -          tiled    (2048,64,32)               9808.8      13.8         -         -  confirmed
sdpa      llama-3.2-1b  -      prefill  softmax-          tiled    (2048,64,32)               7204.4      10.2         -         -  confirmed
sdpa      llama-3.2-1b  -      prefill  av     -          tiled    (2048,64,32)              14479.4     843.0         -         -  confirmed
sdpa      llama-3.2-1b  -      prefill  total  -          tiled    (2048,64,32)              31492.7     830.5         -         -  confirmed
sdpa      llama-3.2-1b  -      prefill  qk     -          coopmat  (2048,64,32)                  0.0       0.0         -         -  confirmed
sdpa      llama-3.2-1b  -      prefill  softmax-          coopmat  (2048,64,32)               7202.7      19.0         -         -  confirmed
sdpa      llama-3.2-1b  -      prefill  av     -          coopmat  (2048,64,32)                  0.0       0.0         -         -  confirmed
sdpa      llama-3.2-1b  -      prefill  total  -          coopmat  (2048,64,32)               7202.7      19.0         -         -  confirmed
sdpa      llama-3.2-1b  -      decode   qk     -          tiled    (1,64,32)                   210.4       6.0         -         -  not_applicable
sdpa      llama-3.2-1b  -      decode   softmax-          tiled    (1,64,32)                     8.4       0.1         -         -  not_applicable
sdpa      llama-3.2-1b  -      decode   av     -          tiled    (1,64,32)                    91.4       4.2         -         -  not_applicable
sdpa      llama-3.2-1b  -      decode   total  -          tiled    (1,64,32)                   310.2       9.0         -         -  not_applicable
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log`, lines 83-96

```text
========== SDPA: coopmat (WMMA) vs tiled, prefill S=2048 ==========
model         sub        tiled_us  coopmat_us  speedup  dispatch
llama-3.1-8b  qk          25697.8         0.0        -  confirmed
llama-3.1-8b  av          37446.2         0.0        -  confirmed
llama-3.1-8b  total       70356.3      7238.1    9.72x  confirmed
llama-3.2-3b  qk          19714.4         0.0        -  confirmed
llama-3.2-3b  av          24148.1         0.0        -  confirmed
llama-3.2-3b  total       49276.4      5427.0    9.08x  confirmed
llama-3.2-1b  qk           9808.8         0.0        -  confirmed
llama-3.2-1b  av          14479.4         0.0        -  confirmed
llama-3.2-1b  total       31492.7      7202.7    4.37x  confirmed
sdpa geomean (total, all models): 7.28x

OVERALL WMMA geomean (3 sites: linear prefill shapes + sdpa prefill totals): 7.28x
```

## results/780m/r4.out: per-step summary lines

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out`, lines 1-31

```text
sdpa correctness rc=1 [sdpa-correctness] tiny_gqa_s256 S=256 D=64 Q_H=2 KV_H=1 qk_coopmat=NO av_coopmat=NO mismatches=0/32768 FAILED [sdpa-correctness] 1b_head_config_s256 S=256 D=64 Q_H=32 KV_H=8 qk_coopmat=NO av_coopmat=
sdpa prefill rc=1 kernels: 
correctness rc=0 
linear 4w rc=1 kernels:  12 "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half"; 12 "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half";
linear 8da4w rc=1 kernels:  12 "sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half"; 12 "sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half";
1b 4w tiled prefill_tok_s=797.197
1b 4w default prefill_tok_s=2694.74
1b 4w check: default vs tiled output SAME
1b 4w unaligned: default vs tiled output SAME
1b 4w decode rc=0 "generated_tokens":31 decode_tok_s=70.7763
1b 8da4w tiled prefill_tok_s=2155.79
1b 8da4w default prefill_tok_s=2544.1
1b 8da4w check: default vs tiled output SAME
1b 8da4w unaligned: default vs tiled output SAME
1b 8da4w decode rc=0 "generated_tokens":31 decode_tok_s=71.1009
3b 4w tiled prefill_tok_s=282.795
3b 4w default prefill_tok_s=1138.41
3b 8da4w tiled prefill_tok_s=850.145
3b 8da4w default prefill_tok_s=1048.11
8b 4w tiled prefill_tok_s=113.734
8b 4w default prefill_tok_s=516.389
8b 8da4w tiled prefill_tok_s=377.372
8b 8da4w default prefill_tok_s=486.692
ALLDONE
pdiff llama-3.2-1b 8da4w buffer rc=0 [production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
pdiff llama-3.2-1b 8da4w texture3d rc=0 [production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
pdiff llama-3.2-3b 8da4w buffer rc=0 [production-diff] ALL PASSED (llama-3.2-3b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
pdiff llama-3.2-3b 8da4w texture3d rc=0 [production-diff] ALL PASSED (llama-3.2-3b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
pdiff llama-3.1-8b 8da4w buffer rc=0 [production-diff] ALL PASSED (llama-3.1-8b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
pdiff llama-3.1-8b 8da4w texture3d rc=0 [production-diff] ALL PASSED (llama-3.1-8b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
ALLDONE
```

## Result directory results/780m/sdpa-e2e: 2048-token prefill, one PyTorchObserver line per run

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-1b-4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":797.197,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548154248,"model_load_end_ms":1790548154539,"inference_start_ms":1790548157146,"inference_end_ms":1790548159715,"model_execution_start_ms":1790548157149,"model_execution_end_ms":1790548159714,"prompt_eval_end_ms":1790548159715,"first_token_ms":1790548159715,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2565,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-1b-4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":2694.74,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548165677,"model_load_end_ms":1790548166039,"inference_start_ms":1790548166838,"inference_end_ms":1790548167598,"model_execution_start_ms":1790548166841,"model_execution_end_ms":1790548167597,"prompt_eval_end_ms":1790548167598,"first_token_ms":1790548167598,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":756,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-1b-8da4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":2155.79,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548173664,"model_load_end_ms":1790548174031,"inference_start_ms":1790548175016,"inference_end_ms":1790548175966,"model_execution_start_ms":1790548175019,"model_execution_end_ms":1790548175965,"prompt_eval_end_ms":1790548175966,"first_token_ms":1790548175966,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":946,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-1b-8da4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":2544.1,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548178953,"model_load_end_ms":1790548179327,"inference_start_ms":1790548180170,"inference_end_ms":1790548180975,"model_execution_start_ms":1790548180172,"model_execution_end_ms":1790548180974,"prompt_eval_end_ms":1790548180975,"first_token_ms":1790548180975,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":802,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-3b-4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":282.795,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548185576,"model_load_end_ms":1790548186402,"inference_start_ms":1790548193617,"inference_end_ms":1790548200859,"model_execution_start_ms":1790548193620,"model_execution_end_ms":1790548200858,"prompt_eval_end_ms":1790548200859,"first_token_ms":1790548200859,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":7238,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-3b-4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":1138.41,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548200969,"model_load_end_ms":1790548201787,"inference_start_ms":1790548203626,"inference_end_ms":1790548205425,"model_execution_start_ms":1790548203629,"model_execution_end_ms":1790548205424,"prompt_eval_end_ms":1790548205425,"first_token_ms":1790548205425,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1795,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-3b-8da4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":850.145,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548205535,"model_load_end_ms":1790548206398,"inference_start_ms":1790548208840,"inference_end_ms":1790548211249,"model_execution_start_ms":1790548208843,"model_execution_end_ms":1790548211248,"prompt_eval_end_ms":1790548211249,"first_token_ms":1790548211249,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2405,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-3b-8da4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":1048.11,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548211361,"model_load_end_ms":1790548212251,"inference_start_ms":1790548214251,"inference_end_ms":1790548216205,"model_execution_start_ms":1790548214253,"model_execution_end_ms":1790548216204,"prompt_eval_end_ms":1790548216205,"first_token_ms":1790548216205,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1951,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-8b-4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":113.734,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548216324,"model_load_end_ms":1790548219250,"inference_start_ms":1790548237241,"inference_end_ms":1790548255248,"model_execution_start_ms":1790548237244,"model_execution_end_ms":1790548255248,"prompt_eval_end_ms":1790548255248,"first_token_ms":1790548255248,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":18004,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-8b-4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":516.389,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548255352,"model_load_end_ms":1790548258377,"inference_start_ms":1790548262372,"inference_end_ms":1790548266338,"model_execution_start_ms":1790548262375,"model_execution_end_ms":1790548266337,"prompt_eval_end_ms":1790548266338,"first_token_ms":1790548266338,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":3962,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-8b-8da4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":377.372,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548266451,"model_load_end_ms":1790548269651,"inference_start_ms":1790548275091,"inference_end_ms":1790548280518,"model_execution_start_ms":1790548275094,"model_execution_end_ms":1790548280517,"prompt_eval_end_ms":1790548280518,"first_token_ms":1790548280518,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":5423,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/prefill-8b-8da4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":486.692,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790548280638,"model_load_end_ms":1790548283731,"inference_start_ms":1790548287972,"inference_end_ms":1790548292180,"model_execution_start_ms":1790548287975,"model_execution_end_ms":1790548292179,"prompt_eval_end_ms":1790548292180,"first_token_ms":1790548292180,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":4204,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Result directory results/780m/sdpa-e2e: check prompt (1972 tokens), 1B

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/check-1b-4w-tiled.log`, line 140

```text
PyTorchObserver {"prefill_token_per_sec":726.603,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790548159808,"model_load_end_ms":1790548160155,"inference_start_ms":1790548160155,"inference_end_ms":1790548162869,"model_execution_start_ms":1790548160158,"model_execution_end_ms":1790548162869,"prompt_eval_end_ms":1790548162869,"first_token_ms":1790548162869,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2711,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/check-1b-4w-default.log`, line 140

```text
PyTorchObserver {"prefill_token_per_sec":725,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790548167692,"model_load_end_ms":1790548168045,"inference_start_ms":1790548168045,"inference_end_ms":1790548170765,"model_execution_start_ms":1790548168050,"model_execution_end_ms":1790548170765,"prompt_eval_end_ms":1790548170765,"first_token_ms":1790548170765,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2715,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/check-1b-8da4w-tiled.log`, line 140

```text
PyTorchObserver {"prefill_token_per_sec":1749.78,"decode_token_per_sec":0,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790548176063,"model_load_end_ms":1790548176431,"inference_start_ms":1790548176431,"inference_end_ms":1790548177559,"model_execution_start_ms":1790548176436,"model_execution_end_ms":1790548177558,"prompt_eval_end_ms":1790548177558,"first_token_ms":1790548177558,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1122,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/check-1b-8da4w-default.log`, line 140

```text
PyTorchObserver {"prefill_token_per_sec":1759.14,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790548181070,"model_load_end_ms":1790548181431,"inference_start_ms":1790548181431,"inference_end_ms":1790548182552,"model_execution_start_ms":1790548181435,"model_execution_end_ms":1790548182552,"prompt_eval_end_ms":1790548182552,"first_token_ms":1790548182552,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1117,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Result directory results/780m/sdpa-e2e: unaligned prompt (1792 tokens), 1B

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/unaligned-1b-4w-tiled.log`, line 7

```text
PyTorchObserver {"prefill_token_per_sec":788.039,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790548162960,"model_load_end_ms":1790548163312,"inference_start_ms":1790548163312,"inference_end_ms":1790548165586,"model_execution_start_ms":1790548163316,"model_execution_end_ms":1790548165586,"prompt_eval_end_ms":1790548165586,"first_token_ms":1790548165586,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2270,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/unaligned-1b-4w-default.log`, line 7

```text
PyTorchObserver {"prefill_token_per_sec":2635.29,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790548170856,"model_load_end_ms":1790548171214,"inference_start_ms":1790548171214,"inference_end_ms":1790548171894,"model_execution_start_ms":1790548171220,"model_execution_end_ms":1790548171894,"prompt_eval_end_ms":1790548171894,"first_token_ms":1790548171894,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":674,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/unaligned-1b-8da4w-tiled.log`, line 7

```text
PyTorchObserver {"prefill_token_per_sec":2140.98,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790548177652,"model_load_end_ms":1790548178023,"inference_start_ms":1790548178023,"inference_end_ms":1790548178860,"model_execution_start_ms":1790548178027,"model_execution_end_ms":1790548178860,"prompt_eval_end_ms":1790548178860,"first_token_ms":1790548178860,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":833,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/unaligned-1b-8da4w-default.log`, line 7

```text
PyTorchObserver {"prefill_token_per_sec":2509.8,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790548182645,"model_load_end_ms":1790548183016,"inference_start_ms":1790548183016,"inference_end_ms":1790548183730,"model_execution_start_ms":1790548183019,"model_execution_end_ms":1790548183729,"prompt_eval_end_ms":1790548183730,"first_token_ms":1790548183730,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":710,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Result directory results/780m/sdpa-e2e: decode, 1B

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/decode-1b-4w.log`, line 9

```text
PyTorchObserver {"prefill_token_per_sec":2569.64,"decode_token_per_sec":70.7763,"prompt_tokens":2048,"generated_tokens":31,"model_load_start_ms":1790548171991,"model_load_end_ms":1790548172332,"inference_start_ms":1790548172332,"inference_end_ms":1790548173567,"model_execution_start_ms":1790548173554,"model_execution_end_ms":1790548173567,"prompt_eval_end_ms":1790548173129,"first_token_ms":1790548173129,"aggregate_sampling_time_ms":11,"aggregate_model_execution_time_ms":1218,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/decode-1b-8da4w.log`, line 9

```text
PyTorchObserver {"prefill_token_per_sec":2420.8,"decode_token_per_sec":71.1009,"prompt_tokens":2048,"generated_tokens":31,"model_load_start_ms":1790548183827,"model_load_end_ms":1790548184192,"inference_start_ms":1790548184192,"inference_end_ms":1790548185474,"model_execution_start_ms":1790548185460,"model_execution_end_ms":1790548185473,"prompt_eval_end_ms":1790548185038,"first_token_ms":1790548185038,"aggregate_sampling_time_ms":19,"aggregate_model_execution_time_ms":1257,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Result directory results/780m/sdpa-e2e: linear microbench with the SDPA rows present

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-4w.log`, lines 153-177

```text
suite     model         scheme regime   op     storage    variant  (M,K,N)                   mean_us     stdev   kern_us   GFLOP/s  dispatch
linear    llama-3.1-8b  4w     prefill  wq_wo  texture3d  coopmat  (2048,4096,4096)           6495.1       4.4    6495.1   10580.2  unexpected_coopmat
linear    llama-3.1-8b  4w     prefill  wq_wo  buffer     coopmat  (2048,4096,4096)           6492.2      11.3    6492.2   10584.9  confirmed
linear    llama-3.1-8b  4w     prefill  wk_wv  texture3d  coopmat  (2048,4096,1024)           1715.5       2.1    1715.5   10014.3  unexpected_coopmat
linear    llama-3.1-8b  4w     prefill  wk_wv  buffer     coopmat  (2048,4096,1024)           1732.0       2.4    1732.0    9919.2  confirmed
linear    llama-3.1-8b  4w     prefill  w1_w3  texture3d  coopmat  (2048,4096,14336)         22092.6      45.5   22092.6   10886.8  unexpected_coopmat
linear    llama-3.1-8b  4w     prefill  w1_w3  buffer     coopmat  (2048,4096,14336)         22210.1      74.7   22210.1   10829.2  confirmed
linear    llama-3.1-8b  4w     prefill  w2     texture3d  coopmat  (2048,14336,4096)         22200.7     126.1   22200.7   10833.8  unexpected_coopmat
linear    llama-3.1-8b  4w     prefill  w2     buffer     coopmat  (2048,14336,4096)         22444.5      80.6   22444.5   10716.2  confirmed
linear    llama-3.2-3b  4w     prefill  wq_wo  texture3d  coopmat  (2048,3072,3072)           3550.8       9.7    3550.8   10886.1  unexpected_coopmat
linear    llama-3.2-3b  4w     prefill  wq_wo  buffer     coopmat  (2048,3072,3072)           3552.4      12.1    3552.4   10881.2  confirmed
linear    llama-3.2-3b  4w     prefill  wk_wv  texture3d  coopmat  (2048,3072,1024)           1260.9       5.6    1260.9   10218.7  unexpected_coopmat
linear    llama-3.2-3b  4w     prefill  wk_wv  buffer     coopmat  (2048,3072,1024)           1281.6       2.9    1281.6   10053.5  confirmed
linear    llama-3.2-3b  4w     prefill  w1_w3  texture3d  coopmat  (2048,3072,8192)           9458.3      67.2    9458.3   10898.3  unexpected_coopmat
linear    llama-3.2-3b  4w     prefill  w1_w3  buffer     coopmat  (2048,3072,8192)           9388.5      34.8    9388.5   10979.3  confirmed
linear    llama-3.2-3b  4w     prefill  w2     texture3d  coopmat  (2048,8192,3072)           9520.7      25.9    9520.7   10826.9  unexpected_coopmat
linear    llama-3.2-3b  4w     prefill  w2     buffer     coopmat  (2048,8192,3072)           9613.5      21.1    9613.5   10722.3  confirmed
linear    llama-3.2-1b  4w     prefill  wq_wo  texture3d  coopmat  (2048,2048,2048)           1617.2      16.3    1617.2   10623.2  unexpected_coopmat
linear    llama-3.2-1b  4w     prefill  wq_wo  buffer     coopmat  (2048,2048,2048)           1610.9       5.8    1610.9   10664.8  confirmed
linear    llama-3.2-1b  4w     prefill  wk_wv  texture3d  coopmat  (2048,2048,512)             439.8       2.2     439.8    9765.3  unexpected_coopmat
linear    llama-3.2-1b  4w     prefill  wk_wv  buffer     coopmat  (2048,2048,512)             443.6       0.5     443.6    9682.6  confirmed
linear    llama-3.2-1b  4w     prefill  w1_w3  texture3d  coopmat  (2048,2048,8192)           6316.1      25.1    6316.1   10880.1  unexpected_coopmat
linear    llama-3.2-1b  4w     prefill  w1_w3  buffer     coopmat  (2048,2048,8192)           6256.9      21.3    6256.9   10983.0  confirmed
linear    llama-3.2-1b  4w     prefill  w2     texture3d  coopmat  (2048,8192,2048)           6501.3      26.3    6501.3   10570.1  unexpected_coopmat
linear    llama-3.2-1b  4w     prefill  w2     buffer     coopmat  (2048,8192,2048)           6567.8      36.3    6567.8   10463.1  confirmed
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-4w.log`, line 201

```text
One or more cases crashed or did not dispatch the expected kernel (see dispatch column) -- do not trust their speedup numbers.
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-8da4w.log`, lines 201-225

```text
suite     model         scheme regime   op     storage    variant  (M,K,N)                   mean_us     stdev   kern_us   GFLOP/s  dispatch
linear    llama-3.1-8b  8da4w  prefill  wq_wo  texture3d  coopmat  (2048,4096,4096)           7164.2      27.4    6829.4    9592.1  unexpected_coopmat
linear    llama-3.1-8b  8da4w  prefill  wq_wo  buffer     coopmat  (2048,4096,4096)           7119.5      17.6    6784.9    9652.3  confirmed
linear    llama-3.1-8b  8da4w  prefill  wk_wv  texture3d  coopmat  (2048,4096,1024)           2065.5       2.7    1731.8    8317.7  unexpected_coopmat
linear    llama-3.1-8b  8da4w  prefill  wk_wv  buffer     coopmat  (2048,4096,1024)           2054.2       0.9    1720.5    8363.4  confirmed
linear    llama-3.1-8b  8da4w  prefill  w1_w3  texture3d  coopmat  (2048,4096,14336)         24271.8     163.9   23937.0    9909.4  unexpected_coopmat
linear    llama-3.1-8b  8da4w  prefill  w1_w3  buffer     coopmat  (2048,4096,14336)         24073.9      66.4   23739.4    9990.8  confirmed
linear    llama-3.1-8b  8da4w  prefill  w2     texture3d  coopmat  (2048,14336,4096)         25142.3      49.8   23936.6    9566.3  unexpected_coopmat
linear    llama-3.1-8b  8da4w  prefill  w2     buffer     coopmat  (2048,14336,4096)         25115.3      38.7   23917.8    9576.6  confirmed
linear    llama-3.2-3b  8da4w  prefill  wq_wo  texture3d  coopmat  (2048,3072,3072)           4103.0       8.8    3848.4    9421.0  unexpected_coopmat
linear    llama-3.2-3b  8da4w  prefill  wq_wo  buffer     coopmat  (2048,3072,3072)           4063.9       9.5    3811.0    9511.8  confirmed
linear    llama-3.2-3b  8da4w  prefill  wk_wv  texture3d  coopmat  (2048,3072,1024)           1558.3       0.9    1305.8    8268.4  unexpected_coopmat
linear    llama-3.2-3b  8da4w  prefill  wk_wv  buffer     coopmat  (2048,3072,1024)           1547.7       2.2    1294.6    8325.4  confirmed
linear    llama-3.2-3b  8da4w  prefill  w1_w3  texture3d  coopmat  (2048,3072,8192)          10540.5      28.6   10287.4    9779.4  unexpected_coopmat
linear    llama-3.2-3b  8da4w  prefill  w1_w3  buffer     coopmat  (2048,3072,8192)          10475.2      49.2   10221.9    9840.3  confirmed
linear    llama-3.2-3b  8da4w  prefill  w2     texture3d  coopmat  (2048,8192,3072)          10906.8      23.3   10232.7    9450.9  unexpected_coopmat
linear    llama-3.2-3b  8da4w  prefill  w2     buffer     coopmat  (2048,8192,3072)          10902.7      27.3   10227.9    9454.4  confirmed
linear    llama-3.2-1b  8da4w  prefill  wq_wo  texture3d  coopmat  (2048,2048,2048)           1917.0       2.9    1749.7    8962.0  unexpected_coopmat
linear    llama-3.2-1b  8da4w  prefill  wq_wo  buffer     coopmat  (2048,2048,2048)           1893.1       2.7    1727.0    9075.2  confirmed
linear    llama-3.2-1b  8da4w  prefill  wk_wv  texture3d  coopmat  (2048,2048,512)             624.5       0.1     455.9    6877.8  unexpected_coopmat
linear    llama-3.2-1b  8da4w  prefill  wk_wv  buffer     coopmat  (2048,2048,512)             618.7       0.5     450.3    6942.3  confirmed
linear    llama-3.2-1b  8da4w  prefill  w1_w3  texture3d  coopmat  (2048,2048,8192)           7090.4      19.3    6922.8    9691.9  unexpected_coopmat
linear    llama-3.2-1b  8da4w  prefill  w1_w3  buffer     coopmat  (2048,2048,8192)           7009.9      22.8    6843.7    9803.2  confirmed
linear    llama-3.2-1b  8da4w  prefill  w2     texture3d  coopmat  (2048,8192,2048)           7566.8      27.6    6892.3    9081.7  unexpected_coopmat
linear    llama-3.2-1b  8da4w  prefill  w2     buffer     coopmat  (2048,8192,2048)           7566.4      11.3    6890.5    9082.2  confirmed
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-8da4w.log`, line 249

```text
One or more cases crashed or did not dispatch the expected kernel (see dispatch column) -- do not trust their speedup numbers.
```

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-4w.json`, lines 1-9

```text
{
  "schema": "test_llama_microbench.v1",
  "device": "amd radeon 780m graphics (radv phoenix)",
  "subgroup_size": 64,
  "timestamp_period_ns": 10,
  "cooperative_matrix": true,
  "warmup_runs": 3,
  "timed_runs": 5,
  "group_size": 128,
```

## Result directory results/780m/sdpa-e2e: linear correctness matrix, rank-3 summary lines

Locator: `openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/correctness.log`, lines 283-286

```text
[rank3 batch=1] linear_q4gsw_M128_K128_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_dq8ca_q4gsw_M128_K128_N128_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_dq8ca_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
```
