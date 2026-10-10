---
id: meas-b580-fused-port
title: "Arc B580: multi-subgroup fused attention kernel (8 x 16 x 16 matrices, subgroups of 16) against the tuned three-kernel parent; straight-port compiler statistics; full-subgroups defect F1 (sarc-1.5-b580-fused-port)"
source_category: measurement
architectures: [arc-b580]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, kernel-fusion, cooperative-matrix, subgroup-size, control-barrier, full-subgroups, coopmat-shape, required-subgroup-size, subgroup-grid, shared-memory-limit]
device: arc-b580
driver: "ANV Mesa 26.2.3"
measured_at: '2026-10-09'
method: "Records of one tuning campaign, quoted from the pushed branch at the commit given per locator. End-to-end cells: llama_main, one 2048-token prefill per run, prefill tok/s, parent and candidate arms interleaved, median of the valid runs per arm (count stated in the excerpts); six cells = Llama 3.2 1B, Llama 3.2 3B, Llama 3.1 8B in the 4w and 8da4w schemes. Gate: SDPA correctness tiers of test_llama_microbench against a CPU reference, the campaign's verify script, and a next-token comparison between the arms. Device and driver are quoted from the vulkaninfo lines of the session's env.txt. Lines of the cited files that hold a host name, a board address or a storage path are not excerpted. The reported sessions (s6-final against the tuned parent, s7-pristine) ran on 2026-10-09 on the build of commit e1e450530f088a576c03d5e7b4af91a2647218a0, 7 valid runs per arm, every run started at once. Compiler statistics come from a compile-time dump (INTEL_DEBUG=cs with the shader cache disabled), not from a hardware counter. Kernel-level screens: test_llama_microbench --sdpa, time per layer at S = 2048, 3 rounds. All pipelines were created without the full-subgroups flag (the record's finding F1)."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/STATUS.md
    description: "Running log: driver, sessions under the authorized protocol, compiler statistics of the straight port, shared-memory reading"
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/env.txt
    description: "Final gate session environment: date, arms and commits, vulkaninfo device and driver lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/summary.csv
    description: "Final gate session per-cell medians, gain, validity counts and next-token column"
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/gate.done
    description: "Final gate verdict"
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/proposal.md
    description: "Campaign record: the port in two parts, shared memory per variant, result table, known defect F1, decode ratios"
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/results/b580/screens/screen5-select.csv
    description: "Selection screen: kernel time per layer of the parent and of the fused variants, per model"
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/results/b580/compile/topic4-fused-kernels.txt
    description: "Compiler statistics dump of the fused pipelines"
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/gate.txt
    description: "Final gate PASS and FAIL lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: a434a49623600f168089173a964efc79661ac286
    locator: openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/runs.csv
    description: "Final gate per-run rows behind summary.csv"
captured_at: '2026-10-10'
commit: e1e450530f088a576c03d5e7b4af91a2647218a0
baseline: "Tuned parent: commit 51d9d757ff4b23c72fbcdbf1e2c20ed5fba28ee4 with profile b580-refine3 (cooperative-matrix QK^T, release fp16 softmax and attn*V as three kernels). Second reference: pristine parent 6a7cc8cc6 with no profile."
---

## Device, driver, session and arms

Locator: `openspec/changes/sarc-1.5-b580-fused-port/STATUS.md`, lines 15-17 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
ANV Mesa 26.2.3 throughout; kernel 7.2.8-200.fc44 until the reboot of 2026-10-09 01:17 UTC, 7.2.9-200.fc44 after
it; GT frequency policy as found and unchanged (`min_freq` 1200, `max_freq` 2850, `rp0` 2850 MHz,
`power_profile` `[base] power_saving`).
```

Locator: `openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/env.txt`, line 1 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
Fri Oct  9 10:45:23 AM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/env.txt`, lines 16-19 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
session s6-final staged 2026-10-09T10:06:46Z
parent = build/parent2 env [ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_DEV_PROFILE=b580-refine3] commit 51d9d757ff4b23c72fbcdbf1e2c20ed5fba28ee4
cand   = build/topic7 env [ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_DEV_PROFILE=b580-fused1] commit e1e450530f088a576c03d5e7b4af91a2647218a0
final stack b580-fused1 on the committed head against the parent (b580-refine3); repeats the gate of s4-final without busy_wait
```

Locator: `openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/env.txt`, lines 27-30 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
	apiVersion         = 1.4.354
	deviceName         = Intel(R) Arc(tm) B580 Graphics (BMG G21)
	driverName         = Intel open-source Mesa driver
	driverInfo         = Mesa 26.2.3
```

