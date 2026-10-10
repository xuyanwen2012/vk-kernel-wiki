---
id: meas-b70-fused-port
title: "Arc Pro B70: the Arc B580's multi-subgroup fused attention kernel brought over unchanged (byte-identical SPIR-V), against the tuned three-kernel parent (sarc-1.5-b70-fused-port)"
source_category: measurement
architectures: [arc-pro-b70]
tags: [sdpa, sdpa-qk, sdpa-av, sdpa-softmax, prefill, kernel-fusion, cooperative-matrix, subgroup-size, control-barrier, full-subgroups, coopmat-shape, required-subgroup-size, subgroup-grid, decode]
device: arc-pro-b70
driver: "ANV Mesa 26.2.3"
measured_at: '2026-10-09'
method: "Records of one tuning campaign, quoted from the pushed branch at the commit given per locator. End-to-end cells: llama_main, one 2048-token prefill per run, prefill tok/s, parent and candidate arms interleaved, median of the valid runs per arm (count stated in the excerpts); six cells = Llama 3.2 1B, Llama 3.2 3B, Llama 3.1 8B in the 4w and 8da4w schemes. Gate: SDPA correctness tiers of test_llama_microbench against a CPU reference, the campaign's verify script, and a next-token comparison between the arms. Device and driver are quoted from the vulkaninfo lines of the session's env.txt. Lines of the cited files that hold a host name, a board address or a storage path are not excerpted. A confirmation with one candidate. Sessions of 2026-10-09: s2-c1 (first gate), s3-final (gate on the build of commit 6ac44c483c167522e613ff5512a027770f27e906) and s4-pristine; 7 valid runs per arm. One kernel screen over already-built variants, 3 rounds, kernel time per layer at S = 2048. Decode: 5 runs per arm, 32 tokens after the 2048-token prompt."
raw_data:
  - repo: https://github.com/sarc-acl/executorch
    commit: c3d67a82125eee10edc14e5e4abdb931166f29fc
    locator: openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/env.txt
    description: "Final gate session environment: date, vulkaninfo device and driver lines"
  - repo: https://github.com/sarc-acl/executorch
    commit: c3d67a82125eee10edc14e5e4abdb931166f29fc
    locator: openspec/changes/sarc-1.5-b70-fused-port/proposal.md
    description: "Campaign record: what was brought, SPIR-V identity, the screen, results, trace, comparison with the B580, negative results"
  - repo: https://github.com/sarc-acl/executorch
    commit: c3d67a82125eee10edc14e5e4abdb931166f29fc
    locator: openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/summary.csv
    description: "Final gate session per-cell medians, gain, validity counts and next-token column"
  - repo: https://github.com/sarc-acl/executorch
    commit: c3d67a82125eee10edc14e5e4abdb931166f29fc
    locator: openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/gate.done
    description: "Final gate verdict"
  - repo: https://github.com/sarc-acl/executorch
    commit: c3d67a82125eee10edc14e5e4abdb931166f29fc
    locator: openspec/changes/sarc-1.5-b70-fused-port/results/b70/screens/screen1-select.csv
    description: "Selection screen medians"
  - repo: https://github.com/sarc-acl/executorch
    commit: c3d67a82125eee10edc14e5e4abdb931166f29fc
    locator: openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/attention.csv
    description: "Attention kernels of the warm traces by name, both arms"
  - repo: https://github.com/sarc-acl/executorch
    commit: c3d67a82125eee10edc14e5e4abdb931166f29fc
    locator: openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/runs.csv
    description: "Final gate per-run rows behind summary.csv"
captured_at: '2026-10-10'
commit: 6ac44c483c167522e613ff5512a027770f27e906
baseline: "Tuned parent: commit 5617714b0 with profile xe2-refine5 (three attention kernels). Second reference: the first campaign's pristine parent 6a7cc8cc6 with no profile."
---

## Device, driver and session date

Locator: `openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/env.txt`, line 1 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
Fri Oct  9 09:22:42 AM UTC 2026
```

Locator: `openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/env.txt`, lines 27-30 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
	apiVersion         = 1.4.354
	deviceName         = Intel(R) Graphics (BMG G31)
	driverName         = Intel open-source Mesa driver
	driverInfo         = Mesa 26.2.3
```

## What the campaign is, and its result line

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 10-19 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
## What this is

