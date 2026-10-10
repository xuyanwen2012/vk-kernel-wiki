# Topic Map / Primer

A map of the knowledge base, organised by the controlled vocabulary in `data/tags.yaml` and the architecture tree in `data/architectures.yaml`. Use it when a question is broad: find the area, then query by the term shown.

**Current corpus: 597 pages, including 4 official-document pages, 2 blog pages and 1 language page that are not tied to the 780M. 18 of them (5 source-measurement pages, 13 wiki pages) are tagged with the single device node `radeon-780m`; the other 572 are generated pull-request pages from `ggml-org/llama.cpp`, `Tencent/ncnn` and `mesa/mesa`.** The tables below list measurement and wiki pages by id. Pull-request pages are not listed by id; where a term or node has only pull-request pages the table says so and names the generated index. Every measurement page carries the driver RADV Mesa 25.2.7; the measurement dates recorded on the pages are 2026-09-01 (`meas-780m-vulkaninfo`), 2026-09-27 (`meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`) and 2026-09-28 (`meas-780m-e2e-prefill`). For `meas-780m-8da4w-port` and `meas-780m-sdpa-port` the driver version is attributed from the package install history captured on the device on 2026-10-04 (`sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`); the runs themselves record the driver name without a version. A term or node marked "no pages yet" has no page. A page listed next to a term carries that term in its frontmatter; the listing is not a claim about behaviour or performance, and nothing here is established for any other device, driver or date. The one-line descriptions repeat the term definitions in `data/tags.yaml`.

Query any term with `python3 scripts/query.py --tag <term>`, and any node with `python3 scripts/query.py --architecture <node>`. Aliases for each are in `data/aliases.yaml`.

---

## Architectures

Any node name is a valid value of the `architectures` field. Asking for a node returns pages tagged with it or any descendant, never pages tagged only with an ancestor.

| Node | Kind | Parent | Pages |
|---|---|---|---|
| `amd` | vendor | | pull-request pages only; list: `queries/by-architecture.md` |
| `rdna3` | generation | `amd` | pull-request pages only; list: `queries/by-architecture.md` |
| `radeon-780m` | device | `rdna3` | 18 pages (5 source-measurement, 13 wiki); list: `queries/by-architecture.md` |
| `rx-7900-xtx` | device | `rdna3` | no pages yet |
| `rx-7600` | device | `rdna3` | no pages yet |
| `intel` | vendor | | pull-request pages only; list: `queries/by-architecture.md` |
| `xe2` | generation | `intel` | pull-request pages only; list: `queries/by-architecture.md` |
| `arc-b580` | device | `xe2` | no pages yet |
| `arc-pro-b70` | device | `xe2` | no pages yet |
| `meteor-lake` | generation | `intel` | pull-request pages only; list: `queries/by-architecture.md` |
| `xe3` | generation | `intel` | pull-request pages only; list: `queries/by-architecture.md` |
| `nvidia` | vendor | | pull-request pages only; list: `queries/by-architecture.md` |
| `rtx-4070-ti-super` | device | `nvidia` | no pages yet |
| `jetson-orin` | device | `nvidia` | no pages yet |
| `turing` | generation | `nvidia` | pull-request and document pages only; list: `queries/by-architecture.md` |
| `ampere` | generation | `nvidia` | pull-request pages only; list: `queries/by-architecture.md` |
| `blackwell` | generation | `nvidia` | pull-request pages only; list: `queries/by-architecture.md` |
| `qualcomm` | vendor | | pull-request pages only; list: `queries/by-architecture.md` |
| `adreno-840` | device | `qualcomm` | no pages yet |
| `adreno-7xx` | generation | `qualcomm` | pull-request pages only; list: `queries/by-architecture.md` |
| `arm` | vendor | | pull-request pages only; list: `queries/by-architecture.md` |
| `mali-g1` | device | `arm` | no pages yet |
| `bifrost` | generation | `arm` | pull-request pages only; list: `queries/by-architecture.md` |
| `samsung` | vendor | | reserved, no devices |