## Final stack b580-fused1 against the tuned parent, per cell, and gate verdict

Locator: `openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/summary.csv`, lines 1-8 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
model,scheme,parent_med_tok_s,cand_med_tok_s,ratio,gain_pct,outside_2pct_band,parent_spread_pct,cand_spread_pct,valid_parent,valid_cand,invalid,clk_med_mhz_range,temp_pre_range,next_token_2048/check/unaligned,fbusy_pct_med_max
1b,4w,13044.60,15058.80,1.1544,+15.44,yes,0.63,0.73,7,7,-,2817-2850,39-44,SAME/SAME/SAME,0.34/0.39
1b,8da4w,15170.40,18285.70,1.2054,+20.54,yes,0.75,0.88,7,7,-,2850-2850,44-45,SAME/SAME/SAME,0.33/0.46
3b,4w,5197.97,5461.33,1.0507,+5.07,yes,0.51,0.27,7,7,-,2783-2783,45-46,SAME/SAME/SAME,0.31/0.37
3b,8da4w,6420.06,6849.50,1.0669,+6.69,yes,0.31,0.33,7,7,-,2850-2850,44-45,SAME/SAME/SAME,0.32/0.38
8b,4w,2308.91,2381.40,1.0314,+3.14,yes,0.34,0.12,7,7,-,2717-2733,45-47,SAME/SAME/SAME,0.32/0.34
8b,8da4w,2998.54,3145.93,1.0492,+4.92,yes,0.15,0.15,7,7,-,2850-2850,42-47,SAME/SAME/SAME,0.32/0.33
geomean over 6 cells: 1.0912 (+9.12 %), min 1.0314, max 1.2054
```

Locator: `openspec/changes/sarc-1.5-b580-fused-port/results/b580/sessions/s6-final/gate.done`, line 1 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
GATE_PASS
```

Locator: `openspec/changes/sarc-1.5-b580-fused-port/STATUS.md`, lines 126-147 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
`s6-final` (10:06 to 11:06 UTC; timed runs 10:46 to 11:04): `parent2` with the parent environment against
`topic7` with `b580-fused1`, the full gate (`gate_sdpa.sh`). The runner had the `busy_unreadable` predicate of
the owner decision of 09:55 UTC from before its timed runs. 84 timed runs, 84 valid; foreign engine time 0.26 to
0.46 %:

| cell | parent `b580-refine3` | final `b580-fused1` | gain | spread parent / final | next token (2048 / real-text / 1792-token prompt) |
|---|---:|---:|---:|---|---|
| 1B 4w | 13044.60 | 15058.80 | **+15.44 %** | 0.6 / 0.7 % | SAME / SAME / SAME |
| 1B 8da4w | 15170.40 | 18285.70 | **+20.54 %** | 0.7 / 0.9 % | SAME / SAME / SAME |
| 3B 4w | 5197.97 | 5461.33 | **+5.07 %** | 0.5 / 0.3 % | SAME / SAME / SAME |
| 3B 8da4w | 6420.06 | 6849.50 | **+6.69 %** | 0.3 / 0.3 % | SAME / SAME / SAME |
| 8B 4w | 2308.91 | 2381.40 | **+3.14 %** | 0.3 / 0.1 % | SAME / SAME / SAME |
| 8B 8da4w | 2998.54 | 3145.93 | **+4.92 %** | 0.1 / 0.2 % | SAME / SAME / SAME |

