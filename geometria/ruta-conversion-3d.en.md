[Español](ruta-conversion-3d.md) · English

# Static route from dieline to 3D model

Source: pacdora-3d-CYhaKcyC1P.js, captured in evidence ev_77d8bd80d9fa88c43120d6cc5bd429c12c5968d9da9a0622cb273808367c498c. Minified names identify only this bundle.

1. `uV` selects the first non-gray layer containing data in `layer`. `dV` obtains the layer list from `modeCate.layerList` or falls back to the available keys in `layer`.
2. `mV` checks faces and their contours, cuts, folds, bleeds, total size, and thickness. `hV` throws an error listing missing fields when validation fails.
3. `gV` copies the selected layer's fields to the top level of the input object. It handles both naming variants, `holes` and `holds`.
4. `bV` selects a converter based on `modeCate.code`: `CurveBox` uses `CB`, `SoftPacking` uses `wB`, and other routes use `XS`. The observed code in the FEFCO 0201 response is `Carton`, compatible with the last branch. That call was not executed here.
5. `XS` initializes a WebAssembly wrapper: `ali` for zh-CN and `aws` for other languages. It serializes the object, uses `allocateUTF8`, calls `_generateGLTFData`, and decodes the result with `UTF8ToString`. The call from `bV` passes auxiliary arguments `0, null, 0, false`.
6. `vV` and `yV` check the result when it is a string starting with `{`: they check scenes, nodes, and meshes, and throw an error for malformed JSON or an empty model. This branch does not validate the entire glTF specification.
7. `bV` passes the result to `nD` and assigns the string to `window.gltfData`.
8. When class `xV` initializes, the returned object is searched for names such as `traditional_outer`, `traditional_inner`, and `traditional_side`. Different materials are applied to the exterior, interior, and edges. For models other than CurveBox and SoftPacking, the V component of certain meshes' UV coordinates is inverted.

Reference locations: `uV` starts at offset 1862741, `gV` at 1864278, `bV` at 1865852, and its call to `XS` appears at 1866081. These are zero-based character indices in text decoded by Python, not memory addresses or original source-code lines.

## WebAssembly inventory

The binary was extracted from previously captured bytes without downloading it again or executing it. Size: 1,206,159 bytes. SHA-256: a5fa190dd24abea89f6eeadbeadfb69520647b66410403e687662837d2ba01b4.

The export table contains `generateGLTFData` at function index 1494, `malloc`, stack functions, memory, and runtime utilities. The full inventory is in wasm-inventory.json. These symbols corroborate the interface used by the wrapper; they do not establish the internal algorithm or the generated model's fidelity.

## Limitations

This is a manual static trace through fragments of the received JavaScript, supported by the captured WASM load. It is not an observation of every runtime call, a WASM decompilation, or an engine reproduction. Downloaded code was not executed during this offline review. The exact output format, engine resource management, and print exporters remain unverified.
