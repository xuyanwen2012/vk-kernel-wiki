# Topic Map / Primer

A map of the knowledge base, organised by the controlled vocabulary in `data/tags.yaml` and the architecture tree in `data/architectures.yaml`. Use it when a question is broad: find the area, then query by the term shown.

**Current corpus: 811 pages. 28 of them (12 source-measurement pages, 16 wiki pages) are first-party measurements and the pages written from them, for seven measured devices: 19 (6 source-measurement, 13 wiki) are tagged with the device node `radeon-780m` alone, the only device with the full set (device properties, linear kernels, attention, end-to-end, fused attention kernel) and the only one with hardware and kernel pages; 6 source-measurement pages hold the fused-attention campaign result only, one each for `rx-7600`, `rx-7900-xtx`, `arc-b580`, `arc-pro-b70`, `rtx-4070-ti-super` and `jetson-orin`; 3 wiki pages (`technique-fused-attention-kernel`, `pattern-invalid-usage-that-passes-tests`, `migration-rdna3-to-xe2`) are written from the fused-attention measurements across devices. 58 document pages, 11 blog pages and 1 language page are not tied to a measured device; the other 713 are generated pull-request pages from `ggml-org/llama.cpp` (405), `mesa/mesa` (169), `Tencent/ncnn` (103), `alibaba/MNN` (10), `jeffbolznv/vk_cooperative_matrix_perf` (10), `KhronosGroup/glslang` (8) and `KhronosGroup/SPIRV-Tools` (8).** The tables below list measurement and wiki pages by id. Document, blog and pull-request pages are not listed by id; where a term or node has only such pages the table says which kinds and names the generated index, and a row that lists ids may have such pages as well. The six `radeon-780m` measurement pages carry the driver RADV Mesa 25.2.7; their measurement dates are 2026-09-01 (`meas-780m-vulkaninfo`), 2026-09-27 (`meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`), 2026-09-28 (`meas-780m-e2e-prefill`) and 2026-10-05 (`meas-780m-fused-attention`). The other six carry RADV Mesa 26.2.3 (`meas-rx7600-fused-attention`, 2026-10-06), AMDVLK 2025.Q2.1 (`meas-7900xtx-fused-attention`, 2026-10-08), ANV Mesa 26.2.3 (`meas-b580-fused-port` and `meas-b70-fused-port`, 2026-10-09), NVIDIA 615.71.09 (`meas-4070ti-fused-port`, 2026-10-09) and NVIDIA 595.78 (`meas-orin-fused-port`, 2026-10-09). For `meas-780m-8da4w-port` and `meas-780m-sdpa-port` the driver version is attributed from the package install history captured on the device on 2026-10-04 (`sources/measurements/780m-driver-history/mesa-install-history-2026-10-04.txt`); the runs themselves record the driver name without a version. A term or node marked "no pages yet" has no page. A page listed next to a term carries that term in its frontmatter; the listing is not a claim about behaviour or performance, and nothing here is established for any other device, driver or date. Do not transfer a number from one device to another. The one-line descriptions repeat the term definitions in `data/tags.yaml`.

Query any term with `python3 scripts/query.py --tag <term>`, and any node with `python3 scripts/query.py --architecture <node>`. Aliases for each are in `data/aliases.yaml`.

---

## Architectures

Any node name is a valid value of the `architectures` field. Asking for a node returns pages tagged with it or any descendant, never pages tagged only with an ancestor.

