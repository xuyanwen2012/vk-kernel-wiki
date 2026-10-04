---
id: meas-780m-4w-bootstrap
title: "Radeon 780M 4w linear coopmat port to release 1.5 (sarc-1.5-bootstrap): microbench, correctness, end-to-end prefill"
source_category: measurement
architectures: [radeon-780m]
tags: [linear-4w, tiled-linear, prefill, decode, cooperative-matrix, subgroup-size, shared-memory-limit, storage-buffer, storage-texture3d, storage-texture2d, workgroup-tile-sizing, fp32-accumulation, drain-in-a-staging]
device: radeon-780m
driver: "RADV Mesa 25.2.7"
measured_at: '2026-09-27'
method: "sarc/tools/verify.sh on the device: test_llama_microbench (3 warmup + 5 timed runs per case, linear group_size=128, prefill M=2048) for kernel dispatch and timing, its correctness and production-diff modes, and llama_main end-to-end runs (2048-token prefill tok/s, real-text and unaligned prompt output comparison against tiled, 32-token decode). Three builds: SARC dev build with ET_VK_SARC_UNVERIFIED=1 (default and ET_VK_FORCE_TILED_LINEAR), stock release 1.5, SARC release export. Single run; clocks not pinned. Excerpt lines that contain a host name are omitted from this page."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/proposal.md
    description: "Change proposal with the 2026-09-27 results section for the Radeon 780M 4w coopmat port (setup, kernels, correctness, end-to-end table, checks, not-verified list)"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/tasks.md
    description: "Task checklist of the change"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out
    description: "Summary lines produced by the verification run: dispatched kernel counts, prefill tok/s, output comparisons, decode, production-diff, for the SARC dev build and the stock build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/env.txt
    description: "Run environment of the SARC dev-build run: start timestamp, environment variables, sha256 of the binaries"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/done.txt
    description: "End timestamp of the SARC dev-build run"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.log
    description: "test_llama_microbench log, 4w linear prefill shapes, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json
    description: "test_llama_microbench JSON output, 4w linear prefill shapes, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/correctness.log
    description: "test_llama_microbench correctness log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.1-8b-4w-buffer.log
    description: "test_llama_microbench production-diff log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.1-8b-4w-texture3d.log
    description: "test_llama_microbench production-diff log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-1b-4w-buffer.log
    description: "test_llama_microbench production-diff log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-1b-4w-texture3d.log
    description: "test_llama_microbench production-diff log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-3b-4w-buffer.log
    description: "test_llama_microbench production-diff log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-3b-4w-texture3d.log
    description: "test_llama_microbench production-diff log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-default.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-tiled.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-default.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-tiled.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-default.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-tiled.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/check-1b-4w-default.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/check-1b-4w-tiled.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/unaligned-1b-4w-default.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/unaligned-1b-4w-tiled.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/decode-1b-4w.log
    description: "llama_main end-to-end log, SARC dev build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/env.txt
    description: "Run environment of the stock release 1.5 run: start timestamp, environment variables, sha256 of the binaries"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/done.txt
    description: "End timestamp of the stock release 1.5 run"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.log
    description: "test_llama_microbench log, 4w linear prefill shapes, stock release 1.5 build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json
    description: "test_llama_microbench JSON output, 4w linear prefill shapes, stock release 1.5 build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-1b-4w-default.log
    description: "llama_main end-to-end log, stock release 1.5 build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-3b-4w-default.log
    description: "llama_main end-to-end log, stock release 1.5 build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-8b-4w-default.log
    description: "llama_main end-to-end log, stock release 1.5 build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/check-1b-4w-default.log
    description: "llama_main end-to-end log, stock release 1.5 build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/unaligned-1b-4w-default.log
    description: "llama_main end-to-end log, stock release 1.5 build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/decode-1b-4w.log
    description: "llama_main end-to-end log, stock release 1.5 build"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/release/env.txt
    description: "Run environment of the SARC release-export run: start timestamp, environment variables, sha256 of the binaries"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/release/done.txt
    description: "End timestamp of the SARC release-export run"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-1b-4w-default.log
    description: "llama_main end-to-end log, SARC release export"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-3b-4w-default.log
    description: "llama_main end-to-end log, SARC release export"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-8b-4w-default.log
    description: "llama_main end-to-end log, SARC release export"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/release/check-1b-4w-default.log
    description: "llama_main end-to-end log, SARC release export"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/release/unaligned-1b-4w-default.log
    description: "llama_main end-to-end log, SARC release export"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-bootstrap/results/780m/release/decode-1b-4w.log
    description: "llama_main end-to-end log, SARC release export"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp
    description: "SARC selection rows for AMD GPUs; the Radeon 780M rows (4w with its driver comment, 8da4w, SDPA QK and AV) with their tile dims, storage masks and status"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: sarc/README.md
    description: "SARC development-zone README: selection layer, dev overrides, promotion checklist, device status table"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: sarc/SWEEP-PARAMETERS.md
    description: "Compile-time parameters of the SARC linear coopmat shaders, variant naming, shipped variants"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h
    description: "Kernel selector header: DeviceInfo and TileDims struct definitions (field order of the tile rows)"
captured_at: '2026-10-03'
glslc_version: "shaderc v2023.8"
baseline: "stock release 1.5 (upstream q4gsw_linear_gemm__tin__w_4x8) and the dev build with ET_VK_FORCE_TILED_LINEAR"
---

## Excerpt: openspec/changes/sarc-1.5-bootstrap/proposal.md, lines 23-28

Locator: `openspec/changes/sarc-1.5-bootstrap/proposal.md`, lines 23-28

```text
- **Proof of concept.** Radeon 780M 4w coopmat (`t128x128k32g42s32f32c`), ported from
  `yanwen/release14-quant-shaders-780m` e4786474b9.
  - The shader is byte-identical to the 1.4 one, split into a body and a wrapper.
  - A `buffer_buffer` variant is added (missing on 1.4).
  - The device match is case-insensitive.
  - Launch dims come from the table instead of kernel-name parsing.
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/proposal.md, lines 36-37, 39-43

Locator: `openspec/changes/sarc-1.5-bootstrap/proposal.md`, lines 36-37, 39-43

```text
- **Microbenchmark on the 780M** (`verify.sh`):
  - every 1B/3B/8B 4w prefill shape dispatches `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_*`;
- **Correctness:** correctness and production-diff pass.
- **End to end (1B/3B/8B 4w):**
  - prefill tok/s for stock 1.5, tiled and SARC;
  - next token == tiled on the real-text and the unaligned prompt;
  - decode works.
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/proposal.md, lines 46-48, 50-52

Locator: `openspec/changes/sarc-1.5-bootstrap/proposal.md`, lines 46-48, 50-52

```text
## Results (2026-09-27)

**Setup.**
  (clocks not pinned).
- Builds: `sarc/tools/build.sh` (`localhost/et-vk-build:rocky10`, shaderc v2023.8).
- PTEs: the existing `llama3_*_vulkan_4w.pte` in `/mnt/linux-share/models` (exported with the 1.4 flow).
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/proposal.md, lines 55-80

Locator: `openspec/changes/sarc-1.5-bootstrap/proposal.md`, lines 55-80

```text
**Kernels.**
- All 24 4w prefill shapes (1B/3B/8B × 4 ops × buffer/texture3d) dispatch
  `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_{texture3d,buffer}_texture2d_half`.
- Median kernel time vs the 1.4 confirmation (`confirm/780m-final`) is 0.988×, range 0.984–0.998×
  (single run).

**Correctness.**
- All 4w numeric checks pass, including the rank-3 cases.
- The binary exits with rc = 1 only because the 8da4w rank-3 cases fall back to tiled; 8da4w is not
  ported yet.
- Production-diff passes for 1B/3B/8B × buffer/texture3d (6/6).

**End to end, 2048-token prefill, tok/s:**

