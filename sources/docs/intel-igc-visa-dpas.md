---
id: doc-intel-igc-visa-dpas
title: "DPAS instruction specification (intel-graphics-compiler vISA documentation)"
author: Intel Corporation
url: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md
source_category: official-doc
architectures:
- intel
tags:
- cooperative-matrix
- int8-cooperative-matrix
- coopmat-shape
- coopmat-fp32-accumulator
- bfloat16-arithmetic
- fp16-arithmetic
- mma-shape-selection
retrieved_at: '2026-10-10'
---

# DPAS instruction (Intel Graphics Compiler vISA documentation)

Repository: https://github.com/intel/intel-graphics-compiler, commit `6f81427a0be7c7c017d5be3f049dabec393cf788` (head of `master` on the retrieval date; the file was last changed by commit `15449850e4b5cbe003234a71915330c406c6699f`, dated 2024-10-21). File: `documentation/visa/instructions/DPAS.md`. Spelling is as in the file.

## Excerpt: documentation/visa/instructions/DPAS.md, lines 25-46 (Semantics, matrix form and K per precision)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L25-L46

```text
   DPAS is a matrix multiply-add operation as follows:

       D = C + A x B

       where
          D (Dst)  : MxN
          C (Src0) : MxN
          A (Src2) : MxK
          B (Src1) : KxN

          M : repeat count
          N : fixed execution size, either 8 or 16
          K : depth * OPS_PER_CHAN
              OPS_PER_CHAN
                 1 : for TF32
                 2 : for 16-bit precision(BF, HF)
                 4 : for 8-bit precision (FP8, UB, B)
                 8 : for less-then 8 bit precision (such as 4-bit data type, 2-bit data type).

              If depth is 8, K would be 8, 16, 32, or 64 (basd on OPS_PER_CHAN).

       Note that Src2 is A, and Src1 is B.
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 52-61 (Semantics, register layout of the operands)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L52-L61

```text
       If we view GRFs as a 1-D memory space in the increasing order of GRF numbers, Dst, Src0, Src2
       are laid out in row-major in this 1-D memory space. But Src1 needs a special layout, neither
       row-major nor column major. To visualize the layout for Src1,  we can view entire GRFs as a 2-D
       memory space with each row being an exactly one whole GRF. For example,  128 GRFs of 16 DWs each
       can be viewed as 128x16 of DW (it would be 128x8 if GRF size is 8 DWs), which means N must be 16.
       Under this view, each column of Src1 (matrix B) of total 16 columns are packed into its corresponding
       column of this 2-D memory space, that is, Column 0 of Src1 to Column 0 of 2-D memory space, column 1
       of Src1 to Column 1 of 2-D memory space, and so on. Take 8-bit precision for example, K is 32. This
       32 elements of 8-bit precision data is packed into 8 DWs (4 for each DW). For all 16 columns, it
       takes 8 rows in this 2-D memory space, which is 8 GRFs.
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 80-95 (Semantics, element sizes and OPS_PER_CHAN)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L80-L95

```text
       // 1) Src1PrecisionInBits and Src2PrecisionInBits are 16 for both bfloat(bf) and half(hf) dpas.
       // 2) Element size for Src0 and Dst are 4 bytes (either int or fp32)
       // 3) Element size for src1 and src2 could be 2 bits, 4 bits, 8 bits, or 16 bits (bf/hf),
       //    which are given as precisons.

       // OPS_PER_CHAN
       if (Src1PrecisionInBits == 16) {
         // BF/HF dpas. Src2PrecisionInBits must be 16
         OPS_PER_CHAN = 2;
       } else if (Src1Precision == 8 || Src2Precision == 8) {
         // integer dpas : dot4 per DW
         OPS_PER_CHAN = 4;
       } else {
         // integer dpas : dot8 per DW
         OPS_PER_CHAN = 8;
       }
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 114-114 (Semantics, execution size)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L114-L114

```text
       Exec_size = isPrePVC ? 8 : 16;
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 140-141 (Semantics, operand advance per repeat count)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L140-L141

```text
       Dst, Src0 are advanced one GRF for each repeat advance; Src2 is advanced 8*OPS_PER_CHAN for
       each repeat advance. Src1 stays the same for each repeat count advance.
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 150-156 (Description, integer and float DPAS)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L150-L156

```text
    Integer DPAS is a element wise multiply add and accumulate operation of multiple elements
    in a systolic pipeline with low precision (<= 8 bits) inputs. Src1 is also refered to
    as Weights, and Src2 as Activation. the element types of Src1 and Src2 are defined by
    Precision W and A, respectively. Src1 is divided into elements along each 32-bit SIMD channel.

    Float DPAS is the same, except its elements are always 16 bits. So each 32-bit channel has
    exactly two elements. And element type is either half float (hf) or bfloat16 (bf).
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 168-195 (Description, operand precision table)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L168-L195