| Node | Kind | Parent | Pages |
|---|---|---|---|
| `amd` | vendor | | pull-request, document and blog pages only; list: `queries/by-architecture.md` |
| `rdna3` | generation | `amd` | `lang-glsl-cooperative-matrix`; otherwise pull-request, document and blog pages only; list: `queries/by-architecture.md` |
| `radeon-780m` | device | `rdna3` | 21 pages (6 source-measurement, 15 wiki: the 13 tagged with this node alone, `technique-fused-attention-kernel` and `pattern-invalid-usage-that-passes-tests`); list: `queries/by-architecture.md` |
| `rx-7900-xtx` | device | `rdna3` | `meas-7900xtx-fused-attention`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel`; otherwise document pages only; list: `queries/by-architecture.md` |
| `rx-7600` | device | `rdna3` | `meas-rx7600-fused-attention`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel` |
| `rdna4` | generation | `amd` | pull-request and document pages only; list: `queries/by-architecture.md` |
| `rx-9070-xt` | device | `rdna4` | document pages only; list: `queries/by-architecture.md` |
| `intel` | vendor | | pull-request and document pages only; list: `queries/by-architecture.md` |
| `xe2` | generation | `intel` | pull-request and blog pages only; list: `queries/by-architecture.md` |
| `arc-b580` | device | `xe2` | `meas-b580-fused-port`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel`; otherwise blog pages only; list: `queries/by-architecture.md` |
| `arc-pro-b70` | device | `xe2` | `meas-b70-fused-port`, `technique-fused-attention-kernel`; otherwise blog pages only; list: `queries/by-architecture.md` |
| `arc-a770` | device | `intel` | blog pages only; list: `queries/by-architecture.md` |
| `meteor-lake` | generation | `intel` | pull-request pages only; list: `queries/by-architecture.md` |
| `xe3` | generation | `intel` | pull-request pages only; list: `queries/by-architecture.md` |
| `nvidia` | vendor | | pull-request, document and blog pages only; list: `queries/by-architecture.md` |
| `rtx-4070` | device | `nvidia` | document pages only; list: `queries/by-architecture.md` |
| `rtx-4070-ti-super` | device | `nvidia` | `meas-4070ti-fused-port`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel` |
| `jetson-orin` | device | `nvidia` | `meas-orin-fused-port`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel` |
| `turing` | generation | `nvidia` | pull-request and document pages only; list: `queries/by-architecture.md` |
| `ampere` | generation | `nvidia` | pull-request pages only; list: `queries/by-architecture.md` |
| `blackwell` | generation | `nvidia` | pull-request pages only; list: `queries/by-architecture.md` |
| `qualcomm` | vendor | | pull-request and document pages only; list: `queries/by-architecture.md` |
| `adreno-840` | device | `qualcomm` | no pages yet |
| `adreno-7xx` | generation | `qualcomm` | pull-request pages only; list: `queries/by-architecture.md` |
| `arm` | vendor | | pull-request and document pages only; list: `queries/by-architecture.md` |
| `mali-g1` | device | `arm` | no pages yet |
| `bifrost` | generation | `arm` | pull-request pages only; list: `queries/by-architecture.md` |
| `samsung` | vendor | | reserved, no devices |

Every measurement page is tagged with one device node. The hardware and kernel pages and 8 of the technique and pattern pages are tagged with `radeon-780m` only, so a query for `rdna3` or `amd` returns them as descendants; `technique-fused-attention-kernel` is tagged with all seven measured devices and `pattern-invalid-usage-that-passes-tests` with six (not `arc-pro-b70`). `migration-rdna3-to-xe2` names its nodes in `from_arch` and `to_arch` and has no `architectures` field, so `--architecture` does not return it; use `--type migration`. Document and blog pages carry the nodes their source names. Some pull-request pages are tagged with a vendor or generation node taken from the pull-request title, from a device check the pull request adds to the code, or from a changed path under a vendor's driver. Measurements per device are indexed in `queries/by-device.md`.

---

## Hardware Features (`hardware_features`)

Pages live in `wiki/hardware/` (id prefix `hw-`). Index: `queries/by-hardware-feature.md`.

### Cooperative matrix

| Term | Meaning (from `data/tags.yaml`) | Pages |
|---|---|---|
| `cooperative-matrix` | VK_KHR_cooperative_matrix / GL_KHR_cooperative_matrix | `meas-4070ti-fused-port`, `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `meas-780m-fused-attention`, `meas-780m-sdpa-port`, `meas-780m-vulkaninfo`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `migration-rdna3-to-xe2`, `pattern-coopmat-name-check-false-failure`, `pattern-invalid-usage-that-passes-tests`, `pattern-sdpa-release-gap`, `pattern-unaligned-m-fallback`, `technique-drain-in-a-staging`, `technique-fp32-accumulation`, `technique-full-a-map`, `technique-fused-attention-kernel`, `technique-workgroup-tile-sizing` |
| `int8-cooperative-matrix` | an int8 cooperative-matrix shape is enumerated | `lang-glsl-cooperative-matrix`; otherwise pull-request and document pages only; list: `queries/by-hardware-feature.md` |
| `cooperative-matrix2` | VK_NV_cooperative_matrix2 / GL_NV_cooperative_matrix2 | `lang-glsl-cooperative-matrix`; otherwise pull-request, document and blog pages only; list: `queries/by-hardware-feature.md` |
| `coopmat-shape` | the M x N x K shapes a device exposes | `meas-b580-fused-port`, `meas-b70-fused-port`, `hw-cooperative-matrix-rdna3`, `migration-rdna3-to-xe2`, `technique-fused-attention-kernel` |
| `coopmat-fp32-accumulator` | fp32 accumulator matrix for fp16 operands | `hw-cooperative-matrix-rdna3`, `kernel-linear-4w-780m`, `kernel-sdpa-prefill-780m`, `technique-fp32-accumulation` |

