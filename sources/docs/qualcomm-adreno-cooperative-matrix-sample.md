---
id: doc-qualcomm-adreno-cooperative-matrix-sample
title: 'Adreno GPU Vulkan code sample framework: cooperative matrix sample (GEMM, vector-to-matrix GEMM, convolution)'
author: Qualcomm Innovation Center, Inc.
url: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/tree/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix
source_category: upstream-code
architectures:
- qualcomm
tags:
- cooperative-matrix
- int8-cooperative-matrix
- coopmat-shape
- subgroup-size
- subgroup-size-control
- wave64
- fp16-arithmetic
- int8-arithmetic
- specialization-constants
- workgroup-tile-sizing
- mma-shape-selection
- required-subgroup-size
- gemm
- convolution
retrieved_at: '2026-10-10'
description: Vendor sample, GLSL embedded in C++ headers; complete files are in artifacts/kernels/adreno-cooperative-matrix-sample
---

# Adreno GPU Vulkan code sample framework: cooperative matrix sample (GEMM, vector-to-matrix GEMM, convolution)

Complete files, pinned to the commit in the locators: `artifacts/kernels/adreno-cooperative-matrix-sample/` (`README.md`, `MxM_Basic.hpp`, `MxM_VecToMat.hpp`, `Conv.hpp`).

## Excerpt: samples/cooperative_matrix/README.md, lines 5-7 (what the sample runs)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/README.md#L5-L7

```text
Runs matrix operations on supported Adreno™ GPUs using `VK_KHR_cooperative_matrix`. The application queries supported tile sizes and component types before creating a workload.

The default layout comparison measures alternative input layouts. The UI also exposes custom layouts and legacy tests. Validate GPU output against the CPU reference before interpreting timings. Available cases, including Qualcomm™-specific paths, depend on device capabilities.
```

## Excerpt: samples/cooperative_matrix/README.md, lines 15-19 (kernel definition and input layouts)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/README.md#L15-L19

```text
Both GEMM kernels compute `R = A × B`, with A shaped M×K and B shaped K×N. They start the accumulator at zero. The C binding is reserved and is not added to the result.

The default comparison uses Tiled K-first inputs, with TILE_K contiguous elements per row of each tile. A uses `row * TILE_K + step * TOTAL_M`; B uses `col * TILE_K + step * TOTAL_N`. M-first A, N-first B, and both output layouts remain in the table to measure their tradeoffs. Select **Legacy K-first comparison** to measure plain K-first input layouts. C and R have M and N axes, so their layouts are named M-first or N-first.

For non-tiled matrices, the allocator adds 64 bytes when the line stride is a multiple of 128 bytes. Tiled inputs need no line padding. Input packing always follows the selected layout, regardless of whether validation is enabled.
```

## Excerpt: samples/cooperative_matrix/README.md, lines 21-23 (workgroup baseline, default shapes, vector-to-matrix requirements)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/README.md#L21-L23

```text
The Adreno workgroup baseline is 64×2×2 invocations, covering two subgroup tiles in M and two in N. Tile sizes and types must match a queried, non-saturating subgroup property. Dispatch limits and subgroup controls are checked before a test is created. Defaults cover M512×N384, with K1024 for FP32, K2048 for FP16, and K4096 for signed and unsigned INT8. The three N tiles are 64, 32, and 16. Other devices can expose different tile sizes; record the actual dimensions printed with each result.

Vector-to-matrix GEMM requires the QCOM conversion feature and a 64-lane subgroup with one lane per tile row. It supports the same layouts as basic GEMM. Convolution uses channels-contiguous input, a 3×3 filter, stride 1, dilation 1, and zero padding. It checks signed coordinates before loading edge pixels. Its fixed K-first input/filter and N-first output layouts follow the implicit im2col access pattern.
```

## Excerpt: samples/cooperative_matrix/README.md, lines 25-31 (validation, timing method, peak-percentage caveat)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/README.md#L25-L31

