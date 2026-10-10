---
id: pattern-invalid-usage-that-passes-tests
title: "Invalid Vulkan usage that passes every test: unsynchronised shared memory, missing full-subgroups flag, shared memory above the limit"
type: pattern
architectures: [radeon-780m, rx-7600, rx-7900-xtx, arc-b580, rtx-4070-ti-super, jetson-orin]
tags: [memory-model, control-barrier, full-subgroups, subgroup-size, required-subgroup-size, shared-memory-limit, cooperative-matrix, kernel-fusion, sdpa]
confidence: verified
symptoms:
  - all-gates-pass-on-one-driver
  - cross-lane-read-after-memory-barrier-only
  - coopmat-pipeline-without-full-subgroups-flag
  - validation-layer-vuid-10770
  - shared-memory-above-reported-limit
  - nan-output-not-counted-as-mismatch
  - wrong-output-or-hang-on-another-vendor
candidate_techniques: [technique-fused-attention-kernel]
related: [technique-fused-attention-kernel, migration-rdna3-to-xe2, lang-glsl-cooperative-matrix]
sources: [meas-780m-fused-attention, meas-rx7600-fused-attention, meas-7900xtx-fused-attention, meas-b580-fused-port, meas-4070ti-fused-port, meas-orin-fused-port, doc-vk-spec-memory-model, doc-glsl-spec-barrier-functions, doc-glsl-spec-spirv-barrier-mapping, doc-glsl-khr-shader-subgroup, doc-vk-spec-spirvenv-cooperative-matrix-subgroups, doc-vk-spec-shaders-compute-subgroups, doc-vk-spec-limits-compute-subgroup-coopmat, doc-vvl-cooperative-matrix-checks, doc-vvl-subgroup-size-and-shared-memory-checks, pr-llama-cpp-17356, pr-llama-cpp-17887, pr-llama-cpp-18831]
evidence_basis:
  - evidence_type: measurement
    source_id: meas-rx7600-fused-attention
    locator: "results/rx7600/sessions/m2a-sgbarrier/summary.csv, lines 2-8; STATUS.md, lines 69-79"
  - evidence_type: measurement
    source_id: meas-780m-fused-attention
    locator: "proposal.md, lines 766-787 and 825-833"
  - evidence_type: measurement
    source_id: meas-b580-fused-port
    locator: "proposal.md, lines 326-358"
  - evidence_type: official-doc
    source_id: doc-vk-spec-memory-model
    locator: "appendices/memorymodel.adoc, lines 1090-1104"
  - evidence_type: official-doc
    source_id: doc-vk-spec-spirvenv-cooperative-matrix-subgroups
    locator: "appendices/spirvenv.adoc, lines 1782-1790"
---

# Invalid usage that passes every test

**What to do.** Before a new kernel's first gate: (1) read every shared-memory slot for its writer, its readers and the *execution* barrier between them; (2) run one pass under the validation layer; (3) compare declared shared memory with the limit of the driver you are on. A gate that passes on one driver shows that this driver tolerated the shader. It is not evidence that the shader is valid, and it does not carry to the next vendor.

Three cases from the fused-attention campaigns follow. In each, every correctness tier, every next-token check and every timed session passed. Citations use the form `[meas-<id>: <file>, lines]`, files relative to the campaign change directory named in that page's `raw_data`.

## Case 1: a cross-lane read ordered by a memory barrier alone

The first fused attention kernel (`fused3`) let a lane read shared slots other lanes of its subgroup had written, with only `memoryBarrierShared()` between the store and the load. It was found by reading the shader during a port, not by a test: "a lane reads slots that other lanes of the same subgroup wrote, ordered only by `memoryBarrierShared()`, without `subgroupBarrier()` ... on RDNA3 (one wave, no divergent branch between the write and the read) it is benign, and every correctness pass agrees" [meas-rx7600-fused-attention: STATUS.md, lines 72-76].

