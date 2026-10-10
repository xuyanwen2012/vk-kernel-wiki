---
id: meas-780m-fused-attention
title: "Radeon 780M: fused attention kernel (fused3, one-pass form, fused3sb subgroup barriers), gains over the parent and gate outcomes (sarc-1.5-780m-prefill-refine, rounds 2 and 3)"
source_category: measurement
architectures: [radeon-780m]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, kernel-fusion, cooperative-matrix, subgroup-size, control-barrier, full-subgroups]
device: radeon-780m
driver: "RADV Mesa 25.2.7"
measured_at: '2026-10-05'
method: "Records of one tuning campaign, quoted from the pushed branch at the commit given per locator. End-to-end cells: llama_main, one 2048-token prefill per run, prefill tok/s, parent and candidate arms interleaved, median of the valid runs per arm (count stated in the excerpts); six cells = Llama 3.2 1B, Llama 3.2 3B, Llama 3.1 8B in the 4w and 8da4w schemes. Gate: SDPA correctness tiers of test_llama_microbench against a CPU reference, the campaign's verify script, and a next-token comparison between the arms. Device and driver are quoted from the vulkaninfo lines of the session's env.txt. Lines of the cited files that hold a host name, a board address or a storage path are not excerpted. Candidate 8 (the fused kernel, two-pass packed form) was timed on 2026-10-05 against candidate 7, both arms the same binary at commit 77cb45c06b99f4bc072277ea29d4a0fdce9827d4 with two then-local hook patches; 5 valid runs per arm. Round 3 (fused3 against fused3sb, same binary, build of commit c639d47605ca1f2b5314e4b6afc6a58752386796 exported from git objects) ran 2026-10-08 to 2026-10-09; its numbers are the monitored sessions recomputed under the throttle-bit rule quoted below. The page-level commit is the round-3 build."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: 71b43d903d8be69b351c3a5538c86ca473cba00c
    locator: openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/c8-fused3/env.txt
    description: "Candidate 8 session environment: date, arms and commits, vulkaninfo device and driver lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: 71b43d903d8be69b351c3a5538c86ca473cba00c
    locator: openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/c8-fused3/summary.csv
    description: "Candidate 8 per-cell medians, gain, validity counts and next-token columns"
  - repo: https://github.com/sarc-acl/executorch
    commit: 71b43d903d8be69b351c3a5538c86ca473cba00c
    locator: openspec/changes/sarc-1.5-780m-prefill-refine/proposal.md
    description: "Campaign record: round 2 candidate table, where the gains come from, round 3 (fused3sb) reasoning, gate and sessions"
  - repo: https://github.com/sarc-acl/executorch
    commit: 71b43d903d8be69b351c3a5538c86ca473cba00c
    locator: openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/r3a-fused3sb-head4-r6/env.txt
    description: "Round 3 item A monitored session environment: date, vulkaninfo device and driver lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: 71b43d903d8be69b351c3a5538c86ca473cba00c
    locator: openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/r3a-fused3sb-head4-r6/analysis.txt
    description: "Round 3 item A: per-cell medians of fused3 against fused3sb under the ruled throttle mask"
  - repo: https://github.com/sarc-acl/executorch
    commit: 71b43d903d8be69b351c3a5538c86ca473cba00c
    locator: openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/c8-fused3/runs.csv
    description: "Candidate 8 per-run rows behind summary.csv"
  - repo: https://github.com/sarc-acl/executorch
    commit: 71b43d903d8be69b351c3a5538c86ca473cba00c
    locator: openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/round3/shader-diff-fused3-fused3sb.txt
    description: "Text diff of the fused3 and fused3sb shader sources"
  - repo: https://github.com/sarc-acl/executorch
    commit: 71b43d903d8be69b351c3a5538c86ca473cba00c
    locator: openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/round3/head4/bitwise/bitwise-fused3sb.txt
    description: "Byte comparison of SDPA outputs, fused3 against fused3sb"
captured_at: '2026-10-10'
commit: c639d47605ca1f2b5314e4b6afc6a58752386796
baseline: "Candidate 8: candidate 7 (profile 780m-refine3 with softmax r3), the three separate attention kernels. Round 3 item A: candidate 11 with the fused3 pair."
---

