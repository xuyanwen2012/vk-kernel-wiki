---
id: doc-wonnx-gemm-template
title: 'wonnx (Rust runtime, WGSL templates, not GLSL): Gemm shader template multiplying matNxN chunks'
author: Xavier Tao, Tommy van der Vorst and WONNX contributors
url: https://github.com/webonnx/wonnx/blob/c62f5d336c152102882a163ebc1eb18e63550de8/wonnx/templates/matrix/gemm.wgsl
source_category: upstream-code
architectures: []
tags:
- gemm
retrieved_at: '2026-10-10'
description: 'Language / backend: WGSL generated from Tera templates for WebGPU (wgpu). Quoted: the chunked matrix-multiply loop'
---

# wonnx (Rust runtime, WGSL templates, not GLSL): Gemm shader template multiplying matNxN chunks

Language and backend of the source: WGSL produced from a Tera template by a Rust runtime (wgpu); not GLSL.

## Excerpt: wonnx/templates/matrix/gemm.wgsl, lines 1-7 (element packing into vectors and square matrices)

Locator: https://github.com/webonnx/wonnx/blob/c62f5d336c152102882a163ebc1eb18e63550de8/wonnx/templates/matrix/gemm.wgsl#L1-L7

```text
alias Scalar = {{ scalar_type }};
alias GemmVec = vec{{ kernel_size }}<{{ scalar_type }}>;
alias GemmMat = mat{{ kernel_size }}x{{ kernel_size }}<{{ scalar_type }}>;

struct GemmArrayVector {
	data: array<GemmVec>
};
```

## Excerpt: wonnx/templates/matrix/gemm.wgsl, lines 26-37 (workgroup size and index mapping)

Locator: https://github.com/webonnx/wonnx/blob/c62f5d336c152102882a163ebc1eb18e63550de8/wonnx/templates/matrix/gemm.wgsl#L26-L37

```text
@compute @workgroup_size({{ workgroup_size_x }}, {{ workgroup_size_y }})
fn main(@builtin(global_invocation_id) global_id: vec3<u32>) {
	let y = global_id.x % {{ n_chunks }}u;
	let x = global_id.x / {{ n_chunks }}u;

	{# Calculate stacking offsets #}
	let stack_index = global_id.y;
	let left_offset = stack_index * {{ stack_left_stride / kernel_size | int }}u;
	let right_offset = stack_index * {{ stack_right_stride / kernel_size | int }}u;
	let output_offset = stack_index * {{ stack_output_stride / kernel_size | int }}u;

	let index = output_offset + (x * {{ right_shape[1] }}u) + y;
```

## Excerpt: wonnx/templates/matrix/gemm.wgsl, lines 52-73 (accumulation over K in matNxN chunks)

Locator: https://github.com/webonnx/wonnx/blob/c62f5d336c152102882a163ebc1eb18e63550de8/wonnx/templates/matrix/gemm.wgsl#L52-L73

```text
	var tmpsum = zero_matrix;
	var product = zero_matrix;

	for(var k: u32 = 0u; k < {{ k_chunks }}u; k = k + 1u) {
		let index_left = left_offset + (x * {{ left_shape[1] }}u) + k;
		let index_right = right_offset + (k * {{ right_shape[1] }}u) + y;

		let mat_left = GemmMat(
			{% for i in range(end = kernel_size) %}
				input_left.data[index_left + {{ i * k_chunks }}u] {%-if not loop.last -%},{%- endif -%}
			{% endfor %}
		);
		
		let mat_right = GemmMat(
			{% for i in range(end = kernel_size) %}
				input_right.data[index_right + ({{ i * n_chunks }}u)] {%-if not loop.last -%},{%- endif -%}
			{% endfor %}
		);
	
		product = mat_right * mat_left;
		tmpsum = tmpsum + product;
	}
```

Licence of the excerpts: MIT OR Apache-2.0 (`README.md` section "License", `LICENSE-MIT`, `LICENSE-APACHE`).
