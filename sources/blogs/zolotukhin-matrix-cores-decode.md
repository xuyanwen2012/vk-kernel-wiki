---
id: blog-zolotukhin-matrix-cores-decode
title: Why RDNA4's matrix cores sit out the local LLM decode loop
author: zolotukhin.ai
url: https://zolotukhin.ai/blog/2026-04-30-rdna4-matrix-cores-sit-out-the-decode-loop/
source_category: community-note
architectures:
- amd
tags:
- cooperative-matrix
- gemm
- gemv
- prefill
- decode
retrieved_at: '2026-10-06'
---

# Why RDNA4's matrix cores sit out the local LLM decode loop

Locator: https://zolotukhin.ai/blog/2026-04-30-rdna4-matrix-cores-sit-out-the-decode-loop/ (post dated 2026-04-30)

Each excerpt is one paragraph of the post, copied in full; the number is the paragraph's position among the post's non-empty `<p>` elements.

## Excerpt: paragraph 12

```text
The Mesa RADV driver landed VK_KHR_cooperative_matrix support for RDNA4 in February of last year, following the earlier RDNA3 support. The Khronos extension is the Vulkan-side surface for what AMD calls WMMA on RDNA3, the wave-level matrix multiply instructions that drive the AI accelerator path. The Khronos extension proposal lays out the cooperative-matrix types and the SPIR-V intrinsics that compile down to those instructions on hardware that supports them.
```

## Excerpt: paragraph 14

```text
The mistake to avoid is reading those engineering decisions as a decode story. They are not. A cooperative-matrix mul_mat_vec for batch=1 decode would issue the same number of memory transactions as the existing scalar dispatch, finish the matrix instruction in a fraction of the time, and then sit idle waiting for the next weight tile to arrive. The wall time would be unchanged. The decode roofline is not going to move, no matter how many cooperative-matrix dispatches the engine learns to issue, because the dot is to the left of the ridge.
```

