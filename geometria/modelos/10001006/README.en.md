[Español](README.md) · English

# Dieline 10001006 · Tuck-end box

Source: https://www.pacdora.com/es/dielines-detail/tuck-end-software-box-dieline-10001006

Initial manufacturing dimensions: **40 × 40 × 130 mm**, 350 g white paperboard, **0.5 mm** thick. Returned family: Pair. The **172.5 × 231 mm** blank has **13 faces, 12 folds, and 76 outer-cut commands**, with no interior openings.

## Files and usage

- troquel-generado.svg: colored faces, red cuts, and dashed blue folds; interior openings, where present, are separate cut paths.
- troquel-generado.json: geometry and provenance.
- vista-previa.png: rasterized SVG, visually inspected.
- generar.py: reproduces SVG and JSON offline using standard Python, without external dependencies.
- base/knife-00.json and base/manifest.json: original response and REA manifest, including captured stages and hash.
- validacion.json: output checks.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/10001006/generar.py
```

This replaces the output SVG and JSON while retaining the initial dimensions; it does not update the PNG preview. It provides no resizing or advanced controls: no parametric variations were captured for this model.

## Verification and limitations

Valid XML, counts, and agreement of every included geometric field with the original response were checked. The calculated total fold length is 810.4040064205623 mm, compared with 810.4 mm declared by the server. The local output was rasterized and inspected, including the glue tab, side flaps, and tuck closures; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Not validated for manufacturing.

REA evidence: ev_4c9d52a11d7a7bccb98fcd7cc22344a35016e616b6af52eb7fab1d14df6ace8a. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
