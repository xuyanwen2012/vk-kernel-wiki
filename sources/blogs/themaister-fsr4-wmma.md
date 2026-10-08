---
id: blog-themaister-fsr4-wmma
title: Conquering FidelityFX FSR4 – Enabling the pretty pixels on Linux through maniacal persistence
author: themaister
url: https://themaister.net/blog/2025/05/09/conquering-fidelityfx-fsr4-enabling-the-pretty-pixels-on-linux-through-maniacal-persistence/
source_category: community-note
architectures:
- rdna3
tags:
- cooperative-matrix
- cooperative-matrix2
- fp16-arithmetic
- shared-memory-limit
retrieved_at: '2026-10-06'
---

# Conquering FidelityFX FSR4 – Enabling the pretty pixels on Linux through maniacal persistence

Locator: https://themaister.net/blog/2025/05/09/conquering-fidelityfx-fsr4-enabling-the-pretty-pixels-on-linux-through-maniacal-persistence/ (post dated 2025-05-09)

Each excerpt is one paragraph of the post, copied in full; the number is the paragraph's position among the post's non-empty `<p>` elements.

## Excerpt: paragraph 12

```text
At this point it was clear that FSR 4 is based on the WMMA (wave matrix multiply accumulate) instructions found on RDNA3 and 4 GPUs. This is encouraging since we have VK_KHR_cooperative_matrix in Vulkan which maps directly to WMMA. D3D12 was supposed to get this feature in SM 6.8, but it was dropped for some inexplicable reason. It’s unknown if FSR 4 could have used standard WMMA opcodes in DXIL if we went down that timeline. Certainly would have saved me a lot of pain and suffering …
```

## Excerpt: paragraph 26

```text
WMMA_Matrix WMMA_MatMulAcc(WaveMatrixOpcode op, 
 WMMA_Matrix A, WMMA_Matrix B, WMMA_Matrix C) 
{ 
 // A matrix 
 AGSMagic(WaveMatrixMulAcc, 0, 
   MatrixIO(0, 0, WaveMatrixRegType_A_TempReg), 
   A.v[0], A.v[1]); 
 AGSMagic(WaveMatrixMulAcc, 0, 
   MatrixIO(1, 0, WaveMatrixRegType_A_TempReg), 
   A.v[2], A.v[3]); 
 AGSMagic(WaveMatrixMulAcc, 0, 
   MatrixIO(0, 1, WaveMatrixRegType_A_TempReg), 
   A.v[4], A.v[5]); 
 AGSMagic(WaveMatrixMulAcc, 0, 
   MatrixIO(1, 1, WaveMatrixRegType_A_TempReg), 
   A.v[6], A.v[7]); 
```

## Excerpt: paragraph 32

```text
Ideally, there would be a straight forward implementation to KHR_cooperative_matrix, but that’s not really the case.
```

## Excerpt: paragraph 55

```text
RADV obviously cannot ship FP8 before there is a Vulkan / SPIR-V spec, but with the power of open source and courage, why not experiment. Nothing is stopping us from just emitting:
```

