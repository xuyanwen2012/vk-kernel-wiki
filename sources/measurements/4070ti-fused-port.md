---
id: meas-4070ti-fused-port
title: "RTX 4070 Ti SUPER: fused attention kernel (fused3sb, one-pass, with a one-full-subgroup run-time guard) against the tuned three-kernel parent (sarc-1.5-4070ti-fused-port)"
source_category: measurement
architectures: [rtx-4070-ti-super]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, kernel-fusion, cooperative-matrix, subgroup-size, control-barrier, full-subgroups, required-subgroup-size, shared-memory-limit]
device: rtx-4070-ti-super
driver: "NVIDIA 615.71.09"
measured_at: '2026-10-09'
method: "Records of one tuning campaign, quoted from the pushed branch at the commit given per locator. End-to-end cells: llama_main, one 2048-token prefill per run, prefill tok/s, parent and candidate arms interleaved, median of the valid runs per arm (count stated in the excerpts); six cells = Llama 3.2 1B, Llama 3.2 3B, Llama 3.1 8B in the 4w and 8da4w schemes. Gate: SDPA correctness tiers of test_llama_microbench against a CPU reference, the campaign's verify script, and a next-token comparison between the arms. Device and driver are quoted from the vulkaninfo lines of the session's env.txt. Lines of the cited files that hold a host name, a board address or a storage path are not excerpted. Gate session s4-c1 and closing session s5-pristine ran on 2026-10-09 on the build of commit ed8b5af9186a9eba00c29f0ce8e2c0b9413ca688; 7 valid interleaved runs per arm; the sampler read the driver's throttle reasons every 20 ms. Attention block times are from warm ETDump traces. Kernel-level figures: test_llama_microbench --sdpa, three interleaved rounds, time per layer at S = 2048."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: 8f8c44e22e2d8c62a6a192f00e252f8768486b0d
    locator: openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md
    description: "Campaign record: device properties, the port, shared memory, barrier reasoning, result, attention trace, kernel-level figures"
  - repo: https://github.com/sarc-acl/executorch
    commit: 8f8c44e22e2d8c62a6a192f00e252f8768486b0d
    locator: openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/env.txt
    description: "Gate session environment: date, vulkaninfo device and driver lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: 8f8c44e22e2d8c62a6a192f00e252f8768486b0d
    locator: openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/summary.csv
    description: "Gate session per-cell medians, gain, validity counts and next-token column"
  - repo: https://github.com/sarc-acl/executorch
    commit: 8f8c44e22e2d8c62a6a192f00e252f8768486b0d
    locator: openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/gate.done
    description: "Gate verdict"
  - repo: https://github.com/sarc-acl/executorch
    commit: 8f8c44e22e2d8c62a6a192f00e252f8768486b0d
    locator: openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/trace/attention.csv
    description: "Attention kernels of the warm traces, both arms"
  - repo: https://github.com/sarc-acl/executorch
    commit: 8f8c44e22e2d8c62a6a192f00e252f8768486b0d
    locator: openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/screens/sdpa-screen2.csv
    description: "Kernel-level screen rows"
  - repo: https://github.com/sarc-acl/executorch
    commit: 8f8c44e22e2d8c62a6a192f00e252f8768486b0d
    locator: openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/runs.csv
    description: "Gate session per-run rows behind summary.csv"
captured_at: '2026-10-10'
commit: ed8b5af9186a9eba00c29f0ce8e2c0b9413ca688
baseline: "Tuned parent: commit 6050b1287 with profile 4070ti-refine1 (cooperative-matrix QK^T and attn*V and the fp32 no-tail softmax as three kernels). Second reference: the same build with no environment."
---