### Subgroups

| Term | Meaning | Pages |
|---|---|---|
| `subgroup-size` | default subgroup size of the device | `meas-4070ti-fused-port`, `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-fused-attention`, `meas-780m-sdpa-port`, `meas-780m-vulkaninfo`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `migration-rdna3-to-xe2`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel` |
| `subgroup-size-control` | VK_EXT_subgroup_size_control (required size per pipeline) | `meas-780m-vulkaninfo`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m` |
| `wave64` | adapters whose native subgroup is 64 lanes | `meas-780m-8da4w-port`, `meas-780m-vulkaninfo`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `subgroup-operations` | GL_KHR_shader_subgroup built-ins a driver exposes (subgroupSupportedOperations, VkPhysicalDeviceSubgroupProperties) | pull-request and document pages only; list: `queries/by-hardware-feature.md` |
| `full-subgroups` | computeFullSubgroups / REQUIRE_FULL_SUBGROUPS (every subgroup launched fully populated) | `meas-4070ti-fused-port`, `meas-780m-fused-attention`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `migration-rdna3-to-xe2`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel`; otherwise document pages only; list: `queries/by-hardware-feature.md` |

### Memory and storage

| Term | Meaning | Pages |
|---|---|---|
| `shared-memory-limit` | maxComputeSharedMemorySize | `meas-4070ti-fused-port`, `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-vulkaninfo`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `hw-cooperative-matrix-rdna3`, `hw-radeon-780m`, `migration-rdna3-to-xe2`, `pattern-invalid-usage-that-passes-tests` |
| `storage-buffer` | tensor stored as a buffer (SSBO) | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `storage-texture3d` | tensor stored as a 3D texture | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `technique-drain-in-a-staging` |
| `storage-texture2d` | packed weights stored as a 2D texture | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m` |
| `workgroup-size-limit` | maxComputeWorkGroupSize / maxComputeWorkGroupInvocations | document pages only; list: `queries/by-hardware-feature.md` |
| `control-barrier` | barrier() / OpControlBarrier, including split barriers | `meas-4070ti-fused-port`, `meas-780m-fused-attention`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `migration-rdna3-to-xe2`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel`; otherwise document pages only; list: `queries/by-hardware-feature.md` |
| `memory-model` | Vulkan memory model: data races, memory semantics, scopes | `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel`; otherwise document pages only; list: `queries/by-hardware-feature.md` |

### Shader arithmetic and constants

| Term | Meaning | Pages |
|---|---|---|
| `fp16-arithmetic` | GL_EXT_shader_explicit_arithmetic_types_float16 | `meas-780m-vulkaninfo`, `hw-radeon-780m` |
| `bfloat16-arithmetic` | GL_EXT_bfloat16 (bf16 scalars, vectors and matrix components) | pull-request, document and blog pages only; list: `queries/by-hardware-feature.md` |
| `int8-arithmetic` | GL_EXT_shader_explicit_arithmetic_types_int8 | `meas-780m-vulkaninfo`, `hw-radeon-780m`, `kernel-linear-8da4w-780m` |
| `8bit-storage` | GL_EXT_shader_8bit_storage | `meas-780m-vulkaninfo`, `hw-radeon-780m` |
| `integer-dot-product` | GL_EXT_integer_dot_product | `meas-780m-vulkaninfo`, `hw-radeon-780m` |
| `specialization-constants` | local_size_*_id and spec-constant shape parameters | `lang-glsl-cooperative-matrix`; otherwise pull-request and document pages only; list: `queries/by-hardware-feature.md` |

---

## Optimization Techniques (`techniques`)

Pages live in `wiki/techniques/` (id prefix `technique-`). Index: `queries/by-technique.md`.

### Tile geometry

| Term | Meaning | Pages |
|---|---|---|
| `workgroup-tile-sizing` | output tile per workgroup (M x N) | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `pattern-unaligned-m-fallback`, `technique-workgroup-tile-sizing` |
| `k-chunk-sizing` | K consumed per main-loop iteration | `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m` |
| `subgroup-grid` | subgroup grid inside the workgroup | `meas-b580-fused-port`, `meas-b70-fused-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `migration-rdna3-to-xe2`, `technique-fused-attention-kernel`, `technique-workgroup-tile-sizing` |
| `required-subgroup-size` | pipeline pinned to one subgroup size | `meas-4070ti-fused-port`, `meas-780m-8da4w-port`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `migration-rdna3-to-xe2`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel` |
| `mma-shape-selection` | shape of one cooperative-matrix multiply-add | `migration-rdna3-to-xe2`; otherwise document pages only; list: `queries/by-technique.md` |
| `per-shape-tile-selection` | different tiles for different operator shapes | document pages only; list: `queries/by-technique.md` |

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
| `shared-memory-fence` | explicit ordering of shared stores against matrix loads | document pages only; list: `queries/by-technique.md` |
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
| `causal-truncation` | skip work above the causal diagonal | `meas-780m-e2e-prefill`, `meas-780m-sdpa-port`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-causal-truncation`, `technique-fused-attention-kernel` |

