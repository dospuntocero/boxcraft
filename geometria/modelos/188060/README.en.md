[Español](README.md) · English

# Dieline 188060 · Hexagonal box

Source: https://www.pacdora.com/es/dielines-detail/custom-dimensions-polygonal-boxes-hexagonal-dieline-188060

Model **188060**, "Custom dimensions polygonal boxes hexagonal dieline" / "Hexagonal box". Pacdora initial configuration: **100.6 × 40.6 × 181.6 mm** manufacturing, 350 g white paperboard, **0.5 mm** (material 103). Inner dimensions **100 × 40 × 180 mm**; outer **145.2 × 41 × 222.6 mm**.

## Geometry

- **19 faces**: six side panels (FL, F, B, BR, TL, T) with upper and lower flaps.
- **26 folds** and **28 cut commands**.
- Blank: **336.7 × 262.8 mm**.
- No real inner holes: the source layer declares an empty list.
- Cuts, faces, and folds come from Pacdora's `project/knife` response; no geometry was invented.

## Dimensions and modes

Pacdora exposes manufacturing, inner, and outer modes. The local base keeps only the manufacturing configuration; no independent inner/outer offsets were captured for other materials.

The model uses an **experimental L/W/H panel engine** for the original material and thickness. The base geometry is exact; L=110 was validated against the rendered SVG (max error 0.7 mm). W=45 and H=190 were validated with the same map: maximum errors 0.16 mm and 0.00 mm respectively.

## L/W/H engine

The blank is reconstructed by panels: width follows the six side panels and height follows flap-body-flap.

- `totalX = 135.5 + 2L`
- `totalY = 2W + H`
- X breaks: `46`, `46+L`, `76+L`, `106+L`, `106+2L`, `135.5+2L`.
- Y: top flap `0..W`, body `W..W+H`, bottom flap `W+H..2W+H`.
- Corner radii stay fixed.

The local editor was verified at **110 × 45 × 190 mm**, with a **355.5 × 280 mm** blank and all three fields editable. The TR face at L=110 matches; the maximum error over the face set was 0.7 mm. L=110 has 0.70 mm error from the notch position; W/H match within 0.16 mm. The model remains experimental because it has no physical validation.

## Files

- `troquel-generado.svg`: full-scale vector blank.
- `troquel-generado.json`: geometry, extent, counts, provenance.
- `vista-previa.png`: local SVG rasterization (generated, not an official image).
- `base/knife-00.json`: preserved original response.
- `base/geometria.json`: normalized layer used by the generator.
- `generar.py`: reproduces SVG/JSON offline.
- `integrar.py`: catalog entry, thumbnail, and material capability.
- `muestras/`: faces for L=110, W=45, and H=190 with their evidence.
- `validacion.json`: checks and hashes.

From `/Users/fran/Herd/pacdora`:

```sh
python3 geometria/modelos/188060/generar.py
/Users/fran/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3 geometria/modelos/188060/integrar.py
```

## Verification and limitations

- Valid JSON/XML; positive extent.
- 19 faces, 26 folds, 28 cuts; base geometry reproduced unchanged.
- Panel engine: exact base; L=110 validated (max error 0.7 mm); W/H analytical without an independent sample.
- Catalog entry, thumbnail, and the 110 × 45 × 190 mm change checked.
- Minimums, other materials/thicknesses, physical assembly, tolerances, and AI/DXF/PDF export were not verified. Samples L=110, W=45, and H=190 validated against the rendered SVG.
- The thumbnail was generated from local geometry; it is not presented as an official Pacdora image.

## Evidence

- Page and initial dimensions: `ev_a75c36365ad2f0f766128a5055d1614f001124e94e80b155d14724abf291b669`.
- Base geometry response: `ev_0c2b9e45f786350aba1b5f6dc8e284902db9d8c40694ea89a7f9010bc4f8ebbc`.
- 110 × 45 × 190 editor change: `ev_f86e32d44ae650592412371043aced9524f23298655a6d2a1447849f962fefb3`.
