---
id: hw-radeon-780m
title: "Radeon 780M on RADV Mesa 25.2.7: device properties for compute-shader kernels"
type: hardware
architectures: [radeon-780m]
tags: [subgroup-size, subgroup-size-control, wave64, shared-memory-limit, cooperative-matrix, fp16-arithmetic, int8-arithmetic, 8bit-storage, integer-dot-product]
confidence: verified
related: [hw-cooperative-matrix-rdna3, kernel-linear-4w-780m, kernel-linear-8da4w-780m, kernel-sdpa-prefill-780m, technique-workgroup-tile-sizing, pattern-unaligned-m-fallback]
sources: [meas-780m-vulkaninfo]
evidence_basis:
  - evidence_type: measurement
    source_id: meas-780m-vulkaninfo
    locator: "sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json, lines 733-738, 791-802, 1232-1261, 1269-1272, 1339-1347"
aliases: ["Radeon 780M", "780M", "AMD Radeon 780M Graphics (RADV PHOENIX)", "PHOENIX", "RADV Mesa 25.2.7"]
---

# Radeon 780M on RADV Mesa 25.2.7: device properties for compute-shader kernels

Scope: one device, one driver, one export. Everything below is read from a Vulkan profile exported from vulkaninfo on the device and recorded in `meas-780m-vulkaninfo`. The raw file is `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`; "line N" below is a line of that file, and JSON paths are relative to `$.capabilities.device` unless they start with `$`. The values hold for this driver version only; nothing here is carried over to another driver, another device or the RDNA3 generation as a whole.

## Identity

| Item | Value | Locator in meas-780m-vulkaninfo |
|---|---|---|
| Device name | `AMD Radeon 780M Graphics (RADV PHOENIX)` | `.properties.VkPhysicalDeviceProperties.deviceName`, line 736 |
| Device type | `VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU` | `.properties.VkPhysicalDeviceProperties.deviceType`, line 737 |
| vendorID | `4098` | `.properties.VkPhysicalDeviceProperties.vendorID`, line 920 |
| deviceID | `5567` | `.properties.VkPhysicalDeviceProperties.deviceID`, line 735 |
| Driver ID | `VK_DRIVER_ID_MESA_RADV` | `.properties.VkPhysicalDeviceVulkan12Properties.driverID`, line 1270 |
| Driver name | `radv` | `.properties.VkPhysicalDeviceVulkan12Properties.driverName`, line 1271 |
| Driver info | `Mesa 25.2.7` | `.properties.VkPhysicalDeviceVulkan12Properties.driverInfo`, line 1272 |
| Profile API version | `1.4.318` | `$.profiles["VP_VULKANINFO_AMD_Radeon_780M_Graphics_(RADV_PHOENIX)_25_2_7"]["api-version"]`, line 11211 |
| Raw apiVersion | `4211006` | `.properties.VkPhysicalDeviceProperties.apiVersion`, line 734 |
| Raw driverVersion | `104865799` | `.properties.VkPhysicalDeviceProperties.driverVersion`, line 738 |
| Export date | `2026-9-1` | `$.profiles[...].history[0].date`, line 11220 |

The raw `apiVersion` and `driverVersion` integers are quoted as exported; this page does not decode them.

## Subgroups

| Property | Value | Locator in meas-780m-vulkaninfo |
|---|---|---|
| `subgroupSize` | `64` | `.properties.VkPhysicalDeviceVulkan11Properties.subgroupSize`, line 1232 |
| `minSubgroupSize` | `32` | `.properties.VkPhysicalDeviceVulkan13Properties.minSubgroupSize`, line 1340 |
| `maxSubgroupSize` | `64` | `.properties.VkPhysicalDeviceVulkan13Properties.maxSubgroupSize`, line 1341 |
| `maxComputeWorkgroupSubgroups` | `4294967295` | `.properties.VkPhysicalDeviceVulkan13Properties.maxComputeWorkgroupSubgroups`, line 1342 |
| `subgroupSizeControl` | `true` | `.features.VkPhysicalDeviceVulkan13Features.subgroupSizeControl`, line 687 |
| `computeFullSubgroups` | `true` | `.features.VkPhysicalDeviceVulkan13Features.computeFullSubgroups`, line 688 |
| `VK_EXT_subgroup_size_control` | spec version `2` | `.extensions.VK_EXT_subgroup_size_control`, line 105 |
| `shaderSubgroupExtendedTypes` | `true` | `.features.VkPhysicalDeviceVulkan12Features.shaderSubgroupExtendedTypes`, line 665 |

