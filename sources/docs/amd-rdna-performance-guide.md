---
id: doc-amd-rdna-performance-guide
title: "AMD RDNA Performance Guide: compute shaders (GPUOpen)"
author: AMD
url: https://gpuopen.com/learn/rdna-performance-guide/
source_category: vendor-doc
architectures:
- amd
tags:
- subgroup-size
- wave64
- shared-memory-limit
retrieved_at: '2026-10-10'
---

# AMD RDNA Performance Guide: compute shaders

Locator: https://gpuopen.com/learn/rdna-performance-guide/ (page metadata: published 2023-03-22; section "Compute shaders")

Each excerpt is one list item of the page, copied in full; the number is the item's position among the page's non-empty `<li>` elements, site navigation included.

The guide is not redistributable; only the items below are quoted.

## Excerpt: list item 132

```text
GCN and RDNA support cross-wave ops via AGS, shader model 6, or SPIR-V subgroup operations. Cross-wave operators are great for reduction problems such as prefix sums, downsampling, filtering, etc.
```

## Excerpt: list item 137

```text
GCN runs shader threads in groups of 64 known as wave64.
```

## Excerpt: list item 138

```text
RDNA runs shader threads in groups of 32 known as wave32.
```

## Excerpt: list item 139

```text
Unused threads in a wave get masked out when running the shader.
```

## Excerpt: list item 140

```text
Make the workgroup size a multiple of 64 to obtain best performance across all GPU generations.
```

## Excerpt: list item 143

```text
Thread group shared memory maps to LDS (Local Data Share) LDS memory is banked on RDNA and GCN.
```

## Excerpt: list item 144

```text
It’s spread across 32 banks.
```

## Excerpt: list item 145

```text
Each bank is 32 bits (1 DWORD).
```

The quoted items state no measured figure, no device and no driver version.
