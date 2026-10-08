---
id: hw-cooperative-matrix-rdna3
title: "Cooperative matrix on the Radeon 780M (RDNA3 iGPU) with RADV Mesa 25.2.7"
type: hardware
architectures: [radeon-780m]
tags: [cooperative-matrix, coopmat-shape, coopmat-fp32-accumulator, subgroup-size, subgroup-size-control, wave64, shared-memory-limit]
confidence: source-reported
related: [hw-radeon-780m, kernel-linear-4w-780m, kernel-linear-8da4w-780m, kernel-sdpa-prefill-780m, technique-fp32-accumulation, technique-drain-in-a-staging, technique-workgroup-tile-sizing, technique-causal-truncation]
sources: [meas-780m-vulkaninfo, meas-780m-4w-bootstrap]
version_sensitive: vs-radv-coopmat-lowering-after-25-2-7
evidence_basis:
  - evidence_type: measurement
    source_id: meas-780m-vulkaninfo
    locator: "sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, lines 125, 320-323, 946-950"
aliases: ["VK_KHR_cooperative_matrix", "GL_KHR_cooperative_matrix", "coopmat", "WMMA", "cooperative matrix 780M"]
---

# Cooperative matrix on the Radeon 780M (RDNA3 iGPU) with RADV Mesa 25.2.7

Scope: the evidence is one device (Radeon 780M) on one driver (RADV Mesa 25.2.7). The page id says "rdna3", but nothing here is established for other RDNA3 devices or for the generation as a whole, and the page is tagged with the device node only.

Two kinds of evidence are used and kept apart:

1. Device properties exported from the device, recorded in `meas-780m-vulkaninfo`. "Line N" in that context is a line of `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`; JSON paths are relative to `$.capabilities.device`.
2. Statements in the kernel-selection code and documentation of https://github.com/sarc-acl/executorch at commit ef079ac41fd09f01656e1ab46c87ca85be6c54ae, as excerpted in `meas-780m-4w-bootstrap` and cited as `[meas-780m-4w-bootstrap: <path>#L<lines>]`. These are what the code and its authors report; the device-properties export does not confirm them.

## What the device-properties export shows

| Item | Value | Locator in meas-780m-vulkaninfo |
|---|---|---|
| `VK_KHR_cooperative_matrix` | spec version `2` | `.extensions.VK_KHR_cooperative_matrix`, line 125 |
| `cooperativeMatrix` | `true` | `.features.VkPhysicalDeviceCooperativeMatrixFeaturesKHR.cooperativeMatrix`, line 321 |
| `cooperativeMatrixRobustBufferAccess` | `true` | `.features.VkPhysicalDeviceCooperativeMatrixFeaturesKHR.cooperativeMatrixRobustBufferAccess`, line 322 |
| `cooperativeMatrixSupportedStages` | `["VK_SHADER_STAGE_COMPUTE_BIT"]` | `.properties.VkPhysicalDeviceCooperativeMatrixPropertiesKHR.cooperativeMatrixSupportedStages`, lines 947-949 |
| Driver | `radv`, `Mesa 25.2.7` | `.properties.VkPhysicalDeviceVulkan12Properties.driverName` / `.driverInfo`, lines 1271-1272 |
| Export date | `2026-9-1` | `$.profiles[...].history[0].date`, line 11220 |

So on this driver the extension is exposed, the feature is enabled, and the only stage listed for cooperative matrices is compute.

### What the export does not show

- **No shape enumeration.** The export has no `VkCooperativeMatrixPropertiesKHR` entries: `VkPhysicalDeviceCooperativeMatrixPropertiesKHR` holds the single key `cooperativeMatrixSupportedStages` (lines 946-950), and a case-insensitive text search of the raw file (`grep -ci`) finds 0 lines for `VkCooperativeMatrixPropertiesKHR`. The supported M x N x K sizes, component types and accumulator types are therefore not measured by this source, and this page does not infer them from it.
- **No int8 shape evidence.** For the same reason the export neither shows nor rules out an int8 cooperative-matrix shape.
- No `VK_NV_cooperative_matrix` key and no `cooperativeMatrixFlexibleDimensions` key appear in the file (the same text search finds 0 lines for each).

## Subgroup and shared-memory context from the same export

Cooperative-matrix kernels are laid out on subgroups and stage their operands in shared memory, so these values from `meas-780m-vulkaninfo` bound the tile choices (full table on `hw-radeon-780m`):

| Property | Value | Locator in meas-780m-vulkaninfo |
|---|---|---|
| `subgroupSize` | `64` | `.properties.VkPhysicalDeviceVulkan11Properties.subgroupSize`, line 1232 |
| `minSubgroupSize` | `32` | `.properties.VkPhysicalDeviceVulkan13Properties.minSubgroupSize`, line 1340 |
| `maxSubgroupSize` | `64` | `.properties.VkPhysicalDeviceVulkan13Properties.maxSubgroupSize`, line 1341 |
| `subgroupSizeControl` | `true` | `.features.VkPhysicalDeviceVulkan13Features.subgroupSizeControl`, line 687 |
| `requiredSubgroupSizeStages` | includes `VK_SHADER_STAGE_COMPUTE_BIT` | `.properties.VkPhysicalDeviceVulkan13Properties.requiredSubgroupSizeStages`, lines 1343-1347 |
| `maxComputeSharedMemorySize` | `65536` | `.properties.VkPhysicalDeviceProperties.limits.maxComputeSharedMemorySize`, line 791 |
| `maxComputeWorkGroupInvocations` | `1024` | `.properties.VkPhysicalDeviceProperties.limits.maxComputeWorkGroupInvocations`, line 797 |