A confirmation, not a port: the fused attention kernel the B580 campaign built for the Intel matrix shape
(`sarc-1.5-b580-fused-port`, candidate 1 `b580-fused1`) is brought here unchanged, selected on top of this card's
final profile, gated and timed. No new kernel, no variant, no search, no sweep; one kernel screen over
already-built variants; one candidate.

**Result: `ET_VK_SARC_UNVERIFIED=1 ET_VK_SARC_DEV_PROFILE=b70-fused1`, `GATE_PASS` (plain pass, next token SAME
everywhere), +8.26 % geomean over the parent on the build of the committed head (+8.34 % on the first gate), and
+72.87 % geomean over the first campaign's pristine parent.**
```

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 43-46 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
- **Profile.** `b70-fused1` is one name: `xe2-refine5` for every call the fused kernel does not take, plus
  `d64_t16x64s16m8g4roj` (head_dim 64) and `d128_t16x128s16m8g8oj` (head_dim 128), the pair `b580-fused1` is at
  `cea76c634`. (The task file names an earlier pair, `d64_t16x32s16m8ro` / `d128_t16x64s16m8ro`; that was the
  B580's first smoke definition and is not what it gated.) Six `b70-fused-<variant>` profiles exist for the screen.
```

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 53-55 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
The kernel reaches a prefill call when S and `input_pos` are multiples of 64 (head_dim 64) or 128 (head_dim 128):
the 2048-token prompt and the 1792-token `r1304.txt` qualify; the 1972-token `prompt_check.txt` and decode run
the three kernels of `xe2-refine5`.
```

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 57-63 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
### SPIR-V identity (`tools/spv_identity.sh`, `results/b70/identity/`)

On `topic1` (`8ba3607be`) and on `topic2` (`6ac44c483`, the committed head that was measured last):
`SPV_IDENTITY_OK`. All 1525 shaders of the parent build are byte-identical in the topic build (1572 shaders); all
47 `sarc_dev_b580_sdpa_fused*` and `..._kvt*` shaders are byte-identical to the B580 campaign's build `topic6`
(`247d08851`, on which its candidate 1 was gated). Shipped-SPIR-V golden: PASS, 53 variants, on `parent`, `topic1`
and `topic2`.
```

## Candidate b70-fused1 against the tuned parent, per cell, and gate verdict

Locator: `openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/summary.csv`, lines 1-8 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
model,scheme,parent_med_tok_s,cand_med_tok_s,ratio,gain_pct,outside_2pct_band,parent_spread_pct,cand_spread_pct,valid_parent,valid_cand,invalid,clk_med_mhz_range,temp_pre_range,next_token_2048/check/unaligned,fbusy_pct_med_max
1b,4w,17964.90,20686.90,1.1515,+15.15,yes,1.75,3.00,7,7,-,2708-2750,61-66,SAME/SAME/SAME,0.00/0.00
1b,8da4w,20480.00,24381.00,1.1905,+19.05,yes,1.01,5.75,7,7,-,2800-2800,63-67,SAME/SAME/SAME,0.00/0.00
3b,4w,7529.41,7968.87,1.0584,+5.84,yes,0.73,2.32,7,7,-,2600-2617,64-67,SAME/SAME/SAME,0.00/0.00
3b,8da4w,9570.09,9990.24,1.0439,+4.39,yes,2.75,3.30,7,7,-,2800-2800,64-66,SAME/SAME/SAME,0.00/0.00
8b,4w,3379.54,3482.99,1.0306,+3.06,yes,0.82,1.20,7,7,-,2533-2533,65-67,SAME/SAME/SAME,0.00/0.00
8b,8da4w,4481.40,4623.02,1.0316,+3.16,yes,1.09,1.34,7,7,-,2800-2800,64-67,SAME/SAME/SAME,0.00/0.00
geomean over 6 cells: 1.0826 (+8.26 %), min 1.0306, max 1.1905
```

Locator: `openspec/changes/sarc-1.5-b70-fused-port/results/b70/sessions/s3-final/gate.done`, line 1 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
GATE_PASS
```

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 299-325 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
**Candidate 1, `b70-fused1`, against the tuned parent** (tok/s, median of 7 valid runs per arm, arms interleaved;
`s2-c1` on `topic1`, `s3-final` on the committed head `topic2`; recomputed from each `runs.csv`):