All measurement and wiki pages are tagged with the device node `radeon-780m` only, so a query for `rdna3` or `amd` returns them as descendants. Some pull-request pages are tagged with a vendor or generation node taken from the pull-request title or from a device check the pull request adds to the code. Measurements per device are indexed in `queries/by-device.md`.

---

## Hardware Features (`hardware_features`)

Pages live in `wiki/hardware/` (id prefix `hw-`). Index: `queries/by-hardware-feature.md`.

### Cooperative matrix

| Term | Meaning (from `data/tags.yaml`) | Pages |
|---|---|---|
| `cooperative-matrix` | VK_KHR_cooperative_matrix / GL_KHR_cooperative_matrix | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `meas-780m-vulkaninfo`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `pattern-coopmat-name-check-false-failure`, `pattern-sdpa-release-gap`, `pattern-unaligned-m-fallback`, `technique-drain-in-a-staging`, `technique-fp32-accumulation`, `technique-full-a-map`, `technique-workgroup-tile-sizing` |
| `int8-cooperative-matrix` | an int8 cooperative-matrix shape is enumerated | pull-request pages only; list: `queries/by-hardware-feature.md` |
| `cooperative-matrix2` | VK_NV_cooperative_matrix2 / GL_NV_cooperative_matrix2 | pull-request pages only; list: `queries/by-hardware-feature.md` |
| `coopmat-shape` | the M x N x K shapes a device exposes | `hw-cooperative-matrix-rdna3` |
| `coopmat-fp32-accumulator` | fp32 accumulator matrix for fp16 operands | `hw-cooperative-matrix-rdna3`, `kernel-linear-4w-780m`, `kernel-sdpa-prefill-780m`, `technique-fp32-accumulation` |

### Subgroups

| Term | Meaning | Pages |
|---|---|---|
| `subgroup-size` | default subgroup size of the device | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`, `meas-780m-vulkaninfo`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `subgroup-size-control` | VK_EXT_subgroup_size_control (required size per pipeline) | `meas-780m-vulkaninfo`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m` |
| `wave64` | adapters whose native subgroup is 64 lanes | `meas-780m-8da4w-port`, `meas-780m-vulkaninfo`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `subgroup-operations` | GL_KHR_shader_subgroup operations a driver exposes (VkPhysicalDeviceSubgroupProperties) | pull-request pages only; list: `queries/by-hardware-feature.md` |

### Memory and storage

| Term | Meaning | Pages |
|---|---|---|
| `shared-memory-limit` | maxComputeSharedMemorySize | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-vulkaninfo`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m` |
| `storage-buffer` | tensor stored as a buffer (SSBO) | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `storage-texture3d` | tensor stored as a 3D texture | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `technique-drain-in-a-staging` |
| `storage-texture2d` | packed weights stored as a 2D texture | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m` |

### Shader arithmetic and constants

| Term | Meaning | Pages |
|---|---|---|
| `fp16-arithmetic` | GL_EXT_shader_explicit_arithmetic_types_float16 | `meas-780m-vulkaninfo`, `hw-radeon-780m` |
| `bfloat16-arithmetic` | GL_EXT_bfloat16 (bf16 scalars, vectors and matrix components) | pull-request pages only; list: `queries/by-hardware-feature.md` |
| `int8-arithmetic` | GL_EXT_shader_explicit_arithmetic_types_int8 | `meas-780m-vulkaninfo`, `hw-radeon-780m`, `kernel-linear-8da4w-780m` |
| `8bit-storage` | GL_EXT_shader_8bit_storage | `meas-780m-vulkaninfo`, `hw-radeon-780m` |
| `integer-dot-product` | GL_EXT_integer_dot_product | `meas-780m-vulkaninfo`, `hw-radeon-780m` |
| `specialization-constants` | local_size_*_id and spec-constant shape parameters | pull-request pages only; list: `queries/by-hardware-feature.md` |

---

## Optimization Techniques (`techniques`)

Pages live in `wiki/techniques/` (id prefix `technique-`). Index: `queries/by-technique.md`.

### Tile geometry

| Term | Meaning | Pages |
|---|---|---|
| `workgroup-tile-sizing` | output tile per workgroup (M x N) | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `pattern-unaligned-m-fallback`, `technique-workgroup-tile-sizing` |
| `k-chunk-sizing` | K consumed per main-loop iteration | `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `subgroup-grid` | subgroup grid inside the workgroup | `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `technique-workgroup-tile-sizing` |
| `required-subgroup-size` | pipeline pinned to one subgroup size | `meas-780m-8da4w-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `mma-shape-selection` | shape of one cooperative-matrix multiply-add | no pages yet |
| `per-shape-tile-selection` | different tiles for different operator shapes | no pages yet |