## What the selection code reports for this device (source-reported, not measured here)

How the device is matched:

- The AMD rows are gated by a predicate that requires an AMD device whose default subgroup size is 64: `return d.is_amd && d.subgroup_size == 64;` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L22-L24]. This agrees with `subgroupSize` 64 in the export (line 1232).
- The code comment on that predicate says the shipped RDNA cooperative-matrix variants were built and validated for wave64 adapters that support cooperative matrix, and that they force subgroup size 32 per pipeline through `SUBGROUP_SIZE` in the yaml [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L19-L21]. The comment is worded for RDNA; the rows it is verified against in this phase are the 780M rows only.
- The selector's device record carries `subgroup_size` ("default subgroup size"), `min_subgroup_size`, `max_subgroup_size`, `subgroup_size_control` ("VK_EXT_subgroup_size_control"), `coopmat`, `int8_coopmat` ("an int8 cooperative-matrix shape is enumerated") and `max_shared_bytes` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h#L48-L58].
- When a row is matched, the selector enforces that `SUBGROUP_SIZE` "equals the device's subgroup size, or lies within its supported range when subgroup-size control is available" and that "shared memory fits the device limit (`max_compute_shared_memory_size`)" [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L79-L81].
- The row comment names the configuration the 780M rows were verified on: "Radeon 780M (gfx1103, RADV, Mesa 25.2.7)" [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L30]. The driver matches the export (line 1272).

Tile geometry of the four 780M rows. The `TileDims` initializer order is `m`, `n`, `k`, `sg_grid_x`, `sg_grid_y`, `subgroup_size`, `mma_m`, `csh_in_ash` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/Select.h#L80-L88]:

| Op | Kernel base | TileDims as written | Status | Locator in meas-780m-4w-bootstrap (table_amd.cpp) |
|---|---|---|---|---|
| `Op::kQ4gswLinear` (4w) | `sarc_linear_q4gsw_coopmat_t128x128k32g42s32f32c` | `{128, 128, 32, 4, 2, 32, 16, true}` | `Status::kVerified` | #L27, #L34-L41 |
| `Op::kDq8caLinear` (8da4w) | `sarc_linear_dq8ca_coopmat_zpg_t128x64k32g42s32` | `{128, 64, 32, 4, 2, 32, 16, false}` | `Status::kVerified` | #L46-L53 |
| `Op::kSdpaQk` | `sarc_sdpa_qk_coopmat_t128x64k32g22s64` | `{128, 64, 32, 2, 2, 64, 16, false}` | `Status::kVerified` | #L81-L88 |
| `Op::kSdpaAv` | `sarc_sdpa_av_coopmat_t64x64k32g22s64` | `{64, 64, 32, 2, 2, 64, 16, false}` | `Status::kVerified` | #L89-L96 |

Reading those rows against the export:

- **Required subgroup size.** The two linear rows carry `subgroup_size` 32 and the two SDPA rows carry 64. Both values lie inside the `minSubgroupSize` 32 to `maxSubgroupSize` 64 range the export reports (lines 1340-1341), and the export reports `subgroupSizeControl` `true` with compute among `requiredSubgroupSizeStages` (lines 687, 1343-1347). That the linear kernels run correctly with 32-lane subgroups is the code's claim, not something the export measures.
- **MMA shape.** All four rows carry `mma_m` 16. Because the export has no shape enumeration, the cooperative-matrix shape these rows rely on is source-reported by the shipped rows, not confirmed by `meas-780m-vulkaninfo`.
- **fp32 accumulator.** The 4w tile token ends in `f32c`; `f32` decodes to `ACC_FP32` and `c` to `CSH_IN_ASH` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L103-L104]. The selection table describes the 4w tile as "t128x128k32g42s32 with fp32 accumulate and the drain staged in Ash" [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L26]. The export does not list an fp32-accumulator shape, so this too is source-reported.
- **Drain staged in the A region.** `CSH_IN_ASH` ("texture3d output drain staged in the dead A shared-memory region") is listed as used by the 780M with the remark "less LDS, higher occupancy" [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L43]; the 4w row sets `csh_in_ash` to `true` [meas-780m-4w-bootstrap: backends/vulkan/runtime/graph/ops/impl/sarc/table_amd.cpp#L27].
- **Shipped variants.** The release 1.5 table lists, for the Radeon 780M, 4w `t128x128k32g42s32f32c` and 8da4w zpg `t128x64k32g42s32` + `A_MAP_FULL` [meas-780m-4w-bootstrap: sarc/SWEEP-PARAMETERS.md#L127], and the device status table lists 4w, 8da4w and SDPA prefill as "verified" for the Radeon 780M [meas-780m-4w-bootstrap: sarc/README.md#L82].

## Confidence

`source-reported`. The export directly supports "the extension is exposed, the feature is on, compute is the supported stage" on this device and driver. The tile geometry in use (`mma_m` 16, fp32 accumulation for the 4w tile) and the subgroup pinning are reported by the selection code and its documentation; no source page in this wiki enumerates the device's cooperative-matrix shapes.
