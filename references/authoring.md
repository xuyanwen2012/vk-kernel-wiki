# Authoring Guide

How to add a first-party measurement source page and a wiki page that cites it, then validate and regenerate the indices.

Field definitions are in `references/schema.md`; the machine-readable schema is `data/schemas.yaml`. Every value in angle brackets below is a placeholder to replace. Nothing in this file is a real measurement.

## Rules That Apply to Every Step

1. **Source pages hold verbatim excerpts and locators only.** No model-written summary, paraphrase or conclusion goes into a file under `sources/`.
2. **Every number needs an exact locator.** If you cannot point at the file and line (or table row, or log line) a number came from, do not write the number.
3. **Every measurement carries device, driver and version, and date.**
4. **This repository may become public.** Remove internal codenames, device serial numbers and internal hostnames from raw files, excerpts, paths and locators before they enter the repository. If a raw file cannot be scrubbed without altering the measured values, do not add it.
5. Use canonical vocabulary terms (`data/tags.yaml`) and architecture node names (`data/architectures.yaml`), not aliases.

## Step 1: Check the vocabulary and the device node

```bash
python3 scripts/query.py --architecture <device-node> --type measurement --compact
```

- The device must be a node of kind `device` in `data/architectures.yaml`. If it is missing, add it under the right vendor (and generation, if any), and add its search spellings to `data/aliases.yaml`. Node names are lowercase kebab-case and unique across the tree.
- Every term you plan to put in `tags` must exist in `data/tags.yaml`. Prefer an existing term. If a new one is needed, add it in the same change.

## Step 2: Add the raw data

Each raw file (log, CSV, JSON) gets one `raw_data` entry, in one of two forms.

**In-repository form.** Put the unmodified measurement output in this repository, or keep it at a stable URL. The entry has `locator` and `description` only; `locator` is the file's repo-relative path (optionally followed by `#fragment`) or an `http(s)` URL. The validator rejects absolute paths, home paths (`~`), `..`, and repo-relative paths that do not name an existing file, so add the raw file before validating.

**External-repository form.** When the raw file already lives in another git repository, cite it there instead of copying it. The entry carries `repo` and `commit` in addition to `locator` and `description`:

```yaml
raw_data:
  - repo: https://<host>/<owner>/<name>
    commit: <40-hex commit that contains the file>
    locator: <path relative to that repository's root>
    description: "<what this file contains>"
```

`repo` must be an `https://` URL and `commit` exactly 40 lowercase hex characters (quote a sha made of digits only). If one of the two is present, the other is required. `locator` must be a relative path, optionally followed by `#fragment`: no leading `/`, no `~`, no `..`, no URL. `scripts/validate.py` checks only this form, not that the file exists; run `scripts/check_external_locators.py` against a local checkout of that repository to check existence (Step 5). Cite only a commit that is published in the repository named by `repo`.

Phase 1 does not fix a directory for raw files. The suggested convention is a directory next to the page, `sources/measurements/<slug>/`, with a non-Markdown extension, so that `scripts/grep_wiki.py --only sources --ext csv,json,txt` can search it. Do not store raw data as `.md` under `sources/`, because every `.md` file there is treated as a page.

Scrub confidential strings first (rule 4), and record in the page's `method` field that the file was scrubbed and what kind of string was removed.

## Step 3: Write the measurement source page

Create `sources/measurements/<slug>.md`. The id starts with `meas-`.

```markdown
---
id: meas-<slug>
title: "<what was measured, on which device>"
source_category: measurement
architectures: [<device-node>]
tags: [<term>, <term>]
device: <device-node>
driver: "<driver name> <driver version>"
measured_at: 'YYYY-MM-DD'
method: "<exact command or procedure, repetitions, what was timed>"
raw_data:
  - locator: sources/measurements/<slug>/<raw-file>
    description: "<what this file contains>"
captured_at: 'YYYY-MM-DD'
os: "<os name and version>"
kernel_version: "<kernel version>"
glslc_version: "<glslc version>"
commit: <40-hex commit of the code under test>
baseline: "<what the run is compared against, if anything>"
---

## Excerpt: <raw-file>, lines <A>-<B>

Locator: `sources/measurements/<slug>/<raw-file>`, lines <A>-<B>

<verbatim lines copied from the raw file, in a fenced code block>
```