### Stated in upstream pull requests

| Term | Meaning | Pages |
|---|---|---|
| `split-k-reduction` | K split across workgroups, partial sums reduced in a second pass | pull-request pages only; list: `queries/by-technique.md` |
| `kernel-fusion` | several operators merged into one dispatch | `meas-4070ti-fused-port`, `meas-780m-fused-attention`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `migration-rdna3-to-xe2`, `pattern-invalid-usage-that-passes-tests`, `technique-fused-attention-kernel`; otherwise pull-request, document and blog pages only; list: `queries/by-technique.md` |
| `device-specific-tuning` | parameters or kernel choice tuned per vendor, generation or device | pull-request, document and blog pages only; list: `queries/by-technique.md` |
| `driver-workaround` | a path disabled or changed because of a driver or compiler defect | pull-request and blog pages only; list: `queries/by-technique.md` |
| `winograd-convolution` | 3x3 convolution through the Winograd transform | pull-request pages only; list: `queries/by-technique.md` |
| `channel-packing` | channels packed into vec4/vec8 elements (pack4, pack8) | pull-request pages only; list: `queries/by-technique.md` |

---

## Kernel Case Studies (`kernel_types`)

Pages live in `wiki/kernels/` (id prefix `kernel-`). Index: `queries/by-kernel-type.md`. Kernel pages carry `performance_claims`: `kernel-linear-4w-780m` (93 claims, measured 2026-09-27 and 2026-09-28), `kernel-linear-8da4w-780m` (88 claims, measured 2026-09-27 and 2026-09-28) and `kernel-sdpa-prefill-780m` (84 claims, measured 2026-09-27 and 2026-09-28), all on `radeon-780m` with RADV Mesa 25.2.7. Read the numbers from the pages; this file repeats none.