## Candidate 8 session: date, arms, device and driver

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/c8-fused3/env.txt`, line 1 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
Mon Oct  5 04:59:02 AM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/c8-fused3/env.txt`, lines 16-19 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
session c8-fused3 staged 2026-10-05T04:10:25Z
parent = build/fused5 env [ET_VK_SARC_DEV_PROFILE=780m-refine3 ET_VK_SARC_780M_SOFTMAX=r3] commit 77cb45c06b99f4bc072277ea29d4a0fdce9827d4
cand   = build/fused5 env [ET_VK_SARC_DEV_PROFILE=780m-refine3 ET_VK_SARC_780M_SOFTMAX=r3 ET_VK_SARC_780M_SDPA_FUSED=fused3_d64_t32x32g11s32rk,fused3_d128_t16x64g11s32rk] commit 77cb45c06b99f4bc072277ea29d4a0fdce9827d4
candidate 8: fused prefill SDPA kernel (sarc_dev_780m_sdpa_fused3, tile-packed K/V copies) through hooks/sdpa-fused-hook.patch in a scratch tree; both arms are the same binary (HEAD 77cb45c06 + working tree + both hook patches); the parent arm is candidate 7 (780m-refine3 + softmax r3)
```

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/c8-fused3/env.txt`, lines 23-26 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
	apiVersion         = 1.4.318
	deviceName         = AMD Radeon 780M Graphics (RADV PHOENIX)
	driverName         = radv
	driverInfo         = Mesa 25.2.7
```

## Candidate 8 (fused kernel) against candidate 7, per cell

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/c8-fused3/summary.csv`, lines 1-8 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
model,scheme,parent_med_tok_s,cand_med_tok_s,ratio,gain_pct,outside_2pct_band,parent_spread_pct,cand_spread_pct,valid_parent,valid_cand,invalid,clk_med_mhz_range,temp_pre_range,next_token_2048/check
1b,4w,3020.65,3624.78,1.2000,+20.00,yes,0.15,0.18,5,5,-,2800-2800,44-48,SAME/SAME
1b,8da4w,3011.76,3618.37,1.2014,+20.14,yes,0.15,0.18,5,5,-,2800-2800,49-50,SAME/SAME
3b,4w,1232.25,1376.34,1.1169,+11.69,yes,0.06,0.20,5,5,-,2799-2800,49-49,SAME/SAME
3b,8da4w,1201.88,1344.71,1.1188,+11.88,yes,1.24,0.79,5,5,-,2800-2800,49-49,SAME/SAME
8b,4w,556.07,601.12,1.0810,+8.10,yes,0.46,0.59,5,5,-,2783-2800,49-49,SAME/SAME
8b,8da4w,561.71,605.74,1.0784,+7.84,yes,0.19,0.21,5,5,-,2800-2800,49-49,DIFFER/SAME
geomean over 6 cells: 1.1316 (+13.16 %), min 1.0784, max 1.2014
```

## Round 2 candidate table (candidates 7 to 11) and gate column

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/proposal.md`, lines 265-279 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
### Candidates

Each against its parent in the same session, median of 5 valid runs per arm, arms interleaved, cool start:

| candidate | what | 1B 4w / 8da4w | 3B 4w / 8da4w | 8B 4w / 8da4w | geomean | gate |
|---|---|---|---|---|---:|---|
| 7 | softmax r3: the row prefix loaded once, exp once, zero fill bounded to what attn*V reads (`ET_VK_SARC_780M_SOFTMAX=r3`; `hooks/softmax-name-hook.patch`) | **+6.78** / **+6.62** % | **+3.43** / **+3.06** % | **+2.44** / **+2.39** % | +4.10 % | pass; SDPA output byte-identical to the parent on 21 cases |
| 8 | fused SDPA kernel `sarc_dev_780m_sdpa_fused3` (`ET_VK_SARC_780M_SDPA_FUSED`; `hooks/sdpa-fused-hook.patch`) | **+20.00** / **+20.14** % | **+11.69** / **+11.88** % | **+8.10** / **+7.84** % | +13.16 % | ACCEPTED (reference-error rule, owner decision 2026-10-04); one next-token item differs (8B 8da4w, `prompt_2048.txt`) |
| 9 | candidate 8 + one-pass form of the fused kernel + the 4w kernel per shape (`ET_VK_SARC_780M_PROFILE=refine9`) | **+4.83** / +1.80 % | **+4.50** / +1.06 % | **+5.45** / +1.59 % | +3.19 % | pass; no next-token item differs; 4w output byte-identical; the 8da4w cells are inside the band |
| 10 | candidate 9 with the refined 4w table (`refine10`: two more refinement rounds and a geometry scan) | +0.94 / 0.00 % | +1.43 / -0.73 % | +1.16 / +0.06 % | +0.47 % | pass; inside the band, not a gain; 4w output byte-identical |
| 11 | candidate 10 + the 8da4w kernel per shape (`ET_VK_SARC_780M_PROFILE=c11`; all 2,238 surviving 8da4w configurations screened) | 0.00 / **+2.02** % | 0.00 / **+2.82** % | +0.06 / **+2.36** % | +1.20 % | pass; no next-token item differs; second consecutive candidate under 2 %: stop rule met |

