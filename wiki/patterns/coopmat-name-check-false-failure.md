---
id: pattern-coopmat-name-check-false-failure
title: "Correctness harness reports FAILED because the kernel name lacks the substring coopmat (Radeon 780M, 8da4w)"
type: pattern
architectures: [radeon-780m]
tags: [cooperative-matrix, linear-8da4w, linear-8da4w-zpg, tiled-linear, prefill]
confidence: source-reported
symptoms:
  - "The correctness or production-diff summary reads FAILED with a non-zero exit code while every case line reads correctness=PASSED"
  - "A case line names a SARC cooperative-matrix kernel and labels it 'NOT coopmat -- fallback'"
  - "The microbenchmark summary marks every buffer row with '!' (did NOT dispatch a coopmat shader) although the dispatched kernel is the SARC kernel"
candidate_techniques: [hw-cooperative-matrix-rdna3]
related: [kernel-linear-8da4w-780m, technique-full-a-map, pattern-unaligned-m-fallback, hw-radeon-780m]
sources: [meas-780m-8da4w-port, meas-780m-sdpa-port]
---

# Correctness harness reports FAILED because the kernel name lacks "coopmat"

Scope: one device (Radeon 780M), one driver (RADV Mesa 25.2.7), two result sets dated 2026-09-27 (`meas-780m-8da4w-port`, `meas-780m-sdpa-port`). Nothing here is established for another device, driver or date.

How the driver version is known: the result sets' own device lines name the driver as `radv phoenix` and record no version [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, line 5] [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/correctness.log, line 5]. The version is attributed from the package install history captured on the device on 2026-10-04, which shows the Vulkan driver package at 25.2.7 since 2026-05-29 with no later entry [meas-780m-8da4w-port: sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt, lines 3-5 and lines 10-14]. It is not recorded by the runs.

"code" below means https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae. A citation of the form `[code: path#L]` points at that commit and is a statement of the code or its authors, not a measurement held in a source page of this wiki.

## Symptom

In the first run of the 8da4w port (output directory `sarc8`; "first run" is the proposal's term, quoted under Cause), the summary lines report failures:

- `correctness rc=1 [correctness] FAILED -- numeric failure(s) and/or a rank-3 case did not dispatch coopmat` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 1-25 (line 1)].
- `linear 8da4w rc=1` for the microbenchmark step [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 1-25 (line 2)].
- `[production-diff] FAILED` with `rc=1` for all six model and storage cases [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 1-25 (lines 12-17)].

The per-case lines of the same logs show a numeric pass:

- `linear_dq8ca_q4gsw_M128_K128_N128_rank3batch1_Buffer -> sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half (NOT coopmat -- fallback), correctness=PASSED`, and the same for the `M128_K4096_N128` case [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/correctness.log, lines 283-287 (lines 285-286)].
- `-> sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half (NOT coopmat -- fallback, cannot validate the shader under test), correctness=PASSED`, followed by `[production-diff] FAILED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/pdiff-llama-3.2-1b-8da4w-buffer.log, line 17; line 51].
- In the microbenchmark summary every row is marked `!` next to `sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half`, with the note "(! = buffer case did NOT dispatch a coopmat shader; shown for reference, excluded from speedups/geomeans)" and the warning "do not trust their speedup numbers" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, lines 227-243 (lines 241 and 243)].

The kernel that these lines call a fallback is the SARC kernel of the port: the microbenchmark dispatched `sarc_linear_dq8ca_zpg_t128x64k32g42s32_buffer_texture2d_half` in 12 cases and `sarc_linear_dq8ca_zpg_t128x64k32g42s32_texture3d_texture2d_half` in 12 cases [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 1-25 (line 2)], with local work size `(256,1,1)` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/linear-8da4w.log, lines 9-14 (line 10)].

## Cause

The proposal states it: "The first run reported FAILED only because the harness saw no "coopmat" in the old `sarc_linear_dq8ca_zpg*` names." [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 49-53 (lines 52-53)]

The harness source at the code commit shows the check. In the correctness matrix, a rank-3 case counts as passed only when the dispatched shader name contains `coopmat` and the numeric status is PASSED:

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp#L876-L892` (code)

```cpp
  // Rank-3, batch=1 dispatch + correctness verdict: numeric PASS alone
  // doesn't prove the coopmat path actually ran -- the tiled fallback would
  // numerically pass too. Explicitly confirm the dispatched kernel name.
  for (const auto& r : results) {
    if (r.get_kernel_name().find("_rank3batch") == std::string::npos) {
      continue;
    }
    const std::string shader_name = linear_kernel(r);
    const bool fired = shader_name.find("coopmat") != std::string::npos;
    const bool ok =
        fired && r.get_correctness_status() == CorrectnessStatus::PASSED;
    all_ok = all_ok && ok;
    std::cout << "[rank3 batch=1] " << r.get_kernel_name() << " -> "
              << shader_name
              << (fired ? " (coopmat dispatched)"
                        : " (NOT coopmat -- fallback)")
              << ", correctness="
```

The production-diff mode uses the same test:

Locator: `backends/vulkan/test/sarc_dev/test_llama_microbench.cpp#L1000-L1009` (code)

```cpp
      const std::string shader_name = linear_kernel(res[0]);
      const bool coopmat_fired =
          shader_name.find("coopmat") != std::string::npos;
      const bool passed =
          res[0].get_correctness_status() == CorrectnessStatus::PASSED;
      all_ok = all_ok && coopmat_fired && passed;
      std::cout << "[production-diff] " << tc.name() << " -> " << shader_name
                << (coopmat_fired ? " (coopmat dispatched)"
                                  : " (NOT coopmat -- fallback, cannot "
                                    "validate the shader under test)")
```

