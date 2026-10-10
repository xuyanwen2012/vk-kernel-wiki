# vk-kernel-wiki: Schema and Authoring Rules

A structured knowledge base about optimizing Vulkan GLSL compute-shader kernels for ML inference across GPU vendors, built for retrieval by LLM agents. This file is the rulebook for agents that edit the repository. For querying, see `SKILL.md`.

Corpus status: 788 pages. 18 (5 source-measurement, 13 wiki) are for the device node `radeon-780m` on RADV Mesa 25.2.7, the only measured device; 58 are document pages (34 `official-doc`, 9 `upstream-code`, 14 `vendor-doc`, 1 `paper`), 11 are blog pages and 1 is a language page; 700 are generated source-pr pages from `ggml-org/llama.cpp` (405), `mesa/mesa` (156), `Tencent/ncnn` (103), `alibaba/MNN` (10), `jeffbolznv/vk_cooperative_matrix_perf` (10), `KhronosGroup/glslang` (8) and `KhronosGroup/SPIRV-Tools` (8). Run `python3 scripts/repo_status.py` for current counts; `index.md` lists the pages.

## Non-Negotiable Authoring Rules

1. **Source pages contain verbatim excerpts and locators only.** Never write a model-authored summary, paraphrase or interpretation into a page under `sources/`. Interpretation belongs in `wiki/`, with a citation back to the source page.
2. **Every number is traceable.** A number may appear in the wiki only if a source page backs it and you can give the exact locator (file and line, table row, log line, section). A number with no locator is not written. Do not round, extrapolate or carry a number over to another device, driver or shape.
3. **Every measurement carries device, driver and version, and date.** The device is one exact device node from `data/architectures.yaml`; the driver string names the driver and its version; the date is an ISO date. A measurement missing any of the three is not recorded.
4. **Confidentiality: this repository may become public.** Never write internal codenames, device serial numbers or internal hostnames into any file, including raw data files, excerpts, paths and locators. Scrub them before a file enters the repository. A vendor node that is reserved and empty in the architecture tree stays empty until it is explicitly opened.

Further rules:

- English only, in every file.
- Do not invent facts. If a source does not state something, the wiki does not state it.
- Use canonical vocabulary terms and node names in frontmatter; aliases are for search only.
- Do not edit `scripts/_vendor/` or `third_party/`.
- Do not edit `queries/` by hand; it is generated. The generated files are committed, and the test suite fails when they are stale.

## Navigation

```bash
python3 scripts/query.py "<keywords>" [--tag X --type Y --architecture Z]
python3 scripts/get_page.py <id-or-path> [--follow-sources]
python3 scripts/grep_wiki.py "<pattern>" [--only wiki|sources]
```

Without the scripts: start at `index.md`, then the generated indices in `queries/` (`by-architecture.md`, `by-device.md`, `by-problem.md`, `by-technique.md`, `by-hardware-feature.md`, `by-kernel-type.md`, `by-language.md`, `by-repo.md`), then follow `sources` ids from any wiki page to the raw evidence.

## Three-Layer Architecture

### Layer 1: Sources (`sources/`)

Raw evidence. Each file has YAML frontmatter with a unique `id`. Bodies hold verbatim excerpts and locators only.

- `sources/measurements/`: first-party measurements. The most trusted source type.
- `sources/prs/`: upstream pull requests.
- `sources/docs/`: official documentation (`official-doc`: specification-grade only), other projects' source files (`upstream-code`), vendor and project articles and guides (`vendor-doc`) and papers.
- `sources/blogs/`: benchmark blogs and community notes.

### Layer 2: Wiki (`wiki/`)

Synthesized knowledge pages, cross-referenced by `id`, each citing source pages.

- `wiki/hardware/`: GPU and driver capabilities the kernels depend on.
- `wiki/techniques/`: optimization techniques.
- `wiki/patterns/`: symptom to candidate-technique diagnosis.
- `wiki/kernels/`: kernel case studies with performance claims.
- `wiki/languages/`: shader language and toolchain guides.
- `wiki/migration/`: porting notes between architecture nodes.

### Layer 3: Queries (`queries/`)