Why the tests could not see it: the workgroup is one subgroup, and on that hardware the subgroup is one wave that executes each instruction for all its lanes before the next, so every store ran before any load. "That is how a wave executes, not something the API promises" [meas-780m-fused-attention: proposal.md, lines 781-787].

Why it is invalid:

| Call | What it gives | Source |
|---|---|---|
| `memoryBarrierShared()` | maps to `OpMemoryBarrier`: no execution scope. It orders the calling invocation's own stores as others observe them; a store is visible to a *future* access, and an access is future only "if a _happens-before_ relation can be established" | [doc-glsl-spec-spirv-barrier-mapping: chapters/spirvmappings.adoc, lines 648-675] [doc-glsl-spec-barrier-functions: chapters/builtinfunctions.adoc, lines 3518-3530 and 3532-3543] |
| `subgroupBarrier()` | `OpControlBarrier` with execution and memory scope Subgroup: all active invocations of the subgroup execute it before any continues | [doc-glsl-khr-shader-subgroup: GL_KHR_shader_subgroup.txt, lines 115-118 and 701-706] |
| `barrier()` | `OpControlBarrier` with execution and memory scope Workgroup; synchronizes accesses to `shared` variables | [doc-glsl-spec-spirv-barrier-mapping: chapters/spirvmappings.adoc, lines 648-675] [doc-glsl-spec-barrier-functions: chapters/builtinfunctions.adoc, lines 3471-3476] |

A release and an acquire in different invocations synchronize through a control barrier in whose execution scope both lie (the memory model also defines synchronization through atomic operations, which these kernels do not use for the exchange) [doc-vk-spec-memory-model: appendices/memorymodel.adoc, lines 556-569]; without such synchronization the write and the read are a data race, and "Applications must: ensure that no data races occur" [doc-vk-spec-memory-model: appendices/memorymodel.adoc, lines 1090-1104].

The repair and its cost: `subgroupBarrier()` after every `memoryBarrierShared()`. Radeon RX 7600, RADV Mesa 26.2.3, 2026-10-08: +0.00 % geomean, SDPA output byte-identical in 21 of 21 cases [meas-rx7600-fused-attention: results/rx7600/sessions/m2a-sgbarrier/summary.csv, line 8; sdpa-error/bitwise.txt, lines 1-21]. Radeon 780M, RADV Mesa 25.2.7, 2026-10-09: -0.14 % geomean, inside the band, output byte-identical [meas-780m-fused-attention: proposal.md, lines 833 and 900-901]. On lockstep hardware the barrier was free; every later port carries it, and the multi-subgroup port uses `barrier()` because slots cross subgroups [meas-b580-fused-port: proposal.md, line 101].

Independent instance: llama.cpp added a `barrier()` with the comment "prevent race on tmpsh" to its scalar and cooperative-matrix flash-attention shaders (`artifacts/prs/llama-cpp/PR-17887/shaders.patch`, lines 8-9 and 21-22) [pr-llama-cpp-17887]. An Intel failure had first been worked around by forcing full subgroups [pr-llama-cpp-17356: excerpt]; that was reverted once "the actual root cause" was attributed to the race fix [pr-llama-cpp-18831: excerpt]. The same shader ran elsewhere before either change.

## Case 2: cooperative-matrix pipelines without the full-subgroups flag

The rule: "Any pipeline containing a shader with OpTypeCooperativeMatrixKHR or OpCooperativeMatrix*KHR instructions must: be created with the VK_PIPELINE_SHADER_STAGE_CREATE_REQUIRE_FULL_SUBGROUPS_BIT flag or the shader module must be version 1.6 or greater" [doc-vk-spec-spirvenv-cooperative-matrix-subgroups: appendices/spirvenv.adoc, lines 1782-1790]. The flag is what guarantees that subgroups launch "with all invocations active" [doc-vk-spec-shaders-compute-subgroups: chapters/shaders.adoc, lines 1980-2009].