Field notes:

- `source_category` must be `measurement`.
- `device` is exactly one device node. Vendor nodes, generation nodes and aliases are rejected. `architectures` must contain the same node.
- `driver` names the driver and its version in one string, in the form `<driver> <version>`, for example a Mesa driver name followed by the Mesa version. A name with no version is rejected.
- `measured_at` is the day the run happened; `captured_at` is the day the page was written. Both are ISO dates.
- `raw_data` must have at least one entry, each with non-empty `locator` and `description`. An entry that cites a file in another git repository also carries `repo` and `commit`, always both (Step 2). `commit` on its own is rejected; the commit of the code under test goes in the page-level `commit` field.
- `os`, `kernel_version`, `glslc_version`, `commit`, `baseline` and `description` are optional. Fill in what you actually know; leave out what you do not.

Body: only headings, locators and verbatim excerpts. Do not add sentences such as "this shows that ..." or a table of derived values. Ratios and speedups computed by you are not excerpts.

## Step 4: Write or update the wiki page that cites it

Interpretation goes here. Example for a kernel case study at `wiki/kernels/<slug>.md`:

```markdown
---
id: kernel-<slug>
title: "<kernel name>"
type: kernel
architectures: [<device-node>]
tags: [<term>]
confidence: verified
reproducibility: snippet
kernel_types: [<kernel-type>]
languages: [glsl]
related: []
sources: [meas-<slug>]
evidence_basis:
  - evidence_type: measurement
    source_id: meas-<slug>
    locator: "sources/measurements/<slug>/<raw-file>, lines <A>-<B>"
performance_claims:
  - gpu: <device-node>
    driver: "<driver name> <driver version>"
    dtype: <dtype>
    shape: "<exact shape>"
    metric: <metric-name>
    value: <number copied from the excerpt>
    measured_at: 'YYYY-MM-DD'
    source_id: meas-<slug>
    source_locator: "sources/measurements/<slug>/<raw-file>, line <N>"
---

<body: what the kernel does, a compilable snippet, and what the measurement shows,
each statement citing meas-<slug> and its locator>
```

Checklist:

- **`sources`** lists every source page the page relies on. Every `source_id` in `evidence_basis` and in `performance_claims` must be an existing source page; `evidence_basis` ids must also appear in `sources`.
- **`performance_claims`**: each claim needs `gpu`, `driver`, `dtype`, `shape`, `metric`, `value` (numeric), `measured_at`, `source_id`, `source_locator`. Optional: `baseline`, `utilization`, `notes`. `gpu` is the device node the number was taken on (not a vendor or generation node). `driver` and `measured_at` must match the measurement page. `value` is copied from the source, not recomputed. A kernel page with no backed numbers uses `performance_claims: []`.
- **`confidence: verified`** is allowed when `evidence_basis` holds a `measurement` entry that resolves to a source-measurement page (as above), or both an `official-doc` entry citing an official-doc source page and an `upstream-code` entry citing a PR source page. File a document page as `official-doc` only when it is specification-grade (a Khronos specification or proposal, the Vulkan Guide, a vendor ISA / instruction specification, driver documentation or release notes); a page quoting another project's source files is `upstream-code` and a vendor or project article, guide, slide deck or framework release note is `vendor-doc`, and neither can stand in for the official-doc half. Otherwise use `source-reported`, `inferred` or `experimental`. A measurement verifies what was measured, on that device and driver; it does not verify a general explanation of why.
- **`architectures`**: tag the device the evidence is for. Do not tag the generation or vendor node on the strength of one device's measurement.
- **`reproducibility`**: technique, kernel and language pages must be at least `snippet`, so the body needs a compilable code fragment. Use `benchmarked` only when the page is runnable and carries performance numbers with environment metadata.
- **Numbers in the body** follow the same rule as claims: state the device, driver version and date, and cite the source id and locator next to the number.
- **Version dependence**: if the statement holds only for some driver or tool versions, add an entry to `data/version-claims.yaml` (id starting with `vs-`, `applies_to` listing this page, at least one id in `source_ids`) and put `version_sensitive: vs-<slug>` in the page frontmatter. Both sides are required: the validator rejects a pointer whose registry entry does not list the page, and a registry entry whose `applies_to` page lacks the pointer.

