# Candidate Ledgers

One YAML ledger per upstream repository. Each ledger records which merged pull requests were looked at and the include / defer / exclude decision for each, so the intake is auditable and repeatable.

- The file name is the ledger slug. Pages generated from `candidates/<slug>.yaml` live in `sources/prs/<slug>/` and carry the id `pr-<slug>-<number>`.
- Ledgers: `llama-cpp.yaml` (GitHub, shaders), `ncnn.yaml` (GitHub, shaders), `mesa.yaml` (GitLab, driver source), `mnn.yaml` (GitHub, shaders).
- The header is written by hand: `repo`, `keywords_used`, `license` (SPDX id, required before any upstream code is saved), `shader_path_markers`, `embedded_shader_path_markers` (optional; files of another language that hold GLSL text), `host_path_markers`, `architecture_code_markers` (optional; maps an identifier in the upstream code to an architecture node, see `scripts/pr_policy.py`). Further optional keys: `forge: gitlab` with `gitlab_api`, `license_path`, `architecture_path_markers`, and `scope_mode: driver` with `driver_path_markers` and `topic_patterns` for a repository of driver source, where a pull request is included when its title matches a topic pattern and it changes a driver path. The scripts fill in `searched_at`, `cutoff_date` and the counts.
- Rows are appended by `scripts/refresh_candidate_ledger.py`. The decision rules are in `scripts/pr_policy.py`: `include` when GLSL shader source was added or modified, `defer` when only backend host source changed, `exclude` otherwise.
- A refresh never changes an existing row. To override a decision, edit the row and add `decision_source: manual`; `--reclassify` leaves such rows alone.
- `scripts/fetch_pr_diff.py` saves the shader patches of `include` rows under `artifacts/prs/<slug>/`.
- `scripts/generate-pr-pages.py` turns `include` rows into source-pr pages. Rows it cannot turn into a valid page are listed in `data/pr-page-skipped.yaml`.

```bash
python3 scripts/refresh_candidate_ledger.py --cutoff YYYY-MM-DD [--repos <slug>]
python3 scripts/fetch_pr_diff.py [--repos <slug>]
python3 scripts/generate-pr-pages.py [--repos <slug>]
python3 scripts/validate.py && python3 scripts/verify_verbatim.py && python3 scripts/generate-indices.py
```

Both scripts call the GitHub API through the `gh` CLI and cache what they fetch under `.cache/pr-evidence/`, which git ignores.

## Manual review

A `defer` row changed backend host source but no shader. It is resolved by hand: set `decision` to `include` or `exclude`, give the `reason`, and add `decision_source: manual` and `reviewed_at`. In `llama-cpp.yaml` the 245 rows of this kind were reviewed on 2026-10-05 from their titles and changed paths: 65 were included (kernel selection, tile or subgroup tuning, shared-memory fit, device-specific kernel workarounds) and 180 excluded (memory, device setup, submission, build, logging, operator plumbing). In `ncnn.yaml` the 60 rows of this kind were reviewed the same way: 18 included, 42 excluded. In `mesa.yaml` 10 rows the rule had included were excluded by hand (stable-branch backports, the OpenGL driver, other vendors' drivers, a CI list, per-game profiles). The patches were not read for these reviews; correct a row if its diff says otherwise.

In `mnn.yaml` the review of 2026-10-10 went both ways, because much of MNN's Vulkan work reaches GitHub as direct pushes or internal-sync pull requests rather than as one pull request per change: 12 rows the rule had included were excluded (shader changes outside matmul, linear, attention and quantization), and of the 42 host-only rows 1 was included (the GEMM benchmark) and 41 excluded. Vulkan changes that have no pull request (the first cooperative-matrix Conv1x1, LLM inference support, the W8A8 cooperative-matrix path, the no-subgroup fallbacks) are covered by the release-note pages `sources/docs/mnn-release-*.md` and by the `mnn-*` bundles in `artifacts/kernels/`.