What this means for a kernel:

- The default subgroup is 64 lanes (`subgroupSize`, line 1232), which is what the `wave64` vocabulary term names.
- A compute pipeline can be pinned to a required subgroup size: `requiredSubgroupSizeStages` lists `VK_SHADER_STAGE_COMPUTE_BIT` (`.properties.VkPhysicalDeviceVulkan13Properties.requiredSubgroupSizeStages`, lines 1343-1347) and `subgroupSizeControl` is `true` (line 687). The range reported for that control is `minSubgroupSize` 32 to `maxSubgroupSize` 64 (lines 1340-1341).
- `subgroupSupportedStages` includes `VK_SHADER_STAGE_COMPUTE_BIT` (`.properties.VkPhysicalDeviceVulkan11Properties.subgroupSupportedStages`, lines 1233-1248).
- `subgroupSupportedOperations` lists `VK_SUBGROUP_FEATURE_BASIC_BIT`, `VK_SUBGROUP_FEATURE_VOTE_BIT`, `VK_SUBGROUP_FEATURE_ARITHMETIC_BIT`, `VK_SUBGROUP_FEATURE_BALLOT_BIT`, `VK_SUBGROUP_FEATURE_SHUFFLE_BIT`, `VK_SUBGROUP_FEATURE_SHUFFLE_RELATIVE_BIT`, `VK_SUBGROUP_FEATURE_CLUSTERED_BIT`, `VK_SUBGROUP_FEATURE_QUAD_BIT`, `VK_SUBGROUP_FEATURE_ROTATE_BIT` and `VK_SUBGROUP_FEATURE_ROTATE_CLUSTERED_BIT` (`.properties.VkPhysicalDeviceVulkan11Properties.subgroupSupportedOperations`, lines 1249-1260).

## Compute limits

| Limit | Value | Locator in meas-780m-vulkaninfo |
|---|---|---|
| `maxComputeSharedMemorySize` | `65536` | `.properties.VkPhysicalDeviceProperties.limits.maxComputeSharedMemorySize`, line 791 |
| `maxComputeWorkGroupInvocations` | `1024` | `.properties.VkPhysicalDeviceProperties.limits.maxComputeWorkGroupInvocations`, line 797 |
| `maxComputeWorkGroupSize` | `[1024, 1024, 1024]` | `.properties.VkPhysicalDeviceProperties.limits.maxComputeWorkGroupSize`, lines 798-802 |
| `maxComputeWorkGroupCount` | `[4294967295, 65535, 65535]` | `.properties.VkPhysicalDeviceProperties.limits.maxComputeWorkGroupCount`, lines 792-796 |
| `maxImageDimension2D` | `16384` | `.properties.VkPhysicalDeviceProperties.limits.maxImageDimension2D`, line 741 |
| `maxImageDimension3D` | `2048` | `.properties.VkPhysicalDeviceProperties.limits.maxImageDimension3D`, line 742 |
| `maxStorageBufferRange` | `4294967295` | `.properties.VkPhysicalDeviceProperties.limits.maxStorageBufferRange`, line 747 |

`maxComputeSharedMemorySize` is the budget that a kernel's shared-memory staging arrays must fit in; `maxComputeWorkGroupInvocations` bounds the workgroup size. The image-dimension limits bound tensors and packed weights stored as textures.

## Cooperative matrix

`VK_KHR_cooperative_matrix` is listed with spec version `2` (`.extensions.VK_KHR_cooperative_matrix`, line 125) and the `cooperativeMatrix` feature is `true` (`.features.VkPhysicalDeviceCooperativeMatrixFeaturesKHR.cooperativeMatrix`, line 321). Details, including what the export does not contain, are on `hw-cooperative-matrix-rdna3`.

## fp16, int8, small-type storage, integer dot product

