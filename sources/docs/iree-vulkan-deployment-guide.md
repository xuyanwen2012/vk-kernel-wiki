---
id: doc-iree-vulkan-deployment-guide
title: 'IREE (MLIR compiler emitting SPIR-V, not GLSL): GPU deployment using Vulkan'
author: The IREE Authors
url: https://iree.dev/guides/deployment-configurations/gpu-vulkan/
source_category: vendor-doc
architectures:
- amd
- arm
- nvidia
- qualcomm
tags:
- device-specific-tuning
retrieved_at: '2026-10-10'
description: 'Language / backend: MLIR compiler that generates SPIR-V directly; no GLSL source. Only the target-selection passages are quoted'
---

# IREE (MLIR compiler emitting SPIR-V, not GLSL): GPU deployment using Vulkan

Language and backend of the source: IREE, an MLIR-based compiler that emits SPIR-V for a Vulkan runtime; its kernels are generated, not GLSL. Source file of the published page: https://github.com/iree-org/iree/blob/3fd498c00d0dec30c179864178715753f536a599/docs/website/docs/guides/deployment-configurations/gpu-vulkan.md

## Excerpt: docs/website/docs/guides/deployment-configurations/gpu-vulkan.md, lines 20-30 (support matrix)

Locator: https://github.com/iree-org/iree/blob/3fd498c00d0dec30c179864178715753f536a599/docs/website/docs/guides/deployment-configurations/gpu-vulkan.md#L20-L30

```text
As IREE and the compiler ecosystem it operates within matures, more
target specific optimizations will be implemented. At this stage, expect
reasonable performance across all GPUs and for improvements to be
made over time for specific vendors and architectures.

GPU Vendor | Category | Performance | Focus Architecture
:--------: | :------: | :---------: | :----------------:
ARM Mali GPU | Mobile |  Good | Valhall+
Qualcomm Adreno GPU | Mobile | Reasonable | 640+
AMD GPU | Desktop/server | Good | RDNA+
NVIDIA GPU | Desktop/server | Reasonable | Turing+
```

## Excerpt: docs/website/docs/guides/deployment-configurations/gpu-vulkan.md, lines 34-38 (runtime baseline)

Locator: https://github.com/iree-org/iree/blob/3fd498c00d0dec30c179864178715753f536a599/docs/website/docs/guides/deployment-configurations/gpu-vulkan.md#L34-L38

```text
IREE's Vulkan HAL targets modern compute-capable Vulkan implementations. The
runtime baseline is Vulkan 1.3 with a compute queue and the
`timelineSemaphore`, `scalarBlockLayout`, and `synchronization2` device
features. Devices missing that baseline still appear in device dumps, but are
reported below the supported feature tier and are not selected for execution.
```

## Excerpt: docs/website/docs/guides/deployment-configurations/gpu-vulkan.md, lines 219-226 (target schemes)

Locator: https://github.com/iree-org/iree/blob/3fd498c00d0dec30c179864178715753f536a599/docs/website/docs/guides/deployment-configurations/gpu-vulkan.md#L219-L226

```text
The `--iree-vulkan-target` specifies the GPU architecture to target. It
accepts a few schemes:

* LLVM CodeGen backend style: this is using LLVM AMDGPU/NVPTX CodeGen targets
  like `gfx1100` for AMD RX 7900XTX and `sm_86` for NVIDIA RTX 3090 GPUs.
* Architecture code name style like `rdna3`/`valhall4`/`ampere`/`adreno`
  for AMD/ARM/NVIDIA/Qualcomm GPUs.
* Product name style: e.g., using `rx7900xtx`/`a100` for corresponding GPUs.
```

## Excerpt: docs/website/docs/guides/deployment-configurations/gpu-vulkan.md, lines 230-247 (target table)

Locator: https://github.com/iree-org/iree/blob/3fd498c00d0dec30c179864178715753f536a599/docs/website/docs/guides/deployment-configurations/gpu-vulkan.md#L230-L247

```text
| GPU                 | Product Name   | Target Architecture | Architecture Code Name |
| ------------------- | -------------- | ------------------- | ---------------------- |
| AMD RX 5000 series  |                |                     | `rdna1`                |
| AMD RX 6000 series  |                |                     | `rdna2`                |
| AMD RX 7700XT       | `rx7700xt`     | `gfx1101`           | `rdna3`                |
| AMD RX 7800XT       | `rx7800xt`     | `gfx1101`           | `rdna3`                |
| AMD RX 7900XT       | `rx7900xt`     | `gfx1100`           | `rdna3`                |
| AMD RX 7900XTX      | `rx7900xtx`    | `gfx1100`           | `rdna3`                |
| AMD RX 9060XT       | `rx9060xt`     | `gfx1200`           | `rdna4`                |
| AMD RX 9070         | `rx9070`       | `gfx1201`           | `rdna4`                |
| AMD RX 9070XT       | `rx9070xt`     | `gfx1201`           | `rdna4`                |
| ARM GPUs            |                |                     | `valhall`              |
| ARM Mali G510       | `mali-g510`    |                     | `valhall3`             |
| ARM Mali G715       | `mali-g715`    |                     | `valhall4`             |
| NVIDIA RTX20 series | `rtx2070super` | `sm_75`             | `turing`               |
| NVIDIA RTX30 series | `rtx3080ti`    | `sm_86`             | `ampere`               |
| NVIDIA RTX40 series | `rtx4090`      | `sm_89`             | `ada`                  |
| Qualcomm GPUs       |                |                     | `adreno`               |
```

## Excerpt: docs/website/docs/guides/deployment-configurations/gpu-vulkan.md, lines 249-259 (default target and limits of a target triple)

Locator: https://github.com/iree-org/iree/blob/3fd498c00d0dec30c179864178715753f536a599/docs/website/docs/guides/deployment-configurations/gpu-vulkan.md#L249-L259

```text
If no target is specified, then a safe but more limited default will be used.

!!! note

    We don't support the full spectrum of GPUs here and it is impossible to
    capture all details of a Vulkan implementation with a target triple, given
    the allowed variances on extensions, properties, limits, etc. So the target
    triple is just an approximation for usage. This is more of a mechanism to
    help us develop IREE itself. In the long term we want to perform
    multi-targeting to generate code for multiple architectures if no explicit
    target is given.
```

Licence of the excerpts: Apache-2.0 WITH LLVM-exception (`LICENSE` of the repository).