Geomean **+9.12 %**, every cell outside the +-2 % band (`s4-final`, behind the wait: +8.82 %; `s2-c1`, desktop in
use: +9.18 %). `stage/s6-final/gate.txt`: `GATE_PASS`, 37 PASS lines (the 36 of the earlier gates and the new
line "no run stored valid without a readable foreign engine share"), no FAIL line: SDPA tiers `all` /
`extended` / `full` 12 passes each with 0 mismatches and `pairing=ok`, unmodified `verify.sh` with the final
environment the same as the parent snapshot, next token SAME in all 18 comparisons. A plain pass on the timing
and correctness items, on pipelines created without the full-subgroups flag (F1; known defect, owner decision
of 15:25 UTC). Reference error, the extra tiers, the golden check and the roofs do not depend on the start time
and are those of the first closing on the same build (below).
```

## Result section of the campaign record

Locator: `openspec/changes/sarc-1.5-b580-fused-port/proposal.md`, lines 293-321 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
## Result

Final stack: the branch head with `ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_DEV_PROFILE=b580-fused1`. Measured on the
build of the committed head (`topic7` = `e1e450530`, no local patch; later commits change `openspec/` only), 7
valid runs per arm, every run started at once, tok/s, sessions `s6-final` (parent) and `s7-pristine` (pristine
parent); `STATUS.md` has the validity counts, the traces and the verification. **These are numbers of pipelines
created without the full-subgroups flag (F1, next section).**

| cell | parent `b580-refine3` | `b580-fused1` | gain | pristine `6a7cc8cc6` | `b580-fused1` (that session) | total gain |
|---|---:|---:|---:|---:|---:|---:|
| 1B 4w | 13044.60 | 15058.80 | +15.44 % | 8677.97 | 15058.80 | +73.53 % |
| 1B 8da4w | 15170.40 | 18285.70 | +20.54 % | 8865.80 | 18285.70 | +106.25 % |
| 3B 4w | 5197.97 | 5461.33 | +5.07 % | 3442.02 | 5461.33 | +58.67 % |
| 3B 8da4w | 6420.06 | 6849.50 | +6.69 % | 3524.96 | 6849.50 | +94.31 % |
| 8B 4w | 2308.91 | 2381.40 | +3.14 % | 1726.81 | 2384.17 | +38.07 % |
| 8B 8da4w | 2998.54 | 3145.93 | +4.92 % | 1845.05 | 3141.10 | +70.24 % |

Geomean **+9.12 %** over the parent (expected ceiling +5 to +8 %), **+72.05 %** over the pristine parent, +76.2 %
over the published numbers. `s6-final` is `GATE_PASS`, a plain pass: the next token is the parent's in all six
cells on the three prompts, and the error against the fp32 reference is not larger than the parent's on every
production shape. The first closing (`s4-final`, `s5-pristine`: +8.82 % and +71.77 %), started through a wait the
owner had not authorized, is kept in `STATUS.md` and is not the evidence. Candidate 2 (`b580-fused2`, the fp32
no-tail softmax `4070ti_nzf` through the D4.1 hook for the calls the fused kernel does not take) read +0.08 %
(`s3c-c2`; -0.13 % with `GATE_PASS` in `s3b-c2`) and is not part of the final stack; the profile stays
selectable. The stop rule "after candidate 2 whatever the result" ended the campaign.

Kernel level (us per layer at S = 2048, idle desktop, screen 5), for predicting the B70: the parent's three
kernels 1989 (1B) / 1771 (3B) / 2297 (8B); the fused kernel with its copy pass 724 / 1139 / 1464: 2.75x / 1.55x /
1.57x. Variants: `d64_t16x64s16m8g4roj` (head_dim 64) and `d128_t16x128s16m8g8oj` (head_dim 128).
```

## The port, part 1: matrix shape, and the straight port's time

Locator: `openspec/changes/sarc-1.5-b580-fused-port/proposal.md`, lines 62-84 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
## The port: what changed from the 780M / RX 7600 kernel

Source: `sarc_dev_780m_sdpa_fused3sb.glsl` (`topic/rx7600-prefill-refine`, `b3bb758e38`), the `fused3` kernel with a
`subgroupBarrier()` after every `memoryBarrierShared()`. Result: `glsl/sarc_dev/sarc_dev_b580_sdpa_fused.glsl`.
The arithmetic, the block walk, the masks and the packed K / V layout are the 780M's. Two things had to change:
the matrix shape, which is mechanical, and the unit of work, which is not.