| cell | parent (`s3-final`) | `b70-fused1` (`s3-final`) | gain, committed head | gain, first gate (`s2-c1`) |
|---|---:|---:|---:|---:|
| 1B 4w | 17964.90 | 20686.90 | **+15.15 %** | +15.15 % |
| 1B 8da4w | 20480.00 | 24381.00 | **+19.05 %** | +17.86 % |
| 3B 4w | 7529.41 | 7968.87 | **+5.84 %** | +6.25 % |
| 3B 8da4w | 9570.09 | 9990.24 | **+4.39 %** | +4.39 % |
| 8B 4w | 3379.54 | 3482.99 | **+3.06 %** | +4.12 % |
| 8B 8da4w | 4481.40 | 4623.02 | **+3.16 %** | +3.16 % |
| geomean | | | **+8.26 %** | +8.34 % |

Every cell is outside the +-2 % band in both sessions. 84 timed runs in each, all valid: foreign engine time
0.00 %, at least one guard poll and 8 clock samples per run, lowest median clock 2533 MHz, no thermal reason.
The runner's timer steps by 1 ms (99 to 114 ms for 1B), so 1B medians move in steps of about 1 %.

Both gates `GATE_PASS` with 35 PASS lines and no FAIL line: SDPA tiers `all` / `extended` / `full`, 12 passes
each, every pass rc 0, 0 mismatches, `pairing=ok`, 192 of 192 case runs served by the fused kernel alone;
unmodified `verify.sh` identical to the parent snapshot line by line (`VERIFY_SAME`, 34 lines); next token parent
vs candidate SAME in all six cells on the three prompts; logits probe `PROBE_CHECK_OK`; `decide.py` `GATE_PASS`.
No next-token item differs, so the result is a plain pass and decisions D1 and D3 are not used. The kernel does
change the arithmetic; its error against the fp32 reference is smaller than the parent's on every production
shape (rms 2.0e-5 against 2.8e-5, maximum 7.1e-4 to 7.9e-4 against 1.06e-3 to 1.19e-3 at S = 2048;
`results/b70/sdpa-error/{c1-ref,final-ref}/`, identical in both runs) and on all eight `extended` cases; in one of
five synthetic `peaked` cases its maximum error is 8 % above the parent's with the rms 7 % below (reported, not a
gate item, fixed beforehand).
```

## The one kernel screen (us per layer)

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 276-291 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
## The one screen (`results/b70/screens/screen1-select{,-runs}.csv`)

The B580's selection screen repeated over the same seven profiles, 3 rounds, cooled before every run, kernel time
per layer at S = 2048 in us (median of the rounds; every round is in `STATUS.md`):

| head_dim | profile | 1B | 3B | 8B | vs the parent's three kernels |
|---|---|---:|---:|---:|---|
| | parent `xe2-refine5` (QK^T + softmax + attn*V) | 1481 | 1285 | 1691 | 1.00x |
| 64 | `d64_t32x32s32m8ro` (the 780M's) | 4255 | | | 0.35x |
| 64 | **`d64_t16x64s16m8g4roj`** | **486** | | | **3.05x** |
| 64 | `d64_t16x64s16m8g4oj` | 551 | | | 2.69x |
| 128 | `d128_t16x64s32m8ro` (the 780M's) | | 9569 | 12577 | 0.13x |
| 128 | **`d128_t16x128s16m8g8oj`** | | **749** | **967** | **1.72x / 1.75x** |
| 128 | `d128_t16x64s16m8g4oj` | | 819 | 1047 | 1.57x / 1.62x |

No variant beats the B580's pair in any round; `b70-fused1` is the B580's pair.
```

## Trace: attention before and after

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 347-361 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
### Trace: attention before and after (warm ETDump, ms per 2048-token prefill, kernels by name)

| cell | arm | dispatch total | QK^T | softmax | attn*V | fused | K/V copy | attention |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1B 4w | pristine parent (`s4-pristine`) | 165.0 | 29.8 | 16.4 | 34.6 | | | 80.8 |
| 1B 4w | tuned parent `xe2-refine5` (`s3-final`) | 105.9 | 4.8 | 12.7 | 6.1 | | | 23.7 |
| 1B 4w | `b70-fused1` | 89.9 | | | | 7.3 | 0.24 | 7.5 |
| 8B 4w | pristine parent (`s4-pristine`) | 828.4 | 116.6 | 33.6 | 134.2 | | | 284.3 |
| 8B 4w | tuned parent `xe2-refine5` (`s3-final`) | 596.2 | 14.4 | 25.9 | 16.2 | | | 56.5 |
| 8B 4w | `b70-fused1` | 571.0 | | | | 31.4 | 0.69 | 32.1 |

