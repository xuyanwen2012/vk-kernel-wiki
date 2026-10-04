---
id: meas-780m-vulkaninfo
title: "Vulkan device properties of the Radeon 780M on RADV Mesa 25.2.7 (vulkaninfo profile export)"
source_category: measurement
architectures: [radeon-780m]
tags: [cooperative-matrix, subgroup-size, subgroup-size-control, wave64, shared-memory-limit, fp16-arithmetic, int8-arithmetic, 8bit-storage, integer-dot-product]
device: radeon-780m
driver: "RADV Mesa 25.2.7"
measured_at: '2026-09-01'
method: "Vulkan profile JSON exported from vulkaninfo on the device (profile description: 'Exported from vulkaninfo'; history author: 'Automated export from vulkaninfo'). In the raw file the six UUID fields hold the string REDACTED (lines 912, 1206, 1209, 1228, 1229, 1474)."
raw_data:
  - locator: sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json
    description: "Vulkan profile export (profiles-0.8 schema) of the device: extensions, features, properties, formats, queue families. The six UUID fields hold the string REDACTED."
captured_at: '2026-10-03'
---

Raw file for every excerpt below: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`. Line numbers are 1-based lines of that file; excerpt lines are copied verbatim, including leading tabs.

## Excerpt: Profile identity, API version and export date

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 11208-11225; JSON path `$.profiles["VP_VULKANINFO_AMD_Radeon_780M_Graphics_(RADV_PHOENIX)_25_2_7"] (keys version, api-version, label, description, contributors, history[0].date, capabilities)`

```json
	"profiles": {
		"VP_VULKANINFO_AMD_Radeon_780M_Graphics_(RADV_PHOENIX)_25_2_7": {
			"version": 1,
			"api-version": "1.4.318",
			"label": "AMD Radeon 780M Graphics (RADV PHOENIX) driver 25.2.7",
			"description": "Exported from vulkaninfo",
			"contributors": {

			},
			"history": [
				{
					"revision": 1,
					"date": "2026-9-1",
					"author": "Automated export from vulkaninfo",
					"comment": ""
				}
			],
			"capabilities": [
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 2; JSON path `$["$schema"]`

```json
	"$schema": "https://schema.khronos.org/vulkan/profiles-0.8-latest.json",
```

## Excerpt: Device identity

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 733-738; JSON path `$.capabilities.device.properties.VkPhysicalDeviceProperties (keys apiVersion, deviceID, deviceName, deviceType, driverVersion)`

```json
				"VkPhysicalDeviceProperties": {
					"apiVersion": 4211006,
					"deviceID": 5567,
					"deviceName": "AMD Radeon 780M Graphics (RADV PHOENIX)",
					"deviceType": "VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU",
					"driverVersion": 104865799,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 920; JSON path `$.capabilities.device.properties.VkPhysicalDeviceProperties.vendorID`

```json
					"vendorID": 4098
```

## Excerpt: Driver identity

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 1269-1278; JSON path `$.capabilities.device.properties.VkPhysicalDeviceVulkan12Properties (keys driverID, driverName, driverInfo, conformanceVersion)`

```json
				"VkPhysicalDeviceVulkan12Properties": {
					"driverID": "VK_DRIVER_ID_MESA_RADV",
					"driverName": "radv",
					"driverInfo": "Mesa 25.2.7",
					"conformanceVersion": {
						"major": 1,
						"minor": 4,
						"subminor": 0,
						"patch": 0
					},
```

## Excerpt: Subgroup properties

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 1232-1261; JSON path `$.capabilities.device.properties.VkPhysicalDeviceVulkan11Properties (keys subgroupSize, subgroupSupportedStages, subgroupSupportedOperations, subgroupQuadOperationsInAllStages)`

```json
					"subgroupSize": 64,
					"subgroupSupportedStages": [
						"VK_SHADER_STAGE_VERTEX_BIT",
						"VK_SHADER_STAGE_TESSELLATION_CONTROL_BIT",
						"VK_SHADER_STAGE_TESSELLATION_EVALUATION_BIT",
						"VK_SHADER_STAGE_GEOMETRY_BIT",
						"VK_SHADER_STAGE_FRAGMENT_BIT",
						"VK_SHADER_STAGE_COMPUTE_BIT",
						"VK_SHADER_STAGE_RAYGEN_BIT_KHR",
						"VK_SHADER_STAGE_ANY_HIT_BIT_KHR",
						"VK_SHADER_STAGE_CLOSEST_HIT_BIT_KHR",
						"VK_SHADER_STAGE_MISS_BIT_KHR",
						"VK_SHADER_STAGE_INTERSECTION_BIT_KHR",
						"VK_SHADER_STAGE_CALLABLE_BIT_KHR",
						"VK_SHADER_STAGE_TASK_BIT_EXT",
						"VK_SHADER_STAGE_MESH_BIT_EXT"
					],
					"subgroupSupportedOperations": [
						"VK_SUBGROUP_FEATURE_BASIC_BIT",
						"VK_SUBGROUP_FEATURE_VOTE_BIT",
						"VK_SUBGROUP_FEATURE_ARITHMETIC_BIT",
						"VK_SUBGROUP_FEATURE_BALLOT_BIT",
						"VK_SUBGROUP_FEATURE_SHUFFLE_BIT",
						"VK_SUBGROUP_FEATURE_SHUFFLE_RELATIVE_BIT",
						"VK_SUBGROUP_FEATURE_CLUSTERED_BIT",
						"VK_SUBGROUP_FEATURE_QUAD_BIT",
						"VK_SUBGROUP_FEATURE_ROTATE_BIT",
						"VK_SUBGROUP_FEATURE_ROTATE_CLUSTERED_BIT"
					],
					"subgroupQuadOperationsInAllStages": true,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 1339-1347; JSON path `$.capabilities.device.properties.VkPhysicalDeviceVulkan13Properties (keys minSubgroupSize, maxSubgroupSize, maxComputeWorkgroupSubgroups, requiredSubgroupSizeStages)`

```json
				"VkPhysicalDeviceVulkan13Properties": {
					"minSubgroupSize": 32,
					"maxSubgroupSize": 64,
					"maxComputeWorkgroupSubgroups": 4294967295,
					"requiredSubgroupSizeStages": [
						"VK_SHADER_STAGE_COMPUTE_BIT",
						"VK_SHADER_STAGE_TASK_BIT_EXT",
						"VK_SHADER_STAGE_MESH_BIT_EXT"
					],
```

## Excerpt: Subgroup features and extensions

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 687-688; JSON path `$.capabilities.device.features.VkPhysicalDeviceVulkan13Features (keys subgroupSizeControl, computeFullSubgroups)`

```json
					"subgroupSizeControl": true,
					"computeFullSubgroups": true,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 665; JSON path `$.capabilities.device.features.VkPhysicalDeviceVulkan12Features.shaderSubgroupExtendedTypes`

```json
					"shaderSubgroupExtendedTypes": true,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 698-699; JSON path `$.capabilities.device.features.VkPhysicalDeviceVulkan14Features (keys shaderSubgroupRotate, shaderSubgroupRotateClustered)`

```json
					"shaderSubgroupRotate": true,
					"shaderSubgroupRotateClustered": true,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 587-589; JSON path `$.capabilities.device.features.VkPhysicalDeviceShaderSubgroupUniformControlFlowFeaturesKHR`

```json
				"VkPhysicalDeviceShaderSubgroupUniformControlFlowFeaturesKHR": {
					"shaderSubgroupUniformControlFlow": true
				},
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 569-571; JSON path `$.capabilities.device.features.VkPhysicalDeviceShaderMaximalReconvergenceFeaturesKHR`

```json
				"VkPhysicalDeviceShaderMaximalReconvergenceFeaturesKHR": {
					"shaderMaximalReconvergence": true
				},
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 102-105; JSON path `$.capabilities.device.extensions (keys VK_EXT_shader_subgroup_ballot, VK_EXT_shader_subgroup_vote, VK_EXT_subgroup_size_control; line 104 is the neighbouring key in between)`

```json
				"VK_EXT_shader_subgroup_ballot": 1,
				"VK_EXT_shader_subgroup_vote": 1,
				"VK_EXT_shader_viewport_index_layer": 1,
				"VK_EXT_subgroup_size_control": 2,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 191; JSON path `$.capabilities.device.extensions.VK_KHR_shader_maximal_reconvergence`

```json
				"VK_KHR_shader_maximal_reconvergence": 1,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 195-197; JSON path `$.capabilities.device.extensions (keys VK_KHR_shader_subgroup_extended_types, VK_KHR_shader_subgroup_rotate, VK_KHR_shader_subgroup_uniform_control_flow)`

```json
				"VK_KHR_shader_subgroup_extended_types": 1,
				"VK_KHR_shader_subgroup_rotate": 2,
				"VK_KHR_shader_subgroup_uniform_control_flow": 1,
```

## Excerpt: Cooperative matrix: extension, features, properties

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 125; JSON path `$.capabilities.device.extensions.VK_KHR_cooperative_matrix`

```json
				"VK_KHR_cooperative_matrix": 2,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 320-323; JSON path `$.capabilities.device.features.VkPhysicalDeviceCooperativeMatrixFeaturesKHR`

```json
				"VkPhysicalDeviceCooperativeMatrixFeaturesKHR": {
					"cooperativeMatrix": true,
					"cooperativeMatrixRobustBufferAccess": true
				},
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 946-950; JSON path `$.capabilities.device.properties.VkPhysicalDeviceCooperativeMatrixPropertiesKHR`

```json
				"VkPhysicalDeviceCooperativeMatrixPropertiesKHR": {
					"cooperativeMatrixSupportedStages": [
						"VK_SHADER_STAGE_COMPUTE_BIT"
					]
				},
```

## Excerpt: Compute limits

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 791-802; JSON path `$.capabilities.device.properties.VkPhysicalDeviceProperties.limits (keys maxComputeSharedMemorySize, maxComputeWorkGroupCount, maxComputeWorkGroupInvocations, maxComputeWorkGroupSize)`

```json
						"maxComputeSharedMemorySize": 65536,
						"maxComputeWorkGroupCount": [
							4294967295,
							65535,
							65535
						],
						"maxComputeWorkGroupInvocations": 1024,
						"maxComputeWorkGroupSize": [
							1024,
							1024,
							1024
						],
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 741-742; JSON path `$.capabilities.device.properties.VkPhysicalDeviceProperties.limits (keys maxImageDimension2D, maxImageDimension3D)`

```json
						"maxImageDimension2D": 16384,
						"maxImageDimension3D": 2048,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 747; JSON path `$.capabilities.device.properties.VkPhysicalDeviceProperties.limits.maxStorageBufferRange`

```json
						"maxStorageBufferRange": 4294967295,
```

## Excerpt: float16, int8, 8-bit and 16-bit storage

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 187; JSON path `$.capabilities.device.extensions.VK_KHR_shader_float16_int8`

```json
				"VK_KHR_shader_float16_int8": 1,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 118-119; JSON path `$.capabilities.device.extensions (keys VK_KHR_16bit_storage, VK_KHR_8bit_storage)`

```json
				"VK_KHR_16bit_storage": 1,
				"VK_KHR_8bit_storage": 1,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 633-635; JSON path `$.capabilities.device.features.VkPhysicalDeviceVulkan12Features (keys storageBuffer8BitAccess, uniformAndStorageBuffer8BitAccess, storagePushConstant8)`

```json
					"storageBuffer8BitAccess": true,
					"uniformAndStorageBuffer8BitAccess": true,
					"storagePushConstant8": true,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 638-639; JSON path `$.capabilities.device.features.VkPhysicalDeviceVulkan12Features (keys shaderFloat16, shaderInt8)`

```json
					"shaderFloat16": true,
					"shaderInt8": true,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 616-620; JSON path `$.capabilities.device.features.VkPhysicalDeviceVulkan11Features (keys storageBuffer16BitAccess, uniformAndStorageBuffer16BitAccess, storagePushConstant16, storageInputOutput16)`

```json
				"VkPhysicalDeviceVulkan11Features": {
					"storageBuffer16BitAccess": true,
					"uniformAndStorageBuffer16BitAccess": true,
					"storagePushConstant16": true,
					"storageInputOutput16": true,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 263-265; JSON path `$.capabilities.device.features.VkPhysicalDeviceFeatures (keys shaderFloat64, shaderInt64, shaderInt16)`

```json
					"shaderFloat64": true,
					"shaderInt64": true,
					"shaderInt16": true,
```

## Excerpt: Integer dot product

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 190; JSON path `$.capabilities.device.extensions.VK_KHR_shader_integer_dot_product`

```json
				"VK_KHR_shader_integer_dot_product": 1,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 693; JSON path `$.capabilities.device.features.VkPhysicalDeviceVulkan13Features.shaderIntegerDotProduct`

```json
					"shaderIntegerDotProduct": true,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 1354-1359; JSON path `$.capabilities.device.properties.VkPhysicalDeviceVulkan13Properties (keys integerDotProduct8Bit*Accelerated, integerDotProduct4x8BitPacked*Accelerated)`

```json
					"integerDotProduct8BitUnsignedAccelerated": true,
					"integerDotProduct8BitSignedAccelerated": true,
					"integerDotProduct8BitMixedSignednessAccelerated": true,
					"integerDotProduct4x8BitPackedUnsignedAccelerated": true,
					"integerDotProduct4x8BitPackedSignedAccelerated": true,
					"integerDotProduct4x8BitPackedMixedSignednessAccelerated": true,
```

## Excerpt: Workgroup memory explicit layout

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 216; JSON path `$.capabilities.device.extensions.VK_KHR_workgroup_memory_explicit_layout`

```json
				"VK_KHR_workgroup_memory_explicit_layout": 1,
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 719-724; JSON path `$.capabilities.device.features.VkPhysicalDeviceWorkgroupMemoryExplicitLayoutFeaturesKHR`

```json
				"VkPhysicalDeviceWorkgroupMemoryExplicitLayoutFeaturesKHR": {
					"workgroupMemoryExplicitLayout": true,
					"workgroupMemoryExplicitLayoutScalarBlockLayout": true,
					"workgroupMemoryExplicitLayout8BitAccess": true,
					"workgroupMemoryExplicitLayout16BitAccess": true
				},
```

## Excerpt: Memory-related values

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 1267; JSON path `$.capabilities.device.properties.VkPhysicalDeviceVulkan11Properties.maxMemoryAllocationSize`

```json
					"maxMemoryAllocationSize": 4294967292
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 1388; JSON path `$.capabilities.device.properties.VkPhysicalDeviceVulkan13Properties.maxBufferSize`

```json
					"maxBufferSize": 4294967292
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 70; JSON path `$.capabilities.device.extensions.VK_EXT_memory_budget`

```json
				"VK_EXT_memory_budget": 1,
```

## Excerpt: Redacted fields

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, lines 1228-1229; JSON path `$.capabilities.device.properties.VkPhysicalDeviceVulkan11Properties (keys deviceUUID, driverUUID)`

```json
					"deviceUUID": "REDACTED",
					"driverUUID": "REDACTED",
```

Locator: `sources/measurements/780m-vulkaninfo/vulkaninfo-profile-radv-mesa-25.2.7.json`, line 912; JSON path `$.capabilities.device.properties.VkPhysicalDeviceProperties.pipelineCacheUUID`

```json
					"pipelineCacheUUID": "REDACTED",
```
