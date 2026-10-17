[Español](README.md) · English

# Dieline 12109002 · Cake box with handles

Source: https://www.pacdora.com/es/dielines-detail/cake-box-dieline-12109002

Initial manufacturing dimensions: **236 × 170 × 180 mm**, material **1.5 mm E-flute**. Returned family: TrapezoidalFoldingAngleHandleTrayBox. The **824 × 1018 mm** blank has **19 faces, 26 folds, 46 outer-cut commands, and 4 interior openings** for handles and closure.

## Files and usage

- troquel-generado.svg: colored faces, red cuts, and dashed blue folds; interior openings, where present, are separate cut paths.
- troquel-generado.json: geometry and provenance.
- vista-previa.png: rasterized SVG, visually inspected.
- generar.py: reproduces SVG and JSON offline using standard Python, without external dependencies.
- base/knife-00.json and base/manifest.json: original response and REA manifest, including captured stages and hash.
- validacion.json: output checks.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/12109002/generar.py
```

This replaces the output SVG and JSON while retaining the initial dimensions; it does not update the PNG preview. It provides no resizing or advanced controls: no parametric variations were captured for this model.

## Verification and limitations

Valid XML, counts, and agreement of every included geometric field with the original response were checked. The calculated total fold length is 4563.102295402743 mm, compared with 4563.1 mm declared by the server. The local output was rasterized and inspected, including visible handles, side slots, tabs, and diagonal folds; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Not validated for manufacturing.

REA evidence: ev_f15d9188197a7f8329e36bc85cb9c878bfb0c34f341a627343031a2b300da5b6. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
