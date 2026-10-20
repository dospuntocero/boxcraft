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

The model is **fixed** at 100.6 × 40.6 × 181.6 mm and 0.5 mm. No parametric engine was enabled: L/W/H variations and the hexagonal closure topology were not tested.

## Files

- `troquel-generado.svg`: full-scale vector blank.
- `troquel-generado.json`: geometry, extent, counts, provenance.
- `vista-previa.png`: local SVG rasterization (generated, not an official image).
- `base/knife-00.json`: preserved original response.
- `base/geometria.json`: normalized layer used by the generator.
- `generar.py`: reproduces SVG/JSON offline.
- `integrar.py`: catalog entry, thumbnail, and material capability.
- `validacion.json`: checks and hashes.

From `/Users/fran/Herd/pacdora`:

```sh
python3 geometria/modelos/188060/generar.py
/Users/fran/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3 geometria/modelos/188060/integrar.py
```

## Verification and limitations

- Valid JSON/XML; positive extent.
- 19 faces, 26 folds, 28 cuts; base geometry reproduced unchanged.
- Catalog entry and thumbnail checked.
- Minimums, other materials/thicknesses, physical assembly, tolerances, and AI/DXF/PDF export were not verified.
- The thumbnail was generated from local geometry; it is not presented as an official Pacdora image.

## Evidence

- Page and initial dimensions: `ev_a75c36365ad2f0f766128a5055d1614f001124e94e80b155d14724abf291b669`.
- Base geometry response: `ev_0c2b9e45f786350aba1b5f6dc8e284902db9d8c40694ea89a7f9010bc4f8ebbc`.
