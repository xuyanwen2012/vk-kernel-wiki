---
name: vk-kernel-wiki
description: Use when the user asks about optimizing Vulkan GLSL compute-shader kernels for ML inference (cooperative-matrix quantized linear, scaled dot-product attention, tile and subgroup sizing, shared-memory staging) across AMD, Intel, Qualcomm, Arm and NVIDIA GPUs, or wants first-party measurements tied to an exact device, driver version and date. Do NOT use for CUDA-specific kernels or for non-kernel framework integration (model export, graph partitioning, runtime scheduling).
argument-hint: "[natural-language-question] | [--tag foo --type kernel] | [page-id]"
allowed-tools: "Bash Read Grep Glob"
---

# vk-kernel-wiki: Vulkan Compute-Shader Kernel Optimization Wiki

Query a structured, cross-referenced knowledge base about optimizing Vulkan GLSL compute-shader kernels for ML inference across GPU vendors. Run `python3 scripts/repo_status.py` for current corpus counts.

**Corpus status: one measured device.** The corpus holds 801 pages. 18 of them (5 source-measurement, 13 wiki) are for the AMD Radeon 780M on RADV Mesa 25.2.7; they are the only first-party measurements and the only pages written from them. The other 783 are 1 language page, 58 document pages, 11 blog pages and 713 upstream pull-request pages from `ggml-org/llama.cpp`, `mesa/mesa`, `Tencent/ncnn`, `alibaba/MNN`, `jeffbolznv/vk_cooperative_matrix_perf`, `KhronosGroup/glslang` and `KhronosGroup/SPIRV-Tools`. These sources span more vendors (Khronos, AMD, Intel, NVIDIA, Qualcomm and Arm material), but they are verbatim excerpts of what their authors wrote, not first-party measurements. See "Current Contents" below before relying on this skill for a measured answer about any other device or driver.

## When To Use This Skill

Trigger this skill when the user asks about:

- **Cooperative-matrix kernels in GLSL**: `GL_KHR_cooperative_matrix`, the shapes a device exposes, accumulator precision
- **Quantized linear kernels**: 4-bit weight and dynamic int8 activation variants, GEMM and GEMV shapes
- **Scaled dot-product attention kernels**: Q K^T, softmax, attention times V
- **Kernel tuning parameters**: workgroup tile sizes, subgroup grid, required subgroup size, shared-memory staging and output drain
- **Cross-vendor differences**: which device or driver a technique or number applies to
- **First-party measurements**: numbers tied to an exact device, driver version and date

Do NOT use this skill for:

- CUDA-specific kernels or any non-Vulkan GPU programming model
- Non-kernel framework integration (model export, delegate partitioning, graph scheduling, runtime memory planning)
- Generic Vulkan API usage that is not about compute-shader kernel performance

## How To Query

All commands run from the skill directory (the directory this `SKILL.md` lives in). The scripts resolve the wiki root on their own; no environment variable is required. Set `VK_KERNEL_WIKI_ROOT` only to point the scripts at a different root.

### Runtime dependencies

None beyond Python 3. The scripts use the host PyYAML package when it is present and fall back to the bundled pure-Python loader in `scripts/_vendor/` otherwise, so they also run under `python3 -S` and without network access.

### Path 1: Unified search (preferred for natural language)

```bash
python3 scripts/query.py "cooperative matrix quantized linear"
python3 scripts/query.py --tag cooperative-matrix --type kernel
python3 scripts/query.py --architecture rdna3 --compact
python3 scripts/query.py --architecture 780M --type measurement
```

Filters: `--type`, `--tag`, `--repo`, `--language`, `--architecture`, `--symptom`, `--confidence`, `--limit` (default 10), `--compact`, `--paths-only`.