Other wiki page types follow the same steps with their own required fields; see `references/schema.md`.

## Step 5: Validate

```bash
python3 scripts/validate.py
```

Fix every reported error before going further. Typical causes: a term missing from `data/tags.yaml`, a `device` that is not a device node, a `source_id` that does not resolve, an `evidence_basis` id missing from `sources`, a missing required field.

If any `raw_data` entry uses the external-repository form, also check that each cited file exists at its commit, using a local checkout of that repository (no network is used):

```bash
python3 scripts/check_external_locators.py --checkout <path-to-local-checkout> --repo <repo-url>
```

The script runs `git -C <checkout> cat-file -e <commit>:<locator-without-fragment>` for every external entry whose `repo` is `<repo-url>` (without `--repo`, for every external entry). It prints one `FAIL:` line per entry that does not resolve. Exit codes: 0 when every checked entry resolves, 1 when at least one does not, 2 when the check could not be made, for example because the checkout does not contain a cited commit. Run it once per external repository.

Checklist before moving on:

- `python3 scripts/validate.py` reports 0 errors.
- `python3 scripts/check_external_locators.py --checkout <path> --repo <repo-url>` exits 0 for every external repository cited in `raw_data` (skip when no entry uses the external-repository form).

## Step 6: Regenerate the indices

```bash
python3 scripts/generate-indices.py
```

This rewrites `queries/*.md`. Never edit those files by hand. The generated files are committed with the pages. The generator exits with code 1 if any page is unreadable or has unparseable frontmatter.

## Step 7: Check that the pages are retrievable

```bash
python3 scripts/get_page.py meas-<slug> --frontmatter-only
python3 scripts/get_page.py kernel-<slug> --follow-sources
python3 scripts/query.py --architecture <device-node> --type measurement
python3 scripts/repo_status.py
```

Confirm that the measurement appears under its device in `queries/by-device.md` and the wiki page under its node in `queries/by-architecture.md`.

## Step 8: Update the curated docs

`index.md` and `references/primer.md` are maintained by hand. Replace the relevant "no pages yet" entry with the new page id and path, and update the "Current Contents" section of `SKILL.md` and the status line in `README.md` once the corpus is no longer empty.

## Adding a PR Source Page

Pull-request pages are normally generated, not written by hand. Add or edit a ledger in `candidates/` (see `candidates/README.md`), then:

```bash
python3 scripts/refresh_candidate_ledger.py --cutoff YYYY-MM-DD --repos <slug>
python3 scripts/generate-pr-pages.py --repos <slug>
```

Review the `defer` rows of the ledger by hand: they changed backend host source but no shader. To promote one, set `decision: include` and `decision_source: manual` on the row and run the generator again. A page written by hand follows the rules below.

Same discipline, different fields: create `sources/prs/<repo>/<file>.md` (one directory per repository; all pages in it carry the same `repo`) with an id starting with `pr-`, `source_category: upstream-code`, `status` (`open`, `merged` or `closed`), and `merge_sha` (40 hex characters) when the status is `merged`. The body must contain the verbatim upstream text between these markers:

```markdown
<!-- upstream-excerpt-start -->
<text copied verbatim from the pull request>
<!-- upstream-excerpt-end -->
```
