---
id: pattern-sdpa-release-gap
title: "End-to-end prefill gap between two releases with matching linear kernels, attributed by the gap report to the SDPA kernels (Radeon 780M)"
type: pattern
architectures: [radeon-780m]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, causal-truncation, cooperative-matrix, prefill, linear-4w, linear-8da4w]
confidence: source-reported
symptoms:
  - "Prefill tok/s on the newer release is well below the older tuned branch on the same device, although the linear kernels take the same GPU time in both"
  - "The gap between the two releases is about the same with ET_VK_FORCE_TILED_LINEAR set"
  - "A port of the linear kernels alone leaves end-to-end prefill below the older branch"
candidate_techniques: [hw-cooperative-matrix-rdna3, technique-causal-truncation]
related: [kernel-sdpa-prefill-780m, kernel-linear-4w-780m, kernel-linear-8da4w-780m, hw-radeon-780m, pattern-unaligned-m-fallback]
sources: [meas-780m-sdpa-port, meas-780m-8da4w-port]
evidence_basis:
  - evidence_type: measurement
    source_id: meas-780m-sdpa-port
    locator: "openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28"
  - evidence_type: measurement
    source_id: meas-780m-sdpa-port
    locator: "openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 1-31"
---

# End-to-end prefill gap between two releases, attributed to the SDPA kernels

Scope: one device (Radeon 780M), one driver (RADV Mesa 25.2.7), two result sets dated 2026-09-27 (`meas-780m-sdpa-port`, `meas-780m-8da4w-port`). Nothing here is established for another device, driver or date.

How the driver version is known: the result sets' own device lines name the driver as `radv phoenix` and record no version [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, line 5] [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, line 5]. The version is attributed from the package install history captured on the device on 2026-10-04, which shows the Vulkan driver package at 25.2.7 since 2026-05-29 with no later entry [meas-780m-sdpa-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 3-5 and lines 10-14]. It is not recorded by the runs.

"1.4" below is the SARC branch of release 1.4, "1.5" is release 1.5 with the SARC linear kernels. They are two software builds on the same device. All ratios on this page are quoted from the evidence; none is computed here.

## Symptom

- "On release 1.5 the Radeon 780M ran 1B 4w prefill at 1930 tok/s, against 2702 on the 1.4 SARC branch, although the linear kernels matched." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 1-12 (lines 5-6)]
- The gap report measured the same cell (Llama 3.2 1B, 4w, 2048-token prefill) at 2702 tok/s for 1.4 and 1916 (1916-1919) tok/s for 1.5 [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28 (line 24)].
- With the linears forced to the tiled kernels the gap is still there: 799 (797-803) tok/s for 1.4 and 710 (706-713) tok/s for 1.5 [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28 (line 24)].
- The same symptom shows for 8da4w after the linear port alone. The 8da4w port measured 1845.05, 649.128 and 336.068 tok/s for Llama 3.2 1B, Llama 3.2 3B and Llama 3.1 8B in default mode [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 1-25 (lines 4, 9, 11)], while its proposal lists "1.4 tuned" as 2538 / 1055 / 486 and notes that on the 780M this "includes the SARC SDPA coopmat, which this change does not contain" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 34-43 (lines 38-39, 43)].

## Diagnosis given by the evidence

Method: "ETDump per-kernel GPU timestamps, last run of 2 per file, 3 repeats per cell (median, with min–max)", on traced `llama_main` builds of both versions [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 1-8 (lines 6-7)].

GPU ms per Llama 3.2 1B 4w prefill, by kernel family, default ("tuned") mode. Every row is cited to [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28], at the line given in the last column:

| Family | 1.4 tuned | 1.5 tuned | delta (as stated) | Line |
|---|---|---|---|---|
| SDPA attn*V | 43.6 (coopmat) | 224.7 (tiled) | +181.1 | 14 |
| SDPA QK^T | 75.3 (coopmat) | 156.7 (tiled) | +81.4 | 15 |
| SDPA softmax | 115.1 | 161.6 | +46.5 | 16 |
| SDPA kv_cache_update | 5.3 | 3.1 | -2.2 | 17 |
| SDPA subtotal | 239.2 | 546.1 | +306.9 | 18 |
| linear 4w | 372.5 | 373.3 | +0.8 | 19 |
| copy/view/slice | 59.2 | 60.8 | +1.6 | 20 |
| add/mul, silu, rms_norm, rope | 81.2 | 81.6 | +0.4 | 21 |
| GPU sum | 752.1 (752.1-752.3) | 1061.5 (1059.6-1062.8) | +309.4 | 22 |
| graph-execute wall | 754.2 | 1063.9 | +309.7 | 23 |

