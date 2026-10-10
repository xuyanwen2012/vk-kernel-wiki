---
id: meas-rx7600-fused-attention
title: "Radeon RX 7600: fused attention kernel (fused3) against the three attention kernels, and the subgroup-barrier copy fused3sb (sarc-1.5-rx7600-prefill-refine, candidates 2 and M2a)"
source_category: measurement
architectures: [rx-7600]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, kernel-fusion, cooperative-matrix, subgroup-size, control-barrier, full-subgroups]
device: rx-7600
driver: "RADV Mesa 26.2.3"
measured_at: '2026-10-06'
method: "Records of one tuning campaign, quoted from the pushed branch at the commit given per locator. End-to-end cells: llama_main, one 2048-token prefill per run, prefill tok/s, parent and candidate arms interleaved, median of the valid runs per arm (count stated in the excerpts); six cells = Llama 3.2 1B, Llama 3.2 3B, Llama 3.1 8B in the 4w and 8da4w schemes. Gate: SDPA correctness tiers of test_llama_microbench against a CPU reference, the campaign's verify script, and a next-token comparison between the arms. Device and driver are quoted from the vulkaninfo lines of the session's env.txt. Lines of the cited files that hold a host name, a board address or a storage path are not excerpted. Candidate 2 (fused3, one-pass packed variants) was timed on 2026-10-06 on the parent binary, the fused kernel selected by environment variable; 5 valid runs per arm. Candidate M2a (fused3sb) was gated on 2026-10-08 against candidate 3. The result files of this branch carry placeholders in angle brackets where the campaign scrubbed host and path names."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/proposal.md
    description: "Campaign record: device and driver, candidate table, adoption rule for M2a, trace attribution, negative results"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/c2-fused/env.txt
    description: "Candidate 2 session environment: date, arms, driver, vulkaninfo lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/c2-fused/summary.csv
    description: "Candidate 2 per-cell medians, gain, validity counts and next-token column"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/acceptance-c2.txt
    description: "Acceptance record of candidate 2 under the reference-error rule"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/STATUS.md
    description: "Running log: shared-memory reading of the ported kernels"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/m2a-sgbarrier/gate.status
    description: "M2a gate timeline and environment"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/m2a-sgbarrier/summary.csv
    description: "M2a per-cell medians, fused3 against fused3sb"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/m2a-sgbarrier/sdpa-error/bitwise.txt
    description: "Byte comparison of SDPA outputs, fused3 against fused3sb, per case"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/c2-fused/runs.csv
    description: "Candidate 2 per-run rows behind summary.csv"
  - repo: https://github.com/sarc-acl/executorch
    commit: c4d7451c5da8b37948e3f252968ddd9b08de353b
    locator: openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/m2a-sgbarrier/sdpa-correctness/summary.txt
    description: "M2a SDPA tier passes"
captured_at: '2026-10-10'
commit: f5f1bf10c510da347a556f716c2c9025a85d6228
baseline: "Candidate 2: candidate 1 (parent commit with the r3 softmax), the cooperative-matrix QK^T and attn*V kernels and the softmax as three dispatches. M2a: candidate 3 with the fused3 pair."
---

## Device, driver and campaign scope

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/proposal.md`, lines 3-6 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
Second-layer prefill tuning of the Radeon RX 7600 (Navi33, gfx1102, RADV Mesa 26.2.3 user-space build), the
780M's position (`CAMPAIGN.md`, owner decision N1): port the 780M's second-layer results, gate each, stop when
two consecutive gated candidates gain under 2 %. Dev zone only. Branch `topic/rx7600-prefill-refine`, forked
from `origin/topic/780m-prefill-refine` at `f5f1bf10c` (the parent).
```

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/c2-fused/env.txt`, line 1 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
Tue Oct  6 01:24:38 PM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/c2-fused/env.txt`, lines 16-20 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
session c2-fused staged 2026-10-06T13:22:47Z
parent = build/rx7600/parent env [ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_780M_PROFILE=c7] commit f5f1bf10c510da347a556f716c2c9025a85d6228
cand   = build/rx7600/parent env [ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_780M_PROFILE=c7 ET_VK_SARC_780M_SDPA_FUSED=fused3_d64_t32x32g11s32rko,fused3_d128_t16x64g11s32rko] commit f5f1bf10c510da347a556f716c2c9025a85d6228
driver = <mesa>/share/vulkan/icd.d/radeon_icd.x86_64.json (Mesa 26.2.3 31e9a6b2e9)
candidate 2: fused attention kernel (780M fused3, fused3_d64_t32x32g11s32rko,fused3_d128_t16x64g11s32rko) on top of candidate 1, parent binary
```

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/c2-fused/env.txt`, lines 27-30 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
	apiVersion         = 1.4.354
	deviceName         = AMD Radeon RX 7600 (RADV NAVI33)
	driverName         = radv
	driverInfo         = Mesa 26.2.3 (git-31e9a6b2e9)
