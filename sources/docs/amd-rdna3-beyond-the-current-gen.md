---
id: doc-amd-rdna3-beyond-the-current-gen
title: "RDNA 3: Beyond the Current Gen (AMD slides, Reboot Develop Blue 2023)"
author: "Lou Kramer (AMD)"
url: https://gpuopen.com/presentations/2023/RDNA3_Beyond-the-current-gen-v4.pdf
source_category: vendor-doc
architectures:
- rdna3
tags:
- subgroup-size
- subgroup-size-control
- wave64
- required-subgroup-size
retrieved_at: '2026-10-10'
---

# RDNA 3: Beyond the Current Gen (slide deck)

Locator: https://gpuopen.com/presentations/2023/RDNA3_Beyond-the-current-gen-v4.pdf (slide deck, 30 slides; title slide "RDNA™ 3: BEYOND THE CURRENT GEN", "LOU KRAMER"; slide footer "AMD PUBLIC | REBOOT DEVELOP BLUE 2023 | RDNA™ 3: BEYOND THE CURRENT GEN | APRIL 2023"; PDF metadata: Title "Get the best out of RDNA3", Author "Lou Kramer", CreationDate 2023-04-19)

Each excerpt is the complete text of one slide as `pdftotext -layout` extracts it, with blank lines, indentation and the footer line removed; indentation carried the bullet nesting. The slide number is the PDF page number, which equals the number printed in the slide footer.

The deck is not redistributable; only the two slides below are quoted.

## Excerpt: slide 10 ((COMPUTE) SHADERS)

```text
(COMPUTE) SHADERS
• RDNA introduced native support for Wave32
• Wave64 also supported
• Which one is it better to use (very generically)
• Wave32 for highly divergent code or long running threads
• Wave64 for ALU heavy and better data access patterns
• See later for shader write compression
• Can control this with WaveSize shader attribute in SM6.6
• Only currently applies to compute shaders
• Vulkan® has an extension too: VK_EXT_subgroup_size_control
• Driver will try to pick the optimal wave size for the given GPU
• The optimal wave size can differ between GPUs
• If you do set it manually
→ Always measure!
```

## Excerpt: slide 14 (SHADER WRITE COMPRESSION)

```text
SHADER WRITE COMPRESSION
• Compressor is “finicky” for optimal performance
• Surface are compressed as 2D 256Byte blocks
• Single store operation from wave needs to fully update 256Byte block
→ Sensitive to wave size, surface Byte per element (BPE), threadId mapping and thread-group dimensions
• Partial 256Byte block updates add significant compression overhead!
• For a 4BPE surface, assuming 1:1 threadId to UAV x,y
• 2D 256Byte blocks: Arranged as 8x8 blocks (8*8*4 = 256)
• Wave32 cannot do full overwrite (32*4 = 128)
• 16x16 thread-group does not fully overwrite
• Four 16x4 wave64
• Best bet is wave64 with 8x8 thread-group
• For large thread-groups remap threadIds to logically 8x8
• Write to all channels (don’t do partial writes)
```

The two slides state no measured figure, no device and no driver version.
