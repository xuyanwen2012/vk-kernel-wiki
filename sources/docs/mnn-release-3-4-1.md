---
id: doc-mnn-release-3-4-1
title: 'MNN 3.4.1 release notes: Vulkan backend entries'
author: MNN contributors (Alibaba)
url: https://github.com/alibaba/MNN/releases/tag/3.4.1
source_category: vendor-doc
architectures: []
tags:
- cooperative-matrix
- convolution
- gated-delta-net
retrieved_at: '2026-10-10'
description: 'Release notes of alibaba/MNN 3.4.1, published 2026-03-05, tag commit 6b1db4c2eacf8193e6b7a1841acb6e31a1938e82'
---

# MNN 3.4.1 release notes: Vulkan backend entries

Published: 2026-03-05. Lines are numbered within the release description as returned by the GitHub API (`repos/alibaba/MNN/releases/tags/3.4.1`, field `body`); the English half of the description is quoted.

## Excerpt: release description, line 119

Locator: https://github.com/alibaba/MNN/releases/tag/3.4.1 (release description, line 119)

```text
*   **Qwen3.5 Support & Linear Attention**: Implements a new Linear Attention operator across CPU, Metal, OpenCL, and Vulkan backends to support the Qwen3.5 series hybrid attention architecture; llmexport adds corresponding model export capabilities.
```

## Excerpt: release description, line 128

Locator: https://github.com/alibaba/MNN/releases/tag/3.4.1 (release description, line 128)

```text
*   **Linear Attention Operator**: Implemented across all four backends (CPU/Metal/OpenCL/Vulkan) with Gated Delta Rule recurrent state updates
```

## Excerpt: release description, line 129

Locator: https://github.com/alibaba/MNN/releases/tag/3.4.1 (release description, line 129)

```text
*   **Vulkan CoopMat Conv1x1**: Cooperative matrix acceleration for Conv1x1 on Vulkan backend
```

## Excerpt: release description, line 146

Locator: https://github.com/alibaba/MNN/releases/tag/3.4.1 (release description, line 146)

```text
    *   Vulkan: Three GLSL compute shader implementation
```

## Excerpt: release description, line 151

Locator: https://github.com/alibaba/MNN/releases/tag/3.4.1 (release description, line 151)

```text
*   **Vulkan CoopMat Conv1x1**: New `VulkanConv1x1Coop` with C4/COOP data layout conversion and INT4/INT8 weight conversion shaders
```
