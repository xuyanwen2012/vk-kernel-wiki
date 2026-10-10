---
id: blog-nvidia-vulkan-cooperative-matrices-2019
title: "Machine Learning Acceleration in Vulkan with Cooperative Matrices"
author: Neil Trevett
url: https://developer.nvidia.com/blog/machine-learning-acceleration-vulkan-cooperative-matrices/
source_category: benchmark-blog
architectures:
- nvidia
tags:
- cooperative-matrix
- coopmat-shape
- fp16-arithmetic
- gemm
retrieved_at: '2026-10-10'
---

# Machine Learning Acceleration in Vulkan with Cooperative Matrices

Locator: https://developer.nvidia.com/blog/machine-learning-acceleration-vulkan-cooperative-matrices/ (post dated 2019-04-16, by Neil Trevett)

Each excerpt is one paragraph of the post, copied in full; the number is the paragraph's position among the post's non-empty `<p>` elements.

## Excerpt: paragraph 14

```text
NVIDIA’s VK_NV_cooperative_matrix Vulkan vendor extension enables programmers to specify matrix operators of the form D = A*B+C in which the sizes of the matrices are MxNxK. (A = MxK, B = KxN, C&D=MxN); where M is the number of rows and N is the number of columns. Programmers select a precision of 16- or 32-bit floating point. We have found this to be a surprisingly clean and elegant programming model with good performance and usability for inferencing acceleration.
```

## Excerpt: paragraph 16

```text
The new matrix type defined by the Cooperative Matrix Vulkan extension spreads the required matrix storage and computations across a set of invocations, typically a subgroup, and all the invocations in the subgroup cooperate efficiently to compute the result. Vulkan shaders can then use and combine these efficient cooperative matrix operations into larger inferencing solutions. Additionally, if the GPU includes dedicated hardware for high-speed matrix operations, such as the Tensor Cores on Turing GPUs, then the Cooperative Matrix extension can tap into the power of this acceleration with no application changes.
```

## Excerpt: paragraph 20

```text
NVIDIA has created a benchmark application in addition to the specifications and drivers. You can find the source in the Cooperative Matrix Github repo. Using the Vulkan extension revealed significant speedups versus code using traditional Vulkan scalar math operations by seamlessly and efficiently harnessing the power of Turing Tensor Cores, as shown in figure 1.
```

## Excerpt: paragraph 21

```text
If the Cooperative Matrix Vulkan extension is interesting to you, you can try it out right now! It is shipping for Turing-based GPUs in NVIDIA driver versions 419.09 (Windows) and 418.31.03 (Linux) available here:https://developer.nvidia.com/vulkan-driver. Links to all the relevant specifications are here: https://github.com/KhronosGroup/Vulkan-Docs/issues/923. Please provide your feedback to us if you try it out.
```

## Figure 1 (image)

Locator: https://developer-blogs.nvidia.com/wp-content/uploads/2019/04/pasted-image-0-11-1024x550.png; caption in the post: "Figure 1. Comparing 16-bit TFLOP matrix multiplication throughput rates"

The figure is an image; the text below is transcribed from it (chart title, legend, then each category with the value printed above each bar).

```text
TFLOPS (fp16) Performance - Matrix Multiplies
legend: RTX 2070, RTX Titan
Typical code using tiled scalar math: 1.5 (RTX 2070), 3 (RTX Titan)
Theoretical peak using scalar math: 15 (RTX 2070), 32 (RTX Titan)
Measured Cooperative Matrix extension: 36 (RTX 2070), 71 (RTX Titan)
Theoretical peak tensor core performance: 60 (RTX 2070), 130 (RTX Titan)
```

Conditions the post states for Figure 1: devices "RTX 2070" and "RTX Titan" (figure legend); precision fp16 (figure title); extension `VK_NV_cooperative_matrix` (paragraph 14); matrix dimensions: not stated; driver version used for the measurement: not stated (paragraph 21 names the driver versions the extension ships in); measurement date: not stated (post dated 2019-04-16).
