---
id: meas-orin-fused-port
title: "Jetson Orin Nano: fused attention kernel (fused3sb with a one-full-subgroup guard), one-pass against two-pass per head dimension, against the tuned three-kernel parent (sarc-1.5-orin-fused-port)"
source_category: measurement
architectures: [jetson-orin]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, kernel-fusion, cooperative-matrix, subgroup-size, control-barrier, full-subgroups, required-subgroup-size]
device: jetson-orin
driver: "NVIDIA 595.78"
measured_at: '2026-10-09'
method: "Records of one tuning campaign, quoted from the pushed branch at the commit given per locator. End-to-end cells: llama_main, one 2048-token prefill per run, prefill tok/s, parent and candidate arms interleaved, median of the valid runs per arm (count stated in the excerpts); six cells = Llama 3.2 1B, Llama 3.2 3B, Llama 3.1 8B in the 4w and 8da4w schemes. Gate: SDPA correctness tiers of test_llama_microbench against a CPU reference, the campaign's verify script, and a next-token comparison between the arms. Device and driver are quoted from the vulkaninfo lines of the session's env.txt. Lines of the cited files that hold a host name, a board address or a storage path are not excerpted. Gate session s5-c1 ran on 2026-10-09 on the build of commit 0bed380905e134c73b56838e4e920e953ee1234a; 5 valid interleaved runs per arm. The build is a cross build whose shader compiler differs from the one the campaign's reference SPIR-V was made with (quoted below). Kernel-level screen of the four forms: test_llama_microbench --sdpa, time per layer at S = 2048, 3 interleaved rounds."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb
    locator: openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/env.txt
    description: "Gate session environment: date, arms and commits, vulkaninfo device and driver lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb
    locator: openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/summary.csv
    description: "Gate session per-cell medians, gain, validity counts and next-token column"
  - repo: https://github.com/sarc-acl/executorch
    commit: da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb
    locator: openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/gate.done
    description: "Gate verdict line"
  - repo: https://github.com/sarc-acl/executorch
    commit: da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb
    locator: openspec/changes/sarc-1.5-orin-fused-port/proposal.md
    description: "Campaign record: the port, shared memory, run-time check, compiler limitation, result, candidates, trace"
  - repo: https://github.com/sarc-acl/executorch
    commit: da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb
    locator: openspec/changes/sarc-1.5-orin-fused-port/STATUS.md
    description: "Running log: kernel-level times of the four forms of the ported kernel"
  - repo: https://github.com/sarc-acl/executorch
    commit: da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb
    locator: openspec/changes/sarc-1.5-orin-fused-port/results/orin/screens/sdpa-screen1.csv
    description: "Kernel-level screen rows of the four forms"
  - repo: https://github.com/sarc-acl/executorch
    commit: da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb
    locator: openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/runs.csv
    description: "Gate session per-run rows behind summary.csv"
captured_at: '2026-10-10'
commit: 0bed380905e134c73b56838e4e920e953ee1234a
baseline: "Tuned parent: commit 8973ced76c6e346f34dc5b31b4755c423ceabc99 with profile orin-refine5 and softmax orin_g64 (three attention kernels). Second reference: the same commit with no environment."
---

## Device, driver, session and arms

Locator: `openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/env.txt`, line 1 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
Fri Oct  9 07:13:34 AM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/env.txt`, lines 17-20 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
session s5-c1 staged 2026-10-09T05:58:11Z
parent = build/parent env [ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_DEV_PROFILE=orin-refine5 ET_VK_SARC_SOFTMAX_VARIANT=orin_g64] commit 8973ced76c6e346f34dc5b31b4755c423ceabc99
cand   = build/topic4 env [ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_DEV_PROFILE=orin-fused1] commit 0bed380905e134c73b56838e4e920e953ee1234a
candidate 1 again on topic4: the fused attention kernel (profile orin-fused1) against the parent build with the parent environment
```

Locator: `openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/env.txt`, lines 42-45 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
	apiVersion         = 1.4.329
	deviceName         = NVIDIA Tegra Orin (nvgpu)
	driverName         = NVIDIA
	driverInfo         = 595.78