```text
CPU validation covers all three kernels. Integer results must match exactly; floating-point comparisons reject non-finite values and use the displayed tolerance. Validation runs outside the GPU timing interval. One untimed dispatch warms each pipeline before measured repetitions.

The start timestamp waits at the compute stage after the preceding dispatch dependency. This prevents the first measured interval from including unfinished warmup work. Timings report the average dispatch interval, excluding input layout conversion and uploads.

Vector-to-matrix GEMM loads contiguous FP16 and INT8 A inputs as packed 32-bit words for QCOM conversion. It gathers and packs strided M-first INT8 input; M-first FP16 and FP32 retain typed loads. Basic GEMM continues to use direct cooperative loads; compare the paths on the target driver before choosing one for an application.

Peak percentage is disabled by default. To use it, supply documented peak TOPS for the tested device and datatype at the stated frequency. The sample does not infer theoretical throughput from a GPU name or from another device's measured table. Compare published tables only with matching dimensions, layouts, tile sizes, driver, and measured GPU and memory frequencies. Large tiles and a 2×2 workgroup are starting points; they do not by themselves prove peak occupancy.
```

## Excerpt: samples/cooperative_matrix/code/main/runtime_shaders/MxM_Basic.hpp, lines 30-55 (specialization constants and local size)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/code/main/runtime_shaders/MxM_Basic.hpp#L30-L55

```text
layout(constant_id = 0) const uint lsx = 64;
layout(constant_id = 1) const uint lsy = 2;
layout(constant_id = 2) const uint lsz = 2;
layout(constant_id = 3) const uint TOTAL_M = 1;
layout(constant_id = 4) const uint TOTAL_N = 1;
layout(constant_id = 5) const uint TOTAL_K = 1;
layout(constant_id = 6) const uint TILE_M = 1;
layout(constant_id = 7) const uint TILE_N = 1;
layout(constant_id = 8) const uint TILE_K = 1;
layout(constant_id = 9)  const bool layoutA_Mfirst = false;
layout(constant_id = 10) const bool layoutB_Nfirst = false;
layout(constant_id = 11) const bool layoutA_TiledKfirst = true;
layout(constant_id = 12) const bool layoutB_TiledKfirst = true;
layout(constant_id = 13) const bool layoutC_Mfirst = false;
layout(constant_id = 14) const bool layoutR_Mfirst = false;
layout(constant_id = 15) const uint strideAinElements = 1;
layout(constant_id = 16) const uint strideBinElements = 1;
layout(constant_id = 17) const uint strideCinElements = 1;
layout(constant_id = 18) const uint strideRinElements = 1;

layout(set=0, binding=0) readonly buffer InputA { A_TYPE x[]; } inputA;
layout(set=0, binding=1) readonly buffer InputB { A_TYPE x[]; } inputB;
layout(set=0, binding=2) readonly buffer InputC { R_TYPE x[]; } inputC;
layout(set=0, binding=3)  buffer Output { R_TYPE x[]; } outputO;

layout(local_size_x_id = 0, local_size_y_id = 1, local_size_z_id = 2) in;
```

## Excerpt: samples/cooperative_matrix/code/main/runtime_shaders/MxM_Basic.hpp, lines 57-104 (basic GEMM main loop)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/code/main/runtime_shaders/MxM_Basic.hpp#L57-L104

```text
void main()
{
    const uint32_t block_id_m = gl_GlobalInvocationID.y;
    const uint32_t block_id_n = gl_GlobalInvocationID.z;
    if ((block_id_m >= TOTAL_M/TILE_M) || (block_id_n >= TOTAL_N/TILE_N)) return;

    const uint32_t row = block_id_m * TILE_M;
    const uint32_t col = block_id_n * TILE_N;

    coopmat<R_TYPE, gl_ScopeSubgroup, TILE_M, TILE_N, gl_MatrixUseAccumulator> matR;
    matR = coopmat<R_TYPE, gl_ScopeSubgroup, TILE_M, TILE_N, gl_MatrixUseAccumulator>(0.0);

    for (uint32_t step = 0; step < TOTAL_K; step += TILE_K)
    {
        coopmat<A_TYPE, gl_ScopeSubgroup, TILE_M, TILE_K, gl_MatrixUseA> matA;
        if (layoutA_Mfirst)
        {
            coopMatLoad(matA, inputA.x, row + step * strideAinElements, strideAinElements, 1);
        }
        else if (layoutA_TiledKfirst)
        {
            coopMatLoad(matA, inputA.x, row * TILE_K + step * TOTAL_M, TILE_K, 0);
        }
        else
        {
            coopMatLoad(matA, inputA.x, row * strideAinElements + step, strideAinElements, 0);
        }

        coopmat<A_TYPE, gl_ScopeSubgroup, TILE_K, TILE_N, gl_MatrixUseB> matB;
        if (layoutB_Nfirst)
        {
            coopMatLoad(matB, inputB.x, col + step * strideBinElements, strideBinElements, 0);
        }
        else if (layoutB_TiledKfirst)
        {
            coopMatLoad(matB, inputB.x, col * TILE_K + step * TOTAL_N, TILE_K, 1);
        }
        else
        {
            coopMatLoad(matB, inputB.x, col * strideBinElements + step, strideBinElements, 1);
        }

        matR = coopMatMulAdd(matA, matB, matR);
    }

    uint32_t subMatrixRStartInElements = layoutR_Mfirst ? col * strideRinElements + row : row * strideRinElements + col;
    coopMatStore(matR, outputO.x, subMatrixRStartInElements, strideRinElements, int(layoutR_Mfirst));
}
```