### Matrix products

| Term | Meaning | Pages |
|---|---|---|
| `gemm` | | `meas-780m-e2e-prefill`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `technique-drain-in-a-staging`, `technique-fp32-accumulation`, `technique-workgroup-tile-sizing` |
| `gemv` | | pull-request, document and blog pages only; list: `queries/by-kernel-type.md` |

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
| `sdpa` | scaled dot-product attention | `meas-4070ti-fused-port`, `meas-780m-e2e-prefill`, `meas-780m-fused-attention`, `meas-780m-sdpa-port`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `kernel-sdpa-prefill-780m`, `migration-rdna3-to-xe2`, `pattern-invalid-usage-that-passes-tests`, `pattern-sdpa-release-gap`, `technique-causal-truncation`, `technique-fused-attention-kernel` |
| `sdpa-qk` | attention weights, Q K^T | `meas-4070ti-fused-port`, `meas-780m-e2e-prefill`, `meas-780m-fused-attention`, `meas-780m-sdpa-port`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-fused-attention-kernel`, `technique-workgroup-tile-sizing` |
| `sdpa-av` | attention output, attn V | `meas-4070ti-fused-port`, `meas-780m-e2e-prefill`, `meas-780m-fused-attention`, `meas-780m-sdpa-port`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-fused-attention-kernel`, `technique-workgroup-tile-sizing` |
| `sdpa-softmax` | attention-weight softmax | `meas-4070ti-fused-port`, `meas-780m-e2e-prefill`, `meas-780m-fused-attention`, `meas-780m-sdpa-port`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `kernel-sdpa-prefill-780m`, `pattern-sdpa-release-gap`, `technique-causal-truncation`, `technique-fused-attention-kernel` |

### Inference phase

| Term | Meaning | Pages |
|---|---|---|
| `prefill` | | `meas-4070ti-fused-port`, `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-e2e-prefill`, `meas-780m-fused-attention`, `meas-780m-sdpa-port`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-orin-fused-port`, `meas-rx7600-fused-attention`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`, `migration-rdna3-to-xe2`, `pattern-coopmat-name-check-false-failure`, `pattern-sdpa-release-gap`, `pattern-unaligned-m-fallback`, `technique-causal-truncation`, `technique-drain-in-a-staging`, `technique-fp32-accumulation`, `technique-full-a-map`, `technique-fused-attention-kernel`, `technique-workgroup-tile-sizing` |
| `decode` | | `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`, `meas-b70-fused-port` |

### Other operator families (upstream pull requests)

| Term | Meaning | Pages |
|---|---|---|
| `moe` | mixture-of-experts routing and per-expert matrix products | pull-request, document and blog pages only; list: `queries/by-kernel-type.md` |
| `convolution` | conv1d/2d/3d, transposed convolution, im2col / col2im | pull-request and document pages only; list: `queries/by-kernel-type.md` |
| `dequantize` | quantized weight blocks expanded to float | pull-request and document pages only; list: `queries/by-kernel-type.md` |
| `rope` | rotary position embedding | pull-request pages only; list: `queries/by-kernel-type.md` |
| `normalization` | RMS, L2, group and layer normalization | pull-request pages only; list: `queries/by-kernel-type.md` |
| `softmax` | standalone softmax | pull-request pages only; list: `queries/by-kernel-type.md` |
| `topk-sort` | argsort, argmax and top-k selection | pull-request pages only; list: `queries/by-kernel-type.md` |
| `gated-delta-net` | gated delta-rule linear attention | pull-request and document pages only; list: `queries/by-kernel-type.md` |
| `tensor-copy` | copy, type conversion, row gather/scatter, concat, pad, repeat | pull-request pages only; list: `queries/by-kernel-type.md` |
| `elementwise` | unary and binary elementwise operators and activations | pull-request pages only; list: `queries/by-kernel-type.md` |

