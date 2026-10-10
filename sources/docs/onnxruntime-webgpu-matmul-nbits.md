---
id: doc-onnxruntime-webgpu-matmul-nbits
title: 'ONNX Runtime WebGPU execution provider (C++ host, WGSL templates, not GLSL): MatMulNBits kernel selection, tile sizes and subgroup-matrix path'
author: Microsoft Corporation
url: https://github.com/microsoft/onnxruntime/tree/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization
source_category: official-doc
architectures:
- intel
- nvidia
- qualcomm
tags:
- gemm
- workgroup-tile-sizing
- k-chunk-sizing
- per-shape-tile-selection
- required-subgroup-size
- subgroup-size-control
- subgroup-size
- fp32-accumulation
- integer-dot-product
- device-specific-tuning
retrieved_at: '2026-10-10'
description: 'Language / backend: C++ host code selecting WGSL shader templates for WebGPU (Dawn). Quoted: host-side selection and sizing rules for quantized matmul'
---

# ONNX Runtime WebGPU execution provider (C++ host, WGSL templates, not GLSL): MatMulNBits kernel selection, tile sizes and subgroup-matrix path

Language and backend of the source: C++ host code of the WebGPU execution provider, which instantiates WGSL templates; not GLSL. "Subgroup matrix" is the WebGPU (Dawn, experimental) counterpart of a cooperative matrix.

## Excerpt: onnxruntime/contrib_ops/webgpu/quantization/subgroup_matrix_matmul_nbits.cc, lines 16-36 (prepack: each subgroup matrix of A made contiguous)

Locator: https://github.com/microsoft/onnxruntime/blob/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization/subgroup_matrix_matmul_nbits.cc#L16-L36

```text
// This program optimizes the layout of input matrix A(MxK) for SubgroupMatrixLoad, so that all elements of each
// subgroup matrix(mxk) are arranged continuously in memory.
// Take "M = 4, K = 4, m = 2, k = 2" as an example, the input matrix A is arranged in row-major order as follows:
// d00, d01, | d02, d03,
// d10, d11, | d12, d13,
// ---------------------
// d20, d21, | d22, d23,
// d30, d31, | d32, d33,
//
// The prepack program rearranges the input matrix A to be in the following order:
// d00, d01,
// d10, d11,
// ---------
// d02, d03,
// d12, d13,
// ---------
// d20, d21,
// d30, d31,
// ---------
// d22, d23,
// d32, d33,
```

## Excerpt: onnxruntime/contrib_ops/webgpu/quantization/subgroup_matrix_matmul_nbits.cc, lines 187-215 (tile and workgroup size by matrix shape configuration and M)

Locator: https://github.com/microsoft/onnxruntime/blob/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization/subgroup_matrix_matmul_nbits.cc#L187-L215

```text
  // Determine tile sizes first (needed for prepack padding).
  uint32_t tile_m = 32;
  uint32_t tile_n = 64;
  uint32_t workgroup_size = 128;
  if (config.Is(8, 16, 16)) {
    // Default: 64x64 tile size, 256 thread.
    tile_m = 64;
    tile_n = 64;
    workgroup_size = 256;
    // Bias output uses a scratch tile, so keep it at 64x64 for workgroup memory limits.
    if (!has_bias) {
      if (M >= 2048 && N % 256 == 0) {
        // Large M (M>=2048): 128x256 tile size, 512 threads.
        tile_m = 128;
        tile_n = 256;
        workgroup_size = 512;
      } else if (M >= 256 && N % 128 == 0) {
        // Mid-sized M (256<=M<2048): 128x128 tile size, 512 threads.
        tile_m = 128;
        tile_n = 128;
        workgroup_size = 512;
      }
    }
  } else if (config.Is(16, 16, 16)) {
    // 16x16x16 config: 4 subgroups, 128 threads, 128x128 tiles
    tile_m = 128;
    tile_n = 128;
    workgroup_size = 128;
  }
```

