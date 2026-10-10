---
id: technique-fused-attention-kernel
title: "Fused attention kernel: QK^T, softmax and attn*V in one compute shader"
type: technique
architectures: [radeon-780m, rx-7600, rx-7900-xtx, arc-b580, arc-pro-b70, rtx-4070-ti-super, jetson-orin]
tags: [kernel-fusion, sdpa, sdpa-qk, sdpa-softmax, sdpa-av, prefill, cooperative-matrix, subgroup-size, required-subgroup-size, subgroup-grid, coopmat-shape, control-barrier, full-subgroups, memory-model, causal-truncation]
confidence: verified
reproducibility: snippet
prerequisites: [lang-glsl-cooperative-matrix]
related: [technique-causal-truncation, pattern-invalid-usage-that-passes-tests, migration-rdna3-to-xe2, pattern-sdpa-release-gap, kernel-sdpa-prefill-780m]
sources: [meas-780m-fused-attention, meas-rx7600-fused-attention, meas-7900xtx-fused-attention, meas-b580-fused-port, meas-b70-fused-port, meas-4070ti-fused-port, meas-orin-fused-port, doc-vk-spec-memory-model, doc-glsl-spec-barrier-functions, doc-glsl-khr-shader-subgroup, doc-vk-spec-spirvenv-cooperative-matrix-subgroups, doc-vk-spec-shaders-compute-subgroups, doc-vk-spec-pipeline-shader-stage-subgroup-flags, pr-llama-cpp-13506, pr-llama-cpp-17356, pr-llama-cpp-18831, pr-mnn-4785]
aliases: ["fused SDPA kernel", "fused3", "fused3sb", "one-pass attention", "online softmax attention"]
symptoms:
  - attention-dominates-prefill
  - softmax-largest-attention-kernel
  - three-attention-dispatches-per-layer
  - fused-port-slower-than-separate-kernels
  - register-spills-in-ported-kernel
evidence_basis:
  - evidence_type: measurement
    source_id: meas-780m-fused-attention
    locator: "results/780m/sessions/c8-fused3/summary.csv, lines 2-8"
  - evidence_type: measurement
    source_id: meas-rx7600-fused-attention
    locator: "results/rx7600/sessions/c2-fused/summary.csv, lines 2-8"
  - evidence_type: measurement
    source_id: meas-7900xtx-fused-attention
    locator: "results/7900xtx/sessions/c2-fused/raw/summary.csv, lines 2-8"
  - evidence_type: measurement
    source_id: meas-b580-fused-port
    locator: "results/b580/sessions/s6-final/summary.csv, lines 2-8"
  - evidence_type: measurement
    source_id: meas-b70-fused-port
    locator: "results/b70/sessions/s3-final/summary.csv, lines 2-8"
  - evidence_type: measurement
    source_id: meas-4070ti-fused-port
    locator: "results/4070ti/sessions/s4-c1/summary.csv, lines 2-8"
  - evidence_type: measurement
    source_id: meas-orin-fused-port
    locator: "results/orin/sessions/s5-c1/summary.csv, lines 2-8"
---

# Fused attention kernel

**Do this** when a prefill still runs attention as three dispatches (QK^T, softmax, attn*V) and the softmax is a large part of the attention time. Six of seven measured devices gained +6 % to +18 % geometric mean over an already tuned three-kernel parent.

**Do not assume it pays.** On the RX 7900 XTX under AMDVLK the same kernel was 13.79 % slower than the three cooperative-matrix kernels and was rejected. Compare kernel time against the three kernels it replaces on the target driver before gating anything.

**Do not port it straight** to a device whose matrix shape or subgroup size differs: on the Arc B580 the straight port was correct and 3 to 6 times slower until the workgroup was split into several subgroups.

Citations: `[meas-<id>: <file>, lines]` names a file inside the campaign change directory listed in that page's `raw_data`; the measurement page holds the verbatim lines. Every figure is for the device, driver version and date in its row; gains are the candidate against its parent in one interleaved session, 2048-token prefill, six cells (Llama 3.2 1B, 3.2 3B, 3.1 8B in 4w and 8da4w). "Stock" below means upstream ExecuTorch's own Vulkan attention kernels; it is the baseline, not a source of the technique.

## What it is

One shader takes a block of query rows of one head, walks the context in column blocks, and for each block computes the scores (cooperative-matrix QK^T), exponentiates them against the row maximum, and accumulates e*V in fp32 cooperative-matrix accumulators; at the end it divides by the row sum. A copy pass first writes tile-packed copies of K and V.