- `--type` takes one of `kernel`, `technique`, `hardware`, `pattern`, `language`, `migration`, `pr`, `doc`, `blog`, `measurement`.
- `--tag` matches a term in any of `tags`, `techniques`, `hardware_features`, `kernel_types`, `languages`, and accepts aliases from `data/aliases.yaml` (`--tag coopmat` matches `cooperative-matrix`).
- `--language` and `--symptom` are exact matches and do not resolve aliases.
- A free-text keyword that is an alias (alone or as part of a multi-word alias such as `matrix cores`) also matches pages carrying its canonical term, but below pages that use the spelling you typed: `DPAS`, `XMX`, `WMMA` and `wave32` rank the pages that name them first, then the pages only tagged `cooperative-matrix` or `subgroup-size`. With `--tag`, an alias is exactly its canonical term.
- Free-text keywords are ranked; every matching page is returned and only the order is decided: pages matching all the keywords come before partial matches (function words such as `on`, `the`, `for` are not counted); then a keyword in the title or id outweighs one in a vocabulary field, which outweighs one in the body; then, when the query names an architecture node (as a keyword or with `--architecture`), pages tagged only with that vendor come before pages that list it among other vendors or only mention it; then wiki pages come before measurement, document and blog pages, which come before pull-request pages.

**Architecture filter semantics.** Architectures form a tree in `data/architectures.yaml` (vendor, generation, device). `--architecture <node>` returns pages tagged with that node or any descendant. It never returns pages tagged only with an ancestor; `query.py` prints on stderr how many such pages were left out and, when any were, which broader node to ask for. Aliases are resolved first and reported on stderr (`780M` and `Phoenix` resolve to `radeon-780m`, `Battlemage` to `xe2`). An unknown value produces a stderr warning and a literal match only. A vendor or device named as a free-text keyword (`"GEMM on Intel Arc"`) is not a filter; when any of the first five results is tagged only with another architecture, `query.py` prints a one-line `WARNING` on stderr naming those architectures. Treat such a result as evidence for the device it is tagged with, and use `--architecture` to drop it.

### Path 2: Fetch a specific page by id or path

```bash
python3 scripts/get_page.py <page-id>
python3 scripts/get_page.py <page-id> --follow-sources
python3 scripts/get_page.py <page-id> --body-only
python3 scripts/get_page.py <page-id> --frontmatter-only
python3 scripts/get_page.py wiki/kernels/<file>.md
```

Exits with code 1 and an error on stderr when the page does not exist. `--follow-sources` appends a 500-character excerpt of each page listed in `sources`.

### Path 3: Regex text search across wiki and source bodies

```bash
python3 scripts/grep_wiki.py "coopMatMulAdd" --only wiki
python3 scripts/grep_wiki.py "subgroup" "64" --context 2
python3 scripts/grep_wiki.py "RADV" "ANV" --any --files-only
python3 scripts/grep_wiki.py "shader_time" --only sources --ext json,csv
```

Several patterns must all match the same line unless `--any` is given. Other flags: `--only wiki|sources|all` (default `all`), `--context N` (default 1), `--limit N` (default 20 files), `--files-only`, `--ext` (extra file extensions besides `.md`).

### Path 4: Generated cross-reference indices

`python3 scripts/generate-indices.py` writes these files under `queries/`:

- `queries/by-architecture.md`: one section per tree node, listing pages tagged exactly with that node
- `queries/by-device.md`: measurement pages per device node, with driver and measurement date, newest first
- `queries/by-problem.md`: symptom, pattern page, candidate techniques
- `queries/by-technique.md`: technique pages
- `queries/by-hardware-feature.md`: hardware feature terms and the pages that carry them
- `queries/by-kernel-type.md`: kernel type terms and the pages that carry them
- `queries/by-language.md`: language terms and the pages that carry them
- `queries/by-repo.md`: PR pages grouped by source repository

A table with no matching page holds a single `_None_` row. The generated files are committed; rerun the generator after every content change.

### Path 5: Primer, schema, examples

- `references/primer.md`: topic map organised by the controlled vocabulary and the architecture tree. Read this first when the question is broad.
- `references/schema.md`: condensed frontmatter schema, confidence rule, reproducibility levels.
- `references/examples.md`: worked query patterns (question to command sequence).
- `references/authoring.md`: how to add a measurement source page and a wiki page that cites it.

## Output Pattern

When answering from this knowledge base:

1. **Cite specific pages** by id and path (`<page-id>`, `wiki/kernels/<file>.md`).
2. **Follow `sources`** to trace each claim back to a measurement, PR, doc or blog source page. Source page bodies hold verbatim excerpts and locators; quote them rather than paraphrasing them into something stronger. A measurement page's `raw_data` entry either names a file in this repository (`locator` only) or a file in another git repository (`repo`, `commit` and a `locator` relative to that repository's root); in the second case the raw file is read from that repository at that commit, not from this one.
3. **Respect confidence levels**: `verified` > `source-reported` > `inferred` > `experimental`. Say so when a claim is `inferred` or `experimental`.
4. **Report performance claims with all required fields**: `gpu`, `driver` (name and version), `dtype`, `shape`, `metric`, `value`, `measured_at`, `source_id`, `source_locator`. Never drop the driver or the date: a number is only meaningful for that device, that driver version and that day. Include `baseline` when the claim has one.
5. **Do not transfer numbers across devices.** A page tagged with one device says nothing measured about a sibling device or about the parent generation.
6. **Say when the wiki has no answer.** If a query returns `No matching pages.`, report that the wiki does not cover the topic; do not fill the gap from memory while attributing it to this wiki.

## Current Contents

Counts from `python3 scripts/repo_status.py`: 801 pages, of which 787 source pages (5 in `sources/measurements/`, 713 in `sources/prs/`: 405 in `llama-cpp/`, 169 in `mesa/`, 103 in `ncnn/`, 10 in `mnn/`, 10 in `vk-coopmat-perf/`, 8 in `glslang/`, 8 in `spirv-tools/`; 58 in `sources/docs/`; 11 in `sources/blogs/`) and 14 wiki pages (2 hardware, 5 technique, 3 pattern, 3 kernel, 1 language, 0 migration).