Generated cross-reference indices. Regenerate with `python3 scripts/generate-indices.py`.

## Page Types

`data/schemas.yaml` is authoritative; `references/schema.md` is the readable reference with one synthetic example per type. Page type is detected from the file path alone: a `.md` file under `wiki/` or `sources/` outside the directories below is rejected.

| Page type | Path | ID prefix | Required fields |
|-----------|------|-----------|-----------------|
| source-measurement | `sources/measurements/` | `meas-` | id, title, source_category (= measurement), architectures, tags, device, driver, measured_at, method, raw_data, captured_at |
| source-pr | `sources/prs/` | `pr-` | id, repo, pr, title, author, date, url, source_category (= upstream-code), architectures, tags, techniques, hardware_features, kernel_types, languages, captured_at, status |
| source-doc | `sources/docs/` | `doc-` | id, title, url, source_category, architectures, tags, retrieved_at |
| source-blog | `sources/blogs/` | `blog-` | id, title, author, url, source_category, architectures, tags, retrieved_at |
| wiki-hardware | `wiki/hardware/` | `hw-` | id, title, type (= hardware), architectures, tags, confidence, related, sources, aliases |
| wiki-technique | `wiki/techniques/` | `technique-` | id, title, type (= technique), architectures, tags, confidence, reproducibility (>= snippet), prerequisites, related, sources |
| wiki-pattern | `wiki/patterns/` | `pattern-` | id, title, type (= pattern), tags, symptoms, candidate_techniques, related, sources |
| wiki-kernel | `wiki/kernels/` | `kernel-` | id, title, type (= kernel), architectures, tags, confidence, reproducibility (>= snippet), kernel_types, languages, related, sources, performance_claims |
| wiki-language | `wiki/languages/` | `lang-` | id, title, type (= language), tags, related, sources, reproducibility (>= snippet) |
| wiki-migration | `wiki/migration/` | `migration-` | id, title, type (= migration), from_arch, to_arch, tags, related, sources |

Source-type specifics:

- **source-measurement**: `device` is exactly one device node (not a vendor or generation, not an alias) and must also be listed in the page's `architectures`. `driver` names the driver and its version (`<driver name> <version>`; a bare name is rejected) and `method` is a non-empty string. `raw_data` is a non-empty list of mappings with `locator` and `description`, in one of two forms. In-repository form (no `repo`, no `commit`): `locator` is an `http(s)` URL or a repo-relative path to a file that exists in this repository (no absolute path, no `~`, no `..`). External-repository form (`repo` and `commit`, always both): `repo` is the `https` URL of another git repository, `commit` is exactly 40 lowercase hex characters, and `locator` is a path relative to that repository's root, optionally followed by `#fragment` (no leading `/`, no `~`, no `..`, no URL); the validator does not check that this file exists, `scripts/check_external_locators.py` does.
- **source-pr**: a GitLab merge request is a source-pr page too; `pr` is its iid, and when the project merges by fast-forward `merge_sha` is the head commit of the merge request (the commit that landed). Optional `architecture_evidence` lists, per node in `architectures`, where the generator found it (`locator: title`, `added-patch:<path>` or `changed-path:<path>`, and the `matched` text). Optional `artifact_dir` is a repository path under `artifacts/prs/` that holds a `PROVENANCE.yaml`. `status` is `open`, `merged` or `closed`. `merge_sha` is required and must be 40 hex characters when `status` is `merged`. The body must contain a non-empty verbatim excerpt between `<!-- upstream-excerpt-start -->` and `<!-- upstream-excerpt-end -->`. Each `sources/prs/<dir>/` directory holds the pages of exactly one `repo`.

Wiki-type specifics:

- **wiki-pattern**: `candidate_techniques` ids are remedies and must start with `technique-`, `hw-` or `migration-`.
- **Any page with `hardware_features`**: a hardware-feature term used in `tags` must also be listed in `hardware_features`.

## Controlled Vocabulary

