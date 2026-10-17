[Español](README.md) · English

# Dieline 150010 · Flip-top mailer box

The user confirmed using the public template's initial values: **315 × 202 × 62 mm manufacturing dimensions**, **1.5 mm E-flute** corrugated board. The family returned by the server is Aircraft. The blank measures **576 × 590 mm** and contains 19 faces, 22 folds, 89 outer-cut commands, and 4 interior slots.

Public source: https://www.pacdora.com/es/dielines-detail/custom-dimensions-flip-top-boxes-mailer-dieline-150010

The original link included id=70845997. That project requires login in the REA session; its dimensions and settings were not recovered. The user explicitly chose the public template, so the following files do not claim to reproduce the private project.

## Files

- troquel-base-publica.svg: SVG with colored faces, red cuts, and dashed blue folds. Includes the 4 slots as separate paths.
- troquel-base-publica.json: public-template geometry and provenance.
- vista-previa.png: rasterized SVG for inspection.
- generar.py: reproduces SVG and JSON offline without external dependencies.
- base-publica/knife-00.json: original geometric response.
- base-publica/manifest.json: stages, URL, and captured-response hash.
- muestras/manifest.json: project access attempt, with the observed authentication dialog and no project geometry responses.
- validacion.json: counts and output-geometry check.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/150010/generar.py
```

This replaces the output SVG and JSON, retains the initial dimensions, and does not modify the PNG preview. It does not provide parametric resizing: no L/W/H variations were captured for this model. Advanced parameters are not exposed.

## Verification

Valid XML, 19 faces, 22 fold lines, and 4 slot paths were checked. Included geometric fields match the original response. The SVG was rendered with Sharp and the resulting image inspected: visible contours, tabs, and slots. This review verifies the local output, not its visual equivalence to a capture of the original editor.

The shared renderer was extended to include `holes`, because these slots are not part of the outer `cuts` contour. Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; tolerances, physical assembly, and manufacturing files were not checked. Not validated for manufacturing.

## REA evidence

- Project requiring authentication: ev_60173e6f93fcf44ac89b537f646726d3a916885ea7ddb4c0f9e5281392b954ec.
- Public template and geometry: ev_d08c5f2a484622e0e1879ed095969a4b8e9aca75e8d3199b8ca638fc1ba95afe.

Both captures completed. Their results exceeded the MCP transport limit and were recovered by evidence export without repeating the captures to recover the same result.
