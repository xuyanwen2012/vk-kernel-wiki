# Artifacts

Verbatim upstream material that source pages point at. Nothing here is written or edited by hand.

## `prs/<slug>/`

One directory per candidate ledger (`candidates/<slug>.yaml`):

- `LICENSE`: the upstream repository's licence text. Everything under this directory is distributed under it.
- `PR-<number>/shaders.patch`: the shader-file patches of that pull request as a unified diff. For a ledger with `scope_mode: driver` (Mesa) the file is `driver.patch` and holds the patches of the files under the ledger's driver paths. The hunks are the verbatim patch text the forge returns per file; the `diff --git`, `---` and `+++` header lines are generated so standard tools can read the file. Backend host source of a shader repository is not saved.
- `PR-<number>/PROVENANCE.yaml`: repository, pull request, merge commit, licence, retrieval date, and the sha256 of each file's verbatim patch text.

The source-pr page of a pull request names its bundle in `artifact_dir`.

```bash
python3 scripts/fetch_pr_diff.py --repos <slug>      # write missing bundles
python3 scripts/verify_verbatim.py                   # offline integrity check
python3 scripts/grep_wiki.py "<regex>" --only artifacts
```
