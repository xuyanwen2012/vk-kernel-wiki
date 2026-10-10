---
id: doc-gpuopen-wmma-on-rdna3
title: "How to accelerate AI applications on RDNA 3 using WMMA (GPUOpen)"
author: "Aaryaman Vasishta, Takahiro Harada (AMD)"
url: https://gpuopen.com/learn/wmma_on_rdna3/
source_category: official-doc
architectures:
- rdna3
- rx-7900-xtx
tags:
- cooperative-matrix
- int8-cooperative-matrix
- coopmat-shape
- coopmat-fp32-accumulator
- bfloat16-arithmetic
- fp16-arithmetic
- subgroup-size
- wave64
- mma-shape-selection
- gemm
retrieved_at: '2026-10-10'
---

# How to accelerate AI applications on RDNA 3 using WMMA

Locator: https://gpuopen.com/learn/wmma_on_rdna3/ (article dated 2023-01-10; authors named on the page: Aaryaman Vasishta, Takahiro Harada)

Each excerpt is one paragraph of the article, copied in full unless the heading says otherwise; the number is the paragraph's position among the article's non-empty `<p>` elements. Table cells are numbered the same way among the non-empty `<th>` and `<td>` elements.

The article is not redistributable; only the elements below are quoted.

## Excerpt: paragraph 5 (data types and theoretical rate)

```text
WMMA supports inputs of FP16 or BF16 that can be useful for training online or offline, as well as 8-bit and 4-bit integer data types suitable for inference. The table below compares the theoretical FLOPS/clock/CU (floating point operations per clock, per compute unit) of our flagship Radeon RX 7900 XTX GPU based on the RDNA 3 architecture over the previous flagship Radeon RX 6950 XT GPU based on RDNA 2 for different data types:
```

## Excerpt: table header cells 1-3 and table cells 1-12 (one table row per line, cells separated by ` | `)

```text
Data type | RX 6950 XT FLOPS/clock/CU | RX 7900 XTX FLOPS/clock/CU
FP16 | 256 | 512
BF16 | N/A | 512
IU8 | 512 | 512
IU4 | 1024 | 1024
```

Conditions the article states for the table: devices in the column headings; the figures are "theoretical" (paragraph 5), not measured; software version: not applicable; date: article dated 2023-01-10.

## Excerpt: paragraph 7 (WMMA Overview)

```text
Unlike traditional per-thread matrix multiplication, WMMA allows the GPU to perform matrix multiplication cooperatively across an entire wavefront of 32 threads in wave32 mode or 64 threads in wave64 mode. This provides the benefit of sharing input/output matrix data across lanes of a wave, thus optimizing the VGPR usage and reducing memory traffic.
```

## Excerpt: paragraph 21 (tile size)

```text
The 16x16x16 represents the GEMM convention for the tile size for a MxNxK matrix multiply, where matrix A is of size MxK, matrix B of size KxN, and matrix C/D is of size MxN. In the case of RDNA 3, only 16x16 tile sizes are supported. If your matrix is larger than 16x16, then split it into chunks of 16x16 which can then be passed into the WMMA instruction. In the context of a wave, internally the WMMA instruction takes a tile of 16x16 for matrix A and a tile of 16x16 for matrix B. It then multiplies them to give a 16x16 tile, which is then added with matrix C to give the final 16x16 matrix D tile.
```

## Excerpt: paragraph 24 (registers per fragment, A and B)

```text
The A_frag, B_frag, C_frag, and D_frag parameters are the matrix fragments holding 16 elements each of matrices A, B, C and D respectively. From the perspective of a single lane (thread) within a wave, each “fragment” is locally stored in VGPRs, with each VGPR being 32 bits wide. Each thread holds A_frag and B_frag in 8 VGPRs for fp16/bf16, 4 VGPRs for iu8, and 2 VGPRs for iu4 regardless of the wave size.
```

## Excerpt: paragraph 25 (registers per fragment, C and D)

```text
C_frag and D_frag requires 8 VGPRs in wave32 mode and 4 VGPRs in wave64 mode, regardless of the datatype used by matrices C and D.
```

## Excerpt: paragraph 26 (lane replication)

```text
It is important to note that WMMA on RDNA 3 requires that the contents of A_frag and B_frag are replicated between lanes 0-15 and lanes 16-31 of the wave in wave32 mode. This means that for wave32 mode, each VGPR in lane 0 must have the exact same matrix data as each VGPR in lane 16. It is similar for lane 1 into lane 17, and so on, all the way to lane 15 into lane 31. This effectively maintains two copies of matrix data between the two half-waves. In wave64 mode, data from lanes 0-15 must also be replicated into lanes 32-47 and 48-63.
```

## Excerpt: table header cells 4-7 and table cells 13-36 (one table row per line, cells separated by ` | `)

```text
wave32 | wave64 | Matrix A,B format | Matrix C,D format
__builtin_amdgcn_wmma_f32_16x16x16_f16_w32 | __builtin_amdgcn_wmma_f32_16x16x16_f16_w64 | FP16 | FP32
__builtin_amdgcn_wmma_f32_16x16x16_bf16_w32 | __builtin_amdgcn_wmma_f32_16x16x16_bf16_w64 | BF16 | FP32
__builtin_amdgcn_wmma_f16_16x16x16_f16_w32 | __builtin_amdgcn_wmma_f16_16x16x16_f16_w64 | FP16 | FP16
__builtin_amdgcn_wmma_bf16_16x16x16_bf16_w32 | __builtin_amdgcn_wmma_bf16_16x16x16_bf16_w64 | BF16 | BF16
__builtin_amdgcn_wmma_i32_16x16x16_iu8_w32 | __builtin_amdgcn_wmma_i32_16x16x16_iu8_w64 | IU8 | I32
__builtin_amdgcn_wmma_i32_16x16x16_iu4_w32 | __builtin_amdgcn_wmma_i32_16x16x16_iu4_w64 | IU4 | I32
```

## Excerpt: paragraph 35 (matrix storage order and packing)

```text
WMMA requires a combination of row-major and column-major inputs for matrices A, B, C, and D. Matrix A is stored in column-major order, whereas matrices B, C, and D are all stored in row-major order. Matrices A and B are stored in packed format (i.e. each VGPR packs 2 fp16 values, 4 iu8 values, or 8 iu4 values), whereas matrices C and D are stored in unpacked format, with the “OPSEL” parameter used to describe the location of storage within the VGPR, described further below.
```
