---
id: doc-glsl-spec-shared-variables
title: 'OpenGL Shading Language specification, Variables and Types: Shared Variables'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/variables.adoc
source_category: official-doc
architectures: []
tags:
- shared-memory-limit
- control-barrier
- glsl
retrieved_at: '2026-10-10'
---

# OpenGL Shading Language specification, Variables and Types: Shared Variables

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/glsl/latest/chapters/variables.html

## Excerpt: chapters/variables.adoc, lines 2698-2717 (Shared Variables)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/variables.adoc#L2698-L2717

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/variables.html#shared-variables

```text
The *shared* qualifier is used to declare global variables that have storage
shared between all work items in a compute shader workgroup.
Variables declared as *shared* may only be used in compute shaders (see
"`<<compute-processor,Compute Processor>>`").
Any other declaration of a *shared* variable is {compiletimeerror}.
Shared variables are implicitly coherent (see
"`<<memory-qualifiers,Memory Qualifiers>>`").

Variables declared as *shared* may not have initializers and their contents
are undefined at the beginning of shader execution.
Any data written to *shared* variables will be visible to other work items
(executing the same shader) within the same workgroup.

In the absence of synchronization, the order of reads and writes to the same
*shared* variable by different invocations of a shader is not defined.

In order to achieve ordering with respect to reads and writes to *shared*
variables, control flow barriers must be employed using the *barrier*() function
(see "`<<shader-invocation-control-functions,Shader Invocation Control
Functions>>`").
```

## Excerpt: chapters/variables.adoc, lines 2719-2723 (Shared Variables, size limit)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/variables.adoc#L2719-L2723

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/variables.html#shared-variables

```text
There is a limit to the total size of all variables declared as *shared* in a
single program.
This limit, expressed in units of basic machine units may be determined by
using the {apiname} API to query the value of
MAX_COMPUTE_SHARED_MEMORY_SIZE.
```

Licence of the excerpts: CC-BY-4.0, Copyright 2008-2026 The Khronos Group Inc. (file header, lines 1-2).
