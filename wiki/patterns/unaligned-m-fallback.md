---
id: pattern-unaligned-m-fallback
title: "SARC linear speedup disappears at a prompt length that is not tile-aligned (Radeon 780M)"
type: pattern
architectures: [radeon-780m]
tags: [workgroup-tile-sizing, tiled-linear, linear-4w, linear-8da4w-zpg, cooperative-matrix, prefill]
confidence: source-reported
symptoms:
  - "With the SARC build, 4w prefill tok/s at a 1972-token prompt is at or below the tiled or stock figure, while at a 2048-token prompt it is well above it"
  - "The next-token comparison between the stock and SARC builds reads DIFFER at a 1972-token prompt for one cell, while the top-1 token is the same at a 2048-token prompt"
candidate_techniques: [technique-workgroup-tile-sizing, hw-cooperative-matrix-rdna3]
related: [technique-causal-truncation, hw-radeon-780m, kernel-linear-4w-780m, kernel-linear-8da4w-780m]
sources: [meas-780m-4w-bootstrap, meas-780m-e2e-prefill]
---

# SARC linear speedup disappears at a prompt length that is not tile-aligned

Scope: one device (Radeon 780M), one driver (RADV Mesa 25.2.7), measurements dated 2026-09-27 (`meas-780m-4w-bootstrap`) and 2026-09-28 (`meas-780m-e2e-prefill`). Nothing here is established for another device, driver or date.

## Symptom 1: throughput at a 1972-token prompt

2026-09-27, Llama 3.2 1B 4w, SARC dev build, single runs, prefill tok/s as logged by `llama_main`:

| Prompt tokens (as logged) | Default mode | Tiled mode (`ET_VK_FORCE_TILED_LINEAR`) | Citations |
|---|---|---|---|
| 2048 | 1915.81 | 714.336 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/prefill-1b-4w-default.log, line 6; .../sarc/prefill-1b-4w-tiled.log, line 6] |
| 1972 | 713.975 | 723.139 | [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/check-1b-4w-default.log, line 140; .../sarc/check-1b-4w-tiled.log, line 140] |

In the same result set the stock release 1.5 build logged 1204.71 tok/s at 2048 tokens and 1246.52 tok/s at 1972 tokens [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/stock/prefill-1b-4w-default.log, line 5; .../stock/check-1b-4w-default.log, line 139].

2026-09-28, release builds, 4w. The 2048-token values are medians of 5 timed runs; the 1972-token values are the single `kind=check` runs:

| Model | stock, 2048 tokens (median) | SARC, 2048 tokens (median) | stock, 1972-token check run | SARC, 1972-token check run | Citations |
|---|---|---|---|---|---|
| Llama 3.2 1B | 1211.83 | 2698.29 | 1256.05 | 737.196 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv, line 2; results/runs_all.csv, lines 12 and 13] |
| Llama 3.2 3B | 425.073 | 1151.21 | 437.93 | 252.368 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv, line 3; results/runs_all.csv, lines 36 and 37] |
| Llama 3.1 8B | 198.008 | 525.802 | 202.776 | 107.519 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv, line 4; results/runs_all.csv, lines 60 and 61] |

For 8da4w the two builds' check runs are close to each other: Llama 3.2 1B stock 1695.61 and SARC 1765.44, against 2048-token medians of 1635.78 and 2544.1 [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/runs_all.csv, lines 24 and 25; results/cells.csv, line 17].

Caution when reading the check-run values: these runs "have no `--warmup`, so their tok/s includes first-inference pipeline creation" and "are used only for the next-token comparison" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 444-447]. They are quoted here as the observed symptom, not as throughput results.

## Symptom 2: next token differs at 1972 tokens for one cell

In the 2026-09-28 campaign the next-token column reads `DIFFER` for the Radeon 780M, Llama 3.1 8B, 8da4w, and `SAME` for the other five 780M cells [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/cells.csv, lines 2, 3, 4, 17, 18, 19]. That comparison is made on the 1972-token check prompt [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 320-327].

The logits probe on the same cell and prompt records stock top-1 id 6062 and SARC top-1 id 45647, `top1_same` `False`, `stock_margin` 0.0938 and `sarc_margin` 0.5 [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv, line 13]. On the 2048-token real-text prompt the same model and scheme has `top1_same` `True` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv, line 12].

## Diagnosis given by the evidence

- The check prompt is 1972 tokens, and "At 1972 tokens, M is not a multiple of any tile" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 320-327].
- The selector only matches a SARC row when "`M % WG_TILE_M == 0`, `N % WG_TILE_N == 0`, `K % WG_TILE_K == 0`" [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 74-81]. The 780M linear tiles are 4w `t128x128k32g42s32f32c` and 8da4w zpg `t128x64k32g42s32` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md, lines 125-127].
- For shapes no row covers, the 4w operator "falls back to release 1.5's own `linear_q4gsw_{tiled,coop}` kernels: decode, unaligned M, bias, fp32" [meas-780m-4w-bootstrap: sarc/README.md, lines 18-24].
- For the 780M row of the 1972-token difference, the SARC path at M = 1972 is described as "GEMM falls back to stock kernels; attention still uses SARC kernels" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, lines 390-394]. So the build under test at that prompt length is a mixed path, not the SARC linear kernels.

Two points the evidence leaves open:

- Which fallback kernel runs. The 4w operator hook is documented as falling back to "release 1.5's own `linear_q4gsw_{tiled,coop}` kernels" for unaligned M [meas-780m-4w-bootstrap: sarc/README.md, lines 18-24], while the stock build's 4w prefill kernel is `q4gsw_linear_gemm__tin__w_4x8_nc_texture3d_half` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv, line 10]. No source page holds a dispatch trace taken at 1972 tokens, so this page does not say which kernel produced the check-run figures above.
- The 2026-09-27 result set also has a 1792-token prompt, which its proposal labels "unaligned prompt (fallback path)" (and gives as 1304-token) [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/proposal.md, lines 55-80]. The logs record `prompt_tokens` 1792 with 2064.52 tok/s in default mode and 731.727 tok/s in tiled mode [meas-780m-4w-bootstrap: openspec/changes/sarc-1.5-bootstrap/results/780m/sarc/unaligned-1b-4w-default.log, line 7; .../sarc/unaligned-1b-4w-tiled.log, line 7]. The logs do not record which kernels ran, so that run is not used as an example of the fallback here.

## Remedy used by the evidence

- To time or validate the SARC linear kernels, use a prompt whose token count is tile-aligned. The campaign added a real-text prompt of "exactly 2048 real-text tokens (GPL-3.0 preamble), tile-aligned" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/CONTRIBUTING-A-GPU.md, line 80] and ran the logits probe on it because that prompt "engages the SARC kernels" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, lines 379-381].
- Read a result taken at an unaligned prompt length as a result of the fallback path. The fallback at unaligned M is documented behaviour of the selection layer (citations above); the evidence does not describe a way to make the tile kernels accept unaligned M.
- Tile dimensions that determine alignment are on `technique-workgroup-tile-sizing` and `hw-cooperative-matrix-rdna3`.

## Confidence

`source-reported`. The figures are measured on the device and cited to the two measurement pages; the diagnosis is the one stated by the campaign's reports and the selector documentation, not an independent trace at the unaligned prompt length.
