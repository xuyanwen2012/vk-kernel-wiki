---
name: vk-kernel-wiki
description: Use when the user asks about optimizing Vulkan GLSL compute-shader kernels for ML inference (cooperative-matrix quantized linear, scaled dot-product attention, tile and subgroup sizing, shared-memory staging) across AMD, Intel, Qualcomm, Arm and NVIDIA GPUs, or wants first-party measurements tied to an exact device, driver version and date. Do NOT use for CUDA-specific kernels or for non-kernel framework integration (model export, graph partitioning, runtime scheduling).
argument-hint: "[natural-language-question] | [--tag foo --type kernel] | [page-id]"
allowed-tools: "Bash Read Grep Glob"
---

# vk-kernel-wiki: Vulkan Compute-Shader Kernel Optimization Wiki

Query a structured, cross-referenced knowledge base about optimizing Vulkan GLSL compute-shader kernels for ML inference across GPU vendors. Run `python3 scripts/repo_status.py` for current corpus counts.

**Corpus status: one measured device.** The corpus holds 590 pages. 18 of them (5 source-measurement, 13 wiki) are for the AMD Radeon 780M on RADV Mesa 25.2.7. The other 572 are upstream pull-request pages from `ggml-org/llama.cpp`, `Tencent/ncnn` and `mesa/mesa`: verbatim excerpts of what upstream wrote, not first-party measurements. See "Current Contents" below before relying on this skill for an answer about any other device or driver.

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
- Free-text keywords are alias-expanded and scored (title, then vocabulary fields, then body).

**Architecture filter semantics.** Architectures form a tree in `data/architectures.yaml` (vendor, generation, device). `--architecture <node>` returns pages tagged with that node or any descendant. It never returns pages tagged only with an ancestor; `query.py` prints on stderr how many such pages were left out and, when any were, which broader node to ask for. Aliases are resolved first and reported on stderr (`780M` and `Phoenix` resolve to `radeon-780m`, `Battlemage` to `xe2`). An unknown value produces a stderr warning and a literal match only.

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

Counts from `python3 scripts/repo_status.py`: 590 pages, of which 577 source pages (5 in `sources/measurements/`, 572 in `sources/prs/`: 405 in `llama-cpp/`, 103 in `ncnn/`, 64 in `mesa/`) and 13 wiki pages (2 hardware, 5 technique, 3 pattern, 3 kernel, 0 language, 0 migration).

- **Measured scope: the AMD Radeon 780M only.** Every measurement and wiki page is tagged with the device node `radeon-780m` and no other node. Nothing in the corpus is measured for another device.
- **Pull-request pages**: 572 upstream pull-request pages generated from three repositories, merged up to 2026-10-05 (`ggml-org/llama.cpp` Vulkan backend: 405; `Tencent/ncnn` Vulkan layers: 103; `mesa/mesa` RADV, ACO and cooperative-matrix lowering: 64), 488 of them with the upstream patches saved under `artifacts/`, listed in `queries/by-repo.md`. Each holds the first 1200 characters of the upstream description (the title where the description is empty) and the changed paths; when `artifact_dir` is set, the upstream patch of that pull request is at `<artifact_dir>/shaders.patch`, or `<artifact_dir>/driver.patch` for Mesa, whose pages hold driver and compiler source instead of shaders (search them with `python3 scripts/grep_wiki.py "<regex>" --only artifacts`). 84 llama.cpp and ncnn pages were included by manual review although they change only backend host source (kernel selection, tile and subgroup tuning, device workarounds); those have no saved patch. The Mesa pages describe the RADV driver that the Radeon 780M measurements ran on, at whatever Mesa version each merge request landed in; check a merge request's date against the measured driver version (RADV Mesa 25.2.7) before assuming it applies to a measurement. Tags are derived mechanically from the title and the changed shader file names, `techniques` is empty on every one, and no wiki page cites them yet. A pull-request page carries an architecture node only where the generator found evidence for one (the title, a device check the pull request adds to the code, or a changed path under a vendor's driver), recorded in `architecture_evidence`; most llama.cpp and ncnn pages carry none, and the Mesa pages are tagged `amd` or `rdna3`. Treat a statement in an excerpt as source-reported by its author for the hardware that author names.
- **Driver and dates as recorded on the pages.** All five measurement pages carry the driver RADV Mesa 25.2.7. Measurement dates: 2026-09-01 (`meas-780m-vulkaninfo`, device-properties export), 2026-09-27 (`meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`) and 2026-09-28 (`meas-780m-e2e-prefill`). For `meas-780m-8da4w-port` and `meas-780m-sdpa-port` the driver version is attributed from the package install history captured on the device on 2026-10-04 (`sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`); the runs themselves record the driver name without a version.
- **Source pages**: `meas-780m-vulkaninfo` (raw file in this repository), `meas-780m-4w-bootstrap` and `meas-780m-e2e-prefill` (raw files in https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae), `meas-780m-8da4w-port` and `meas-780m-sdpa-port` (raw files at the same commit, plus the install-history file in this repository).
- **Hardware pages**: `hw-radeon-780m` (verified), `hw-cooperative-matrix-rdna3` (source-reported; evidence is the 780M only, despite the id).
- **Kernel pages**: `kernel-linear-4w-780m` (verified, 93 performance claims), `kernel-linear-8da4w-780m` (verified, 88 claims from `meas-780m-8da4w-port`, `meas-780m-sdpa-port` and `meas-780m-e2e-prefill`), `kernel-sdpa-prefill-780m` (source-reported, 84 claims from `meas-780m-sdpa-port` and `meas-780m-e2e-prefill`).
- **Technique pages** (all source-reported): `technique-fp32-accumulation`, `technique-drain-in-a-staging`, `technique-workgroup-tile-sizing`, `technique-causal-truncation`, `technique-full-a-map`.
- **Pattern pages** (all source-reported): `pattern-unaligned-m-fallback`, `pattern-sdpa-release-gap`, `pattern-coopmat-name-check-false-failure`.
- **No pages** of type language, migration, doc or blog. The version-claim registry `data/version-claims.yaml` has no claims.
- **Controlled vocabulary** in `data/tags.yaml` and an alias map in `data/aliases.yaml`; **architecture tree** in `data/architectures.yaml`: `amd` (generation `rdna3`), `intel` (generation `xe2`), `nvidia`, `qualcomm`, `arm`, and one reserved vendor node with no devices. Only `radeon-780m` has measurement and wiki pages.
- **Schemas** in `data/schemas.yaml` for six wiki page types and four source page types.
- **Tooling**: `scripts/query.py`, `scripts/get_page.py`, `scripts/grep_wiki.py`, `scripts/generate-indices.py`, `scripts/repo_status.py`, `scripts/validate.py`, `scripts/check_external_locators.py`.

For a question about any device other than the Radeon 780M, or about a driver version or date not listed above, this wiki has no answer; say so.
