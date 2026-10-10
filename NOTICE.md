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
| `sources/prs/mnn/`, `artifacts/prs/mnn/` | https://github.com/alibaba/MNN | Apache-2.0, Copyright (c) 2018 Alibaba Group Holding Limited; the upstream repository has no `NOTICE` file; the saved files are unmodified | `artifacts/prs/mnn/LICENSE` (upstream `LICENSE.txt`) |
| `sources/prs/vk-coopmat-perf/`, `artifacts/prs/vk-coopmat-perf/` | https://github.com/jeffbolznv/vk_cooperative_matrix_perf | MIT, Copyright (c) 2019-2025 NVIDIA CORPORATION & AFFILIATES | `artifacts/prs/vk-coopmat-perf/LICENSE` (upstream `LICENSE`) |
| `sources/prs/glslang/` (description excerpts only; no patches are saved) | https://github.com/KhronosGroup/glslang | several licences per file (BSD-3-Clause, BSD-2-Clause, MIT, Apache-2.0 and others; GitHub reports no single SPDX id), Copyright The Khronos Group Inc. and contributors | upstream `LICENSE.txt` (not copied) |
| `sources/prs/spirv-tools/` (description excerpts only; no patches are saved) | https://github.com/KhronosGroup/SPIRV-Tools | Apache-2.0, Copyright The Khronos Group Inc. and contributors | upstream `LICENSE` (not copied) |
| `artifacts/kernels/adreno-cooperative-matrix-sample/` | https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework | BSD-3-Clause, Copyright (c) Qualcomm Innovation Center, Inc. | `artifacts/prs/adreno-samples/LICENSE` (upstream `LICENSE.txt`) |

Mesa licence check of 2026-10-10 (upstream commit `5c80eda3f1c0ac7cb80b0597473ae83da4b97c08`): `licenses/MIT` is byte-identical to `artifacts/prs/mesa/LICENSE`; `docs/license.rst` says "Most of the Mesa code is licensed under MIT license, but individual files may have their own licenses" and "In general, consult each source file SPDX identifier for license terms". Each of the 241 files patched by the 92 merge-request bundles added that day (Intel, NVIDIA, Qualcomm and Arm drivers and compilers) was read at that commit, or at the merge commit when it no longer exists: 239 carry `SPDX-License-Identifier: MIT` or the MIT permission text. `src/intel/compiler/brw_disasm.c` carries a different permission notice (Copyright 2008 Keith Packard) and `src/intel/compiler/brw_lex.l` has no licence header; the ledger lists both in `artifact_exclude_path_markers`, their patches are not saved, and the four affected bundles name them under `omitted_files`.

`artifacts/kernels/<bundle>/` holds complete upstream files from the repositories in the table above that have a licence text under `artifacts/prs/`, pinned to a commit and under the same licences; each bundle's `PROVENANCE.yaml` names the repository, commit and licence file. The `mnn-*` bundles hold MNN's Vulkan shaders, their host-side selection code and, in `mnn-vulkan-optimize-notes`, two of its optimization documents (written in Chinese), all Apache-2.0 and byte for byte as upstream.

`sources/docs/` and `sources/blogs/` hold short verbatim excerpts, each with a link to its source and remaining the work of its authors: the Vulkan-Docs proposals, extension appendices and specification chapters (https://github.com/KhronosGroup/Vulkan-Docs), the Vulkan Guide chapter (https://github.com/KhronosGroup/Vulkan-Guide) and the OpenGL Shading Language specification chapters (https://github.com/KhronosGroup/GLSL, `chapters/`) are CC-BY-4.0 (Copyright The Khronos Group Inc.; the Vulkan-Docs Shaders chapter also carries Copyright (c) 2020-2021 NVIDIA Corporation); the GLSL extension specifications (`GLSL_KHR_cooperative_matrix.txt`, `GL_KHR_shader_subgroup.txt`) are Copyright The Khronos Group Inc. under the terms at http://www.khronos.org/registry/speccopyright.html, are marked `LicenseRef-Proprietary` in that repository's `REUSE.toml`, and are quoted in short excerpts only; the Mesa documentation is MIT; the MNN release notes and optimization handbook are by the MNN contributors (repository licence Apache-2.0); the two blog posts are quoted paragraph by paragraph with attribution and are not relicensed; the Intel Graphics Compiler vISA documentation is MIT (Copyright (C) 2020-2022 Intel Corporation; pinned commit and file named on the page). The vendor material is quoted in short excerpts with attribution, is not relicensed and remains the property of its publisher: the NVIDIA Vulkanised 2025 slide deck, the NVIDIA developer blog post and the NVIDIA Vulkan driver release notes (NVIDIA Corporation); the oneAPI GPU Optimization Guide pages (Intel Corporation); the GPUOpen articles, the RDNA performance guide and the RDNA 3 slide deck (Advanced Micro Devices, Inc.).

Further `sources/docs/` pages quote short passages of upstream source files and documents at a pinned commit, each under the upstream licence named at the foot of the page: Vulkan-ValidationLayers and VK-GL-CTS (Apache-2.0, Copyright The Khronos Group Inc., Valve Corporation, LunarG, Inc. and contributors), the Adreno GPU Vulkan code sample framework (BSD-3-Clause, Copyright Qualcomm Innovation Center, Inc.), libGPUCounters (MIT, Copyright Arm Limited), IREE (Apache-2.0 WITH LLVM-exception), Apache TVM (Apache-2.0), ONNX Runtime (MIT, Copyright Microsoft Corporation), CubeK and wonnx (MIT OR Apache-2.0), and the WebLLM paper (CC-BY 4.0, copyright its authors). The Vulkanised 2025 slide deck, the MLC blog post and the GitHub issue and discussion threads under `sources/blogs/` are quoted with attribution to their authors and are not relicensed; the slide deck itself is not stored here.

Each `artifacts/prs/<slug>/PR-<number>/PROVENANCE.yaml` records the pull request, its merge commit, the retrieval date and a sha256 per file.

## PyYAML

`scripts/_vendor/yaml/` is a bundled copy of the pure-Python portion of PyYAML, taken over from KernelWiki and used as a fallback when the host Python has no PyYAML installed. It is distributed under the MIT license.

- License text: `scripts/_vendor/LICENSE`
- Description of the bundled copy: `scripts/_vendor/README.md`
