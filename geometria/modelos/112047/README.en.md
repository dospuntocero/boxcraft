[Español](README.md) · English

# Dieline 112047 · Gable box with cord and snap-lock bottom

Source: https://www.pacdora.com/es/dielines-detail/roofing-cord-buckle-bottom-box-dieline-112047

The initial manufacturing dimensions are retained: **70 × 50 × 60 mm**, 350 g white paperboard, **0.5 mm** thick. The returned family is RoofWiringAndBottomBox. The blank measures **252.5 × 152.5 mm**, with **19 faces, 18 folds, 72 outer-cut commands, and 4 circular top holes**. The returned hole radius is 2 mm.

## Files and usage

- troquel-generado.svg: colored faces, red cuts, and dashed blue folds; interior openings, where present, are separate cut paths.
- troquel-generado.json: geometry and provenance.
- vista-previa.png: rasterized SVG, visually inspected.
- generar.py: reproduces SVG and JSON offline using standard Python, without external dependencies.
- base/knife-00.json and base/manifest.json: original response and REA manifest, including captured stages and hash.
- validacion.json: output checks.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/112047/generar.py
```

This replaces the output SVG and JSON while retaining the initial dimensions; it does not update the PNG preview. It provides no resizing or advanced controls: no parametric variations were captured for this model.

## Verification and limitations

Valid XML, counts, and agreement of every included geometric field with the original response were checked. The calculated total fold length is 1010.7692338711901 mm, compared with 1010.77 mm declared by the server. The local output was rasterized and inspected, with four visible holes, roof folds, side tab, and bottom closure; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Not validated for manufacturing.

REA evidence: ev_4f668f2c1bdecad06f7412545afea068086c1ad9e77e5d01e76afba6a6b770c0. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
