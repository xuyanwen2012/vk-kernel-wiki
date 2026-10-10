---
id: blog-mlc-amd-gpus-llm-inference
title: Making AMD GPUs competitive for LLM inference (MLC-LLM / Apache TVM, generated kernels, not GLSL)
author: MLC Community
url: https://blog.mlc.ai/2023/08/09/Making-AMD-GPUs-competitive-for-LLM-inference
source_category: benchmark-blog
architectures:
- amd
tags:
- kernel-fusion
- device-specific-tuning
retrieved_at: '2026-10-10'
description: 'Language / backend: MLC-LLM on Apache TVM Unity; kernels generated from TensorIR for ROCm and Vulkan. The post''s benchmark figures are in images and are not quoted'
---

# Making AMD GPUs competitive for LLM inference (MLC-LLM / Apache TVM, generated kernels, not GLSL)

Locator: https://blog.mlc.ai/2023/08/09/Making-AMD-GPUs-competitive-for-LLM-inference (post dated Aug 9, 2023)

Language and backend of the source: MLC-LLM on Apache TVM Unity, generating kernels from TensorIR for ROCm and Vulkan; not GLSL. Each excerpt is one paragraph or list of the post, copied in full with whitespace collapsed; the number is the paragraph's position among the post's non-empty `<p>` elements. The benchmark charts of the post are images and are not transcribed.

## Excerpt: paragraph 2 (TL;DR)

Locator: https://blog.mlc.ai/2023/08/09/Making-AMD-GPUs-competitive-for-LLM-inference

```text
MLC-LLM makes it possible to compile LLMs and deploy them on AMD GPUs using ROCm with competitive performance. More specifically, AMD Radeon™ RX 7900 XTX gives 80% of the speed of NVIDIA® GeForce RTX™ 4090 and 94% of the speed of NVIDIA® GeForce RTX™ 3090Ti for Llama2-7B/13B. Besides ROCm, our Vulkan support allows us to generalize LLM deployment to other AMD devices, for example, a SteamDeck with an AMD APU.
```

## Excerpt: paragraph 9 (MLC for AMD GPUs and APUs)

Locator: https://blog.mlc.ai/2023/08/09/Making-AMD-GPUs-competitive-for-LLM-inference

```text
MLC for AMD GPUs and APUs. There are several possible ways to support AMD GPU: ROCm, OpenCL, Vulkan, and WebGPU. ROCm stack is what AMD recently push for and has a lot of the corresponding building blocks similar to the CUDA stack. Vulkan is the latest graphics standard and offers the widest range of support across GPU devices. WebGPU is the latest web standard that allows the computation to run on web browsers. While there are so many possible ways, few ML software solutions that build for solutions other than CUDA, largely due to the engineering cost to replicate a stack for a new hardware or GPU programming model. We support automatic code generation without having to recraft GPU kernels for each and bring support to all these ways. This being said, the performance still depends on how good the low-level GPU runtimes are and their availability in each platform. We pick ROCm for Radeon 7900 XTX and Vulkan for Steamdeck’s APU. We find that ROCm stack works out of the box. Thanks to the productive Python-based development pipeline in TVM unity, we spent a few more hours to further bring an optimized version. We made the following things to bring ROCm support:
```

## Excerpt: list after paragraph 9

Locator: https://blog.mlc.ai/2023/08/09/Making-AMD-GPUs-competitive-for-LLM-inference

```text
Reuse the whole MLC pipeline for existing targets (such as CUDA and Metal), including memory planning, operator fusion, etc.
Reuse a generic GPU kernel optimization space written in TVM TensorIR and re-target it to AMD GPUs.
Reuse TVM’s ROCm code generation flow that generates low-level ROCm kernels through LLVM.
Finally, export generated code as a shared or static library that can be invoked by CLI, Python and REST APIs.
```

## Excerpt: paragraph 10 (benchmark setup)

Locator: https://blog.mlc.ai/2023/08/09/Making-AMD-GPUs-competitive-for-LLM-inference

```text
We benchmarked the Llama 2 7B and 13B with 4-bit quantization. And we measure the decoding performance by setting a single prompt token and generating 512 tokens. All the results are measured for single batch inference.
```

## Excerpt: paragraph 15 (SteamDeck using Vulkan with unified memory)

Locator: https://blog.mlc.ai/2023/08/09/Making-AMD-GPUs-competitive-for-LLM-inference

```text
Let us also look into a broader set of AMD devices, more specifically, SteamDeck equipped with an AMD APU. While the GPU VRAM available in ROCm is capped to 4GB in BIOS, the Mesa Vulkan driver has robust support that allows the buffer to go beyond the cap using unified memory up to 16GB, which is sufficient to run 4bit-quantized Llama-7B.
```

The post is quoted paragraph by paragraph with attribution and is not relicensed.
