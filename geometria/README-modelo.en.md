[Español](README-modelo.md) · English

# Local FEFCO 0201 generator

Run from /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelo-parametrico.py --length 457.2 --width 228.6 --height 279.4
```

Produces troquel-generado.svg and troquel-generado.json in this directory. Dimensions are manufacturing dimensions in millimeters. Runs offline without external libraries. Each run rebuilds the rules from local captures and checks the independent combination before generating the file. Previous output files are replaced.

Supported ranges: length 434–508 mm, width 214–254 mm, height 278–304.8 mm. Fixed material: B-flute, 3 mm thick, OF=2, R=3, G=45, and GT=15. Other thicknesses and manual changes to advanced parameters are not represented.

This is an empirical affine model: variations observed in three samples, one per axis, are applied to each numeric geometry field. It is not Pacdora's original code. The independent 457.2 × 228.6 × 279.4 mm combination is not used to fit the rules and validates 822 numeric fields. Only bleed differences below 0.001 mm are tolerated; other numeric differences must be within 0.000001 units. validacion-modelo.json records the full result.

## Summary of observed rules

With manufacturing L, W, and H, and the fixed configuration above:

- Blank extent: X=45+2L+2W−1; Y=H+W+2.
- Flaps: F=W/2+1; F1=W/2+3.
- Main faces: widths L, W, L, and W−1, in that order.
- Glue tab: width 45; metadata height H−4.
- Internal dimensions: L−4, W−4, H−8.
- External dimensions: L+2, W+2, H+4.

These relationships agree with the inspected samples. They do not establish validity outside the range, with another material, or after changing advanced parameters. Contours and arcs are generated from per-field coefficients retained in reglas-parametricas.json.

## Files and provenance

- experimentos/: individual L, W, H, and thickness samples, plus a manifest with stages, hashes, and statuses.
- validacion-parametrica/: independent check samples; the final one is knife-04.json.
- reglas-parametricas.json: template and coefficients learned exclusively from individual dimension samples.
- modelo-parametrico.py: fitting, validation, and SVG/JSON output.

Sample evidence: ev_70c78216d8ca163ef7f939d0aed16da00ebc22365fb62afe71f36c34f435b46a. Check evidence: ev_e71c55c541c5bd0970f35ad5e7d9e8acfe58b97439dd0975c40c6f3260455e65. Both captures reported cleanup_incomplete: the partial record retains all completed actions and the actual responses used, but does not establish successful browser closure. Their lifecycle is not presented as complete.

The advanced tab observed in ev_f5a6bc57aa5f99256bd933eac5f9a8ebfa1cfaf1ca8187ee3166b635309300bf requires “Upgrade to Business” (“Actualizar a Negocios”). Those parameters were not changed and no attempt was made to bypass the restriction.

The SVG uses inspection colors for faces, cuts, and folds. Bleed is not exported, arcs were not visually compared, and the result is not validated for manufacturing. Extending the engine requires additional combinations, authorized parameter changes, visual verification, and a physical sample.
