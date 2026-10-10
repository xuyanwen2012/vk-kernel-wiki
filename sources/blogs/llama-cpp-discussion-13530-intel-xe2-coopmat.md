---
id: blog-llama-cpp-discussion-13530-intel-xe2-coopmat
title: 'llama.cpp discussion 13530: Vulkan VK_KHR_cooperative_matrix performance of Intel Xe2 arch GPUs (B580 & LNL)'
author: asto18089, 0cc4m, rillomas
url: https://github.com/ggml-org/llama.cpp/discussions/13530
source_category: benchmark-blog
architectures:
- arc-b580
- arc-a770
- xe2
tags:
- cooperative-matrix
- subgroup-size
- device-specific-tuning
retrieved_at: '2026-10-10'
description: 'GitHub discussion thread (page type: source-blog, the closest existing type). Third-party llama-bench figures on Windows, graphics driver 32.0.101.6795, llama.cpp build b5200'
---

# llama.cpp discussion 13530: Vulkan VK_KHR_cooperative_matrix performance of Intel Xe2 arch GPUs (B580 & LNL)

GitHub discussion thread, quoted comment by comment. Hardware, driver and build of every figure are stated in the quoted comment itself: Windows, graphics driver 32.0.101.6795, llama.cpp b5200, model gemma-2-2b-it-Q4_K_M.

## Excerpt: opening post by asto18089, 2025-05-14

Locator: https://github.com/ggml-org/llama.cpp/discussions/13530

```text
According to this issue: https://github.com/ggml-org/llama.cpp/issues/12690
and this commit: https://github.com/ggml-org/llama.cpp/commit/b56f079e28fda692f11a8b59200ceb815b05d419

It looks like Intel GPUs do support using matrix cores in Vulkan inference, but it got disabled since actual performance is worse and not easily sorted out why.
However, that assumption is made using A-series cards but not latest B-series Xe2 cards. After a rough search, I also cannot find anyone done such experiments. Are there any performance numbers out there? Or are anyone willing to give it a try?
```

## Excerpt: comment by 0cc4m, 2025-05-14

Locator: https://github.com/ggml-org/llama.cpp/discussions/13530#discussioncomment-13142515

```text
I only have an A770 so that's what I'm limited to for tests, but if someone has a B580 (or other Battlemage card) and wants to give it a shot, I can give instructions. They would have to build the project manually with slight code changes.
```

## Excerpt: comment by rillomas, 2025-05-28 (benchmark results)

Locator: https://github.com/ggml-org/llama.cpp/discussions/13530#discussioncomment-13290732

```text
Hi @0cc4m. The performance regression issue you mentioned in #12690 with Arc A770 is acknowledged but we don't have an ETA for the fix yet. In the meantime, we were wondering if there's a good way to enable coopmat for other Arc GPUs, especially Xe2 (LunarLake, Battlemage). Following are benchmark results I've performed on b5200. There's a significant performance boost for Xe2 GPUs so would be great if we can target specific GPUs and enable it.

I've only tested on Windows with llama-bench using gemma2 but what other testing is required for a PR?

## Benchmark results
- `llama-bench.exe -m gemma-2-2b-it-Q4_K_M.gguf -pg 1788,100 -t <Number of P cores>`
- Tested on Windows with Graphics driver 32.0.101.6795

Platform | Benchmark | b5200-vulkan-x64-intel-coopmat-enabled   t/s | b5200-vulkan-x64 t/s | Difference
-- | -- | -- | -- | --
i9-12900K + Arc A770 | pp512 | 260.74 | 961.3 | 27%
  | tg128 | 96.62 | 93.95 | 103%
  | pg1788+tg100 | 231.77 | 614 | 38%
U9-288V | pp512 | 398.49 | 154.09 | 259%
  | tg128 | 37.45 | 37.12 | 101%
  | pg1788+tg100 | 169.95 | 117.13 | 145%
U7-265H | pp512 | 296.60 | 274.34 | 108%
  | tg128 | 38.28 | 38.01 | 101%
  | pg1788+tg100 | 201.33 | 194.52 | 104%
U7-265K + Arc B580 | pp512 | 1607.09 | 488.50 | 329%
  | tg128 | 125.35 | 128.64 | 97%
  | pg1788+tg100 | 935.55 | 408.70 | 229%
```

## Excerpt: comment by rillomas, 2025-05-28 (source change used for the test)

Locator: https://github.com/ggml-org/llama.cpp/discussions/13530#discussioncomment-13290732

````text
### Source code diff for testing
```diff
diff --git a/ggml/src/ggml-vulkan/ggml-vulkan.cpp b/ggml/src/ggml-vulkan/ggml-vulkan.cpp 
index 131ee1ea..e2326a48 100644 
--- a/ggml/src/ggml-vulkan/ggml-vulkan.cpp 
+++ b/ggml/src/ggml-vulkan/ggml-vulkan.cpp 
@@ -8744,7 +8744,7 @@ static bool ggml_vk_khr_cooperative_matrix_support(const vk::PhysicalDevicePrope 
     switch (props.vendorID) { 
     case VK_VENDOR_ID_INTEL: 
         // Intel drivers don't support coopmat properly yet 
-        return false; 
+        return true; 
     case VK_VENDOR_ID_AMD: 
         if (driver_props.driverID == vk::DriverId::eAmdProprietary || driver_props.driverID == vk::DriverId::eAmdOpenSource) { 
             // Workaround for AMD proprietary driver reporting support on all GPUs 
```
````

## Excerpt: reply by 0cc4m, 2025-05-28

Locator: https://github.com/ggml-org/llama.cpp/discussions/13530#discussioncomment-13292986

```text
Yes, that is possible, but we need to figure out which devices benefit from it and which do not, and how to recognize them. For an example you can look at how it is handled for AMD below the code you quoted.
```

## Excerpt: reply by rillomas, 2025-05-28

Locator: https://github.com/ggml-org/llama.cpp/discussions/13530#discussioncomment-13293325

```text
Thanks. Intel GPUs that support cooperative_matrix are ones that have XMX, and since the first Arc series seem to have less impact in performance (or regresses) I was initially thinking of enabling for Xe2 GPUs: LunarLake and Battlemage. I still need to figure out the best way to distinguish Xe2 GPUs but it seems minSubgroupSize has changed from 8 to 16 in Xe2 so I'll probably use this.
I'll see if I can extend the vk_device_architecture and get_device_architecture() function for checking.
```

The thread is quoted with attribution to its authors and is not relicensed.