### Accumulation precision

| Term | Meaning | Pages |
|---|---|---|
| `fp32-accumulation` | fp32 accumulator matrix | `meas-780m-4w-bootstrap`, `meas-780m-e2e-prefill`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `technique-fp32-accumulation` |
| `group-fp32-accumulation` | fp16 within a quantization group, fp32 running total | no pages yet |
| `register-fp32-total` | fp32 running total kept in per-invocation registers | no pages yet |

### Shared-memory staging and pipeline

| Term | Meaning | Pages |
|---|---|---|
| `double-buffering` | ping-pong shared-memory slices, prefetch ahead of the multiply | `meas-780m-8da4w-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `technique-full-a-map` |
| `shared-memory-fence` | explicit ordering of shared stores against matrix loads | no pages yet |
| `fragment-contiguous-layout` | unpadded, fragment-contiguous shared-memory layout | no pages yet |
| `f16vec4-shared-memory` | shared memory stored as f16vec4 | no pages yet |
| `shared-memory-pool` | operands and output drain share one pool | no pages yet |
| `storage-image-loads` | imageLoad instead of sampler fetches | no pages yet |
| `column-major-b-staging` | B staged N-major and loaded column-major | no pages yet |
| `full-a-map` | each thread stages exactly one A block | `meas-780m-8da4w-port`, `kernel-linear-8da4w-780m`, `technique-full-a-map` |
| `multi-block-a-staging` | each thread stages several A blocks | no pages yet |
| `raw-a-staging` | A copied to shared memory as raw words | no pages yet |
| `paired-b-nibbles` | one weight texel feeds both nibble parities | no pages yet |
| `early-b-select` | keep only the selected weight word after the fetch | no pages yet |

### Output drain (texture3d output)

| Term | Meaning | Pages |
|---|---|---|
| `drain-in-a-staging` | drain staged in the dead A shared-memory region | `meas-780m-4w-bootstrap`, `kernel-linear-4w-780m`, `technique-drain-in-a-staging` |
| `full-tile-drain` | whole tile staged and drained in one pass | no pages yet |
| `band-drain` | one subgroup-grid band drained at a time | no pages yet |
| `drain-unroll` | hand-expanded drain loop with constant indices | no pages yet |

### Quantization handling

| Term | Meaning | Pages |
|---|---|---|
| `zero-point-hoisting` | zero-point correction moved out of the group loop | `meas-780m-8da4w-port`, `kernel-linear-8da4w-780m` |
| `group-sums` | per-group sums computed when activations are packed | no pages yet |
| `row-major-activations` | row-major packed int8 activations | no pages yet |

### Attention

| Term | Meaning | Pages |
|---|---|---|
| `causal-truncation` | skip work above the causal diagonal | `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-causal-truncation` |

### Stated in upstream pull requests

| Term | Meaning | Pages |
|---|---|---|
| `split-k-reduction` | K split across workgroups, partial sums reduced in a second pass | pull-request pages only; list: `queries/by-technique.md` |
| `kernel-fusion` | several operators merged into one dispatch | pull-request pages only; list: `queries/by-technique.md` |
| `device-specific-tuning` | parameters or kernel choice tuned per vendor, generation or device | pull-request pages only; list: `queries/by-technique.md` |
| `driver-workaround` | a path disabled or changed because of a driver or compiler defect | pull-request pages only; list: `queries/by-technique.md` |
| `winograd-convolution` | 3x3 convolution through the Winograd transform | pull-request pages only; list: `queries/by-technique.md` |
| `channel-packing` | channels packed into vec4/vec8 elements (pack4, pack8) | pull-request pages only; list: `queries/by-technique.md` |

---

## Kernel Case Studies (`kernel_types`)

Pages live in `wiki/kernels/` (id prefix `kernel-`). Index: `queries/by-kernel-type.md`. Kernel pages carry `performance_claims`: `kernel-linear-4w-780m` (93 claims, measured 2026-09-27 and 2026-09-28), `kernel-linear-8da4w-780m` (88 claims, measured 2026-09-27 and 2026-09-28) and `kernel-sdpa-prefill-780m` (84 claims, measured 2026-09-27 and 2026-09-28), all on `radeon-780m` with RADV Mesa 25.2.7. Read the numbers from the pages; this file repeats none.

### Matrix products

| Term | Meaning | Pages |
|---|---|---|
| `gemm` | | `meas-780m-e2e-prefill`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `technique-drain-in-a-staging`, `technique-fp32-accumulation`, `technique-workgroup-tile-sizing` |
| `gemv` | | pull-request pages only; list: `queries/by-kernel-type.md` |

### Quantized linear

| Term | Meaning | Pages |
|---|---|---|
| `linear-4w` | fp16 activations, 4-bit group-symmetric weights | `meas-780m-4w-bootstrap`, `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-linear-4w-780m`, `pattern-sdpa-release-gap`, `pattern-unaligned-m-fallback`, `technique-drain-in-a-staging`, `technique-fp32-accumulation`, `technique-workgroup-tile-sizing` |
| `linear-8da4w` | dynamic int8 activations, 4-bit weights | `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-linear-8da4w-780m`, `pattern-coopmat-name-check-false-failure`, `pattern-sdpa-release-gap`, `technique-full-a-map` |
| `linear-8da4w-zpg` | 8da4w family reading 4h4w activation blocks | `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-linear-8da4w-780m`, `pattern-coopmat-name-check-false-failure`, `pattern-unaligned-m-fallback`, `technique-full-a-map`, `technique-workgroup-tile-sizing` |
| `linear-8da4w-zpgtr` | 8da4w family reading row-major activations | no pages yet |
| `tiled-linear` | non-cooperative-matrix tiled baseline / fallback | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `pattern-coopmat-name-check-false-failure`, `pattern-unaligned-m-fallback` |
| `quantize-and-pack` | activation quantization and packing | `meas-780m-8da4w-port`, `kernel-linear-8da4w-780m` |

### Attention

| Term | Meaning | Pages |
|---|---|---|
| `sdpa` | scaled dot-product attention | `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-causal-truncation` |
| `sdpa-qk` | attention weights, Q K^T | `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-workgroup-tile-sizing` |
| `sdpa-av` | attention output, attn V | `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-workgroup-tile-sizing` |
| `sdpa-softmax` | attention-weight softmax | `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-causal-truncation` |

### Inference phase

| Term | Meaning | Pages |
|---|---|---|
| `prefill` | | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `pattern-coopmat-name-check-false-failure`, `pattern-sdpa-release-gap`, `pattern-unaligned-m-fallback`, `technique-causal-truncation`, `technique-drain-in-a-staging`, `technique-fp32-accumulation`, `technique-full-a-map`, `technique-workgroup-tile-sizing` |
| `decode` | | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port` |

