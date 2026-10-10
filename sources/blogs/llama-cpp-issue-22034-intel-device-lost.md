---
id: blog-llama-cpp-issue-22034-intel-device-lost
title: 'llama.cpp issue 22034: Device Lost on Intel dGPU using Vulkan backend'
author: rillomas, mamama1, tbsecurity29, TomTheHand
url: https://github.com/ggml-org/llama.cpp/issues/22034
source_category: community-note
architectures:
- arc-b580
- arc-pro-b70
- xe2
tags:
- cooperative-matrix
- driver-workaround
- moe
- gemm
retrieved_at: '2026-10-10'
description: 'GitHub issue thread (page type: source-blog, the closest existing type). Device loss with cooperative-matrix pipelines on Intel Windows drivers 32.0.101.8515 to .8737; reported fixed in 32.0.101.8860'
---

# llama.cpp issue 22034: Device Lost on Intel dGPU using Vulkan backend

GitHub issue thread, state `closed`, opened 2026-04-17, closed 2026-07-01. Each excerpt names the hardware, driver and build it belongs to.

## Excerpt: issue body by rillomas, 2026-04-17 (version, command, description, environment)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034

````text
### Name and Version

λ llama-cli.exe --version
version: 8827 (5e6c0e18b)
built with MSVC 19.50.35728.0 for x64

### Operating systems

Windows

### Which llama.cpp modules do you know to be affected?

Vulkan backend

### Command line

```shell
llama-bench.exe -m Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf -n 0 -b 32 -ub 32
```

### Problem description & steps to reproduce
I was trying to benchmark the smaller warptile pipelines (`*aligned_s` pipelines) when I found this. Reproduction is 100% when running llama-bench but may not occur on llama-cli and llama-completion.

1. [Download model](https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF/blob/main/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf)
2. Build with cmake option `-DGGML_VULKAN=ON -DLLAMA_CURL=OFF -DGGML_VULKAN_VALIDATE=ON`
3. Execute `llama-bench.exe -m Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf -n 0 -b 32 -ub 32` . `llama-bench.exe -m Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf -n 0` does **not** crash on the same environment
#### Environment
- i9-13900K + Arc B580, Graphics driver 32.0.101.8724, 32GB RAM 5600MT, Win 11 24H2 10.0.26100.8246
````

## Excerpt: issue body by rillomas, 2026-04-17 (device line of the log)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034

```text
ggml_vulkan: Found 1 Vulkan devices:
ggml_vulkan: 0 = Intel(R) Arc(TM) B580 Graphics (Intel Corporation) | uma: 0 | fp16: 1 | bf16: 0 | warp size: 32 | shared memory: 49152 | int dot: 1 | matrix cores: KHR_coopmat
```

## Excerpt: issue body by rillomas, 2026-04-17 (last lines of the log)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034

```text
Validation Warning: [ BestPractices-Error-Result ] | MessageID = 0x53c1342f
vkGetFenceStatus(): Returned error VK_ERROR_DEVICE_LOST.
```

## Excerpt: comment by mamama1, 2026-04-19 (Arc Pro B70 setup)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4276735065

```text
Setup:

GPU: Intel Arc Pro B70 (32 GB)
OS: Windows Server 2022
Driver version: 32.0.101.8515
llama.cpp build: b8850-4eac5b450 (self-built)
Model: Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf (Q4_K_M, MoE architecture, 30B/3B active)
Vulkan SDK version: 1.4.341.1
```

## Excerpt: comment by mamama1, 2026-04-19 (regression window and workaround)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4276735065

````text
Key observation: Build b8555 (the version shipped with Intel AI Playground) does not exhibit this crash on identical hardware with the same model. The regression appears somewhere between b8555 and b8850.

cmake flags used for b8850 build:

> -DGGML_NATIVE=OFF -DGGML_VULKAN=ON -DLLAMA_BUILD_TESTS=OFF
> -DGGML_BACKEND_DL=ON -DGGML_CPU_ALL_VARIANTS=ON
> -DGGML_VULKAN_COOPMAT=OFF -DGGML_VULKAN_COOPMAT2=OFF

(coopmat explicitly disabled - crash persists regardless)

Startup log excerpt showing the crash context:

> sched_reserve: graph splits = 2
> llama_context: flash_attn    = enabled

