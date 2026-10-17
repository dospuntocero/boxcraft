[Español](MATERIALES.md) · English

# Materials and thicknesses

The application displays only material, thickness, and dimension combinations with available geometry. Materials without a valid combination for the current dimensions and size mode are hidden. When only one material remains, the selector is hidden and its name appears next to the thickness.

Thickness uses discrete observed values and depends on the material. New geometries are exact captures with their own internal and external allowances; thicknesses are neither interpolated nor scaled. Previous parametric editing is retained for the original material and thickness. New combinations have fixed dimensions, and the interface states this scope.

## Additional geometry coverage

| Model | Additional observed materials | Additional material and thickness combinations |
|---|---:|---:|
| 200010 — FEFCO shipping box | 1 | 2 |
| 10001029 — Lotion box | 7 | 7 |
| 102010 — Snap-lock bottom box | 1 | 8 |
| 150010 — Mailer box with lid | 9 | 16 |
| 112047 — Gable box with cord | 7 | 7 |
| 12109002 — Cake box | 0 | 0 |
| 112310 — Box with handle and bottom closure | 9 | 9 |
| 10001006 — Tuck-end carton | 2 | 6 |
| 10002003 — Hanging carton | 2 | 3 |
| 180370 — French fries carton | 2 | 3 |
| 180320 — Sandwich box with window | 2 | 3 |

## Review limitations

Box 12109002 retains its original material: alternatives were not fully verified. The reference source returned HTTP 403 during captures and left controls disabled. Continuous thickness ranges and unrestricted dimension editing for new materials also remain unvalidated. A hidden material means the application has no enabled configuration; it does not establish physical incompatibility at every possible size.

Full responses and research are retained locally. Each additional geometry includes a capture reference (a REA identifier when available) and the response's SHA-256. Tests cover actual path changes, limits, conversions, and rejection of combinations outside checked dimensions.