```

## Candidate 2 (fused3) against candidate 1, per cell

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/c2-fused/summary.csv`, lines 1-8 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
model,scheme,parent_med_tok_s,cand_med_tok_s,ratio,gain_pct,outside_2pct_band,parent_spread_pct,cand_spread_pct,valid_parent,valid_cand,invalid,clk_med_mhz_range,temp_pre_range,next_token_2048/real/check
1b,4w,8031.37,10395.90,1.2944,+29.44,yes,0.39,0.51,5,5,-,2541-2557,42-46,SAME/SAME/SAME
1b,8da4w,7529.41,9481.48,1.2593,+25.93,yes,0.74,3.17,5,5,-,2564-2592,48-50,SAME/SAME/SAME
3b,4w,3340.95,3930.90,1.1766,+17.66,yes,0.16,0.19,5,5,-,2513-2533,50-54,SAME/SAME/SAME
3b,8da4w,3117.20,3592.98,1.1526,+15.26,yes,0.46,1.24,5,5,-,2552-2573,52-54,SAME/SAME/SAME
8b,4w,1532.93,1723.91,1.1246,+12.46,yes,0.07,0.08,5,5,-,2498-2527,52-54,SAME/SAME/SAME
8b,8da4w,1416.32,1555.05,1.0980,+9.80,yes,0.14,0.23,5,5,-,2552-2569,52-54,SAME/SAME/SAME
geomean over 6 cells: 1.1822 (+18.22 %), min 1.0980, max 1.2944
```

## Candidate 2 acceptance record

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/acceptance-c2.txt`, lines 1-17 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
ACCEPTED (reference-error rule, owner decision 2026-10-04)

Candidate 2: fused attention kernel (`fused3_d64_t32x32g11s32rko`, `fused3_d128_t16x64g11s32rko`) on top of candidate 1.
Timed session `c2-fused`: geomean +18.22 % over candidate 1 (results/rx7600/sessions/c2-fused).

Evidence (all in this directory, paths relative to results/rx7600/):
- D3.1 error against the fp64 reference, one coherent run: sdpa-error/error.csv (17 rows, complete), sdpa-error/README.md,
  sdpa-error/runs.txt, sdpa-error/bitwise.txt, raw logs sdpa-error/logs/. Production shapes (tier full, S = 2048):
  4 of 4 "yes". One non-production row reads NO (peaked_tiny_gqa_s256, S = 256, max ratio 1.140, rms ratio 0.812),
  explained in sdpa-error/README.md; it is not counted as a pass.
- D3.2 real-text probe: probe/comparison.csv (18 rows, 32 prompts per cell).
- D3.3 gross-divergence check: largest top-1 difference 4 of 32 prompts (limit one third), largest mean KL 0.0345 nat
  (limit 0.5): passed.
- Attention tiers extended and full: sdpa-correctness/ (12 passes each, 0 mismatches, pairing=ok).
- verify.sh identical to the parent snapshot s0-parent-verify (rates removed), 32 of 32 lines.