```

## Candidate orin-fused1 against the tuned parent, per cell, and gate verdict

Locator: `openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/summary.csv`, lines 1-8 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
model,scheme,parent_med_tok_s,cand_med_tok_s,ratio,gain_pct,outside_2pct_band,parent_spread_pct,cand_spread_pct,valid_parent,valid_cand,invalid,clk_med_mhz_range,temp_pre_range,clkmin,next_token
1b,4w,1490.54,1656.96,1.1117,+11.17,yes,0.36,0.40,5,5,-,612-612,55-58,593,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
1b,8da4w,1379.12,1520.42,1.1025,+10.25,yes,0.54,0.37,5,5,-,612-612,58-59,593,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
3b,4w,629.19,659.58,1.0483,+4.83,yes,0.15,0.10,5,5,-,612-612,59-59,593,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
3b,8da4w,570.32,595.35,1.0439,+4.39,yes,0.14,0.06,5,5,-,612-612,59-59,593,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
8b,4w,295.44,305.49,1.0340,+3.40,yes,0.06,0.10,5,5,-,612-612,59-60,593,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
8b,8da4w,269.05,277.24,1.0305,+3.05,yes,0.09,0.04,5,5,-,612-612,59-60,593,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
geomean over 6 cells: 1.0613 (+6.13 %), min 1.0305, max 1.1117
```

Locator: `openspec/changes/sarc-1.5-orin-fused-port/results/orin/sessions/s5-c1/gate.done`, line 1 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
GATE_ACCEPTED 2026-10-09T08:00:47Z all steps passed; the gain is in raw/summary.csv
```

## Result section of the campaign record: cells, candidates, trace

Locator: `openspec/changes/sarc-1.5-orin-fused-port/proposal.md`, lines 224-259 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
## Result

Final stack: `ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_DEV_PROFILE=orin-fused1` on build `topic4`. Tok/s, 2048-token
prefill, median of 5 valid interleaved runs per arm:

| cell | published `dev/1.5` | pristine (`s8-pristine`) | tuned parent (`s5-c1`) | final stack (`s5-c1`) | over the parent | over pristine (`s8-pristine`) |
|---|---:|---:|---:|---:|---:|---:|
| 1B 4w | 890.82 | 891.60 | 1490.54 | 1656.96 | +11.17 % | +85.24 % |
| 1B 8da4w | 822.82 | 823.81 | 1379.12 | 1520.42 | +10.25 % | +84.70 % |
| 3B 4w | 360.37 | 360.50 | 629.19 | 659.58 | +4.83 % | +82.96 % |
| 3B 8da4w | 320.30 | 320.35 | 570.32 | 595.35 | +4.39 % | +85.79 % |
| 8B 4w | 189.74 | 189.84 | 295.44 | 305.49 | +3.40 % | +60.94 % |
| 8B 8da4w | 170.43 | 170.48 | 269.05 | 277.24 | +3.05 % | +62.60 % |
| geomean | | | | | **+6.13 %** | **+76.70 %** |

Both sessions: 60 of 60 timed runs valid, GPU clock 612 MHz in every run, thermal throttle state 0 in every
clock sample, repeat spread at most 0.54 %, next token the same as the other arm on all four prompts in every
cell. A/A under the same rules (`s4-aa2`): +0.07 %.

| candidate | profile | gate | gain over its parent | outcome |
|---|---|---|---:|---|
| 1: fused attention kernel, one pass, packed K / V | `orin-fused1` | `s5-c1` on `topic4` (first: `s3-c1` on `topic1`, +6.01 %) | +6.13 % | **ACCEPTED (reference-error rule, owner decision 2026-10-04)**: criterion 1 met on the five S = 2048 cases (`results/orin/sdpa-error2/`), 41-prompt probe of the final stack with no gross divergence (`results/orin/probe/final-fused/`), differing next-token items: none. The gate's own `gate.done` reads `GATE_ACCEPTED ... all steps passed` and is kept as written |
| 2: two-pass form for head_dim 64 | `orin-fused2` | `s6-c2` on `topic4`, against candidate 1 | +0.54 % (1B +1.72 / +1.59 %) | GATE_ACCEPTED on the gate and on criterion 1 of the reference-error rule only (`sdpa-error2`, next token SAME in 24 of 24 rows); no broad real-text probe of `orin-fused2` exists, so no D3 acceptance is claimed for it; every cell inside the +-2 % band: not adopted. Gated as candidate 2 by the owner's decision of 2026-10-09 01:00 UTC; the pre-registered clause of `thresholds.txt` (an unpacked form) stays unedited and by its letter there was no candidate 2 |

Stop: two candidates at most (task), candidate 2 sub-threshold; closed by N3 with candidate 1 as the result.

Where the gain comes from (warm ETDump of `s5-c1`, ms per 2048-token prefill, parent -> final):

| cell | QK^T + softmax + attn*V | fused kernel + K / V copy | attention | dispatch total |
|---|---:|---:|---|---|
| 1B 4w | 302.1 | 172.2 + 3.1 | 302.1 -> 175.3 (-42 %) | 1359.2 -> 1225.2 |
| 1B 8da4w | 302.1 | 171.9 + 3.1 | 302.1 -> 175.0 | 1469.9 -> 1333.9 |
| 3B 4w | 516.0 | 371.0 + 11.5 | 516.0 -> 382.5 (-26 %) | 3236.6 -> 3086.8 |
| 3B 8da4w | 516.6 | 371.2 + 11.3 | 516.6 -> 382.4 | 3571.0 -> 3420.0 |
| 8B 4w | 783.2 | 561.8 + 13.0 | 783.2 -> 574.7 (-27 %) | 6916.6 -> 6686.1 |
| 8B 8da4w | 783.3 | 561.1 + 12.9 | 783.3 -> 573.9 | 7588.6 -> 7363.1 |
```

