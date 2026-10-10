---
id: doc-vk-gl-cts-cooperative-matrix-tests
title: 'VK-GL-CTS: cooperative-matrix compute tests (dEQP-VK.compute.*.cooperative_matrix)'
author: The Khronos Group Inc.
url: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp
source_category: upstream-code
architectures: []
tags:
- cooperative-matrix
- cooperative-matrix2
- subgroup-size-control
- required-subgroup-size
- shared-memory-limit
retrieved_at: '2026-10-10'
description: C++ source of the conformance tests; where the tests live and which cases they generate
---

# VK-GL-CTS: cooperative-matrix compute tests (dEQP-VK.compute.*.cooperative_matrix)

## Excerpt: external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp, lines 97-104 (matrix use per test group)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp#L97-L104

```text
typedef enum
{
    UT_NV = 0,
    UT_KHR_A,
    UT_KHR_B,
    UT_KHR_C,
    UT_KHR_Result,
} UseType;
```

## Excerpt: external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp, lines 173-202 (storage classes, addressing methods, subgroup size modes, feature levels)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp#L173-L202

```text
typedef enum
{
    SC_BUFFER = 0,
    SC_WORKGROUP,
    SC_WORKGROUP_VARIABLE_POINTERS,
    SC_BUFFER_VARIABLE_POINTERS,
    SC_PHYSICAL_STORAGE_BUFFER,
} StorageClass;

typedef enum
{
    ADDR_LINEAR = 0,
    ADDR_TENSORLAYOUT,
    ADDR_BLOCKSIZE,
    ADDR_DECODE,
} AddrMethod;

enum SubgroupSizeMode
{
    SUBGROUP_SIZE_NONE = 0,
    SUBGROUP_SIZE_MIN  = 1,
    SUBGROUP_SIZE_MAX  = 2,
};

enum CoopMatFeature
{
    CMF_BASE = 0,
    CMF_NV2,
    CMF_MAINT1,
};
```

## Excerpt: external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp, lines 6257-6281 (multiply-add test types and their case names)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp#L6257-L6281

```text
        {TT_FUNC_CONST_IN, "func_const_in"},
        // OpCooperativeMatrixMulAdd
        {TT_MATRIXMULADD, "matrixmuladd"},
        // OpCompositeConstruct w/array
        {TT_COMPOSITE_ARRAY, "composite_array"},
        // OpCooperativeMatrixMulAdd w/array
        {TT_MATRIXMULADD_ARRAY, "matrixmuladd_array"},
        // OpCooperativeMatrixMulAdd w/saturations
        {TT_MATRIXMULADD_SATURATED, "matrixmuladd_saturated"},
        // OpCooperativeMatrixMulAdd w/wrapping
        {TT_MATRIXMULADD_WRAPPING, "matrixmuladd_wrapping"},
        // OpCooperativeMatrixMulAdd w/stride==0
        {TT_MATRIXMULADD_STRIDE0, "matrixmuladd_stride0"},
        // OpCooperativeMatrixMulAdd
        {TT_MATRIXMULADD_CROSS, "matrixmuladd_cross"},
        // OpCooperativeMatrixMulAdd w/decode
        {TT_MATRIXMULADD_DEQUANT, "matrixmuladd_dequant"},
        // OpCooperativeMatrixMulAdd
        {TT_MATRIXMULADD_PUSH_CONSTANTS, "matrixmuladd_push"},
        //OpCooperativeMatrixMulAdd /w split barrier
        {TT_MATRIXMULADD_SPLITBARRIER, "matrixmuladd_split_barrier"},
        //OpCooperativeMatrixMulAdd /w split barrier and looped subgroup work
        {TT_MATRIXMULADD_SPLITBARRIER_LOOP, "matrixmuladd_split_barrier_loop"},
        //OpCooperativeMatrixMulAdd /w split barrier and skewed looped subgroup work
        {TT_MATRIXMULADD_SPLITBARRIER_SKEW, "matrixmuladd_split_barrier_skew"},
```

## Excerpt: external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp, lines 6398-6425 (layout, addressing, scope and storage-class dimensions of the case names)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp#L6398-L6425