| Build / mode | 1B | 3B | 8B |
|---|---:|---:|---:|
| tiled (dev build, `ET_VK_FORCE_TILED_LINEAR`) | 714 | 246 | 104 |
| stock release 1.5 (upstream `q4gsw_linear_gemm__tin__w_4x8`) | 1205 | 421 | 194 |
| SARC (dev build, `ET_VK_SARC_UNVERIFIED=1`) | 1916 | 683 | 352 |
| SARC release export (row verified, no env) | 1930 | 690 | 352 |
| SARC vs stock 1.5 | 1.60× | 1.64× | 1.81× |

**Checks.**
- Next token: the release export and SARC match tiled on the 1973-token real-text prompt and on the
  1304-token unaligned prompt (fallback path).
- Decode, 32 tokens: SARC 70.8–73.5 tok/s vs stock 69.5.
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/proposal.md, lines 83-89

Locator: `openspec/changes/sarc-1.5-bootstrap/proposal.md`, lines 83-89

```text
- `check.sh` passes: zone rule, twins, selection test, host and Android release-export builds, SPIR-V golden.
- The SPIR-V verified on the device (dev build) is byte-identical to the release export.

**Not verified.**
- The `buffer_buffer` variant (buffer weights) builds and is in the golden, but no microbench or PTE
  case uses buffer-stored 4-bit weights, so it has not run on the device.
- Clocks were not pinned.
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/proposal.md, lines 91-98

Locator: `openspec/changes/sarc-1.5-bootstrap/proposal.md`, lines 91-98

```text
**Finding: 1.5 vs 1.4 end to end.**
- The 1.4 780M branch reached 2702 tok/s (1B), versus 1916 here, although the linear kernels are ~1 %
  *faster*.
- Both tiled and SARC gain the same ~311 ms per prefill: tiled 2557 → 2868 ms, SARC 758 → 1069 ms. So
  the difference lies outside the 4w linears.
- The most likely cause is the SDPA coopmat work (`sdpa_*_coopmat`) carried by the 1.4 dev branches and
  not yet ported to 1.5. **Not yet confirmed**; the next step is `test_llama_microbench --sdpa` / ETDump
  on both.
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/tasks.md, line 7

Locator: `openspec/changes/sarc-1.5-bootstrap/tasks.md`, line 7

```text
- [x] Promote 780M row to verified, golden SPIR-V
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out, lines 1-25

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/run-all.out`, lines 1-25

```text
correctness rc=1 [correctness] FAILED -- numeric failure(s) and/or a rank-3 case did not dispatch coopmat
linear 4w rc=1 kernels:  12 "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half"; 12 "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half";
1b 4w tiled prefill_tok_s=714.336
1b 4w default prefill_tok_s=1915.81
1b 4w check: default vs tiled output SAME
1b 4w unaligned: default vs tiled output SAME
1b 4w decode rc=0 "generated_tokens":31 decode_tok_s=70.7763
3b 4w tiled prefill_tok_s=246.065
3b 4w default prefill_tok_s=683.35
8b 4w tiled prefill_tok_s=104.357
8b 4w default prefill_tok_s=351.951
pdiff llama-3.2-1b 4w buffer rc=0 [production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_q4gsw, buffer)
pdiff llama-3.2-1b 4w texture3d rc=0 [production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_q4gsw, texture3d)
pdiff llama-3.2-3b 4w buffer rc=0 [production-diff] ALL PASSED (llama-3.2-3b, 4 shapes, M=2048, linear_q4gsw, buffer)
pdiff llama-3.2-3b 4w texture3d rc=0 [production-diff] ALL PASSED (llama-3.2-3b, 4 shapes, M=2048, linear_q4gsw, texture3d)
pdiff llama-3.1-8b 4w buffer rc=0 [production-diff] ALL PASSED (llama-3.1-8b, 4 shapes, M=2048, linear_q4gsw, buffer)
pdiff llama-3.1-8b 4w texture3d rc=0 [production-diff] ALL PASSED (llama-3.1-8b, 4 shapes, M=2048, linear_q4gsw, texture3d)
---- stock
correctness rc=1 [correctness] FAILED -- numeric failure(s) and/or a rank-3 case did not dispatch coopmat
linear 4w rc=1 kernels:  12 "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half"; 12 "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half";
1b 4w default prefill_tok_s=1204.71
1b 4w decode rc=0 "generated_tokens":31 decode_tok_s=69.5067
3b 4w default prefill_tok_s=421.486
8b 4w default prefill_tok_s=193.829
ALLDONE
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/env.txt, lines 1, 3-7

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/env.txt`, lines 1, 3-7

```text
Sun Sep 27 08:58:03 PM UTC 2026
ETVK_DEVICE_INDEX=0
ET_VK_SARC_UNVERIFIED=1
b5791f98ba8af95e5b6c601a5dc24ba0eb992009c14510a22e4e30139c7428a3  test_llama_microbench
93f98e4059bc2e7b21307609983a8c1ccdc618ffa5f4e364198e402c0433c504  llama_main
7316cc3dd220104c07db8272a504759feabec77a8d15c2ec0cd2adb36d005372  libllama_runner.so
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/done.txt, line 1

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/done.txt`, line 1

```text
Sun Sep 27 09:01:15 PM UTC 2026
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/env.txt, lines 1, 3-6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/env.txt`, lines 1, 3-6

```text
Sun Sep 27 09:01:15 PM UTC 2026
ETVK_DEVICE_INDEX=0
b5791f98ba8af95e5b6c601a5dc24ba0eb992009c14510a22e4e30139c7428a3  test_llama_microbench
93f98e4059bc2e7b21307609983a8c1ccdc618ffa5f4e364198e402c0433c504  llama_main
7316cc3dd220104c07db8272a504759feabec77a8d15c2ec0cd2adb36d005372  libllama_runner.so
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/done.txt, line 1

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/done.txt`, line 1

```text
Sun Sep 27 09:02:47 PM UTC 2026
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/release/env.txt, lines 1, 3-5

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/release/env.txt`, lines 1, 3-5

```text
Sun Sep 27 09:13:28 PM UTC 2026
ETVK_DEVICE_INDEX=0
e058f7c054ac35be68027f5c2bbe992bf3d2691b5abb6f9b821cb6b1338a982e  llama_main
f6d62b01465f63ea60d783e06f037ac0a4ee5ae55e98522b3ad4346f842b0b03  libllama_runner.so
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/release/done.txt, line 1

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/release/done.txt`, line 1

```text
Sun Sep 27 09:13:58 PM UTC 2026
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.log, lines 4-5

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.log`, lines 4-5

```text
Llama microbench (3.1 8B / 3.2 3B / 3.2 1B real e2e shapes; prefill 2048 / decode 1 @ ctx3072; linear group_size=128; 3 warmup + 5 timed runs per case)
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json, lines 1-36

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/linear-4w.json`, lines 1-36

