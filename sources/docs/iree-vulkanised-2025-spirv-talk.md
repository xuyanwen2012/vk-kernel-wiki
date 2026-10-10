---
id: doc-iree-vulkanised-2025-spirv-talk
title: 'The Long Tail of AI: SPIR-V in IREE and MLIR (Vulkanised 2025 slides; MLIR compiler, not GLSL)'
author: Jakub Kuderski, AMD
url: https://www.vulkan.org/user/pages/09.events/vulkanised-2025/T12-Jakub-Kuderski-AMD-IREE-MLIR.pdf
source_category: vendor-doc
architectures:
- rdna3
tags:
- kernel-fusion
- cooperative-matrix
- device-specific-tuning
- workgroup-tile-sizing
- shared-memory-limit
retrieved_at: '2026-10-10'
description: 'Language / backend: IREE and MLIR generating SPIR-V; conference slides, quoted by slide number, not redistributed'
---

# The Long Tail of AI: SPIR-V in IREE and MLIR (Vulkanised 2025 slides; MLIR compiler, not GLSL)

Language and backend of the source: IREE and MLIR, generating SPIR-V; the kernels are compiler output, not GLSL. Slide deck of 31 slides presented at Vulkanised 2025 (Cambridge, UK, February 11-13, 2025). Each excerpt is the text of one slide as extracted with `pdftotext -layout`, blank lines and the slide-number footer removed; the slide number is the page of the PDF.

## Excerpt: slide 21 (Device Code Generation)

Locator: https://www.vulkan.org/user/pages/09.events/vulkanised-2025/T12-Jakub-Kuderski-AMD-IREE-MLIR.pdf (slide 21 of 31)

```text
Device Code Generation
We rely on structured op based code generation
    Tile + fuse         Multiple
                                          Tile
    + distribute     levels of tile
                                       reduction   Vectorize
      parallel         + fuse for
                                       dimension
    dimensions          caches
```

## Excerpt: slide 22 (Code Generation Strategy Selection)

Locator: https://www.vulkan.org/user/pages/09.events/vulkanised-2025/T12-Jakub-Kuderski-AMD-IREE-MLIR.pdf (slide 22 of 31)

```text
Code Generation Strategy Selection
●   Unlike traditional C compilers, multiple pass pipelines
●   Each codegen strategy is a (configurable) pass pipeline
     ○   SPIRVSubgroupReduce
     ○   SPIRVCooperativeMatrixVectorize
     ○   LLVMGPUTileAndFuse
     ○   LLVMGPUVectorDistribution
     ○   …
●   Selected strategies are embedded in the IR as attributes
     ○   Allows for ‘autotuning’
```

## Excerpt: slide 24 (Inter-dispatch Optimization)

Locator: https://www.vulkan.org/user/pages/09.events/vulkanised-2025/T12-Jakub-Kuderski-AMD-IREE-MLIR.pdf (slide 24 of 31)

```text
Inter-dispatch Optimization
Dispatch (kernel) formation decided by the compiler. Not a kernel generator.
●   Free to decide the dispatch data layout and ABI
     ○   We only need to preserve the input and output data format
●   Allows for arbitrary fusions
     ○   E.g., matmul and elementwise activation, two matmuls (horizontal fusion)
```

## Excerpt: slide 26 (Data Tiling and ukernels)

Locator: https://www.vulkan.org/user/pages/09.events/vulkanised-2025/T12-Jakub-Kuderski-AMD-IREE-MLIR.pdf (slide 26 of 31)

```text
Data Tiling and ukernels
Main idea:
 ●   Lay out data in a format most friendly to the target hardware
 ●   Perform simplified computation on this packed data
       ○   Offload the implementation to a handwritten innermost loop
 ●   Unpack the data back to the ‘global’ data format
 ●   Inline at the level of MLIR or LLVM IR
Difficulty:
 ●   Account for pack/unpack overhead
 ●   Decide the ukernel calling convention
      ○ E.g., required workgroup memory size
```

## Excerpt: slide 27 (Support for Handwritten SPIR-V Kernels)

Locator: https://www.vulkan.org/user/pages/09.events/vulkanised-2025/T12-Jakub-Kuderski-AMD-IREE-MLIR.pdf (slide 27 of 31)

```text
Support for Handwritten SPIR-V Kernels
glslang / DXC not the best for ML kernel development.
 ●   Recently added support for kernels compiled to SPIR-V in upstream MLIR
      ○ Source language: structured control flow, (n-dimensional) vectors, spir-v
      ○ Support for SPIR-V / Vulkan integration tests with mlir-runner
      ○ Useful for both MLIR (test coverage) and IREE (ukernels)
●    Direct GLSL to MLIR compiler: ShaderPulse
      ○   https://github.com/wpmed92/shaderpulse
```

## Excerpt: slide 28 (Results)

Locator: https://www.vulkan.org/user/pages/09.events/vulkanised-2025/T12-Jakub-Kuderski-AMD-IREE-MLIR.pdf (slide 28 of 31)

```text
Results
●   Vulkan / SPIR-V gives us very wide coverage of GPU targets
     ○   Specialized targets with known properties (usually key desktop cards)
     ○   Generic targets that cover ‘modern GPUs’ (recent desktop card, high-end phones)
     ○   Fallback target for everything else (e.g., emulate int64 with int32)
●   Support for popular Gen AI models like Llama3 and Stable Diffusion XL
     ○   Supported weight/parameter formats: npy, safetensors, GGUF, IRPA
     ○   Support for popular data types, e.g., fp16, fp8, int8, int4
●   Historical results (2024):
     ○   SOTA performance in Llama2 7B int4 via Vulkan on AMD RDNA3
     ○   SOTA performance in Stable Diffusion 2.1 via Vulkan on AMD RDNA3
     ○   SOTA performance in Stable Diffusion XL on AMD MI300X
     ○   ‘Competitive’ performance in microbenchmarks against kernel libraries
```

The slides are quoted for reference with attribution and are not relicensed; the deck itself is not stored in this repository.