```text
    TestGroupCase colCases[] = {
        {0, "rowmajor"},
        {1, "colmajor"},
    };

    TestGroupCase addrCases[] = {
        {ADDR_LINEAR, "linear"},
        {ADDR_TENSORLAYOUT, "tensorlayout"},
        {ADDR_BLOCKSIZE, "blocksize"},
        {ADDR_DECODE, "decode"},
    };

    TestGroupCase scopeCases[] = {
        {VK_SCOPE_SUBGROUP_KHR, "subgroupscope"},
        {VK_SCOPE_WORKGROUP_KHR, "workgroupscope"},
    };

    TestGroupCase scCases[] = {
        // SSBO
        {SC_BUFFER, "buffer"},
        // shared memory
        {SC_WORKGROUP, "workgroup"},
        // SSBO w/variable pointers
        {SC_BUFFER_VARIABLE_POINTERS, "buffer_varptr"},
        // shared memory w/variable pointers
        {SC_WORKGROUP_VARIABLE_POINTERS, "workgroup_varptr"},
        // physical_storage_buffer
        {SC_PHYSICAL_STORAGE_BUFFER, "physical_buffer"},
```

## Excerpt: external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp, lines 6464-6473 (subgroup-size variants are generated for matrixmuladd only)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp#L6464-L6473

```text
            for (int sgsNdx = 0; sgsNdx < DE_LENGTH_OF_ARRAY(sgsCases); sgsNdx++)
            {
                if (testType != TT_MATRIXMULADD && sgsCases[sgsNdx].value != SUBGROUP_SIZE_NONE)
                    continue;

                if (testType == TT_MATRIXMULADD && sgsCases[sgsNdx].value != SUBGROUP_SIZE_NONE && useType == UT_NV)
                    continue;

                const string name = string(ttCases[ttNdx].name) + sgsCases[sgsNdx].name;
                de::MovePtr<tcu::TestCaseGroup> ttGroup(new tcu::TestCaseGroup(testCtx, name.c_str()));
```

## Excerpt: external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp, lines 7417-7427 (top-level group)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/modules/vulkan/compute/vktComputeCooperativeMatrixTests.cpp#L7417-L7427

```text
tcu::TestCaseGroup *createCooperativeMatrixTests(tcu::TestContext &testCtx,
                                                 vk::ComputePipelineConstructionType computePipelineConstructionType)
{
    de::MovePtr<tcu::TestCaseGroup> group(new tcu::TestCaseGroup(testCtx, "cooperative_matrix"));

    group->addChild(createCooperativeMatrixTestsInternal(testCtx, computePipelineConstructionType, UT_NV));
    group->addChild(createCooperativeMatrixTestsInternal(testCtx, computePipelineConstructionType, UT_KHR_A));
    group->addChild(createCooperativeMatrixTestsInternal(testCtx, computePipelineConstructionType, UT_KHR_B));
    group->addChild(createCooperativeMatrixTestsInternal(testCtx, computePipelineConstructionType, UT_KHR_C));
    group->addChild(createCooperativeMatrixTestsInternal(testCtx, computePipelineConstructionType, UT_KHR_Result));
    createCooperativeMatrixOpConstantNullTests(testCtx, group.operator->(), computePipelineConstructionType);
```

## Excerpt: external/vulkancts/mustpass/main/vk-default/compute.txt, lines 8874-8878 (case names in the main must-pass list)

Locator: https://github.com/KhronosGroup/VK-GL-CTS/blob/5c715f61311aaa60a78632091606de56efa220a1/external/vulkancts/mustpass/main/vk-default/compute.txt#L8874-L8878

```text
dEQP-VK.compute.pipeline.cooperative_matrix.khr_r.subgroupscope.matrixmuladd.bfloat16_bfloat16.buffer.colmajor.linear
dEQP-VK.compute.pipeline.cooperative_matrix.khr_r.subgroupscope.matrixmuladd.bfloat16_bfloat16.buffer.colmajor.tensorlayout
dEQP-VK.compute.pipeline.cooperative_matrix.khr_r.subgroupscope.matrixmuladd.bfloat16_bfloat16.buffer.rowmajor.linear
dEQP-VK.compute.pipeline.cooperative_matrix.khr_r.subgroupscope.matrixmuladd.bfloat16_bfloat16.buffer.rowmajor.tensorlayout
dEQP-VK.compute.pipeline.cooperative_matrix.khr_r.subgroupscope.matrixmuladd.bfloat16_bfloat16.buffer_varptr.colmajor.linear
```

Licence of the excerpts: Apache-2.0 (`LICENSE` of the repository; copyright notices are in the file header).