```json
{
  "schema": "test_llama_microbench.v1",
  "device": "amd radeon 780m graphics (radv phoenix)",
  "subgroup_size": 64,
  "timestamp_period_ns": 10,
  "cooperative_matrix": true,
  "warmup_runs": 3,
  "timed_runs": 5,
  "group_size": 128,
  "cases": [
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 4096, "N": 4096, "kv_heads": 0, "op_mean_us": 6478.58, "op_stdev_us": 3.68821, "kernel_mean_us": 6478.58, "kernel_median_us": 6481, "kernel_cov": 0.00232137, "gflops": 10607.2, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 4096, "N": 4096, "kv_heads": 0, "op_mean_us": 6489.77, "op_stdev_us": 9.27326, "kernel_mean_us": 6489.77, "kernel_median_us": 6481.4, "kernel_cov": 0.00411775, "gflops": 10588.9, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 4096, "N": 1024, "kv_heads": 0, "op_mean_us": 1718.17, "op_stdev_us": 4.9287, "kernel_mean_us": 1718.17, "kernel_median_us": 1716.96, "kernel_cov": 0.00893543, "gflops": 9998.91, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 4096, "N": 1024, "kv_heads": 0, "op_mean_us": 1732.51, "op_stdev_us": 3.70114, "kernel_mean_us": 1732.51, "kernel_median_us": 1732.96, "kernel_cov": 0.00651676, "gflops": 9916.17, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 4096, "N": 14336, "kv_heads": 0, "op_mean_us": 22075.5, "op_stdev_us": 98.57, "kernel_mean_us": 22075.5, "kernel_median_us": 22023.1, "kernel_cov": 0.00658599, "gflops": 10895.2, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 4096, "N": 14336, "kv_heads": 0, "op_mean_us": 22059.5, "op_stdev_us": 36.737, "kernel_mean_us": 22059.5, "kernel_median_us": 22060.3, "kernel_cov": 0.00175795, "gflops": 10903.2, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 14336, "N": 4096, "kv_heads": 0, "op_mean_us": 22090.9, "op_stdev_us": 15.6719, "kernel_mean_us": 22090.9, "kernel_median_us": 22098.7, "kernel_cov": 0.00202827, "gflops": 10887.6, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 14336, "N": 4096, "kv_heads": 0, "op_mean_us": 22322.8, "op_stdev_us": 32.2589, "kernel_mean_us": 22322.8, "kernel_median_us": 22312.4, "kernel_cov": 0.00164488, "gflops": 10774.6, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 3072, "N": 3072, "kv_heads": 0, "op_mean_us": 3659.97, "op_stdev_us": 86.8789, "kernel_mean_us": 3659.97, "kernel_median_us": 3582.48, "kernel_cov": 0.0371478, "gflops": 10561.5, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 3072, "N": 3072, "kv_heads": 0, "op_mean_us": 3551.59, "op_stdev_us": 8.17665, "kernel_mean_us": 3551.59, "kernel_median_us": 3545.96, "kernel_cov": 0.00464702, "gflops": 10883.8, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 3072, "N": 1024, "kv_heads": 0, "op_mean_us": 1256.36, "op_stdev_us": 1.80523, "kernel_mean_us": 1256.36, "kernel_median_us": 1256.44, "kernel_cov": 0.00572993, "gflops": 10255.7, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 3072, "N": 1024, "kv_heads": 0, "op_mean_us": 1277.82, "op_stdev_us": 5.29507, "kernel_mean_us": 1277.82, "kernel_median_us": 1276.52, "kernel_cov": 0.0100036, "gflops": 10083.5, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 3072, "N": 8192, "kv_heads": 0, "op_mean_us": 9406.45, "op_stdev_us": 30.2847, "kernel_mean_us": 9406.45, "kernel_median_us": 9404.12, "kernel_cov": 0.00433232, "gflops": 10958.4, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 3072, "N": 8192, "kv_heads": 0, "op_mean_us": 9388.37, "op_stdev_us": 64.589, "kernel_mean_us": 9388.37, "kernel_median_us": 9389.78, "kernel_cov": 0.00984994, "gflops": 10979.5, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 8192, "N": 3072, "kv_heads": 0, "op_mean_us": 9489.43, "op_stdev_us": 16.1867, "kernel_mean_us": 9489.43, "kernel_median_us": 9488.56, "kernel_cov": 0.0021151, "gflops": 10862.5, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 8192, "N": 3072, "kv_heads": 0, "op_mean_us": 9644.26, "op_stdev_us": 113.322, "kernel_mean_us": 9644.26, "kernel_median_us": 9597.64, "kernel_cov": 0.0172155, "gflops": 10688.1, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 2048, "N": 2048, "kv_heads": 0, "op_mean_us": 1608.4, "op_stdev_us": 2.63144, "kernel_mean_us": 1608.4, "kernel_median_us": 1607.96, "kernel_cov": 0.00366602, "gflops": 10681.4, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 2048, "N": 2048, "kv_heads": 0, "op_mean_us": 1598.36, "op_stdev_us": 4.11488, "kernel_mean_us": 1598.36, "kernel_median_us": 1598.5, "kernel_cov": 0.00454611, "gflops": 10748.4, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 2048, "N": 512, "kv_heads": 0, "op_mean_us": 438.941, "op_stdev_us": 0.356731, "kernel_mean_us": 438.94, "kernel_median_us": 438.52, "kernel_cov": 0.00833277, "gflops": 9784.85, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 2048, "N": 512, "kv_heads": 0, "op_mean_us": 444.363, "op_stdev_us": 1.01094, "kernel_mean_us": 444.363, "kernel_median_us": 443.84, "kernel_cov": 0.0111758, "gflops": 9665.45, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 2048, "N": 8192, "kv_heads": 0, "op_mean_us": 6298.14, "op_stdev_us": 18.7464, "kernel_mean_us": 6298.14, "kernel_median_us": 6297.8, "kernel_cov": 0.003431, "gflops": 10911.1, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 2048, "N": 8192, "kv_heads": 0, "op_mean_us": 6242.85, "op_stdev_us": 25.1022, "kernel_mean_us": 6242.85, "kernel_median_us": 6246.16, "kernel_cov": 0.00435099, "gflops": 11007.7, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half", "M": 2048, "K": 8192, "N": 2048, "kv_heads": 0, "op_mean_us": 6480.29, "op_stdev_us": 19.8502, "kernel_mean_us": 6480.29, "kernel_median_us": 6479.96, "kernel_cov": 0.00522873, "gflops": 10604.4, "dispatch": "unexpected_coopmat", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "coopmat", "kernel": "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half", "M": 2048, "K": 8192, "N": 2048, "kv_heads": 0, "op_mean_us": 6535.7, "op_stdev_us": 10.9332, "kernel_mean_us": 6535.7, "kernel_median_us": 6538.68, "kernel_cov": 0.00313167, "gflops": 10514.5, "dispatch": "confirmed", "correctness": "SKIPPED", "detail": "", "ok": true}
  ]
}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.log, lines 3-4

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.log`, lines 3-4

```text
Llama microbench (3.1 8B / 3.2 3B / 3.2 1B real e2e shapes; prefill 2048 / decode 1 @ ctx3072; linear group_size=128; 3 warmup + 5 timed runs per case)
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json, lines 1-36

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/linear-4w.json`, lines 1-36