Bold = outside the +-2 % band. A/A floor of this round: geomean +0.01 %, cells within +-0.23 % (`t3-aa`).
Candidates 7 to 9 were measured through two local patches; since the owner decision of 2026-10-05 the entry
points are committed and every candidate is one profile of the committed branch (`c7` to `c11`).
```

## Where the gain comes from: fused kernel and its one-pass form

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/proposal.md`, lines 319-330 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
- **Fused SDPA (candidate 8).** QK^T, softmax and attn*V each move the S x S attention matrix through memory
  (about 550 MB a layer on 1B). The fused kernel never writes it: per 16 or 32 query rows of a head it walks the
  context in blocks, computes the scores, exponentiates them in shared memory private to one subgroup and
  accumulates e V in fp32. Traces: QK^T + softmax + attn*V 158.9 / 296.2 / 449.4 ms are replaced by the copy pass
  + fused kernel at 45.3 / 120.7 / 184.2 ms. Kernel time per layer at a steady clock: 9.96 -> 2.82 ms (1B),
  10.24 -> 4.32 ms (3B), 13.51 -> 5.54 ms (8B). What made it fast, in the order found (roofline fed-MMA table and
  the disassembly, `STATUS.md`): no shared staging and no barrier (one subgroup per workgroup); Q tiles kept in
  registers; K and V read from tile-packed copies in which a 16 x 16 operand tile is 512 contiguous bytes
  (head_dim 128: 9.95 -> 4.96 ms from that alone). It runs at about 71 % of the fp16 -> fp32 matrix roof.
- **One-pass fused kernel (candidate 9).** A running row maximum with rescaled accumulators instead of a first
  pass over the scores: 2.82 -> 2.26 ms (1B), 4.31 -> 3.22 ms (3B), 5.54 -> 4.05 ms (8B) per layer; -10 / -31 /
  -48 ms in the traces. Alone it is +1.1 to +1.8 % end to end, inside the band.
```

## Round 3: the record's section on the subgroup barriers (fused3sb)

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/proposal.md`, lines 702-704 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
**The recommended configuration is now `ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_DEV_PROFILE=780m-final`.** It
dispatches what candidate 11 dispatched, with the `fused3sb` pair in place of the `fused3` pair.
`ET_VK_SARC_DEV_PROFILE=780m-refine3 ET_VK_SARC_780M_PROFILE=c11` still works and selects the same kernels.
```

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/proposal.md`, lines 766-787 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
### Why the barriers

`fused3` runs one subgroup per workgroup and keeps its scores, e values, row maxima, row sums and rescale
divisors in shared memory. No two invocations write the same location (read again on 2026-10-08: a lane writes
only its own `Psh[e_idx + i]`, `Rsh[e_row * SEGS + e_seg]`, and the `Dsh` / `Psh` divisor slots `j` of its row
with `j mod SEGS = e_seg`), but a lane reads what other lanes of its subgroup wrote: the scores a subgroup-wide
`coopMatStore` put into `Psh`, the other segment's `Rsh` slot (16-row variants, two lanes per row), and the
`coopMatLoad`s of e, of the divisor tile and of the row sums. Those reads were ordered against the writes by
`memoryBarrierShared()` alone.