### Other operator families (upstream pull requests)

| Term | Meaning | Pages |
|---|---|---|
| `moe` | mixture-of-experts routing and per-expert matrix products | pull-request pages only; list: `queries/by-kernel-type.md` |
| `convolution` | conv1d/2d/3d, transposed convolution, im2col / col2im | pull-request pages only; list: `queries/by-kernel-type.md` |
| `dequantize` | quantized weight blocks expanded to float | pull-request pages only; list: `queries/by-kernel-type.md` |
| `rope` | rotary position embedding | pull-request pages only; list: `queries/by-kernel-type.md` |
| `normalization` | RMS, L2, group and layer normalization | pull-request pages only; list: `queries/by-kernel-type.md` |
| `softmax` | standalone softmax | pull-request pages only; list: `queries/by-kernel-type.md` |
| `topk-sort` | argsort, argmax and top-k selection | pull-request pages only; list: `queries/by-kernel-type.md` |
| `gated-delta-net` | gated delta-rule linear attention | pull-request pages only; list: `queries/by-kernel-type.md` |
| `tensor-copy` | copy, type conversion, row gather/scatter, concat, pad, repeat | pull-request pages only; list: `queries/by-kernel-type.md` |
| `elementwise` | unary and binary elementwise operators and activations | pull-request pages only; list: `queries/by-kernel-type.md` |