## Device, driver and session date

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md`, lines 10-13 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
- Device: NVIDIA GeForce RTX 4070 Ti SUPER, driver 615.71.09 (as found 2026-10-08), the only GPU of a KVM guest;
  subgroup size 32 (minimum = maximum), `computeFullSubgroups` and `subgroupSizeControl` available,
  `maxComputeSharedMemorySize` 49152 bytes, at most 1024 invocations per workgroup. Clock policy as found:
  P0, 3120 MHz maximum, 285 W limit; not changed.
```

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/env.txt`, line 1 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
Fri Oct  9 01:52:48 AM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/env.txt`, lines 42-45 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
	apiVersion         = 1.4.351
	deviceName         = NVIDIA GeForce RTX 4070 Ti SUPER
	driverName         = NVIDIA
	driverInfo         = 615.71.09
```

## Candidate 4070ti-fused1 against the tuned parent, per cell, and gate verdict

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/summary.csv`, lines 1-8 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
model,scheme,parent_med_tok_s,cand_med_tok_s,ratio,gain_pct,outside_2pct_band,parent_spread_pct,cand_spread_pct,valid_parent,valid_cand,invalid,clk_med_mhz_range,temp_pre_range,clkmin,next_token
1b,4w,29681.20,35310.30,1.1897,+18.97,yes,2.90,1.75,7,7,-,2640-2790,45-50,2517,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
1b,8da4w,32507.90,39384.60,1.2115,+21.15,yes,1.61,1.96,7,7,-,2640-2640,49-50,2517,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
3b,4w,12962.00,14027.40,1.0822,+8.22,yes,0.00,0.69,7,7,-,2625-2640,50-50,2517,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
3b,8da4w,14948.90,16254.00,1.0873,+8.73,yes,1.46,2.40,7,7,-,2640-2640,48-50,2517,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
8b,4w,6023.53,6380.06,1.0592,+5.92,yes,0.29,0.31,7,7,-,2595-2640,50-50,2517,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
8b,8da4w,6989.76,7474.45,1.0693,+6.93,yes,1.03,0.73,7,7,-,2640-2760,47-50,2517,prompt_real_2048:SAME;prompt_check:SAME;r1304:SAME;prompt_2048:SAME
geomean over 6 cells: 1.1149 (+11.49 %), min 1.0592, max 1.2115
```

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/results/4070ti/sessions/s4-c1/gate.done`, line 1 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
GATE_ACCEPTED 2026-10-09T02:38:27Z all steps passed; the gain is in raw/summary.csv
```

## Result section of the campaign record

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md`, lines 179-212 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
## Result