## Kernel level: the four forms (one pass, two passes, packed, unpacked)

Locator: `openspec/changes/sarc-1.5-orin-fused-port/STATUS.md`, lines 579-599 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
## Kernel level: the four forms of the ported kernel (`sdpa-screen1`, 22:12 to 22:25 UTC, build `topic1`)

`test_llama_microbench --sdpa`, ms per layer at S = 2048 (copy pass + fused kernel; the parent: QK^T + softmax +
attn*V), 3 rounds interleaved, every round listed (`results/orin/screens/sdpa-screen1.csv`):

| form | 1B (head_dim 64, `t32x32`) | 3B (head_dim 128, `t16x64`) | 8B (head_dim 128, `t16x64`) |
|---|---|---|---|
| parent, three kernels | 18.87 / 18.89 / 18.90 | 18.45 / 18.46 / 18.45 | 24.45 / 24.48 / 24.48 |
| `rko` one pass, packed (**candidate 1**) | 11.62 / 11.53 / 11.59 | 13.84 / 13.90 / 13.90 | 18.25 / 18.27 / 18.25 |
| `rk` two passes, packed | **9.61 / 9.62 / 9.64** | 19.19 / 19.20 / 19.26 | 25.26 / 25.27 / 25.33 |
| `ro` one pass, unpacked | 17.21 / 17.26 / 17.29 | 47.11 / 47.08 / 47.19 | 62.27 / 62.28 / 62.47 |
| `r` two passes, unpacked | 23.56 / 23.43 / 23.47 | 66.46 / 66.51 / 66.35 | 88.28 / 88.35 / 88.42 |

- The copy passes save far more than they cost: unpacked is 1.5 times (head_dim 64) and 3.4 times (128) slower.
  By the clause of `thresholds.txt` there is no "unpacked" candidate.
- One pass against two: for head_dim 128 the one-pass form takes 28 % less time, as on the 780M; for head_dim 64 it is
  20.4 % slower (median 11.59 against 9.62 ms; the two-pass form takes 17.0 % less time and clears the 3 % margin
  in every round). On the 780M the one-pass form won for both. The two-pass form computes the scores twice, but it
  declares 2 KB less shared memory per workgroup (no rescale divisors) and has no rescale branch; the first
  campaign measured that a workgroup's time on this device grows with the shared memory it declares. That is an
  observation that fits, not a measured cause.
```

## The port: variants and what changed against the source kernel

Locator: `openspec/changes/sarc-1.5-orin-fused-port/proposal.md`, lines 65-81 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
## The port

What runs: for an LLM-mode attention call with fp16 buffers whose shape fits (S a multiple of the row tile and of
the column tile, `input_pos` a multiple of the column tile, head_dim 64 or 128), the node
`impl/sarc_dev/orin/SdpaOrinFused.cpp` dispatches `sarc_dev_orin_sdpa_kvt` (tile-packed copies of K and V for the
visible context) and then `sarc_dev_orin_sdpa_fused3sb_<variant>`, and the QK^T, softmax and attention x V nodes
dispatch nothing. Every other call (decode, an unaligned prompt) runs the parent's three kernels with the softmax
`orin_g64`, exactly as the parent does: an `orin-fused*` profile carries the preferences of `orin-refine5` and
names that softmax itself, so one variable selects the whole stack.

| head_dim | models | rows x columns per workgroup | `orin-fused1` (candidate 1) | `orin-fused2` (candidate 2) |
|---|---|---|---|---|
| 64 | 1B | 32 x 32, 32 invocations | `fused3sb_d64_t32x32g11s32rko` (one pass) | `fused3sb_d64_t32x32g11s32rk` (two passes) |
| 128 | 3B, 8B | 16 x 64, 32 invocations | `fused3sb_d128_t16x64g11s32rko` (one pass) | the same |

`r`: Q tiles kept in registers; `k`: tile-packed K and V; `o`: one pass with a running row maximum. The yaml also
builds the unpacked forms (`ro`, `r`), reachable only through `ET_VK_SARC_ORIN_SDPA_FUSED` for kernel timing.
```