What the report concludes from the table:

- "SDPA accounts for 307 of the 309 ms per prefill (99 %)" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 1-8 (line 3)].
- "Dispatch counts are identical in the two versions." and "Wall minus GPU sum is ~2 ms (tuned) and ~6 ms (tiled) in both versions, so 1.5 adds no CPU or submission overhead." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28 (lines 26-27)]
- "The gap is the same in tiled mode because 1.4 runs its SDPA coopmat there too; `ET_VK_FORCE_TILED_LINEAR` only affects the linears." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28 (line 28)] In tiled mode the SDPA subtotal is 239.4 ms for 1.4 and 541.6 ms for 1.5, stated delta +302.2 [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28 (line 18)].

The cause, as the proposal puts it: "the 1.4 branch ran SARC's SDPA coopmat kernels (AMD subgroup 64)", "1.4 also ran a causally truncated softmax", and "release 1.5 has neither" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 1-12 (lines 10-12)].

Larger models. The SDPA microbenchmark per call (`--sdpa --regime=prefill`, excluding the kv-cache update) gave [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 30-39 (lines 34-36)]:

| Model | 1.4 | 1.5 | predicted end-to-end delta | observed |
|---|---|---|---|---|
| 1B | 15.0 ms | 33.6 ms | x16 layers = 0.30 s | 0.31 s |
| 3B | 14.6 ms | 52.7 ms | x28 = 1.07 s | 1.1 s |
| 8B | 18.7 ms | 70.6 ms | x32 = 1.66 s | 1.8 s |

The report limits this: "The 3B/8B attribution is inferred from the microbench, not traced end to end. About 0.14 s of the 8B gap is unexplained." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 30-39 (lines 38-39)]

## Remedy used by the evidence

The gap report lists what the 1.4 branch had and release 1.5 lacked, with the time it attributes to each [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 41-56]:

1. attn*V cooperative-matrix kernel (t64x64k32g22s64), "~181 ms" (lines 43-44).
2. QK^T cooperative-matrix kernel (t128x64k32g22s64), "~81 ms" (lines 45-46).
3. Softmax causal-tail truncation, "~46 ms" (lines 47-48). See `technique-causal-truncation`.
4. Supporting `SDPA.cpp` changes, among them the gate `supports_cooperative_matrix() && subgroup_size()==64` (lines 49-54). The device condition is on `hw-cooperative-matrix-rdna3`.

The port (`sarc-1.5-sdpa-port`) brought these to release 1.5 as `sarc_sdpa_qk_coopmat` (t128x64k32g22s64), `sarc_sdpa_av_coopmat` (t64x64k32g22s64) and `sarc_sdpa_attn_weights_softmax` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 14-29 (lines 16-22)]. The 780M selection rows are `Op::kSdpaQk` with `sarc_sdpa_qk_coopmat_t128x64k32g22s64` and `Op::kSdpaAv` with `sarc_sdpa_av_coopmat_t64x64k32g22s64`, both `Status::kVerified` [meas-780m-sdpa-port: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp, lines 78-96]. The kernels are described on `kernel-sdpa-prefill-780m`.

## Result after the port

SDPA correctness, with both cooperative-matrix kernels dispatched: four cases, `mismatches=0/16384`, `0/262144`, `0/32768` and `0/524288`, all `PASSED` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-correctness.log, lines 1-23 (lines 19-22)].

End to end, 2048-token prefill tok/s with the 4w, 8da4w and SDPA rows, one run per cell [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 1-31]. "tiled" is `ET_VK_FORCE_TILED_LINEAR=1` in `sarc/tools/verify.sh` at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae of https://github.com/sarc-acl/executorch [meas-780m-sdpa-port: sarc/tools/verify.sh, lines 86-106]; the result set does not record the command line, and the summary-line formats of `r4.out` lines 3-23 and 25-30 match that script. The 1.4 columns are the proposal's rounded figures for the 1.4 build [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 32-48 (lines 42-43)].

