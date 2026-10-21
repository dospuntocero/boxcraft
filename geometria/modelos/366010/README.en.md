[Español](README.md) · English

# Dieline 366010 · Rigid box with lid

Source: <https://www.pacdora.com/es/dielines-detail/custom-dimensions-box-with-lid-luxury-box-dieline-366010>

Model **366010**, “Custom dimensions box with lid luxury box dieline”, internal Pacdora id **1563**, category `1593`. Initial configuration: **180 × 100 × 40 mm** manufacturing, 0.15 mm “Boutique custom” wrapping paper (science 48), and 2 mm greyboard (editable 1.5–2.5 mm).

![Dieline preview](vista-previa.png)

## Four pieces

| Piece | Pacdora layer | Thickness | Extent | Faces | Cuts | Folds | Bleeds |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Bottom · greyboard | `BoutiqueboxDivideEquallyCoverBottomGreyboard` | 2 mm | 260 × 180 mm | 5 | 22 | 4 | 0 |
| Bottom · paper | `BoutiqueboxDivideEquallyCoverBottomFacepaper` | 0.15 mm | 300.95 × 220.95 mm | 25 | 86 | 24 | 38 |
| Lid · greyboard | `BoutiqueboxDivideEquallyCoverTopGreyboard` | 2 mm | 269.8 × 189.8 mm | 5 | 22 | 4 | 0 |
| Lid · paper | `BoutiqueboxDivideEquallyCoverTopFacepaper` | 0.15 mm | 310.75 × 230.75 mm | 25 | 86 | 24 | 38 |

The local sheet places the four pieces in a 2 × 2 grid with a 25 mm gap: **605.55 × 476.7 mm**, **60 faces**, **56 folds**, **216 cut commands**, and **no holes**.

The original response carries **76 bleed commands**, but they form a stepped polygon that does not follow the cut with a uniform offset: some spans sit 6 mm away and the corners jump at right angles. It is therefore not used for drawing. The SVG and editor show a contour computed **3 mm from the cut**, only for the two paper pieces (2 subpaths); greyboard has no bleed. The original layer remains as evidence in `base/knife-00.json`, and the computed contour is stored in `base/bleed-path.txt`. It follows Pacdora’s official layout: bottom box on the left/top, lid on the left/bottom, wrapping paper on the right.

## Parametric L/W/H/thickness engine

The model is editable within **L 160–220 mm, W 80–140 mm, H 30–70 mm and thickness 1.5–2.5 mm** (0.25 mm steps). **60 L/W/H** and **17 thickness** configurations were captured; **75** are used for fitting and validation.

The server geometry has two regimes:

- **A (L < 200)**: fixed 15 mm outer wrap depth.
- **B (L ≥ 200)**: outer depth `clamp(floor(H/2), 15, 20)`. The blank therefore changes size when crossing **L=200** or at H=32, 34, …, 40. This is a real Pacdora step, not rounding.

Within each regime all four layers are affine:

- A: `f = f(180,100,40) + sL·ΔL + sW·ΔW + sH·ΔH`.
- B: `f = f(200,100,40) + sL·ΔL + sW·ΔW + sH·ΔH + sO·(outer−20)`.

L/W/H coefficients are fitted from single-axis samples (`L195`, `W120`, `H60`, `L210`, `L200/W120`, `L200/H60`, `L200/H30`). Thickness uses **independent base templates** at L=180 and L=200 for each of the five values: board and paper compensate differently, so a single straight line did not reproduce the corners. L/W/H slopes are applied to the selected thickness template.

Validation covers **75 samples** (58 L/W/H + 17 thickness), including the 160/80/30 and 220/140/70 corners. **Maximum error: 0.01 mm**, below the 0.5 mm target. Topology is constant: 5/22/4/0 and 25/86/24/38.

The local `rigid366010` engine selects the thickness template, applies L/W/H, composes the four layers and recomputes a 3 mm bleed for the two paper pieces only. Greyboard has no bleed. The editor preview and export run without Pacdora.

## Files and verification

- `troquel-generado.svg` / `.json`: base sheet and per-piece geometry.
- `base/knife-00.json`, `base/details.json`: original responses.
- `base/geometria.json`, `base/manifest.json`: normalized layers, provenance and hashes.
- `muestras/`: initial L, W, H and combined samples.
- `parametricas/`: 60 L/W/H captures and their manifest.
- `espesor/`: 17 thickness captures (1.5–2.5 mm) and their manifest.
- `reglas.json`: two-regime templates for each thickness and per-field coefficients.
- `parametrizar.py`: fits and validates the 75 samples.
- `generar.py`, `validar.py`, `integrar.py`: base generation, validation and catalog integration.
- `generar-parametrico.py` + `bleed-node.cjs`: offline SVG/JSON for any in-range L/W/H/thickness.
- `vista-previa.png`: local raster preview; `icono-3d.jpg`: official Pacdora mockup.
- `exportado-editor.svg`: real SVG downloaded at 180 × 100 × 40 mm.
- `exportado-editor-210x120x50.svg`: real SVG at 210 × 120 × 50 mm and 2 mm.
- `exportado-editor-210x120x50-T2.5.svg`: same box at 2.5 mm.
- `captura-espesor.png`: app screenshot with the thickness selector at 2.5 mm.
- `captura-editor.png`: app screenshot with 210 × 120 × 50 mm.

`validar.py` passes **17 base checks**, including exact translation, per-piece counts, finite values, unique names, no overlaps, valid SVG/XML and the 3 mm paper-only bleed. `parametrizar.py` validates **75 samples** (58 L/W/H + 17 thickness) with a **0.010 mm** maximum error and constant topology. The local app was exercised in Chromium at 210 × 120 × 50 mm: 60 faces, 56 folds, 2 bleed subpaths, out-of-range rejection, and real SVG exports at 180 × 100 × 40 mm (13,362 bytes), 210 × 120 × 50 mm at 2 mm (13,468 bytes) and at 2.5 mm (13,893 bytes). Project tests: **83 passing**, including `parametric-366010.test.cjs` and `thickness-366010.test.cjs`.

## Limits

- Verified range: **L 160–220 mm, W 80–140 mm, H 30–70 mm**. Outside it the editor refuses the value; nothing is extrapolated.
- Material is fixed (greyboard + 0.15 mm paper) and board thickness is limited to **1.5–2.5 mm in 0.25 mm steps**. Other materials and paper thicknesses are not enabled.
- At **L=200** and at the H steps (32, 34, …, 40) the outer depth changes discretely. This is observed server behaviour, not a continuous surface.
- The offline generator needs Node/ClipperLib for bleed; the editor still works and computes bleed in the browser.
- No physical assembly, production tolerance, or AI/PDF/DXF original export was verified.
- Pacdora requires authentication for downloads; the SVG is a vector reconstruction of the received geometry, not the manufacturer’s file.
- Digital equivalence does not prove manufacturability.

## Evidence

- Page and base knife response: `ev_9bbab1a9d4276e5f6454243d88be37c523f6071b25883dbfdd7913a043478f1a`.
- Second REA anchor for the page and base geometry: `ev_8a1f522b2feaaf33ae7d8b02bf6d78896d54af4583da1044013d07d7fba9017e`.
- REA page capture at L=200: `ev_700ae83528d04468565ebaa8c797a41ee7ba549744bc572db355405341c67f77`; the event budget did not retain that variant's body, which is preserved in the CDP matrix.
- **60 L/W/H** captures in `parametricas/manifest.json` and **17 thickness** captures in `espesor/manifest.json`; per-sample error in `validacion-parametrica.json`.
- REA anchors and CDP samples are kept complete; completed captures were not repeated.