The microbenchmark classifies a kernel as `coopmat` by the substring `_coopmat` [code: backends/vulkan/test/sarc_dev/test_llama_microbench.cpp#L802-L806].

The harness comment gives the reason for the check: a numeric pass "doesn't prove the coopmat path actually ran -- the tiled fallback would numerically pass too" (first excerpt above). The check therefore assumes that every cooperative-matrix kernel has `coopmat` in its name. The names of the first run, `sarc_linear_dq8ca_zpg_*`, do not.

## Remedy used by the evidence

"The kernels have been renamed, and the re-run is in `results/*/pdiff2`." [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 49-53 (line 53)] The shipped names are `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half` and `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_texture3d_texture2d_half` [meas-780m-8da4w-port: backends/vulkan/runtime/graph/ops/glsl/sarc/sarc_linear_dq8ca_coopmat_zpg.yaml, lines 10-35 (lines 31, 33)].

After the rename:

- Production-diff re-run: `-> sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED` and `[production-diff] ALL PASSED (llama-3.2-1b, 4 shapes, M=2048, linear_dq8ca_q4gsw, buffer)` [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log, lines 7-51 (lines 17 and 51)]. The other five files end the same way [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-texture3d.log, lines 7-51 (line 51); openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-3b-8da4w-buffer.log, lines 7-51 (line 51); openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-3b-8da4w-texture3d.log, lines 7-51 (line 51); openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-buffer.log, lines 7-51 (line 51); openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.1-8b-8da4w-texture3d.log, lines 7-51 (line 51)].
- The first run had already passed numerically on the case line (`correctness=PASSED`, cited under Symptom), and for the Llama 3.2 1B buffer file the first sampled-diff line is the same before and after the rename: `max abs diff 0.0156136 (tol 0.5)` in the `sarc8` log [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/pdiff-llama-3.2-1b-8da4w-buffer.log, line 11] and in the `pdiff2` log [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/pdiff2/pdiff-llama-3.2-1b-8da4w-buffer.log, lines 7-51 (line 11)]. The proposal gives the 780M range as "max |err| 0.016–0.124 against 0.5" [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/proposal.md, lines 49-53 (lines 50-51)].
- In the `sdpa-e2e` run of the SDPA port, timestamped later the same day (`Sun Sep 27 10:28:02 PM UTC 2026` against `Sun Sep 27 10:09:35 PM UTC 2026` for `sarc8`) [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/env.txt, line 1] [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt, line 1], the correctness matrix reports the two dq8ca rank-3 cases as `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32_buffer_texture2d_half (coopmat dispatched), correctness=PASSED` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/correctness.log, lines 283-286 (lines 285-286)], the summary line is `correctness rc=0` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 1-31 (line 3)], and the six production-diff lines read `rc=0 [production-diff] ALL PASSED` [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 1-31 (lines 25-30)].

So the rule the evidence follows is a naming convention: a cooperative-matrix kernel that this harness is to validate carries `coopmat` in its shader name. The hardware condition for the cooperative-matrix path itself is on `hw-cooperative-matrix-rdna3`; no technique page is a remedy for this symptom.

## Telling this case from a real fallback

The same summary line also appears when a non-cooperative-matrix kernel really ran. In the `stock8` run of the same result set, the dq8ca rank-3 cases dispatched `linear_dq8ca_q4gsw_tiled_buffer_texture2d_half_zpint8`, labelled `(NOT coopmat -- fallback)`, and the summary is the same `[correctness] FAILED` line [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/stock8/correctness.log, lines 282-286 (lines 284-286)]. There the label is accurate: that run dispatched release 1.5's tiled kernel in all 24 microbenchmark cases [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/run8.out, lines 1-25 (line 20)].

To tell the two apart, read the kernel name on the case line, not the label:

- a `sarc_linear_dq8ca_zpg_*` name with `correctness=PASSED` is the false failure described here;
- a `linear_dq8ca_q4gsw_tiled_*` name is a real fallback. For reasons a SARC row may not match (unaligned M among them), see `pattern-unaligned-m-fallback`.

The selection layer does not depend on the name in this way: "launch dims come from the row and kernel names are never parsed" [meas-780m-8da4w-port: sarc/SWEEP-PARAMETERS.md, lines 83-87]. Only the test harness reads the substring.

## Not covered by this pattern

- After the rename, the SDPA port's summary still shows `linear 4w rc=1` and `linear 8da4w rc=1` for the microbenchmark steps [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/r4.out, lines 1-31 (lines 4-5)], and the microbenchmark tables carry the dispatch label `unexpected_coopmat` on texture3d rows [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa-e2e/linear-4w.log, lines 153-177 (line 170)]. That label comes from a different branch of the harness [code: backends/vulkan/test/sarc_dev/test_llama_microbench.cpp#L1146-L1149]. The evidence gives no diagnosis or remedy for it, so it is not treated here.
- The SDPA correctness log in the result directory `sdpa` reports `qk_coopmat=NO av_coopmat=NO` and `FAILED` with 0 mismatches [meas-780m-sdpa-port: openspec/changes/sarc-1.5-sdpa-port/results/780m/sdpa/sdpa-correctness.log, lines 1-23 (lines 19-22)]. The evidence does not attribute that to kernel naming.

## Confidence

`source-reported`. The symptom and the result after the rename are log lines taken on the device and cited to the two measurement pages. The cause is the one stated by the proposal and visible in the harness source; the result set does not contain a run that changes only the name while holding the binary otherwise fixed (binaries are identified only by sha256 [meas-780m-8da4w-port: openspec/changes/sarc-1.5-8da4w-port/results/780m/sarc8/env.txt, lines 3-7]).
