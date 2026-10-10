# Artifacts

Verbatim upstream material that source pages point at. Nothing here is written or edited by hand.

## `prs/<slug>/`

One directory per candidate ledger (`candidates/<slug>.yaml`):

- `LICENSE`: the upstream repository's licence text. Everything under this directory is distributed under it.
- `PR-<number>/shaders.patch`: the shader-file patches of that pull request as a unified diff. For a ledger with `scope_mode: driver` (Mesa) the file is `driver.patch` and holds the patches of the files under the ledger's driver paths. The hunks are the verbatim patch text the forge returns per file; the `diff --git`, `---` and `+++` header lines are generated so standard tools can read the file. Backend host source of a shader repository is not saved.
- `PR-<number>/PROVENANCE.yaml`: repository, pull request, merge commit, licence, retrieval date, and the sha256 of each file's verbatim patch text. `omitted_files` lists changed files under the saved paths whose patch was left out because the file's own licence header is not the ledger's licence (the ledger's `artifact_exclude_path_markers`), each with the reason.

## `kernels/<bundle>/`

Complete upstream files pinned to one commit, for reading a kernel from top to bottom. `kernels/MANIFEST.yaml` lists the bundles; `scripts/fetch_kernel_files.py` writes them. Each bundle has a `PROVENANCE.yaml` with the repository, commit, licence file and a sha256 per file. Wiki pages quote code from these files and give the file, line range and commit as the locator.

The source-pr page of a pull request names its bundle in `artifact_dir`.

```bash
python3 scripts/fetch_pr_diff.py --repos <slug>      # write missing bundles
python3 scripts/verify_verbatim.py                   # offline integrity check
python3 scripts/grep_wiki.py "<regex>" --only artifacts
```
