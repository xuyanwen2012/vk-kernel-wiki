---
id: meas-7900xtx-fused-attention
title: "Radeon RX 7900 XTX on AMDVLK: fused attention kernel (fused3sb, two-pass variants) rejected on performance against the three cooperative-matrix attention kernels (sarc-1.5-7900xtx-prefill-refine, candidate 2)"
source_category: measurement
architectures: [rx-7900-xtx]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, kernel-fusion, cooperative-matrix, subgroup-size, control-barrier, full-subgroups, shared-memory-limit]
device: rx-7900-xtx
driver: "AMDVLK 2025.Q2.1"
measured_at: '2026-10-08'
method: "Records of one tuning campaign, quoted from the pushed branch at the commit given per locator. End-to-end cells: llama_main, one 2048-token prefill per run, prefill tok/s, parent and candidate arms interleaved, median of the valid runs per arm (count stated in the excerpts); six cells = Llama 3.2 1B, Llama 3.2 3B, Llama 3.1 8B in the 4w and 8da4w schemes. Gate: SDPA correctness tiers of test_llama_microbench against a CPU reference, the campaign's verify script, and a next-token comparison between the arms. Device and driver are quoted from the vulkaninfo lines of the session's env.txt. Lines of the cited files that hold a host name, a board address or a storage path are not excerpted. Fused-variant screen: test_llama_microbench --sdpa, 3 rounds, fused kernel plus copy pass at S = 2048. Candidate 2 was timed on 2026-10-08 against candidate 1, 7 valid runs per arm; its gate was stopped by the actor after the timed session. The candidate build commit named in env.txt (86a7f96c80243236dd7dbdf5f79205b96af6535f) is not reachable from the pushed branch, so no page-level commit is given. The result files carry placeholders in angle brackets where the campaign scrubbed host and path names."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/proposal.md
    description: "Campaign record: device and driver, candidate table, per-cell and trace figures of candidate 2, negative results, shared-memory finding"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/raw/env.txt
    description: "Candidate 2 session environment: date, arms, driver, vulkaninfo lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/fused/README.md
    description: "Fused-variant screen: method, rule and result"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/fused/pick-analysis.txt
    description: "Fused-variant screen: per-variant ratios against the incumbent and median kernel time"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/raw/summary.csv
    description: "Candidate 2 per-cell medians, gain, validity counts and next-token column"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/gate.status
    description: "Candidate 2 gate timeline, stopped after the timed session"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/sdpa-correctness/summary.txt
    description: "SDPA tier passes that ran before the gate was stopped"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/raw/runs.csv
    description: "Candidate 2 per-run rows behind summary.csv"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/trace/families.csv
    description: "Warm ETDump family times of both arms"
  - repo: https://github.com/sarc-acl/executorch
    commit: 82aaec9983f940cf50dfff30b93e8ecece90917d
    locator: openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/fused/fused-screen.csv
    description: "Fused-variant screen rows"
captured_at: '2026-10-10'
baseline: "Candidate 1: parent commit 90fe4d013dd39a6fcf7d68fd5f8038de5324bca3 with the r3 softmax, cooperative-matrix QK^T and attn*V kernels as separate dispatches."
---

## Device, driver and campaign scope

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/proposal.md`, lines 3-5 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
Second-layer prefill tuning of the Radeon RX 7900 XTX (Navi31, gfx1100, AMDVLK 2025.Q2.1 / LLPC), in the 780M's position
(owner decision N1): port the 780M's and the RX 7600's second-layer results, gate each, stop when two consecutive gated
candidates gain under 2 %. Dev zone only. Branch `topic/7900xtx-prefill-refine`, forked from `origin/topic/780m-prefill-refine`
```

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/raw/env.txt`, line 1 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
Thu Oct  8 09:01:31 PM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/raw/env.txt`, lines 16-20 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
session c2-fused staged 2026-10-08T19:56:30Z
parent = build/7900xtx/parent env [ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_780M_PROFILE=c7] commit 90fe4d013dd39a6fcf7d68fd5f8038de5324bca3
cand   = build/7900xtx/c2 env [ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_780M_PROFILE=c7 ET_VK_SARC_780M_SDPA_FUSED=fused3sb_d64_t32x32g11s32rk,fused3sb_d128_t16x64g11s32rk] commit 86a7f96c80243236dd7dbdf5f79205b96af6535f
driver = AMDVLK 2025.Q2.1 (LLPC), VK_ICD_FILENAMES=/etc/vulkan/icd.d/amd_icd64.json (set by env.sh on the GPU host)
candidate 2: fused attention kernel fused3sb (M2a), rk variants picked by the fused-variant screen (stage c1-softmax/fused-screen.csv); parent arm = candidate 1 (parent binary, c7)
```

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/raw/env.txt`, lines 27-30 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
	apiVersion         = 1.4.313
	deviceName         = Radeon RX 7900 XTX
	driverName         = AMD open-source driver
	driverInfo         = 2025.Q2.1 (LLPC)
