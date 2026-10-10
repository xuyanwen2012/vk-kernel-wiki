---
id: doc-tvm-vulkan-runtime
title: 'Apache TVM (TensorIR compiler emitting SPIR-V, not GLSL): Vulkan runtime, device capabilities used by code generation'
author: The Apache Software Foundation
url: https://github.com/apache/tvm/blob/9059d9d25149c9ca7a015717b5023d1e2e1185fd/docs/arch/runtimes/vulkan.rst
source_category: official-doc
architectures: []
tags:
- 8bit-storage
- fp16-arithmetic
- int8-arithmetic
- storage-buffer
retrieved_at: '2026-10-10'
description: 'Language / backend: TVM generates SPIR-V from TensorIR; no GLSL source. Quoted: which device capabilities the code generator keys on'
---

# Apache TVM (TensorIR compiler emitting SPIR-V, not GLSL): Vulkan runtime, device capabilities used by code generation

Language and backend of the source: Apache TVM, which compiles each kernel from TensorIR to a SPIR-V compute shader; not GLSL.

## Excerpt: docs/arch/runtimes/vulkan.rst, lines 23-25 (kernels are compiled to SPIR-V)

Locator: https://github.com/apache/tvm/blob/9059d9d25149c9ca7a015717b5023d1e2e1185fd/docs/arch/runtimes/vulkan.rst#L23-L25

```text
TVM supports using Vulkan compute shaders to execute queries.  Each
computational kernel is compiled into a SPIR-V shader, which can then
be called using the TVM interface.
```

## Excerpt: docs/arch/runtimes/vulkan.rst, lines 34-48 (capabilities and limits drive code generation; -from_device)

Locator: https://github.com/apache/tvm/blob/9059d9d25149c9ca7a015717b5023d1e2e1185fd/docs/arch/runtimes/vulkan.rst#L34-L48

```text
Since different Vulkan implementations may enable different optional
features or have different physical limits, the code generation must
know which features are available to use.  These correspond to
specific Vulkan capabilities/limits as in
:ref:`Vulkan Capabilities Table <tvm-table-vulkan-capabilities>`.
If unspecified, TVM assumes that a capability is not available, or
that a limit is the minimum guaranteed by the Vulkan spec in the
`Required Limits`_ section.

These parameters can be either explicitly specific when defining a
:ref:`Target <tvm-target-specific-target>`, or can be queried from a
device.  To query from a device, the special parameter
``-from_device=N`` can be used to query all vulkan device parameters
from device id ``N``.  Any additional parameters explicitly specified
will override the parameters queried from the device.
```

## Excerpt: docs/arch/runtimes/vulkan.rst, lines 56-64 (subgroup operations parameter)

Locator: https://github.com/apache/tvm/blob/9059d9d25149c9ca7a015717b5023d1e2e1185fd/docs/arch/runtimes/vulkan.rst#L56-L64

```text
   * - Target Parameter
     - Required Vulkan Version/Extension
     - Parameter Queried
     - Default Value

   * - ``supported_subgroup_operations``
     - Vulkan 1.1+
     - ``VkPhysicalDeviceSubgroupProperties::supportedOperations``
     - 0 (interpreted as `VkSubgroupFeatureFlagBits`_)
```

## Excerpt: docs/arch/runtimes/vulkan.rst, lines 95-122 (8-bit and 16-bit storage, float16 and int8 parameters)

Locator: https://github.com/apache/tvm/blob/9059d9d25149c9ca7a015717b5023d1e2e1185fd/docs/arch/runtimes/vulkan.rst#L95-L122

```text
   * - ``supports_storage_buffer_8bit_access``
     - VK_KHR_8bit_storage
     - ``VkPhysicalDevice8BitStorageFeaturesKHR::storageBuffer8BitAccess``
     - false


   * - ``supports_storage_buffer_16bit_access``
     - VK_KHR_16bit_storage
     - ``VkPhysicalDevice16BitStorageFeaturesKHR::storageBuffer16BitAccess``
     - false


   * - ``supports_float16``
     - VK_KHR_shader_float16_int8
     - ``VkPhysicalDeviceShaderFloat16Int8FeaturesKHR::shaderFloat16``
     - false


   * - ``supports_float64``
     -
     - ``VkPhysicalDeviceFeatures::shaderFloat64``
     - false


   * - ``supports_int8``
     - VK_KHR_shader_float16_int8
     - ``VkPhysicalDeviceShaderFloat16Int8FeaturesKHR::shaderInt8``
     - false
```

## Excerpt: docs/arch/runtimes/vulkan.rst, lines 150-158 (declared SPIR-V capabilities)

Locator: https://github.com/apache/tvm/blob/9059d9d25149c9ca7a015717b5023d1e2e1185fd/docs/arch/runtimes/vulkan.rst#L150-L158

```text
Some of the device-specific capabilities also correspond to SPIR-V
capabilities or extensions that must be declared in the shader, or a
minimum SPIR-V version required in order to use a feature.  The
TVM-generated shaders will declare the minimum set of
extensions/capabilities and the minimum allowed version of SPIR-V
that are needed to execute the compiled graph.

If the shader generation requires a capability or extension that is
not enabled in the ``Target``, an exception will be raised.
```

Licence of the excerpts: Apache-2.0 (file header and `LICENSE` of the repository).
