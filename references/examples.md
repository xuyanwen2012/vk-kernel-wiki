# Worked Query Examples

Patterns for turning a user question into a command sequence. All commands run from the repository root and are valid against the current scripts.

The corpus currently holds pages for one device only, the Radeon 780M (`radeon-780m`). A command below that filters on another device or on a page type with no pages prints `No matching pages.` Placeholders in angle brackets (`<page-id>`) stand for ids that the previous command returns; `index.md` lists the page ids that exist.

---

## Example 1: "What do we know about cooperative-matrix linear kernels on RDNA3?"

**Navigation path**:
1. Filter kernel pages by tag and architecture node.
2. Read stderr: it reports how many pages tagged only `amd` were left out.
3. Open each result and follow its sources.

**Commands**:
```bash
python3 scripts/query.py --tag cooperative-matrix --type kernel --architecture rdna3
python3 scripts/get_page.py <page-id> --follow-sources
```

`--architecture rdna3` returns pages tagged `rdna3` or any of its devices. If the stderr note reports excluded pages, rerun with `--architecture amd` to see the vendor-level pages as well.

---

## Example 2: "Show me the measurements we have for the 780M"

**Navigation path**:
1. Ask for measurement pages on the device, using the alias.
2. Or read the generated per-device index, which lists driver and date per measurement.
3. Open a measurement page to get the raw-data locators.

**Commands**:
```bash
python3 scripts/query.py --architecture 780M --type measurement
python3 scripts/generate-indices.py
python3 scripts/get_page.py meas-<slug> --frontmatter-only
```

stderr shows `Architecture '780M' resolved to 'radeon-780m'.` Then read the `radeon-780m` section of `queries/by-device.md`. Report every number with its device, driver version and `measured_at` date.

---

## Example 3: "Is there anything specific to one device that the generation-level pages miss?"

**Navigation path**:
1. Query the device node; note the excluded count on stderr.
2. Query the generation node, then the vendor node, and compare.

**Commands**:
```bash
python3 scripts/query.py --architecture rx-7900-xtx --compact
python3 scripts/query.py --architecture rdna3 --compact
python3 scripts/query.py --architecture amd --compact --limit 50
```

A device query never returns pages tagged only with `rdna3` or `amd`. Treat those broader pages as not confirmed for the device unless a source says so.

---

## Example 4: "My kernel shows a specific symptom; what should I try?"

**Navigation path**:
1. List the pattern pages to see which symptoms are recorded. `--symptom` is an exact match on a page's `symptoms` entries, so copy the string from a pattern page.
2. Filter by that symptom.
3. Open the pattern page and each id in its `candidate_techniques`.

**Commands**:
```bash
python3 scripts/query.py --type pattern --limit 50
python3 scripts/query.py --symptom "<exact symptom string>"
python3 scripts/get_page.py pattern-<slug>
python3 scripts/get_page.py technique-<slug>
```

`queries/by-problem.md` gives the same symptom, pattern, candidate-technique mapping as one table.

---

## Example 5: "Where is double buffering used?"

**Navigation path**:
1. Tag filter with the canonical term; `--tag` checks `tags`, `techniques`, `hardware_features`, `kernel_types` and `languages`.
2. Text search for places that mention it without tagging it.

**Commands**:
```bash
python3 scripts/query.py --tag double-buffering --limit 30
python3 scripts/query.py --tag dbuf4 --compact
python3 scripts/grep_wiki.py "double.buffer" --only wiki --context 2
```

The second command shows alias resolution: `dbuf4` is listed under `double-buffering` in `data/aliases.yaml`.

---

## Example 6: "Which upstream PRs touched the attention kernels?"

**Navigation path**:
1. Filter PR source pages by kernel type, optionally by repository.
2. Open a PR page; its body holds the verbatim upstream excerpt.

**Commands**:
```bash
python3 scripts/query.py --type pr --tag sdpa --limit 30
python3 scripts/query.py --type pr --tag sdpa-qk --repo <repo-name-fragment>
python3 scripts/get_page.py pr-<slug> --body-only
```

`--repo` is a case-insensitive partial match on the page's `repo` field. `queries/by-repo.md` groups all PR pages by repository.

---

## Example 7: "Which claims are actually verified, and by what?"

**Navigation path**:
1. Filter by confidence.
2. Read the page's `evidence_basis` to see whether it is backed by a first-party measurement or by official documentation plus upstream code.
3. Follow the cited source ids.

**Commands**:
```bash
python3 scripts/query.py --confidence verified --type technique
python3 scripts/get_page.py <page-id> --frontmatter-only
python3 scripts/get_page.py <page-id> --follow-sources
```

When answering, state the confidence level of each page you rely on, and flag `inferred` and `experimental` pages explicitly.

---

## Example 8: "Find every mention of a driver or extension name"

**Navigation path**:
1. Regex search across wiki and source files; several patterns must match the same line unless `--any` is given.
2. Widen to raw data files stored next to source pages with `--ext`.

**Commands**:
```bash
python3 scripts/grep_wiki.py "RADV" --only sources --files-only
python3 scripts/grep_wiki.py "VK_EXT_subgroup_size_control" "GL_KHR_cooperative_matrix" --any
python3 scripts/grep_wiki.py "RADV" --only sources --ext json,csv,txt
```

---

## Reporting a Performance Claim

When a kernel page carries `performance_claims`, report every required field, never a bare number:

- `gpu`, `driver` (name and version), `dtype`, `shape`, `metric`, `value`, `measured_at`
- `source_id` and `source_locator`, so the reader can open the source page and find the number
- `baseline`, when the claim has one

```bash
python3 scripts/get_page.py kernel-<slug> --frontmatter-only
python3 scripts/get_page.py <source_id>
```

If a claim lacks a field, say so instead of filling it in.