## Excerpt: samples/cooperative_matrix/code/main/runtime_shaders/MxM_VecToMat.hpp, lines 74-115 (per-lane A row packed into words and converted with vectorToCoopmatQCOM)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/code/main/runtime_shaders/MxM_VecToMat.hpp#L74-L115

```text
    for (uint32_t step = 0; step < TOTAL_K; step += TILE_K)
    {
        coopmat<A_TYPE, gl_ScopeSubgroup, TILE_M, TILE_K, gl_MatrixUseA> matA;
        const uint laneRow = row + gl_SubgroupInvocationID;
#if PACKED_A
        // QCOM conversion interprets each word as NUM_PACK input components.
        uint32_t vecA[TILE_K / NUM_PACK];
        if (layoutA_Mfirst)
        {
            // Gather strided INT8 components without changing their bit patterns.
            const uint bitsPerComponent = 32 / NUM_PACK;
            const uint componentMask = (1u << bitsPerComponent) - 1u;
            for (uint k = 0; k < TILE_K / NUM_PACK; ++k)
            {
                uint packed = 0;
                for (uint c = 0; c < NUM_PACK; ++c)
                {
                    const uint offset = laneRow + (step + k * NUM_PACK + c) * strideAinElements;
                    const uint component = (inputA.x[offset / NUM_PACK] >> ((offset % NUM_PACK) * bitsPerComponent)) & componentMask;
                    packed |= component << (c * bitsPerComponent);
                }
                vecA[k] = packed;
            }
        }
        else
        {
            const uint wordOffset = (layoutA_TiledKfirst ? laneRow * TILE_K + step * TOTAL_M
                                                       : laneRow * strideAinElements + step) / NUM_PACK;
            for (uint k = 0; k < TILE_K / NUM_PACK; ++k)
                vecA[k] = inputA.x[wordOffset + k];
        }
#else
        A_TYPE vecA[TILE_K];
        for (uint k = 0; k < TILE_K; ++k)
        {
            const uint offset = layoutA_Mfirst ? laneRow + (step + k) * strideAinElements
                : (layoutA_TiledKfirst ? laneRow * TILE_K + step * TOTAL_M + k
                                      : laneRow * strideAinElements + step + k);
            vecA[k] = inputA.x[offset];
        }
#endif
        vectorToCoopmatQCOM(vecA, matA);
```

## Excerpt: samples/cooperative_matrix/code/main/runtime_shaders/Conv.hpp, lines 83-121 (implicit im2col convolution loop)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/code/main/runtime_shaders/Conv.hpp#L83-L121

