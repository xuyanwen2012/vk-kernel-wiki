---
id: doc-mnn-vulkan-optimization-handbook
title: 'MNN Vulkan optimization handbook (skills/vulkan-optimize): cooperative matrix, subgroup reduction, fused epilogue, occupancy'
author: MNN contributors (Alibaba)
url: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md
source_category: official-doc
architectures:
- qualcomm
- arm
tags:
- cooperative-matrix
- coopmat-shape
- specialization-constants
- subgroup-size
- kernel-fusion
- gemm
- convolution
- sdpa-av
- sdpa-softmax
retrieved_at: '2026-10-10'
description: 'Upstream optimization notes for the MNN Vulkan buffer backend, Apache-2.0, in Chinese; the complete file is pinned at artifacts/kernels/mnn-vulkan-optimize-notes/optimization-handbook.md'
---

# MNN Vulkan optimization handbook

The upstream document is written in Chinese; excerpts are verbatim. Complete pinned copy: `artifacts/kernels/mnn-vulkan-optimize-notes/optimization-handbook.md` (commit `9c1788748c4d8aba00f9b644f50f5c15576d7d80`).

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 60-68 (technique 1, cooperative-matrix matmul)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L60-L68

```text
### 技巧 1：Cooperative matrix 重写 matmul（Adreno）

**针对瓶颈**：GEMM / QKV 的 compute + 访存。**适用**：Adreno 支持 `VK_KHR_cooperative_matrix`（`getCoopMatInfo().supportCoopMat`），K 维够大（headDim/hidden ≥ COOP_K 且能整除）。

**做法**：用 `coopmat<...>` + `coopMatLoad/coopMatMulAdd/coopMatStore` 替代 scalar 累加；COOP_M/N/K 用设备 `selectedFP16CoopMatShape`（Adreno 常 16×16×16 或 64×64×16）经 spec constant 传入；local_size_x = subgroup size，一个 workgroup 一个 subgroup。

**注意**：coop matrix **只对 int8/int4 有硬件定义**（陷阱 H）；shader 需 `--target-env vulkan1.1`（陷阱 D）；K 维太小时 shared staging 开销盖过收益（headDim=128 做 coop-QK 实测 e2e −3%，负收益，已弃）。

**收益参考**：attention QK·V 用 coop（`885be352de`），scalar `qkv_acc_full` 102ms → `coop_qkv` 54ms（−47%，Adreno prefill）。
```

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 72-80 (technique 2, subgroup reduction)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L72-L80

```text
### 技巧 2：Subgroup 归约替代 shared-memory tree reduction

**针对瓶颈**：归约类 kernel（softmax / reduce）里的 barrier 开销。**适用**：设备支持 `VK_SUBGROUP_FEATURE_BASIC|ARITHMETIC`（`getSubgroupInfo().ops`）。

**做法**：一个 workgroup = 一个 subgroup（`local_size_x_id=0` 设为 subgroup size），用 `subgroupMax/subgroupAdd` 替代"shared 数组 + barrier + stride 折半"的树形归约，去掉所有 reduction barrier。保留 tree-reduction pipeline 作 Mali/老 driver fallback。

**注意**：需 `#extension GL_KHR_shader_subgroup_arithmetic : require` + `--target-env vulkan1.1`；host 按 `getSubgroupSize()` 动态设 local size，别 hardcode。

**收益参考**：prefill online-softmax（`6ac7caa5f5`）28.79→17.87ms（−38% kernel）。⚠️ 但 prefill e2e 0%（CPU-bound，见 §1.4 / 陷阱 F）——收益体现在散热/长文脉/大模型，不在短 prefill e2e。
```

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 84-92 (technique 3, coalesced epilogue store)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L84-L92

```text
### 技巧 3：Epilogue 合并写（coalesced store）

**针对瓶颈**：memory（非合并写 = scatter → DRAM 流量爆炸）。**适用**：coop matmul / 任意把 tile 写成非行连续布局（如 NC4HW4 转置）的 epilogue。

**做法**：让**输出的连续维在相邻线程间最快变化**。NC4HW4 输出 `[N/4, M, 4]`（`Cvec4[gn4*M + gm]`，token 维 gm 连续），epilogue 循环里让 `m = idx % TILE_M`（gm 最快）而非 `m = idx / n4PerTile`（n4 最快）——后者相邻线程写地址跨步 `M`（=token 数），完全非合并。纯线程→元素重映射，输出逐字节不变。

**注意**：改后 shared 读可能变 strided（bank conflict），但 global 合并写的收益 ≫ smem bank conflict，通常不用补 padding（本仓库实测加 smem padding 无额外收益）。

**收益参考**：conv1x1 coop epilogue（`80e26673f`），大 N int4 conv 该 shader 从 scatter 恢复合并写，4B-c4 prefill −13%→回收约一半（Convolution op 1304→1144ms）。
```

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 96-104 (technique 4, fused epilogue)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L96-L104

```text
### 技巧 4：融合 epilogue（把 unpack/scale 折进 matmul）

