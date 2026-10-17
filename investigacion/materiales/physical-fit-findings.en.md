[Original](physical-fit-findings.md) · English

# Physical thickness fit audit: 150010

Source: REA saved responses in `ev_525240b360f6d9a8cfa055b66b964b4594d53f5abdac7ac469b0d5d5a8d28510/knife-*.json`.
Actual thickness is `data.layer.traditional.thickness`; `data.science` remains the original material record. These responses have fixed manufacturing dimensions `knifeSize = 315 x 202 x 62`, while interior dimensions and allowances vary.

| thickness | size.id | size.ed | layer totalX | layer totalY | cut commands |
|---:|---:|---:|---:|---:|---:|
|0.8|0.5|3|566|589.8|105|
|1.1|0.5|3.5|573|590.1|89|
|1.5|1|5|576|590|89|
|1.7|1|5|577|590.2|89|
|2|1|6|579|590|89|
|3|2|9|585|590|89|
|5|3|15|597|590|89|

At 0.8 mm topology changes relative to all other samples. Face H, HL, HR, L and R contain changed command types and/or command counts. Faces and folds are also ordered differently; canonicalize faces by name before comparisons. Interpolating arrays by index is invalid.

For common topology 1.1–5 mm, 662 numeric face-coordinate/metadata paths have identical structure. Leave-one-sample-out regressions:

| features | maximum heldout numeric error mm |
|---|---:|
|1,t|1.935672515|
|1,t,size.id|3.450657895|
|1,t,size.id,size.ed|4.437500000|

Errors include actual face path points and radii, not arrow labels. Even linear allowance-aware coordinate transforms do not reproduce the available samples. Floor-derived features are visibly required: FT width is exactly 315 - 2t and F width is 315 - 2ed; FTL width jumps nonmonotonically 54,53,52,52,53,51,48 across these thicknesses. FTL height is 60.25,59.75,58.5,58.5,59,57,54. Adding sufficient floor features to interpolate seven samples would overfit and leave no independent validation for all regimes.

## Safe minimum

Keep exact samples at their measured manufacturing dimensions and thicknesses as a lookup, with geometry/metadata copied from the source. This permits only the seven measured thickness presets at 315 x 202 x 62. Reuse existing dimension solvers only at their validated original material/thickness. Do not combine an independently derived dimension solver with thickness offsets without heldout mixed dimension-and-thickness responses.

Continuous custom thickness requires source formulas or additional independent responses around rounding thresholds and topology boundaries; server allowance conversion must also be established. Existing `engines.js` physical guard is appropriately conservative until such a solver is validated. No approximate scaling can be claimed exact.

Reproducer: `python3 material-research/fit-physical.py`. Script currently excludes 0.8 mm from regression because of topology differences and canonicalizes faces by name.
