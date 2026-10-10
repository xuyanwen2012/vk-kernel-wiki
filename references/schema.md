# Schema Reference

Condensed reference for the wiki's page schemas. The machine-readable
definition is `data/schemas.yaml`; `scripts/validate.py` enforces it. When
this file and `data/schemas.yaml` disagree, the yaml wins.

Every example below is synthetic: titles start with `EXAMPLE` and all values
are placeholders. None of them is a real measurement, source, or claim.

## Page Types and IDs

Page type is detected from the file path alone; the frontmatter `type` field
must agree with it but never decides it. A `.md` file under `wiki/` or
`sources/` that is not inside one of the directories below is rejected, and
the extension must be lowercase `.md`. Every page has a unique `id` with a
type-specific prefix.

| Type | Path | ID prefix | Purpose |
|------|------|-----------|---------|
| wiki-hardware | `wiki/hardware/` | `hw-` | GPU / driver hardware feature pages |
| wiki-technique | `wiki/techniques/` | `technique-` | Optimization techniques |
| wiki-pattern | `wiki/patterns/` | `pattern-` | Symptom to candidate-technique diagnosis |
| wiki-kernel | `wiki/kernels/` | `kernel-` | Kernel case studies with performance claims |
| wiki-language | `wiki/languages/` | `lang-` | Shader language / toolchain guides |
| wiki-migration | `wiki/migration/` | `migration-` | Porting notes between architecture nodes |
| source-pr | `sources/prs/` | `pr-` | An upstream pull request |
| source-doc | `sources/docs/` | `doc-` | Official documentation, papers |
| source-blog | `sources/blogs/` | `blog-` | Benchmark blogs, community notes |
| source-measurement | `sources/measurements/` | `meas-` | First-party measurements (most trusted) |

## Shared Rules

- **Controlled vocabulary.** `data/tags.yaml` is the single source of truth for
  `tags`, `techniques`, `hardware_features`, `kernel_types`, `languages`,
  `confidence`, `reproducibility`, `source_categories`, and `evidence_types`.
  This file deliberately does not duplicate those lists.
- **Architectures.** `data/architectures.yaml` is the single source of truth
  (a vendor -> generation -> device tree). Any node name is a valid value of
  the `architectures` field, and of `from_arch` / `to_arch`. Aliases in
  `data/aliases.yaml` are resolved by the query tools; frontmatter uses
  canonical node names.
- **Source bodies.** No model-written summaries. A source page body holds
  verbatim excerpts and locators only.
- **Dates** are ISO `YYYY-MM-DD`. A timestamp (date plus time) is rejected.
- **Scalar fields** (`id`, `type`, `confidence`, `reproducibility`,
  `source_category`, `status`, `device`, `from_arch`, `to_arch`) hold one
  string each, never a list or mapping.
- **Tags and hardware features.** `tags` accepts any term of the four topical
  groups, but never an architecture node name (those go in `architectures`).
  When a page has a `hardware_features` field, every hardware-feature term in
  its `tags` must also be listed in `hardware_features`.

## Source Pages

### source-pr

Required: `id`, `repo`, `pr`, `title`, `author`, `date`, `url`,
`source_category` (= `upstream-code`), `architectures`, `tags`, `techniques`,
`hardware_features`, `kernel_types`, `languages`, `captured_at`, `status`
(`open` | `merged` | `closed`).
Optional: `merge_sha`, `description`, `changed_paths`, `inclusion_reason`.

`merge_sha` is required, and must be a full 40-hex commit id, when
`status: merged`.

Each directory `sources/prs/<dir>/` holds the PR pages of exactly one
repository: all pages in it must carry the same `repo` value.

```yaml
id: pr-example-repo-1
repo: example-org/example-repo
pr: 1
title: "EXAMPLE pull request title"
author: example-author
date: '2000-01-01'
url: https://example.invalid/example-org/example-repo/pull/1
source_category: upstream-code
architectures: [<architecture-node>]
tags: [<tag>]
techniques: [<technique>]
hardware_features: [<hardware-feature>]
kernel_types: [<kernel-type>]
languages: [glsl]
captured_at: '2000-01-02'
status: merged
merge_sha: 0000000000000000000000000000000000000000
description: "EXAMPLE one-line description"
changed_paths:
  - path/to/example_shader.glsl
inclusion_reason: "EXAMPLE reason this pull request is kept"
```

The body must contain a verbatim excerpt of the upstream text between these
markers:

```markdown
<!-- upstream-excerpt-start -->
EXAMPLE verbatim text copied from the pull request.
<!-- upstream-excerpt-end -->
```

The start marker must come first, and the excerpt must contain real text: an
excerpt that is empty once HTML comments and code-fence delimiter lines are
removed is rejected.

### source-doc

Required: `id`, `title`, `url`, `source_category` (`official-doc` |
`upstream-code` | `vendor-doc` | `paper`), `architectures`, `tags`,
`retrieved_at`.
Optional: `author`, `description`.

Which category a document page takes:

- `official-doc`: a specification-grade document. Khronos specifications,
  extension texts and proposals, the Vulkan Guide, a vendor ISA or instruction
  specification, driver documentation and driver release notes. Only this
  category counts as `official-doc` evidence for `verified`.
- `upstream-code`: a page that quotes another project's source files, tests
  or code samples at a pinned commit (it is not a pull request, so it is not
  `upstream-code` evidence for `verified` either, which needs a `source-pr`
  page).
- `vendor-doc`: a vendor or project article, guide, handbook, slide deck or
  framework release note.
- `paper`: a published paper.

All four are citable in a page's `sources` and as a claim's `source_id`.

```yaml
id: doc-example-specification
title: "EXAMPLE specification document"
url: https://example.invalid/spec
source_category: official-doc
architectures: [<architecture-node>]
tags: [<tag>]
retrieved_at: '2000-01-01'
author: "EXAMPLE publisher"
description: "EXAMPLE one-line description"
```

### source-blog

Required: `id`, `title`, `author`, `url`, `source_category`
(`benchmark-blog` | `community-note`), `architectures`, `tags`,
`retrieved_at`.
Optional: `description`.

```yaml
id: blog-example-post
title: "EXAMPLE blog post"
author: example-author
url: https://example.invalid/blog/post
source_category: community-note
architectures: [<architecture-node>]
tags: [<tag>]
retrieved_at: '2000-01-01'
description: "EXAMPLE one-line description"
```

### source-measurement

First-party measurements. Required: `id`, `title`, `source_category`
(= `measurement`), `architectures`, `tags`, `device`, `driver`, `measured_at`,
`method`, `raw_data`, `captured_at`.
Optional: `os`, `kernel_version`, `glslc_version`, `commit`, `baseline`,
`description`.

- `device`: exactly one device (leaf) node from `data/architectures.yaml`.
  The same node must also be listed in the page's `architectures`.
- `driver`: non-empty string naming the driver and its version, in the form
  `<driver name> <version>`. A name with no version is rejected.
- `measured_at`, `captured_at`: ISO dates.
- `raw_data`: non-empty list of mappings with `locator` and `description`.
  An entry has one of two forms:
  - **In-repository form** (no `repo`, no `commit`): `locator` is either an
    `http(s)://` URL or a repo-relative path (optionally followed by
    `#fragment`) to a file that exists in this repository. Absolute paths,
    home paths (`~`) and `..` are rejected.
  - **External-repository form** (`repo` and `commit`): the raw file lives in
    another git repository. `repo` is the `https://` URL of that repository
    and `commit` is exactly 40 lowercase hex characters (quote a sha that
    consists of digits only, or YAML reads it as a number). If either field
    is present, both are required. `locator` is a path relative to the root
    of that repository, optionally followed by `#fragment`; absolute paths,
    home paths (`~`), `..` and URLs are rejected. The validator does not look
    this file up in the wiki repository. `scripts/check_external_locators.py`
    verifies that it exists at that commit, against a local checkout.

```yaml
id: meas-example-run
title: "EXAMPLE measurement run"
source_category: measurement
architectures: [<device-node>]
tags: [<tag>]
device: <device-node>
driver: "<driver name> <driver version>"
measured_at: '2000-01-01'
method: "EXAMPLE description of how the numbers were collected"
raw_data:
  - locator: sources/measurements/example-run/example-raw-log.txt
    description: "EXAMPLE raw benchmark log kept in this repository"
  - repo: https://example.org/example-owner/example-repo
    commit: 0123456789abcdef0123456789abcdef01234567
    locator: path/in/that/repo/example-results.csv
    description: "EXAMPLE raw results file kept in another git repository"
captured_at: '2000-01-02'
os: "<os name and version>"
kernel_version: "<kernel version>"
glslc_version: "<glslc version>"
commit: 0000000000000000000000000000000000000000
baseline: "EXAMPLE description of the baseline being compared against"
description: "EXAMPLE one-line description"
```