```json
{
  "schema": "test_llama_microbench.v1",
  "device": "amd radeon 780m graphics (radv phoenix)",
  "subgroup_size": 64,
  "timestamp_period_ns": 10,
  "cooperative_matrix": true,
  "warmup_runs": 3,
  "timed_runs": 5,
  "group_size": 128,
  "cases": [
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 4096, "N": 4096, "kv_heads": 0, "op_mean_us": 17265, "op_stdev_us": 26.6435, "kernel_mean_us": 16310.4, "kernel_median_us": 16314.4, "kernel_cov": 0.00198504, "gflops": 3980.29, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 4096, "N": 4096, "kv_heads": 0, "op_mean_us": 17476.3, "op_stdev_us": 31.0295, "kernel_mean_us": 16315.3, "kernel_median_us": 16320.7, "kernel_cov": 0.00233924, "gflops": 3932.16, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 4096, "N": 1024, "kv_heads": 0, "op_mean_us": 5042.02, "op_stdev_us": 15.349, "kernel_mean_us": 4092.05, "kernel_median_us": 4089.84, "kernel_cov": 0.00396356, "gflops": 3407.34, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 4096, "N": 1024, "kv_heads": 0, "op_mean_us": 5251.01, "op_stdev_us": 12.3293, "kernel_mean_us": 4088.85, "kernel_median_us": 4083.16, "kernel_cov": 0.00636852, "gflops": 3271.73, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 4096, "N": 14336, "kv_heads": 0, "op_mean_us": 58170.9, "op_stdev_us": 164.815, "kernel_mean_us": 57206, "kernel_median_us": 57203.9, "kernel_cov": 0.00254577, "gflops": 4134.68, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 4096, "N": 14336, "kv_heads": 0, "op_mean_us": 58579, "op_stdev_us": 270.458, "kernel_mean_us": 57414.7, "kernel_median_us": 57293.3, "kernel_cov": 0.00420693, "gflops": 4105.88, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 14336, "N": 4096, "kv_heads": 0, "op_mean_us": 61428.4, "op_stdev_us": 19.1305, "kernel_mean_us": 57495.6, "kernel_median_us": 57492.9, "kernel_cov": 0.000232393, "gflops": 3915.42, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 14336, "N": 4096, "kv_heads": 0, "op_mean_us": 62144.4, "op_stdev_us": 50.6998, "kernel_mean_us": 57546.9, "kernel_median_us": 57557.6, "kernel_cov": 0.0007505, "gflops": 3870.31, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 3072, "N": 3072, "kv_heads": 0, "op_mean_us": 9755.8, "op_stdev_us": 26.9935, "kernel_mean_us": 9142.02, "kernel_median_us": 9143.62, "kernel_cov": 0.00359616, "gflops": 3962.23, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 3072, "N": 3072, "kv_heads": 0, "op_mean_us": 9843.71, "op_stdev_us": 69.451, "kernel_mean_us": 9186.4, "kernel_median_us": 9160.06, "kernel_cov": 0.0145401, "gflops": 3926.84, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 3072, "N": 1024, "kv_heads": 0, "op_mean_us": 3690.41, "op_stdev_us": 12.6639, "kernel_mean_us": 3076.16, "kernel_median_us": 3073.8, "kernel_cov": 0.00640426, "gflops": 3491.46, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 3072, "N": 1024, "kv_heads": 0, "op_mean_us": 3727.88, "op_stdev_us": 11.2618, "kernel_mean_us": 3074.22, "kernel_median_us": 3074.28, "kernel_cov": 0.00636324, "gflops": 3456.36, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 3072, "N": 8192, "kv_heads": 0, "op_mean_us": 25158.2, "op_stdev_us": 112.905, "kernel_mean_us": 24538.2, "kernel_median_us": 24486.5, "kernel_cov": 0.00896708, "gflops": 4097.25, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 3072, "N": 8192, "kv_heads": 0, "op_mean_us": 25172.6, "op_stdev_us": 55.6747, "kernel_mean_us": 24514.3, "kernel_median_us": 24522.6, "kernel_cov": 0.00287067, "gflops": 4094.9, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 8192, "N": 3072, "kv_heads": 0, "op_mean_us": 26824.4, "op_stdev_us": 213.958, "kernel_mean_us": 24662.1, "kernel_median_us": 24595.6, "kernel_cov": 0.0102667, "gflops": 3842.74, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 8192, "N": 3072, "kv_heads": 0, "op_mean_us": 27261.6, "op_stdev_us": 386.538, "kernel_mean_us": 24738.3, "kernel_median_us": 24609.1, "kernel_cov": 0.0132468, "gflops": 3781.11, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 2048, "N": 2048, "kv_heads": 0, "op_mean_us": 4331.08, "op_stdev_us": 15.6509, "kernel_mean_us": 4085.46, "kernel_median_us": 4094.84, "kernel_cov": 0.00835203, "gflops": 3966.65, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 2048, "N": 2048, "kv_heads": 0, "op_mean_us": 4398.83, "op_stdev_us": 17.1972, "kernel_mean_us": 4079.88, "kernel_median_us": 4090.64, "kernel_cov": 0.00786503, "gflops": 3905.55, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 2048, "N": 512, "kv_heads": 0, "op_mean_us": 1309.73, "op_stdev_us": 3.44657, "kernel_mean_us": 1065.47, "kernel_median_us": 1065.8, "kernel_cov": 0.00628026, "gflops": 3279.28, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 2048, "N": 512, "kv_heads": 0, "op_mean_us": 1382.63, "op_stdev_us": 5.31418, "kernel_mean_us": 1062.62, "kernel_median_us": 1062.44, "kernel_cov": 0.00622795, "gflops": 3106.37, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 2048, "N": 8192, "kv_heads": 0, "op_mean_us": 16538.2, "op_stdev_us": 25.9625, "kernel_mean_us": 16292.7, "kernel_median_us": 16309.5, "kernel_cov": 0.00362216, "gflops": 4155.19, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 2048, "N": 8192, "kv_heads": 0, "op_mean_us": 16616.7, "op_stdev_us": 42.6883, "kernel_mean_us": 16298.6, "kernel_median_us": 16300.6, "kernel_cov": 0.00352991, "gflops": 4135.56, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half", "M": 2048, "K": 8192, "N": 2048, "kv_heads": 0, "op_mean_us": 18717.5, "op_stdev_us": 91.7867, "kernel_mean_us": 16564.8, "kernel_median_us": 16523.3, "kernel_cov": 0.0071766, "gflops": 3671.4, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "q4gsw_linear_gemm__tin__w_4x8_nc_buffer_half", "M": 2048, "K": 8192, "N": 2048, "kv_heads": 0, "op_mean_us": 19088.1, "op_stdev_us": 28.6891, "kernel_mean_us": 16558, "kernel_median_us": 16547.7, "kernel_cov": 0.00478978, "gflops": 3600.13, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true}
  ]
}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/correctness.log, lines 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, 94, 99, 104, 249, 254, 271-272

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/correctness.log`, lines 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, 94, 99, 104, 249, 254, 271-272

```text
linear_q4gsw_tiled_texture3d_texture2d_half        (8,16,1)        (8,8,1)     linear_q4gsw_M64_K128_N64_Texture3D                                                          [64x128]          25.453 μs         41.196 GFLOP/s   PASSED
linear_q4gsw_tiled_buffer_texture2d_half           (8,16,1)        (8,8,1)     linear_q4gsw_M64_K128_N64_Buffer                                                             [64x128]          20.579 μs         50.953 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K256_N128_Texture3D                                                       [128x256]          26.558 μs        315.861 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K256_N128_Buffer                                                          [128x256]          24.281 μs        345.480 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K128_N128_Texture3D                                                       [128x128]          18.121 μs        231.467 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K128_N128_Buffer                                                          [128x128]          15.746 μs        266.366 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (512,2,1)       (256,1,1)   linear_q4gsw_M256_K256_N256_Texture3D                                                       [256x256]          26.923 μs       1246.296 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (512,2,1)       (256,1,1)   linear_q4gsw_M256_K256_N256_Buffer                                                          [256x256]          25.198 μs       1331.627 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (512,1,1)       (256,1,1)   linear_q4gsw_M128_K128_N256_Texture3D                                                       [128x128]          18.636 μs        450.135 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (512,1,1)       (256,1,1)   linear_q4gsw_M128_K128_N256_Buffer                                                          [128x128]          16.168 μs        518.843 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,2,1)       (256,1,1)   linear_q4gsw_M256_K128_N128_Texture3D                                                       [256x128]          18.451 μs        454.643 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,2,1)       (256,1,1)   linear_q4gsw_M256_K128_N128_Buffer                                                          [256x128]          16.228 μs        516.915 GFLOP/s   PASSED
linear_q4gsw_tiled_texture3d_texture2d_half        (32,16,1)       (8,8,1)     linear_q4gsw_M64_K128_N256_Texture3D                                                         [64x128]          26.298 μs        159.494 GFLOP/s   PASSED
linear_q4gsw_tiled_buffer_texture2d_half           (32,16,1)       (8,8,1)     linear_q4gsw_M64_K128_N256_Buffer                                                            [64x128]          25.026 μs        167.596 GFLOP/s   PASSED
linear_q4gsw_tiled_texture3d_texture2d_half        (8,64,1)        (8,8,1)     linear_q4gsw_M256_K128_N64_Texture3D                                                        [256x128]          22.802 μs        183.946 GFLOP/s   PASSED
linear_q4gsw_tiled_buffer_texture2d_half           (8,64,1)        (8,8,1)     linear_q4gsw_M256_K128_N64_Buffer                                                           [256x128]          21.301 μs        196.903 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K2048_N128_Texture3D                                                     [128x2048]          64.381 μs       1042.371 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K2048_N128_Buffer                                                        [128x2048]          68.003 μs        986.848 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K4096_N128_Texture3D                                                     [128x4096]         110.182 μs       1218.143 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K4096_N128_Buffer                                                        [128x4096]         121.950 μs       1100.593 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K128_N128_rank3batch1_Buffer                                            [1x128x128]           6.277 μs        668.177 GFLOP/s   PASSED
sarc_linear_q4gsw_coopmat_t128x128k32g42s32f..     (256,1,1)       (256,1,1)   linear_q4gsw_M128_K4096_N128_rank3batch1_Buffer                                          [1x128x4096]         121.802 μs       1101.936 GFLOP/s   PASSED
[rank3 batch=1] linear_q4gsw_M128_K128_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/correctness.log, lines 271-275

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/correctness.log`, lines 271-275

