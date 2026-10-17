[Español](README.md) · English

# Dieline 180320 · Sandwich box with window

Source: https://www.pacdora.com/es/dielines-detail/sandwich-box-with-window-dieline-180320

Initial manufacturing dimensions exposed by the interface: **120 × 75 mm**, 350 g white paperboard, **0.5 mm** thick. This model has two dimensional controls; H=0 is an auxiliary API value, not a physical height of zero. Returned family: WindowLockSandwichBox.

The blank measures **289.4533188057741 × 289.37794000823277 mm**, with **12 faces, 13 folds, 63 outer-cut commands, and one interior window**.

## Files and usage

- troquel-generado.svg: colored faces, red cuts, and dashed blue folds; interior openings, where present, are separate cut paths.
- troquel-generado.json: geometry and provenance with L/W as the exposed dimensions.
- vista-previa.png: rasterized SVG, visually inspected.
- generar.py: reproduces SVG and JSON offline using standard Python, without external dependencies.
- base/knife-00.json and base/manifest.json: original response and REA manifest, including captured stages and hash.
- validacion.json: output checks.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/180320/generar.py
```

This replaces the output SVG and JSON while retaining the initial dimensions; it does not update the PNG preview. It provides no resizing or advanced controls: no parametric variations were captured for this model.

## Verification and limitations

Valid XML, counts, and agreement of every included geometric field with the original response were checked. The calculated total fold length is 1033.7041481883562 mm, compared with 1033.7 mm declared by the server. The local output was rasterized and inspected, including the window, diagonal folds, and tabs; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Window-film placement was not checked. Not validated for manufacturing.

REA evidence: ev_9e09f689ace42c23508869c90acd37b28df78921975b0730b2b74f72a35d73b1. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
