---
id: doc-glsl-khr-cooperative-matrix
title: GL_KHR_cooperative_matrix GLSL extension specification
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GLSL_KHR_cooperative_matrix.txt
source_category: official-doc
architectures: []
tags:
- cooperative-matrix
- glsl
- specialization-constants
retrieved_at: '2026-10-06'
---

# GL_KHR_cooperative_matrix GLSL extension specification

## Excerpt: extensions/khr/GLSL_KHR_cooperative_matrix.txt, lines 34-51 (Overview)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GLSL_KHR_cooperative_matrix.txt#L34-L51

```text
This extension adds a new set of types known as "cooperative matrix" types,
where the storage for and computations performed on the matrix are spread
across a set of invocations such as a subgroup. These types give the
implementation freedom in how to optimize matrix multiply operations.

This extension introduces the types and built-in functions, but does not
specify rules about what sizes/combinations are valid. This is left to
the Vulkan extension specifications, and it is expected that different
implementations may support different sizes. To help accommodate this,
the dimensions of the cooperative types are parameterized and can be
specialized via specialization constants.

This extension introduces limited support for parameterized types, with
the parameters specified as in C++ template syntax. The new built-in type
"coopmat" is the only type that can be parameterized, and its parameters
are a scalar type for the component type, an integer value that controls
the scope of the type, the number of rows and columns in the matrix, and
which matrix accumulation argument the matrix can be.
```

## Excerpt: extensions/khr/GLSL_KHR_cooperative_matrix.txt, lines 122-128 (matrix use constants)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GLSL_KHR_cooperative_matrix.txt#L122-L128

```text
gl_MatrixUse* are constant integer values which can be used for the MatrixUse template
parameter in cooperative matrix types. These control which operand of coopMatMulAdd the
type can be used as.

    const int gl_MatrixUseA             = 0;
    const int gl_MatrixUseB             = 1;
    const int gl_MatrixUseAccumulator   = 2;
```

## Excerpt: extensions/khr/GLSL_KHR_cooperative_matrix.txt, lines 178-183 (load and store)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GLSL_KHR_cooperative_matrix.txt#L178-L183

```text
The following functions are used to load and store cooperative matrix
values from and to memory. In memory, the matrices are stored as arrays
of their element type and size. In the following functions, the generic type
"coopmat" can accept a coopmat type with any type parameters. The
"buf" arrays must be in either buffer storage or shared storage, and the
array that is passed in can be sized or unsized.
```

## Excerpt: extensions/khr/GLSL_KHR_cooperative_matrix.txt, lines 287-297 (coopMatMulAdd)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/extensions/khr/GLSL_KHR_cooperative_matrix.txt#L287-L297

```text
coopmat coopMatMulAdd(coopmat A, coopmat B, coopmat C, int matrixOperands = 0);

Description: Linear-algebraic matrix multiply of A by B and then
component-wise add C. The order of the operations is implementation
dependent. The internal precision of the operations is defined by the
Vulkan specification.

The dimensions of A, B, and C, must form a valid matrix multiply (e.g.
the number of columns of A must match the number of rows of B). A, B,
and C must have the same scope. A's type must use gl_MatrixUseA.
B's type must use gl_MatrixUseB. C's type must use gl_MatrixUseAccumulator.
```

Copyright of the excerpts: Copyright (c) 2022-2023 The Khronos Group Inc.; copyright terms at http://www.khronos.org/registry/speccopyright.html (Notice section of the file, line 12).