One candidate, accepted: **+11.49 % geomean over the parent** (the first campaign's stack), inside the band the
task predicted (+8 to +12 %), **+63.28 % over the pristine `dev/1.5` state** (the first campaign's
stack alone: +46.74 % in its gate session `s5-c4`, +46.35 % in its committed-build session `s8-c4e`). The numbers are those of build `topic3` (`ed8b5af91`), gate `s4-c1` and closing session
`s5-pristine`, the sessions that record the driver's throttle reasons per run. tok/s, median of 7 valid
interleaved runs per arm:

| cell | pristine `dev/1.5` (`s5-pristine`) | published (`cells.csv`) | parent, `4070ti-refine1` (`s4-c1`) | `4070ti-fused1` (`s4-c1` / `s5-pristine`) | gain over the parent | gain over pristine | gain over published |
|---|---:|---:|---:|---|---:|---:|---:|
| 1B 4w | 19883.5 | 19692.3 | 29681.2 | 35310.3 / 35929.8 | +18.97 % | +80.70 % | +82.46 % |
| 1B 8da4w | 21113.4 | 20898.0 | 32507.9 | 39384.6 / 39384.6 | +21.15 % | +86.54 % | +88.46 % |
| 3B 4w | 8752.1 | 8752.1 | 12962.0 | 14027.4 / 14027.4 | +8.22 % | +60.27 % | +60.27 % |
| 3B 8da4w | 9752.4 | 9660.4 | 14948.9 | 16254.0 / 16254.0 | +8.73 % | +66.67 % | +68.25 % |
| 8B 4w | 4511.0 | 4491.2 | 6023.5 | 6380.1 / 6400.0 | +5.92 % | +41.88 % | +42.50 % |
| 8B 8da4w | 5056.8 | 5031.9 | 6989.8 | 7474.5 / 7501.8 | +6.93 % | +48.35 % | +49.08 % |
| geomean | | | | | **+11.49 %** | **+63.28 %** | +64.34 % |

The gains over the published numbers use the unrounded medians of `cells.csv`.

- `s4-c1` (the gate, 2026-10-09 01:09 to 02:38 UTC): GATE_ACCEPTED, plain pass: 36 of 36 SDPA passes (12 each of
  `all`, `extended`, `full`; 192 cases) with 0 mismatches and `pairing=ok`, `verify.out` equal to the parent
  snapshot line by line with rates removed, next token SAME in 24 of 24 rows, 84 timed runs all valid, 12
  traces. `s5-pristine` (02:40 to 02:54 UTC): 84 timed runs all valid, `gate_check.py session` ACCEPT with 0
  findings, next token SAME in 24 of 24 rows against the stock attention kernels too. In both, every timed run
  has at least 48 samples of the driver's throttle reasons and no thermal reason in any of them. The pristine
  arm is within 1.03 % of the published numbers in every cell.
- History: the first gate (`s2-c1`, build `topic2`) read +11.64 % and the first closing session (`s3-pristine`)
  +63.53 %. Review round 1 found that they had not recorded throttle reasons, that the gate lacked the 12 `all`
  passes, and that the shared test file had been edited in place. They are kept as evidence with that
  limitation; the absence of throttling in them is not inferred. The candidate's medians agree with the new
  sessions within two steps of the 1 ms timer in every cell (at most 1.6 %, on 3B 8da4w).
- 1B cells are whole milliseconds (69 -> 58 ms, 63 -> 52 ms); one timer step is 1.7 to 1.9 % of the candidate's
  time. ETDump dispatch totals: 67.6 -> 56.3 ms and 61.2 -> 50.0 ms.
```

## Where the gain comes from, and kernel-level times

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md`, lines 214-231 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
Where the gain comes from: the attention block alone (warm ETDump, ms per prefill, parent -> candidate;
`results/4070ti/sessions/s4-c1/trace/attention.csv`):

| cell | QK^T + softmax + attention x V (parent) | fused kernel + K / V copy (candidate) | attention removed | linear GEMM | everything else | attention share of the prefill |
|---|---|---|---:|---|---|---|
| 1B 4w | 4.18 + 7.47 + 5.42 = 17.07 | 5.71 + 0.11 = 5.82 | 66 % | 34.30 -> 34.21 | 16.19 -> 16.29 | 25 % -> 10 % |
| 1B 8da4w | 4.15 + 7.46 + 5.41 = 17.02 | 5.70 + 0.11 = 5.81 | 66 % | 27.66 -> 27.67 | 16.50 -> 16.56 | 28 % -> 12 % |
| 3B 4w | 8.44 + 9.80 + 8.17 = 26.40 | 13.58 + 0.34 = 13.92 | 47 % | 96.58 -> 95.74 | 33.06 -> 32.94 | 17 % -> 10 % |
| 3B 8da4w | 8.35 + 9.70 + 8.09 = 26.14 | 13.34 + 0.33 = 13.67 | 48 % | 74.76 -> 74.38 | 35.11 -> 35.01 | 19 % -> 11 % |
| 8B 4w | 13.01 + 14.92 + 11.63 = 39.56 | 20.29 + 0.44 = 20.73 | 48 % | 239.58 -> 238.70 | 60.96 -> 60.79 | 12 % -> 6 % |
| 8B 8da4w | 12.51 + 14.83 + 11.49 = 38.83 | 19.40 + 0.42 = 19.82 | 49 % | 181.16 -> 181.27 | 71.21 -> 73.08 | 13 % -> 7 % |

Kernel level, for comparison with the other devices (`test_llama_microbench --sdpa`, us per layer at S = 2048,
three interleaved rounds on `topic3`, `results/4070ti/screens/sdpa-screen2.csv`): fused kernel plus copy pass
against QK^T + softmax + attention x V of the parent: 1B 369 to 381 against 1059 to 1065 (0.35 to 0.36x), 3B 488
to 510 against 935 to 942 (0.52 to 0.55x), 8B 619 to 654 against 1211 to 1215 (0.51 to 0.54x); the stock
kernels of `dev/1.5` take about 3220, 3545 and 4705. The d64 variant gains more than the d128 one, as the 1B
cells show end to end. (`sdpa-screen1.csv` is the same screen on `topic2`: the same ratios within 0.02.)
```

## The port: variants and what changed against the source kernel

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md`, lines 84-99 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
## The port (candidate 1, profile `4070ti-fused1`)

What runs: for an LLM-mode attention call with fp16 buffers whose shape fits (S a multiple of the row tile and
of the column tile, `input_pos` a multiple of the column tile, head_dim 64 or 128), the node
`impl/sarc_dev/4070ti/Sdpa4070tiFused.cpp` dispatches `sarc_dev_4070ti_sdpa_kvt` (tile-packed copies of K and V
for the visible context) and then `sarc_dev_4070ti_sdpa_fused3sb_<variant>`, and the QK^T, softmax and
attention x V nodes dispatch nothing. Every other call (decode, an unaligned prompt) runs the three kernels of
`4070ti-refine1` with the `4070ti_nzf` softmax, exactly as the parent does.

| head_dim | variant | rows x columns per workgroup | workgroup | models |
|---|---|---|---|---|
| 64 | `fused3sb_d64_t32x32g11s32rko` | 32 x 32 | 32 invocations = 1 subgroup | 1B |
| 128 | `fused3sb_d128_t16x64g11s32rko` | 16 x 64 | 32 invocations = 1 subgroup | 3B, 8B |

These are the two variants the Radeon 780M and the RX 7600 run (`r` Q tiles kept in registers, `k` tile-packed
K and V, `o` one pass with a running row maximum). No other variant is built and none was screened.
```

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md`, lines 101-110 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
What changed against the source kernels:

| item | 780M / RX 7600 | here | why |
|---|---|---|---|
| shader text from `#version` on | `sarc_dev_780m_sdpa_fused3sb.glsl` (RX 7600 commit `b3bb758e38`) | the same plus four lines: `if (gl_NumSubgroups != 1u \|\| gl_SubgroupSize != SUBGROUP_SIZE) return;` after the row-range check | the kernel's shared memory is private to one subgroup only if the workgroup is one subgroup; the pipeline asks for subgroup size 32 but nothing asks for full subgroups, so the kernel checks it itself and writes nothing otherwise (the correctness tiers then fail on stale output instead of racing silently) |
| constants (`MMA`, tiles, `SUBGROUP_SIZE`, `P_STRIDE`, spec constants) | | unchanged | 16 x 16 x 16 fp16 and fp32-accumulator matrices and subgroup 32 exist on this card |
| name prefix | `sarc_dev_780m_sdpa_` | `sarc_dev_4070ti_sdpa_` | separable content; `Sdpa780mFused.cpp` is not edited |
| copy pass | `sarc_dev_780m_sdpa_kvt.glsl` | the same text from `#version` on, workgroup 8 x 8 fixed | |
| the unpacked path (`vt`) and the two-pass and unpacked variants | built | not built | not what the AMD cards ship |
| selection | `ET_VK_SARC_780M_SDPA_FUSED` or the 780M profile variable | `ET_VK_SARC_DEV_PROFILE=4070ti-fused1` alone | one name per configuration |
```

## Shared memory per workgroup

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md`, lines 112-119 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
Shared memory of one workgroup (limit on this card 49152 bytes):

| array | elements | d64 `t32x32` | d128 `t16x64` | holds |
|---|---|---:|---:|---|
| `Psh` | `WG_TILE_M x max(WG_TILE_N / 8 + 1, 4)` uvec4 | 32 x 5 x 16 = 2560 B | 16 x 9 x 16 = 2304 B | the block's scores (fp16), then e (fp16); at the end the row sums as 16 fp32 per row |
| `Rsh` | `WG_TILE_M x SEGS` float | 32 x 1 x 4 = 128 B | 16 x 2 x 4 = 128 B | per-invocation block maximum, at the end the per-invocation row sum |
| `Dsh` | `WG_TILE_M x 4` vec4 | 32 x 4 x 16 = 2048 B | 16 x 4 x 16 = 1024 B | per-row rescale divisor exp(new max - old max), 16 fp32 per row |
| total | | 4736 B | 3456 B | |
```

## Barrier reasoning and where the one-subgroup assumption is enforced

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md`, lines 121-146 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
Barrier reasoning for NVIDIA. Invocation `l` of the subgroup owns row `l % WG_TILE_M` and column segment
`l / WG_TILE_M` (one segment of 32 columns for d64; two segments of 32 for d128). Who writes each slot and
what orders each read by another invocation:

| step (per column block unless noted) | write | writer | read by | ordered by |
|---|---|---|---|---|
| scores | `Psh` rows x columns of the block | the subgroup's cooperative-matrix store (`coopMatStore`, subgroup scope) | each invocation, its own segment | `memoryBarrierShared(); subgroupBarrier();` after the store |
| block maximum (d128 only, `SEGS > 1`) | `Rsh[row x SEGS + segment]` | the owning invocation, one slot each | both invocations of the row | barriers after the write; barriers again after the reads, before the slot is written in the next block |
| rescale divisor (only when `subgroupAny` saw a maximum rise: the branch is uniform over the subgroup) | `Dsh[row x 4 + j]`, `j` = segment, segment + SEGS, ... | the owning invocation(s) of the row; disjoint slots, equal values (both segments hold the same running maximum) | the subgroup's `coopMatLoad` of the divisor tile | barriers after the writes; barriers after the loads |
| e = exp(score - maximum) | `Psh`, own segment | the owning invocation | the subgroup's `coopMatLoad` in attention x V | barriers after the writes; barriers after attention x V, before the next block's score store |
| row sum (once, at the end) | `Rsh[row x SEGS + segment]` | the owning invocation | both invocations of the row | barriers after the write (the last reads of `Rsh` were followed by barriers) |
| denominator (once) | `Psh[row x P_STRIDE + j]`, `j` as for `Dsh` | the owning invocation(s); disjoint slots | the subgroup's `coopMatLoad` | barriers after the writes (the last loads of `Psh` were followed by barriers) |

No slot is written by two invocations, no value is reduced into one shared slot by several lanes (the lesson
of L8 does not arise in this kernel), and no invocation reads a slot another invocation wrote without an
execution barrier between the write and the read. Every barrier is in control flow that is uniform over the
subgroup: the block loop bound and both early returns depend on the workgroup only, and the one conditional
block is entered on `subgroupAny`. The 780M's `fused3` has the same structure with `memoryBarrierShared()`
alone, which orders nothing between invocations that are scheduled independently; that form is not built here.

Where the one-subgroup assumption is enforced: (1) the local size is the variant's `g11s32` = 32 invocations
(`pick_fused_gwg`, `pick_required_lwg`); (2) the pipeline is created with required subgroup size 32 (the
`SUBGROUP_SIZE` parameter of the yaml becomes `// REQUIRED_SUBGROUP_SIZE = 32`, read back by
`resolve_required_subgroup_size`; this card's minimum and maximum subgroup size are both 32); (3) the kernel
returns unless `gl_NumSubgroups == 1` and `gl_SubgroupSize == 32`. The copy pass `kvt` has no shared memory and
writes each element of the copies from exactly one invocation.
```

## Arithmetic

Locator: `openspec/changes/sarc-1.5-4070ti-fused-port/proposal.md`, lines 148-151 (commit `8f8c44e22e2d8c62a6a192f00e252f8768486b0d`)

```text
Arithmetic: scores and the attention x V accumulation are fp32 cooperative-matrix accumulators as in the
parent's kernels; the score is rounded to fp16 once (store to `Psh`), e is computed in fp32 against the running
maximum and rounded to fp16 for the matrix multiply, the row sum and the final division are fp32. The summation
order differs from the three-kernel path, so the candidate is judged by the reference-error rule (D3).
```