- `data/tags.yaml` is the single source of truth for `tags`, `techniques`, `hardware_features`, `kernel_types` and `languages`, and for the `confidence`, `reproducibility`, `source_categories` and `evidence_types` value sets. Unknown terms are rejected by the validator.
- `data/architectures.yaml` is the single source of truth for the `architectures` field, for `from_arch` / `to_arch`, and for a measurement's `device`. It is a tree: vendor, optional generation, device. `data/tags.yaml` has no architectures list.
- `data/aliases.yaml` maps each canonical term or node to its search spellings. An alias never maps to two different canonicals.

Vocabulary discipline:

- Use an existing term when one fits. Do not add a near-synonym; add an alias instead.
- Add a new term only when a page needs it and it names something concrete (a device capability, a shader parameter, an operator family). Add it to `data/tags.yaml` in the same change as the page that uses it.
- Terms and node names are lowercase kebab-case.
- Tag a page with the most specific architecture node the evidence supports. Tag a device node only when the evidence is for that device; tag a generation or vendor node only when the source makes the claim at that level. Queries for a device do not return pages tagged only with its ancestors.
- Adding a device means adding a node to `data/architectures.yaml` (and its aliases to `data/aliases.yaml`); no script hardcodes node names.

## Confidence Rules

- `verified`: enforced by the validator. The page needs a non-empty `evidence_basis` (a list of mappings with at least `evidence_type` and `source_id`), and every `source_id` must also appear in the page's `sources`. It passes if either
  - (a) at least one entry has `evidence_type: measurement` and its `source_id` resolves to a source-measurement page, or
  - (b) it has at least one `official-doc` entry and at least one `upstream-code` entry.

  Labels are bound to what they cite: an `official-doc` entry must cite a source page with `source_category: official-doc`, and an `upstream-code` entry must cite a source-pr page. `official-doc` is reserved for specification-grade documents (Khronos specifications and proposals, the Vulkan Guide, vendor ISA / instruction specifications, driver documentation and release notes); a document page that quotes another project's source is `upstream-code` and a vendor or project article, guide or slide deck is `vendor-doc`, and neither counts towards (b).
- `source-reported`: stated by at least one cited source.
- `inferred`: synthesized from several sources; no single source states it.
- `experimental`: undocumented or version-dependent behaviour. Attach a `version_sensitive` pointer where a tool or driver version matters.

When unsure, choose the lower level.

## Reproducibility Levels

`concept` < `pseudocode` < `snippet` < `runnable` < `benchmarked`. Technique, kernel and language pages must be at least `snippet`.

## Performance Claim Format

`performance_claims` is a list of mappings on wiki-kernel pages. Required per claim: `gpu`, `driver`, `dtype`, `shape`, `metric`, `value` (numeric), `measured_at`, `source_id`, `source_locator`. Optional: `baseline`, `utilization`, `notes`. `source_id` must be the id of an existing source page and `source_locator` a non-empty exact locator inside it. `gpu` is exactly one device node; `driver` names the driver and its version; `dtype`, `shape` and `metric` are non-empty strings; `value` is a finite number; `measured_at` is an ISO date.

```yaml
performance_claims:
  - gpu: <device-node>
    driver: "<driver name> <driver version>"
    dtype: <dtype>
    shape: "<exact shape>"
    metric: <metric-name>
    value: <number copied from the source>
    measured_at: 'YYYY-MM-DD'
    source_id: meas-<slug>
    source_locator: "<path>, line <N>"
```

A kernel page with no backed numbers carries `performance_claims: []`.

## Version-Sensitive Claims

A page whose claim depends on a tool or driver version carries `version_sensitive: vs-<slug>` (or a mapping with `id`). The id must resolve to an entry in `data/version-claims.yaml`, and that entry's `applies_to` must list the page. Entry fields: `id`, `tool`, `claim_valid_for`, `last_verified_release`, `last_verified_at`, `applies_to` (at least one path), `source_ids` (at least one), optional `notes`. `tool` is one of `mesa-radv`, `mesa-anv`, `glslc`, `vulkan-sdk`, `adreno-driver`, `mali-driver`, `nvidia-driver`, `executorch`.

## Tooling

