---
id: doc-intel-oneapi-gpu-guide-xmx
title: "Boost Matrix Multiplication Performance with Intel Xe Matrix Extensions (oneAPI GPU Optimization Guide 2025.2)"
author: Intel Corporation
url: https://web.archive.org/web/20250930094857/https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/2025-2/boost-matrix-multiplication-performance-with-intel.html
source_category: official-doc
architectures:
- intel
tags:
- cooperative-matrix
- bfloat16-arithmetic
- fp16-arithmetic
- gemm
retrieved_at: '2026-10-10'
---

# Boost Matrix Multiplication Performance with Intel Xe Matrix Extensions (oneAPI GPU Optimization Guide)

Locator: https://web.archive.org/web/20250930094857/https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/2025-2/boost-matrix-multiplication-performance-with-intel.html (snapshot of 2025-09-30; original address https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/2025-2/boost-matrix-multiplication-performance-with-intel.html; guide version 2025.2 in the address; page metadata `lastModifieddate` 2025-07-10)

Retrieved from the Internet Archive snapshot named in the locator, because intel.com answered a direct request with HTTP 403 on the retrieval date. Each excerpt is one element of the page, copied in full; the number is the element's position among the non-empty elements of that kind (`<p>`, `<li>`, `<pre>`, `<th>`/`<td>`) in the snapshot's HTML, counted from 1 over the whole document, site navigation included.

The guide is not redistributable; only the elements below are quoted.

## Excerpt: paragraph 7 (Intel Xe Matrix Extensions)

```text
Intel® Xe Matrix Extensions (Intel® XMX) specializes in executing Dot Product Accumulate Systolic (DPAS) instructions on 2D systolic arrays. A systolic array in parallel computer architecture is a homogeneous network of tightly coupled data processing units. Each unit computes a partial result as a function of data received from its upstream neighbors, stores the result within itself and passes it downstream. Intel® XMX supports numerous data types, depending on hardware generation, such as int8, fp16, bf16, and tf32. To understand Intel® XMX inside Intel® Data Center GPU Max Series, please refer to Intel® Intel® Iris® Xe GPU Architecture section.
```

## Excerpt: paragraph 14 (oneMKL algorithms)

```text
oneMKL supports several algorithms for accelerating single-precision gemm and gemm_batch using Intel® XMX. The bf16x2 and bf16x3 are 2 such algorithms using bf16 to approximate single-precision gemm.
```

## Excerpt: paragraph 15 (bf16 variants)

```text
Internally single-precision input data is converted into bf16 and multiplied with the systolic array. The three variants – bf16, bf16x2, and bf16x3 – allow you to make a tradeoff between accuracy and performance, with bf16 being the fastest and bf16x3 the most accurate (similar to the accuracy of standard single-precision gemm). The example Matrix Multiplication shows how to use these algorithms and the table below compares the performance difference.
```

## Excerpt: table header cells 1-4 and table cells 1-16 (one table row per line, cells separated by ` | `)

```text
Precision | Data type/ Algorithm | Peak (TF) | Performance relative totheoretical peak ofsingle precision(%)
Single | fp32 | 26 | 98
Single | bf16 | 151 | 577
Single | bf16x2 | 74 | 280
Single | bf16x3 | 42 | 161
```

## Excerpt: paragraph 16 (test system)

```text
The test is performed on a Intel® Xeon® 8480+ with512 GB DDR5-4800 + Intel® Data Center GPU Max 1550 running Ubuntu 22.04.
```

Conditions the page states for the table: system in paragraph 16 (host processor, memory, "Intel® Data Center GPU Max 1550", "Ubuntu 22.04"); matrix dimensions: not stated; oneMKL, compiler or driver version: not stated; measurement date: not stated.
