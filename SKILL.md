---
name: vk-kernel-wiki
description: Use when the user asks about optimizing Vulkan GLSL compute-shader kernels for ML inference (cooperative-matrix quantized linear, scaled dot-product attention, tile and subgroup sizing, shared-memory staging) across AMD, Intel, Qualcomm, Arm and NVIDIA GPUs, or wants first-party measurements tied to an exact device, driver version and date. Do NOT use for CUDA-specific kernels or for non-kernel framework integration (model export, graph partitioning, runtime scheduling).
argument-hint: "[natural-language-question] | [--tag foo --type kernel] | [page-id]"
allowed-tools: "Bash Read Grep Glob"
---

# vk-kernel-wiki: Vulkan Compute-Shader Kernel Optimization Wiki

Query a structured, cross-referenced knowledge base about optimizing Vulkan GLSL compute-shader kernels for ML inference across GPU vendors. Run `python3 scripts/repo_status.py` for current corpus counts.

**Measured scope is narrow.** Most pages are verbatim excerpts of upstream pull requests, documents and blogs; only a few devices have first-party measurements, and only some of those have kernel and hardware pages. Check coverage before answering: `python3 scripts/repo_status.py` prints corpus counts and measurement pages per device, and `queries/by-device.md` lists each device's measurement pages with driver and date. Each number holds only for the device, driver version and date on its page.

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

## What The Corpus Holds

For live counts run `python3 scripts/repo_status.py`; for what exists per device, repository, technique or problem, read the generated files under `queries/`.

- **Measurement pages** (`sources/measurements/`, `--type measurement`): first-party results, each tagged with one device node and recording the driver name and version and the measurement date. A `raw_data` entry with `repo` and `commit` points at a file in another public repository at that commit.
- **Wiki pages** (`wiki/`): hardware, technique, pattern, kernel, language and migration pages written from the source pages they list in `sources`. Check each page's `architectures` before applying it to a device.
- **Pull-request pages** (`sources/prs/<repo>/`, `--type pr`): the start of the upstream description and the changed paths. When `artifact_dir` is set, the upstream patch is at `<artifact_dir>/shaders.patch` (`driver.patch` for Mesa); search patches with `python3 scripts/grep_wiki.py "<regex>" --only artifacts`. Tags are derived mechanically from the title and file names, and an architecture node is set only where `architecture_evidence` records why. Treat a statement in an excerpt as source-reported by its author, for the hardware that author names.
- **Document and blog pages** (`sources/docs/`, `sources/blogs/`): verbatim excerpts with locators. Only `source_category: official-doc` counts as official-doc evidence for `verified`.
- **Reference kernels** (`artifacts/kernels/<bundle>/`): complete upstream files pinned to a commit, with `PROVENANCE.yaml`. Read these when you need a whole shader rather than a patch.
- **Driver applicability.** A driver merge request describes the driver at whatever release it landed in. Before applying one to a measurement, check its date against the measured driver version. Claims known to depend on the driver version are listed in `data/version-claims.yaml`; say so when you report one of those numbers for a newer driver.
- **Vocabulary and architecture tree**: `data/tags.yaml`, `data/aliases.yaml`, `data/architectures.yaml` (vendor, generation, device). Schemas: `data/schemas.yaml`.
- **Tooling**: `scripts/query.py`, `scripts/get_page.py`, `scripts/grep_wiki.py`, `scripts/generate-indices.py`, `scripts/repo_status.py`, `scripts/validate.py`, `scripts/check_external_locators.py`.

For a device, kernel, driver version or date with no measurement page, this wiki has no measured answer: say so, and present what a document, blog or pull-request page states as source-reported by its author.