```

## Fused-variant screen (which form was picked)

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/fused/README.md`, lines 1-8 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
# Fused attention variant screen (2026-10-08 19:47 to 19:50 UTC)

`tools/q-screens.sh` -> `tools/fused_screen.sh`: `test_llama_microbench --sdpa` (`ET_VK_SDPA_PERF_RUNS=20,8`), the parent binary with
`ET_VK_SARC_780M_PROFILE=c7`, 3 rounds, order rotated per round, one `gl.sh` job per (round, pair); total fused kernel + copy pass at S = 2048
per model. Rule (R8): a variant replaces the incumbent (the 780M's `fused3_d64_t32x32g11s32rko`, `fused3_d128_t16x64g11s32rko`) only if it is at
least 3 % faster in every round on every model of its head dimension; among several the fastest median wins (`pick-analysis.txt`, `pick.out`).
Result: `fused3_d64_t32x32g11s32rk` and `fused3_d128_t16x64g11s32rk` (two-pass, tile-packed K / V copies, no online softmax). The online variants
(`rko`) are 1.3 to 2.6 times slower than the two-pass ones on this card with AMDVLK.
```

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/fused/pick-analysis.txt`, lines 1-9 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
d64 fused3_d64_t16x32g11s32rko: vs incumbent per (model, round) 1.112 1.124 1.140; median 2515 us; no
d64 fused3_d64_t32x32g11s32rk: vs incumbent per (model, round) 0.724 0.790 0.767; median 1707 us; QUALIFIES
d64 fused3_d64_t32x32g11s32rko: vs incumbent per (model, round) 1.000 1.000 1.000; median 2236 us; incumbent
d64 fused3_d64_t32x64g11s32rko: vs incumbent per (model, round) 1.315 1.328 1.347; median 2974 us; no
d128 fused3_d128_t16x16g11s32rko: vs incumbent per (model, round) 0.556 0.557 0.558 0.566 0.566 0.566; median 6034 us; QUALIFIES
d128 fused3_d128_t16x32g11s32rko: vs incumbent per (model, round) 0.629 0.636 0.637 0.639 0.639 0.640; median 6830 us; QUALIFIES
d128 fused3_d128_t16x64g11s32rk: vs incumbent per (model, round) 0.384 0.390 0.393 0.373 0.379 0.376; median 4095 us; QUALIFIES
d128 fused3_d128_t16x64g11s32rko: vs incumbent per (model, round) 1.000 1.000 1.000 1.000 1.000 1.000; median 10743 us; incumbent
d128 fused3_d128_t32x32g11s32rko: vs incumbent per (model, round) 0.541 0.555 0.547 0.550 0.548 0.543; median 5884 us; QUALIFIES
```

## Candidate 2 (fused3sb, two-pass variants) against candidate 1, per cell

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/raw/summary.csv`, lines 1-8 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
model,scheme,parent_med_tok_s,cand_med_tok_s,ratio,gain_pct,outside_2pct_band,parent_spread_pct,cand_spread_pct,valid_parent,valid_cand,invalid,clk_med_mhz_range,temp_pre_range,next_token_2048/real/check
1b,4w,20480.00,20480.00,1.0000,+0.00,no,11.37,4.00,7,7,-,2797-2906,44-52,SAME/SAME/SAME
1b,8da4w,22755.60,22755.60,1.0000,+0.00,no,3.37,3.30,7,7,-,2730-2787,50-53,SAME/SAME/SAME
3b,4w,10138.60,7907.34,0.7799,-22.01,yes,7.08,1.53,7,7,-,2778-2998,50-52,SAME/SAME/SAME
3b,8da4w,10449.00,7937.98,0.7597,-24.03,yes,2.59,5.60,7,7,-,2760-2969,52-54,SAME/SAME/SAME
8b,4w,4785.05,4055.45,0.8475,-15.25,yes,2.37,1.19,7,7,-,2814-2988,52-54,SAME/SAME/SAME
8b,8da4w,5019.61,4104.21,0.8176,-18.24,yes,0.98,1.41,7,7,-,2789-2918,52-54,SAME/SAME/SAME
geomean over 6 cells: 0.8621 (-13.79 %), min 0.7597, max 1.0000
```

## Gate timeline and the tier passes that ran

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/gate.status`, lines 1-3 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
2026-10-08T21:01:28Z gate start reps=7 sdpa=sdpa env=[ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_780M_PROFILE=c7 ET_VK_SARC_780M_SDPA_FUSED=fused3sb_d64_t32x32g11s32rk,fused3sb_d128_t16x64g11s32rk]
2026-10-08T22:23:18Z timed session done
2026-10-08T22:25:08Z c2 gate stopped by the actor after the timed session (candidate rejected on performance, see STATUS.md)
```

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/results/7900xtx/sessions/c2-fused/sdpa-correctness/summary.txt`, lines 1-18 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
cand all r1 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r2 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r3 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r4 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r5 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r6 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r7 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r8 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r9 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r10 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r11 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand all r12 rc=0 passed=4 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand extended r1 rc=0 passed=8 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand extended r2 rc=0 passed=8 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand extended r3 rc=0 passed=8 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand extended r4 rc=0 passed=8 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand extended r5 rc=0 passed=8 failed=0 mismatch_nonzero=0 pairing_not_ok=0
cand extended r6 rc=0 passed=8 failed=0 mismatch_nonzero=0 pairing_not_ok=0
```

## Campaign record of candidate 2: state, per cell, trace, what was not run

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/proposal.md`, line 144 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
| 2 | fused attention kernel `fused3sb` (`rk` variants picked by the fused-variant screen; D4.3 hook; build `c2`) | 1 | **-13.79 %** | **rejected on performance**; gate not completed (see below); next token SAME everywhere; the SDPA tiers that ran (all x 12, extended x 6) passed with 0 mismatches | `sessions/c2-fused`, `fused/` |
```

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/proposal.md`, lines 161-167 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
Candidate 2, per cell against candidate 1 (median of 7 valid runs, 0 invalid runs, `sessions/c2-fused/raw/summary.csv`): 1B 4w 20480.00 -> 20480.00 (+0.00 %), 1B 8da4w 22755.60 -> 22755.60 (+0.00 %),
3B 4w 10138.60 -> 7907.34 (-22.01 %), 3B 8da4w 10449.00 -> 7937.98 (-24.03 %), 8B 4w 4785.05 -> 4055.45 (-15.25 %), 8B 8da4w 5019.61 -> 4104.21 (-18.24 %); geomean -13.79 %.
Why (warm ETDump, `sessions/c2-fused/trace/`, ms per 2048-token prefill, attention of candidate 1 = QK^T + softmax + AV against the fused node with its K / V copy pass):
1B 26.3 -> 28.3 (4w), 3B 41.3 -> 109.5, 8B 55.2 -> 152.2. The existing three-kernel coopmat attention costs 1.5 to 1.7 ms per layer on this card; the best fused variant needs 1.7 ms (d64) and 3.7 to 4.5 ms
(d128) per layer. The fused-variant screen (`fused/`) compared the fused variants with each other only and could not show this; on the RX 7600, where the unfused path is slow, the same kernel gained +18 %.
The rest of the gate (SDPA tiers beyond the passes above, `verify.sh`, the reference-error evidence and the real-text probe) was not run for a candidate that loses 13.8 %: it would only
re-check the correctness of a rejected kernel. Nothing of candidate 2 enters the final stack. The attention share left to gain after candidate 1 is small anyway (QK^T + AV about 20 % of the 1B prefill, 9 % of 8B).
```

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/proposal.md`, line 283 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
**Negative results** (all with numbers above): the fused attention kernel `fused3sb` (-13.79 %; the existing three-kernel coopmat attention is 2.6x faster than the best fused variant on 3B / 8B; the kernel itself is correct on AMDVLK: 12 + 6 tier passes, 0 mismatches before its gate was stopped); whole-texel 8da4w staging (-0.42 %);
```

## Workgroup memory declared and the limit the driver reports

Locator: `openspec/changes/sarc-1.5-7900xtx-prefill-refine/proposal.md`, lines 292-295 (commit `82aaec9983f940cf50dfff30b93e8ecece90917d`)

```text
**Known risk: workgroup memory above the device limit (reviewer's finding, verified from the SPIR-V of build `c9`).** AMDVLK reports `maxComputeSharedMemorySize` = 32,768 bytes (the microbench's `max_shared_mem_bytes`), but the shaders declare more workgroup memory than that:
QK^T `sarc_sdpa_qk_coopmat_pk_t128x128k32g42s32nf` (every QK^T of the final stack) 53,248 bytes, the 780M's `afmb1` 8da4w kernel (1B w2 in the final stack) 60,160, the 4w `sweep_t128x128k32g42s32f32cbt` (1B 4w picks) 40,960, and the parent's own release 4w row
`t256x128k32g24s32f32cbt` 61,440. The overrun is pre-existing (the parent's table row is the largest) and not a regression of this campaign; the driver accepts these pipelines and every correctness gate passes, but it breaks a Vulkan valid-usage rule and `Select.cpp` checks shared memory
only for texture3d linear rows, not for attention rows. No kernel was changed for this. Whether to accept it on AMDVLK or to require in-limit kernels before any promotion is the owner's decision (`STATUS.md`).
```