- **Measured scope: the AMD Radeon 780M only.** Every measurement page and every hardware, technique, pattern and kernel page is tagged with the device node `radeon-780m` and no other node. Nothing in the corpus is measured for another device. Document, blog and pull-request pages now cover AMD, Intel, NVIDIA, Qualcomm and Arm hardware, but only as what an upstream author, vendor or specification states.
- **Pull-request pages**: 713 upstream pull-request pages generated from seven repositories (`ggml-org/llama.cpp` Vulkan backend: 405 and `Tencent/ncnn` Vulkan layers: 103, both merged up to 2026-10-05; `mesa/mesa` Vulkan drivers and compilers, RADV / ACO, ANV, NVK / NAK, Turnip / ir3 and Panvk, with the common cooperative-matrix lowering: 169; `alibaba/MNN` Vulkan backend: 10; `jeffbolznv/vk_cooperative_matrix_perf`, NVIDIA's cooperative-matrix benchmark: 10; `KhronosGroup/glslang`: 8; `KhronosGroup/SPIRV-Tools`: 8; these five searched up to 2026-10-10), 607 of them with the upstream patches saved under `artifacts/`, listed in `queries/by-repo.md`. Each holds the first 1200 characters of the upstream description (the title where the description is empty) and the changed paths; when `artifact_dir` is set, the upstream patch of that pull request is at `<artifact_dir>/shaders.patch`, or `<artifact_dir>/driver.patch` for Mesa, whose pages hold driver and compiler source instead of shaders (search them with `python3 scripts/grep_wiki.py "<regex>" --only artifacts`). 106 pages have no saved patch: 84 llama.cpp and ncnn pages, 5 vk_cooperative_matrix_perf pages and 1 MNN page that change only host source (kernel selection, tile and subgroup tuning, device workarounds, a benchmark) and were included by manual review, and the 16 glslang and SPIRV-Tools pages, which carry the description excerpt only. The RADV and ACO Mesa pages describe the driver that the Radeon 780M measurements ran on, at whatever Mesa version each merge request landed in; check a merge request's date against the measured driver version (RADV Mesa 25.2.7) before assuming it applies to a measurement. The ANV, NVK, Turnip and Panvk pages describe drivers that no measurement in this wiki ran on. Tags are derived mechanically from the title and the changed shader file names; `techniques` is filled on 140 of them and only with terms the title or a file name states outright. A pull-request page carries an architecture node only where the generator found evidence for one (the title, a device check the pull request adds to the code, or a changed path under a vendor's driver), recorded in `architecture_evidence`; most llama.cpp and ncnn pages carry none, and 161 of the 169 Mesa pages carry the vendor of the driver they change (`amd`, `intel`, `nvidia`, `qualcomm`, `arm`) or a generation named in the title. Treat a statement in an excerpt as source-reported by its author for the hardware that author names.
- **Driver and dates as recorded on the pages.** All five measurement pages carry the driver RADV Mesa 25.2.7. Measurement dates: 2026-09-01 (`meas-780m-vulkaninfo`, device-properties export), 2026-09-27 (`meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`) and 2026-09-28 (`meas-780m-e2e-prefill`). For `meas-780m-8da4w-port` and `meas-780m-sdpa-port` the driver version is attributed from the package install history captured on the device on 2026-10-04 (`sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`); the runs themselves record the driver name without a version.
- **Source pages**: `meas-780m-vulkaninfo` (raw file in this repository), `meas-780m-4w-bootstrap` and `meas-780m-e2e-prefill` (raw files in https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae), `meas-780m-8da4w-port` and `meas-780m-sdpa-port` (raw files at the same commit, plus the install-history file in this repository).
- **Hardware pages**: `hw-radeon-780m` (verified), `hw-cooperative-matrix-rdna3` (source-reported; evidence is the 780M only, despite the id).
- **Kernel pages**: `kernel-linear-4w-780m` (verified, 93 performance claims), `kernel-linear-8da4w-780m` (verified, 88 claims from `meas-780m-8da4w-port`, `meas-780m-sdpa-port` and `meas-780m-e2e-prefill`), `kernel-sdpa-prefill-780m` (source-reported, 84 claims from `meas-780m-sdpa-port` and `meas-780m-e2e-prefill`).
- **Technique pages** (all source-reported): `technique-fp32-accumulation`, `technique-drain-in-a-staging`, `technique-workgroup-tile-sizing`, `technique-causal-truncation`, `technique-full-a-map`.
- **Pattern pages** (all source-reported): `pattern-unaligned-m-fallback`, `pattern-sdpa-release-gap`, `pattern-coopmat-name-check-false-failure`.
- **Document pages** (58, by `source_category`): official documents (`official-doc`, the only category that counts as official-doc evidence for `verified`): `doc-glsl-khr-cooperative-matrix`, `doc-glsl-khr-shader-subgroup`, `doc-glsl-spec-barrier-functions`, `doc-glsl-spec-shared-variables`, `doc-glsl-spec-spirv-barrier-mapping`, `doc-intel-igc-visa-dpas`, `doc-mesa-features-vulkan-compute`, `doc-mesa-radv-envvars`, `doc-mesa-relnotes-19-1-0`, `doc-mesa-relnotes-21-1-0`, `doc-mesa-relnotes-23-3-0`, `doc-mesa-relnotes-25-0-0`, `doc-mesa-relnotes-25-1-0`, `doc-mesa-relnotes-25-2-0`, `doc-mesa-relnotes-26-2-0`, `doc-mesa-relnotes-new-features`, `doc-nvidia-vulkan-beta-driver-release-notes`, `doc-vk-ext-cooperative-matrix-maintenance1-proposal`, `doc-vk-ext-shader-split-barrier-proposal`, `doc-vk-ext-subgroup-size-control`, `doc-vk-khr-cooperative-matrix-proposal`, `doc-vk-nv-cooperative-matrix-decode-vector-proposal`, `doc-vk-nv-cooperative-matrix2-extension`, `doc-vk-nv-cooperative-matrix2-proposal`, `doc-vk-qcom-cooperative-matrix-conversion-proposal`, `doc-vk-spec-cooperative-matrix-properties`, `doc-vk-spec-features-subgroup-coopmat`, `doc-vk-spec-limits-compute-subgroup-coopmat`, `doc-vk-spec-memory-model`, `doc-vk-spec-pipeline-shader-stage-subgroup-flags`, `doc-vk-spec-shaders-compute-subgroups`, `doc-vk-spec-spirvenv-cooperative-matrix-subgroups`, `doc-vk-spec-subgroup-builtins`, `doc-vulkan-guide-subgroups`; other projects' source files (`upstream-code`): `doc-arm-libgpucounters-shader-core-counters`, `doc-cubek-matmul`, `doc-onnxruntime-webgpu-matmul-nbits`, `doc-qualcomm-adreno-cooperative-matrix-sample`, `doc-vk-gl-cts-cooperative-matrix-tests`, `doc-vk-gl-cts-subgroup-size-control-tests`, `doc-vvl-cooperative-matrix-checks`, `doc-vvl-subgroup-size-and-shared-memory-checks`, `doc-wonnx-gemm-template`; vendor and project articles and guides (`vendor-doc`): `doc-amd-rdna-performance-guide`, `doc-amd-rdna3-beyond-the-current-gen`, `doc-gpuopen-matrix-cores-rdna4`, `doc-gpuopen-wmma-on-rdna3`, `doc-intel-oneapi-gpu-guide-joint-matrix`, `doc-intel-oneapi-gpu-guide-xmx`, `doc-iree-vulkan-deployment-guide`, `doc-iree-vulkanised-2025-spirv-talk`, `doc-mnn-release-3-4-0`, `doc-mnn-release-3-4-1`, `doc-mnn-release-3-6-0`, `doc-mnn-vulkan-optimization-handbook`, `doc-nvidia-vulkanised-2025-cooperative-matrix2`, `doc-tvm-vulkan-runtime`; paper: `doc-webllm-paper`. **Blog pages** (11): `blog-glslang-issue-3929-bfloat16-coopmat-elementwise`, `blog-glslang-issue-3948-small-index-types`, `blog-llama-cpp-discussion-13530-intel-xe2-coopmat`, `blog-llama-cpp-issue-22034-intel-device-lost`, `blog-mlc-amd-gpus-llm-inference`, `blog-nvidia-vulkan-cooperative-matrices-2019`, `blog-shaderc-issue-1594-coopmat2-optimizer-capability`, `blog-spirv-tools-issue-6077-coopmat-bitwise-ops`, `blog-spirv-tools-issue-6410-coopmat-load-through-array`, `blog-themaister-fsr4-wmma`, `blog-zolotukhin-matrix-cores-decode`. All hold verbatim excerpts with locators. `doc-mnn-vulkan-optimization-handbook` quotes a document written in Chinese.
- **Language page**: `lang-glsl-cooperative-matrix` (what the GLSL extension specifies, and one upstream int8 cooperative-matrix shader quoted from a pinned file). **No pages** of type migration.
- **Reference kernels**: complete upstream files pinned to a commit under `artifacts/kernels/`, 10 bundles (`llama-cpp-matmul`, `llama-cpp-flash-attention`, `ncnn-gemm-coopmat`, `mesa-radv-coopmat`, `mnn-coopmat-conv1x1`, `mnn-lowbit-gemv-gemm`, `mnn-attention`, `mnn-vulkan-optimize-notes`, `vk-coopmat-perf-gemm`, `adreno-cooperative-matrix-sample`). Read these when you need a whole shader rather than a patch.
- **Version-sensitive claim**: `vs-radv-coopmat-lowering-after-25-2-7` in `data/version-claims.yaml`. The three kernel pages and `hw-cooperative-matrix-rdna3` rest on measurements taken on RADV Mesa 25.2.7; 23 cooperative-matrix merge requests in the corpus are not contained in that release (membership was checked on 2026-10-06 for the 64 RADV / ACO merge requests present then; the 105 Mesa merge requests added on 2026-10-10 are unchecked). Say so when you report one of those numbers for a newer driver.
- **Controlled vocabulary** in `data/tags.yaml` and an alias map in `data/aliases.yaml`; **architecture tree** in `data/architectures.yaml`: 28 nodes (6 vendor, 10 generation, 12 device): `amd` (generations `rdna3`, `rdna4`), `intel` (generations `xe2`, `meteor-lake`, `xe3`), `nvidia` (generations `turing`, `ampere`, `blackwell`), `qualcomm` (generation `adreno-7xx`), `arm` (generation `bifrost`), and one reserved vendor node with no devices. Only `radeon-780m` has measurement, hardware, technique, pattern and kernel pages.
- **Schemas** in `data/schemas.yaml` for six wiki page types and four source page types.
- **Tooling**: `scripts/query.py`, `scripts/get_page.py`, `scripts/grep_wiki.py`, `scripts/generate-indices.py`, `scripts/repo_status.py`, `scripts/validate.py`, `scripts/check_external_locators.py`.

For a question about any device other than the Radeon 780M, or about a driver version or date not listed above, this wiki has no measured answer; say so, and present what a document, blog or pull-request page states as source-reported by its author.
