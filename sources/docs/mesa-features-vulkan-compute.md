---
id: doc-mesa-features-vulkan-compute
title: 'Mesa features.txt: drivers listed for cooperative matrix, bfloat16, subgroup size control, integer dot product, float16/int8, 8-bit storage and workgroup memory layout'
author: Mesa contributors
url: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt
source_category: official-doc
architectures:
- rdna3
- intel
- turing
- qualcomm
- arm
tags:
- cooperative-matrix
- bfloat16-arithmetic
- subgroup-size-control
- integer-dot-product
- fp16-arithmetic
- int8-arithmetic
- 8bit-storage
- shared-memory-limit
retrieved_at: '2026-10-10'
---

# Mesa features.txt: drivers listed for cooperative matrix, bfloat16, subgroup size control, integer dot product, float16/int8, 8-bit storage and workgroup memory layout

Line locators refer to commit `5c80eda3f1c0ac7cb80b0597473ae83da4b97c08` (head of `main` on 2026-10-10).

## Excerpt: docs/features.txt, lines 5-17 (how to read the file)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L5-17

```text
all DONE: <driver>, ...
    All the extensions are done for the given list of drivers.

DONE
    The extension is done for Mesa and no implementation is necessary on the
    driver-side.

DONE ()
    The extension is done for Mesa and all the drivers in the "all DONE" list.

DONE (<driver>, ...)
    The extension is done for Mesa, all the drivers in the "all DONE" list, and
    all the drivers in the brackets.
```

## Excerpt: docs/features.txt, lines 470-472 (Vulkan 1.2 drivers and VK_KHR_8bit_storage)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L470-472

```text
Vulkan 1.2 -- all DONE: anv, hk, nvk, panvk, pvr, tu, vn

  VK_KHR_8bit_storage                                   DONE (anv, dzn, hasvk, kk, lvp, nvk, panvk, radv, tu/a750+, v3dv, vn)
```

## Excerpt: docs/features.txt, line 483 (VK_KHR_shader_float16_int8)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L483

```text
  VK_KHR_shader_float16_int8                            DONE (anv, dzn, hasvk, kk, lvp, nvk, panvk, radv, tu, v3dv/vc7+, vn)
```

## Excerpt: docs/features.txt, line 497 (Vulkan 1.3 drivers)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L497

```text
Vulkan 1.3 -- all DONE: anv, hk, kk, lvp, nvk, panvk, radv, tu, vn, v3dv
```

## Excerpt: docs/features.txt, line 503 (VK_KHR_shader_integer_dot_product)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L503

```text
  VK_KHR_shader_integer_dot_product                     DONE (anv, dzn, hasvk, lvp, nvk, panvk, pvr, radv, tu, v3dv, vn)
```

## Excerpt: docs/features.txt, line 517 (VK_EXT_subgroup_size_control)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L517

```text
  VK_EXT_subgroup_size_control                          DONE (anv, dzn, hasvk, lvp, nvk, panvk, pvr, radv, tu, v3dv, vn)
```

## Excerpt: docs/features.txt, line 542 (section heading)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L542

```text
Khronos extensions that are not part of any Vulkan version:
```

## Excerpt: docs/features.txt, line 547 (VK_KHR_cooperative_matrix)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L547

```text
  VK_KHR_cooperative_matrix                             DONE (anv, lvp, nvk/Turing+, panvk/v11+, radv/gfx11+, vn)
```

## Excerpt: docs/features.txt, line 587 (VK_KHR_shader_bfloat16)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L587

```text
  VK_KHR_shader_bfloat16                                DONE (anv/gfx12.5+, radv/gfx12+, vn)
```

## Excerpt: docs/features.txt, line 607 (VK_KHR_workgroup_memory_explicit_layout)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L607

```text
  VK_KHR_workgroup_memory_explicit_layout               DONE (anv, hk, kk, lvp, nvk, hasvk, panvk, pvr, radv, tu, v3dv, vn)
```

## Excerpt: docs/features.txt, line 622 (VK_EXT_cooperative_matrix_maintenance1)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/5c80eda3f1c0ac7cb80b0597473ae83da4b97c08/docs/features.txt#L622

```text
  VK_EXT_cooperative_matrix_maintenance1                DONE (lvp, radv/gfx11+)
```

Licence of the excerpts: MIT (Mesa); see `artifacts/prs/mesa/LICENSE`.
