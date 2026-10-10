---
id: doc-intel-oneapi-gpu-guide-joint-matrix
title: "Programming Intel XMX Using SYCL Joint Matrix Extension (oneAPI GPU Optimization Guide 2025.2)"
author: Intel Corporation
url: https://web.archive.org/web/20251008202018/https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/2025-2/programming-intel-xmx-using-sycl-joint-matrix.html
source_category: vendor-doc
architectures:
- intel
tags:
- cooperative-matrix
- int8-cooperative-matrix
- coopmat-shape
- coopmat-fp32-accumulator
- bfloat16-arithmetic
- mma-shape-selection
- workgroup-tile-sizing
- k-chunk-sizing
- subgroup-grid
- gemm
retrieved_at: '2026-10-10'
---

# Programming Intel XMX Using SYCL Joint Matrix Extension (oneAPI GPU Optimization Guide)

Locator: https://web.archive.org/web/20251008202018/https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/2025-2/programming-intel-xmx-using-sycl-joint-matrix.html (snapshot of 2025-10-08; original address https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/2025-2/programming-intel-xmx-using-sycl-joint-matrix.html; guide version 2025.2 in the address; page metadata `lastModifieddate` 2025-07-10)

Retrieved from the Internet Archive snapshot named in the locator, because intel.com answered a direct request with HTTP 403 on the retrieval date. Each excerpt is one element of the page, copied in full; the number is the element's position among the non-empty elements of that kind (`<p>`, `<li>`, `<pre>`, `<th>`/`<td>`) in the snapshot's HTML, counted from 1 over the whole document, site navigation included.

The guide is not redistributable; only the elements below are quoted.

## Excerpt: paragraph 8 (DPAS)

```text
In the code below, the kernel makes use of the joint matrix interface by declaring 3 joint_matrix matrices: tA, tB, tC and computes the operation tC += tA * tB. DPAS (Dot Product and Accumulate Systolic) is the name of the elementary operations done in Intel® XMX. For more examples that use joint_matrix, please refer to the Intel SYCL E2E tests repo.
```

## Excerpt: code block 3 (shape combinations per device family; lines 8 to 31 of the block)

```text
    if (combinations[i].nsize == 0) { // Intel AMX
      passed &=
          test<int8_t, int8_t, int32_t, 16, 16, 64, class amx_int_16x16x64>();
      passed &= test<bfloat16, bfloat16, float, 16, 16, 32,
                     class amx_bf16_16x16x32>();
      break;
    }

    if (combinations[i].nsize == 16) { // architecture::intel_gpu_pvc
      passed &=
          test<int8_t, int8_t, int32_t, 8, 16, 32, class pvc_int_8x16x32>();
      passed &=
          test<bfloat16, bfloat16, float, 8, 16, 16, class pvc_bf16_8x16x16>();
      break;
    }

    if (combinations[i].nsize == 8) { // architecture::intel_gpu_dg2*
      passed &= test<int8_t, int8_t, int32_t, 8, 8, 32, class dg2_int_8x8x32>();
      passed &=
          test<bfloat16, bfloat16, float, 8, 8, 16, class dg2_bf16_8x16x16>();
      break;
    }
  }
```

## Excerpt: paragraph 12 (Tuning Techniques for Performance)

```text
In order to get optimal performance on Intel® XMX, the GEMM kernel has to be written in a way that keeps feeding Intel® XMX with data it needs to perform the maximum multiply and adds operations/cycle. Some of these tuning techniques are the following:
```

## Excerpt: list item 117 (sub-group partitioning and register use)

```text
Sub-group partitioning: One sub-group can perform multiple DPAS operations. The different combinations that are supported are documented in Combinations and Restrictions on Intel GPUs. In order to optimally utilize the registers available to the matrix engine, a combination of 32x64x16 should be used. This can be achieved via either issuing 16 joint_matrix_mad operations by one sub-group that reuse 4 A matrices, 4 B matrices, and 16 C matrices or directly use joint_matrix shape combination of 32x64x16.
```

## Excerpt: list item 118 (work-group partitioning and blocking)

```text
Work group partitioning: The loop blocking for cache locality should be made on the three`` i``,``j``, and k dimensions. Blocking on the first two dimensions is included in the global range of the kernel. The k-level cache blocking is done within the kernel body. e.g. by choosing block factors of 256x256x32, global range results in: range<2> global{M / 256, N / 256 * SG_SIZE};
```

## Excerpt: paragraph 13 (sub-group shape)

```text
Then, by choosing one sub - group to perform 32x64x32 elements, local range results in:
```

## Excerpt: code block 4 (local range)

```text
range<2> local{256 / 64, 256 / 32 * SG_SIZE};
```

## Excerpt: list item 119 (large register file)

```text
Large register file per thread gives the best results for the GEMM kernel. This can be explicitly specified in the compilation command as follows: icpx -fsycl -fsycl-targets=spir64_gen -Xsycl-target-backend "-device pvc -options -ze-opt-large-register-file" joint-matrix.cpp
```

## Excerpt: list item 120 (prefetch)

```text
Prefetch: the usage of the API joint_matrix_prefetch delivers about 30 of additional performance on PVC hardware. An example of usage can be found in Matrix/joint_matrix_bf16_fill_k_cache_prefetch.cpp.
```

## Excerpt: paragraph 14 (Pre and Post Processing)

```text
Using joint_matrix_apply generates efficient vectorized code on the GPU with no extra trips to the memory as the data used for the GEMM reside in the same GPU registers used for the element-wise operation:
```

Conditions the page states for the figure in list item 120: hardware "PVC hardware"; unit of the figure "30": not stated; compiler or driver version: not stated; measurement date: not stated.