**1. Matrix shape (mechanical).**

| item | 780M / RX 7600 | B580 | why |
|---|---|---|---|
| matrix shape | `MMA = 16`, square, for every tile | `MMA_M = 8`, `MMA_N = 16`, `MMA_K = 16`, three constants | ANV exposes fp16 8 x 16 x 16 only |
| score, e, accumulator, Q, divisor tiles | 16 rows x 16 | 8 rows x 16: `coopmat<.., MMA_M, MMA_N, Accumulator>`, Q as `coopmat<.., MMA_M, MMA_K, A>` | the M of every product is the query row |
| operand tiles K^T (d x c) and V (c x d) | 16 x 16 `B` | `coopmat<.., MMA_K, MMA_N, B>` = 16 x 16 | both are K x N, unchanged, so the packed copies keep the 780M's layout and the copy shader (`kvt`) is the 780M's |
| tile counts | `MMAS_M = WG_TILE_M / 16`, `MMAS_C = WG_TILE_N / 16`, `MMAS_D = HEAD_DIM / 16` | `MMAS_M = WG_TILE_M / MMA_M`, the other two `/ MMA_N` | row tiling follows the 8-row matrix |
| row offsets of tile i into `Psh`, `Dsh`, `t_q`, `t_output` | `16 * i * stride` | `MMA_M * i * stride` | as above; the softmax part indexes `Psh` per row and segment and does not change |
| subgroup size | 32, not required by the pipeline | 16, required by the pipeline through the yaml `SUBGROUP_SIZE`, like the Xe2 kernels | Intel runs 8, 16 or 32 lanes |
| selection | `ET_VK_SARC_780M_SDPA_FUSED` beside the profile | the profile alone: `b580-fused1` | owner: single-name configurations |
| forms kept | unpacked, transposed-V, packed; measurement-only variant | packed only; one-pass (`o`) and two-pass | the packed form is what both AMD campaigns ship |

With only these changes the kernel is correct (five tiers, 0 mismatches) and 3 to 6 times slower than the
parent's three kernels in the 780M's shapes (`results/b580/screens/screen5-select.csv`: 5.9 ms against 2.0 ms
for head_dim 64, 14.4 ms against 2.3 ms for head_dim 128 on 8B).
```

## The port, part 2: several subgroups per workgroup

Locator: `openspec/changes/sarc-1.5-b580-fused-port/proposal.md`, lines 86-109 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
**2. Unit of work: several subgroups per workgroup instead of one.** The 780M kernel assumes that one subgroup
keeps all its tiles in registers: for head_dim 128 that is 16 fp32 accumulator tiles, 16 fp16 Q tiles and a
block of score tiles. On this card a thread has 128 registers = 4096 bytes of 16-lane values, and the fp32
accumulators of 8 rows x 128 alone are 4096 bytes. The compiler's statistics (`INTEL_DEBUG=cs`,
`results/b580/compile/`) show 199 to 1250 spilled values for the head_dim 128 variants and 32 for the one
single-subgroup variant that beat the three kernels. What was tried and what it did is in `STATUS.md`; what
is kept:

| item | 780M / RX 7600 | B580 (`MULTI_SG`, G = 4 or 8 subgroups) |
|---|---|---|
| workgroup | one subgroup, 16 or 32 rows | G subgroups of 16 lanes, 16 rows; local size G x 16 |
| accumulators | all head_dim tiles of the rows in one subgroup | each subgroup owns `HEAD_DIM / 16 / G` head_dim tiles of the rows (one 16-wide slice in the chosen variants): 2 tiles |
| scores of a block | all tiles computed and stored by the one subgroup | subgroup g computes the columns j with `j % G == g`, one column at a time (`QK_J_OUTER`), and stores them to `Psh` |
| softmax part | lane = (row, segment), `SEGS = 32 / WG_TILE_M` | the same over all G x 16 lanes: `lane = gl_SubgroupID * 16 + gl_SubgroupInvocationID`, `SEGS = G * 16 / WG_TILE_M` |
| e of a block | loaded from `Psh` by the one subgroup | loaded from `Psh` by every subgroup (it needs all columns for its head_dim slice) |
| barriers | `memoryBarrierShared()` (`fused3`), plus `subgroupBarrier()` (`fused3sb`) | `memoryBarrierShared(); barrier();` at the same places (`SYNC()`): the slots are now shared between subgroups |
| rescale decision of the one-pass form | `subgroupAny(new_max > row_max)` | an atomic flag in shared memory read by every lane after a barrier, so that the branch, which contains barriers, is uniform for the workgroup |
| Q tiles | in registers (`AQ_REG`) | head_dim 64: in registers; head_dim 128: loaded per product (16 Q tiles are 2048 bytes of registers) |
| workgroup = G full subgroups | assumed (one subgroup) | checked in the kernel (`gl_NumSubgroups == G`, `gl_SubgroupSize == 16`), NaN rows otherwise (seen by the gate through the non-finite `[sdpa-error]` record, not through the mismatch count): the release-zone pipeline code sets the required size but not the full-subgroups flag (known defect F1) |

No product changes and every tile accumulates in the same order as in the 780M kernel; the row sum is added
up per lane segment first, as there, with 4 or 8 segments a row instead of 1 or 2. K and V are still read
straight from the packed copies and nothing is staged for another subgroup except the block's scores and e,
which the single-subgroup form also keeps in shared memory.
```

