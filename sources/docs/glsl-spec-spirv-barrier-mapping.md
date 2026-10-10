---
id: doc-glsl-spec-spirv-barrier-mapping
title: 'OpenGL Shading Language specification, SPIR-V mappings: mapping of barrier() and the memoryBarrier functions'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/spirvmappings.adoc
source_category: official-doc
architectures: []
tags:
- control-barrier
- memory-model
- glsl
- spirv
retrieved_at: '2026-10-10'
---

# OpenGL Shading Language specification, SPIR-V mappings: mapping of barrier() and the memoryBarrier functions

Rendered form of this file (unpinned `latest` build, fetched 2026-10-10): https://docs.vulkan.org/glsl/latest/chapters/spirvmappings.html

## Excerpt: chapters/spirvmappings.adoc, lines 648-675 (Mapping of barriers)

Locator: https://github.com/KhronosGroup/GLSL/blob/0099bf83b0288469917fc2e2972cb0a2b74d6711/chapters/spirvmappings.adoc#L648-L675

Rendered locator: https://docs.vulkan.org/glsl/latest/chapters/spirvmappings.html#_mapping_of_barriers

```text
=== Mapping of barriers

    barrier() (compute) -> OpControlBarrier(/*Execution*/Workgroup,
                                            /*Memory*/Workgroup,
                                            /*Semantics*/AcquireRelease |
                                                        WorkgroupMemory)

    barrier() (tess control) -> OpControlBarrier(/*Execution*/Workgroup,
                                                /*Memory*/Invocation,
                                                /*Semantics*/None)

    memoryBarrier() -> OpMemoryBarrier(/*Memory*/Device,
                                        /*Semantics*/AcquireRelease |
                                                    UniformMemory |
                                                    WorkgroupMemory |
                                                    ImageMemory)

    memoryBarrierBuffer() -> OpMemoryBarrier(/*Memory*/Device,
                                            /*Semantics*/AcquireRelease |
                                                        UniformMemory)

    memoryBarrierShared() -> OpMemoryBarrier(/*Memory*/Device,
                                            /*Semantics*/AcquireRelease |
                                                        WorkgroupMemory)

    memoryBarrierImage() -> OpMemoryBarrier(/*Memory*/Device,
                                            /*Semantics*/AcquireRelease |
                                                        ImageMemory)
```

Licence of the excerpts: CC-BY-4.0, Copyright 2008-2024 The Khronos Group Inc. (file header, lines 1-2).