```text
[rank3 batch=1] linear_q4gsw_M128_K128_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_dq8ca_q4gsw_M128_K128_N128_rank3batch1_Buffer -> linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8 (NOT coopmat -- fallback), correctness=PASSED
[rank3 batch=1] linear_dq8ca_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8 (NOT coopmat -- fallback), correctness=PASSED
[correctness] FAILED -- numeric failure(s) and/or a rank-3 case did not dispatch coopmat
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.1-8b-4w-buffer.log, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.1-8b-4w-buffer.log`, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

```text
[production-diff] llama-3.1-8b_prefill_wq_wo_linear_q4gsw_M2048_K4096_N4096_rank3batch1_Buffer (M=2048, K=4096, N=4096, group_size=128)
[sampled reference] checking 8200 of 8388608 elements
[sampled reference] max abs diff 0.0259933 (tol 0.5), max rel diff 0.0230018 (tol 0.05, |ref| > abs tol)
[production-diff] llama-3.1-8b_prefill_wq_wo_linear_q4gsw_M2048_K4096_N4096_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_wk_wv_linear_q4gsw_M2048_K4096_N1024_rank3batch1_Buffer (M=2048, K=4096, N=1024, group_size=128)
[sampled reference] checking 8008 of 2097152 elements
[sampled reference] max abs diff 0.022 (tol 0.500), max rel diff 0.011 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.1-8b_prefill_wk_wv_linear_q4gsw_M2048_K4096_N1024_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_w1_w3_linear_q4gsw_M2048_K4096_N14336_rank3batch1_Buffer (M=2048, K=4096, N=14336, group_size=128)
[sampled reference] checking 8254 of 29360128 elements
[sampled reference] max abs diff 0.020 (tol 0.500), max rel diff 0.015 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.1-8b_prefill_w1_w3_linear_q4gsw_M2048_K4096_N14336_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_w2_linear_q4gsw_M2048_K14336_N4096_rank3batch1_Buffer (M=2048, K=14336, N=4096, group_size=128)
[sampled reference] checking 8209 of 8388608 elements
[sampled reference] max abs diff 0.041 (tol 0.500), max rel diff 0.023 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.1-8b_prefill_w2_linear_q4gsw_M2048_K14336_N4096_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.1-8b, 4 shapes, M=2048, linear_q4gsw, buffer)
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.1-8b-4w-texture3d.log, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.1-8b-4w-texture3d.log`, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

```text
[production-diff] llama-3.1-8b_prefill_wq_wo_linear_q4gsw_M2048_K4096_N4096_rank3batch1_Texture3D (M=2048, K=4096, N=4096, group_size=128)
[sampled reference] checking 8200 of 8388608 elements
[sampled reference] max abs diff 0.0259933 (tol 0.5), max rel diff 0.0230018 (tol 0.05, |ref| > abs tol)
[production-diff] llama-3.1-8b_prefill_wq_wo_linear_q4gsw_M2048_K4096_N4096_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_wk_wv_linear_q4gsw_M2048_K4096_N1024_rank3batch1_Texture3D (M=2048, K=4096, N=1024, group_size=128)
[sampled reference] checking 8008 of 2097152 elements
[sampled reference] max abs diff 0.022 (tol 0.500), max rel diff 0.011 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.1-8b_prefill_wk_wv_linear_q4gsw_M2048_K4096_N1024_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_w1_w3_linear_q4gsw_M2048_K4096_N14336_rank3batch1_Texture3D (M=2048, K=4096, N=14336, group_size=128)
[sampled reference] checking 8254 of 29360128 elements
[sampled reference] max abs diff 0.020 (tol 0.500), max rel diff 0.015 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.1-8b_prefill_w1_w3_linear_q4gsw_M2048_K4096_N14336_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_w2_linear_q4gsw_M2048_K14336_N4096_rank3batch1_Texture3D (M=2048, K=14336, N=4096, group_size=128)
[sampled reference] checking 8209 of 8388608 elements
[sampled reference] max abs diff 0.041 (tol 0.500), max rel diff 0.023 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.1-8b_prefill_w2_linear_q4gsw_M2048_K14336_N4096_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.1-8b, 4 shapes, M=2048, linear_q4gsw, texture3d)
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-1b-4w-buffer.log, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-1b-4w-buffer.log`, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

```text
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_q4gsw_M2048_K2048_N2048_rank3batch1_Buffer (M=2048, K=2048, N=2048, group_size=128)
[sampled reference] checking 8161 of 4194304 elements
[sampled reference] max abs diff 0.0195694 (tol 0.5), max rel diff 0.0119457 (tol 0.05, |ref| > abs tol)
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_q4gsw_M2048_K2048_N2048_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_wk_wv_linear_q4gsw_M2048_K2048_N512_rank3batch1_Buffer (M=2048, K=2048, N=512, group_size=128)
[sampled reference] checking 7772 of 1048576 elements
[sampled reference] max abs diff 0.020 (tol 0.500), max rel diff 0.013 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-1b_prefill_wk_wv_linear_q4gsw_M2048_K2048_N512_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_w1_w3_linear_q4gsw_M2048_K2048_N8192_rank3batch1_Buffer (M=2048, K=2048, N=8192, group_size=128)
[sampled reference] checking 8242 of 16777216 elements
[sampled reference] max abs diff 0.019 (tol 0.500), max rel diff 0.011 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-1b_prefill_w1_w3_linear_q4gsw_M2048_K2048_N8192_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_w2_linear_q4gsw_M2048_K8192_N2048_rank3batch1_Buffer (M=2048, K=8192, N=2048, group_size=128)
[sampled reference] checking 8133 of 4194304 elements
[sampled reference] max abs diff 0.034 (tol 0.500), max rel diff 0.019 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-1b_prefill_w2_linear_q4gsw_M2048_K8192_N2048_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_q4gsw, buffer)
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-1b-4w-texture3d.log, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-1b-4w-texture3d.log`, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

```text
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_q4gsw_M2048_K2048_N2048_rank3batch1_Texture3D (M=2048, K=2048, N=2048, group_size=128)
[sampled reference] checking 8161 of 4194304 elements
[sampled reference] max abs diff 0.0195694 (tol 0.5), max rel diff 0.0119457 (tol 0.05, |ref| > abs tol)
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_q4gsw_M2048_K2048_N2048_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_wk_wv_linear_q4gsw_M2048_K2048_N512_rank3batch1_Texture3D (M=2048, K=2048, N=512, group_size=128)
[sampled reference] checking 7772 of 1048576 elements
[sampled reference] max abs diff 0.020 (tol 0.500), max rel diff 0.013 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-1b_prefill_wk_wv_linear_q4gsw_M2048_K2048_N512_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_w1_w3_linear_q4gsw_M2048_K2048_N8192_rank3batch1_Texture3D (M=2048, K=2048, N=8192, group_size=128)
[sampled reference] checking 8242 of 16777216 elements
[sampled reference] max abs diff 0.019 (tol 0.500), max rel diff 0.011 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-1b_prefill_w1_w3_linear_q4gsw_M2048_K2048_N8192_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_w2_linear_q4gsw_M2048_K8192_N2048_rank3batch1_Texture3D (M=2048, K=8192, N=2048, group_size=128)
[sampled reference] checking 8133 of 4194304 elements
[sampled reference] max abs diff 0.034 (tol 0.500), max rel diff 0.019 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-1b_prefill_w2_linear_q4gsw_M2048_K8192_N2048_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_q4gsw, texture3d)
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-3b-4w-buffer.log, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-3b-4w-buffer.log`, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

