---
id: doc-mesa-radv-envvars
title: 'Mesa environment variables: RADV_DEBUG and RADV_PERFTEST flags for shader inspection and cooperative matrix'
author: Mesa contributors
url: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst
source_category: official-doc
architectures:
- amd
tags:
- cooperative-matrix
- bfloat16-arithmetic
- subgroup-size
retrieved_at: '2026-10-06'
---

# Mesa environment variables: RADV_DEBUG and RADV_PERFTEST flags

## Excerpt: docs/envvars.rst, lines 1467-1468 (RADV_DEBUG flag `nocache`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1467-1468

```text
   ``nocache``
      disable shaders cache
```

## Excerpt: docs/envvars.rst, lines 1507-1508 (RADV_DEBUG flag `preoptir`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1507-1508

```text
   ``preoptir``
      Dump backend IR (ACO or LLVM) before any optimizations.
```

## Excerpt: docs/envvars.rst, lines 1516-1517 (RADV_DEBUG flag `shaders`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1516-1517

```text
   ``shaders``
      dump shaders
```

## Excerpt: docs/envvars.rst, lines 1518-1519 (RADV_DEBUG flag `shaderstats`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1518-1519

```text
   ``shaderstats``
      dump shader statistics
```

## Excerpt: docs/envvars.rst, lines 1522-1523 (RADV_DEBUG flag `spirv`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1522-1523

```text
   ``spirv``
      dump SPIR-V
```

## Excerpt: docs/envvars.rst, lines 1544-1545 (RADV_DEBUG flag `cs`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1544-1545

```text
   ``cs``
      Dump compute (and ray tracing) shaders.
```

## Excerpt: docs/envvars.rst, lines 1546-1547 (RADV_DEBUG flag `nir`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1546-1547

```text
   ``nir``
      Dump NIR for selected shader stages.
```

## Excerpt: docs/envvars.rst, lines 1548-1549 (RADV_DEBUG flag `ir`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1548-1549

```text
   ``ir``
      Dump backend IR (ACO or LLVM) for selected shader stages.
```

## Excerpt: docs/envvars.rst, lines 1550-1551 (RADV_DEBUG flag `asm`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1550-1551

```text
   ``asm``
      Dump shader disassembly for selected shader stages.
```

## Excerpt: docs/envvars.rst, lines 1596-1597 (RADV_PERFTEST flag `cswave32`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1596-1597

```text
   ``cswave32``
      enable wave32 for compute shaders (GFX10+)
```

## Excerpt: docs/envvars.rst, lines 1631-1632 (RADV_PERFTEST flag `bfloat16`)

Locator: https://gitlab.freedesktop.org/mesa/mesa/-/blob/0b2fa0445c2cdf6ab5e3a00214954670f0e0d2af/docs/envvars.rst#L1631-1632

```text
   ``bfloat16``
      enable bfloat16 cooperative matrix support on GFX11-11.5
```

Licence of the excerpts: MIT (Mesa); see `artifacts/prs/mesa/LICENSE`.