Next-token items that differ: none (timed, real-text and unaligned prompts all SAME in the six cells).
```

## Candidate table and trace attribution

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/proposal.md`, lines 96-102 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
| # | candidate | parent | geomean | state | evidence |
|---|---|---|---:|---|---|
| 1 | softmax `r3` (the 780M's; `ET_VK_SARC_780M_PROFILE=c7`) | pristine parent | +1.48 % | gated, bit-identical to the release softmax in 21 of 21 SDPA cases | `sessions/c1-softmax` |
| 2 | fused attention kernel `fused3` (D4.3 hook, owner review before promotion) | 1 | +18.22 % | **ACCEPTED (reference-error rule, owner decision 2026-10-04)**; next token SAME everywhere | `sessions/c2-fused`, `sdpa-error/`, `probe/`, `acceptance-c2.txt` |
| 3 | linear kernel per layer shape (`rx7600-refine2`, real build `c3`) | 2 | +5.49 % | gated; outputs byte-identical in 24 of 24 linear shapes (no arithmetic change) | `screens/`, `sessions/c3-linear` |
| 4 | whole-texel 8da4w staging everywhere (`rx7600-refine3`, build `c4`) | 3 | -0.15 % | gated, **not adopted** (8B 8da4w -1.51 %) | `sessions/c4-texel` |
| M2a | `fused3sb`: `subgroupBarrier()` after every `memoryBarrierShared()` | 3 | +0.00 % | gated, output byte-identical to `fused3`, adopted under the rule above | `sessions/m2a-sgbarrier` |
```

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/proposal.md`, lines 122-124 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
Where each gain came from (warm ETDump, 8B 8da4w, ms per 2048-token prefill, final session: `sessions/final/trace-families.csv`, `trace-totals.csv`):
total dispatch time 1447.0 (pristine parent) -> 1162.1 (final). Attention: QK^T 72.4 + softmax 64.6 + attn x V 55.1 = 192.2 ms -> the one-pass fused
kernel with its K / V copy pass 46.7 ms (candidate 2; the softmax `r3` alone, candidate 1, took the softmax from 64.2 to 53.1 ms in the `c1-softmax` trace).
```

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/proposal.md`, lines 128-129 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
Negative results: whole-texel staging on every shape (-0.15 %); the 780M's fused-variant alternatives (no variant >= 3 % faster in every round,
`results/rx7600/fused/`); 4w kernels: only 6 of 12 shapes pass the 3 % rule and give +0.5 to +1.5 % per cell.
```

## Shared-memory reading of the ported kernels

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/STATUS.md`, lines 69-79 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
Shared memory of the ported kernels, read before the gate (R7): `r3` (softmax): every worker writes only its own
slot of `shared_max` / `shared_exp_sum`, every cross-worker read follows `barrier()`; clean. `kvt` (copy pass): no
shared memory. `fused3`: no two invocations write the same shared location (each lane writes its own (row,
segment) slots of `Psh`, `Rsh`, `Dsh`; the stores of whole tiles are cooperative); but a lane reads slots that other
lanes of the same subgroup wrote, ordered only by `memoryBarrierShared()`, without `subgroupBarrier()`. The
workgroup is one subgroup and the code relies on it executing in lockstep. Under the Vulkan memory model that is
formally unsynchronised; on RDNA3 (one wave, no divergent branch between the write and the read) it is benign, and
every correctness pass agrees. The 780M uses the same kernel. Adding `subgroupBarrier()` after each
`memoryBarrierShared()` would make it formally correct; per the owner decision of 2026-10-07 23:08 UTC it is done as its
own gated candidate (M2a) in a copy of the kernel, `sarc_dev_780m_sdpa_fused3sb`, after candidates 3 and 4, not by editing the 780M's file. The copy keeps the 780M's name prefix (it does not carry the device tag R3 asks for) because `Sdpa780mFused.cpp` builds the shader name as `sarc_dev_780m_sdpa_` + variant; see "Decision needed from the owner", item 3.
The wave size RADV picks for a 32-invocation workgroup (the yaml sets no required subgroup size) is UNVERIFIED.
```

## M2a (fused3sb): adoption rule, gate timeline, per cell, byte comparison

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/proposal.md`, lines 39-45 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
- **M2a** (`fused3sb`: `subgroupBarrier()` after every `memoryBarrierShared()` in the fused kernel; its own gated candidate by
  the owner decision of 2026-10-07 23:08 UTC, reported either way): it is a correctness-hygiene change (an execution
  barrier where the 780M kernel relies on lockstep), not a speed-up. It enters the final stack if (a) the gate passes (SDPA tiers
  all / extended / full, 12 passes each, 0 mismatches, `pairing=ok`; `verify.sh` as the snapshot; next token SAME) and its
  output is byte-identical to `fused3` in the SDPA evidence (else D3, error against the fp32 reference not larger) and (b)
  its geomean change over candidate 3 is not worse than -2 % (inside the noise band or better). Otherwise it stays out and
  the stack keeps `fused3` with the formal-race finding recorded.