[crash occurs mid-inference with no error output system just freezes completely]

Happy to provide additional logs or test specific builds/flags if it helps narrow down the regression.

edit:
apparently, this has fixed it:
```
set GGML_VK_DISABLE_COOPMAT=1
set GGML_VK_DISABLE_COOPMAT2=1
```

no more freezes...
````

## Excerpt: comment by rillomas, 2026-04-20

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4278517030

````text
Thanks for the info. Disabling coopmat with `set GGML_VK_DISABLE_COOPMAT=1` does actually work on my case as well, so probably an issue in the coopmat shader or the driver. I'll see if I can look deeper.

Update: So far I've confirmed that the crash happens when running the following two pipelines in MUL_MAT operator. The number of calls required for crashing is random (sometimes it doesn't crash) so possibly a race condition within these shaders?

```
matmul_q4_k_f32_f16acc_aligned_s
matmul_q6_k_f32_f16acc_aligned_s
```

Update2: Seems like device lost occurs on other pipelines as well, so likely a compiler/driver issue. Currently checking internally.
````

## Excerpt: comment by tbsecurity29, 2026-06-10 (environment)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4671090069

```text
Adding a data point from an Arc Pro B70 on a newer driver and build — this still reproduces, and I'm seeing it surface as a host-side STATUS_STACK_BUFFER_OVERRUN rather than "Device Lost," which may be the same coopmat bug manifesting through a second fault path.
Environment

Build: b9245 (b39a7bf1b), Clang 19.1.5, Windows x86_64
GPU: Intel Arc Pro B70 (Vulkan0, 32 GB); AMD Radeon iGPU at Vulkan1 (not targeted)
Driver: 32.0.101.8737 (2026-04-28), DRIVER_ID_INTEL_PROPRIETARY_WINDOWS — newer than the .8724 reported above, still broken
Vulkan: Instance 1.4.313, device 1.4.344; VK_KHR_cooperative_matrix rev 2, cooperativeMatrix=true, cooperativeMatrixRobustBufferAccess=true; no VK_NV_cooperative_matrix2 (so this is the KHR coopmat path)
```

## Excerpt: comment by tbsecurity29, 2026-06-10 (workaround and its cost)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4671090069

```text
Workaround confirmed: GGML_VK_DISABLE_COOPMAT=1 + GGML_VK_DISABLE_COOPMAT2=1 → same config ran 4/4 clean. (Cost on this card: ~12 tok/s vs ~17–22 with coopmat on.)
```

## Excerpt: comment by TomTheHand, 2026-06-11 (environment)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4677171817

```text
## Environment

| Item | Details |
|---|---|
| GPU | Intel Arc B60 (BMG-G21), 24 GB VRAM |
| Driver | 32.0.101.6870 (Intel Arc Control reports 1.13.684.081) |
| OS | Windows 11 24H2 (Build 22631) |
| llama.cpp | Official prebuilt release `b9196`, build `9592 (ac4cdde)` |
| Backend | Vulkan |
```

## Excerpt: comment by TomTheHand, 2026-06-11 (workaround)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4677171817

```text
## Workaround: `GGML_VK_DISABLE_COOPMAT=1`

Setting `GGML_VK_DISABLE_COOPMAT=1` **completely eliminates the crash** on both models, same official binary.
```

## Excerpt: comment by TomTheHand, 2026-06-11 (throughput with the workaround)

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4677171817

```text
### Performance (no-coopmat, IQ3_M)
- Completion throughput: **~66 tok/s** average
- Prompt processing: **~56 tok/s** average (varies with prompt length and concurrency)
- Usable and stable for sustained serving.
```

## Excerpt: comment by rillomas, 2026-07-01

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4849637738

```text
This is fixed with latest graphics driver [32.0.101.8860](https://www.intel.com/content/www/us/en/download/785597/intel-arc-graphics-windows.html)
```

## Excerpt: comment by TomTheHand, 2026-07-02

Locator: https://github.com/ggml-org/llama.cpp/issues/22034#issuecomment-4861683457

```text
For anyone wanting to run Arc Pro drivers (B60/B70/whatever), the slightly older, Arc Pro-targeted 32.0.101.8804 _also_ seems to have the issue resolved.
```

The thread is quoted with attribution to its authors and is not relicensed.