Locator: `openspec/changes/sarc-1.5-b580-fused-port/proposal.md`, lines 111-118 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
Shared memory (device limit 49152 bytes, measured in the first campaign): `Psh` `WG_TILE_M x max(WG_TILE_N / 8 + 1, 4)`
uvec4, `Rsh` one float per lane, `Dsh` `WG_TILE_M x 4` vec4, `Gsh` one uint.

| variant (rows x block, lanes) | `Psh` | `Rsh` | `Dsh` | total bytes |
|---|---:|---:|---:|---:|
| `b580-fused1`, head_dim 64: 16 x 64, 4 x 16 | 2304 | 256 | 1024 | 3588 |
| `b580-fused1`, head_dim 128: 16 x 128, 8 x 16 | 4352 | 512 | 1024 | 5892 |
| the 780M's shapes: 32 x 32, 32 and 16 x 64, 32 | 2560 / 2304 | 128 | 2048 / 1024 | 4736 / 3456 |
```

Locator: `openspec/changes/sarc-1.5-b580-fused-port/proposal.md`, lines 122-127 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
The node (`impl/sarc_dev/b580/SdpaB580Fused.cpp`, from `780m/Sdpa780mFused.cpp`): it serves an LLM-mode call when
q is an fp16 buffer, the device has active attention rows (only the B580 with a `b580-*` profile and
`ET_VK_SARC_UNVERIFIED=1`), the profile names a variant for the head_dim, and S and `input_pos` are multiples of
the row tile and of the block (64 columns for head_dim 64, 128 for head_dim 128). Every other call (decode, the
1972-token prompt, `ET_VK_DISABLE_COOPMAT`) runs the three kernels of `b580-refine3`, which the profile also
selects.
```

## Compiler statistics of the fused pipelines and the forms tried

Locator: `openspec/changes/sarc-1.5-b580-fused-port/STATUS.md`, lines 442-477 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
Compiler statistics of the fused pipelines (`INTEL_DEBUG=cs` with the shader cache disabled: a compile-time
dump of the test process, no hardware counter; `results/b580/compile/topic4-fused-kernels.txt`). ANV compiles
the kernel for 16 lanes with 128 registers:

| variant | instructions | spills : fills | kernel us per layer (where measured) |
|---|---:|---:|---|
| `d64_t8x32 ro` (the only form of screen 1 that beat the three kernels) | 1304 | 32 : 57 | 1375 (1B), idle |
| `d64_t16x32 ro` | 3974 | 204 : 313 | 2585 to 2718 |
| `d128_t8x64 ro` | 4178 to 5187 | 199 : 336 to 268 : 470 | 3520 (8B) |
| `d128_t16x64 ro` (the 780M's shape at 16 lanes) | 15093 to 16537 | 1114 : 1309 to 1250 : 1467 | 17056 (8B) |
| `d128_t8x64 g2 oj` (2 subgroups) | 1107 | 0 : 0 | |
| `d128_t8x64 g4 roj` (4 subgroups) | 768 | 0 : 0 | |
| `d128_t16x64 g4 oj` | 1155 | 0 : 0 | |
| `d64_t16x64 g4 roj` | 924 | 0 : 0 | |

A thread's register file holds 4096 bytes of 16-lane values; the fp32 accumulators of 8 rows x head_dim 128
alone are 4096 bytes. So one subgroup cannot own whole rows of head_dim 128 on this card, whatever the tile.

What was tried, in order (all correct in a pass of tiers `extended`, `peaked`, `fused`; `raw/c1-smoke2..3/`):

1. `j`: one column of score tiles live instead of a block's. No real effect (1B `t8x32`: 1311 against 1339 us,
   idle).
2. `a`: accumulators in shared memory, loaded and stored around each block. Slower in every case (one-shot look
   with the desktop in use, `results/b580/looks/look1-*.txt`: head_dim 128 5.7 to 11 ms against 3.5 ms). Shared
   memory is not a cheap extension of the register file here.
3. `g<G>`: **a workgroup of G subgroups.** Each subgroup owns 1 / G of the score-tile columns of a block and
   1 / G of the head_dim tiles of the accumulators; the block's scores and e values go through shared memory
   (`Psh`), which every subgroup reads, so the barriers become workgroup barriers and the rescale decision of
   the one-pass form is taken for the whole workgroup (an atomic flag in shared memory instead of
   `subgroupAny`). K and V are still read straight from the packed copies; no product changes and every tile
   accumulates in the same order; the row sum is added up per lane segment first, as before, with 4 or 8
   segments a row instead of 1 or 2. One-shot look with the desktop in use (`results/b580/looks/look2-*.txt`; the parent's kernels read
   2308 / 1788 / 2255 us for 8B / 3B / 1B in the same look, 0 to 9 % above their idle values):
   `d128_t16x64 g4 oj` 1508 / 1195 us (8B / 3B), `d128_t8x64 g4 roj` 2063 / 1716, `d128_t8x64 g2 oj` 2217 / 1732;
   `d64_t16x64 g4 roj` 726 us (1B), `d64_t8x32 g2 roj` 944, `d64_t8x32 oj` 1178. These are single disturbed runs:
   a direction, not a result.
```

## Selection screen (kernel time per layer, ms)

Locator: `openspec/changes/sarc-1.5-b580-fused-port/results/b580/screens/screen5-select.csv`, lines 1-8 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
profile,llama-3.1-8b_qk,llama-3.1-8b_softmax,llama-3.1-8b_av,llama-3.1-8b_total,llama-3.1-8b_x,llama-3.1-8b_min_x,llama-3.2-1b_qk,llama-3.2-1b_softmax,llama-3.2-1b_av,llama-3.2-1b_total,llama-3.2-1b_x,llama-3.2-1b_min_x,llama-3.2-3b_qk,llama-3.2-3b_softmax,llama-3.2-3b_av,llama-3.2-3b_total,llama-3.2-3b_x,llama-3.2-3b_min_x,geomean_x,n
b580-refine3,0.57,1.07,0.66,2.30,1.000,1.000,0.42,1.07,0.50,1.99,1.000,1.000,0.44,0.81,0.52,1.77,1.000,1.000,1.000,3
b580-fused-d64_t32x32s32m8ro,0.57,1.07,0.66,2.30,1.000,1.000,0.00,0.00,0.00,5.94,0.335,0.333,0.44,0.81,0.52,1.77,1.002,0.992,0.695,3
b580-fused-d128_t16x64s32m8ro,0.00,0.00,0.00,14.42,0.159,0.156,0.42,1.07,0.49,2.00,0.996,0.916,0.00,0.00,0.00,11.00,0.161,0.160,0.295,3
b580-fused-d64_t16x64s16m8g4roj,0.57,1.07,0.66,2.30,1.000,0.968,0.00,0.00,0.00,0.72,2.748,2.738,0.44,0.81,0.52,1.77,1.001,1.001,1.401,3
b580-fused-d64_t16x64s16m8g4oj,0.57,1.07,0.66,2.30,1.001,0.989,0.00,0.00,0.00,0.82,2.424,2.422,0.44,0.81,0.52,1.77,1.002,0.991,1.345,3
b580-fused-d128_t16x128s16m8g8oj,0.00,0.00,0.00,1.46,1.569,1.569,0.42,1.07,0.49,1.99,1.001,0.999,0.00,0.00,0.00,1.14,1.554,1.550,1.346,3
b580-fused-d128_t16x64s16m8g4oj,0.00,0.00,0.00,1.56,1.472,1.470,0.42,1.07,0.49,1.98,1.003,1.001,0.00,0.00,0.00,1.21,1.465,1.436,1.293,3
```