---

## Languages (`languages`)

Pages live in `wiki/languages/` (id prefix `lang-`). Index: `queries/by-language.md`.

| Term | Pages |
|---|---|
| `glsl` | `lang-glsl-cooperative-matrix`, `kernel-linear-4w-780m`, `kernel-linear-8da4w-780m`, `kernel-sdpa-prefill-780m`; also pull-request and document pages; list: `queries/by-language.md` |
| `spirv` | document and blog pages only; list: `queries/by-language.md` |
| `cpp` | pull-request pages only; list: `queries/by-language.md` |
| `c` | pull-request pages only; list: `queries/by-language.md` |
| `python` | pull-request pages only; list: `queries/by-language.md` |
| `rust` | pull-request pages only; list: `queries/by-language.md` |

---

## Problem Diagnosis (`wiki/patterns/`)

Pattern pages map `symptoms` to `candidate_techniques` (id prefix `pattern-`). Symptoms are free text on each pattern page, not a controlled group in `data/tags.yaml`. Four pages: `pattern-unaligned-m-fallback` (`wiki/patterns/unaligned-m-fallback.md`), `pattern-sdpa-release-gap` (`wiki/patterns/sdpa-release-gap.md`), `pattern-coopmat-name-check-false-failure` (`wiki/patterns/coopmat-name-check-false-failure.md`) and `pattern-invalid-usage-that-passes-tests` (`wiki/patterns/invalid-usage-that-passes-tests.md`). Index: `queries/by-problem.md`.

## Migration Notes (`wiki/migration/`)

Migration pages describe porting a kernel from one architecture node to another (`from_arch`, `to_arch`; id prefix `migration-`). One page: `migration-rdna3-to-xe2` (`wiki/migration/rdna3-to-xe2.md`), `rdna3` to `xe2`, for the fused attention kernel only.

---

## Sources