## Excerpt: onnxruntime/contrib_ops/webgpu/quantization/subgroup_matrix_matmul_nbits.cc, lines 262-269 (pin the subgroup size; dispatch count)

Locator: https://github.com/microsoft/onnxruntime/blob/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization/subgroup_matrix_matmul_nbits.cc#L262-L269

```text
  // Pin kernels running on variable-size adapters to the subgroup size they were written for.
  if (context.HasFeature(wgpu::FeatureName::SubgroupSizeControl)) {
    matmul_program.SetSubgroupSize(config.subgroupSize);
  }

  uint32_t num_N_tile = CeilDiv(N, tile_n);
  uint32_t num_M_tile = CeilDiv(M, tile_m);
  matmul_program.SetDispatchGroupSize(num_N_tile, num_M_tile, 1);
```

## Excerpt: onnxruntime/contrib_ops/webgpu/quantization/subgroup_matrix_matmul_nbits.cc, lines 338-369 (preconditions; f16 accumulation and the fp32-accumulator request)

Locator: https://github.com/microsoft/onnxruntime/blob/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization/subgroup_matrix_matmul_nbits.cc#L338-L369

```text
  // Subgroup matrix kernels only support 4-bit/8-bit quantization with block_size 32.
  if (!((nbits == 4 || nbits == 8) && block_size == 32)) {
    return false;
  }

  if (M < kMinMForTileOptimization) {
    return false;
  }

  if (K % 32 != 0 || N % 64 != 0) {
    return false;
  }

  // TODO: Support batch.
  if (batch_count != 1) {
    return false;
  }

  // TODO: Support weight_idx_indirect.
  if (has_weight_idx_indirect) {
    return false;
  }

  // Every fp16 preference below has resultComponentType == F16, and the kernels declare
  // subgroup_matrix_result<f16, ...> to match, so the accumulation inside
  // subgroupMatrixMultiplyAccumulate is f16 and there is no variant of this kernel that can
  // honour an f32 accumulator request. Decline the path instead of ignoring the option: the
  // caller then falls through to a kernel that does honour it. Only fp16 outputs are affected;
  // the fp32 config accumulates in f32 already.
  if (is_fp16 && context.EnableMatmulFp32Accumulation()) {
    return false;
  }
```

## Excerpt: onnxruntime/contrib_ops/webgpu/quantization/matmul_nbits.cc, lines 246-247 (integer dot product on FP32-only and Qualcomm GPUs)

Locator: https://github.com/microsoft/onnxruntime/blob/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization/matmul_nbits.cc#L246-L247

```text
  // On FP32 only GPUs and Qualcomm GPUs, integer math is faster than FP32 therefore always use DP4A independent of length of M.
  // DP4A Q2 path now supports custom zero points via a 1024-entry LUT (4 zero-point sections × 256 byte values).
```

## Excerpt: onnxruntime/contrib_ops/webgpu/quantization/matmul_nbits.cc, lines 253-284 (wide-tile program for prefill; subgroup shuffle versus direct reduction)

Locator: https://github.com/microsoft/onnxruntime/blob/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization/matmul_nbits.cc#L253-L284

