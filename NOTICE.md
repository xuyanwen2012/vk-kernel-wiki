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
| `sources/prs/mesa/`, `artifacts/prs/mesa/` | https://gitlab.freedesktop.org/mesa/mesa | MIT; copyright notices are in the headers of the upstream files. Mesa states that most of its code is MIT but individual files may carry their own licence (`docs/license.rst`); the patches of two files that do not carry the MIT text (`brw_disasm.c`, `brw_lex.l`) are not saved, see below | `artifacts/prs/mesa/LICENSE` (upstream `licenses/MIT`) |

Mesa licence check of 2026-10-10 (upstream commit `5c80eda3f1c0ac7cb80b0597473ae83da4b97c08`): `licenses/MIT` is byte-identical to `artifacts/prs/mesa/LICENSE`; `docs/license.rst` says "Most of the Mesa code is licensed under MIT license, but individual files may have their own licenses" and "In general, consult each source file SPDX identifier for license terms". Each of the 241 files patched by the 92 merge-request bundles added that day (Intel, NVIDIA, Qualcomm and Arm drivers and compilers) was read at that commit, or at the merge commit when it no longer exists: 239 carry `SPDX-License-Identifier: MIT` or the MIT permission text. `src/intel/compiler/brw_disasm.c` carries a different permission notice (Copyright 2008 Keith Packard) and `src/intel/compiler/brw_lex.l` has no licence header; the ledger lists both in `artifact_exclude_path_markers`, their patches are not saved, and the four affected bundles name them under `omitted_files`.

`artifacts/kernels/<bundle>/` holds complete upstream files from the same three repositories, pinned to a commit and under the same licences; each bundle's `PROVENANCE.yaml` names the repository, commit and licence file.

`sources/docs/` and `sources/blogs/` hold short verbatim excerpts, each with a link to its source and remaining the work of its authors: the Vulkan-Docs proposals are CC-BY-4.0 (Copyright The Khronos Group Inc.); the GLSL extension specification is Copyright The Khronos Group Inc. under the terms at http://www.khronos.org/registry/speccopyright.html; the Mesa documentation is MIT; the two blog posts are quoted paragraph by paragraph with attribution and are not relicensed.

Each `artifacts/prs/<slug>/PR-<number>/PROVENANCE.yaml` records the pull request, its merge commit, the retrieval date and a sha256 per file.

## PyYAML

`scripts/_vendor/yaml/` is a bundled copy of the pure-Python portion of PyYAML, taken over from KernelWiki and used as a fallback when the host Python has no PyYAML installed. It is distributed under the MIT license.

- License text: `scripts/_vendor/LICENSE`
- Description of the bundled copy: `scripts/_vendor/README.md`