| Scheme | Model | 1.5 tiled | 1.5 default | r4.out lines | 1.4 tiled (proposal) | 1.4 tuned (proposal) |
|---|---|---|---|---|---|---|
| 4w | Llama 3.2 1B | 797.197 | 2694.74 | 6, 7 | 801 | 2702 |
| 4w | Llama 3.2 3B | 282.795 | 1138.41 | 16, 17 | 283 | 1142 |
| 4w | Llama 3.1 8B | 113.734 | 516.389 | 20, 21 | 114 | 516 |
| 8da4w | Llama 3.2 1B | 2155.79 | 2544.1 | 11, 12 | 2151 | 2538 |
| 8da4w | Llama 3.2 3B | 850.145 | 1048.11 | 18, 19 | 858 | 1055 |
| 8da4w | Llama 3.1 8B | 377.372 | 486.692 | 22, 23 | 375 | 486 |

The proposal's conclusion: "The 780M is back at its 1.4 numbers (within 0.7 %)." [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/proposal.md, lines 32-48 (line 45)] The gap report had predicted "~2705 tok/s tuned (inferred)" for the 1B 4w cell [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 41-56 (line 56)].

Other checks of the same run: the next-token comparison between default and tiled reads `SAME` for the check prompt and the unaligned prompt, for both schemes [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 1-31 (lines 8, 9, 13, 14)], and the six 8da4w production-diff cases read `ALL PASSED` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 1-31 (lines 25-30)].

## How to apply the diagnosis elsewhere

The steps the evidence took, in order:

1. Compare per-family GPU time from per-kernel timestamps of both builds on the same prompt, not only tok/s [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 1-8].
2. Check that the linear family matches (here 372.5 ms against 373.3 ms [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28 (line 19)]) and that dispatch counts and wall-minus-GPU time match, which rules out the linear kernels and the CPU side.
3. Repeat with `ET_VK_FORCE_TILED_LINEAR`. That switch "only affects the linears", so a gap that stays is outside the linear kernels [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, lines 10-28 (line 28)].

## Limits of this evidence

- The post-port end-to-end values are single runs per cell, taken with `ET_VK_SARC_UNVERIFIED=1` set [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/env.txt, lines 1, 3-7].
- The per-family times are for the two builds before the port. The result set holds no per-kernel time for the ported cooperative-matrix SDPA kernels on release 1.5: in the SDPA microbenchmark of the port the `coopmat` rows record 0.0 for `qk` and `av`, so that log's `total` and `speedup` figures for `coopmat` are not full SDPA times and are not used here [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa2/sdpa-prefill.log, lines 44-81 (lines 50-53, 62-65, 74-77)].
- The result directory `results/780m/sdpa` reports `qk_coopmat=NO av_coopmat=NO` and `FAILED` in all four cases, with 0 mismatches [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-correctness.log, lines 1-23 (lines 19-22)]. The summary line of `r4.out` for SDPA correctness shows the same `qk_coopmat=NO av_coopmat=NO` result with `rc=1` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 1-31 (line 1)]. The correctness result cited above is from the directory `sdpa2`, where both kernels were dispatched. Neither directory carries a timestamp; the result set does not record their order, nor why the kernels were not dispatched in `sdpa`.
- The 3B and 8B attribution is the report's inference from the microbenchmark, as quoted above.

## Confidence

`source-reported`. The per-family GPU times of the two builds exist in the result set only as the summary table of the gap report; the report lists its raw data as "`t14-*`, `t14b-*`, `t15-*` (ETDumps and logs), `summary.txt`, `analyze.py`, `run.sh`, `mb/`" [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/sdpa-gap-REPORT.md, line 80], and none of those files is in the result set at that commit (its `results` directory holds only the report and the `780m` directory), so the traces cannot be re-read from this wiki's sources. The 1.4 columns of the after-port table are the proposal's figures, not a run in the result set. The after-port 1.5 values are single runs logged on the device (`r4.out` and the `sdpa-e2e` logs). The split of the SDPA gap into three causes with "~181 ms", "~81 ms" and "~46 ms" is the gap report's attribution; no measurement in the result set enables the three changes one at a time. The same evidence is rated `source-reported` on `kernel-sdpa-prefill-780m`.
