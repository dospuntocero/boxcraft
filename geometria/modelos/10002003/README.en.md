[Español](README.md) · English

# Dieline 10002003 · Double hanging-tab box

Source: https://www.pacdora.com/es/dielines-detail/custom-dimensions-hook-boxes-double-hook-dieline-10002003-10002003

Initial manufacturing dimensions: **100 × 40 × 120 mm**, 350 g white paperboard, **0.5 mm** thick. Returned family: PairWithHook. The **295.5 × 263.75 mm** blank has **16 faces, 15 folds, 94 outer-cut commands, and 2 hanging openings**.

## Files and usage

- troquel-generado.svg: colored faces, red cuts, and dashed blue folds; interior openings, where present, are separate cut paths.
- troquel-generado.json: geometry and provenance.
- vista-previa.png: rasterized SVG, visually inspected.
- generar.py: reproduces SVG and JSON offline using standard Python, without external dependencies.
- base/knife-00.json and base/manifest.json: original response and REA manifest, including captured stages and hash.
- validacion.json: output checks.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/10002003/generar.py
```

This replaces the output SVG and JSON. The editor uses a `compiled` engine that adapts L/W/H through rules over the internal parameters `A, AR, C, CR, G, L1, NX, NY`; it does not update the PNG preview.

## Verified engine

The editor applies compiled rules over the internal parameters returned by Pacdora:

- `A = floor(W/2) + (L >= 100 ? 8 : 7)`.
- `AR = W < 31 ? 1 : W < 33 ? 5 : W < 41 ? 6 : 7`.
- `C = L >= 100 ? 15 : 13`; `CR = L >= 100 ? 8 : 7`.
- `G = L + W >= 129 ? 16 : 13`; `L1 = L - 1`.
- `NX = NY = W < 31 ? 2 : 3`.

**49 configurations** were captured (L 80–120, W 30–48, H 80–150 mm), with 12 held out. The maximum error was **0.000000000003 mm**; topology stays at 16 faces, 15 folds, 94 cuts and 2 openings. The report is in `reglas-parametricas.json` and `validacion-parametrica.json`.

## Verification and limitations

Valid XML, counts, and agreement of every included geometric field with the original response were checked. The calculated total fold length is 1270.0040064205623 mm, compared with 1270 mm declared by the server. The local output was rasterized and inspected, including both hanging openings and tuck closures; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Not validated for manufacturing.

REA evidence: ev_418dd2411d60f065f42d0416564f26e7f24c8424b3a209c929e9d5f15451e97e. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
