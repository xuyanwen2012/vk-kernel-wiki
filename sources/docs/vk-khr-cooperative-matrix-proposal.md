---
id: doc-vk-khr-cooperative-matrix-proposal
title: VK_KHR_cooperative_matrix proposal (Vulkan-Docs)
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/Vulkan-Docs/blob/e4e53e4b31e13eeaee1ad99fb940aa72b2ec1b14/proposals/VK_KHR_cooperative_matrix.adoc
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
retrieved_at: '2026-10-06'
---

# VK_KHR_cooperative_matrix proposal (Vulkan-Docs)

## Excerpt: proposals/VK_KHR_cooperative_matrix.adoc, lines 11-37 (introduction, Problem Statement, Solution Space)

Locator: https://github.com/KhronosGroup/Vulkan-Docs/blob/e4e53e4b31e13eeaee1ad99fb940aa72b2ec1b14/proposals/VK_KHR_cooperative_matrix.adoc#L11-L37

```text
This document proposes adding support for so-called cooperative matrix
operations that enables multiple shader invocations to cooperatively and
efficiently perform matrix multiplications.

== Problem Statement

A growing number of GPU applications are making use of matrix multiplication
operations. Modern GPU HW can take advantage of cross-invocation communication
channels or other hardware facilities to implement matrix multiplications
operations more efficiently but there is currently no suitable standard
SPIR-V/API mechanism to expose these features to applications or libraries.

== Solution Space

Applications or libraries can use subgroup primitives to write more efficient
matrix multiplication kernels but, while technically possible on some hardware,
this approach often does not make it possible to write optimal kernels and
requires applications to have a lot of device-specific knowledge.

NVIDIA exposed with VK_NV_cooperative_matrix a new set of abstractions for such
cooperative matrix operations. These include cooperative load and store
instructions, a matrix multiplication-addition instruction as well a limited
support for element-wise operations on these matrices. Since the release of
that extension, a growing body of evidence in the form of discussions and
other similar vendor extensions suggests that this approach is suitable for
a wide variety of devices and applications and is thus a good candidate for
standardization.
```

Licence of the excerpt: CC-BY-4.0, Copyright 2021-2026 The Khronos Group Inc. (file header, lines 1-3).
