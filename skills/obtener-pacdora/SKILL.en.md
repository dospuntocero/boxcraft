---
name: obtener-pacdora
description: Acquire a Pacdora box by code using REA, document geometry, materials and dimensions, obtain its icon, and integrate it locally. Activate with «obtener CODIGO» in this project.
---

[Español](SKILL.md) · English

# Acquire a Pacdora box

Interpret `obtener CODIGO` as the complete instruction below. Preserve every digit of the code. Accept natural-language options, for example `obtener 15030101, 200 × 120 × 80 mm, cartulina de 0,5 mm, pliego 1000 × 700 mm`. This example does not instruct you to acquire the model when reading the skill.

## Execution prompt

Acquire the specified Pacdora model and complete REA research, local geometric reconstruction, technical sheet, icon, and addition to this project's editor. Use the available REA skill. Continue until the files and integration are verifiable; a proposal or isolated capture does not complete the request.

### Identity and preparation

Review `geometria/modelos/`, `investigacion/materiales/`, `editor-troqueles/`, and existing applications. Identify the current source application before editing; do not blindly synchronize copies in `archivo/copias/`. Reuse complete evidence for the same model and configuration without overwriting originals.

Locate and verify the actual page by code, title, and family. Do not invent the URL slug. Select the user's session, if present, through supported tools. Use actual REA schemas. If evidence exceeds transport limits, use views or export the record without repeating a completed capture.

### Dimensions, materials, and parameters

Without options, retain Pacdora's initial values as the base. Prioritize a requested configuration when provided. Record, per configuration:

- Requested and effective dimensions, units, axis meanings, and internal/external/manufacturing mode. Use mm as the canonical unit. Do not introduce a fictitious height in two-axis models.
- Material: ID, name, family, effective thickness, available options, and observed limits/steps for this model.
- Accessible advanced parameters, original values, automatic changes, internal/external allowances, radii, tabs, slots, and closures present in responses.
- Actual blank extent, sheet size, and allowed orientation. Do not treat limits from other boxes as universal.

Enumerate materials/thicknesses offered by this model and capture accessible discrete combinations. For continuous intervals, record range and step and take representative and boundary samples: do not claim exhaustive interval coverage. Maintain a matrix of complete, rejected, blocked, and pending cases.

Verify the effective selection after each change and wait for the corresponding response. Pacdora may change the material when dimensions change. `science` may retain the initial material: compare the visible control with `layer.traditional.science_id` and `layer.traditional.thickness` when present. A requested selection does not establish that the geometry corresponds to it.

### Evidence and reconstruction

Preserve original requests and responses, date, URL, REA references, and requested/effective configuration. Capture outer cuts, interior openings, folds, faces, curves/arcs, and metadata. Record bleed and dimensions when present and explain which layers are reproduced.

To reconstruct variable dimensions, vary one axis at a time and then validate independent combinations not used to fit rules. Repeat per material/thickness when behavior changes. Do not replace allowances with uniform scaling. If topology changes, distinguish cases or limit the engine to exact configurations.

Generate a reproducible local engine that does not query Pacdora to open or download results. Enable only axes, materials, and ranges supported by evidence. Separate checked rules, experimental approximations, and unknowns. Do not silently enable a fit that fails comparison. Preserve useful exact geometries even when a complete parametric engine cannot be reconstructed.

### Document and icon

Obtain the thumbnail/icon from the resource Pacdora actually uses and store it locally with URL, type, and SHA-256. Verify that it matches the code and that the editor does not depend on remote loading. If the original is inaccessible, generate a thumbnail from local geometry and label it as generated. Do not simulate an original icon with AI.

The default document is `geometria/modelos/CODIGO/README.md`: identity and sources; dimensions/modes; materials and thicknesses; coverage matrix; parameters; extent and sheet; rules; files; reproduction; validations and limitations. Include the blank preview and icon. If the user requests DOCX or PDF, also produce that format using its skill and verify rendering.

### Deliverables and local integration

Follow the project's actual schemas. Retain in `geometria/modelos/CODIGO/`:

- `README.md`, `base/` with the original response and manifest, and additional samples per configuration.
- `troquel-generado.svg`, `troquel-generado.json`, `vista-previa.png`, and a reproducible generator.
- Local icon and `validacion.json`.
- Provenance manifest: code, URL, date, requested/effective configurations, units, paths, hashes, REA references, and capture status. This may be part of the base manifest.

Integrate the model, icon, and checked configurations into the local catalog and data-preparation processes. Check selection, dimensions, materials, layers, preview, and export. Do not enable combinations without geometry. If the user requests research/documentation only, omit integration. Publishing, deployment, and uploading changes are outside the alias's scope.

### Validation and completion

Check valid JSON/XML, finite values, positive extent, and geometric correspondence with original responses, including arcs, folds, and openings. Compare independent samples field by field and document tolerance and maximum error; matching counts do not prove equivalence. Rasterize and inspect the SVG and visually compare it with the accessible reference. Verify sheet fit when its limits are established.

Run relevant existing tests and check the exported file, not just the button. State which checks could not be performed. Digital equivalence does not establish physical assembly or suitability for manufacturing.

If authentication, payment, HTTP 403, or disabled controls block progress, retain results and record the blocker without bypassing restrictions or repeating identical attempts. Complete independent tasks and list pending work. `cleanup_incomplete` does not establish successful session closure, though complete responses may serve as verifiable observations.

Deliver links to the document, SVG, preview, and icon; the integration location; tests; and the effective dimension/material scope. Declare complete only what was produced and verified; if required deliverables are missing, report partial results and the reason.
