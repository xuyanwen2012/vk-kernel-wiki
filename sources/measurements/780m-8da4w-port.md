---
id: meas-780m-8da4w-port
title: "Radeon 780M 8da4w (dq8ca) linear coopmat port to release 1.5 (sarc-1.5-8da4w-port): microbench, correctness, production-diff, end-to-end prefill"
source_category: measurement
architectures: [radeon-780m]
tags: [linear-8da4w, linear-8da4w-zpg, tiled-linear, quantize-and-pack, prefill, decode, cooperative-matrix, subgroup-size, wave64, shared-memory-limit, storage-buffer, storage-texture3d, storage-texture2d, workgroup-tile-sizing, required-subgroup-size, full-a-map, zero-point-hoisting, double-buffering]
device: radeon-780m
driver: "RADV Mesa 25.2.7"
measured_at: '2026-09-27'
method: "Two runs on the device with output directories sarc8 and stock8. The result set does not record the command line. The output file names and the summary-line formats of run8.out match sarc/tools/verify.sh at the cited commit; run8.out also contains the lines '---- stock' and 'ALLDONE', which that script does not print, and the binaries predate the kernel rename. The steps of that script, per run: test_llama_microbench --correctness-only; test_llama_microbench --linear --regime=prefill --scheme=8da4w --skip-correctness (the logs record 3 warmup + 5 timed runs per case, linear group_size=128, prefill M=2048, 24 cases); llama_main end-to-end runs with --temperature 0 (prompt_2048.txt, 1 new token, --warmup, value = prefill_token_per_sec of the PyTorchObserver line; for 1B also a check prompt and an unaligned prompt without --warmup, and a 32-new-token decode run). The sarc8 run has ET_VK_SARC_UNVERIFIED=1 in its env.txt, runs each end-to-end case in tiled mode (ET_VK_FORCE_TILED_LINEAR=1) and default mode, compares the generated text of the two modes, and runs the sampled production-diff (--production-diff, --production-diff-nonzero-zp; 3 models x buffer/texture3d, 4 shapes each). The stock8 run has no ET_VK_SARC_UNVERIFIED line in its env.txt and runs default mode only; both env.txt files list the same sha256 values for test_llama_microbench, llama_main and libllama_runner.so. The production-diff was run again after the kernels were renamed (results/780m/pdiff2); those logs carry no timestamp of their own. Single run per case; the result set records no driver version: the driver version is attributed from the package install history captured on the device on 2026-10-04 (see raw_data), not recorded by the runs. Excerpt lines that contain a host name, and lines that name other devices, are omitted from this page."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log
    description: "Microbench log, sarc8 run: 24 prefill 8da4w linear cases"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json
    description: "Microbench JSON, sarc8 run: per-case kernel name, op and kernel times"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.log
    description: "Microbench log, stock8 run: 24 prefill 8da4w linear cases"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt
    description: "Environment of the sarc8 run: UTC timestamp, ET_VK/ETVK variables, binary sha256 values"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/done.txt
    description: "End timestamp of the stock8 run"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/proposal.md
    description: "Change proposal: kernel row, results table (2026-09-27), production-diff, next-token and decode notes"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out
    description: "Console summary lines: sarc8 run block, then stock8 run block (formats match the echo statements of sarc/tools/verify.sh; also holds the lines '---- stock' and 'ALLDONE', which that script does not print)"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/done.txt
    description: "End timestamp of the sarc8 run"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/env.txt
    description: "Environment of the stock8 run: UTC timestamp, ET_VK/ETVK variables, binary sha256 values"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: sarc/tools/verify.sh
    description: "Verification script at the cited commit whose output file names and summary-line formats match the result set; the result set does not record the command line"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json
    description: "Microbench JSON, stock8 run: per-case kernel name, op and kernel times"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-1b-8da4w-default.log
    description: "llama_main prefill log, sarc8 run, 1b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-1b-8da4w-tiled.log
    description: "llama_main prefill log, sarc8 run, 1b 8da4w, tiled mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-3b-8da4w-default.log
    description: "llama_main prefill log, sarc8 run, 3b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-3b-8da4w-tiled.log
    description: "llama_main prefill log, sarc8 run, 3b 8da4w, tiled mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-8b-8da4w-default.log
    description: "llama_main prefill log, sarc8 run, 8b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-8b-8da4w-tiled.log
    description: "llama_main prefill log, sarc8 run, 8b 8da4w, tiled mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/prefill-1b-8da4w-default.log
    description: "llama_main prefill log, stock8 run, 1b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/prefill-3b-8da4w-default.log
    description: "llama_main prefill log, stock8 run, 3b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/prefill-8b-8da4w-default.log
    description: "llama_main prefill log, stock8 run, 8b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/decode-1b-8da4w.log
    description: "llama_main decode log, sarc8 run, 1b 8da4w"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/decode-1b-8da4w.log
    description: "llama_main decode log, stock8 run, 1b 8da4w"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/check-1b-8da4w-default.log
    description: "llama_main check log, sarc8 run, 1b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/check-1b-8da4w-tiled.log
    description: "llama_main check log, sarc8 run, 1b 8da4w, tiled mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/check-1b-8da4w-default.log
    description: "llama_main check log, stock8 run, 1b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/unaligned-1b-8da4w-default.log
    description: "llama_main unaligned log, sarc8 run, 1b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/unaligned-1b-8da4w-tiled.log
    description: "llama_main unaligned log, sarc8 run, 1b 8da4w, tiled mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/unaligned-1b-8da4w-default.log
    description: "llama_main unaligned log, stock8 run, 1b 8da4w, default mode"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/correctness.log
    description: "Microbench correctness log, sarc8 run"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/correctness.log
    description: "Microbench correctness log, stock8 run"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/pdiff-llama-3.2-1b-8da4w-buffer.log
    description: "First production-diff run (kernel names before the rename), llama-3.2-1b buffer"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log
    description: "Production-diff re-run, llama-3.2-1b, buffer: 4 shapes, max abs diff and dispatched kernel per case"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-texture3d.log
    description: "Production-diff re-run, llama-3.2-1b, texture3d: 4 shapes, max abs diff and dispatched kernel per case"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-3b-8da4w-buffer.log
    description: "Production-diff re-run, llama-3.2-3b, buffer: 4 shapes, max abs diff and dispatched kernel per case"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-3b-8da4w-texture3d.log
    description: "Production-diff re-run, llama-3.2-3b, texture3d: 4 shapes, max abs diff and dispatched kernel per case"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-buffer.log
    description: "Production-diff re-run, llama-3.1-8b, buffer: 4 shapes, max abs diff and dispatched kernel per case"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-texture3d.log
    description: "Production-diff re-run, llama-3.1-8b, texture3d: 4 shapes, max abs diff and dispatched kernel per case"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp
    description: "AMD selection rows, including the 780M 8da4w row"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h
    description: "Selection row types: TileDims field order, storage sets"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.yaml
    description: "Shipped zpg shader variants and parameter defaults"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl
    description: "zpg shader template header"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh
    description: "zpg kernel body"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: sarc/SWEEP-PARAMETERS.md
    description: "Shader parameter reference: zpg parameters, preconditions, variant naming, shipped variants"
  - repo: https://github.com/sarc-acl/executorch
    commit: ef079ac41fd09f01656e1ab46c87ca85be6c54ae
    locator: sarc/README.md
    description: "SARC readme: device status table"
  - locator: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt
    description: "Package install history and boot history captured on the device on 2026-10-04; basis of the driver version and kernel version attributed to this result set"
captured_at: '2026-10-04'
baseline: "the stock8 run (labelled 'stock' in run8.out and 'stock 1.5' in proposal.md; dispatches linear_dq8ca_q4gsw_tiled_* for 8da4w) and the tiled mode of the sarc8 run (ET_VK_FORCE_TILED_LINEAR=1)"
description: "Verbatim excerpts for the Radeon 780M result set of the 8da4w port to release 1.5: dispatched kernel names, 24-case prefill linear microbench for the sarc8 and stock8 runs, correctness and production-diff logs, end-to-end 2048-token prefill and decode tok/s for Llama 3.2 1B / 3.2 3B / 3.1 8B, the selection row and the shader parameters of the shipped zpg variant."
---

## Environment / driver attribution

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log`, line 5 (the result set's own device line; it names the driver as `radv phoenix` and records no driver version)

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json`, line 3 (same device string in the JSON result file; no driver version)

```text
  "device": "amd radeon 780m graphics (radv phoenix)",
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.log`, line 4 (device line of the stock8 run; no driver version)

```text
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt`, line 1 (start timestamp of the sarc8 run, written by `date -u`)

```text
Sun Sep 27 10:09:35 PM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/done.txt`, line 1 (end timestamp of the stock8 run, written by `date -u`)