## Wiki Pages

### wiki-hardware

Required: `id`, `title`, `type` (= `hardware`), `architectures`, `tags`,
`confidence`, `related`, `sources`, `aliases`.
Optional: `reproducibility`, `prerequisites`, `evidence_basis`,
`version_sensitive`.

```yaml
id: hw-example-feature
title: "EXAMPLE hardware feature"
type: hardware
architectures: [<architecture-node>]
tags: [<tag>]
confidence: source-reported
related: [technique-example-technique]
sources: [doc-example-specification]
aliases: ["EXAMPLE alias"]
```

### wiki-technique

Required: `id`, `title`, `type` (= `technique`), `architectures`, `tags`,
`confidence`, `reproducibility` (>= `snippet`), `prerequisites`, `related`,
`sources`.
Optional: `aliases`, `symptoms`, `evidence_basis`, `version_sensitive`.

This example also shows a `verified` page passing through alternative (b) of
the rule below, and a `version_sensitive` pointer.

```yaml
id: technique-example-technique
title: "EXAMPLE technique"
type: technique
architectures: [<architecture-node>]
tags: [<tag>]
confidence: verified
reproducibility: snippet
prerequisites: [hw-example-feature]
related: [kernel-example-kernel]
sources: [doc-example-specification, pr-example-repo-1]
evidence_basis:
  - evidence_type: official-doc
    source_id: doc-example-specification
    locator: "EXAMPLE section reference"
  - evidence_type: upstream-code
    source_id: pr-example-repo-1
    locator: "path/to/example_shader.glsl"
version_sensitive: vs-example-claim
```

### wiki-pattern

Required: `id`, `title`, `type` (= `pattern`), `tags`, `symptoms`,
`candidate_techniques`, `related`, `sources`.
Optional: `architectures`, `confidence`, `evidence_basis`,
`version_sensitive`.

```yaml
id: pattern-example-symptom
title: "EXAMPLE diagnostic pattern"
type: pattern
tags: [<tag>]
symptoms: ["EXAMPLE observable symptom"]
candidate_techniques: [technique-example-technique]
related: [kernel-example-kernel]
sources: [doc-example-specification]
```

### wiki-kernel

Required: `id`, `title`, `type` (= `kernel`), `architectures`, `tags`,
`confidence`, `reproducibility` (>= `snippet`), `kernel_types`, `languages`,
`related`, `sources`, `performance_claims`.
Optional: `aliases`, `prerequisites`, `symptoms`, `evidence_basis`,
`version_sensitive`.

This example shows a `verified` page passing through alternative (a).

```yaml
id: kernel-example-kernel
title: "EXAMPLE kernel case study"
type: kernel
architectures: [<device-node>]
tags: [<tag>]
confidence: verified
reproducibility: snippet
kernel_types: [<kernel-type>]
languages: [glsl]
related: [technique-example-technique]
sources: [meas-example-run]
evidence_basis:
  - evidence_type: measurement
    source_id: meas-example-run
    locator: "path/to/example-raw-log.txt"
performance_claims:
  - gpu: <device-node>
    driver: "<driver name> <driver version>"
    dtype: <dtype>
    shape: "<exact shape>"
    metric: <metric-name>
    value: 0
    measured_at: '2000-01-01'
    source_id: meas-example-run
    source_locator: "path/to/example-raw-log.txt, line <N>"
    baseline: "EXAMPLE baseline description"
    notes: "EXAMPLE placeholder claim; the value 0 is not a measurement"
```

### wiki-language

Required: `id`, `title`, `type` (= `language`), `tags`, `related`, `sources`,
`reproducibility` (>= `snippet`).
Optional: `architectures`, `confidence`, `aliases`, `evidence_basis`,
`version_sensitive`.

```yaml
id: lang-example-language
title: "EXAMPLE language guide"
type: language
tags: [<tag>]
related: [technique-example-technique]
sources: [doc-example-specification]
reproducibility: snippet
```

### wiki-migration

Required: `id`, `title`, `type` (= `migration`), `from_arch`, `to_arch`,
`tags`, `related`, `sources`.
Optional: `confidence`, `reproducibility`, `prerequisites`, `evidence_basis`,
`version_sensitive`.

```yaml
id: migration-example-a-to-b
title: "EXAMPLE migration from one node to another"
type: migration
from_arch: <architecture-node>
to_arch: <architecture-node>
tags: [<tag>]
related: [technique-example-technique]
sources: [doc-example-specification]
```

## performance_claims