```text
[production-diff] llama-3.2-3b_prefill_wq_wo_linear_q4gsw_M2048_K3072_N3072_rank3batch1_Buffer (M=2048, K=3072, N=3072, group_size=128)
[sampled reference] checking 8185 of 6291456 elements
[sampled reference] max abs diff 0.0198975 (tol 0.5), max rel diff 0.0134082 (tol 0.05, |ref| > abs tol)
[production-diff] llama-3.2-3b_prefill_wq_wo_linear_q4gsw_M2048_K3072_N3072_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_wk_wv_linear_q4gsw_M2048_K3072_N1024_rank3batch1_Buffer (M=2048, K=3072, N=1024, group_size=128)
[sampled reference] checking 8026 of 2097152 elements
[sampled reference] max abs diff 0.018 (tol 0.500), max rel diff 0.012 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-3b_prefill_wk_wv_linear_q4gsw_M2048_K3072_N1024_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_w1_w3_linear_q4gsw_M2048_K3072_N8192_rank3batch1_Buffer (M=2048, K=3072, N=8192, group_size=128)
[sampled reference] checking 8248 of 16777216 elements
[sampled reference] max abs diff 0.019 (tol 0.500), max rel diff 0.012 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-3b_prefill_w1_w3_linear_q4gsw_M2048_K3072_N8192_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_w2_linear_q4gsw_M2048_K8192_N3072_rank3batch1_Buffer (M=2048, K=8192, N=3072, group_size=128)
[sampled reference] checking 8187 of 6291456 elements
[sampled reference] max abs diff 0.037 (tol 0.500), max rel diff 0.019 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-3b_prefill_w2_linear_q4gsw_M2048_K8192_N3072_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.2-3b, 4 shapes, M=2048, linear_q4gsw, buffer)
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-3b-4w-texture3d.log, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/pdiff-llama-3.2-3b-4w-texture3d.log`, lines 7, 10-11, 15-16, 19-20, 24-25, 28-29, 33-34, 37-38, 42-43

```text
[production-diff] llama-3.2-3b_prefill_wq_wo_linear_q4gsw_M2048_K3072_N3072_rank3batch1_Texture3D (M=2048, K=3072, N=3072, group_size=128)
[sampled reference] checking 8185 of 6291456 elements
[sampled reference] max abs diff 0.0198975 (tol 0.5), max rel diff 0.0134082 (tol 0.05, |ref| > abs tol)
[production-diff] llama-3.2-3b_prefill_wq_wo_linear_q4gsw_M2048_K3072_N3072_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_wk_wv_linear_q4gsw_M2048_K3072_N1024_rank3batch1_Texture3D (M=2048, K=3072, N=1024, group_size=128)
[sampled reference] checking 8026 of 2097152 elements
[sampled reference] max abs diff 0.018 (tol 0.500), max rel diff 0.012 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-3b_prefill_wk_wv_linear_q4gsw_M2048_K3072_N1024_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_w1_w3_linear_q4gsw_M2048_K3072_N8192_rank3batch1_Texture3D (M=2048, K=3072, N=8192, group_size=128)
[sampled reference] checking 8248 of 16777216 elements
[sampled reference] max abs diff 0.019 (tol 0.500), max rel diff 0.012 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-3b_prefill_w1_w3_linear_q4gsw_M2048_K3072_N8192_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_w2_linear_q4gsw_M2048_K8192_N3072_rank3batch1_Texture3D (M=2048, K=8192, N=3072, group_size=128)
[sampled reference] checking 8187 of 6291456 elements
[sampled reference] max abs diff 0.037 (tol 0.500), max rel diff 0.019 (tol 0.050, |ref| > abs tol)
[production-diff] llama-3.2-3b_prefill_w2_linear_q4gsw_M2048_K8192_N3072_rank3batch1_Texture3D -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.2-3b, 4 shapes, M=2048, linear_q4gsw, texture3d)
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-default.log, line 6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":1915.81,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542738120,"model_load_end_ms":1790542738521,"inference_start_ms":1790542739623,"inference_end_ms":1790542740692,"model_execution_start_ms":1790542739626,"model_execution_end_ms":1790542740691,"prompt_eval_end_ms":1790542740692,"first_token_ms":1790542740692,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1065,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-tiled.log, line 6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":714.336,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542725895,"model_load_end_ms":1790542726199,"inference_start_ms":1790542729099,"inference_end_ms":1790542731966,"model_execution_start_ms":1790542729102,"model_execution_end_ms":1790542731966,"prompt_eval_end_ms":1790542731966,"first_token_ms":1790542731966,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2864,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-default.log, line 6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":683.35,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542764870,"model_load_end_ms":1790542765625,"inference_start_ms":1790542768679,"inference_end_ms":1790542771676,"model_execution_start_ms":1790542768682,"model_execution_end_ms":1790542771676,"prompt_eval_end_ms":1790542771676,"first_token_ms":1790542771676,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2994,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-tiled.log, line 6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-3b-4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":246.065,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542747313,"model_load_end_ms":1790542748129,"inference_start_ms":1790542756434,"inference_end_ms":1790542764757,"model_execution_start_ms":1790542756438,"model_execution_end_ms":1790542764757,"prompt_eval_end_ms":1790542764757,"first_token_ms":1790542764757,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":8319,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-default.log, line 6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":351.951,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542814125,"model_load_end_ms":1790542817191,"inference_start_ms":1790542823049,"inference_end_ms":1790542828868,"model_execution_start_ms":1790542823052,"model_execution_end_ms":1790542828868,"prompt_eval_end_ms":1790542828868,"first_token_ms":1790542828868,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":5816,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-tiled.log, line 6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-8b-4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":104.357,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542771780,"model_load_end_ms":1790542774837,"inference_start_ms":1790542794386,"inference_end_ms":1790542814011,"model_execution_start_ms":1790542794389,"model_execution_end_ms":1790542814010,"prompt_eval_end_ms":1790542814011,"first_token_ms":1790542814011,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":19621,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/check-1b-4w-default.log, line 140

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/check-1b-4w-default.log`, line 140

```text
PyTorchObserver {"prefill_token_per_sec":713.975,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790542740787,"model_load_end_ms":1790542741136,"inference_start_ms":1790542741136,"inference_end_ms":1790542743898,"model_execution_start_ms":1790542741140,"model_execution_end_ms":1790542743897,"prompt_eval_end_ms":1790542743898,"first_token_ms":1790542743898,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2757,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/check-1b-4w-tiled.log, line 140

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/check-1b-4w-tiled.log`, line 140

```text
PyTorchObserver {"prefill_token_per_sec":723.139,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790542732061,"model_load_end_ms":1790542732410,"inference_start_ms":1790542732410,"inference_end_ms":1790542735137,"model_execution_start_ms":1790542732414,"model_execution_end_ms":1790542735137,"prompt_eval_end_ms":1790542735137,"first_token_ms":1790542735137,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2723,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/unaligned-1b-4w-default.log, line 7

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/unaligned-1b-4w-default.log`, line 7

```text
PyTorchObserver {"prefill_token_per_sec":2064.52,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790542743990,"model_load_end_ms":1790542744347,"inference_start_ms":1790542744347,"inference_end_ms":1790542745215,"model_execution_start_ms":1790542744352,"model_execution_end_ms":1790542745215,"prompt_eval_end_ms":1790542745215,"first_token_ms":1790542745215,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":863,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/unaligned-1b-4w-tiled.log, line 7

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/unaligned-1b-4w-tiled.log`, line 7