What moves through shared memory, per block: the block's scores (fp16), then e in the same slots, the per-lane row maxima and sums, and in the one-pass form the per-row rescale divisors; 3456 to 5892 bytes per workgroup in the one-pass variants of the two ports cited here [meas-4070ti-fused-port: proposal.md, lines 114-119] [meas-b580-fused-port: proposal.md, lines 114-118].

Why it saves time, as the 780M record states it: the three kernels "each move the S x S attention matrix through memory (about 550 MB a layer on 1B). The fused kernel never writes it" [meas-780m-fused-attention: proposal.md, lines 319-320]. The traces agree on where the time went: on the Arc Pro B70 the softmax was 12.7 of the 23.7 ms of 1B attention before the change [meas-b70-fused-port: proposal.md, lines 358-361]; on the RTX 4070 Ti SUPER 1B 4w attention went from 4.18 + 7.47 + 5.42 ms to 5.71 + 0.11 ms [meas-4070ti-fused-port: proposal.md, line 219]. Those records also list tile-packed K and V and Q tiles kept in registers as what made the kernel fast [meas-780m-fused-attention: proposal.md, lines 324-327]; on the Orin the unpacked forms were 1.5 and 3.4 times slower [meas-orin-fused-port: STATUS.md, line 592].

The exchange point, single-subgroup form (https://github.com/sarc-acl/executorch at commit 8f8c44e22e2d8c62a6a192f00e252f8768486b0d, `backends/vulkan/runtime/graph/ops/glsl/sarc_dev/sarc_dev_4070ti_sdpa_fused3sb.glsl#L217-L221` and `#L308-L311`):

```glsl
  // 4070ti: Psh, Rsh and Dsh are private to this subgroup, and every slot has
  // one writer, only if the workgroup is one full subgroup.
  if (gl_NumSubgroups != 1u || gl_SubgroupSize != SUBGROUP_SIZE) {
    return;
  }
```

```glsl
  for (uint b = 0; b < num_blocks; ++b) {
    qk_block(q_base, b * K_BLOCK + k_head);
    memoryBarrierShared();
    subgroupBarrier();
```

## Per-vendor forms and measured outcomes

| Device, driver, date | Form | Gain over its parent (geomean; range of cells) | Gate | Citation |
|---|---|---|---|---|
| Radeon 780M, RADV Mesa 25.2.7, 2026-10-05 | one subgroup of 32 per workgroup, two-pass, packed; no run-time guard, subgroup size not required by the pipeline | +13.16 % (+7.84 to +20.14 %) | accepted under a reference-error rule; one next-token item differs (8B 8da4w) | [meas-780m-fused-attention: results/780m/sessions/c8-fused3/summary.csv, lines 2-8; proposal.md, line 272] |
| same, 2026-10-09 | `fused3` replaced by `fused3sb` (subgroup barrier added), one-pass | -0.14 % (-0.96 to +0.16 %), inside the band | tiers 0 mismatches; output byte-identical to `fused3` | [meas-780m-fused-attention: proposal.md, lines 827-833, 896-901] |
| Radeon RX 7600, RADV Mesa 26.2.3, 2026-10-06 | the 780M's kernel, one-pass, packed | +18.22 % (+9.80 to +29.44 %) | accepted under the reference-error rule; next token same everywhere | [meas-rx7600-fused-attention: results/rx7600/sessions/c2-fused/summary.csv, lines 2-8; results/rx7600/acceptance-c2.txt, lines 1-17] |
| same, 2026-10-08 | `fused3sb` against `fused3` | +0.00 % (-0.19 to +0.17 %) | gated; byte-identical in 21 of 21 cases | [meas-rx7600-fused-attention: results/rx7600/sessions/m2a-sgbarrier/summary.csv, lines 2-8; sdpa-error/bitwise.txt, lines 1-21] |
| RTX 4070 Ti SUPER, NVIDIA 615.71.09, 2026-10-09 | `fused3sb` unchanged plus a guard: return unless the workgroup is one subgroup of 32; one-pass | +11.49 % (+5.92 to +21.15 %) | `GATE_ACCEPTED`, 36 of 36 tier passes, next token same | [meas-4070ti-fused-port: results/4070ti/sessions/s4-c1/summary.csv, lines 2-8; proposal.md, lines 199-203] |
| Jetson Orin Nano, NVIDIA 595.78, 2026-10-09 | the same with the same guard; one-pass for both head dimensions | +6.13 % (+3.05 to +11.17 %) | accepted (reference-error rule); cross build with another shader compiler | [meas-orin-fused-port: results/orin/sessions/s5-c1/summary.csv, lines 2-8; proposal.md, lines 245, 171-174] |
| Arc B580, ANV Mesa 26.2.3, 2026-10-09 | multi-subgroup: 4 or 8 subgroups of 16 per workgroup, 8 x 16 x 16 matrices, workgroup barrier, guard writes NaN rows | +9.12 % (+3.14 to +20.54 %) | `GATE_PASS`, next token same in 18 comparisons | [meas-b580-fused-port: results/b580/sessions/s6-final/summary.csv, lines 2-8; STATUS.md, lines 140-144] |
| Arc Pro B70, ANV Mesa 26.2.3, 2026-10-09 | the B580's kernel, byte-identical SPIR-V | +8.26 % (+3.06 to +19.05 %) | `GATE_PASS` | [meas-b70-fused-port: results/b70/sessions/s3-final/summary.csv, lines 2-8; proposal.md, lines 59-63, 316-320] |
| Radeon RX 7900 XTX, AMDVLK 2025.Q2.1, 2026-10-08 | `fused3sb`, two-pass variants picked by a screen | **-13.79 %** (1B +0.00 %; 3B and 8B -15.25 to -24.03 %) | **rejected on performance**; gate stopped after the timed session (tier `all` 12 passes and `extended` 6 passes ran, 0 mismatches) | [meas-7900xtx-fused-attention: results/7900xtx/sessions/c2-fused/raw/summary.csv, lines 2-8; gate.status, lines 1-3; sdpa-correctness/summary.txt, lines 1-18] |

Reading the table:

- **The gain is largest on the small model.** The 1B cells gain +10 to +29 %, the 8B cells +3 to +12 % on the six devices that adopted it. After adoption attention is 6 to 12 % of a prefill [meas-4070ti-fused-port: proposal.md, lines 219-224] [meas-b70-fused-port: proposal.md, line 361], and a second attention candidate stayed inside the +-2 % band on the B580 (+0.08 %) and the Orin (+0.54 %) [meas-b580-fused-port: proposal.md, lines 314-317] [meas-orin-fused-port: proposal.md, line 246].
- **The parents differ.** Every parent already ran cooperative-matrix QK^T and attn*V kernels; the gains are not over stock.
- **The 7900 XTX rejection.** The record's explanation is that the three-kernel path is already fast there: 1.5 to 1.7 ms per layer, against 1.7 ms (head_dim 64) and 3.7 to 4.5 ms (head_dim 128) for the best fused variant [meas-7900xtx-fused-attention: proposal.md, lines 163-165]. The AMD pipelines do not require a subgroup size [meas-b580-fused-port: proposal.md, line 78] and the run-time guard exists only in the later ports [meas-4070ti-fused-port: proposal.md, line 105], so the subgroup width it ran with under AMDVLK is **unverified**; the record does not state it. Whether the slowdown belongs to the driver's compiler, to the subgroup width or to the kernel is not established. The same holds for RADV: the RX 7600 record says the wave size RADV picks for the 32-invocation workgroup "is UNVERIFIED" [meas-rx7600-fused-attention: STATUS.md, line 79].

## Multi-subgroup form on Intel Xe2

ANV exposes fp16 8 x 16 x 16 only and compiles the kernel for 16 lanes with 128 registers [meas-b580-fused-port: proposal.md, line 73; STATUS.md, lines 443-444]. With only the matrix shape changed, the kernel passed five tiers with 0 mismatches and took 5.9 ms against 2.0 ms (head_dim 64) and 14.4 ms against 2.3 ms (head_dim 128, 8B) for the parent's three kernels [meas-b580-fused-port: proposal.md, lines 82-84].

Why: the single-subgroup kernel keeps all accumulator and Q tiles of its rows in registers. "A thread's register file holds 4096 bytes of 16-lane values; the fp32 accumulators of 8 rows x head_dim 128 alone are 4096 bytes" [meas-b580-fused-port: STATUS.md, lines 457-458]. The compile-time statistics show 1114 to 1250 spills for the 780M's head_dim 128 shape at 16 lanes and 0 for every multi-subgroup variant [meas-b580-fused-port: STATUS.md, lines 451-455]. Moving the accumulators to shared memory was slower in every case [meas-b580-fused-port: STATUS.md, lines 464-466].

What changed: each of G subgroups owns 1/G of a block's score columns and 1/G of the accumulator's head_dim tiles; scores and e go through shared memory that every subgroup reads; every barrier becomes a workgroup barrier; the one-pass rescale vote `subgroupAny` becomes an atomic flag read after a barrier [meas-b580-fused-port: proposal.md, lines 96-104]. Commit a434a49623600f168089173a964efc79661ac286, `.../sarc_dev/sarc_dev_b580_sdpa_fused.glsl#L136-L141` and `#L453-L462`:

```glsl
#ifdef MULTI_SG
#define SYNC() memoryBarrierShared(); barrier()
#define SG_ID gl_SubgroupID
#else
#define SYNC() memoryBarrierShared(); subgroupBarrier()
#define SG_ID 0u
```

```glsl
    const float new_max = max(row_max, blk_max);
#ifdef MULTI_SG
    // The rescale has barriers, so every subgroup must take it together.
    if (new_max > row_max) {
      atomicOr(Gsh, 1u);
    }
    SYNC();
    if (Gsh != 0u) {
#else
    if (subgroupAny(new_max > row_max)) {
```

Kernel time per layer at S = 2048 on the B580: the three kernels 1989 / 1771 / 2297 us (1B / 3B / 8B), the fused kernel with its copy pass 724 / 1139 / 1464 us [meas-b580-fused-port: proposal.md, lines 319-321]. On the B70 the 780M's shapes screened at 0.35x and 0.13x of the parent and the multi-subgroup pair at 3.05x and 1.72x / 1.75x [meas-b70-fused-port: proposal.md, lines 283-288]. See `migration-rdna3-to-xe2`.

llama.cpp's KHR cooperative-matrix flash-attention shader is an independent kernel of the same shape: its comment reads "Bc split across workgroup (four subgroups)", each subgroup takes a share of the columns, and the exchanges are `barrier()` calls (`artifacts/kernels/llama-cpp-flash-attention/flash_attn_cm1.comp`, lines 265-266 and 441-443, commit c479922ac520a08969b4c1dc154d7bbb3c386d85). Its first version states that it needs the 16 x 16 x 16 shape and a subgroup size of 32, and uses the matrices for QK^T only [pr-llama-cpp-13506: excerpt].

## One pass or two

Two-pass: a first walk over the context finds the row maxima, a second computes e and accumulates. One-pass ("online"): a running maximum, with the accumulator and row sum rescaled when it rises; it needs the divisor array and a workgroup-uniform rescale branch.

| Device, driver | Finding | Chosen | Citation |
|---|---|---|---|
| Radeon 780M, RADV Mesa 25.2.7 | one-pass kernel time 2.82 -> 2.26 ms (1B), 4.31 -> 3.22 (3B), 5.54 -> 4.05 (8B) per layer; alone +1.1 to +1.8 % end to end, inside the band | one-pass | [meas-780m-fused-attention: proposal.md, lines 328-330] |
| Jetson Orin Nano, NVIDIA 595.78 | head_dim 128: one-pass 13.84 to 13.90 ms against 19.19 to 19.26 (3B). head_dim 64: two-pass 9.61 to 9.64 ms against 11.53 to 11.62; gated as a second candidate at +0.54 %, inside the band | one-pass for both (two-pass head_dim 64 not adopted) | [meas-orin-fused-port: STATUS.md, lines 587-588; proposal.md, line 246] |
| RX 7900 XTX, AMDVLK 2025.Q2.1 | one-pass variants 1.3 to 2.6 times slower than two-pass in the screen | two-pass (then rejected against the three kernels) | [meas-7900xtx-fused-attention: results/7900xtx/fused/README.md, lines 7-8; pick-analysis.txt, lines 2 and 7] |
| Arc B580 / B70, ANV Mesa 26.2.3 | both selected variants are one-pass; the screens did not include a two-pass multi-subgroup variant | one-pass | [meas-b580-fused-port: proposal.md, line 321] |

So the choice is per device and per head dimension; screen both. MNN's attention path is an independent online-softmax implementation that keeps the softmax as its own shader and makes the same one-subgroup assumption: "Host sets local_size_x == device subgroup size, so the whole workgroup is a single subgroup" (`artifacts/kernels/mnn-attention/attention_prefill_kblock_softmax_online_subgroup.comp`, lines 34-37, commit 9c1788748c4d8aba00f9b644f50f5c15576d7d80; file listed by [pr-mnn-4785]).

## Correctness conditions

1. **An execution barrier at every shared-memory exchange.** The first kernel ordered cross-lane reads with `memoryBarrierShared()` alone and passed every test on RDNA3 [meas-780m-fused-attention: proposal.md, lines 768-787]. A store is visible only to a "future" access, and "An access is only a _future_ access if a _happens-before_ relation can be established" [doc-glsl-spec-barrier-functions: chapters/builtinfunctions.adoc, lines 3518-3530]; a control barrier is what links a release to an acquire across invocations [doc-vk-spec-memory-model: appendices/memorymodel.adoc, lines 556-569], and an unordered write and read of one location is a data race the application must not cause [doc-vk-spec-memory-model: appendices/memorymodel.adoc, lines 1090-1104]. Use `subgroupBarrier()` [doc-glsl-khr-shader-subgroup: GL_KHR_shader_subgroup.txt, lines 701-706] when the workgroup is one subgroup and `barrier()` when slots cross subgroups. Details: `pattern-invalid-usage-that-passes-tests`.
2. **One writer per slot, uniform control flow around barriers.** Each lane owns a (row, segment); whole tiles are stored by cooperative-matrix stores; the one data-dependent branch is entered on `subgroupAny` or on the atomic flag [meas-4070ti-fused-port: proposal.md, lines 134-139] [meas-b580-fused-port: STATUS.md, lines 621-625].
3. **The workgroup must be the full subgroups the lane mapping assumes.** A pipeline with cooperative matrices must be created with the full-subgroups flag or from SPIR-V 1.6 [doc-vk-spec-spirvenv-cooperative-matrix-subgroups: appendices/spirvenv.adoc, lines 1782-1790]; full subgroups mean every subgroup launches with all invocations active [doc-vk-spec-shaders-compute-subgroups: chapters/shaders.adoc, lines 1980-2009], and with a required subgroup size the local size in X must be a multiple of it [doc-vk-spec-pipeline-shader-stage-subgroup-flags: chapters/pipelines.adoc, lines 1297-1303]. **None of the measured pipelines had the flag** (SPIR-V 1.3, stage flags 0) [meas-b580-fused-port: proposal.md, lines 333-342]. The NVIDIA and Intel ports check `gl_NumSubgroups` and `gl_SubgroupSize` at run time; the record is explicit that this "does not make the pipeline valid" [meas-b580-fused-port: proposal.md, lines 343-346] [meas-orin-fused-port: proposal.md, lines 147-150]. The AMD kernel has neither a required size nor the check. llama.cpp forced full subgroups for its flash-attention shader on Intel [pr-llama-cpp-17356: excerpt] and later reverted that [pr-llama-cpp-18831: excerpt].
4. **The separate softmax still serves some calls.** The fused node takes only LLM-mode fp16 calls whose S and `input_pos` are multiples of the row and column tiles; decode and an unaligned prompt run the parent's three kernels [meas-4070ti-fused-port: proposal.md, lines 86-91] [meas-b70-fused-port: proposal.md, lines 53-55]. A truncated softmax in that path stays tied to its attn*V kernel: the 780M softmax bounds its zero fill "to what attn*V reads" [meas-780m-fused-attention: proposal.md, line 271]; see `technique-causal-truncation`.
5. **The arithmetic changes.** The summation order differs from the three-kernel path, so candidates were judged by error against a reference, not by bit identity [meas-4070ti-fused-port: proposal.md, lines 148-151].

## What this does not show

- Not a gain over stock: every parent already had cooperative-matrix attention kernels.
- Not why AMDVLK lost. One driver version, no compiler statistics, subgroup width unverified, gate not completed.
- Not validity. All gates ran on pipelines without the full-subgroups flag. A later note in the campaign's overview reports that adding the flag on the Arc B580 removed the validation message and left output and speed unchanged within the band; that note gives no driver version and its raw data is not published, so no figure from it is recorded here [meas-b580-fused-port: openspec/changes/sarc-1.5-campaign-playbook/report/tuning-overview.html, line 248]. No other device has been re-run.
- Not decode. With the fused node present decode was 0 to 2.5 % slower on the B70 and 0.1 to 1.5 % slower on the B580, although decode does not run the kernel; the cost was not located [meas-b70-fused-port: proposal.md, lines 382-385] [meas-b580-fused-port: proposal.md, lines 359-363].
- Not unaligned or real-length prompts: a 1972-token prompt gains nothing [meas-b70-fused-port: proposal.md, lines 389-390].
- The Orin figures come from a cross build whose shader compiler differs from the campaign's reference [meas-orin-fused-port: proposal.md, lines 171-174]. The 780M's first gain was measured through local hook patches [meas-780m-fused-attention: proposal.md, lines 278-279].
- One driver version per device; no Qualcomm or Arm device.

## Confidence

`verified` for the measured outcomes in the tables: each is a first-party session on the named device and driver. The explanations of why (memory traffic, register pressure, why a driver lost) are the records' own reasoning and are source-reported, not isolated by a measurement.
