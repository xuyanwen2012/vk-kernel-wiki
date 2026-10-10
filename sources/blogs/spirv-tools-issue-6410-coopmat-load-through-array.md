---
id: blog-spirv-tools-issue-6410-coopmat-load-through-array
title: 'SPIRV-Tools issue 6410: [spirv-val] OpCooperativeMatrixLoadKHR not checking if loading through an array'
author: spencer-lunarg, jeffbolznv
url: https://github.com/KhronosGroup/SPIRV-Tools/issues/6410
source_category: community-note
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- storage-buffer
- spirv
retrieved_at: '2026-10-10'
description: 'GitHub issue thread (page type: source-blog). What OpCooperativeMatrixLoadKHR may point at: the last access-chain element must be an array of scalars or vectors'
---

# SPIRV-Tools issue 6410: [spirv-val] OpCooperativeMatrixLoadKHR not checking if loading through an array

GitHub issue thread in `KhronosGroup/SPIRV-Tools`, state `open`, opened 2025-11-12.

## Excerpt: issue body by spencer-lunarg, 2025-11-12 (question)

Locator: https://github.com/KhronosGroup/SPIRV-Tools/issues/6410

````text
but found that if I remove the array, there is no validation error

@jeffbolznv so what is the exact restriction here? I notice a basic glslang shader will "loads through" the array as its in the middle of the access chain, but what was the real thing you are trying to avoid? something around variable pointer?

```
  %5 = OpTypeRuntimeArray %9
  %6 = OpTypeStruct %5
%15 = OpTypePointer StorageBuffer %6
  %4 = OpVariable %15 StorageBuffer

 %24 = OpAccessChain %19 %4 0 0
 %25 = OpCooperativeMatrixLoadKHR %13 %24 ...
```
````

## Excerpt: comment by jeffbolznv, 2025-11-12

Locator: https://github.com/KhronosGroup/SPIRV-Tools/issues/6410#issuecomment-3524265088

```text
The intent is to have the instruction load several values from within a single array, rather than having it do something weird like load across several values in the structure. Though I'm not sure I've fully understood what you're asking.
```

## Excerpt: comment by jeffbolznv, 2025-11-13

Locator: https://github.com/KhronosGroup/SPIRV-Tools/issues/6410#issuecomment-3525309126

```text
Yeah, for KHR_coopmat I think we meant "the last item of the access chain must be an array of scalar/vector" as you say. Be warned though that for NV_coopmat2 we intentionally allow the pointer to be into an array of any type.
```

## Excerpt: comment by spencer-lunarg, 2025-11-14

Locator: https://github.com/KhronosGroup/SPIRV-Tools/issues/6410#issuecomment-3534090595

````text
another one I found, if you generated code that looked like

```
layout(set=0, binding=0) coherent buffer SSBO { 
    uint8_t payload[128][128]; 
};
coopMatLoad(mat, payload, 0, 16, gl_CooperativeMatrixLayoutRowMajor);
```

and are you allowed to load through a double array?
````

## Excerpt: comment by jeffbolznv, 2025-11-14

Locator: https://github.com/KhronosGroup/SPIRV-Tools/issues/6410#issuecomment-3534342790

```text
Not 100% sure, but I think this would be invalid and if you have a 128x128 tensor you should use `payload[128*128]` (or better, `payload[]`)
```

The thread is quoted with attribution to its authors and is not relicensed.
