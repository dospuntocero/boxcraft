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
- compilar-reglas.py: derives the internal parameters and fits the rules from `parametrico/`.
- parametrico/: historical captures plus `extension/` with 273 samples from the range extensions.

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/10001006/generar.py
```

This replaces the output SVG and JSON. The editor uses a `compiled` engine that adapts L/W/H through rules over the internal parameters `A, AR, C, CR, E, S, G, NX, NY`, split into three width regimes; it does not update the PNG preview.

## Verified engine

The editor applies compiled rules over the internal parameters returned by Pacdora, split into three width regimes:

- `W <= 20`: ATT = 0, AX = 2.5, NX = NY = 2.
- `20 < W < 30`: ATT = 13, AX = 2.5, NX = NY = 2.
- `W >= 30`: ATT = 13, AX = 3.5, NX = NY = 3.

Parameters derived from L/W:

- `A = min(floor(L/2), floor((ceil(W) + C + 0.5)/2 + 0.5))`.
- `AR = W <= 30 ? 1 : L < 40 ? floor((W+2)/8)+1 : L < 60 ? floor((W+3)/8)+1 : L < 100 ? floor((W+13)/8) : floor((W+14)/8)`.
- `C = 10/11/13/15` and `CR = 5/6/7/8` for `L < 40`, `L < 60`, `L < 100`, and `L >= 100`.
- `E = 8` if `L >= 65`; otherwise `6` for `W > 30`, `4`/`5`/`6` for `L < 40`, `L < 45`, or the rest.
- `S = L >= 65 ? 6 : 4`.
- `G = L + W >= 125.25 ? 16 : min(13, W - 1.5)`.
- `NX = NY = W <= 30 ? 2 : 3`.

**321 responses** were captured (314 inside the validated range) and **79 holdouts** were reserved. The maximum error was **0.0000000000026 mm**; topology stayed at 13 faces, 12 folds and 76 cuts. The engine reproduces **L 30-100, W 10.6-60 and H 80-180 mm**, including fractional boundary samples and narrow widths such as **74 × 14 × 124 mm** (188 × 177 mm blank). Report in `reglas-parametricas.json` and `validacion-parametrica.json`; `compilar-reglas.py` rebuilds both from `parametrico/`.

Non-obvious boundaries were probed with fractions: `W = 10.6`, `14`, `20.5`, `29.5`, and `30.5`; `L = 64.5` and `99.5`; and `L + W = 125.25`. `G` changes at 125.25 (not 126), narrows to `W - 1.5` when `W < 15`, and `AR` changes formula at L = 40, 60, and 100.

## Verification and limitations

Using the Node engine, the 314 unique samples inside the range (378 files including historical duplicates) were checked field by field against the 725 numeric fields of the `traditional` layer (maximum error 1.9e-12). Valid XML, counts, and agreement with the original response were also checked. The calculated total fold length is 810.4040064205623 mm, compared with 810.4 mm declared by the server. The local output was rasterized and inspected, including the glue tab, side flaps, and tuck closures; it was not compared with an image of the original editor.

Arcs are interpreted as SVG A commands using the returned fields. Bleed and sizeArrowData annotations are excluded. Colors are for inspection; physical assembly, production tolerances, and AI/DXF/PDF files were not checked. Not validated for manufacturing.

Original REA evidence: ev_4c9d52a11d7a7bccb98fcd7cc22344a35016e616b6af52eb7fab1d14df6ace8a. The extension captures were taken with Playwright on 2026-10-28 and are kept in `parametrico/extension/` with a manifest and SHA-256. The capture completed; it exceeded the MCP transport limit and was recovered by exporting the record without repeating the capture.