- `scripts/validate.py`: validates frontmatter against `data/schemas.yaml`, the vocabulary, the architecture tree, cross-references and the version-claim registry.
- `scripts/check_external_locators.py --checkout <path> [--repo <url>]`: for every `raw_data` entry in the external-repository form (limited to `<url>` when `--repo` is given), checks with `git cat-file` that the file exists at the cited commit in a local checkout. Exit 0 when all resolve, 1 on any failure, 2 when the checkout does not contain a cited commit.
- `scripts/generate-indices.py`: regenerates `queries/*.md` from frontmatter.
- `scripts/repo_status.py`: prints corpus counts.
- `scripts/refresh_candidate_ledger.py --cutoff <date> [--repos <slug>]`: searches an upstream repository for merged pull requests and appends one include / defer / exclude row per pull request to `candidates/<slug>.yaml`. Existing rows are never changed; a row edited by hand carries `decision_source: manual`. `--reclassify-excluded` recomputes only excluded, non-manual rows (use it after widening a ledger header).
- `scripts/generate-pr-pages.py [--repos <slug>]`: writes `sources/prs/<slug>/PR-<number>.md` for every `include` row. Rows that cannot become a valid page are listed in `data/pr-page-skipped.yaml`.
- `scripts/pr_policy.py`: the intake rules both scripts share. Pages under `sources/prs/<slug>/` are generated: change the policy or the ledger and regenerate with `--force` instead of editing a page by hand. The generator fills `techniques` only with the terms a title or shader file name states outright (tile sizing, split-k, fusion, tuning, workaround, Winograd, channel packing, required subgroup size, fp32 accumulation); every other technique term requires reading the diff.
- `scripts/fetch_pr_diff.py [--repos <slug>]`: saves the shader patches of included pull requests under `artifacts/prs/<slug>/PR-<number>/` (`shaders.patch`, or `driver.patch` for a `scope_mode: driver` ledger, and `PROVENANCE.yaml`) and the upstream licence text at `artifacts/prs/<slug>/LICENSE`. The ledger must name the licence (`license: <SPDX id>`); files whose own header carries another licence are listed in the ledger's `artifact_exclude_path_markers` and are not saved. Run it before the page generator so pages receive `artifact_dir`.
- `scripts/fetch_kernel_files.py`: saves the complete upstream files listed in `artifacts/kernels/MANIFEST.yaml`, pinned to a commit. Quote code in a wiki page from these files, with the file, line range and commit as the locator.
- `scripts/check_release_membership.py --repos <slug> --tag <tag>`: records in `data/release-membership.yaml` which included merge requests a release tag contains (by commit id). Use it before writing a version-sensitive claim.
- `scripts/verify_verbatim.py [--against-cache]`: checks every artifact bundle against its recorded sha256 and against the pages. Never edit a file under `artifacts/` by hand.
- The intake scripts call GitHub through `gh` and cache what they fetch under `.cache/pr-evidence/` (ignored by git). Everything else, including the test suite, is offline.
- No Python package is required. The scripts prefer host PyYAML and fall back to the bundled loader, so they run under `python3 -S`.
- `VK_KERNEL_WIKI_ROOT` points every script at another wiki root (a directory containing `data/tags.yaml`). Tests use it.

After every content change:

```bash
python3 scripts/validate.py
python3 scripts/generate-indices.py
```

When a measurement page cites raw data in another git repository, also run `python3 scripts/check_external_locators.py --checkout <path> --repo <url>` against a local checkout of that repository.

Step-by-step authoring instructions are in `references/authoring.md`.

## Scope Rules

- **Kernel-only.** Compute-shader kernel optimization. No model export, graph partitioning or runtime scheduling topics.
- **Vulkan GLSL only.** No CUDA-specific content.
- **Vendor-neutral structure, vendor-specific evidence.** No architecture is "primary"; every claim is scoped by its architecture nodes. AMD RDNA3 is the first vendor layer to receive content.
- **First-party measurements first.** Prefer a measurement source page over any secondary report of the same quantity.
- **Fixtures are not knowledge.** Synthetic pages live only under `tests/fixtures`, with titles starting with `FIXTURE`. Never copy them into `wiki/` or `sources/`.

## Attribution

Structure and scripts are derived from KernelWiki (MIT). See `NOTICE.md`.
