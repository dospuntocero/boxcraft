[Español](README.md) · English

# Dieline 180370 · French fries carton

Source: https://www.pacdora.com/es/dielines-detail/french-fries-box-dieline-180370

Initial manufacturing dimensions: **120 × 80 × 160 mm**, 250 g white paperboard, **0.35 mm** thick. Returned family: ChipBox. The **314.301396 × 453 mm** blank has **10 faces, 9 folds, and 26 outer-cut commands**, with no interior openings.

## Files and usage

- troquel-generado.svg: colored faces, red cuts, and dashed blue folds; interior openings, where present, are separate cut paths.
- troquel-generado.json: geometry and provenance.
- vista-previa.png: rasterized SVG, visually inspected.
- generar.py: reproduces SVG and JSON offline using standard Python, without external dependencies.
- base/knife-00.json and base/manifest.json: original response and REA manifest, including captured stages and hash.
- validacion.json: output checks.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/180370/generar.py
```

This replaces the output SVG and JSON while retaining the initial dimensions; it does not update the PNG preview. It provides no resizing or advanced controls: no parametric variations were captured for this model.

## Verification and limitations

Valid XML, counts, and agreement of every included geometric field with the original response were checked. The calculated total fold length is 1326.0558990037791 mm, compared with 1326.06 mm declared by the server. The local output was rasterized and inspected, with curved contours, sloping walls, and side tabs; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Not validated for manufacturing.

REA evidence: ev_122d9d496f87d479cdc26e2cd7caaeb42656bbc63e440199f52f8ae5a71e0ae5. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