```text
PyTorchObserver {"prefill_token_per_sec":731.727,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790542735229,"model_load_end_ms":1790542735579,"inference_start_ms":1790542735579,"inference_end_ms":1790542738028,"model_execution_start_ms":1790542735583,"model_execution_end_ms":1790542738028,"prompt_eval_end_ms":1790542738028,"first_token_ms":1790542738028,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2445,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/decode-1b-4w.log, line 9

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/decode-1b-4w.log`, line 9

```text
PyTorchObserver {"prefill_token_per_sec":1853.39,"decode_token_per_sec":70.7763,"prompt_tokens":2048,"generated_tokens":31,"model_load_start_ms":1790542745310,"model_load_end_ms":1790542745672,"inference_start_ms":1790542745672,"inference_end_ms":1790542747215,"model_execution_start_ms":1790542747201,"model_execution_end_ms":1790542747214,"prompt_eval_end_ms":1790542746777,"first_token_ms":1790542746777,"aggregate_sampling_time_ms":13,"aggregate_model_execution_time_ms":1522,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-1b-4w-default.log, line 5

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-1b-4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":1204.71,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542921975,"model_load_end_ms":1790542922293,"inference_start_ms":1790542924035,"inference_end_ms":1790542925735,"model_execution_start_ms":1790542924037,"model_execution_end_ms":1790542925735,"prompt_eval_end_ms":1790542925735,"first_token_ms":1790542925735,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1698,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-3b-4w-default.log, line 5

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-3b-4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":421.486,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542932356,"model_load_end_ms":1790542933215,"inference_start_ms":1790542938104,"inference_end_ms":1790542942963,"model_execution_start_ms":1790542938107,"model_execution_end_ms":1790542942963,"prompt_eval_end_ms":1790542942963,"first_token_ms":1790542942963,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":4856,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-8b-4w-default.log, line 5

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-8b-4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":193.829,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790542943077,"model_load_end_ms":1790542946210,"inference_start_ms":1790542956704,"inference_end_ms":1790542967270,"model_execution_start_ms":1790542956707,"model_execution_end_ms":1790542967270,"prompt_eval_end_ms":1790542967270,"first_token_ms":1790542967270,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":10563,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/check-1b-4w-default.log, line 139

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/check-1b-4w-default.log`, line 139

```text
PyTorchObserver {"prefill_token_per_sec":1246.52,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790542925829,"model_load_end_ms":1790542926190,"inference_start_ms":1790542926190,"inference_end_ms":1790542927772,"model_execution_start_ms":1790542926194,"model_execution_end_ms":1790542927772,"prompt_eval_end_ms":1790542927772,"first_token_ms":1790542927772,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1578,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/unaligned-1b-4w-default.log, line 6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/unaligned-1b-4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":1271.82,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790542927864,"model_load_end_ms":1790542928213,"inference_start_ms":1790542928213,"inference_end_ms":1790542929622,"model_execution_start_ms":1790542928217,"model_execution_end_ms":1790542929622,"prompt_eval_end_ms":1790542929622,"first_token_ms":1790542929622,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1405,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/decode-1b-4w.log, line 9

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/stock/decode-1b-4w.log`, line 9

```text
PyTorchObserver {"prefill_token_per_sec":1174.99,"decode_token_per_sec":69.5067,"prompt_tokens":2048,"generated_tokens":31,"model_load_start_ms":1790542929715,"model_load_end_ms":1790542930068,"inference_start_ms":1790542930068,"inference_end_ms":1790542932257,"model_execution_start_ms":1790542932242,"model_execution_end_ms":1790542932256,"prompt_eval_end_ms":1790542931811,"first_token_ms":1790542931811,"aggregate_sampling_time_ms":10,"aggregate_model_execution_time_ms":2176,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-1b-4w-default.log, line 5

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-1b-4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":1930.25,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790543608386,"model_load_end_ms":1790543608748,"inference_start_ms":1790543609851,"inference_end_ms":1790543610912,"model_execution_start_ms":1790543609854,"model_execution_end_ms":1790543610912,"prompt_eval_end_ms":1790543610912,"first_token_ms":1790543610912,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1058,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-3b-4w-default.log, line 5

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-3b-4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":689.795,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790543617454,"model_load_end_ms":1790543618274,"inference_start_ms":1790543621277,"inference_end_ms":1790543624246,"model_execution_start_ms":1790543621280,"model_execution_end_ms":1790543624245,"prompt_eval_end_ms":1790543624246,"first_token_ms":1790543624246,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2965,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-8b-4w-default.log, line 5

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/release/prefill-8b-4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":352.193,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790543624357,"model_load_end_ms":1790543627250,"inference_start_ms":1790543633098,"inference_end_ms":1790543638913,"model_execution_start_ms":1790543633101,"model_execution_end_ms":1790543638913,"prompt_eval_end_ms":1790543638913,"first_token_ms":1790543638913,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":5812,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/release/check-1b-4w-default.log, line 139

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/release/check-1b-4w-default.log`, line 139

