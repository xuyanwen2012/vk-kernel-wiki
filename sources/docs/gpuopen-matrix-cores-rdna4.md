---
id: doc-gpuopen-matrix-cores-rdna4
title: "Using the Matrix Cores of AMD RDNA 4 architecture GPUs (GPUOpen)"
author: "Takahiro Harada, Atsushi Yoshimura (AMD)"
url: https://gpuopen.com/learn/using_matrix_core_amd_rdna4/
source_category: vendor-doc
architectures:
- rdna4
- rx-9070-xt
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
- mma-shape-selection
- gemm
retrieved_at: '2026-10-10'
---

# Using the Matrix Cores of AMD RDNA 4 architecture GPUs

Locator: https://gpuopen.com/learn/using_matrix_core_amd_rdna4/ (article dated 2025-07-11; authors named on the page: Takahiro Harada, Atsushi Yoshimura)

Each excerpt is one paragraph of the article, copied in full unless the heading says otherwise; the number is the paragraph's position among the article's non-empty `<p>` elements. Table cells are numbered the same way among the non-empty `<th>` and `<td>` elements.

The article is not redistributable; only the elements below are quoted.

## Excerpt: paragraph 1 (generations and layout change)

```text
AMD RDNA™ 4 architecture GPUs, which have 3rd-generation Matrix Cores, improved the performance of Generalized Matrix Multiplication (GEMM) operations. The table below compares theoretical FLOPS/clock/CU (floating point operations per clock, per compute unit) to previous generations. However, we changed the VGPR layout for the arguments of Wave Matrix Multiply Accumulate (WMMA) operations compared to the previous RDNA 3 generation [1]. Therefore, it does not have backward compatibility. In order to accelerate GEMM operations on RDNA 4 GPUs, we need to use the new intrinsics added for GPUs of this generation. In this post, we explain how to use matrix cores on RDNA 4 GPUs from a HIP kernel.
```

## Excerpt: table header cells 1-3 and table cells 1-12 (one table row per line, cells separated by ` | `; the first header cell of the table is empty)

```text
 | AMD Radeon™ RX 6950 XT (RDNA 2) | AMD Radeon™ RX 7900 XTX (RDNA 3) | AMD Radeon™ RX 9070 XT (RDNA 4)
FP16 | 256 | 512 | 1024
BF16 | N/A | 512 | 1024
I8 | 512 | 512 | 2048
```

Conditions the article states for the table: devices in the column headings; the figures are "theoretical FLOPS/clock/CU" (paragraph 1), not measured; software version: not applicable; date: article dated 2025-07-11.

## Excerpt: paragraph 3 (matrix dimension)

```text
WMMA operates on matrices of 16x16 dimension only. Thus, if the matrix we are working on is smaller than that, the matrices need to be padded. If the matrix is larger than that, we can still use WMMA intrinsics by decomposing the larger matrix into GEMM operations of 16x16 matrices.
```

## Excerpt: paragraph 8 (intrinsic name)

```text
__builtin_amdgcn_wmma_<C, D format>_16x16x16_<A, B format>_w32_gfx12
```

## Excerpt: paragraph 10 (sentences 1, 2 and 4; sentence 3 holds a formula and is not copied)

```text
In the AMD RDNA 3 architecture, we needed to duplicate some elements for A and B, but it is removed for RDNA 4, which makes the layout simpler in VGPRs. Each lane only needs to load (or store) 8 elements of a matrix.
One thing to note is that B, C, and D matrices are row major while A is transposed thus column major as shown in the figure above.
```

## Excerpt: paragraph 14 (Transitioning from AMD RDNA 3 WMMA to RDNA 4 WMMA)

```text
As briefly mentioned above, the VGPR format for WMMA has been changed since the AMD RDNA 3 architecture. The VGPR format of RDNA 4 is much simpler than the one of RDNA 3 which is illustrated below. We can see that C and D matrices are split into even and odd for lower 16 lanes and upper 16 lanes. Therefore, in order to convert D matrix to B matrix to chain WMMA operations as we do for MLP we will explain shortly, data needs to be shuffled among lanes in RDNA 3. This is not needed for RDNA 4.
```
