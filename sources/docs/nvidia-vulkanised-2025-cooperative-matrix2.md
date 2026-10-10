---
id: doc-nvidia-vulkanised-2025-cooperative-matrix2
title: "Machine Learning in Vulkan with Cooperative Matrix 2 (Vulkanised 2025 slides)"
author: Jeff Bolz, NVIDIA
url: https://vulkan.org/user/pages/09.events/vulkanised-2025/T47-Jeff-Bolz-NVIDIA.pdf
source_category: official-doc
architectures:
- nvidia
- rtx-4070
tags:
- cooperative-matrix
- cooperative-matrix2
- coopmat-shape
- coopmat-fp32-accumulator
- int8-cooperative-matrix
- shared-memory-limit
- workgroup-tile-sizing
- k-chunk-sizing
- double-buffering
- gemm
- moe
- sdpa
- dequantize
- prefill
- decode
retrieved_at: '2026-10-10'
---

# Machine Learning in Vulkan with Cooperative Matrix 2

Locator: https://vulkan.org/user/pages/09.events/vulkanised-2025/T47-Jeff-Bolz-NVIDIA.pdf (slide deck, 28 slides; title slide: "The 7th Vulkan Developer Conference, Cambridge, UK | February 11-13, 2025", "Jeff Bolz, NVIDIA"; PDF metadata: Author "Jeff Bolz", CreationDate 2025-02-15)

Each excerpt is a run of consecutive text lines of one slide as `pdftotext` extracts them in reading order (blank lines removed, a wrapped bullet stays on two lines); the slide number is the PDF page number, which equals the number printed on the slide. Code listings and diagrams on the slides are not copied. A trailing pictograph after a throughput figure is omitted.

The deck is not redistributable; only the lines below are quoted.

## Excerpt: slide 4 (Terminology)

```text
• “Cooperative Matrix” – a new matrix type where the storage for and computations performed on the matrix are spread
across a set of invocations such as a subgroup (KHR_coopmat) or workgroup (NV_coopmat2)
• KHR_cooperative_matrix (coopmat1): released summer 2023, widely supported today
• NV_cooperative_matrix2: released October 2024, currently NVIDIA-only
• “D = A*B+C”
• Matrix types are templated by component type, scope, dimensions, “Use” (A/B/Accumulator)
• E.g. coopmat<float16_t, gl_ScopeSubgroup, M, K, gl_MatrixUseA> matA;
• “MxNxK” matrix multiply
```

## Excerpt: slide 4 (Terminology, sizes)

```text
• A = MxK, B = KxN, C,D=MxN (rows x columns)
• Supported sizes queried from Vulkan extension
```

## Excerpt: slide 4 (Terminology, precision)

```text
• Precision
• A=B=fp16, C=D={fp16 or fp32} (precision of C and D must match)
• A=B=(s/u)int8, C=D=(s/u)int32
• Hopefully more in the future
```

## Excerpt: slide 5 (Simple Cooperative Multiply, text and local matrix size)

```text
Simple Cooperative Multiply
• Straightforward application of coopmat1 types and
functions - sum(AikBkj) to accumulate one result tile
• Memory bandwidth-limited, not designed to get
good reuse of memory
• Tiles are too small!
lM = 16; lN = 8; lK = 16;
```

## Excerpt: slide 5 (Simple Cooperative Multiply, throughput)

```text
~8 TFLOPS (RTX 4070)
(RTX 4070 peak tensor core FP16 rate is around 116 TFLOPS)
```

## Excerpt: slide 6 (Optimized Coopmat1 Multiply, goal)

```text
• Goal is to maximize the result tile size, which
minimizes how many times A/B are loaded
```

## Excerpt: slide 6 (Optimized Coopmat1 Multiply, tiling example)

```text
• Subgroups cooperate to copy slivers of A/B from
global to shared, then load out of shared
• Example (FP16): 8 subgroups split a 256x256 tile into
8 128x64 tiles (K=32)
• Cooperate to copy A block (256x32) and B block
(32x256) into shared memory
• Then each subgroup loads the portions it needs
from shared memory
```

## Excerpt: slide 6 (Optimized Coopmat1 Multiply, source and sizes)

```text
Full source code available at
https://github.com/jeffbolznv/vk_cooperative_matrix_perf
• Optimal sizes depend on HW
```

## Excerpt: slide 6 (Optimized Coopmat1 Multiply, throughput; line 42 is a diagram label)