A list of mappings on `wiki-kernel` pages (schema section `performance-claim`).
The field is required, but the list may be empty: a kernel page with no backed
numbers carries `performance_claims: []`.

| Field | Required | Rule |
|-------|----------|------|
| `gpu` | yes | Exactly one device node from `data/architectures.yaml` (no vendor or generation node, no alias) |
| `driver` | yes | Driver name and version, `<driver name> <version>`; a name with no version is rejected |
| `dtype` | yes | Data type of the workload; non-empty string |
| `shape` | yes | Exact problem shape; non-empty string |
| `metric` | yes | Name of the measured quantity; non-empty string |
| `value` | yes | A finite number (not a string, boolean, NaN or infinity) |
| `measured_at` | yes | ISO date (not a timestamp) |
| `source_id` | yes | Must be the id of an existing source page |
| `source_locator` | yes | Non-empty exact locator inside that source |
| `baseline` | no | What the value is compared against |
| `utilization` | no | Free text |
| `notes` | no | Free text |

## Confidence Levels

- **`verified`**: enforced by the validator (schema section
  `verified_evidence_rule`). The page needs a non-empty `evidence_basis`, a
  list of mappings with at least `evidence_type` and `source_id`. Every
  `source_id` must be listed in the page's `sources`. The page passes if
  **either**
  - (a) at least one entry has `evidence_type: measurement` and its
    `source_id` resolves to a `source-measurement` page, **or**
  - (b) it has at least one `official-doc` entry **and** at least one
    `upstream-code` entry.

  The evidence types used by the rule are bound to the page they cite, so a
  label alone never satisfies it: a `measurement` entry must cite a
  `source-measurement` page, an `official-doc` entry a source page whose
  `source_category` is `official-doc`, and an `upstream-code` entry a
  `source-pr` page. A document page filed as `upstream-code` or `vendor-doc`
  therefore never counts towards alternative (b). A mismatch is an error on any page that carries
  `evidence_basis`, whatever its confidence.
- **`source-reported`**: stated by at least one cited source.
- **`inferred`**: synthesized from several sources; no single source states it.
- **`experimental`**: undocumented or version-dependent behaviour; attach a
  `version_sensitive` pointer where a tool or driver version matters.

## Reproducibility Levels

`wiki-technique`, `wiki-kernel`, and `wiki-language` must be at least
`snippet`.

| Level | Meaning |
|-------|---------|
| `concept` | Text only |
| `pseudocode` | Language-agnostic algorithm |
| `snippet` | Compilable code fragment |
| `runnable` | Self-contained buildable example |
| `benchmarked` | Runnable plus performance numbers with environment metadata |

## Version-Sensitive Claims

A page whose claim depends on a tool or driver version carries a pointer:

```yaml
version_sensitive: vs-example-claim
```

The pointer may also be a mapping with at least `id` (optional `tool`,
`claim_valid_for`, `last_verified_release`, `last_verified_at`). The id starts
with `vs-` and must resolve to an entry in `data/version-claims.yaml`:

```yaml
claims:
  - id: vs-example-claim
    tool: glslc
    claim_valid_for: "<version range>"
    last_verified_release: "<release>"
    last_verified_at: '2000-01-01'
    applies_to:
      - wiki/techniques/example-technique.md
    source_ids:
      - doc-example-specification
    notes: "EXAMPLE placeholder entry"
```

- `tool` is one of `mesa-radv`, `mesa-anv`, `glslc`, `vulkan-sdk`,
  `adreno-driver`, `mali-driver`, `nvidia-driver`, `executorch`.
- `applies_to` and `source_ids` each need at least one entry.
- `claim_valid_for` and `last_verified_release` are non-empty strings.
- Consistency is checked in both directions: every pointer resolves to a
  registry entry whose `applies_to` lists the page carrying the pointer, and
  every `applies_to` path exists and carries that pointer.

## Cross-Reference Fields

- `sources`: source page ids whose content backs this wiki page.
- `related`: wiki page ids that are topically related.
- `prerequisites`: wiki page ids the reader should read first.
- `candidate_techniques` (pattern only): wiki page ids that address the
  listed symptoms. They are remedies, so each id must start with
  `technique-`, `hw-` or `migration-` (schema key
  `candidate_techniques_id_prefixes` under `wiki-pattern`).

Every id in `related`, `prerequisites` and `candidate_techniques` must resolve
to an existing page, and every id in `sources` to an existing source page.

## Attribution

The schema layout is derived from KernelWiki (MIT).