- Why that is a race under the Vulkan memory model: a memory barrier orders the memory accesses of the
  invocation that executes it; it makes no invocation wait for another. Only a control barrier does that
  (`barrier()` for the workgroup, `subgroupBarrier()` for the subgroup). Without one, the invocations of a
  workgroup have no defined order relative to each other, so nothing says that lane A's store has executed when
  lane B executes its load: formally an unsynchronised read, whatever the values.
- Why RDNA3 tolerated it: the workgroup is one subgroup and the subgroup is one 32-lane wave, which executes
  each instruction for all its lanes before the next one; and every barrier sits in subgroup-uniform control
  flow (the loop counts depend on the workgroup, the one data-dependent branch is taken on `subgroupAny`). So on
  this hardware every lane's store has run before any lane's load. That is how a wave executes, not something
  the API promises, and it does not hold on a device whose subgroup is smaller than the workgroup or whose
  compiler may move a load across the memory barrier. It is the class of defect of lesson L8, found by reading
  before it failed.
```

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/proposal.md`, lines 800-804 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
The copy differs from `fused3` in the header comment (8 lines) and in 13 inserted `subgroupBarrier();` lines,
one after each `memoryBarrierShared();`, nothing else (`results/780m/round3/shader-diff-fused3-fused3sb.txt`;
every line is listed in `STATUS.md`). The task file and the commit message speak of 14 calls: the kernel has 13;
the fourteenth match of a text search is the sentence in the new header. The yaml lists the two variants of the
final pair with the parameters of their `fused3` twins.
```

## Round 3 item A: gate with fused3sb

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/proposal.md`, lines 884-904 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
Item A on `head4` (`r3a-fused3sb-head4`, started 2026-10-08 23:35 UTC at 43 C), same binary in both arms:

| cell | `c11` with `fused3` | `c11` with `fused3sb` | difference | repeat spread parent / candidate | next token (`prompt_2048` / `prompt_check` / `r1304`) |
|---|---:|---:|---:|---|---|
| 1B 4w | 3842.40 | 3835.21 | -0.19 % | 0.19 / 0.19 % | SAME / SAME / SAME |
| 1B 8da4w | 3764.71 | 3764.71 | 0.00 % | 0.18 / 0.18 % | SAME / SAME / SAME |
| 3B 4w | 1458.69 | 1458.69 | 0.00 % | 0.07 / 0.14 % | SAME / SAME / SAME |
| 3B 8da4w | 1422.22 | 1416.32 | -0.41 % | 0.48 / 0.49 % | SAME / SAME / SAME |
| 8B 4w | 640.60 | 640.60 | 0.00 % | 0.53 / 0.44 % | SAME / SAME / SAME |
| 8B 8da4w | 628.99 | 628.22 | -0.12 % | 0.21 / 0.25 % | SAME / SAME / SAME |
| geomean | | | **-0.12 %** | | |