What the campaigns had: SPIR-V 1.3, a Vulkan 1.1 instance and stage `flags` 0 for every compute stage, so neither alternative held; the record says this applies to every cooperative-matrix pipeline of every device, the shipped ones included [meas-b580-fused-port: proposal.md, lines 330-342]. All gates passed on ANV Mesa 26.2.3, NVIDIA 615.71.09 and 595.78, RADV Mesa 25.2.7 and 26.2.3.

A run-time guard is not validity. The Intel and NVIDIA kernels check `gl_NumSubgroups` and `gl_SubgroupSize` and write nothing (or NaN rows) otherwise. The records say what that does not do: "It does not make the pipeline valid, it does not cover the parent's and the shipped kernels" [meas-b580-fused-port: proposal.md, lines 343-346]; "it does not guarantee that all 32 invocations of the one subgroup are active (that is what the flag specifies)" [meas-orin-fused-port: proposal.md, lines 147-149]. On the Orin the guard "never fired" [meas-orin-fused-port: proposal.md, lines 145-146]: the driver was permissive, and the test suite cannot tell permissive from guaranteed.

A test blind spot found on the way: the guard's NaN rows "are not counted by the correctness test's mismatch counter (a NaN comparison is false)" [meas-b580-fused-port: proposal.md, lines 346-348]. A gate that counts mismatches needs a separate finite-output check.

## Case 3: more workgroup memory than the driver reports

On the Radeon RX 7900 XTX, AMDVLK 2025.Q2.1 (campaign of 2026-10-08), the driver reports `maxComputeSharedMemorySize` = 32,768 bytes while kernels in use declare 40,960 to 61,440 bytes; "the driver accepts these pipelines and every correctness gate passes, but it breaks a Vulkan valid-usage rule" [meas-7900xtx-fused-attention: proposal.md, lines 292-295]. The limit is the total storage available to `shared` variables [doc-vk-spec-limits-compute-subgroup-coopmat: chapters/limits.adoc, lines 499-503]. The kernels were sized on other drivers; the limit is per driver, not per GPU model.

## How to detect each

| Defect | Validation layer | By reading |
|---|---|---|
| Missing full-subgroups flag | Reported as VUID-RuntimeSpirv-OpTypeCooperativeMatrixKHR-10770 when the module has cooperative-matrix instructions, the API version is below 1.3 and the stage does not require full subgroups [doc-vvl-cooperative-matrix-checks: cc_spirv_cooperative.cpp, lines 219-230] | stage `flags`, SPIR-V version, instance API version |
| Shared memory above the limit | Reported as VUID-RuntimeSpirv-Workgroup-06530 [doc-vvl-subgroup-size-and-shared-memory-checks: cc_spirv.cpp, lines 463-475] | sum the `shared` declarations per variant against the limit of each target driver |
| Data race on shared memory | **Not detected** by the pipeline-creation checks cited here; no test caught it on lockstep hardware either | per slot: who writes, who reads, which control barrier lies between, and whether that barrier's scope covers both; and whether every barrier sits in control flow uniform for that scope |

The reading that the ports used is a table with one row per shared slot: writer, reader, "what orders the read after the write" [meas-b580-fused-port: STATUS.md, lines 611-619] [meas-4070ti-fused-port: proposal.md, lines 125-132]. Write that table before the gate, and have the reviewer redo it.

## What this does not show

- No failing run exists in these sources for cases 2 and 3: they are valid-usage violations with no observed wrong output on the drivers named.
- The cost of the full-subgroups flag is published only as a note without raw data for one device (see `technique-fused-attention-kernel`, "What this does not show"); no figure is recorded here.
- Whether staying inside the AMDVLK shared-memory limit changes timing was not measured.
- The validation-layer rows quote the layer's source at one commit; they were not run by this wiki.
