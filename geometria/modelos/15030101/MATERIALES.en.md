[Español](MATERIALES.md) · English

# Coverage matrix 15030101

Manufacturing configuration: 150 × 150 × 50 mm. Available options checked in the selector and through geometric responses. Custom thicknesses: discrete samples; no continuous interval is enabled.

| Material | ID | Verified thicknesses (mm) | Status |
|---|---:|---|---|
| White paperboard 350g (0.5mm) | 103 | 0.5 | Complete geometries and local integration |
| White paperboard 210g (0.27mm) | 100 | 0.27 | Complete geometries and local integration |
| White paperboard 250g (0.35mm) | 101 | 0.35 | Complete geometries and local integration |
| White paperboard 300g (0.42mm) | 102 | 0.42 | Complete geometries and local integration |
| Custom white paperboard | 8 | 0.2, 0.35, 0.5 | Complete geometries and local integration |
| Kraft paperboard 190g (0.26mm) | 108 | 0.26 | Complete geometries and local integration |
| Kraft paperboard 250g (0.33mm) | 109 | 0.33 | Complete geometries and local integration |
| Kraft paperboard 350g (0.46mm) | 110 | 0.46 | Complete geometries and local integration |
| Custom kraft paperboard | 7 | 0.2, 0.35, 0.5 | Complete geometries and local integration |
| Coated paper 200g (0.2mm) | 47 | 0.2 | Complete geometries and local integration |
| Coated paper 350g (0.32mm) | 42 | 0.32 | Complete geometries and local integration |
| Custom coated paper | 153 | 0.2, 0.35, 0.5 | Complete geometries and local integration |

Options disabled at these dimensions: 400 g white paperboard (0.55 mm), 120 g kraft (0.14 mm), and all corrugated materials listed by the selector. This does not establish physical incompatibility outside this configuration.

Custom materials were checked at 0.2 / 0.35 / 0.5 mm. The catalog may declare wider ranges, but the limits response for this box and dimensions returns 0.2–0.5 mm. The editing step was not established.

## Other dimensional configurations

Original material ID 103, 0.5 mm; available as exact cases through the CLI generator:

- 160 × 150 × 50 mm — `parametricas/knife-02.json`.
- 150 × 160 × 50 mm — `parametricas/knife-04.json`.
- 150 × 150 × 60 mm — `parametricas/knife-06.json`.
- 155 × 150 × 60 mm — `parametricas/knife-07.json`.
- 155 × 155 × 60 mm — `parametricas/knife-08.json`.
- 155 × 150 × 50 mm — `independiente/knife-02.json`.
- 155 × 155 × 50 mm — `independiente/knife-03.json`.
- 155 × 155 × 55 mm — `independiente/knife-04.json`.

Dimensions and thicknesses are not interpolated. The affine dimension fit failed and remains disabled; see `validacion-parametrizacion.json`.
