[Español](README.md) · English

# Dieline 112310 · Box with handle and snap-lock bottom

Source: https://www.pacdora.com/es/dielines-detail/custom-dimensions-tuck-end-box-variations-auto-bottome-snap-lock-boxes-dieline-112310

The initial manufacturing dimensions are retained: **302 × 152 × 182 mm**, material **1.5 mm E-flute**. Returned family: BuckleSuitcaseForward. The blank measures **952 × 439 mm**, with **16 faces, 15 folds, 72 outer-cut commands, and 3 interior openings**.

## Files and usage

- troquel-generado.svg: colored faces, red cuts, and dashed blue folds; interior openings, where present, are separate cut paths.
- troquel-generado.json: geometry and provenance.
- vista-previa.png: rasterized SVG, visually inspected.
- generar.py: reproduces SVG and JSON offline using standard Python, without external dependencies.
- base/knife-00.json and base/manifest.json: original response and REA manifest, including captured stages and hash.
- validacion.json: output checks.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/112310/generar.py
```

This replaces the output SVG and JSON while retaining the initial dimensions; it does not update the PNG preview. It provides no resizing or advanced controls: no parametric variations were captured for this model.

## Verification and limitations

Valid XML, counts, and agreement of every included geometric field with the original response were checked. The calculated total fold length is 3190.7774125491183 mm, compared with 3190.78 mm declared by the server. The local output was rasterized and inspected, including the handle opening, slots, and bottom tabs; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Not validated for manufacturing.

REA evidence: ev_a908ce42df7992776ec9aa9f023d02b40ed588be86d11b3e40489dbabec3274f. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
