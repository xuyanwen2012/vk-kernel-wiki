---
id: doc-mnn-release-3-6-0
title: 'MNN 3.6.0 release notes: Vulkan backend entries'
author: MNN contributors (Alibaba)
url: https://github.com/alibaba/MNN/releases/tag/3.6.0
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- convolution
- gemv
- gated-delta-net
retrieved_at: '2026-10-10'
description: 'Release notes of alibaba/MNN 3.6.0, published 2026-06-16, tag commit cc20f672af9e177e2fa338c332dc097de2fc9264'
---

# MNN 3.6.0 release notes: Vulkan backend entries

Published: 2026-06-16. Lines are numbered within the release description as returned by the GitHub API (`repos/alibaba/MNN/releases/tags/3.6.0`, field `body`); the English half of the description is quoted.

## Excerpt: release description, line 206

Locator: https://github.com/alibaba/MNN/releases/tag/3.6.0 (release description, line 206)

```text
*   **Deep Multi-Backend GPU Optimization**: Vulkan adds VulkanConv1x1CoopA8 (W8A8 coopMat) and no-subgroup fallback paths; OpenCL adds heuristic GEMM/GEMV scheduling, int4 image1d_buffer_t optimization, native TopKV2 and 2/3-bit weight quantization; Metal optimizes Conv1x1 branch selection; CUDA supports Blackwell (sm_120) and optimizes Eagle speculative decoding; QNN supports Qwen3.5 and multi-process parallel offline graph export.
```

## Excerpt: release description, line 216

Locator: https://github.com/alibaba/MNN/releases/tag/3.6.0 (release description, line 216)

```text
*   **Full-Stack 2/3-bit Weight Quantization**: 2/3-bit weight quantization across CPU (low-bit ARM kernels) and GPU (OpenCL/Metal/Vulkan)
```

## Excerpt: release description, line 217

Locator: https://github.com/alibaba/MNN/releases/tag/3.6.0 (release description, line 217)

```text
*   **Vulkan W8A8 coopMat**: New VulkanConv1x1CoopA8 with dynamic-quant W8A8 + Cooperative Matrix
```

## Excerpt: release description, line 238

Locator: https://github.com/alibaba/MNN/releases/tag/3.6.0 (release description, line 238)

```text
*   **Vulkan VulkanConv1x1CoopA8**: Dynamic-quant W8A8 + Cooperative Matrix conv
```

## Excerpt: release description, line 239

Locator: https://github.com/alibaba/MNN/releases/tag/3.6.0 (release description, line 239)

```text
*   **Vulkan LinearAttention no-subgroup fallback**
```

## Excerpt: release description, line 240

Locator: https://github.com/alibaba/MNN/releases/tag/3.6.0 (release description, line 240)

```text
*   **Vulkan gemv decode no-subgroup fallback**
```

## Excerpt: release description, line 247

Locator: https://github.com/alibaba/MNN/releases/tag/3.6.0 (release description, line 247)

```text
*   **OpenCL/Metal/Vulkan 2/3-bit Weight Quantization**: Unified across GPU backends (CPU supported via low-bit ARM quant kernels)
```

## Excerpt: release description, line 299

Locator: https://github.com/alibaba/MNN/releases/tag/3.6.0 (release description, line 299)

```text
*   **Vulkan attention and other op fixes**
```