```text
        +-------------------+-------------+--------+--------+
        | Operand Precision |  Range      | Binary | Text   |
        |                   |             | Format | Format |
        +-------------------+-------------+--------+--------+
        | unused            |             |  0x00  |        |
        +-------------------+-------------+--------+--------+
        | Unsigned 1-bit    | [0, 1]      |  0x01  | u1     |
        +-------------------+-------------+--------+--------+
        | Signed 1-bit      | [-1, 0]     |  0x02  | s1     |
        +-------------------+-------------+--------+--------+
        | Unsigned 2-bits   | [0, 3]      |  0x03  | u2     |
        +-------------------+-------------+--------+--------+
        | Signed 2-bits     | [-2, 1]     |  0x04  | s2     |
        +-------------------+-------------+--------+--------+
        | Unsigned 4-bits   | [0, 15]     |  0x05  | u4     |
        +-------------------+-------------+--------+--------+
        | Signed 4-bits     | [-8, 7]     |  0x06  | s4     |
        +-------------------+-------------+--------+--------+
        | Unsigned 8-bits   | [0, 255]    |  0x07  | u8     |
        +-------------------+-------------+--------+--------+
        | Signed 8-bits     | [-128, 127] |  0x08  | s8     |
        +-------------------+-------------+--------+--------+
        | bfloat            | bfloat16    |  0x09  | bf     |
        +-------------------+-------------+--------+--------+
        | half              | fp16        |  0x0a  | hf     |
        +-------------------+-------------+--------+--------+
        | tf32              | tf32        |  0x0b  | tf32   |
        +-------------------+-------------+--------+--------+
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 207-215 (Description, precision rules, accumulator and systolic depth)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L207-L215

```text
    For integer type, the precision of the sources can vary per src1 and src2. For float type, src1
    and src2 must be the same precision (either bf or hf, not mixed). For df type, dst/src0/src1/srcs must
    have same df precision.

    The dst and src0 take a regular integer type (e.g. D or UD) or float type which is 32 bits in size,
    Src0 is used as an accumulator to add operands to. The SD parameter is the systolic depth of the operation,
    meaning we perform a sequence of these operations advancing over successive inputs. The output of each stage
    is a dword (integer or float) or df which is the accumulated input to the next systolic stage. The first stage
    accumulation input is defined via Src0. The last stage accumulated output is written to Dst.
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 224-240 (Description, legal type combinations and systolic depth)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L224-L240

```text
       +--------+---------+------------+------------+
       | Dst    |  Src0   | Src1       | Src2       |
       |        |         | Precision  | Preision   |
       +--------+---------+------------+------------+
       | UD, D  |  UD,D   | int        | int        |
       +--------+---------+------------+------------+
       | F, BF  |  F, BF  | BF         | BF         |
       +--------+---------+------------+------------+
       | F, HF  |  F, HF  | HF         | HF         |
       +--------+---------+------------+------------+
       | F      |  F      | TF32       | TF32       |
       +--------+---------+------------+------------+
       | F      |  F      | BF8, HF8   | BF8, HF8   |
       +--------+---------+------------+------------+


    SD can be encoded as 1, 2, 4, and 8. XEHP+ only supports a systolic depth of 8.
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 246-249 (Exec_size encoding)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L246-L249

```text
  - Bit[2..0]: size of the region for source and destination operands

    - {XEHP}0b011:  8 elements
    - {PVC}0b100:  16 elements
```

## Excerpt: documentation/visa/instructions/DPAS.md, lines 316-328 (Notes, alignment and examples)

Locator: https://github.com/intel/intel-graphics-compiler/blob/6f81427a0be7c7c017d5be3f049dabec393cf788/documentation/visa/instructions/DPAS.md#L316-L328

```text
      - **Register region:** No
      - **Alignment:** Dst, Src0, and Src1 are GRF aligned; for interger or float(bf, hf) DPAS, Src2 is
        (SD/(32/(Src2PrecisionInBits * OPS_PER_CHAN))) DWORD aligned. That is, for SD=8 and OPS_PER_CHAN=4,
        src2 would be 8 DWORD aligned for s8/u8 precision; 4 DWORD aligned for s4/u4; and 2 DWORD aligned
        for s2/u2.

      Here are some examples:

      -  DPAS.u4.s8.8.8  (Exec_size) <dst> <src0> <src1> <src2>   // int DPAS with u4 for src1 and s8 for src1
      -  DPAS.bf.bf.8.8  (Exec_size) <dst> <src0> <src1> <src2>   // float DPAS with bfloat as element type
      -  DPAS.hf.hf.8.8  (Exec_size) <dst> <src0> <src1> <src2>   // float DPAS with half as element type

      Exec_size is 16 for PVC and 8 otherwise for int or float DPAS.
```

Licence of the excerpts: MIT, Copyright (C) 2020-2022 Intel Corporation (file header, lines 1-7; repository `LICENSE.md`).