## Shared-memory reading of the multi-subgroup form

Locator: `openspec/changes/sarc-1.5-b580-fused-port/STATUS.md`, lines 603-631 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
## Shared-memory reading of the fused kernel (R7; the final form, written before its gate)

Read on `glsl/sarc_dev/sarc_dev_b580_sdpa_fused.glsl` at `247d08851`, multi-subgroup form (`MULTI_SG`), one-pass
(`ONLINE`), as `b580-fused1` builds it. A workgroup is G subgroups of 16 lanes (G = 4 or 8). Lane
`L = gl_SubgroupID * 16 + gl_SubgroupInvocationID` owns row `L % 16` and segment `L / 16` of every block: a
bijection between the G x 16 invocations and the (row, segment) pairs. Every barrier is
`memoryBarrierShared(); barrier();` (`SYNC()`), a workgroup barrier.

| slot | writer | reader | what orders the read after the write |
|---|---|---|---|
| `Psh` scores, tile (i, j) | one `coopMatStore` by the subgroup that owns column j (`j % G == gl_SubgroupID`); tiles are disjoint ranges of `Psh` | each lane reads its own segment of its own row | `SYNC()` right after `qk_block` |
| `Rsh[row * SEGS + seg]` (block maximum; at the end the row's partial sum) | the one lane that owns (row, seg) | every lane of the row reads all `SEGS` slots | `SYNC()` between the store and the reads, and another after the reads before the slot is written again |
| `Gsh` ("some row's maximum rose") | any lane, only with `atomicOr(Gsh, 1)`; cleared by lane 0 alone | every lane reads it once to decide the rescale | `SYNC()` after the `atomicOr`s and before the read; lane 0 clears it only after the `SYNC()` that follows the divisor stores, i.e. after every read; the next `atomicOr` is two `SYNC()`s later |
| `Dsh[row * 4 + j]` (rescale divisors) | the lane of the row whose segment is j (segments 0 to 3): one writer per slot, and the lanes of a row hold the same value | `coopMatLoad` of the divisor tiles by every subgroup | `SYNC()` after the stores, `SYNC()` after the loads |
| `Psh` e values, own segment | the one lane that owns (row, seg) | `coopMatLoad` in `av_block` by every subgroup | `SYNC()` before `av_block`, `SYNC()` after it (before the next block's score stores) |
| `Psh[row * P_STRIDE + j]`, final divisors | the lane of the row whose segment is j | `coopMatLoad` of `den` by every subgroup | `SYNC()` after the stores; the last loads of `Psh` are a `SYNC()` earlier |
| `t_output` | one `coopMatStore` per tile by the subgroup that owns that head_dim slice | none in this kernel | |

No slot has two plain writers in a phase; the only slot several lanes write is `Gsh`, atomically and with the
same value. Control flow around every `barrier()` is uniform for the workgroup: `num_blocks` and `s_base` are
per workgroup, the two early returns come before the first barrier, and the rescale branch is taken on the
value of `Gsh` that every lane reads after the same barrier (that is why the vote of the single-subgroup form,
`subgroupAny`, is replaced). The accumulators and the Q tiles are per-subgroup registers and are never shared.
The assumption "the workgroup is exactly G full subgroups of 16": the pipeline is created with required
subgroup size 16 (yaml `SUBGROUP_SIZE`, as for the Xe2 kernels) and the node launches a local size of G x 16;
the release-zone pipeline code does not set the full-subgroups flag, so the kernel checks
`gl_NumSubgroups == G` and `gl_SubgroupSize == 16` and writes NaN rows otherwise (one writer per row). The tiers' mismatch count
would not report them (corrected: "Finding F2"); the `[sdpa-error]` record would, and the gate now requires it
finite. The copy pass `sarc_dev_b580_sdpa_kvt` has no shared memory.
```

## Known defect F1: full-subgroups flag, and decode ratios

Locator: `openspec/changes/sarc-1.5-b580-fused-port/proposal.md`, lines 326-363 (commit `a434a49623600f168089173a964efc79661ac286`)

```text
## Known defect: F1 (owner decision 2026-10-09 15:25 UTC, option C: no release-zone change in this campaign)

The sentences of the Vulkan and GLSL specifications that the multi-subgroup form relies on are quoted in
`STATUS.md` (section "Specification quotes"), from the `vulkan-docs` MCP server as the owner asked. None
contradicts the exchange through shared memory. One requirement is not met, here and in every
cooperative-matrix pipeline of every device, the shipped ones included:

- **The sentence.** "VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10770 Any pipeline containing a shader with
  OpTypeCooperativeMatrixKHR or OpCooperativeMatrix*KHR instructions must be created with the
  VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT flag or the shader module must be version 1.6 or
  greater" (`refpages/latest/RuntimeSpirv.md`).
- **The SPIR-V version.** 1.3 (header `0x00010300`) for both fused shaders of `b580-fused1` and for the parent's
  cooperative-matrix kernels.
- **The code.** `backends/vulkan/runtime/vk_api/Pipeline.cpp` lines 305 and 540: every compute stage is created
  with `flags` `0u` (the required subgroup size is chained in `pNext`). `vk_api/Runtime.cpp:91`: the instance is
  created for `VK_API_VERSION_1_1`, so SPIR-V 1.6 is not available. `vk_api/Device.cpp:317` already reads
  `computeFullSubgroups`.
- **The kernel's run-time check** (`gl_NumSubgroups == G`, `gl_SubgroupSize == 16`, NaN rows otherwise)
  guarantees that whenever the kernel computes, the workgroup is exactly G full subgroups of 16 and the lane
  mapping of the shared-memory table holds. It does not make the pipeline valid, it does not cover the parent's
  and the shipped kernels, and its NaN rows are not counted by the correctness test's mismatch counter (a NaN
  comparison is false); they do make the test's `[sdpa-error]` record non-finite, which `tools/gate_check.py`
  now rejects (`STATUS.md`, "Finding F2"; all 960 records of the five gates are finite).
- **The two forms** for the later change. A: a per-shader yaml parameter carried through `gen_vulkan_spv.py`,
  `vk_api/Shader.{h,cpp}` and `vk_api/Pipeline.{h,cpp}` that sets the stage flag when a required subgroup size is
  in force and the device reports `computeFullSubgroups`; 30 to 40 lines; inert for every shader that does not
  ask. B: set the flag in `Pipeline.cpp` at both places for every pipeline with a required subgroup size on a
  device that reports the feature; about 10 lines; it changes how every such pipeline of every device is
  created (the local size in X must then be a multiple of the required size,
  VUID-VkPipelineShaderStageCreateInfo-pNext-02757).
- **The ruling.** F1 is repaired once, in the release zone, in a change of its own before any promotion pull
  request, with every device gated and timed again under it. Nothing is rebuilt, re-gated or re-timed for it
  here; the numbers above stand as measured.
- **Decode with the fused node present** (not investigated): final / parent 0.98462 / 0.99148 / 0.99150 /
  0.98960 / 0.99830 / 0.99603 (`s4-final`, 32 tokens, medians of 5; 1B 4w, 1B 8da4w, 3B 4w, 3B 8da4w, 8B 4w, 8B
  8da4w) and 0.99396 / 0.99448 / 0.99177 / 0.99621 / 0.99918 / 0.99533 (`s2-c1`), from `decode/decode.csv`:
  0.1 to 1.5 % slower, inside the +-2 % band, below 1 in all
  twelve readings. Decode does not run the fused kernel.
```
