# Notice

## License of this repository

This repository's own content (scripts, schemas, wiki pages, measurement pages and documentation) is distributed under the MIT license; see [`LICENSE`](LICENSE). The third-party components below keep their own licenses.

## KernelWiki

The directory structure, page schema layout, and the scripts under `scripts/` are derived from KernelWiki by mit-han-lab, which is distributed under the MIT license.

- Upstream revision the derivation started from: `third_party/KernelWiki-REVISION`
- Upstream license text: `third_party/KernelWiki-LICENSE`

The derived files have been modified for this repository: the subject matter, controlled vocabulary, architecture model, page types and validation rules differ from upstream. No knowledge pages were copied from KernelWiki.

## Upstream pull-request material

`sources/prs/<slug>/` holds short verbatim excerpts of upstream pull-request descriptions, each with a link to the pull request. `artifacts/prs/<slug>/` holds verbatim shader patches from those pull requests. Both remain the work of their upstream authors and are distributed under the upstream licence, not under this repository's own terms.

| Directory | Upstream | Licence | Licence text |
|---|---|---|---|
| `sources/prs/llama-cpp/`, `artifacts/prs/llama-cpp/` | https://github.com/ggml-org/llama.cpp | MIT, Copyright (c) 2023-2026 The ggml authors | `artifacts/prs/llama-cpp/LICENSE` |
| `sources/prs/ncnn/`, `artifacts/prs/ncnn/` | https://github.com/Tencent/ncnn | BSD-3-Clause, Copyright (C) 2017 Tencent; the saved files are ncnn's own shader sources, not the third-party components its licence file lists | `artifacts/prs/ncnn/LICENSE` (upstream `LICENSE.txt`) |
| `sources/prs/mesa/`, `artifacts/prs/mesa/` | https://gitlab.freedesktop.org/mesa/mesa | MIT; copyright notices are in the headers of the upstream files | `artifacts/prs/mesa/LICENSE` (upstream `licenses/MIT`) |

Each `artifacts/prs/<slug>/PR-<number>/PROVENANCE.yaml` records the pull request, its merge commit, the retrieval date and a sha256 per file.

## PyYAML

`scripts/_vendor/yaml/` is a bundled copy of the pure-Python portion of PyYAML, taken over from KernelWiki and used as a fallback when the host Python has no PyYAML installed. It is distributed under the MIT license.

- License text: `scripts/_vendor/LICENSE`
- Description of the bundled copy: `scripts/_vendor/README.md`
