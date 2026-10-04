---
id: technique-causal-truncation
title: "Causal-tail truncation in the attention-weight softmax (sarc_sdpa_attn_weights_softmax) on the Radeon 780M"
type: technique
architectures: [radeon-780m]
tags: [causal-truncation, sdpa, sdpa-softmax, prefill]
confidence: source-reported
reproducibility: snippet
prerequisites: [hw-radeon-780m]
related: [hw-cooperative-matrix-rdna3, pattern-unaligned-m-fallback, kernel-sdpa-prefill-780m]
sources: [meas-780m-e2e-prefill]
aliases: ["truncated softmax", "causal-mask truncation", "reduce_len"]
---

# Causal-tail truncation in the attention-weight softmax

Scope: one device (Radeon 780M), one driver (RADV Mesa 25.2.7), measured 2026-09-28 (`meas-780m-e2e-prefill`). Nothing here is established for another device, driver or date.

"code" below means https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae. A citation of the form `[code: path#L]` points at that commit and is a statement of the code or its authors, not a measurement held in a source page of this wiki.

## What the technique is

In LLM mode the attention-weight row for query position `s` is causally masked beyond column `s + input_pos`. The softmax shader therefore runs its three passes (row maximum, sum of exponentials, normalization) only over the unmasked prefix of each row, and writes zeros to the masked tail without loading it.

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.glsl#L140-L162` (code)

```glsl
  // Causal-mask truncation. In LLM mode the QK^T shader has already written
  // -inf to every element with c > s + input_pos, so for row s only the first
  // (s + input_pos + 1) columns carry information: a masked element
  // contributes exp(-inf - max) == 0 to the sum, cannot be the row max unless
  // the whole row is masked, and normalizes to exactly 0. All three passes can
  // therefore stop at reduce_len instead of context_len, which on a full
  // prefill halves the bytes read (the rows are a triangle, not a rectangle).
  //
  // The STORE still has to cover the whole context_len row: attn*V stages
  // every chunk with chunkK < context_len and multiplies it by V, so the
  // masked tail must be written as zero rather than left stale. Writing zero
  // is cheaper than reading + exp + writing, and needs no load.
  //
  // Fused mode has no input_pos and gets its mask from an attn_mask bias
  // instead, so no truncation is valid there.
#ifdef HAS_INPUT_POS
  const int reduce_len = min(context_len, s + input_pos + 1);
#else
  const int reduce_len = context_len;
#endif
  const int reduce_texel_len = div_up_4(reduce_len);
  const int reduce_len_aligned_down = reduce_len - mod_4(reduce_len);
  const int R4_limit = div_4(reduce_len_aligned_down);
```

Locator: `backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.glsl#L293-L301` (code)

```glsl
  // Causally-masked tail: every element normalizes to exactly 0, so write zero
  // WITHOUT loading the input. This is the read the truncation saves in pass 3,
  // and the store attn*V depends on (it stages the whole context_len row).
  // Spread across all workers, unlike the straddling texel above.
  for (int c4 = reduce_texel_len + worker_id; c4 < context_texel_len;
       c4 += NUM_WORKERS_PER_WG) {
    store_attn_weights_softmax_c4(
        VEC4_T(0), c4, s, q_h, context_texel_len, attn_S, Q_H);
  }
```

Conditions stated by the shader comment above:

- It relies on the QK^T shader having written `-inf` to every masked element.
- The masked tail must still be stored as zero, because the attn*V kernel stages the whole row.
- It is valid in LLM mode only (`HAS_INPUT_POS`); fused mode takes its mask from a bias and is not truncated.

The shader yaml describes the kernel as a copy of release 1.5's `sdpa_attn_weights_softmax` (LLM mode only) with this truncation added, selected for devices with an SDPA row [code: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_sdpa_attn_weights_softmax.yaml#L7-L10].

## Use on the Radeon 780M

- In the 2026-09-28 campaign the SARC build dispatched `sarc_sdpa_attn_weights_softmax_buffer_half` 16 times per Llama 3.2 1B 4w prefill; the stock build dispatched `sdpa_attn_weights_softmax_buffer_half` 16 times [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/dispatch.csv, lines 5 and 12].
- The campaign report lists `sarc_sdpa_attn_weights_softmax` among the SDPA kernels of the SARC build on the Radeon 780M [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 340-343, 345] and states that the 780M's speedup "includes the coopmat QKᵀ/AV kernels and the truncated softmax" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 115-116].

## Measured GPU time of the softmax family on the 780M

GPU time of the trace family "attention: softmax" per 2048-token prefill, 4w, from the warm ETDump traces [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, line 76]:

| Model | stock build, ms | SARC build, ms | Citations |
|---|---|---|---|
| Llama 3.2 1B | 161.568 | 115.253 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv, lines 16 and 3] |
| Llama 3.2 3B | 206.803 | 150.302 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv, lines 68 and 55] |
| Llama 3.1 8B | 315.328 | 229.259 | [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/evidence/trace/families.csv, lines 120 and 107] |

The technical report states the per-kernel softmax speedup on the 780M (4w) as 1.40 for 1B, 1.38 for 3B and 1.38 for 8B [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, lines 227-233]. Those ratios are the report's own figures; this page does not recompute them.

Limits of this evidence:

- The traces are "One `--warmup` run per cell" [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, line 76]; the family times are single-trace values, not medians of repeats.
- The two builds differ in more than this shader. That the SARC softmax differs from the stock softmax only by the truncation is stated by the shader yaml comment (code), not isolated by a measurement.
- The timed prompt of the main campaign is the word "the" repeated 2048 times [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/REPORT.md, lines 431-432].

## Correctness evidence on the 780M

The logits probe compared the stock and SARC builds on the device. On the 2048-token real-text prompt, `top1_same` is `True` in all six 780M rows of `prompt=real` [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv, lines 2, 4, 6, 8, 10, 12]. `bitwise_identical_top10` is `False` in every 780M row [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/results/real/probe.csv, lines 2-13]. These rows compare whole builds (linear and attention kernels together), so they do not attribute any logit difference to the softmax.

At the 1972-token check prompt the linear GEMMs fall back while "attention still uses SARC kernels", and the Llama 3.1 8B 8da4w top-1 token differs between builds [meas-780m-e2e-prefill: openspec/changes/sarc-1.5-e2e-benchmark/TECHNICAL-REPORT.md, lines 390-394]; see `pattern-unaligned-m-fallback`.

## Confidence

`source-reported`. The mechanism is taken from the shader source. The family GPU times are measured on the device and cited to `meas-780m-e2e-prefill`, but they compare two builds rather than the truncation in isolation, so the page is not marked `verified`.
