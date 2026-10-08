---
id: lang-glsl-cooperative-matrix
title: 'GLSL cooperative matrix (GL_KHR_cooperative_matrix): types, load/store and multiply-add as specified and as used upstream'
type: language
tags:
- glsl
- cooperative-matrix
- int8-cooperative-matrix
- cooperative-matrix2
- specialization-constants
architectures:
- rdna3
related:
- hw-cooperative-matrix-rdna3
sources:
- doc-glsl-khr-cooperative-matrix
- doc-vk-khr-cooperative-matrix-proposal
- doc-vk-nv-cooperative-matrix2-proposal
- doc-mesa-radv-envvars
- pr-llama-cpp-27952
- pr-llama-cpp-10206
reproducibility: snippet
---

# GLSL cooperative matrix (GL_KHR_cooperative_matrix)

This page collects what the extension specification states about the GLSL cooperative-matrix types and functions, and shows one upstream shader that uses them. Every statement is followed by its source page; the code is copied from a pinned upstream file. Nothing here is a measurement.

## What the extension defines

- The extension "adds a new set of types known as \"cooperative matrix\" types, where the storage for and computations performed on the matrix are spread across a set of invocations such as a subgroup" (`doc-glsl-khr-cooperative-matrix`, Overview, lines 34-37).
- It "does not specify rules about what sizes/combinations are valid. This is left to the Vulkan extension specifications", and "the dimensions of the cooperative types are parameterized and can be specialized via specialization constants" (`doc-glsl-khr-cooperative-matrix`, Overview, lines 39-44).
- The parameters of `coopmat` are "a scalar type for the component type, an integer value that controls the scope of the type, the number of rows and columns in the matrix, and which matrix accumulation argument the matrix can be" (`doc-glsl-khr-cooperative-matrix`, Overview, lines 46-51).
- The use parameter is one of `gl_MatrixUseA`, `gl_MatrixUseB`, `gl_MatrixUseAccumulator`; these "control which operand of coopMatMulAdd the type can be used as" (`doc-glsl-khr-cooperative-matrix`, lines 122-128).
- For load and store, "the \"buf\" arrays must be in either buffer storage or shared storage" (`doc-glsl-khr-cooperative-matrix`, lines 178-183).
- `coopMatMulAdd(A, B, C)` is described as "Linear-algebraic matrix multiply of A by B and then component-wise add C"; A, B and C "must have the same scope", and "the type of the result matches the type of C" (`doc-glsl-khr-cooperative-matrix`, lines 287-297).

## One upstream use: int8 operands, int32 accumulator

The file below was added by `pr-llama-cpp-27952`, whose description says the shader "is limited to those two architectures since it hardcodes their specific coopmat access patterns", the two being RDNA3 and RDNA4 (`pr-llama-cpp-27952`, excerpt, Overview).

Extensions the shader requires. Source: `artifacts/kernels/llama-cpp-matmul/mul_mmq_cm1.comp`, lines 3-10 (upstream `ggml/src/ggml-vulkan/vulkan-shaders/mul_mmq_cm1.comp` at commit `c479922ac520a08969b4c1dc154d7bbb3c386d85`).

```glsl
#extension GL_EXT_control_flow_attributes : enable
#extension GL_EXT_shader_16bit_storage : require
#extension GL_EXT_shader_explicit_arithmetic_types_int8 : require
#extension GL_EXT_shader_explicit_arithmetic_types_float16 : require

#extension GL_KHR_shader_subgroup_basic : require
#extension GL_KHR_cooperative_matrix : require
#extension GL_KHR_memory_scope_semantics : enable
```

Operand and accumulator declarations, the two loads and the multiply-add. A is loaded with the row-major layout constant and B with the column-major one; both operand matrices have `int8_t` components and the accumulator has `int32_t` components; all three use subgroup scope, and the dimensions are the names `TM`, `TN`, `TK`. Source: `artifacts/kernels/llama-cpp-matmul/mul_mmq_cm1.comp`, lines 330-331 (upstream `ggml/src/ggml-vulkan/vulkan-shaders/mul_mmq_cm1.comp` at commit `c479922ac520a08969b4c1dc154d7bbb3c386d85`) and `artifacts/kernels/llama-cpp-matmul/mul_mmq_cm1.comp`, lines 343-351 (upstream `ggml/src/ggml-vulkan/vulkan-shaders/mul_mmq_cm1.comp` at commit `c479922ac520a08969b4c1dc154d7bbb3c386d85`).

```glsl
coopmat<int8_t, gl_ScopeSubgroup, TM, TK, gl_MatrixUseA> cache_a;
coopMatLoad(cache_a, buf_a_qs, (a_row0 + r * TM) * QPITCH + ks * (BK / 4) + h * (TK / 4), QPITCH, gl_CooperativeMatrixLayoutRowMajor);
```

```glsl
coopmat<int8_t, gl_ScopeSubgroup, TK, TN, gl_MatrixUseB> cache_b;
coopMatLoad(cache_b, buf_b_qs, (b_col0 + c * TN) * QPITCH + ks * (BK / 4) + h * (TK / 4), QPITCH, gl_CooperativeMatrixLayoutColumnMajor);

const float scale_b_v = buf_b_d[ks * BN + b_col0 + c * TN + elem_col0];

coopmat<int32_t, gl_ScopeSubgroup, TM, TN, gl_MatrixUseAccumulator> acc =
    coopmat<int32_t, gl_ScopeSubgroup, TM, TN, gl_MatrixUseAccumulator>(
        USE_MAGIC_BIAS ? ACC_BIAS_BITS : 0);
acc = coopMatMulAdd(cache_a, cache_b, acc);
```

## What cooperative_matrix2 is meant to add

The VK_NV_cooperative_matrix2 proposal lists as limitations of the KHR extension that "subgroup scope matrices are small enough that using them the natural way in a GEMM does not lead to good performance. Shader authors can work around this by explicitly tiling and staging through shared memory, but it is cumbersome", and that for quantized weights "there is not a great way to dequantize these as they are loaded into a cooperative matrix" (`doc-vk-nv-cooperative-matrix2-proposal`, lines 16-33). The upstream shaders written against it are in `artifacts/kernels/llama-cpp-matmul/mul_mm_cm2.comp`, added by `pr-llama-cpp-10206`.

## Looking at what RADV generates

Mesa documents these `RADV_DEBUG` flags: `shaders` ("dump shaders"), `shaderstats` ("dump shader statistics"), `cs` ("Dump compute (and ray tracing) shaders"), `nir`, `ir` and `asm` (dump NIR, backend IR and shader disassembly "for selected shader stages"), and `nocache` ("disable shaders cache"). Under `RADV_PERFTEST` it documents `bfloat16` ("enable bfloat16 cooperative matrix support on GFX11-11.5") and `cswave32` ("enable wave32 for compute shaders (GFX10+)") (`doc-mesa-radv-envvars`). The documentation excerpted there is from Mesa `main` at the pinned commit, not from Mesa 25.2.7.