```text
Sun Sep 27 10:13:40 PM UTC 2026
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, line 1 (file in this repository; header line of the capture)

```text
# Captured 2026-10-04 on the Radeon 780M host. Commands and their verbatim output.
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 3-5 (file in this repository; the driver version in this page's `driver` field is attributed from this install history, it is not recorded by the run)

```text
$ rpm -q --qf "%{NAME}-%{VERSION}-%{RELEASE} installed %{INSTALLTIME:date} built %{BUILDTIME:date}\n" mesa-vulkan-drivers mesa-dri-drivers
mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1 installed Fri 29 May 2026 10:08:07 PM PDT built Wed 25 Feb 2026 06:58:58 AM PST
mesa-dri-drivers-25.2.7-4.el10.rocky.0.1 installed Fri 29 May 2026 10:08:06 PM PDT built Wed 25 Feb 2026 06:58:58 AM PST
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 7-8 (file in this repository; package that owns the RADV driver library)

```text
$ rpm -qf /usr/lib64/libvulkan_radeon.so
mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1.x86_64
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 10-14 (file in this repository; the command and its complete output: every package-log entry for these two packages)

```text
$ grep -h -E "mesa-(vulkan|dri)-drivers" /var/log/dnf.rpm.log*
2026-05-29T22:08:06-0700 SUBDEBUG Upgrade: mesa-dri-drivers-25.2.7-4.el10.rocky.0.1.x86_64
2026-05-29T22:08:06-0700 SUBDEBUG Upgrade: mesa-vulkan-drivers-25.2.7-4.el10.rocky.0.1.x86_64
2026-05-29T22:10:09-0700 SUBDEBUG Upgraded: mesa-vulkan-drivers-25.0.7-6.el10_1.x86_64
2026-05-29T22:10:20-0700 SUBDEBUG Upgraded: mesa-dri-drivers-25.0.7-6.el10_1.x86_64
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 16-18 (file in this repository; oldest entry of the retained package log)

```text
$ ls /var/log/dnf.rpm.log*   (oldest entry of the retained log)
/var/log/dnf.rpm.log
2026-02-23T19:29:04-0800 INFO --- logging initialized ---
```

Locator: `sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`, lines 20-26 (file in this repository; boot history; the kernel field is truncated by `last` and the lines carry no time zone; `kernel_version` is not set in this page's frontmatter)

```text
$ last reboot | head -6
reboot   system boot  6.12.0-211.61.1. Thu Oct  1 09:52   still running
reboot   system boot  6.12.0-211.60.1. Sat Sep 26 21:45 - 09:52 (4+12:07)
reboot   system boot  6.12.0-211.58.1. Thu Sep 24 07:00 - 21:44 (2+14:44)
reboot   system boot  6.12.0-211.56.1. Wed Sep 23 20:59 - 06:59  (10:00)
reboot   system boot  6.12.0-211.56.1. Sat Sep 19 13:56 - crash (4+07:02)
reboot   system boot  6.12.0-211.55.1. Wed Sep 16 13:46 - 13:56 (3+00:10)
```

## proposal.md: purpose of the change

Locator: `openspec/changes/sarc-1.5-8da4w-port/proposal.md`, lines 5-6

```text
This change ports the 8da4w (dq8ca: dynamic int8 activations, 4-bit weights) coopmat winners of the
release-1.4 SARC branches to release 1.5.
```

## proposal.md: op path

Locator: `openspec/changes/sarc-1.5-8da4w-port/proposal.md`, lines 17-20

```text
**Op path:** `impl/sarc/Dq8caCoopmat.cpp`, hooked into `linear_dq8ca_q4gsw`.
- The activation layout follows the kernel chosen for the build-time shape.
- A row-major op keeps its kernel for every M (the unaligned-M fix).
- A 4h4w op falls back to release 1.5's dq8ca tiled/coop kernels.
```

## proposal.md: device row for the 780M

Locator: `openspec/changes/sarc-1.5-8da4w-port/proposal.md`, lines 24-26

```text
| Device | Kernel |
|---|---|
| 780M | zpg t128x64k32g42s32 |
```

## proposal.md: results heading, definitions and the 780M row

Locator: `openspec/changes/sarc-1.5-8da4w-port/proposal.md`, lines 34-43

```text
## Results (2026-09-27; release 1.5, 2048-token prefill tok/s, 1B / 3B / 8B)

Logs are in `results/<gpu>`.
- Kernel ratio: microbench kernel median against the 1.4 confirmation, 24 shapes.
- "1.4 tuned" is the 1.4 branch's end-to-end result. On the 780M it includes the SARC SDPA coopmat,
  which this change does not contain.

| GPU | tiled | stock 1.5 | SARC | SARC / stock | 1.4 tuned | kernel ratio vs 1.4 |
|---|---|---|---|---|---|---|
| Radeon 780M | 1631 / 566 / 280 | 1624 / 569 / 281 | 1845 / 649 / 336 | 1.14 / 1.14 / 1.20× | 2538 / 1055 / 486 | 0.992 (0.985–1.002) |
```

## proposal.md: production-diff

Locator: `openspec/changes/sarc-1.5-8da4w-port/proposal.md`, lines 49-53

```text
**Production-diff (1B/3B/8B × buffer/texture3d, non-zero activation zero points):**
- Every case is numerically within tolerance on all five GPUs (for example, 780M max |err| 0.016–0.124
  against 0.5).
- The first run reported FAILED only because the harness saw no "coopmat" in the old
  `sarc_linear_dq8ca_zpg*` names. The kernels have been renamed, and the re-run is in `results/*/pdiff2`.
```

## proposal.md: next token vs tiled

Locator: `openspec/changes/sarc-1.5-8da4w-port/proposal.md`, lines 55-56

```text
**Next token vs tiled:**
- The 1973-token real-text prompt matches on all five GPUs.
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/proposal.md`, lines 59-60 (lines 57-58, which open this bullet, name other devices and are not excerpted)

```text
  780M: 1.4 tiled, 1.4 tuned and 1.5 SARC all give the same token, and only 1.5 tiled flips.
  Production-diff is within tolerance. This is a near-tie flip in 1.5's tiled path, not a port error.
```

## proposal.md: decode

Locator: `openspec/changes/sarc-1.5-8da4w-port/proposal.md`, line 62

```text
**Decode:** works on all five GPUs.
```

## run8.out: console summary lines, sarc8 run then stock8 run

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out`, lines 1-25

```text
correctness rc=1 [correctness] FAILED -- numeric failure(s) and/or a rank-3 case did not dispatch coopmat
linear 8da4w rc=1 kernels:  12 "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half"; 12 "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half";
1b 8da4w tiled prefill_tok_s=1630.57
1b 8da4w default prefill_tok_s=1845.05
1b 8da4w check: default vs tiled output SAME
1b 8da4w unaligned: default vs tiled output DIFFER
1b 8da4w decode rc=0 "generated_tokens":31 decode_tok_s=69.3512
3b 8da4w tiled prefill_tok_s=565.902
3b 8da4w default prefill_tok_s=649.128
8b 8da4w tiled prefill_tok_s=279.743
8b 8da4w default prefill_tok_s=336.068
pdiff llama-3.2-1b 8da4w buffer rc=1 [production-diff] FAILED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
pdiff llama-3.2-1b 8da4w texture3d rc=1 [production-diff] FAILED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
pdiff llama-3.2-3b 8da4w buffer rc=1 [production-diff] FAILED (llama-3.2-3b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
pdiff llama-3.2-3b 8da4w texture3d rc=1 [production-diff] FAILED (llama-3.2-3b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
pdiff llama-3.1-8b 8da4w buffer rc=1 [production-diff] FAILED (llama-3.1-8b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
pdiff llama-3.1-8b 8da4w texture3d rc=1 [production-diff] FAILED (llama-3.1-8b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
---- stock
correctness rc=1 [correctness] FAILED -- numeric failure(s) and/or a rank-3 case did not dispatch coopmat
linear 8da4w rc=1 kernels:  12 "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8"; 12 "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8";
1b 8da4w default prefill_tok_s=1624.11
1b 8da4w decode rc=0 "generated_tokens":31 decode_tok_s=75.4258
3b 8da4w default prefill_tok_s=569.363
8b 8da4w default prefill_tok_s=280.702
ALLDONE
```

## Run environment: sarc8/env.txt and stock8/env.txt

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt`, line 1 (line 2 holds a host name and is not excerpted)

```text
Sun Sep 27 10:09:35 PM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt`, lines 3-7

```text
ETVK_DEVICE_INDEX=0
ET_VK_SARC_UNVERIFIED=1
5e9414a2175aa2f4c6489910c0b20529e8c1c7020de73a6713767c242116f7ae  test_llama_microbench
1475addd355bc30e867f3d960554979a410d4c007b03050678a6ad99e91eeac7  llama_main
7316cc3dd220104c07db8272a504759feabec77a8d15c2ec0cd2adb36d005372  libllama_runner.so
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/done.txt`, line 1

```text
Sun Sep 27 10:12:22 PM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/env.txt`, line 1 (line 2 holds a host name and is not excerpted)

```text
Sun Sep 27 10:12:22 PM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/env.txt`, lines 3-6

```text
ETVK_DEVICE_INDEX=0
5e9414a2175aa2f4c6489910c0b20529e8c1c7020de73a6713767c242116f7ae  test_llama_microbench
1475addd355bc30e867f3d960554979a410d4c007b03050678a6ad99e91eeac7  llama_main
7316cc3dd220104c07db8272a504759feabec77a8d15c2ec0cd2adb36d005372  libllama_runner.so
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/done.txt`, line 1

```text
Sun Sep 27 10:13:40 PM UTC 2026
```

## sarc/tools/verify.sh at the cited commit: script whose output file names and summary-line formats match the result set (command line not recorded)

Locator: `sarc/tools/verify.sh`, lines 2-6

```text
# On-device verification of a SARC build, run ON THE GPU HOST. Produces the
# evidence a promotion PR needs: dispatched kernel names + kernel times
# (microbench), correctness, sampled production-diff, end-to-end prefill tok/s
# (tiled vs default), next-token equality vs tiled on a real-text and an
# unaligned prompt, and decode.
```

Locator: `sarc/tools/verify.sh`, lines 50-53

```text
export ETVK_DEVICE_INDEX=$DEV LD_LIBRARY_PATH=$DIR
{
  date -u; hostname; env | grep -E '^(ET_VK|ETVK)' | sort
  sha256sum test_llama_microbench llama_main libllama_runner.so 2>/dev/null
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

## Microbench, sarc8 run: banner, protocol and device

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log`, line 1

```text
[sarc_dev] overrides active: unverified=1 variant=
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log`, lines 4-5

```text
Llama microbench (3.1 8B / 3.2 3B / 3.2 1B real e2e shapes; prefill 2048 / decode 1 @ ctx3072; linear group_size=128; 3 warmup + 5 timed runs per case)
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

## Microbench, sarc8 run: first two cases as logged

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log`, lines 9-14

```text
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  334.302 μs                                 
sarc_linear_dq8ca_zpg_t128x64k32g42s32_textu..     (16384,16,1)    (256,1,1)                                                                                                                6796.338 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Texture3D        [1x2048x4096]        7130.640 μs       9637.211 GFLOP/s  SKIPPED
----------------------------------------------------------------------
Completed 1 test cases
RESULT,linear,llama-3.1-8b,8da4w,prefill,tiled,4096,4096,7130.640,4.073,9637.211,not_applicable,SKIPPED,texture3d,2048,6796.338,sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log`, lines 17-19

```text
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  333.149 μs                                 
sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffe..     (16384,16,1)    (256,1,1)                                                                                                                6754.870 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Buffer        [1x2048x4096]        7088.018 μs       9695.161 GFLOP/s  SKIPPED
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log`, line 22

```text
RESULT,linear,llama-3.1-8b,8da4w,prefill,tiled,4096,4096,7088.018,3.264,9695.161,fallback_tiled,SKIPPED,buffer,2048,6754.870,sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
```

## Microbench, sarc8 run: JSON header

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json`, lines 2-9

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

## Microbench, sarc8 run: JSON cases (24 prefill linear cases)

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.json`, lines 11-34

```text
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 4096, "N": 4096, "kv_heads": 0, "op_mean_us": 7130.64, "op_stdev_us": 4.07285, "kernel_mean_us": 6796.34, "kernel_median_us": 6798.32, "kernel_cov": 0.00107392, "gflops": 9637.21, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 4096, "N": 4096, "kv_heads": 0, "op_mean_us": 7088.02, "op_stdev_us": 3.26445, "kernel_mean_us": 6754.87, "kernel_median_us": 6751.96, "kernel_cov": 0.00219342, "gflops": 9695.16, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 4096, "N": 1024, "kv_heads": 0, "op_mean_us": 2064.03, "op_stdev_us": 3.51132, "kernel_mean_us": 1730.85, "kernel_median_us": 1731.12, "kernel_cov": 0.00218718, "gflops": 8323.46, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 4096, "N": 1024, "kv_heads": 0, "op_mean_us": 2051.2, "op_stdev_us": 2.17357, "kernel_mean_us": 1717.77, "kernel_median_us": 1717.68, "kernel_cov": 0.00175565, "gflops": 8375.53, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 4096, "N": 14336, "kv_heads": 0, "op_mean_us": 24050.6, "op_stdev_us": 30.0622, "kernel_mean_us": 23716.9, "kernel_median_us": 23703.8, "kernel_cov": 0.00159882, "gflops": 10000.5, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 4096, "N": 14336, "kv_heads": 0, "op_mean_us": 23923.3, "op_stdev_us": 53.822, "kernel_mean_us": 23587.1, "kernel_median_us": 23608.8, "kernel_cov": 0.00219436, "gflops": 10053.7, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 14336, "N": 4096, "kv_heads": 0, "op_mean_us": 25043.1, "op_stdev_us": 19.1902, "kernel_mean_us": 23839.1, "kernel_median_us": 23836.2, "kernel_cov": 0.00131433, "gflops": 9604.19, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 14336, "N": 4096, "kv_heads": 0, "op_mean_us": 25034.9, "op_stdev_us": 73.5298, "kernel_mean_us": 23839.9, "kernel_median_us": 23831.6, "kernel_cov": 0.00287112, "gflops": 9607.33, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 3072, "N": 3072, "kv_heads": 0, "op_mean_us": 4093.95, "op_stdev_us": 4.93535, "kernel_mean_us": 3840.33, "kernel_median_us": 3840.68, "kernel_cov": 0.00158071, "gflops": 9441.91, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 3072, "N": 3072, "kv_heads": 0, "op_mean_us": 4056.25, "op_stdev_us": 6.72411, "kernel_mean_us": 3803.54, "kernel_median_us": 3803.32, "kernel_cov": 0.00188655, "gflops": 9529.67, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 3072, "N": 1024, "kv_heads": 0, "op_mean_us": 1557.53, "op_stdev_us": 1.97117, "kernel_mean_us": 1304.55, "kernel_median_us": 1304.34, "kernel_cov": 0.00230195, "gflops": 8272.63, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 3072, "N": 1024, "kv_heads": 0, "op_mean_us": 1544.78, "op_stdev_us": 1.17982, "kernel_mean_us": 1292.14, "kernel_median_us": 1291.96, "kernel_cov": 0.00198684, "gflops": 8340.94, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 3072, "N": 8192, "kv_heads": 0, "op_mean_us": 10491.6, "op_stdev_us": 20.5521, "kernel_mean_us": 10238.7, "kernel_median_us": 10246.4, "kernel_cov": 0.00239735, "gflops": 9824.9, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 3072, "N": 8192, "kv_heads": 0, "op_mean_us": 10415.6, "op_stdev_us": 32.1678, "kernel_mean_us": 10162.3, "kernel_median_us": 10167.4, "kernel_cov": 0.00301453, "gflops": 9896.64, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 8192, "N": 3072, "kv_heads": 0, "op_mean_us": 10871.4, "op_stdev_us": 17.5201, "kernel_mean_us": 10196.7, "kernel_median_us": 10195.5, "kernel_cov": 0.00245609, "gflops": 9481.66, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 8192, "N": 3072, "kv_heads": 0, "op_mean_us": 10858.1, "op_stdev_us": 30.926, "kernel_mean_us": 10182.9, "kernel_median_us": 10175.7, "kernel_cov": 0.00316362, "gflops": 9493.28, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 2048, "N": 2048, "kv_heads": 0, "op_mean_us": 1918.78, "op_stdev_us": 10.7169, "kernel_mean_us": 1751.49, "kernel_median_us": 1748.84, "kernel_cov": 0.011856, "gflops": 8953.56, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 2048, "N": 2048, "kv_heads": 0, "op_mean_us": 1891.24, "op_stdev_us": 2.88365, "kernel_mean_us": 1724.82, "kernel_median_us": 1725.1, "kernel_cov": 0.00329953, "gflops": 9083.91, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 2048, "N": 512, "kv_heads": 0, "op_mean_us": 623.833, "op_stdev_us": 0.847147, "kernel_mean_us": 455.248, "kernel_median_us": 455.4, "kernel_cov": 0.00317123, "gflops": 6884.8, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 2048, "N": 512, "kv_heads": 0, "op_mean_us": 618.324, "op_stdev_us": 0.432846, "kernel_mean_us": 450.006, "kernel_median_us": 450.04, "kernel_cov": 0.00273261, "gflops": 6946.14, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 2048, "N": 8192, "kv_heads": 0, "op_mean_us": 7064.27, "op_stdev_us": 29.9782, "kernel_mean_us": 6896.83, "kernel_median_us": 6886.1, "kernel_cov": 0.00492874, "gflops": 9727.76, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 2048, "N": 8192, "kv_heads": 0, "op_mean_us": 6995.22, "op_stdev_us": 31.9824, "kernel_mean_us": 6828.96, "kernel_median_us": 6828.16, "kernel_cov": 0.00525154, "gflops": 9823.78, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half", "M": 2048, "K": 8192, "N": 2048, "kv_heads": 0, "op_mean_us": 7549.48, "op_stdev_us": 10.7428, "kernel_mean_us": 6876, "kernel_median_us": 6871.94, "kernel_cov": 0.00254699, "gflops": 9102.54, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half", "M": 2048, "K": 8192, "N": 2048, "kv_heads": 0, "op_mean_us": 7534.13, "op_stdev_us": 12.4713, "kernel_mean_us": 6859.97, "kernel_median_us": 6860.36, "kernel_cov": 0.00210639, "gflops": 9121.09, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true}
```

## Microbench, sarc8 run: RAW RESULTS table

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log`, lines 200-225

```text
==================== RAW RESULTS ====================
suite     model         scheme regime   op     storage    variant  (M,K,N)                   mean_us     stdev   kern_us   GFLOP/s  dispatch
linear    llama-3.1-8b  8da4w  prefill  wq_wo  texture3d  tiled    (2048,4096,4096)           7130.6       4.1    6796.3    9637.2  not_applicable
linear    llama-3.1-8b  8da4w  prefill  wq_wo  buffer     tiled    (2048,4096,4096)           7088.0       3.3    6754.9    9695.2  fallback_tiled
linear    llama-3.1-8b  8da4w  prefill  wk_wv  texture3d  tiled    (2048,4096,1024)           2064.0       3.5    1730.9    8323.5  not_applicable
linear    llama-3.1-8b  8da4w  prefill  wk_wv  buffer     tiled    (2048,4096,1024)           2051.2       2.2    1717.8    8375.5  fallback_tiled
linear    llama-3.1-8b  8da4w  prefill  w1_w3  texture3d  tiled    (2048,4096,14336)         24050.6      30.1   23716.9   10000.5  not_applicable
linear    llama-3.1-8b  8da4w  prefill  w1_w3  buffer     tiled    (2048,4096,14336)         23923.3      53.8   23587.1   10053.7  fallback_tiled
linear    llama-3.1-8b  8da4w  prefill  w2     texture3d  tiled    (2048,14336,4096)         25043.1      19.2   23839.1    9604.2  not_applicable
linear    llama-3.1-8b  8da4w  prefill  w2     buffer     tiled    (2048,14336,4096)         25034.9      73.5   23839.9    9607.3  fallback_tiled
linear    llama-3.2-3b  8da4w  prefill  wq_wo  texture3d  tiled    (2048,3072,3072)           4093.9       4.9    3840.3    9441.9  not_applicable
linear    llama-3.2-3b  8da4w  prefill  wq_wo  buffer     tiled    (2048,3072,3072)           4056.2       6.7    3803.5    9529.7  fallback_tiled
linear    llama-3.2-3b  8da4w  prefill  wk_wv  texture3d  tiled    (2048,3072,1024)           1557.5       2.0    1304.5    8272.6  not_applicable
linear    llama-3.2-3b  8da4w  prefill  wk_wv  buffer     tiled    (2048,3072,1024)           1544.8       1.2    1292.1    8340.9  fallback_tiled
linear    llama-3.2-3b  8da4w  prefill  w1_w3  texture3d  tiled    (2048,3072,8192)          10491.6      20.6   10238.7    9824.9  not_applicable
linear    llama-3.2-3b  8da4w  prefill  w1_w3  buffer     tiled    (2048,3072,8192)          10415.6      32.2   10162.3    9896.6  fallback_tiled
linear    llama-3.2-3b  8da4w  prefill  w2     texture3d  tiled    (2048,8192,3072)          10871.4      17.5   10196.7    9481.7  not_applicable
linear    llama-3.2-3b  8da4w  prefill  w2     buffer     tiled    (2048,8192,3072)          10858.1      30.9   10182.9    9493.3  fallback_tiled
linear    llama-3.2-1b  8da4w  prefill  wq_wo  texture3d  tiled    (2048,2048,2048)           1918.8      10.7    1751.5    8953.6  not_applicable
linear    llama-3.2-1b  8da4w  prefill  wq_wo  buffer     tiled    (2048,2048,2048)           1891.2       2.9    1724.8    9083.9  fallback_tiled
linear    llama-3.2-1b  8da4w  prefill  wk_wv  texture3d  tiled    (2048,2048,512)             623.8       0.8     455.2    6884.8  not_applicable
linear    llama-3.2-1b  8da4w  prefill  wk_wv  buffer     tiled    (2048,2048,512)             618.3       0.4     450.0    6946.1  fallback_tiled
linear    llama-3.2-1b  8da4w  prefill  w1_w3  texture3d  tiled    (2048,2048,8192)           7064.3      30.0    6896.8    9727.8  not_applicable
linear    llama-3.2-1b  8da4w  prefill  w1_w3  buffer     tiled    (2048,2048,8192)           6995.2      32.0    6829.0    9823.8  fallback_tiled
linear    llama-3.2-1b  8da4w  prefill  w2     texture3d  tiled    (2048,8192,2048)           7549.5      10.7    6876.0    9102.5  not_applicable
linear    llama-3.2-1b  8da4w  prefill  w2     buffer     tiled    (2048,8192,2048)           7534.1      12.5    6860.0    9121.1  fallback_tiled
```

## Microbench, sarc8 run: harness summary table and notes

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log`, lines 227-243

```text
========== LINEAR: coopmat (WMMA) vs tiled, prefill M=2048 ==========
scheme model         op     (K,N)             tiled_tex     coopmat     op_x   kern_x  (us; op_x = whole op incl. 8da4w act-quant, kern_x = linear shader only)
8da4w  llama-3.1-8b  wq_wo  (4096,4096)          7130.6      7088.0        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.1-8b  wk_wv  (4096,1024)          2064.0      2051.2        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.1-8b  w1_w3  (4096,14336)        24050.6     23923.3        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.1-8b  w2     (14336,4096)        25043.1     25034.9        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.2-3b  wq_wo  (3072,3072)          4093.9      4056.2        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.2-3b  wk_wv  (3072,1024)          1557.5      1544.8        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.2-3b  w1_w3  (3072,8192)         10491.6     10415.6        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.2-3b  w2     (8192,3072)         10871.4     10858.1        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.2-1b  wq_wo  (2048,2048)          1918.8      1891.2        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.2-1b  wk_wv  (2048,512)            623.8       618.3        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.2-1b  w1_w3  (2048,8192)          7064.3      6995.2        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
8da4w  llama-3.2-1b  w2     (8192,2048)          7549.5      7534.1        -        -  ! sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half
(! = buffer case did NOT dispatch a coopmat shader; shown for reference, excluded from speedups/geomeans)

One or more cases crashed or did not dispatch the expected kernel (see dispatch column) -- do not trust their speedup numbers.
```

## Microbench, stock8 run: protocol and device

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.log`, lines 3-4

```text
Llama microbench (3.1 8B / 3.2 3B / 3.2 1B real e2e shapes; prefill 2048 / decode 1 @ ctx3072; linear group_size=128; 3 warmup + 5 timed runs per case)
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

## Microbench, stock8 run: first case as logged

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.log`, lines 8-13

```text
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  327.190 μs                                 
linear_dq8ca_q4gsw_tiled_texture3d_texture2d..     (512,512,1)     (8,8,1)                                                                                                                  9624.839 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Texture3D        [1x2048x4096]        9952.029 μs       6905.072 GFLOP/s  SKIPPED
----------------------------------------------------------------------
Completed 1 test cases
RESULT,linear,llama-3.1-8b,8da4w,prefill,tiled,4096,4096,9952.029,36.649,6905.072,not_applicable,SKIPPED,texture3d,2048,9624.839,linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8
```

## Microbench, stock8 run: JSON header

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json`, lines 2-9

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

## Microbench, stock8 run: JSON cases (24 prefill linear cases)

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.json`, lines 11-34

```text
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 4096, "N": 4096, "kv_heads": 0, "op_mean_us": 9952.03, "op_stdev_us": 36.6485, "kernel_mean_us": 9624.84, "kernel_median_us": 9631.9, "kernel_cov": 0.00527814, "gflops": 6905.07, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 4096, "N": 4096, "kv_heads": 0, "op_mean_us": 9630.18, "op_stdev_us": 54.3844, "kernel_mean_us": 9302.94, "kernel_median_us": 9291.28, "kernel_cov": 0.0105797, "gflops": 7135.85, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 4096, "N": 1024, "kv_heads": 0, "op_mean_us": 2616.84, "op_stdev_us": 5.18479, "kernel_mean_us": 2287.08, "kernel_median_us": 2288.84, "kernel_cov": 0.00633826, "gflops": 6565.11, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 4096, "N": 1024, "kv_heads": 0, "op_mean_us": 2560.82, "op_stdev_us": 6.06298, "kernel_mean_us": 2231.28, "kernel_median_us": 2236.04, "kernel_cov": 0.0102197, "gflops": 6708.74, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 4096, "N": 14336, "kv_heads": 0, "op_mean_us": 33522.4, "op_stdev_us": 123.04, "kernel_mean_us": 33192.5, "kernel_median_us": 33248.7, "kernel_cov": 0.00990917, "gflops": 7174.85, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 4096, "N": 14336, "kv_heads": 0, "op_mean_us": 32078.7, "op_stdev_us": 308.162, "kernel_mean_us": 31748.9, "kernel_median_us": 31736.3, "kernel_cov": 0.0115311, "gflops": 7497.75, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 14336, "N": 4096, "kv_heads": 0, "op_mean_us": 34215, "op_stdev_us": 38.7117, "kernel_mean_us": 33016.3, "kernel_median_us": 33019.1, "kernel_cov": 0.00170589, "gflops": 7029.61, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.1-8b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 14336, "N": 4096, "kv_heads": 0, "op_mean_us": 33409.7, "op_stdev_us": 123.456, "kernel_mean_us": 32217.8, "kernel_median_us": 32163.7, "kernel_cov": 0.00357625, "gflops": 7199.05, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 3072, "N": 3072, "kv_heads": 0, "op_mean_us": 5621.91, "op_stdev_us": 19.7275, "kernel_mean_us": 5374.88, "kernel_median_us": 5375.38, "kernel_cov": 0.00902197, "gflops": 6875.72, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 3072, "N": 3072, "kv_heads": 0, "op_mean_us": 5466.29, "op_stdev_us": 22.7474, "kernel_mean_us": 5219.72, "kernel_median_us": 5228.02, "kernel_cov": 0.0100498, "gflops": 7071.47, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 3072, "N": 1024, "kv_heads": 0, "op_mean_us": 1822.58, "op_stdev_us": 4.49448, "kernel_mean_us": 1571.06, "kernel_median_us": 1568.94, "kernel_cov": 0.0149494, "gflops": 7069.61, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 3072, "N": 1024, "kv_heads": 0, "op_mean_us": 1803.65, "op_stdev_us": 4.37893, "kernel_mean_us": 1551.97, "kernel_median_us": 1554.52, "kernel_cov": 0.00931017, "gflops": 7143.8, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 3072, "N": 8192, "kv_heads": 0, "op_mean_us": 14335.6, "op_stdev_us": 224.269, "kernel_mean_us": 14086.4, "kernel_median_us": 13988.7, "kernel_cov": 0.017943, "gflops": 7190.46, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 3072, "N": 8192, "kv_heads": 0, "op_mean_us": 13932.6, "op_stdev_us": 61.1528, "kernel_mean_us": 13683.8, "kernel_median_us": 13685.8, "kernel_cov": 0.00819481, "gflops": 7398.42, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 8192, "N": 3072, "kv_heads": 0, "op_mean_us": 15133.6, "op_stdev_us": 40.1237, "kernel_mean_us": 14465, "kernel_median_us": 14441, "kernel_cov": 0.00529831, "gflops": 6811.3, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-3b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 8192, "N": 3072, "kv_heads": 0, "op_mean_us": 14681.1, "op_stdev_us": 41.1871, "kernel_mean_us": 14013.8, "kernel_median_us": 14009.2, "kernel_cov": 0.00351867, "gflops": 7021.23, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 2048, "N": 2048, "kv_heads": 0, "op_mean_us": 2398.82, "op_stdev_us": 3.56823, "kernel_mean_us": 2235.85, "kernel_median_us": 2238.06, "kernel_cov": 0.00656593, "gflops": 7161.81, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "wq_wo", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 2048, "N": 2048, "kv_heads": 0, "op_mean_us": 2342.16, "op_stdev_us": 6.94405, "kernel_mean_us": 2179.66, "kernel_median_us": 2177.68, "kernel_cov": 0.00908503, "gflops": 7335.07, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 2048, "N": 512, "kv_heads": 0, "op_mean_us": 706.513, "op_stdev_us": 2.07214, "kernel_mean_us": 538.464, "kernel_median_us": 538.92, "kernel_cov": 0.00633938, "gflops": 6079.11, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "wk_wv", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 2048, "N": 512, "kv_heads": 0, "op_mean_us": 705.269, "op_stdev_us": 2.48993, "kernel_mean_us": 537.435, "kernel_median_us": 537.96, "kernel_cov": 0.00631742, "gflops": 6089.83, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 2048, "N": 8192, "kv_heads": 0, "op_mean_us": 9684.01, "op_stdev_us": 32.3042, "kernel_mean_us": 9518.63, "kernel_median_us": 9509.38, "kernel_cov": 0.00700957, "gflops": 7096.18, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "w1_w3", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 2048, "N": 8192, "kv_heads": 0, "op_mean_us": 9507.96, "op_stdev_us": 24.2707, "kernel_mean_us": 9343.01, "kernel_median_us": 9322.12, "kernel_cov": 0.00722291, "gflops": 7227.57, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "texture3d", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_texture3d_texture2d_half_zpint8", "M": 2048, "K": 8192, "N": 2048, "kv_heads": 0, "op_mean_us": 10506.8, "op_stdev_us": 61.9255, "kernel_mean_us": 9838.55, "kernel_median_us": 9809.82, "kernel_cov": 0.00946338, "gflops": 6540.47, "dispatch": "not_applicable", "correctness": "SKIPPED", "detail": "", "ok": true},
    {"suite": "linear", "model": "llama-3.2-1b", "scheme": "8da4w", "regime": "prefill", "op": "w2", "storage": "buffer", "variant": "tiled", "kernel": "linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8", "M": 2048, "K": 8192, "N": 2048, "kv_heads": 0, "op_mean_us": 10209.5, "op_stdev_us": 32.7931, "kernel_mean_us": 9540.61, "kernel_median_us": 9523.04, "kernel_cov": 0.00552659, "gflops": 6730.96, "dispatch": "fallback_tiled", "correctness": "SKIPPED", "detail": "", "ok": true}
```

## Microbench, stock8 run: RAW RESULTS table

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.log`, lines 199-224

```text
==================== RAW RESULTS ====================
suite     model         scheme regime   op     storage    variant  (M,K,N)                   mean_us     stdev   kern_us   GFLOP/s  dispatch
linear    llama-3.1-8b  8da4w  prefill  wq_wo  texture3d  tiled    (2048,4096,4096)           9952.0      36.6    9624.8    6905.1  not_applicable
linear    llama-3.1-8b  8da4w  prefill  wq_wo  buffer     tiled    (2048,4096,4096)           9630.2      54.4    9302.9    7135.8  fallback_tiled
linear    llama-3.1-8b  8da4w  prefill  wk_wv  texture3d  tiled    (2048,4096,1024)           2616.8       5.2    2287.1    6565.1  not_applicable
linear    llama-3.1-8b  8da4w  prefill  wk_wv  buffer     tiled    (2048,4096,1024)           2560.8       6.1    2231.3    6708.7  fallback_tiled
linear    llama-3.1-8b  8da4w  prefill  w1_w3  texture3d  tiled    (2048,4096,14336)         33522.4     123.0   33192.5    7174.9  not_applicable
linear    llama-3.1-8b  8da4w  prefill  w1_w3  buffer     tiled    (2048,4096,14336)         32078.7     308.2   31748.9    7497.8  fallback_tiled
linear    llama-3.1-8b  8da4w  prefill  w2     texture3d  tiled    (2048,14336,4096)         34215.0      38.7   33016.3    7029.6  not_applicable
linear    llama-3.1-8b  8da4w  prefill  w2     buffer     tiled    (2048,14336,4096)         33409.7     123.5   32217.8    7199.0  fallback_tiled
linear    llama-3.2-3b  8da4w  prefill  wq_wo  texture3d  tiled    (2048,3072,3072)           5621.9      19.7    5374.9    6875.7  not_applicable
linear    llama-3.2-3b  8da4w  prefill  wq_wo  buffer     tiled    (2048,3072,3072)           5466.3      22.7    5219.7    7071.5  fallback_tiled
linear    llama-3.2-3b  8da4w  prefill  wk_wv  texture3d  tiled    (2048,3072,1024)           1822.6       4.5    1571.1    7069.6  not_applicable
linear    llama-3.2-3b  8da4w  prefill  wk_wv  buffer     tiled    (2048,3072,1024)           1803.6       4.4    1552.0    7143.8  fallback_tiled
linear    llama-3.2-3b  8da4w  prefill  w1_w3  texture3d  tiled    (2048,3072,8192)          14335.6     224.3   14086.4    7190.5  not_applicable
linear    llama-3.2-3b  8da4w  prefill  w1_w3  buffer     tiled    (2048,3072,8192)          13932.6      61.2   13683.8    7398.4  fallback_tiled
linear    llama-3.2-3b  8da4w  prefill  w2     texture3d  tiled    (2048,8192,3072)          15133.6      40.1   14465.0    6811.3  not_applicable
linear    llama-3.2-3b  8da4w  prefill  w2     buffer     tiled    (2048,8192,3072)          14681.1      41.2   14013.8    7021.2  fallback_tiled
linear    llama-3.2-1b  8da4w  prefill  wq_wo  texture3d  tiled    (2048,2048,2048)           2398.8       3.6    2235.8    7161.8  not_applicable
linear    llama-3.2-1b  8da4w  prefill  wq_wo  buffer     tiled    (2048,2048,2048)           2342.2       6.9    2179.7    7335.1  fallback_tiled
linear    llama-3.2-1b  8da4w  prefill  wk_wv  texture3d  tiled    (2048,2048,512)             706.5       2.1     538.5    6079.1  not_applicable
linear    llama-3.2-1b  8da4w  prefill  wk_wv  buffer     tiled    (2048,2048,512)             705.3       2.5     537.4    6089.8  fallback_tiled
linear    llama-3.2-1b  8da4w  prefill  w1_w3  texture3d  tiled    (2048,2048,8192)           9684.0      32.3    9518.6    7096.2  not_applicable
linear    llama-3.2-1b  8da4w  prefill  w1_w3  buffer     tiled    (2048,2048,8192)           9508.0      24.3    9343.0    7227.6  fallback_tiled
linear    llama-3.2-1b  8da4w  prefill  w2     texture3d  tiled    (2048,8192,2048)          10506.8      61.9    9838.5    6540.5  not_applicable
linear    llama-3.2-1b  8da4w  prefill  w2     buffer     tiled    (2048,8192,2048)          10209.5      32.8    9540.6    6731.0  fallback_tiled
```

## Microbench, stock8 run: harness summary table and notes

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/linear-8da4w.log`, lines 226-242

```text
========== LINEAR: coopmat (WMMA) vs tiled, prefill M=2048 ==========
scheme model         op     (K,N)             tiled_tex     coopmat     op_x   kern_x  (us; op_x = whole op incl. 8da4w act-quant, kern_x = linear shader only)
8da4w  llama-3.1-8b  wq_wo  (4096,4096)          9952.0      9630.2        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.1-8b  wk_wv  (4096,1024)          2616.8      2560.8        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.1-8b  w1_w3  (4096,14336)        33522.4     32078.7        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.1-8b  w2     (14336,4096)        34215.0     33409.7        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.2-3b  wq_wo  (3072,3072)          5621.9      5466.3        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.2-3b  wk_wv  (3072,1024)          1822.6      1803.6        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.2-3b  w1_w3  (3072,8192)         14335.6     13932.6        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.2-3b  w2     (8192,3072)         15133.6     14681.1        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.2-1b  wq_wo  (2048,2048)          2398.8      2342.2        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.2-1b  wk_wv  (2048,512)            706.5       705.3        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.2-1b  w1_w3  (2048,8192)          9684.0      9508.0        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
8da4w  llama-3.2-1b  w2     (8192,2048)         10506.8     10209.5        -        -  ! linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8
(! = buffer case did NOT dispatch a coopmat shader; shown for reference, excluded from speedups/geomeans)

One or more cases crashed or did not dispatch the expected kernel (see dispatch column) -- do not trust their speedup numbers.
```

## End-to-end prefill logs, sarc8 run: PyTorchObserver lines

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-1b-8da4w-default.log`, line 3 (banner line present in every sarc8 run log)

```text
[sarc_dev] overrides active: unverified=1 variant=
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-1b-8da4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":1845.05,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547023499,"model_load_end_ms":1790547023917,"inference_start_ms":1790547025070,"inference_end_ms":1790547026180,"model_execution_start_ms":1790547025072,"model_execution_end_ms":1790547026179,"prompt_eval_end_ms":1790547026180,"first_token_ms":1790547026180,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1107,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-1b-8da4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":1630.57,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547017403,"model_load_end_ms":1790547017758,"inference_start_ms":1790547019044,"inference_end_ms":1790547020300,"model_execution_start_ms":1790547019047,"model_execution_end_ms":1790547020300,"prompt_eval_end_ms":1790547020300,"first_token_ms":1790547020300,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1253,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-3b-8da4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":649.128,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547039690,"model_load_end_ms":1790547040638,"inference_start_ms":1790547043831,"inference_end_ms":1790547046986,"model_execution_start_ms":1790547043834,"model_execution_end_ms":1790547046985,"prompt_eval_end_ms":1790547046986,"first_token_ms":1790547046986,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":3151,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-3b-8da4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":565.902,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547031378,"model_load_end_ms":1790547032304,"inference_start_ms":1790547035957,"inference_end_ms":1790547039576,"model_execution_start_ms":1790547035959,"model_execution_end_ms":1790547039576,"prompt_eval_end_ms":1790547039576,"first_token_ms":1790547039576,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":3617,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-8b-8da4w-default.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":336.068,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547065138,"model_load_end_ms":1790547068250,"inference_start_ms":1790547074386,"inference_end_ms":1790547080480,"model_execution_start_ms":1790547074388,"model_execution_end_ms":1790547080480,"prompt_eval_end_ms":1790547080480,"first_token_ms":1790547080480,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":6092,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/prefill-8b-8da4w-tiled.log`, line 6

```text
PyTorchObserver {"prefill_token_per_sec":279.743,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547047102,"model_load_end_ms":1790547050339,"inference_start_ms":1790547057700,"inference_end_ms":1790547065021,"model_execution_start_ms":1790547057703,"model_execution_end_ms":1790547065021,"prompt_eval_end_ms":1790547065021,"first_token_ms":1790547065021,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":7318,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## End-to-end prefill logs, stock8 run: PyTorchObserver lines

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/prefill-1b-8da4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":1624.11,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547185972,"model_load_end_ms":1790547186284,"inference_start_ms":1790547187576,"inference_end_ms":1790547188837,"model_execution_start_ms":1790547187579,"model_execution_end_ms":1790547188837,"prompt_eval_end_ms":1790547188837,"first_token_ms":1790547188837,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1258,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/prefill-3b-8da4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":569.363,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547194234,"model_load_end_ms":1790547195111,"inference_start_ms":1790547198744,"inference_end_ms":1790547202341,"model_execution_start_ms":1790547198747,"model_execution_end_ms":1790547202340,"prompt_eval_end_ms":1790547202341,"first_token_ms":1790547202341,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":3593,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/prefill-8b-8da4w-default.log`, line 5

```text
PyTorchObserver {"prefill_token_per_sec":280.702,"prompt_tokens":2048,"generated_tokens":0,"model_load_start_ms":1790547202458,"model_load_end_ms":1790547205677,"inference_start_ms":1790547213003,"inference_end_ms":1790547220299,"model_execution_start_ms":1790547213006,"model_execution_end_ms":1790547220298,"prompt_eval_end_ms":1790547220299,"first_token_ms":1790547220299,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":7292,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Decode logs (1B, 32 new tokens requested): PyTorchObserver lines

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/decode-1b-8da4w.log`, line 10

```text
PyTorchObserver {"prefill_token_per_sec":1777.78,"decode_token_per_sec":69.3512,"prompt_tokens":2048,"generated_tokens":31,"model_load_start_ms":1790547029308,"model_load_end_ms":1790547029678,"inference_start_ms":1790547029678,"inference_end_ms":1790547031277,"model_execution_start_ms":1790547031263,"model_execution_end_ms":1790547031276,"prompt_eval_end_ms":1790547030830,"first_token_ms":1790547030830,"aggregate_sampling_time_ms":21,"aggregate_model_execution_time_ms":1568,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/decode-1b-8da4w.log`, line 9

```text
PyTorchObserver {"prefill_token_per_sec":1585.14,"decode_token_per_sec":75.4258,"prompt_tokens":2048,"generated_tokens":31,"model_load_start_ms":1790547192056,"model_load_end_ms":1790547192430,"inference_start_ms":1790547192430,"inference_end_ms":1790547194133,"model_execution_start_ms":1790547194120,"model_execution_end_ms":1790547194132,"prompt_eval_end_ms":1790547193722,"first_token_ms":1790547193722,"aggregate_sampling_time_ms":6,"aggregate_model_execution_time_ms":1692,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Check-prompt logs (1B, prompt_check.txt): PyTorchObserver lines

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/check-1b-8da4w-default.log`, line 140

```text
PyTorchObserver {"prefill_token_per_sec":1631.1,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790547026276,"model_load_end_ms":1790547026635,"inference_start_ms":1790547026635,"inference_end_ms":1790547027844,"model_execution_start_ms":1790547026640,"model_execution_end_ms":1790547027844,"prompt_eval_end_ms":1790547027844,"first_token_ms":1790547027844,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1204,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/check-1b-8da4w-tiled.log`, line 140

```text
PyTorchObserver {"prefill_token_per_sec":1700,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790547020395,"model_load_end_ms":1790547020755,"inference_start_ms":1790547020755,"inference_end_ms":1790547021915,"model_execution_start_ms":1790547020761,"model_execution_end_ms":1790547021915,"prompt_eval_end_ms":1790547021915,"first_token_ms":1790547021915,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1154,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/check-1b-8da4w-default.log`, line 139

```text
PyTorchObserver {"prefill_token_per_sec":1704.41,"prompt_tokens":1972,"generated_tokens":0,"model_load_start_ms":1790547188931,"model_load_end_ms":1790547189302,"inference_start_ms":1790547189302,"inference_end_ms":1790547190459,"model_execution_start_ms":1790547189306,"model_execution_end_ms":1790547190458,"prompt_eval_end_ms":1790547190459,"first_token_ms":1790547190459,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1152,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Unaligned-prompt logs (1B): generated-text line and PyTorchObserver line

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/unaligned-1b-8da4w-default.log`, lines 6-7 (line 6 is the last text line before the observer line; the echoed prompt on line 5 is not excerpted)

```text
 
PyTorchObserver {"prefill_token_per_sec":1988.9,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790547027940,"model_load_end_ms":1790547028309,"inference_start_ms":1790547028309,"inference_end_ms":1790547029210,"model_execution_start_ms":1790547028313,"model_execution_end_ms":1790547029210,"prompt_eval_end_ms":1790547029210,"first_token_ms":1790547029210,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":897,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/unaligned-1b-8da4w-tiled.log`, lines 6-7 (line 6 is the last text line before the observer line; the echoed prompt on line 5 is not excerpted)

```text
2
PyTorchObserver {"prefill_token_per_sec":1744.89,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790547022008,"model_load_end_ms":1790547022376,"inference_start_ms":1790547022376,"inference_end_ms":1790547023403,"model_execution_start_ms":1790547022379,"model_execution_end_ms":1790547023403,"prompt_eval_end_ms":1790547023403,"first_token_ms":1790547023403,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1024,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/unaligned-1b-8da4w-default.log`, lines 5-6 (line 5 is the last text line before the observer line; the echoed prompt on line 4 is not excerpted)

```text
2
PyTorchObserver {"prefill_token_per_sec":1741.5,"decode_token_per_sec":0,"prompt_tokens":1792,"generated_tokens":0,"model_load_start_ms":1790547190554,"model_load_end_ms":1790547190932,"inference_start_ms":1790547190932,"inference_end_ms":1790547191962,"model_execution_start_ms":1790547190937,"model_execution_end_ms":1790547191961,"prompt_eval_end_ms":1790547191961,"first_token_ms":1790547191961,"aggregate_sampling_time_ms":0,"aggregate_model_execution_time_ms":1024,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
```

## Correctness log, sarc8 run: dq8ca rank-3 cases and summary

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/correctness.log`, lines 271-273

```text
quantize_and_pack_4h4w_with_group_sums_o4w16..     (2,32,1)        (4,1,16)                                                                                                                    2.701 μs                                 
sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffe..     (512,1,1)       (256,1,1)                                                                                                                   7.718 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               linear_dq8ca_q4gsw_M128_K128_N128_rank3batch1_Buffer                                      [1x128x128]          10.419 μs        402.574 GFLOP/s   PASSED
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/correctness.log`, lines 278-280

```text
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,32,1)       (2,1,32)                                                                                                                   13.945 μs                                 
sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffe..     (512,1,1)       (256,1,1)                                                                                                                  90.486 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               linear_dq8ca_q4gsw_M128_K4096_N128_rank3batch1_Buffer                                    [1x128x4096]         104.432 μs       1285.220 GFLOP/s   PASSED
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/correctness.log`, lines 283-287

```text
[rank3 batch=1] linear_q4gsw_M128_K128_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_dq8ca_q4gsw_M128_K128_N128_rank3batch1_Buffer -> sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half (NOT coopmat -- fallback), correctness=PASSED
[rank3 batch=1] linear_dq8ca_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half (NOT coopmat -- fallback), correctness=PASSED
[correctness] FAILED -- numeric failure(s) and/or a rank-3 case did not dispatch coopmat
```

## Correctness log, stock8 run: dq8ca rank-3 cases and summary

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/correctness.log`, lines 270-272

```text
quantize_and_pack_4h4w_with_group_sums_o4w16..     (2,32,1)        (4,1,16)                                                                                                                    3.035 μs                                 
linear_dq8ca_q4gsw_tiled_buffer_texture2d_ha..     (16,32,1)       (8,8,1)                                                                                                                    11.018 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               linear_dq8ca_q4gsw_M128_K128_N128_rank3batch1_Buffer                                      [1x128x128]          14.053 μs        298.469 GFLOP/s   PASSED
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/correctness.log`, lines 277-279

```text
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,32,1)       (2,1,32)                                                                                                                   13.842 μs                                 
linear_dq8ca_q4gsw_tiled_buffer_texture2d_ha..     (16,32,1)       (8,8,1)                                                                                                                   127.363 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               linear_dq8ca_q4gsw_M128_K4096_N128_rank3batch1_Buffer                                    [1x128x4096]         141.205 μs        950.519 GFLOP/s   PASSED
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/correctness.log`, lines 282-286

```text
[rank3 batch=1] linear_q4gsw_M128_K128_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[rank3 batch=1] linear_dq8ca_q4gsw_M128_K128_N128_rank3batch1_Buffer -> linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8 (NOT coopmat -- fallback), correctness=PASSED
[rank3 batch=1] linear_dq8ca_q4gsw_M128_K4096_N128_rank3batch1_Buffer -> linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8 (NOT coopmat -- fallback), correctness=PASSED
[correctness] FAILED -- numeric failure(s) and/or a rank-3 case did not dispatch coopmat
```

## Production-diff, first run (sarc8, kernel names before the rename): llama-3.2-1b buffer

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/pdiff-llama-3.2-1b-8da4w-buffer.log`, line 17

```text
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K2048_N2048_rank3batch1_Buffer -> sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half (NOT coopmat -- fallback, cannot validate the shader under test), correctness=PASSED
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/pdiff-llama-3.2-1b-8da4w-buffer.log`, line 51

```text
[production-diff] FAILED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/pdiff-llama-3.2-1b-8da4w-buffer.log`, line 11

```text
[sampled reference] max abs diff 0.0156136 (tol 0.5), max rel diff 0.000481556 (tol 0.05, |ref| > abs tol)
```

## Production-diff re-run (pdiff2): llama-3.2-1b buffer

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log`, line 1

```text
[sarc_dev] overrides active: unverified=1 variant=
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log`, lines 4-5

```text
Llama microbench (3.1 8B / 3.2 3B / 3.2 1B real e2e shapes; prefill 2048 / decode 1 @ ctx3072; linear group_size=128; 3 warmup + 5 timed runs per case)
DEVICE,amd radeon 780m graphics (radv phoenix),timestamp_period_ns=10,subgroup_size=64,coopmat=yes,max_shared_mem_bytes=65536
```

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log`, lines 7-51

```text
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K2048_N2048_rank3batch1_Buffer (M=2048, K=2048, N=2048, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8161 of 4194304 elements
[sampled reference] max abs diff 0.0156136 (tol 0.5), max rel diff 0.000481556 (tol 0.05, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (16,512,1)      (2,1,32)                                                                                                                  166.815 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (8192,16,1)     (256,1,1)                                                                                                                1781.263 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-1b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K2048_N2048_rank3batch1_Buffer        [1x2048x2048]        1948.078 μs       8818.881 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K2048_N2048_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K2048_N512_rank3batch1_Buffer (M=2048, K=2048, N=512, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 7772 of 1048576 elements
[sampled reference] max abs diff 0.016 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (16,512,1)      (2,1,32)                                                                                                                  168.306 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (2048,16,1)     (256,1,1)                                                                                                                 453.758 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-1b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K2048_N512_rank3batch1_Buffer        [1x2048x2048]         622.064 μs       6904.380 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-1b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K2048_N512_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K2048_N8192_rank3batch1_Buffer (M=2048, K=2048, N=8192, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8242 of 16777216 elements
[sampled reference] max abs diff 0.016 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (16,512,1)      (2,1,32)                                                                                                                  166.779 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (32768,16,1)    (256,1,1)                                                                                                                7088.909 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-1b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K2048_N8192_rank3batch1_Buffer        [1x2048x2048]        7255.688 μs       9471.117 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-1b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K2048_N8192_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N2048_rank3batch1_Buffer (M=2048, K=8192, N=2048, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8133 of 4194304 elements
[sampled reference] max abs diff 0.062 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (64,512,1)      (2,1,32)                                                                                                                  674.294 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (8192,16,1)     (256,1,1)                                                                                                                7064.388 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-1b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N2048_rank3batch1_Buffer         [1x2048x8192]        7738.681 μs       8879.998 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-1b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N2048_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
```

## Production-diff re-run (pdiff2): llama-3.2-1b texture3d

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-texture3d.log`, lines 7-51

```text
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K2048_N2048_rank3batch1_Texture3D (M=2048, K=2048, N=2048, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8161 of 4194304 elements
[sampled reference] max abs diff 0.0156136 (tol 0.5), max rel diff 0.000481556 (tol 0.05, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (16,512,1)      (2,1,32)                                                                                                                  167.056 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (8192,16,1)     (256,1,1)                                                                                                                1784.243 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-1b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K2048_N2048_rank3batch1_Texture3D        [1x2048x2048]        1951.298 μs       8804.326 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-1b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K2048_N2048_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K2048_N512_rank3batch1_Texture3D (M=2048, K=2048, N=512, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 7772 of 1048576 elements
[sampled reference] max abs diff 0.016 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (16,512,1)      (2,1,32)                                                                                                                  168.294 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (2048,16,1)     (256,1,1)                                                                                                                 457.023 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-1b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K2048_N512_rank3batch1_Texture3D        [1x2048x2048]         625.318 μs       6868.458 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-1b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K2048_N512_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K2048_N8192_rank3batch1_Texture3D (M=2048, K=2048, N=8192, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8242 of 16777216 elements
[sampled reference] max abs diff 0.016 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (16,512,1)      (2,1,32)                                                                                                                  167.821 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (32768,16,1)    (256,1,1)                                                                                                                7087.514 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-1b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K2048_N8192_rank3batch1_Texture3D        [1x2048x2048]        7255.333 μs       9471.580 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-1b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K2048_N8192_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-1b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N2048_rank3batch1_Texture3D (M=2048, K=8192, N=2048, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8133 of 4194304 elements
[sampled reference] max abs diff 0.062 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (64,512,1)      (2,1,32)                                                                                                                  672.640 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (8192,16,1)     (256,1,1)                                                                                                                6978.324 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-1b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N2048_rank3batch1_Texture3D        [1x2048x8192]        7650.963 μs       8981.807 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-1b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N2048_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
```

## Production-diff re-run (pdiff2): llama-3.2-3b buffer

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-3b-8da4w-buffer.log`, lines 7-51

```text
[production-diff] llama-3.2-3b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K3072_N3072_rank3batch1_Buffer (M=2048, K=3072, N=3072, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8185 of 6291456 elements
[sampled reference] max abs diff 0.0309753 (tol 0.5), max rel diff 0.000487805 (tol 0.05, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (24,512,1)      (2,1,32)                                                                                                                  253.279 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (12288,16,1)    (256,1,1)                                                                                                                3873.016 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-3b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K3072_N3072_rank3batch1_Buffer        [1x2048x3072]        4126.295 μs       9367.896 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-3b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K3072_N3072_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K3072_N1024_rank3batch1_Buffer (M=2048, K=3072, N=1024, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8026 of 2097152 elements
[sampled reference] max abs diff 0.031 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (24,512,1)      (2,1,32)                                                                                                                  252.592 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (4096,16,1)     (256,1,1)                                                                                                                1308.534 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-3b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K3072_N1024_rank3batch1_Buffer        [1x2048x3072]        1561.125 μs       8253.599 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-3b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K3072_N1024_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K3072_N8192_rank3batch1_Buffer (M=2048, K=3072, N=8192, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8248 of 16777216 elements
[sampled reference] max abs diff 0.031 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (24,512,1)      (2,1,32)                                                                                                                  253.762 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (32768,16,1)    (256,1,1)                                                                                                               10429.344 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-3b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K3072_N8192_rank3batch1_Buffer        [1x2048x3072]       10683.106 μs       9648.806 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-3b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K3072_N8192_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N3072_rank3batch1_Buffer (M=2048, K=8192, N=3072, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8187 of 6291456 elements
[sampled reference] max abs diff 0.062 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (64,512,1)      (2,1,32)                                                                                                                  676.402 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (12288,16,1)    (256,1,1)                                                                                                               10399.619 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-3b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N3072_rank3batch1_Buffer         [1x2048x8192]       11076.022 μs       9306.519 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-3b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N3072_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.2-3b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
```

## Production-diff re-run (pdiff2): llama-3.2-3b texture3d

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-3b-8da4w-texture3d.log`, lines 7-51

```text
[production-diff] llama-3.2-3b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K3072_N3072_rank3batch1_Texture3D (M=2048, K=3072, N=3072, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8185 of 6291456 elements
[sampled reference] max abs diff 0.0309753 (tol 0.5), max rel diff 0.000487805 (tol 0.05, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (24,512,1)      (2,1,32)                                                                                                                  254.931 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (12288,16,1)    (256,1,1)                                                                                                                3896.274 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-3b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K3072_N3072_rank3batch1_Texture3D        [1x2048x3072]        4151.206 μs       9311.681 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-3b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K3072_N3072_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K3072_N1024_rank3batch1_Texture3D (M=2048, K=3072, N=1024, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8026 of 2097152 elements
[sampled reference] max abs diff 0.031 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (24,512,1)      (2,1,32)                                                                                                                  252.921 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (4096,16,1)     (256,1,1)                                                                                                                1317.231 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-3b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K3072_N1024_rank3batch1_Texture3D        [1x2048x3072]        1570.152 μs       8206.151 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-3b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K3072_N1024_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K3072_N8192_rank3batch1_Texture3D (M=2048, K=3072, N=8192, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8248 of 16777216 elements
[sampled reference] max abs diff 0.031 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (24,512,1)      (2,1,32)                                                                                                                  253.616 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (32768,16,1)    (256,1,1)                                                                                                               10449.562 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-3b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K3072_N8192_rank3batch1_Texture3D        [1x2048x3072]       10703.178 μs       9630.711 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-3b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K3072_N8192_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.2-3b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N3072_rank3batch1_Texture3D (M=2048, K=8192, N=3072, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8187 of 6291456 elements
[sampled reference] max abs diff 0.062 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (64,512,1)      (2,1,32)                                                                                                                  675.770 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (12288,16,1)    (256,1,1)                                                                                                               10391.415 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.2-3b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N3072_rank3batch1_Texture3D        [1x2048x8192]       11067.185 μs       9313.951 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.2-3b_prefill_w2_linear_dq8ca_q4gsw_M2048_K8192_N3072_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.2-3b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
```

## Production-diff re-run (pdiff2): llama-3.1-8b buffer

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-buffer.log`, lines 7-51

```text
[production-diff] llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Buffer (M=2048, K=4096, N=4096, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8200 of 8388608 elements
[sampled reference] max abs diff 0.031105 (tol 0.5), max rel diff 0.000484944 (tol 0.05, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  334.557 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (16384,16,1)    (256,1,1)                                                                                                                6891.742 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Buffer        [1x2048x4096]        7226.299 μs       9509.636 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K4096_N1024_rank3batch1_Buffer (M=2048, K=4096, N=1024, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8008 of 2097152 elements
[sampled reference] max abs diff 0.031 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  333.917 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (4096,16,1)     (256,1,1)                                                                                                                1729.547 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K4096_N1024_rank3batch1_Buffer        [1x2048x4096]        2063.463 μs       8325.744 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.1-8b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K4096_N1024_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K4096_N14336_rank3batch1_Buffer (M=2048, K=4096, N=14336, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8254 of 29360128 elements
[sampled reference] max abs diff 0.031 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  334.108 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (57344,16,1)    (256,1,1)                                                                                                               24104.229 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K4096_N14336_rank3batch1_Buffer        [1x2048x4096]       24438.334 μs       9841.840 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.1-8b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K4096_N14336_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_w2_linear_dq8ca_q4gsw_M2048_K14336_N4096_rank3batch1_Buffer (M=2048, K=14336, N=4096, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8209 of 8388608 elements
[sampled reference] max abs diff 0.124 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (112,512,1)     (2,1,32)                                                                                                                 1193.172 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (16384,16,1)    (256,1,1)                                                                                                               24298.893 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_w2_linear_dq8ca_q4gsw_M2048_K14336_N4096_rank3batch1_Buffer       [1x2048x14336]       25492.064 μs       9435.021 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.1-8b_prefill_w2_linear_dq8ca_q4gsw_M2048_K14336_N4096_rank3batch1_Buffer -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.1-8b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)
```

## Production-diff re-run (pdiff2): llama-3.1-8b texture3d

Locator: `openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-texture3d.log`, lines 7-51

```text
[production-diff] llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Texture3D (M=2048, K=4096, N=4096, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8200 of 8388608 elements
[sampled reference] max abs diff 0.031105 (tol 0.5), max rel diff 0.000484944 (tol 0.05, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  334.707 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (16384,16,1)    (256,1,1)                                                                                                                6940.576 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Texture3D        [1x2048x4096]        7275.283 μs       9445.608 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.1-8b_prefill_wq_wo_linear_dq8ca_q4gsw_M2048_K4096_N4096_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K4096_N1024_rank3batch1_Texture3D (M=2048, K=4096, N=1024, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8008 of 2097152 elements
[sampled reference] max abs diff 0.031 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  333.919 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (4096,16,1)     (256,1,1)                                                                                                                1738.428 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K4096_N1024_rank3batch1_Texture3D        [1x2048x4096]        2072.347 μs       8290.054 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.1-8b_prefill_wk_wv_linear_dq8ca_q4gsw_M2048_K4096_N1024_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K4096_N14336_rank3batch1_Texture3D (M=2048, K=4096, N=14336, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8254 of 29360128 elements
[sampled reference] max abs diff 0.031 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (32,512,1)      (2,1,32)                                                                                                                  333.860 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (57344,16,1)    (256,1,1)                                                                                                               24133.271 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K4096_N14336_rank3batch1_Texture3D        [1x2048x4096]       24467.131 μs       9830.257 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.1-8b_prefill_w1_w3_linear_dq8ca_q4gsw_M2048_K4096_N14336_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] llama-3.1-8b_prefill_w2_linear_dq8ca_q4gsw_M2048_K14336_N4096_rank3batch1_Texture3D (M=2048, K=14336, N=4096, group_size=128)
Executing 1 test cases for LlamaMicrobenchProductionDiff
----------------------------------------------------------------------
[sampled reference] checking 8209 of 8388608 elements
[sampled reference] max abs diff 0.124 (tol 0.500), max rel diff 0.000 (tol 0.050, |ref| > abs tol)
quantize_and_pack_4h4w_with_group_sums_o2w32..     (112,512,1)     (2,1,32)                                                                                                                 1203.404 μs                                 
sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s..     (16384,16,1)    (256,1,1)                                                                                                               24165.377 μs                                 
et_vk.linear_dq8ca_q4gsw.default                                               llama-3.1-8b_prefill_w2_linear_dq8ca_q4gsw_M2048_K14336_N4096_rank3batch1_Texture3D       [1x2048x14336]       25368.779 μs       9480.873 GFLOP/s   PASSED
----------------------------------------------------------------------
Completed 1 test cases
[production-diff] llama-3.1-8b_prefill_w2_linear_dq8ca_q4gsw_M2048_K14336_N4096_rank3batch1_Texture3D -> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half (coopmat dispatched), correctness=PASSED
[production-diff] ALL PASSED (llama-3.1-8b, 4 shapes, M=2048, linear_dq8ca_q4gsw, texture3d)
```

## table_amd.cpp: file comment, wave64 predicate and the 780M 8da4w row

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp`, lines 9-11

```text
// SARC selection rows for AMD GPUs. First matching row wins, so list the most
// specific device first. Status kVerified requires sarc/tools/verify.sh
// evidence on that device (see sarc/README.md).
```

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp`, lines 19-24

```text
// The shipped RDNA coopmat variants were built and validated for wave64
// adapters that support cooperative matrix; they force subgroup 32 per
// pipeline (SUBGROUP_SIZE in the yaml).
bool amd_wave64(const DeviceInfo& d) {
  return d.is_amd && d.subgroup_size == 64;
}
```

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp`, lines 42-53

```text
    // Radeon 780M 8da4w: zpg (4h4w activations), full A map. Verified on
    // release 1.5 (sarc-1.5-8da4w-port): kernels 0.992x of the 1.4 study;
    // with the SDPA rows, prefill 1B/3B/8B 2544/1048/487 tok/s (1.4:
    // 2538/1055/486).
    {"780m",
     amd_wave64,
     Op::kDq8caLinear,
     "sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32",
     {128, 64, 32, 4, 2, 32, 16, false},
     kTex3dTex2d | kBufTex2d,
     nullptr,
     Status::kVerified},
```

## Select.h: TileDims field order and storage sets

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/Select.h`, lines 80-94

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
```

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/Select.h`, lines 96-102

```text
// Storage combinations (IO_STORAGE x WEIGHT_STORAGE) a variant is built for;
// the yaml must contain <kernel_base>_<io>_<weight>_half for each set bit.
enum StorageSet : uint8_t {
  kTex3dTex2d = 1u << 0, // texture3d input/output, texture2d weight
  kBufTex2d = 1u << 1, // buffer input/output, texture2d weight
  kBufBuf = 1u << 2, // buffer input/output, buffer weight
};
```

Locator: `backends/vulkan/runtime/graph/ops/impl/sarc/Select.h`, lines 104-116

```text
struct Row {
  const char* device_substr; // matched against DeviceInfo::name
  bool (*device_ok)(const DeviceInfo&); // extra device requirements, or null
  Op op;
  const char* kernel_base; // shader name without _<io>_<weight>_<dtype>
  TileDims dims;
  uint8_t storages; // StorageSet bits
  // Extra shape requirement (beyond tile alignment), or null. Rows are tried
  // in order, so a later row can serve the shapes an earlier one rejects.
  bool (*shape_ok)(const ShapeInfo&);
  Status status;
  bool rowmajor_a = false; // kDq8caLinear: reads row-major int8 activations
};
```

## zpg yaml: defaults and the 780M variants

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.yaml`, line 7

```text
# SARC release zone: shipped zpg variants (rows in impl/sarc/table_<vendor>.cpp).
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.yaml`, lines 10-35

```text
sarc_linear_dq8ca_coopmat_zpg:
  parameter_names_with_default_values:
    PRECISION: highp
    HAS_BIAS: false
    IO_STORAGE: buffer
    WEIGHT_NBITS: 4
    WEIGHT_STORAGE: texture2d
    A_MAP_FULL: false
    A_MULTI_BLOCK: false
    A_BLOCKS: 1
    MMA_M: 16
    MMA_N: 16
    MMA_K: 16
    WG_TILE_M: 128
    WG_TILE_N: 64
    WG_TILE_K: 32
    SG_GRID_X: 4
    SG_GRID_Y: 2
    SUBGROUP_SIZE: 32
  shader_variants:
    # Radeon 780M (RDNA3). 1.4 branch yanwen/release14-quant-shaders-780m.
    - NAME: sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half
      A_MAP_FULL: true
    - NAME: sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half
      IO_STORAGE: texture3d
      A_MAP_FULL: true
```

## zpg shader template header

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl`, lines 9-19 (line 20, which names another device, and the closing line 21 are not excerpted)

```text
/*
 * SARC dq8ca (8da4w) int8 cooperative-matrix linear, "zpg" family: 4h4w int8
 * activations, zero-point hoisted out of the group loop, dbuf4 pipeline.
 *
 * Template header only (bindings, spec constants, per-variant tile geometry);
 * the kernel is the untemplated sarc_linear_dq8ca_coopmat_zpg_body.glslh, shared with the sweep twin
 * glsl/sarc_dev/sarc_linear_dq8ca_coopmat_zpg_sweep.glsl, which must stay byte-identical to this
 * file from the version directive on (sarc/tools/check.sh).
 *
 * Feature defines (yaml parameters, default off):
 *   A_MAP_FULL     every thread stages exactly one A block (full A map)
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl`, lines 23-31

```text
#version 450 core

#extension GL_KHR_cooperative_matrix : require
#extension GL_KHR_memory_scope_semantics : require
#extension GL_KHR_shader_subgroup_basic : enable
#extension GL_EXT_shader_explicit_arithmetic_types : require
#extension GL_EXT_shader_explicit_arithmetic_types_int8 : require
#extension GL_EXT_shader_explicit_arithmetic_types_float16 : require
#extension GL_EXT_control_flow_attributes : enable
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl`, lines 38-45

```text
// INTERVENTION G: when the A staging thread map exactly covers the workgroup
// (A_ACTIVE_THREADS == WG_SIZE) the `a_active` guard is statically always true,
// but the driver compiler does not fold it -- gl_LocalInvocationID.x's bound
// comes from a spec constant, so the comparison survives into the hot loop as a
// real branch. Set A_MAP_FULL only for tiles where the equality has been
// checked arithmetically; the yaml records the arithmetic per variant.
$if A_MAP_FULL:
  #define A_ALWAYS_ACTIVE
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl`, lines 60-76

```text
// Bindings — match add_linear_dqa_qw_node arg order:
//   output(0), fp_input(1), packed_int8_input(2), int_input_sums(3 - unused),
//   input_scales(4), input_zps(5), packed_weight(6), weight_sums(7),
//   weight_scales(8), bias(9).
${layout_declare_tensor(B, "w", "t_output",              "half", IO_STORAGE, is_scalar_array=True)}
// t_input is unread here -- the activations arrive already quantized in
// t_packed_int8_input -- but stays declared so the binding layout matches the
// dispatch site. It tracks IO_STORAGE so the two IO tensors stay consistent.
${layout_declare_tensor(B, "r", "t_input",               "half", IO_STORAGE, is_scalar_array=False)}
${layout_declare_tensor(B, "r", "t_packed_int8_input",   "int",  "buffer", is_scalar_array=False)}
${layout_declare_tensor(B, "r", "t_int8_input_sums",     "int",  "buffer", is_scalar_array=True)}
${layout_declare_tensor(B, "r", "t_int8_input_scales",   "half", "texture3d")}
${layout_declare_tensor(B, "r", "t_int8_input_zps",      "int8", "texture3d")}
${layout_declare_tensor(B, "r", "t_packed_weight",       "int",  WEIGHT_STORAGE, is_scalar_array=False)}
${layout_declare_tensor(B, "r", "t_weight_sums",         "int",  "buffer", is_scalar_array=True)}
${layout_declare_tensor(B, "r", "t_weight_scales",       "half", "buffer", is_scalar_array=False)}
${layout_declare_tensor(B, "r", "t_bias",                "half", "buffer", is_scalar_array=True)}
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl`, line 81

```text
layout(local_size_x_id = 0, local_size_y_id = 1, local_size_z_id = 2) in;
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.glsl`, lines 89-100

```text
// Tile geometry
const uint MMA_M = ${MMA_M};
const uint MMA_N = ${MMA_N};
const uint MMA_K = ${MMA_K};

const uint WG_TILE_M = ${WG_TILE_M};
const uint WG_TILE_N = ${WG_TILE_N};
const uint WG_TILE_K = ${WG_TILE_K};

const uint SG_GRID_X = ${SG_GRID_X};
const uint SG_GRID_Y = ${SG_GRID_Y};
const uint SUBGROUP_SIZE = ${SUBGROUP_SIZE};
```

## zpg kernel body: workgroup size, staging and accumulators

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh`, lines 16-22

```text
const uint NUM_SUBGROUPS = SG_GRID_X * SG_GRID_Y;
const uint WG_SIZE = NUM_SUBGROUPS * SUBGROUP_SIZE;

const uint SG_TILE_M = WG_TILE_M / SG_GRID_Y;
const uint SG_TILE_N = WG_TILE_N / SG_GRID_X;
const uint MMAS_PER_SG_M = SG_TILE_M / MMA_M;
const uint MMAS_PER_SG_N = SG_TILE_N / MMA_N;
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh`, lines 37-43

```text
// One ping-pong slice covers all K-slabs of one chunk.
const uint ASH_SLICE_U32 = NUM_K_SLABS * A_SLAB_U32;
const uint BSH_SLICE_U32 = NUM_K_SLABS * B_SLAB_U32;

// Double-buffered MMA operand staging.
shared uint Ash_int8[2u * ASH_SLICE_U32];
shared uint Bsh_int8[2u * BSH_SLICE_U32];
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg_body.glslh`, lines 71-77

```text
// Running fp32 accumulator (across all groups).
coopmat<float, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator>
    result[MMAS_PER_SG_M][MMAS_PER_SG_N];

// Per-group int32 MMA accumulator.
coopmat<int32_t, gl_ScopeSubgroup, MMA_M, MMA_N, gl_MatrixUseAccumulator>
    accum_int32[MMAS_PER_SG_M][MMAS_PER_SG_N];
```

## SWEEP-PARAMETERS.md: families, zpg parameters, preconditions, naming, shipped 780M variants

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 8-12

```text
| Scheme | Family | Activation layout |
|---|---|---|
| 4w | `sarc_linear_q4gsw_coopmat` | fp16 |
| 8da4w | `sarc_linear_dq8ca_coopmat_zpg` | int8, 4h4w blocks |
| 8da4w | `sarc_linear_dq8ca_coopmat_zpgtr` | int8, row-major (`kPackedInt8_4W`) |
```

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 17-18

```text
The choice between zpg and zpgtr is itself a sweep dimension. The op path (`impl/sarc/Dq8caCoopmat.cpp`)
packs the activations in the layout of the kernel that the build-time shape selects.
```

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 22-26 (table header and three rows; the following rows name other devices and are not excerpted)

```text
| Parameter | Meaning | Values used so far |
|---|---|---|
| `WG_TILE_M`, `WG_TILE_N` | Output tile per workgroup | M 32/64/128/256; N 32/64/128/256 (32 only in sweep candidates) |
| `WG_TILE_K` | K consumed per main-loop iteration | 16 / 32 / 64 |
| `SG_GRID_X`, `SG_GRID_Y` | Subgroup grid in the workgroup (X along N, Y along M); workgroup size = X·Y·`SUBGROUP_SIZE` | 2×1, 2×2, 4×2, 2×4, 4×4, 4×8 |
```

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 53-57 (the remaining rows of this table name other devices and are not excerpted)

```text
## 8da4w zpg only (`sarc_linear_dq8ca_coopmat_zpg`)

| Parameter | Effect | Used by |
|---|---|---|
| `WEIGHT_NBITS` | Weight bit width; 4 defines `WEIGHT_INT4` | 4 |
```

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 72-81

```text
## Hard preconditions

The shaders contain no shape checks. `sarc::select()` enforces these when it matches a row:
- `M % WG_TILE_M == 0`, `N % WG_TILE_N == 0`, `K % WG_TILE_K == 0`;
- `group_size % WG_TILE_K == 0`;
- no bias, batch 1, not a single-token (gemv) call;
- the storage combination is allowed by the row's `storages` mask;
- `SUBGROUP_SIZE` equals the device's subgroup size, or lies within its supported range when subgroup-size
  control is available;
- shared memory fits the device limit (`max_compute_shared_memory_size`).
```

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 83-87

```text
The table row must also repeat the tile geometry in its `TileDims`, because launch dims come from the row and
kernel names are never parsed. `test_sarc_select` checks that every row names an existing variant.

Rows for the row-major (zpgtr) path stay on their kernel for every M. This is the unaligned-M fix:
the activation layout was fixed at build time, so the op cannot fall back to a 4h4w kernel.
```

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 97-102

```text
| Token part | Meaning |
|---|---|
| `t<M>x<N>` | `WG_TILE_M` × `WG_TILE_N` |
| `k<K>` | `WG_TILE_K` |
| `g<X><Y>` | `SG_GRID_X`, `SG_GRID_Y` |
| `s<S>` | `SUBGROUP_SIZE` |
```

Locator: `sarc/SWEEP-PARAMETERS.md`, line 121

```text
Any other shipped flag, such as zpg's `A_MAP_FULL`, is not in the name. Read the yaml entry.
```

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 125-127

```text
| Device | 4w | 8da4w |
|---|---|---|
| Radeon 780M | `t128x128k32g42s32f32c` | zpg `t128x64k32g42s32` + `A_MAP_FULL` |
```

Locator: `sarc/SWEEP-PARAMETERS.md`, lines 152-154

```text
**Other dev switches:**
- `ET_VK_SARC_UNVERIFIED=1` activates `kUnverified` rows.
- `ET_VK_FORCE_TILED_LINEAR=1` sends the SARC linears to release 1.5's tiled/coop kernels, as the baseline.
```

## sarc/README.md: device status row

Locator: `sarc/README.md`, lines 78-82

```text
## Devices (release 1.5 status)

| Device | 4w | 8da4w | SDPA prefill | Evidence |
|---|---|---|---|---|
| Radeon 780M | verified | verified | verified | `openspec/changes/sarc-1.5-{bootstrap,8da4w-port,sdpa-port}` |
```
