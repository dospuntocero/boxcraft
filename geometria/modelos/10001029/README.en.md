[Español](README.md) · English

# Body lotion box · 10001029

Source: https://www.pacdora.com/es/dielines-detail/body-lotion-box-dieline-10001029

A folding dieline from the `Pair` family was captured, with 13 faces, 76 cut commands, and 12 folds. The initial configuration has manufacturing dimensions of 60 × 45 × 120 mm, 350 g white paperboard, and 0.5 mm thickness. The initial blank measures 222.5 × 235 mm.

## Results

- troquel-base.svg: rendering of the original captured blank, 60 × 45 × 120 mm.
- troquel-generado.svg: local reconstruction, defaulting to 68.58 × 53.34 × 139.7 mm.
- troquel-generado.json: geometry generated offline.
- reglas.json: coefficients and template obtained from 8 training samples.
- validacion-generador.json: comparison with 3 independent responses excluded from fitting.
- muestras/, ajustes/, and validacion/: REA responses and manifests with stages and hashes.

## Run

From /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/10001029/generar.py --length 70 --width 55 --height 140
```

Replaces troquel-generado.svg and troquel-generado.json in this directory. Uses standard Python without dependencies or requests to Pacdora. Dimensions are manufacturing dimensions in mm. Supports L=68.58–76.2, W=45–63.5, and H=120–152.4 with the original material and thickness. The 60 × 45 × 120 mm blank is retained as a capture; that length is outside the generator's range because it belongs to a different branch of automatic values.

## Reconstruction method

Individual samples used L=76.2, W=63.5, and H=152.4 relative to the 60 × 45 × 120 base. L=70 and W=50,55,60 were added to isolate automatic adjustments. Contours were modeled as affine functions of L,W,H and three internal values E,A,AR.

Advanced controls are not exposed. Automatic values are required to reproduce basic-control behavior: in the supported branch E=8 and S=6; inferred formulas A=floor(min(L/2,0.65W)) and AR=max(7,floor(0.15W)) agree with the inspected samples. These are bounded inferences, not recovered original code or proof of every threshold.

Independent checks:

| L × W × H, mm | Numeric fields compared | Result |
| --- | --- | --- |
| 68.58 × 45 × 120 | 784 | Match within 0.000001 units |
| 68.58 × 53.34 × 120 | 784 | Match within 0.000001 units |
| 68.58 × 53.34 × 139.7 | 784 | Match within 0.000001 units |

The three states belong to one independent capture, not three independent sessions. The region bounded by the ranges was not exhaustively checked. Bleed is not generated: its initial fit showed deviations up to 0.0045823 mm and was excluded from the final model, comparison, and output. sizeArrowData annotations, which are not rendered in the SVG, were also excluded.

Arcs use the original fields in SVG A commands. XML syntax was checked, but visual equivalence with the editor and a physical sample were not. The SVG uses inspection colors and is not validated for manufacturing.

## Evidence

- Initial inspection: ev_e3efff917250484126939187e1645d372d2628e3b319ed45df287669f241196f.
- Samples: ev_4372b6a27b21d7713b101585d6645366f184b5b625ed9e15d73b6c30f52f9a8c.
- Adjustments: ev_72b528c47cfcd19649fe1797a2ba81c62a81da3f9359c0ea3a0e0006ccbdc452.
- Independent check: ev_d5b586b9829507684a1c975a9d86fb0e734ef0326bb860329189afdbc5e937ef.

Sample and adjustment captures reported cleanup_incomplete; their retained partial observations were recovered. Recorded actions completed and the responses used are present. The check capture completed but exceeded the transport limit; it was recovered by export without repeating it. These limitations remain part of the interpretation.