| Source type | Directory | `source_category` values | Pages |
|---|---|---|---|
| First-party measurement | `sources/measurements/` | `measurement` | `meas-780m-vulkaninfo`, `meas-780m-4w-bootstrap`, `meas-780m-8da4w-port`, `meas-780m-sdpa-port`, `meas-780m-e2e-prefill`, `meas-780m-fused-attention`, `meas-rx7600-fused-attention`, `meas-7900xtx-fused-attention`, `meas-b580-fused-port`, `meas-b70-fused-port`, `meas-4070ti-fused-port`, `meas-orin-fused-port` |
| Upstream pull request | `sources/prs/` | `upstream-code` | 713 generated pages in `sources/prs/llama-cpp/` (405), `mesa/` (169), `ncnn/` (103), `mnn/` (10), `vk-coopmat-perf/` (10), `glslang/` (8) and `spirv-tools/` (8); list: `queries/by-repo.md` |
| Documentation and papers | `sources/docs/` | `official-doc` (specification-grade), `upstream-code` (another project's source files), `vendor-doc` (vendor and project articles, guides, slide decks), `paper` | 58 pages: 34 `official-doc` (`doc-glsl-khr-cooperative-matrix`, `doc-glsl-khr-shader-subgroup`, `doc-glsl-spec-barrier-functions`, `doc-glsl-spec-shared-variables`, `doc-glsl-spec-spirv-barrier-mapping`, `doc-intel-igc-visa-dpas`, `doc-mesa-features-vulkan-compute`, `doc-mesa-radv-envvars`, `doc-mesa-relnotes-19-1-0`, `doc-mesa-relnotes-21-1-0`, `doc-mesa-relnotes-23-3-0`, `doc-mesa-relnotes-25-0-0`, `doc-mesa-relnotes-25-1-0`, `doc-mesa-relnotes-25-2-0`, `doc-mesa-relnotes-26-2-0`, `doc-mesa-relnotes-new-features`, `doc-nvidia-vulkan-beta-driver-release-notes`, `doc-vk-ext-cooperative-matrix-maintenance1-proposal`, `doc-vk-ext-shader-split-barrier-proposal`, `doc-vk-ext-subgroup-size-control`, `doc-vk-khr-cooperative-matrix-proposal`, `doc-vk-nv-cooperative-matrix-decode-vector-proposal`, `doc-vk-nv-cooperative-matrix2-extension`, `doc-vk-nv-cooperative-matrix2-proposal`, `doc-vk-qcom-cooperative-matrix-conversion-proposal`, `doc-vk-spec-cooperative-matrix-properties`, `doc-vk-spec-features-subgroup-coopmat`, `doc-vk-spec-limits-compute-subgroup-coopmat`, `doc-vk-spec-memory-model`, `doc-vk-spec-pipeline-shader-stage-subgroup-flags`, `doc-vk-spec-shaders-compute-subgroups`, `doc-vk-spec-spirvenv-cooperative-matrix-subgroups`, `doc-vk-spec-subgroup-builtins`, `doc-vulkan-guide-subgroups`); 9 `upstream-code` (`doc-arm-libgpucounters-shader-core-counters`, `doc-cubek-matmul`, `doc-onnxruntime-webgpu-matmul-nbits`, `doc-qualcomm-adreno-cooperative-matrix-sample`, `doc-vk-gl-cts-cooperative-matrix-tests`, `doc-vk-gl-cts-subgroup-size-control-tests`, `doc-vvl-cooperative-matrix-checks`, `doc-vvl-subgroup-size-and-shared-memory-checks`, `doc-wonnx-gemm-template`); 14 `vendor-doc` (`doc-amd-rdna-performance-guide`, `doc-amd-rdna3-beyond-the-current-gen`, `doc-gpuopen-matrix-cores-rdna4`, `doc-gpuopen-wmma-on-rdna3`, `doc-intel-oneapi-gpu-guide-joint-matrix`, `doc-intel-oneapi-gpu-guide-xmx`, `doc-iree-vulkan-deployment-guide`, `doc-iree-vulkanised-2025-spirv-talk`, `doc-mnn-release-3-4-0`, `doc-mnn-release-3-4-1`, `doc-mnn-release-3-6-0`, `doc-mnn-vulkan-optimization-handbook`, `doc-nvidia-vulkanised-2025-cooperative-matrix2`, `doc-tvm-vulkan-runtime`); 1 `paper` (`doc-webllm-paper`) |
| Blogs and notes | `sources/blogs/` | `benchmark-blog`, `community-note` | 11 pages: `blog-glslang-issue-3929-bfloat16-coopmat-elementwise`, `blog-glslang-issue-3948-small-index-types`, `blog-llama-cpp-discussion-13530-intel-xe2-coopmat`, `blog-llama-cpp-issue-22034-intel-device-lost`, `blog-mlc-amd-gpus-llm-inference`, `blog-nvidia-vulkan-cooperative-matrices-2019`, `blog-shaderc-issue-1594-coopmat2-optimizer-capability`, `blog-spirv-tools-issue-6077-coopmat-bitwise-ops`, `blog-spirv-tools-issue-6410-coopmat-load-through-array`, `blog-themaister-fsr4-wmma`, `blog-zolotukhin-matrix-cores-decode` |

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

Registry: `data/version-claims.yaml`. One claim: `vs-radv-coopmat-lowering-after-25-2-7`. Tracked tools: `mesa-radv`, `mesa-anv`, `glslc`, `vulkan-sdk`, `adreno-driver`, `mali-driver`, `nvidia-driver`, `executorch`.