```text
  // WideTileProgram
  // This program is optimized for Block32 prefill.
  const bool use_wide_tile_program = CanApplyWideTileMatMulNBits(M,
                                                                 K,
                                                                 block_size,
                                                                 nbits,
                                                                 has_weight_idx_indirect,
                                                                 components_a,
                                                                 components_b);

  const bool acc_f32 = context.EnableMatmulFp32Accumulation();

  if (use_wide_tile_program) {
    // Enforce output components to 1.
    components = 1;

    constexpr uint32_t workgroup_size = 128;
    constexpr uint32_t tile_n = workgroup_size;
    const bool is_f16 = a->DataType() == DataTypeImpl::GetType<MLFloat16>();
    const uint32_t tile_m = is_f16 ? 2 * workgroup_size / 8 : workgroup_size / 8;
    const uint32_t num_N_tile = CeilDiv(N, tile_n);
    const uint32_t num_M_tile = CeilDiv(dispatch_M, tile_m);

    bool is_nvidia = context.AdapterInfo().vendor == std::string_view{"nvidia"};

    // The template shuffles tile_m lanes in bands of subgroup_min_size when that's a
    // width it supports; otherwise (including when Subgroups isn't supported) it falls
    // back to a direct reduction.
    // NOTE: NVIDIA GPUs prefer direct reduction.
    const uint32_t subgroup_min_size = (context.HasFeature(wgpu::FeatureName::Subgroups) && !is_nvidia)
                                           ? context.AdapterInfo().subgroupMinSize
                                           : 0u;
```

## Excerpt: onnxruntime/contrib_ops/webgpu/quantization/matmul_nbits.cc, lines 332-345 (K tile width per vendor and dispatch)

Locator: https://github.com/microsoft/onnxruntime/blob/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization/matmul_nbits.cc#L332-L345

```text
  // Use tile_size_k_vec=32 by default for better K-dimension parallelism.
  // Intel devices use 16 as they have different subgroup/cache characteristics.
  const uint32_t tile_size_k_vec =
      (context.AdapterInfo().vendor == std::string_view{"intel"}) ? 16u : 32u;

  constexpr uint32_t workgroup_size = 128;
  constexpr uint32_t tile_size = 8;
  constexpr uint32_t kU32Components = 4;
  uint32_t components_b_with_u32 = components_b * kU32Components;
  uint32_t K_of_b = (n_blocks_per_col * blob_size) / components_b_with_u32;
  MatMulNBitsProgram program{tile_size, static_cast<uint32_t>(nbits), has_zero_points, has_bias, has_weight_idx, has_weight_idx_indirect, single_scale_weights, tile_size_k_vec, broadcast_a, acc_f32};
  program.SetWorkgroupSize(workgroup_size);
  uint32_t num_N_tile = (N + tile_size - 1) / tile_size;
  program.SetDispatchGroupSize(num_N_tile, dispatch_M, batch_count);
```

## Excerpt: onnxruntime/contrib_ops/webgpu/quantization/dp4a_matmul_nbits.cc, lines 210-227 (when the DP4A path is used)

Locator: https://github.com/microsoft/onnxruntime/blob/8fc9fd597453baae1ad73379c313f0586d812867/onnxruntime/contrib_ops/webgpu/quantization/dp4a_matmul_nbits.cc#L210-L227

```text
  // macOS - Avoid using dp4a on Metal, as it does not appear to have native dp4a support.
  // https://github.com/gpuweb/gpuweb/issues/2677#issuecomment-1713292226
  // Use 'vendor' to check for metal; 'backend' is always WEBGPU when running under wasm.
  bool use_dp4a = context.HasFeature(wgpu::FeatureName::Subgroups) &&
                  context.AdapterInfo().vendor != std::string_view{"apple"};
  if (!(accuracy_level == 4 && block_size % 32 == 0 &&
        components_k == 4 && K % 128 == 0 && N % 16 == 0 &&
        use_dp4a)) {
    return false;
  }

  // Dispatch precondition: DP4A is used either when M is large enough (and the
  // weight is contiguous), or unconditionally on FP32-only GPUs and Qualcomm
  // GPUs where integer math beats FP32.
  const bool m_large_enough = (M >= kMinMForTileOptimization && !has_weight_idx_indirect);
  const bool fp32_output = (y != nullptr && y->DataType() == DataTypeImpl::GetType<float>());
  const bool qualcomm_vendor = context.AdapterInfo().vendor == std::string_view{"qualcomm"};
  return m_large_enough || fp32_output || qualcomm_vendor;
```

Licence of the excerpts: MIT, Copyright (c) Microsoft Corporation (file headers and `LICENSE` of the repository).
