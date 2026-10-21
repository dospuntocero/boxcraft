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

This replaces the output SVG and JSON. The editor uses a `compiled` engine that adapts L/W/H through rules over the internal parameters `A, AR, C, CR, E, NX, NY`; it does not update the PNG preview.

## Verified engine

The editor applies compiled rules over the internal parameters returned by Pacdora:

- `A = min(floor(L/2), floor(W/2 + (L >= 60 ? 7 : 6)))`.
- `AR`: 1 for W <= 30; 5 for W <= 37; 6 for W <= 44; 7 for W <= 52 (6 if L < 40 and W <= 45); 8 above. L=60 with W=60 uses 9; L=60 with 31 <= W <= 37 uses 6.
- `C` = 10 / 11 / 13 and `CR` = 5 / 6 / 7 for L < 40, L < 60, or L >= 60.
- `E`: 4/5/6 at W=30 depending on L; 6 otherwise.
- `NX = NY = W <= 30 ? 2 : 3`.

**97 configurations** were captured (L 30-60, W 30-60, H 80-180 mm), with 83 unique validated. The maximum error was **0.000000000001 mm**; topology stayed at 13 faces, 12 folds and 76 cuts. Report in `reglas-parametricas.json` and `validacion-parametrica.json`.

## Verification and limitations

Valid XML, counts, and agreement of every included geometric field with the original response were checked. The calculated total fold length is 810.4040064205623 mm, compared with 810.4 mm declared by the server. The local output was rasterized and inspected, including the glue tab, side flaps, and tuck closures; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Not validated for manufacturing.

REA evidence: ev_4c9d52a11d7a7bccb98fcd7cc22344a35016e616b6af52eb7fab1d14df6ace8a. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