All six cells of both arms: `results/b70/sessions/{s2-c1,s3-final}/attention.csv`. The gain is the attention
family alone: 23.7 -> 7.5 ms on 1B (-68 %), 37.2 -> 21.4 ms on 3B (-42 %), 56.5 -> 32.1 ms on 8B (-43 %); the
dispatch total falls by the same amount. Most of what is removed is the softmax's pass over the S x S matrix
(12.7 of 23.7 ms on 1B). After the change attention is 8 % of the 1B prefill and 6 % of the 8B prefill.
```

## B580 against B70

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 363-378 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
## B580 against B70

The B580 campaign's prediction for this card ("expect the same two variants"; kernel level 2.75x / 1.55x / 1.57x
for 1B / 3B / 8B; about +9 % geomean, most of it on 1B; numbers of `topic/b580-fused-port` at `cea76c634`, a
citation) held. The same pair wins the screen here with the same ranking in every row. At kernel level the B70
gains a little more than predicted, 3.05x / 1.72x / 1.75x, in the same proportion for all three models (the
B70's kernels are 1.3 to 1.5 times faster in absolute time: 486 / 749 / 967 us against 724 / 1139 / 1464). End
to end the two cards agree within 2.4 points in every cell: 1B +15.2 / +19.1 % here against the B580's +17.1 /
+19.0 %, 3B +5.8 / +4.4 % against +5.4 / +6.8 %, 8B +3.1 / +3.2 % against +3.5 / +4.3 %, +8.26 % geomean against
+9.18 %. The traces do not show a smaller saving here: the fused kernel removes 15 % of the 1B dispatch time
and 4.2 % of the 8B dispatch time on this card (16 of 106 ms, 25 of 596 ms), against 12 % and 3.6 % on the B580
by its trace (19 of 161 ms, 33 of 917 ms). The end-to-end difference between the cards is therefore not
explained by the kernel; it is of the size of the B580 session's own spread (that session ran on a desktop in
use, arm spreads up to 5 %) and of the 1 ms timer step on 1B here, and is left as measured. The reference
errors are identical to the B580's to every printed digit, as they must be for the same SPIR-V on the same
inputs. No difference between the two cards was found that would call for a card-specific variant (L7 again).
```

## Negative results and limits (decode, unserved prompts, F1)

Locator: `openspec/changes/sarc-1.5-b70-fused-port/proposal.md`, lines 380-398 (commit `c3d67a82125eee10edc14e5e4abdb931166f29fc`)

```text
## Negative results and limits

- **Decode is 0 to 2.5 % slower with `b70-fused1`** (5 runs per arm, 32 tokens after the 2048-token prompt;
  `s2-c1`: 1B -2.5 / -1.2 %, 3B -1.3 / -1.5 %, 8B -0.8 / -1.0 %; `s3-final`: 1B -2.2 / 0.0 %, 3B -2.3 / -1.1 %,
  8B -1.1 / -0.9 %). The fused kernel does not serve decode; the cost was not located (no decode trace). Not a
  gate item; to be looked at before a promotion.
- No candidate 2: the B580 campaign gated its own (`b580-fused2`, the fp32 no-tail softmax for the calls the
  fused kernel does not take) at -0.13 % geomean and did not adopt it (its `STATUS.md` at `f613e3ed4`, read
  08:00 UTC, a citation), so by task section 6.4 none was brought here.
- The fused kernel serves only prompts whose length and position are multiples of the block (64 / 128 columns);
  the 1972-token real-text prompt runs the parent's kernels and gains nothing.
- Roofs were not re-measured: the campaign changes no linear kernel and the driver is the first campaign's
  (Mesa 26.2.3); its roofs of 2026-10-04 (`sarc-1.5-xe2-prefill-refine/results/xe2/roofline/`) stand as a
  citation, and no percent-of-roof is claimed here.
- What limits further progress on this card after this change: attention is 6 to 8 % of a prefill; the rest is
  the linear layers, which the first campaign's search left at 1 % steps.
- The B580 campaign's finding F1 (cooperative-matrix pipelines of the branch, shipped ones included, are SPIR-V
  1.3 without the full-subgroups flag the specification asks for) applies to this card unchanged; the fused
  kernel checks its subgroup layout at run time and every tier passed.
```
