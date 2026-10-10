---
id: blog-spirv-tools-issue-6077-coopmat-bitwise-ops
title: 'SPIRV-Tools issue 6077: Missing handling for unary/binary opcodes with cooperative matrix'
author: HansKristian-Work, alan-baker
url: https://github.com/KhronosGroup/SPIRV-Tools/issues/6077
source_category: community-note
architectures: []
tags:
- cooperative-matrix
- spirv
retrieved_at: '2026-10-10'
description: 'GitHub issue thread (page type: source-blog). Bit instructions such as OpBitwiseAnd are not valid on cooperative matrices; only arithmetic instructions are'
---

# SPIRV-Tools issue 6077: Missing handling for unary/binary opcodes with cooperative matrix

GitHub issue thread in `KhronosGroup/SPIRV-Tools`, state `closed`, opened 2025-04-02, closed 2025-04-02.

## Excerpt: issue body by HansKristian-Work, 2025-04-02 (first lines)

Locator: https://github.com/KhronosGroup/SPIRV-Tools/issues/6077

````text
This shader fails validation:

```
; SPIR-V
; Version: 1.3
; Generator: Unknown(30017); 21022
; Bound: 70
; Schema: 0
               OpCapability Shader
               OpCapability Float16
               OpCapability Int16
               OpCapability Int8
               OpCapability DenormPreserve
               OpCapability CooperativeMatrixKHR
               OpExtension "SPV_KHR_cooperative_matrix"
               OpExtension "SPV_KHR_float_controls"
               OpMemoryModel Logical GLSL450
               OpEntryPoint GLCompute %main "main"
               OpExecutionMode %main LocalSize 32 1 1
````

## Excerpt: comment by HansKristian-Work, 2025-04-02

Locator: https://github.com/KhronosGroup/SPIRV-Tools/issues/6077#issuecomment-2772582187

```text
It's not 100% clear to me that BitwiseAnd should be banned, since I read

> Binary arithmetic instructions operate on the individual elements of a pair of cooperative matrices whose type must match.

which implied to me that all binary arithmetic instructions were valid.
```

## Excerpt: comment by alan-baker, 2025-04-02

Locator: https://github.com/KhronosGroup/SPIRV-Tools/issues/6077#issuecomment-2772903329

```text
The text you quoted is under modifications to Arithmetic instructions whereas `OpBitwiseAnd` is under Bit instructions in SPIR-V so I believe the validation is correct.

In order to do what you want you'd have to do it in a loop (bounded by `OpCooperativeMatrixLengthKHR`, loading and storing the elements.
```

The thread is quoted with attribution to its authors and is not relicensed.