| Feature | Value | Locator in meas-780m-vulkaninfo |
|---|---|---|
| `shaderFloat16` | `true` | `.features.VkPhysicalDeviceVulkan12Features.shaderFloat16`, line 638 |
| `shaderInt8` | `true` | `.features.VkPhysicalDeviceVulkan12Features.shaderInt8`, line 639 |
| `shaderInt16` | `true` | `.features.VkPhysicalDeviceFeatures.shaderInt16`, line 265 |
| `storageBuffer8BitAccess` | `true` | `.features.VkPhysicalDeviceVulkan12Features.storageBuffer8BitAccess`, line 633 |
| `uniformAndStorageBuffer8BitAccess` | `true` | `.features.VkPhysicalDeviceVulkan12Features.uniformAndStorageBuffer8BitAccess`, line 634 |
| `storagePushConstant8` | `true` | `.features.VkPhysicalDeviceVulkan12Features.storagePushConstant8`, line 635 |
| `storageBuffer16BitAccess` | `true` | `.features.VkPhysicalDeviceVulkan11Features.storageBuffer16BitAccess`, line 617 |
| `uniformAndStorageBuffer16BitAccess` | `true` | `.features.VkPhysicalDeviceVulkan11Features.uniformAndStorageBuffer16BitAccess`, line 618 |
| `shaderIntegerDotProduct` | `true` | `.features.VkPhysicalDeviceVulkan13Features.shaderIntegerDotProduct`, line 693 |
| `integerDotProduct8BitUnsignedAccelerated` | `true` | `.properties.VkPhysicalDeviceVulkan13Properties`, line 1354 |
| `integerDotProduct8BitSignedAccelerated` | `true` | `.properties.VkPhysicalDeviceVulkan13Properties`, line 1355 |
| `integerDotProduct8BitMixedSignednessAccelerated` | `true` | `.properties.VkPhysicalDeviceVulkan13Properties`, line 1356 |
| `integerDotProduct4x8BitPackedUnsignedAccelerated` | `true` | `.properties.VkPhysicalDeviceVulkan13Properties`, line 1357 |
| `integerDotProduct4x8BitPackedSignedAccelerated` | `true` | `.properties.VkPhysicalDeviceVulkan13Properties`, line 1358 |
| `integerDotProduct4x8BitPackedMixedSignednessAccelerated` | `true` | `.properties.VkPhysicalDeviceVulkan13Properties`, line 1359 |

The matching extensions are listed too: `VK_KHR_shader_float16_int8` (line 187), `VK_KHR_8bit_storage` (line 119), `VK_KHR_16bit_storage` (line 118) and `VK_KHR_shader_integer_dot_product` (line 190), each with spec version `1` under `.extensions`.

## Shared-memory layout

`VK_KHR_workgroup_memory_explicit_layout` is listed (`.extensions`, line 216), with `workgroupMemoryExplicitLayout`, `workgroupMemoryExplicitLayoutScalarBlockLayout`, `workgroupMemoryExplicitLayout8BitAccess` and `workgroupMemoryExplicitLayout16BitAccess` all `true` (`.features.VkPhysicalDeviceWorkgroupMemoryExplicitLayoutFeaturesKHR`, lines 720-723).

## Memory

The export contains no memory heap list: a case-insensitive text search of the raw file `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json` (`grep -ci`) finds 0 lines for `memoryHeap` and 0 lines for `VkPhysicalDeviceMemoryProperties`. This page therefore states no heap sizes. The memory-related values that are present:

| Property | Value | Locator in meas-780m-vulkaninfo |
|---|---|---|
| `maxMemoryAllocationSize` | `4294967292` | `.properties.VkPhysicalDeviceVulkan11Properties.maxMemoryAllocationSize`, line 1267 |
| `maxBufferSize` | `4294967292` | `.properties.VkPhysicalDeviceVulkan13Properties.maxBufferSize`, line 1388 |
| `VK_EXT_memory_budget` | spec version `1` | `.extensions.VK_EXT_memory_budget`, line 70 |

## Limits of this page

- The six UUID fields of the raw file hold the string `REDACTED` (lines 912, 1206, 1209, 1228, 1229, 1474; for example `.properties.VkPhysicalDeviceVulkan11Properties.deviceUUID`, line 1228).
- The export does not enumerate cooperative-matrix shapes and does not list memory heaps.
- This page carries no timing or throughput numbers.
