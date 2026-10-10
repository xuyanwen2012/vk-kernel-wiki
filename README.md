# vk-kernel-wiki

A structured knowledge base about optimizing Vulkan GLSL compute-shader kernels for ML inference (cooperative-matrix quantized linear, scaled dot-product attention) across GPU vendors, packaged as a Claude Code skill. The repository root is the skill directory.

> **Status: current contents.** 801 pages: 5 source-measurement pages, 58 document pages (34 official documents: Khronos Vulkan, GLSL and Vulkan Guide specification text and extension proposals, the Intel DPAS instruction specification, Mesa documentation and release notes, NVIDIA driver release notes; 9 pages quoting other projects' source files, tests and code samples; 14 vendor and project articles, guides, slide decks and framework release notes; 1 paper), 11 blog pages (benchmark posts, write-ups and upstream issue threads), 713 upstream pull-request pages generated from seven repositories (`ggml-org/llama.cpp` Vulkan backend: 405 and `Tencent/ncnn` Vulkan layers: 103, both merged up to 2026-10-05; `mesa/mesa` Vulkan drivers and compilers, RADV / ACO, ANV, NVK / NAK, Turnip / ir3 and Panvk, with the common cooperative-matrix lowering: 169; `alibaba/MNN` Vulkan backend: 10; `jeffbolznv/vk_cooperative_matrix_perf`, NVIDIA's cooperative-matrix benchmark: 10; `KhronosGroup/glslang`: 8; `KhronosGroup/SPIRV-Tools`: 8; these five searched up to 2026-10-10), 607 of them with the upstream patches saved under `artifacts/`, and 14 wiki pages (2 hardware, 5 technique, 3 pattern, 3 kernel, 1 language). First-party measurements cover one device only: the AMD Radeon 780M (device node `radeon-780m`), driver RADV Mesa 25.2.7, with measurement dates 2026-09-01 (device-properties export), 2026-09-27 and 2026-09-28 as recorded on the pages; the hardware, technique, pattern and kernel pages are written from those measurements. No other device has a measurement or a hardware, technique, pattern or kernel page. The other sources now span more vendors: document, blog and pull-request pages quote Khronos, AMD, Intel, NVIDIA, Qualcomm and Arm material and carry nodes of all five vendors, but they are verbatim excerpts of what their authors wrote, not measurements made for this wiki. A pull-request page carries an architecture node only where the generator found evidence for one (the title, a device check the pull request adds to the code, or a changed path under a vendor's driver), recorded in `architecture_evidence`; most llama.cpp and ncnn pages carry none, and 161 of the 169 Mesa pages carry the vendor of the driver they change (`amd`, `intel`, `nvidia`, `qualcomm`, `arm`) or a generation named in the title.

## Install as a Claude Code Skill

Place a clone or copy of this repository at `~/.claude/skills/vk-kernel-wiki`. `SKILL.md` lives at the root, so the skill registers itself, and the scripts resolve the wiki root to their own repository. No environment variable and no Python package is required: the scripts prefer a host PyYAML installation and fall back to the bundled pure-Python loader, including under `python3 -S` and offline.

Smoke test:

```bash
cd ~/.claude/skills/vk-kernel-wiki
python3 scripts/repo_status.py
python3 scripts/query.py --architecture rdna3 --compact
```

`repo_status.py` reports 801 indexed pages (787 source, 14 wiki), and the query lists the pages tagged `rdna3` or one of its devices.

Optional override to point the scripts at another wiki root (a directory containing `data/tags.yaml`):

```bash
export VK_KERNEL_WIKI_ROOT=/path/to/another/root
```

## What's Here

- Page schemas for six wiki page types and four source page types, including first-party measurement pages ([`data/schemas.yaml`](data/schemas.yaml)).
- A controlled vocabulary ([`data/tags.yaml`](data/tags.yaml)) and alias map ([`data/aliases.yaml`](data/aliases.yaml)).
- A data-driven architecture tree of vendors, generations and devices ([`data/architectures.yaml`](data/architectures.yaml)).
- A version-claim registry ([`data/version-claims.yaml`](data/version-claims.yaml)) with one claim: the 780M pages were measured on RADV Mesa 25.2.7, and 23 later cooperative-matrix merge requests are not in that release ([`data/release-membership.yaml`](data/release-membership.yaml)).
- Ten reference bundles of complete upstream kernel files pinned to a commit ([`artifacts/kernels/`](artifacts/README.md)): llama.cpp matmul and flash attention shaders, ncnn cooperative-matrix shaders, Mesa's RADV cooperative-matrix lowering, MNN's cooperative-matrix Conv1x1, low-bit GEMV / GEMM and attention shaders with its optimization notes, NVIDIA's cooperative-matrix benchmark, and Qualcomm's Adreno cooperative-matrix sample.
- Query, validation and index-generation scripts.
- 18 knowledge pages for the AMD Radeon 780M on RADV Mesa 25.2.7: 5 first-party measurement source pages and 13 wiki pages (2 hardware, 5 technique, 3 pattern, 3 kernel). See [`index.md`](index.md).
- 713 upstream pull-request pages generated from seven repositories (`ggml-org/llama.cpp` Vulkan backend: 405 and `Tencent/ncnn` Vulkan layers: 103, both merged up to 2026-10-05; `mesa/mesa` Vulkan drivers and compilers, RADV / ACO, ANV, NVK / NAK, Turnip / ir3 and Panvk, with the common cooperative-matrix lowering: 169; `alibaba/MNN` Vulkan backend: 10; `jeffbolznv/vk_cooperative_matrix_perf`, NVIDIA's cooperative-matrix benchmark: 10; `KhronosGroup/glslang`: 8; `KhronosGroup/SPIRV-Tools`: 8; these five searched up to 2026-10-10), 607 of them with the upstream patches saved under `artifacts/`. See [`queries/by-repo.md`](queries/by-repo.md).
- 58 document pages (34 official documents: Khronos Vulkan, GLSL and Vulkan Guide specification text and extension proposals, the Intel DPAS instruction specification, Mesa documentation and release notes, NVIDIA driver release notes; 9 pages quoting other projects' source files, tests and code samples; 14 vendor and project articles, guides, slide decks and framework release notes; 1 paper), 11 blog pages (benchmark posts, write-ups and upstream issue threads), all holding verbatim excerpts with locators. See [`index.md`](index.md).
- A pull-request intake pipeline: candidate ledgers in [`candidates/`](candidates/README.md), a decision policy, a page generator, and verbatim upstream shader patches with provenance in [`artifacts/`](artifacts/README.md).

## Query Tools

All tools run from the repository root.

| Tool | Purpose |
|---|---|
| `scripts/query.py` | Unified search across source and wiki pages (keywords, filters, alias-aware, architecture-tree aware) |
| `scripts/get_page.py` | Fetch a page by `id` or path; `--follow-sources` appends excerpts of cited sources |
| `scripts/grep_wiki.py` | Regex text search across wiki and source files |

```bash
python3 scripts/query.py "cooperative matrix quantized linear" --limit 5
python3 scripts/query.py --tag coopmat --type hardware --compact     # alias of cooperative-matrix
python3 scripts/query.py --architecture 780M --type measurement      # alias of radeon-780m
python3 scripts/get_page.py <page-id> --follow-sources
python3 scripts/grep_wiki.py "coopMatMulAdd" --only wiki
```

Architecture filters follow the tree: asking for a node returns pages tagged with that node or any of its descendants, and never pages tagged only with an ancestor. `query.py` reports on stderr how many ancestor-only pages were left out.

## Companion Docs

- [`SKILL.md`](SKILL.md): skill entry point. When to engage, how to query, output contract.
- [`CLAUDE.md`](CLAUDE.md): schema and authoring rules for agents editing this repository.
- [`references/primer.md`](references/primer.md): topic map organised by the vocabulary and the architecture tree.
- [`references/schema.md`](references/schema.md): frontmatter schema with one synthetic example per page type.
- [`references/examples.md`](references/examples.md): worked query patterns.
- [`references/authoring.md`](references/authoring.md): how to add a measurement source page and a wiki page that cites it.
- [`index.md`](index.md): curated top-level navigation.
- [`NOTICE.md`](NOTICE.md): attribution and third-party licenses.

## Architecture

Three layers:

1. **`sources/`**: raw evidence. First-party measurements, upstream PRs, docs and blogs. Bodies hold verbatim excerpts and locators only, never model-written summaries.
2. **`wiki/`**: synthesized knowledge pages, cross-referenced by `id`, each citing source pages.
3. **`queries/`**: generated cross-reference indices, committed to the repository. Do not edit by hand; regenerate with `scripts/generate-indices.py` after every content change.

Rules that shape the content:

- Every number is traceable to a source page through an exact locator.
- Every measurement carries the exact device, the driver name and version, and the date.
- First-party measurements are the most trusted source type and are one of the two ways a wiki page can reach `verified` confidence.
- No architecture is "primary". Every claim is scoped by nodes of the architecture tree.

## Maintenance Tooling

| Script | Purpose |
|---|---|
| `scripts/validate.py` | Validate frontmatter against the schemas, vocabulary, architecture tree, cross-references and version-claim registry |
| `scripts/generate-indices.py` | Regenerate `queries/*.md` from frontmatter |
| `scripts/repo_status.py` | Print corpus counts |
| `scripts/check_external_locators.py` | Check, against a local checkout, that every `raw_data` file cited in another git repository exists at its cited commit |
| `scripts/refresh_candidate_ledger.py` | Search an upstream repository (GitHub through `gh`, or a GitLab instance over its public API) for merged pull requests and append include / defer / exclude rows to `candidates/<slug>.yaml` |
| `scripts/generate-pr-pages.py` | Write a source-pr page for every `include` row of a ledger; rows it cannot turn into a page go to `data/pr-page-skipped.yaml` |
| `scripts/fetch_pr_diff.py` | Save the shader patches of included pull requests as `artifacts/prs/<slug>/PR-<number>/` with a `PROVENANCE.yaml` and the upstream licence text |
| `scripts/fetch_kernel_files.py` | Save the complete upstream files listed in `artifacts/kernels/MANIFEST.yaml`, pinned to a commit, with a `PROVENANCE.yaml` per bundle |
| `scripts/check_release_membership.py` | Record in `data/release-membership.yaml` which included merge requests of a GitLab ledger a release tag contains |
| `scripts/verify_verbatim.py` | Check offline that every artifact bundle matches its recorded sha256 and is named by a page; `--against-cache` also compares with the cached upstream patches |
| `scripts/pr_policy.py`, `scripts/pr_evidence.py`, `scripts/pr_artifacts.py` | The intake decision rules, the `gh` fetch and cache layer, and the artifact bundle format shared by the scripts above |

```bash
python3 scripts/validate.py
python3 scripts/generate-indices.py
python3 scripts/repo_status.py
```

## Scope Rules

- **Kernel-only.** Compute-shader kernel optimization; no model export, graph partitioning or runtime scheduling topics.
- **Vulkan GLSL only.** No CUDA-specific content.
- **English only.**
- **Public-safe.** No internal codenames, device serial numbers or internal hostnames in any file.

## Repository Layout

```
vk-kernel-wiki/
├── SKILL.md                    # Skill entry point
├── README.md                   # This file
├── CLAUDE.md                   # Schema and authoring rules
├── index.md                    # Curated top-level navigation
├── NOTICE.md                   # Attribution and third-party licenses
├── LICENSE                     # MIT license of this repository's own content
│
├── data/
│   ├── schemas.yaml            # Required and optional fields per page type
│   ├── tags.yaml               # Controlled vocabulary
│   ├── aliases.yaml            # Canonical term -> search spellings
│   ├── architectures.yaml      # Vendor / generation / device tree
│   ├── version-claims.yaml     # Version-sensitive claim registry
│   └── pr-page-skipped.yaml    # Included ledger rows without a page, and why
│
├── candidates/                 # One pull-request ledger per upstream repository
├── artifacts/prs/<slug>/       # Upstream shader patches, PROVENANCE.yaml per PR, upstream LICENSE
│
├── scripts/
│   ├── query.py                # Unified search
│   ├── get_page.py             # Page fetcher
│   ├── grep_wiki.py            # Regex search
│   ├── validate.py             # Validator
│   ├── generate-indices.py     # Query-index generator
│   ├── repo_status.py          # Corpus counts
│   ├── check_external_locators.py  # External raw_data locator check
│   ├── refresh_candidate_ledger.py  # Pull-request search and triage
│   ├── generate-pr-pages.py    # source-pr page generator
│   ├── pr_policy.py            # Pull-request intake rules
│   ├── pr_evidence.py          # gh fetch, evidence cache, ledger I/O
│   ├── fetch_pr_diff.py        # Shader-patch artifact writer
│   ├── verify_verbatim.py      # Artifact integrity check
│   ├── pr_artifacts.py         # Artifact bundle format
│   ├── arch_policy.py          # Architecture-tree queries and alias resolution
│   ├── _wiki_root.py           # Shared root resolver (VK_KERNEL_WIKI_ROOT)
│   ├── _yaml_compat.py         # Host PyYAML or bundled fallback
│   └── _vendor/                # Bundled PyYAML (do not edit)
│
├── references/
│   ├── primer.md
│   ├── schema.md
│   ├── examples.md
│   └── authoring.md
│
├── sources/                    # Layer 1: raw evidence
│   ├── measurements/           # 5 pages (Radeon 780M)
│   ├── prs/                    # glslang/, llama-cpp/, mesa/, mnn/, ncnn/, spirv-tools/, vk-coopmat-perf/: 713 generated pages
│   ├── docs/                   # 58 pages
│   └── blogs/                  # 11 pages
│
├── wiki/                       # Layer 2: synthesized knowledge
│   ├── hardware/               # 2 pages
│   ├── techniques/             # 5 pages
│   ├── patterns/               # 3 pages
│   ├── kernels/                # 3 pages
│   ├── languages/              # 1 page
│   └── migration/
│
├── queries/                    # Layer 3: generated indices
├── tests/                      # Tests and synthetic fixtures
└── third_party/                # Upstream license and revision (do not edit)
```

## Attribution and License

The structure and scripts are derived from KernelWiki (MIT, mit-han-lab). This repository's own content is distributed under the MIT license ([`LICENSE`](LICENSE)). Upstream pull-request excerpts and shader patches keep their upstream license. See [`NOTICE.md`](NOTICE.md).