```

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/m2a-sgbarrier/gate.status`, lines 1-6 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
2026-10-08T04:36:14Z gate start reps=5 sdpa=sdpa env=[ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_780M_PROFILE=c7 ET_VK_SARC_780M_SDPA_FUSED=fused3sb_d64_t32x32g11s32rko,fused3sb_d128_t16x64g11s32rko ET_VK_SARC_RX7600_PROFILE=rx7600-refine2]
2026-10-08T05:18:03Z timed session done
2026-10-08T07:05:54Z sdpa tiers done
2026-10-08T07:15:20Z verify done: VERIFY_COMPARE: DIFFERS (32 / 32 lines, 2 differ)
2026-10-08T07:17:41Z trace done
2026-10-08T07:17:41Z GATE_DONE
```

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/m2a-sgbarrier/summary.csv`, lines 1-8 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
model,scheme,parent_med_tok_s,cand_med_tok_s,ratio,gain_pct,outside_2pct_band,parent_spread_pct,cand_spread_pct,valid_parent,valid_cand,invalid,clk_med_mhz_range,temp_pre_range,next_token_2048/real/check
1b,4w,10449.00,10449.00,1.0000,+0.00,no,4.43,1.02,5,5,-,2532-2559,46-48,SAME/SAME/SAME
1b,8da4w,10291.50,10291.50,1.0000,+0.00,no,0.50,0.50,5,5,-,2532-2536,50-52,SAME/SAME/SAME
3b,4w,3976.70,3976.70,1.0000,+0.00,no,0.19,0.39,5,5,-,2502-2507,52-52,SAME/SAME/SAME
3b,8da4w,3953.67,3946.05,0.9981,-0.19,no,0.19,0.19,5,5,-,2522-2528,52-54,SAME/SAME/SAME
8b,4w,1750.43,1750.43,1.0000,+0.00,no,0.26,0.43,5,5,-,2493-2498,52-52,SAME/SAME/SAME
8b,8da4w,1737.07,1740.02,1.0017,+0.17,no,0.26,0.34,5,5,-,2519-2525,52-54,SAME/SAME/SAME
geomean over 6 cells: 1.0000 (-0.00 %), min 0.9981, max 1.0017
```

Locator: `openspec/changes/sarc-1.5-rx7600-prefill-refine/results/rx7600/sessions/m2a-sgbarrier/sdpa-error/bitwise.txt`, lines 1-21 (commit `c4d7451c5da8b37948e3f252968ddd9b08de353b`)

```text
all sdpa_1b_head_config.bin IDENTICAL
all sdpa_1b_head_config_s256.bin IDENTICAL
all sdpa_tiny_gqa.bin IDENTICAL
all sdpa_tiny_gqa_s256.bin IDENTICAL
extended sdpa_1b_head_config_s256_pos256.bin IDENTICAL
extended sdpa_3b_head_config_pos128.bin IDENTICAL
extended sdpa_3b_head_config_s256.bin IDENTICAL
extended sdpa_8b_head_config_s256.bin IDENTICAL
extended sdpa_tiny_d128_s2048.bin IDENTICAL
extended sdpa_tiny_gqa_pos64.bin IDENTICAL
extended sdpa_tiny_gqa_s2048.bin IDENTICAL
extended sdpa_tiny_gqa_s256_pos128.bin IDENTICAL
peaked sdpa_peaked_1b_head_config_s256_pos256.bin IDENTICAL
peaked sdpa_peaked_8b_head_config_s256.bin IDENTICAL
peaked sdpa_peaked_tiny_d128_s2048.bin IDENTICAL
peaked sdpa_peaked_tiny_gqa_s2048.bin IDENTICAL
peaked sdpa_peaked_tiny_gqa_s256.bin IDENTICAL
full sdpa_1b_head_config_s2048.bin IDENTICAL
full sdpa_3b_head_config_s2048.bin IDENTICAL
full sdpa_8b_head_config_s1024_pos1024.bin IDENTICAL
full sdpa_8b_head_config_s2048.bin IDENTICAL
```