Locator: `openspec/changes/sarc-1.5-orin-fused-port/proposal.md`, lines 85-88 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
| item | source | here | why |
|---|---|---|---|
| fused kernel from `#version` on | `sarc_dev_780m_sdpa_fused3sb.glsl` of the RX 7600 branch (`b3bb758e38`): the 780M's third structure with `subgroupBarrier()` after every `memoryBarrierShared()` | the same text plus five lines after the row-range check: `if (gl_NumSubgroups != 1u \|\| gl_SubgroupSize != SUBGROUP_SIZE) return;` (commit `0bed38090`, as the 4070 Ti port has it) | the shared memory is private to one subgroup only if the workgroup is one full subgroup. The pipeline requires subgroup size 32 but not full subgroups (release zone), so the kernel checks it and writes nothing otherwise: the correctness tiers then fail instead of the kernel racing silently |
| constants (`MMA`, tiles, `SUBGROUP_SIZE`, `P_STRIDE`, spec constants) | | unchanged | fp16 16 x 16 x 16 matrices with fp32 result and subgroup 32 exist on this device (`results/orin/vk-caps-first-campaign.txt`) |
```

## Shared memory per workgroup and the shared-memory reading

Locator: `openspec/changes/sarc-1.5-orin-fused-port/proposal.md`, lines 95-102 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
Shared memory of one workgroup:

| array | elements | d64 `t32x32` | d128 `t16x64` | holds |
|---|---|---:|---:|---|
| `Psh` | `WG_TILE_M x max(WG_TILE_N / 8 + 1, 4)` uvec4 | 32 x 5 x 16 = 2560 B | 16 x 9 x 16 = 2304 B | the block's scores (fp16), then e (fp16); at the end the row sums as 16 fp32 per row |
| `Rsh` | `WG_TILE_M x SEGS` float | 128 B | 128 B | per-invocation block or row maximum, at the end the per-invocation row sum |
| `Dsh` (one-pass forms only) | `WG_TILE_M x 4` vec4 | 2048 B | 1024 B | per-row rescale divisor exp(new maximum - old maximum), 16 fp32 per row |
| total, one pass / two passes | | 4736 / 2688 B | 3456 / 2432 B | |
```

Locator: `openspec/changes/sarc-1.5-orin-fused-port/proposal.md`, lines 104-112 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
The reading of the kernel for unsynchronised shared writes (who writes each slot, what orders each read by
another invocation), the specification sentences it rests on and the SPIR-V barrier counts are in `STATUS.md`
("Shared-memory reading of the kernel", "Specification text the shader reading rests on", and the row on the
one-full-subgroup check under "What I took from the 4070 Ti fused port"). In short: every slot of `Psh`, `Rsh`
and `Dsh` has exactly one writing invocation or is written by a cooperative-matrix store of the whole subgroup;
every read of a slot another invocation wrote comes after `memoryBarrierShared(); subgroupBarrier();`; every
read phase is closed by the same pair before the slot is written again; every barrier is in control flow that
is uniform over the subgroup (the block loop bound and both early returns depend on the workgroup only, the one
conditional block is entered on `subgroupAny`). The copy passes use no shared memory.
```

## The record's description of the run-time check

Locator: `openspec/changes/sarc-1.5-orin-fused-port/proposal.md`, lines 142-150 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
- What the kernel's run-time check does: `sarc_dev_orin_sdpa_fused3sb` returns before any shared-memory access
  unless `gl_NumSubgroups == 1` and `gl_SubgroupSize == 32`, so with a driver that splits a workgroup of 32
  into several subgroups the kernel writes nothing and the correctness tiers fail instead of two subgroups
  exchanging through one `Psh` / `Rsh` / `Dsh`. On this driver it never fired: 222 of 222 cases per gate are
  served by the fused kernel and correct.
- What it does not do: it does not make the pipeline valid as created; it does not guarantee that all 32
  invocations of the one subgroup are active (that is what the flag specifies); and it covers the fused kernel
  only: the parent's QK^T, softmax and attention x V kernels, which still serve decode and unaligned prompts in
  the final stack, and the shipped cooperative-matrix linear kernels have no such check.
```

## Known limitation: shader compiler of the cross build

Locator: `openspec/changes/sarc-1.5-orin-fused-port/proposal.md`, lines 171-174 (commit `da92b4b3ceec6e6cf09759c6ed8d7fc25c92aedb`)

```text
**Every number of this campaign is measured on builds whose shaders were compiled by the cross image's `glslc`,
not by the compiler the goldens were made with.** By the owner's decision byte identity of the measured build's
SPIR-V with `sarc/golden/spirv.json` is not required for this campaign, the numbers stand as measured on `topic4`,
nothing is measured again, and the difference does not keep the campaign open.
```