**针对瓶颈**：多余 dispatch + 中间 buffer 往返（Vulkan CPU 调度重，省 dispatch 收益大）。**适用**：matmul 后紧跟一个只读结果、逐元素变换再写出的独立 pass（unpack / 转置 / bias+relu / scale）。

**做法**：matmul 把 tile 存进 `shared`，`barrier()`，再直接按目标布局写出（含 bias/激活），省掉"写 temp → 独立 pass 读 temp"的一次 dispatch + 整个 temp buffer 往返。

**注意**：⚠️ 引入的 `shared` staging **会吃 occupancy**——小 N 净赚（省 dispatch/temp），**大 N 反伤**（occupancy 下降 > 省的调度，见技巧 5 + §1.3）。必须配合技巧 5 按规模门控。

**收益参考**：conv1x1 融合 COOP_to_C4（`45249b9c3`）+ scale_oacc 融进 coop QKV（`fba8885fb4`）：小模型（0.6B-c4）prefill +8%。
```

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 108-116 (technique 5, gating fused and split paths by output size)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L108-L116

```text
### 技巧 5：按输出规模门控融合 vs 分离路径

**针对瓶颈**：occupancy——同一融合优化对小/大问题规模收益相反。**适用**：技巧 4 的融合 epilogue 用了 `shared`，在大 N 上 occupancy 损失盖过省下的 dispatch。

**做法**：保留两条路径——小 N 走**融合**（零 temp，省 dispatch），大 N 走**分离**（matmul 写 row-major temp，**不用 shared → 高 occupancy** + 一个独立 unpack pass）。用 `padN` 阈值门控（env 可调）。阈值靠**逐 conv dump 出真实 N 分布**确定：本仓库 dump 出 2B 最大 conv N=6144 偏好融合、4B N=9728 偏好分离，故阈值取 8192 干净切分。

**注意**：阈值是设备/模型相关，做成 env 可调（`MNN_VK_CONV_FUSE_MAXN`）便于调优；两条路径都要过正确性。用 spec-constant 或两个 shader 变体实现分离路径的"零 shared matmul"。

**收益参考**：conv1x1 coop 按 N 门控（`80e26673f`），4B-c4 prefill −6%→**+2.6%**（超 baseline），同时 0.6B +9% / 2B +7% 全保住。
```

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 158-160 (pitfall D, target environment)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L158-L160

```text
### 陷阱 D：coop / subgroup / memory_scope shader 需 target-env vulkan1.1

含 `GL_KHR_cooperative_matrix` / `GL_KHR_shader_subgroup*` / `GL_KHR_memory_scope_semantics` 的 shader 会 emit `SPV_KHR_vulkan_memory_model`（需 SPIR-V ≥ 1.3）。不加 `--target-env vulkan1.1`，glslang 默认 emit SPIR-V 1.0，spirv-opt 拒绝 → 静默回退到未优化 SPIR-V（或编译失败）。makeshader 已按扩展关键字判断，手动外科式重生成时务必带上。
```

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 174-176 (pitfall H)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L174-L176

```text
### 陷阱 H：cooperative matrix 只支持 int8/int4

coop matrix 用硬件 S8S8S32 / S4S8S32 指令，只对 int8/int4 weight 有定义。新加 w2/w3 时 host 必须显式跳过 coop 路径走 `VulkanConv1x1General`（native 低 bit gemv），否则用错 layout 解 buffer → 数值乱或 driver crash。
```

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 178-180 (pitfall I, shared arrays)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L178-L180

```text
### 陷阱 I：shared 数组吃 occupancy

Vulkan compute 的 `shared` 数组直接限制常驻 workgroup 数。融合 epilogue 引入 8KB `shared` 在大 N conv 上使 occupancy 下降、净 +148ms（技巧 5）。加 `shared` 前评估 occupancy 影响，大问题规模考虑无-shared 的分离路径。
```

## Excerpt: skills/vulkan-optimize/optimization-handbook.md, lines 190-192 (pitfall L, partial tiles)

Locator: https://github.com/alibaba/MNN/blob/9c1788748c4d8aba00f9b644f50f5c15576d7d80/skills/vulkan-optimize/optimization-handbook.md#L190-L192

```text
### 陷阱 L：coop 端数 tile 越界读靠 robustBufferAccess 兜底（UB）

coop `coopMatLoad` 按固定 COOP_M/N/K 块读，M（如 qLen/token）非块整数倍时末尾 tile 会读到 buffer 之外（此前靠 robustBufferAccess 返回 0 + store guard 兜底，输出对但是 UB）。修法：host 侧把对应 workspace 的 M 维 padding 到 COOP_M 倍数，让 coop load 恒在界内（本仓库 coop_qkv 的 W buffer 修复，`80e26673f`）。
```