```text
~98 TFLOPS (RTX 4070)
Acc
(RTX 4070 peak tensor core FP16 rate is around 116 TFLOPS)
```

## Excerpt: slide 7 (Problems with Coopmat1)

```text
• GEMM wants large matrices split across a workgroup
• Decomposing larger sizes into implementation-dependent tiles is
something a compiler should do
• Manually staging through shared memory is clunky
• Get bogged down in addressing math
• Issues with type punning (want 16B loads, but elements are only 2B)
```

## Excerpt: slide 7 (Problems with Coopmat1, bounds checking)

```text
• Tensor isn’t always a multiple of the HW matrix size
• Need bounds-checking on loads/stores
• Storing a matrix with bounds checking is surprisingly difficult
• No knowledge of (row,col) information, so you have to go through
shared memory
• The whole matrix may not fit in shared memory! Go one warp at a time?
• Workarounds on top of workarounds when you just want to say “store”
```

## Excerpt: slide 9 (Cooperative Matrix 2, local matrix size)

```text
lM = 256; lN = 256; lK = 32;
```

## Excerpt: slide 9 (Cooperative Matrix 2, throughput)

```text
~97 TFLOPS (RTX 4070)
(RTX 4070 peak tensor core FP16 rate is around 116 TFLOPS)
```

Conditions the deck states for the throughput figures on slides 5, 6 and 9: device "RTX 4070" (same line as each figure); operand precision FP16 (slides 5, 6, 9); matrix dimensions of the multiply (M, N, K): not stated; driver version: not stated; operating system: not stated; measurement date: not stated (the conference took place 2025-02-11 to 2025-02-13).

## Excerpt: slide 15 (llama.cpp/ggml, use cases)

```text
• Key use cases to accelerate:
• Matrix-matrix multiply
• Mixture-of-Experts mat-mat mul
• Flash Attention
• Quantization Formats
```

## Excerpt: slide 15 (llama.cpp/ggml, matrix paths and flash attention)

```text
• Where we are today:
• Vulkan backend works “everywhere” (needs basic vk1.2 support)
• Mat-mat mul has scalar, KHR_coopmat, NV_coopmat2 paths
• Flash Attention has an NV_coopmat2 path
• Quantization Formats supported in all paths
```

## Excerpt: slide 18 (Dequantization Callback)

```text
• Implementation computes block coordinate, coordinate in block, and pointer to start of the block
• Passes these to shader-supplied callback function -> return value populates the matrix
• This works well with compiler-implemented staging through shared memory
• Generic, composable way to support dequantization
• Mat-mul and FlashAttention kernels just plug in a different callback function for each format
• Consider decoding two or in some cases four elements at a time, for performance
```

## Excerpt: slide 20 (Flash Attention 2, required coopmat2 features)

```text
• Needs the following coopmat2 features:
• Row reductions (for softmax)
• Matrix Use conversions (convert QK^t from Accumulator to A matrix)
• Per-element operations (to clear padding elements)
```

## Excerpt: slide 22 (Cooperative Matrix 2, Seven New Features)

```text
• (And performance heavily relies on workgroup scope, flexible dimensions, and tensor addressing)
```

## Excerpt: slide 27 (Conclusion, availability)

```text
• The Vulkan/SPIR-V/GLSL NV_coopmat2 extensions are available now
• In the Vulkan 1.4.304 SDK
• Supported in developer drivers at https://developer.nvidia.com/vulkan-driver
• Will be in next major release (R575)
• Supported on all NVIDIA RTX GPUs
```

## Slides 23 to 26 (Performance charts)

The four slides are bar charts embedded as images; `pdftotext` returns only the heading "Performance" and the slide number. The text below is transcribed from the rendered slide images. The bars carry no numeric labels, so no value is recorded here.

```text
slide 23 chart title: RTX 4070 - Prompt Processing - 512 Tokens
slide 24 chart title: RTX 4070 - Token Generation - 128 Tokens
slide 25 chart title: RTX 6000 Ada - Prompt Processing - 512 Tokens
slide 26 chart title: RTX 6000 Ada - Token Generation - 128 Tokens
vertical axis (all four): Tokens/s
horizontal axis (all four): Model
legend (all four): Vulkan(none), Vulkan(KHR_coopmat), Vulkan(NV_coopmat2), CUDA
```

Conditions the deck states for slides 23 to 26: device in each chart title; model names on the horizontal axis; llama.cpp version or commit: not stated; driver version: not stated; measurement date: not stated.