---

## Languages (`languages`)

Pages live in `wiki/languages/` (id prefix `lang-`). Index: `queries/by-language.md`.

| Term | Pages |
|---|---|
| `glsl` | `lang-glsl-cooperative-matrix`, `doc-glsl-khr-cooperative-matrix`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `spirv` | no pages yet |
| `cpp` | pull-request pages only; list: `queries/by-language.md` |
| `c` | pull-request pages only; list: `queries/by-language.md` |
| `python` | pull-request pages only; list: `queries/by-language.md` |
| `rust` | pull-request pages only; list: `queries/by-language.md` |

---

## Problem Diagnosis (`wiki/patterns/`)

Pattern pages map `symptoms` to `candidate_techniques` (id prefix `pattern-`). Symptoms are free text on each pattern page, not a controlled group in `data/tags.yaml`. Three pages: `pattern-unaligned-m-fallback` (`wiki/patterns/unaligned-m-fallback.md`), `pattern-sdpa-release-gap` (`wiki/patterns/sdpa-release-gap.md`) and `pattern-coopmat-name-check-false-failure` (`wiki/patterns/coopmat-name-check-false-failure.md`). Index: `queries/by-problem.md`.

## Migration Notes (`wiki/migration/`)

Migration pages describe porting a kernel from one architecture node to another (`from_arch`, `to_arch`; id prefix `migration-`). No pages yet.

---

## Sources

| Source type | Directory | `source_category` values | Pages |
|---|---|---|---|
| First-party measurement | `sources/measurements/` | `measurement` | `meas-780m-vulkaninfo`, `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`, `meas-780m-e2e-prefill` |
| Upstream pull request | `sources/prs/` | `upstream-code` | 572 generated pages in `sources/prs/llama-cpp/`, `sources/prs/ncnn/` and `sources/prs/mesa/`; list: `queries/by-repo.md` |
| Documentation and papers | `sources/docs/` | `official-doc` (specification-grade), `upstream-code` (another project's source files), `vendor-doc` (vendor and project articles, guides, slide decks), `paper` | `doc-vk-khr-cooperative-matrix-proposal`, `doc-vk-nv-cooperative-matrix2-proposal`, `doc-glsl-khr-cooperative-matrix`, `doc-mesa-radv-envvars` |
| Blogs and notes | `sources/blogs/` | `benchmark-blog`, `community-note` | `blog-themaister-fsr4-wmma`, `blog-zolotukhin-matrix-cores-decode` |

First-party measurements are the most trusted source type. Index per device: `queries/by-device.md`. PR pages per repository: `queries/by-repo.md`.

---

## Confidence and Evidence

| Group | Values |
|---|---|
| `confidence` | `verified`, `source-reported`, `inferred`, `experimental` |
| `reproducibility` | `concept`, `pseudocode`, `snippet`, `runnable`, `benchmarked` |
| `evidence_types` | `official-doc`, `upstream-code`, `paper`, `benchmark`, `measurement`, `inference` |

A `verified` wiki page needs an `evidence_basis` that holds either a `measurement` entry resolving to a source-measurement page, or both an `official-doc` entry (citing a document page whose `source_category` is `official-doc`) and an `upstream-code` entry (citing a pull-request page). Details: `references/schema.md`.

## Version-Sensitive Claims

Registry: `data/version-claims.yaml`. No claims yet. Tracked tools: `mesa-radv`, `mesa-anv`, `glslc`, `vulkan-sdk`, `adreno-driver`, `mali-driver`, `nvidia-driver`, `executorch`.