Inside the band: no gain and no cost that this measurement resolves. Gate with the candidate's environment on
the timed binary: unmodified `verify.sh` rc = 0 (12 of 12 production-diff ALL PASSED, default vs tiled SAME,
decode 31 tokens; against the parent snapshot only the two linear kernel-name lines differ, as for candidate
11); tiers `all` / `extended` / `full` at 12 passes: 192 cases, 0 failed, 0 mismatches, `pairing=ok` in every
line, only the `fused3sb` pair dispatched; SDPA output byte-identical to `fused3` in 21 of 21 cases and in the 5
of tier `fused`, and identical to the dumps of `head3`; error against the fp64 reference equal in both arms.
Fused kernel time at a steady clock: 2.266 -> 2.268 ms a layer (1B), 3.221 -> 3.214 (3B), 4.051 -> 4.062 (8B);
+0.07 / -0.21 / +0.25 %. Warm traces (candidate second, no cooling between): copy / view / other -1.2 to
+2.2 %, linear GEMM +1.2 to +2.0 %.
```

## Round 3: monitored timed sessions, fused3 against fused3sb

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/r3a-fused3sb-head4-r6/env.txt`, line 1 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
Fri Oct  9 03:28:20 AM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/r3a-fused3sb-head4-r6/env.txt`, lines 23-26 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
	apiVersion         = 1.4.318
	deviceName         = AMD Radeon 780M Graphics (RADV PHOENIX)
	driverName         = radv
	driverInfo         = Mesa 25.2.7
```

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/proposal.md`, lines 806-833 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
### Monitored timed sessions on `head4` (owner decisions 2026-10-09 02:50 and 04:55 UTC): the round's numbers

The earlier `head4` sessions (item A -0.12 %, item B +33.92 %) did not record two predicates of the R6 validity
rule: GPU workload during a run, and a thermal throttle reason. The owner ordered them replaced by sessions on
the same binaries with `tools/e2e5.sh` also recording `throttle_status` of `gpu_metrics` in its 0.1 s sampler,
the guard's processes and the DRM clients readable to this user during each run (a foreign one with engine
time: invalid), a clock-sample minimum of 5, and `nvtop` in the guard's pattern. The gate, the tiers and the
byte comparison were not repeated.

The sessions (2026-10-09 03:28 to 04:40 UTC) first ran under "any non-zero status rejects" and came out
incomplete: `throttle_status` reads `0x00000002` in at least one window sample of 113 of 186 timed runs (every
8B run of item A), and nothing else was found. Asked, the owner ruled (04:55 UTC): on this APU the thermal
reasons are bits 4, 5, 6 (`THM_CORE`, `THM_GFX`, `THM_SOC`) and 9, 10 (`PROCHOT`); bits 0 to 3 (package power
limits; bit 1 is `FPPT`) and 7, 8, 11, 12 (current limits) are recorded and do not reject; any bit above 12
rejects. This is lesson L16: a power-limit flag that a loaded APU sets by design. The sessions were recomputed
under that rule from the recorded rows, no new run: 94 of 94 and 92 of 92 timed rows valid, medians of the first
5 per arm per cell (`results/780m/sessions/{r3a-fused3sb-head4-r6,r3b-final-dev15-head4-r6}/`, `runs-ruled.csv`,
`analysis.txt`; `tools/r6_analyze.py`).

| cell | A: `c11` with `fused3` | A: `c11` with `fused3sb` | A: difference | B: `dev/1.5` dispatch | B: `780m-final` | B: gain | round 2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1B 4w | 3835.21 | 3835.21 | 0.00 % | 2694.74 | 3835.21 | +42.32 % | +42.51 % |
| 1B 8da4w | 3764.71 | 3764.71 | 0.00 % | 2537.79 | 3757.80 | +48.07 % | +48.35 % |
| 3B 4w | 1457.65 | 1457.65 | 0.00 % | 1141.58 | 1457.65 | +27.69 % | +27.85 % |
| 3B 8da4w | 1412.41 | 1398.91 | -0.96 % | 1047.57 | 1414.36 | +35.01 % | +33.72 % |
| 8B 4w | 639.00 | 640.00 | +0.16 % | 519.53 | 639.00 | +23.00 % | +23.42 % |
| 8B 8da4w | 628.80 | 628.61 | -0.03 % | 487.16 | 628.41 | +29.00 % | +28.73 % |
| geomean | | | **-0.14 %** | | | **+33.90 %** | +33.82 % |
```

Locator: `openspec/changes/sarc-1.5-780m-prefill-refine/results/780m/sessions/r3a-fused3sb-head4-r6/analysis.txt`, lines 7-15 (commit `71b43d903d8be69b351c3a5538c86ca473cba00c`)

```text
## medians of the first 5 valid rows per arm per cell
cell,parent_med,cand_med,gain_pct,parent_spread_pct,cand_spread_pct,valid/rows parent,valid/rows cand,rows used with a recorded bit parent,cand,window samples with bit 1 parent,cand
1b 4w,3835.21,3835.21,+0.000000,0.19,0.19,8/8,8/8,0/5,3/5,0/40,3/40
1b 8da4w,3764.71,3764.71,+0.000000,0.37,0.37,7/7,7/7,0/5,2/5,0/35,2/35
3b 4w,1457.65,1457.65,+0.000000,0.07,0.14,8/8,8/8,3/5,2/5,7/104,4/106
3b 8da4w,1412.41,1398.91,-0.955813,1.03,0.97,8/8,8/8,2/5,3/5,3/112,4/112
8b 4w,639.002,640,+0.156181,0.34,0.34,8/8,8/8,5/5,5/5,77/240,80/240
8b 8da4w,628.8,628.607,-0.030693,0.18,0.25,8/8,8/8,5/5,5/5,48/248,47/247
geomean over 6 cells: -0.139078 %
```
