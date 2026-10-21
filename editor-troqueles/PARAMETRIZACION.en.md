[Español](PARAMETRIZACION.md) · English

# Parameterization of the eight previously fixed-size models

## Current parameterization status (2026-10-20)

A model is marked **verified** only when its engine reproduces the reference captures exactly and independent holdouts pass. The status is derived from `geometria/modelos/<code>/validacion-parametrica.json`, never written by hand.

| Model | Status | Evidence | Remaining work |
|---|---|---|---|
| 187000 | **Digitally verified** | 7 captures; cut 0.00007 mm; faces 0.00003 mm | Physical validation; extra `rt`/`y0` boundaries |
| 366010 | **Digitally verified** | 58 captures; 0.000 mm outside `/bleeds`; A/B regimes | Physical validation; wider range |
| 112047 | Experimental | 138 dense captures | `M` and `K3` exact; 1D W non-linearity with rounding notches at 48.2–48.6 and 54.4–54.6; closed formula remains |
| 12109002 | Experimental | 3 holdouts up to 1.57 mm | Step/breakpoint detection |
| 112310 | Experimental | 2 holdouts up to 2.50 mm | `H1,HT,K1,K3,SP,MR` formulas |
| 10001006 | **Digitally verified** | 97 captures; 0.000 mm; compiled rules over `A/AR/C/CR/E/NX/NY` | Physical validation |
| 10002003 | **Digitally verified** | 49 captures; 0.000 mm; compiled rules over `A/AR/C/CR/G/L1/NX/NY` | Physical validation |
| 180370 | Experimental | 3 holdouts up to 0.54 mm | Arc formulas and `D1/L1/L2/W1` |
| 180320 | Experimental | 150 captures; most parameters with exact formulas | Geometry is not affine in those parameters across the dense L sweep; the non-linear regime remains |
| 15030101 | Experimental | 3.88 mm; `enabled=false` | Small topology and exact large rule |
| 102010 | Experimental | 1.82 mm; only 80-cut topology | 92-cut topology and exact rule |
| 188060 | Experimental | L 0.70 mm | Exact notch and independent W/H |

Capture and fitting infrastructure lives in `investigacion/parametrico/`. New captures are stored per model and do not overwrite historical samples.

All eight models now have local generators. Selection, dimension fields, mm/in conversion, layers, and SVG use the same generated geometry. Material and thickness remain fixed.

| Model | New axes | Method | Scope |
|---|---|---|---|
| 150010 · Mailer | L/W/H | Per-coordinate rules derived from dimension variations | Two additional samples match all 1,297 numeric fields; observed range 315–330 / 202–212 / 62–66 mm |
| 112047 · Gable and cord | L/W/H | Parameter rules + 1D W table | Experimental; parameters exact, but the W non-linearity has no closed formula and 1/2 mm tables miss 0.1 mm |
| 12109002 · Cake | L/W/H | Empirical per-coordinate rules | Experimental; maximum difference 1.574 |
| 112310 · Handle and bottom | L/W/H | Empirical per-coordinate rules | Experimental; maximum difference 2.5 |
| 10001006 · Tuck flaps | L/W/H | Compiled rules over internal parameters | Digitally verified; 97 captures, 0.000 mm error |
| 10002003 · Hanging | L/W/H | Compiled rules over internal parameters | Digitally verified; 49 captures, 0.000 mm error |
| 180370 · French fries | L/W/H | Empirical per-coordinate rules preserving arcs | Experimental; maximum difference 0.536 |
| 180320 · Sandwich | L/W | Panel and diagonal transformation | Experimental; 150 captures and most parameter formulas, but the non-linear regime remains |

These differences include every numeric field in the blank; they are not physical manufacturing tolerances. Coordinate and length fields are in mm. Full values are in `validacion-parametrizacion.json`. A failed comparison is not presented as a passed validation.

Engines that are still experimental adapt geometry but do not reproduce every automatic adjustment and rounding operation of the original service. They are marked in the catalog and dimension panel. 187000, 366010, 10002003 and 10001006 are digitally verified; the rest keep observed ranges and warnings. A physical sample is needed to confirm assembly.

The three previously editable models retain their rules: 200010 and 10001029 support L/W/H; 102010 supports L/W/H with L <= 2W. The sandwich box retains its two original parameters without introducing a fictitious height. 102010 still lacks the 92-cut topology.

## Local verification

`node comprobar-parametrizacion.cjs` checks:

- Identity with the original geometry at the initial dimensions.
- Changes to cuts and folds when each supported axis varies.
- Preservation of face and opening counts.
- Endpoint combinations for models with independent ranges, and exact material-boundary cases for FEFCO, with finite dimensions, positive extent, and nonnegative radii.
- Rejection of out-of-range dimensions and nonnumeric values.

Results are saved in `comprobacion-motores.json`. These checks do not establish absence of intersections, closure fit, 3D folding, or full equivalence with the reference system.

## Evidence and limitations

Original samples are in `../geometria/modelos/<código>/parametricas/`, with manifests of dimensions, hashes, and stages. REA evidence:

- 150010: `ev_a18825c5a61e966696c553ba3647c52a8389a9bac182d10c9d2af4daad5a49bb`.
- 112047: `ev_cd90c934ef31fc36ebf2c28a9b1ea358996b3729433a3a73e679f52fc3f296a3`.
- 12109002: `ev_602b037b5204b8d18330691126ae1490b9ca509157ab98d0b3f27c281d6ec51d`.
- 112310: `ev_3d3f8c25ee3fcf3f0e6c3ce21115fc2c3d0e79b2ae3c7c53c6b47596e35185bd`.
- 10002003: `ev_da1553065cabada5c63e4a89bc115d334d059ff994b3da064b4b33ffde15041f`.
- 180370: `ev_9f15a6df8c23b64cf0650dd5bdfaa650770c22ebe822a4de8e305e2fccc72385`.

These captures returned `cleanup_incomplete`: completed actions and geometric responses were retained, but successful browser closure was not established. Variation captures for 10001006 and 180320 did not complete. Their rules were designed from the original blank's panels and folds; they are not attributed to the original code.

`parametrizar-modelos.py` integrates rules and metadata into the self-contained JSON used by the browser. `preparar-datos.py` reapplies this integration when original data are regenerated. The published editor uses only its local data.

## FEFCO 200010 material width

The configured physical limit is 1,200 mm for the unfolded blank's `totalX`, in the displayed orientation. Automatic rotation is not applied. The observed relationship is `totalX = 44 + 2L + 2W`; form maxima are recalculated using the other dimension. Height has a 20.6 mm minimum and no configured material-length maximum. Minimums L=30 and W=24 mm are retained. The generator rejects any blank exceeding 1,200 mm and preserves the last valid geometry.

Initial editor dimensions for this material are 434 × 144 × 278 mm; the original captured dimensions remain separate for empirical rules and identity tests. The expanded-range control is not shown for FEFCO because its limits depend on material width. Manufacturing limits and empirical verification ranges are separate concepts.

## Sheet size for box 10001029

User-specified minimums: L=15, W=10.6, H=15.6 mm. The complete dieline must fit 1,000 × 700 mm, or 700 × 1,000 mm when rotated. The engine validates both dimensions and the panel shows the fitting orientation. Each field's maximum is recalculated while retaining the other dimensions, using the blank-extent rules. The SVG retains the canvas orientation; it may be rotated when placed on the sheet. Ranges checked against captures remain separate from these physical limits.

## Sheet size for box 102010

Supplied reference minimums: L=15, W=10.6, H=20.6 mm; sheet 1,000 × 700 mm, rotation allowed. Only H remains active: L/W changes can alter snap-lock topology, and a complete rule is unavailable. L/W minimums are recorded and displayed as references next to fixed fields without pretending they are editable. At L=120.6 and W=60.6 mm, the maximum height fitting the sheet is 878.85 mm with the blank rotated. Minimum height, sheet boundary, and rejection of fixed-axis changes are checked.

## Additional sheet limits

| Model | Minimum L × W × H (mm) | Sheet (mm) |
|---|---|---|
| 150010 | 20 × 22 × 17.6 | 1,000 × 700 |
| 112047 | 30 × 30 × 30.6 | 1,000 × 700 |
| 12109002 | 30 × 30 × 30.6 | 1,000 × 700 |
| 112310 | 40 × 40 × 41 | 1,200 × 2,300 |
| 10001006 | 15 × 10.6 × 15.6 | 1,000 × 700 |

A 90° rotation is allowed. Field limits are recalculated from the other dimensions; the engine checks both blank dimensions before accepting changes. For 12109002, initial editor dimensions are 200 × 140 × 120 mm: the resulting 609.13 × 742.18 mm blank fits when rotated. Its original captured geometry remains separate because it does not fit the new sheet. These material limits replace arbitrary exploration ranges; they do not extend the validation of the geometric reconstruction.