```text
    for (uint32_t step = 0; step < TOTAL_K; step += TILE_K)
    {
        uint32_t subMatrixBStartInElements = col * FILTER_H * FILTER_W * strideBinElements + step; // B is Kfirst
        for (uint32_t filter_row = 0; filter_row < FILTER_H; filter_row++)
        {
            for (uint32_t filter_col = 0; filter_col < FILTER_W; filter_col++)
            {
                coopmat<A_TYPE, gl_ScopeSubgroup, TILE_K, TILE_N, gl_MatrixUseB> matB;
                coopmat<A_TYPE, gl_ScopeSubgroup, TILE_M, TILE_K, gl_MatrixUseA> matA;

                // load B matrix input data using coop_mat extension
                coopMatLoad(matB, inputB.x, subMatrixBStartInElements, FILTER_H * FILTER_W * strideBinElements, int(true));

                // Check signed spatial coordinates before touching the input buffer.
                const int input_row_id = int(STRIDE * out_row_id) + int(DILATION) * (int(filter_row) - int(filter_offset_h));
                const int input_col_id = int(STRIDE * out_col_id) + int(DILATION) * (int(filter_col) - int(filter_offset_w));
                const bool inBounds = input_row_id >= 0 && input_row_id < int(INPUT_H)
                    && input_col_id >= 0 && input_col_id < int(INPUT_W);
                uint32_t vecA[TILE_K / NUM_PACK];
                for (uint i = 0; i < TILE_K / NUM_PACK; ++i)
                {
                    vecA[i] = 0;
                    if (inBounds)
                        vecA[i] = inputAuint.x[((uint(input_row_id) * INPUT_W + uint(input_col_id)) * strideAinElements + step) / NUM_PACK + i];
                }

                // convert A vector to A matrix
                vectorToCoopmatQCOM(vecA, matA);

                matR = coopMatMulAdd(matA, matB, matR);

                subMatrixBStartInElements += strideBinElements;
            }
        }
    }

    // Store results
    uint32_t subMatrixRStartInElements = row * strideRinElements + col;
    coopMatStore(matR, outputO.x, subMatrixRStartInElements, strideRinElements, int(false));
```

## Excerpt: samples/cooperative_matrix/code/main/cooperative_matrix_tester.cpp, lines 1293-1305 (subgroup-size-control and dispatch-limit checks before a test is created)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/code/main/cooperative_matrix_tester.cpp#L1293-L1305

```text
    const auto* subgroupControl = m_vulkan_instance.GetExtension<ExtensionLib::Ext_VK_EXT_subgroup_size_control>();
    if (!subgroupControl || !subgroupControl->RequestedFeatures.subgroupSizeControl
        || !(subgroupControl->Properties.requiredSubgroupSizeStages & VK_SHADER_STAGE_COMPUTE_BIT)
        || subgroup_size < subgroupControl->Properties.minSubgroupSize || subgroup_size > subgroupControl->Properties.maxSubgroupSize
        || local_size_x > device_limits.maxComputeWorkGroupSize[0]
        || local_size_y > device_limits.maxComputeWorkGroupSize[1] || local_size_z > device_limits.maxComputeWorkGroupSize[2]
        || local_size_x * local_size_y * local_size_z > device_limits.maxComputeWorkGroupInvocations
        || (MSizeInBlocks + local_size_y - 1) / local_size_y > device_limits.maxComputeWorkGroupCount[1]
        || (NSizeInBlocks + local_size_z - 1) / local_size_z > device_limits.maxComputeWorkGroupCount[2])
    {
        LOGI("Skipping test: subgroup or dispatch requirements exceed device support.");
        return std::nullopt;
    }
```

## Excerpt: samples/cooperative_matrix/code/main/cooperative_matrix_tester.cpp, lines 1589-1595 (pipeline created with a required subgroup size)

Locator: https://github.com/SnapdragonGameStudios/adreno-gpu-vulkan-code-sample-framework/blob/584f0528d46d120a73b4f7bbd0102abfb358220b/samples/cooperative_matrix/code/main/cooperative_matrix_tester.cpp#L1589-L1595

```text
    // Create pipeline with a desired subgroup size (e.g., AMD supports two subgroup sizes)
    VkPipelineShaderStageRequiredSubgroupSizeCreateInfo subgroupSizeInfo = {};
    subgroupSizeInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_REQUIRED_SUBGROUP_SIZE_CREATE_INFO;
    subgroupSizeInfo.requiredSubgroupSize = subgroup_size; // Must be between min and max

    // SPIR-V 1.6 does not require REQUIRE_FULL_SUBGROUPS. X still equals the pinned subgroup size.
    VkPipelineShaderStageCreateInfo shaderCreateInfo   = {VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO, &subgroupSizeInfo, 0, VK_SHADER_STAGE_COMPUTE_BIT, shaderModule, "main", &specInfo};
```

Licence of the excerpts: BSD-3-Clause, Copyright (c) Qualcomm Innovation Center, Inc.; see `artifacts/prs/adreno-samples/LICENSE`.