```text
PyTorchObserver {"prefill_token_per_sec":728.482,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790543611006,"model_load_end_ms":1790543611353,"inference_start_ms":1790543611353,"inference_end_ms":1790543614060,"model_execution_start_ms":1790543611357,"model_execution_end_ms":1790543614060,"prompt_eval_end_ms":1790543614060,"first_token_ms":1790543614060,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":2703,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/release/unaligned-1b-4w-default.log, line 6

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/release/unaligned-1b-4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":2069.28,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790543614153,"model_load_end_ms":1790543614499,"inference_start_ms":1790543614499,"inference_end_ms":1790543615365,"model_execution_start_ms":1790543614502,"model_execution_end_ms":1790543615365,"prompt_eval_end_ms":1790543615365,"first_token_ms":1790543615365,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":863,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: openspec/changes/sarc-1.5-bootstrap/results/780m/release/decode-1b-4w.log, line 8

Locator: `openspec/changes/sarc-1.5-bootstrap/results/780m/release/decode-1b-4w.log`, line 8

```text
PyTorchObserver {"prefill_token_per_sec":1851.72,"decode_token_per_sec":73.4597,"prompt_tokens":2048,"generated_tokens":31,"model_load_start_ms":1790543615460,"model_load_end_ms":1790543615827,"inference_start_ms":1790543615827,"inference_end_ms":1790543617355,"model_execution_start_ms":1790543617341,"model_execution_end_ms":1790543617354,"prompt_eval_end_ms":1790543616933,"first_token_ms":1790543616933,"aggregate_sampling_time_ms":15,"aggregate_model_execution_time_ms":1508,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Excerpt: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 19-41

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp`, lines 19-41

```cpp
// The shipped RDNA coopmat variants were built and validated for wave64
// adapters that support cooperative matrix; they force subgroup 32 per
// pipeline (SUBGROUP_SIZE in the yaml).
bool amd_wave64(const DeviceInfo& d) {
  return d.is_amd && d.subgroup_size == 64;
}

// t128x128k32g42s32 with fp32 accumulate and the drain staged in Ash.
constexpr TileDims k780mDims = {128, 128, 32, 4, 2, 32, 16, true};

const Row kAmdRows[] = {
    // Radeon 780M (gfx1103, RADV, Mesa 25.2.7). Verified on release 1.5
    // (openspec/changes/sarc-1.5-bootstrap/results/780m): 2048-token prefill
    // 1B/3B/8B 1916/683/352 tok/s vs stock 1.5 1205/421/194; kernel times
    // within -1.6..-0.2 % of the 1.4 study; next token == tiled; pdiff pass.
    {"780m",
     amd_wave64,
     Op::kQ4gswLinear,
     "sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c",
     k780mDims,
     kTex3dTex2d | kBufTex2d | kBufBuf,
     /*shape_ok=*/nullptr,
     Status::kVerified},
```

## Excerpt: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 46-53

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp`, lines 46-53

```cpp
    {"780m",
     amd_wave64,
     Op::kDq8caLinear,
     "sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32",
     {128, 64, 32, 4, 2, 32, 16, false},
     kTex3dTex2d | kBufTex2d,
     nullptr,
     Status::kVerified},
```

## Excerpt: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 81-96

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp`, lines 81-96

```cpp
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

## Excerpt: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h, lines 48-58

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/Select.h`, lines 48-58

```cpp
struct DeviceInfo {
  std::string name; // lower-case
  bool is_amd = false;
  uint32_t subgroup_size = 0; // default subgroup size
  uint32_t min_subgroup_size = 0;
  uint32_t max_subgroup_size = 0;
  bool subgroup_size_control = false; // VK_EXT_subgroup_size_control
  bool coopmat = false;
  bool int8_coopmat = false; // an int8 cooperative-matrix shape is enumerated
  uint32_t max_shared_bytes = 0;
};
```

## Excerpt: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h, lines 80-88

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/Select.h`, lines 80-88

```cpp
struct TileDims {
  uint32_t m;
  uint32_t n;
  uint32_t k;
  uint32_t sg_grid_x;
  uint32_t sg_grid_y;
  uint32_t subgroup_size;
  uint32_t mma_m;
  bool csh_in_ash; // texture3d drain staged in Ash (no extra Csh LDS)
```

## Excerpt: sarc/README.md, lines 18-24

Locator: `sarc/README.md`, lines 18-24

```text
- **Kernel selection**: `impl/sarc/Select.{h,cpp}` with per-vendor tables in `impl/sarc/table_<vendor>.cpp`.
  - A row is `{device substring, device predicate, op, kernel base name, tile dims, storage-combination mask, shape predicate, status, rowmajor_a}`; rows are tried in order.
  - `kUnverified` rows are inert in a release. In a dev build, `ET_VK_SARC_UNVERIFIED=1` enables them.
  - Launch dims come from the row. Nothing parses kernel names.
- **Op hooks**: `impl/sarc/Q4gswCoopmat.cpp` builds 4w linear on the SARC path when the device has an active row.
  - For shapes no row covers, it falls back to release 1.5's own `linear_q4gsw_{tiled,coop}` kernels: decode, unaligned M, bias, fp32.
  - It is called from `Q4gswLinear.cpp:q4gsw_linear` (listed in `sarc/HOOKS`).
```

## Excerpt: sarc/README.md, lines 34-37

Locator: `sarc/README.md`, lines 34-37

```text
- **Dev overrides**: `impl/sarc_dev/Overrides.cpp` holds the env vars:
  - `ET_VK_SARC_UNVERIFIED`;
  - `ET_VK_FORCE_TILED_LINEAR` (tiled baseline);
  - `ET_VK_SARC_Q4GSW_VARIANT=<tile>` (sweep; also builds 4w on the SARC path on devices without rows);
```

## Excerpt: sarc/README.md, lines 61-71

Locator: `sarc/README.md`, lines 61-71

```text
## Promotion checklist (one PR into dev/1.5)

1. Move the variant block from the `sarc_dev` sweep yaml to the release yaml, renamed `sarc_<family>_<tile>_<io>_<weight>_<dtype>`.
2. Add a row to `table_<vendor>.cpp`, or flip its status to `kVerified`, and extend `test_sarc_select` with the device fixture.
3. Build with `build.sh`, then run `verify.sh` on the device. Required evidence:
   - the dispatched kernel names;
   - microbench correctness;
   - production-diff for 1B/3B/8B × buffer/texture3d, with nonzero zp for 8da4w;
   - e2e prefill tok/s (tiled vs default);
   - next token == tiled on the real-text and the unaligned prompt;
   - decode.
```

## Excerpt: sarc/README.md, lines 80-82

Locator: `sarc/README.md`, lines 80-82

```text
| Device | 4w | 8da4w | SDPA prefill | Evidence |
|---|---|---|---|---|
| Radeon 780M | verified | verified | verified | `openspec/changes/sarc-1.5-{bootstrap,8da4w-port,sdpa-port}` |
```

## Excerpt: sarc/SWEEP-PARAMETERS.md, lines 8-10

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 8-10

```text
| Scheme | Family | Activation layout |
|---|---|---|
| 4w | `sarc_linear_q4gsw_coopmat` | fp16 |
```

## Excerpt: sarc/SWEEP-PARAMETERS.md, lines 22-26, 29-32

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 22-26, 29-32

```text
| Parameter | Meaning | Values used so far |
|---|---|---|
| `WG_TILE_M`, `WG_TILE_N` | Output tile per workgroup | M 32/64/128/256; N 32/64/128/256 (32 only in sweep candidates) |
| `WG_TILE_K` | K consumed per main-loop iteration | 16 / 32 / 64 |
| `SG_GRID_X`, `SG_GRID_Y` | Subgroup grid in the workgroup (X along N, Y along M); workgroup size = X·Y·`SUBGROUP_SIZE` | 2×1, 2×2, 4×2, 2×4, 4×4, 4×8 |
| `IO_STORAGE` | Input and output tensor storage | `buffer`, `texture3d` |
| `WEIGHT_STORAGE` | Packed weight storage | `texture2d`, `buffer` |
| `HAS_BIAS` | Bias epilogue | only `false` is shipped; the selector never picks SARC for linears with bias |
| `PRECISION` | GLSL default precision | `highp` |
```

## Excerpt: sarc/SWEEP-PARAMETERS.md, lines 38-39, 43

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 38-39, 43

```text
| Flag | Effect | Used by |
|---|---|---|
| `CSH_IN_ASH` | texture3d output drain staged in the dead A shared-memory region | 780M (less LDS, higher occupancy) |
```

## Excerpt: sarc/SWEEP-PARAMETERS.md, lines 74-81

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 74-81

```text
The shaders contain no shape checks. `sarc::select()` enforces these when it matches a row:
- `M % WG_TILE_M == 0`, `N % WG_TILE_N == 0`, `K % WG_TILE_K == 0`;
- `group_size % WG_TILE_K == 0`;
- no bias, batch 1, not a single-token (gemv) call;
- the storage combination is allowed by the row's `storages` mask;
- `SUBGROUP_SIZE` equals the device's subgroup size, or lies within its supported range when subgroup-size
  control is available;
- shared memory fits the device limit (`max_compute_shared_memory_size`).
```

## Excerpt: sarc/SWEEP-PARAMETERS.md, lines 91-104

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 91-104

```text
Names follow the pattern `<family>[_sweep]_<tile>_<io>_<weight>_half`. For example,
`sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_texture3d_texture2d_half` has:
- `IO_STORAGE` texture3d;
- `WEIGHT_STORAGE` texture2d;
- the tile token `t128x128k32g42s32f32c`, decoded below.

| Token part | Meaning |
|---|---|
| `t<M>x<N>` | `WG_TILE_M` × `WG_TILE_N` |
| `k<K>` | `WG_TILE_K` |
| `g<X><Y>` | `SG_GRID_X`, `SG_GRID_Y` |
| `s<S>` | `SUBGROUP_SIZE` |
| `f32` | `ACC_FP32` |
| `c` | `CSH_IN_ASH` (4w) |
```

## Excerpt: sarc/SWEEP-PARAMETERS.md, lines 125-127

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 125-127

```text
| Device | 4w | 8da4w |
|---|---|---|
| Radeon 780M | `t128x128k32g42s32f32c` | zpg `t128x64k32g42s32` + `A_MAP_FULL` |
```

## Excerpt: sarc/SWEEP-PARAMETERS.md, lines 153-154

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 153-154

```text
- `ET_VK_SARC_UNVERIFIED=1` activates `kUnverified` rows.
- `ET_VK_FORCE_TILED_LINEAR=1` sends the SARC linears to release 1.5's tiled/coop kernels, as the baseline.
```
