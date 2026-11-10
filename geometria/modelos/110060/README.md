# Troquel 110060 · Caja para baraja (PlayingCardBox)

Fuente: https://www.pacdora.com/es/dielines-detail/custom-dimensions-tuck-end-box-variations-dieline-110060

Identidad verificada: `cate_no` **110060**, código interno **PlayingCardBox**, nombre original **扑克牌卡盒** (caja para baraja). La página se titula “Custom Dimensions Tuck End Boxes Double Tray Dieline 100010”, pero la respuesta y el catálogo identifican el modelo como 110060.

## Medidas iniciales

| Modo | L | W | H |
|---|---|---|---|
| Interior (`size`) | 60 | 20 | 90 |
| Manufactura (`knifeSize`) | **61,6** | **20,6** | **91,6** |
| Exterior (`outSize`) | 62 | 21 | 92 |

Material: **cartón blanco 350 g de 0,5 mm** (science 103). Plano de **101,8 × 236,15 mm**, con **13 caras, 12 pliegues, 66 comandos de corte y 0 aberturas**. Longitud de pliegue calculada 674,3387 mm (declarada 674,34); longitud de corte declarada 884,21 mm. Sin sangría incluida en la reconstrucción.

## Archivos y uso

- `troquel-generado.svg`: caras coloreadas, cortes rojos y pliegues azules discontinuos.
- `troquel-generado.json`: capa `traditional`, procedencia y medidas.
- `vista-previa.png`: render del SVG revisado visualmente.
- `generar.py`: reproduce SVG y JSON sin red.
- `validar.py`: comprueba la salida y escribe `validacion.json`.
- `base/knife-00.json`, `base/manifest.json`: respuesta inicial y procedencia.
- `parametrico/`: 101 capturas de barridos L/W/H con manifiesto y SHA-256.
- `reglas-parametricas.json`, `validacion-parametrica.json`: motor compilado y su informe.
- `compilar-reglas.py`, `integrar.py`: recompilación y alta reproducible en el editor.
- `icono.jpg`, `icono.manifest.json`: miniatura oficial y su identidad.

Desde la raíz:

```sh
python3 geometria/modelos/110060/generar.py
python3 geometria/modelos/110060/validar.py
```

## Estructura del plano

| Cara | Tamaño (mm) | Papel observado |
|---|---|---|
| B | 61,6 × 20,6 | fondo |
| H | 61,6 × 91,6 | frontal |
| F | 61,6 × 91,1 | trasera, unida por B |
| FR / FL | 20,1 × 91,1 | laterales del frontal |
| HT | 61,6 × 19,85 | solapa superior |
| HT1 | 61,6 × 13 | pestaña de cierre superior |
| HL / HR | 20,1 × 91,6 | laterales traseros |
| HLT / HRT | 20,1 × 17 | pestañas superiores |
| HLB / HRB | 20,1 × 14 | pestañas inferiores |

Pliegues: `B_H`, `B_F`, `H_HT`, `H_HR`, `H_HL`, `F_FR`, `F_FL`, `HT_HT1`, `HL_HLB`, `HL_HLT`, `HR_HRT`, `HR_HRB`. La topología (13/12/66/0) se mantuvo en las 101 capturas, desde 20,6 × 15,6 × 20,6 hasta 150 × 50 × 200 mm.

## Materiales y espesor

La respuesta declara un único material (`science` 103, 0,5 mm) con `can_set = 0` y `min_thickness = max_thickness = 0,5`. El selector de la página muestra cuatro familias (cartulina blanca, kraft, papel arte y cartón corrugado), pero al elegir “Cartulina blanca” no cambia ni el material ni el espesor ni se emite una nueva respuesta: la geometría permanece en 103/0,5. Por eso el motor local queda limitado a ese material. No se probaron otras familias como si estuvieran disponibles.

## Límites observados

- Límites de la interfaz: L 20–2000, W 15–2000, H 20–2000 mm.
- Mínimos efectivos de manufactura: **L 20,6, W 15,6, H 20,6 mm**; por debajo, Pacdora ajusta al mínimo.
- Rango capturado: L 20–150, W 15,6–50, H 20,6–200 mm.
- Rango habilitado en el editor: **L 30–120, W 20–50, H 30–200 mm**.
- Modo de medida: dimensiones de manufactura. Los modos interior/exterior usan las compensaciones de la respuesta base; no se capturaron geometrías separadas para esos modos.

## Parámetros internos

En el rango L ≥ 30 mm, los parámetros observados se explican exactamente (81 capturas dentro del rango habilitado) por:

| Parámetro | Regla observada |
|---|---|
| `C` / `CR` | 10/5 para L < 40; 11/6 para L < 60; 13/7 para L < 100; 15/8 para L < 150; 20/10 desde 150 |
| `E` | 3 si L < 28; 4 si L < 36; 5 si L < 44; 6 si L < 65; 8 si L < 150; 11 desde 150. Con W > 30, mínimo 6 |
| `S` | 4 hasta L < 65; 6 desde 65; 9 desde 150 (ausente por debajo de L 30) |
| `N` | `min(30, floor(L/2), max(10, round(2W/3)))` |
| `A` | `min(floor((L−1)/2), floor((ceil(W) + C + 0,5)/2 + 0,5))` |
| `AR` | 2 si W ≤ 30; `floor((W + C)/8)` si W > 30 |
| `ATT` | 0 si W < 20; 13 si W ≥ 20 |
| `AX` / `AXX` / `AS` | 2,5 / 3,5 / 2,5 si W < 30; 3,5 / 4,5 / 3,5 si W ≥ 30 |
| `NX` / `NY` | 2 si W ≤ 30; 3 si W > 30 |
| `R1` | 7 (L 20), 8 (L 25), 9 (L 26–28), 10 (L 29–149), 15 desde 150 |

Hallazgos que corrigen supuestos habituales:

- `N` no depende solo de W: también se limita por `floor(L/2)` y por 30.
- `A` usa `ceil(W)` y el valor de `C`, no una fórmula fija por bandas.
- `AR` usa `C`, por lo que cambia con L aunque W sea la misma.
- `ATT` conmuta en W = 20 y `AX`/`NX` en W = 30, pero con umbrales distintos (`AX` desde 30; `NX` desde 31).
- Con H muy pequeño (20,6 mm) aparecen acoplamientos adicionales: `C` baja a 5 y `R1` a 4. Por eso las fórmulas anteriores se declaran para L ≥ 30 y H ≥ 30.

## Motor verificado

La geometría es **afín por tramos de anchura** en los parámetros anteriores. Se comprobó exactitud en **81 capturas dentro del rango habilitado**, con 19 holdouts y error máximo **1,5 × 10⁻¹² mm**. Regímenes:

- `W = 20`: 15 muestras.
- `21 ≤ W ≤ 29`: 34 muestras.
- `W = 30`: 16 muestras.
- `W ≥ 31`: 16 muestras.

El motor se integró en `editor-troqueles` como `compiled` y se probó en la interfaz: medidas **120 × 50 × 200 mm**, plano **219 × 513,75 mm**, 4 cajas por pliego y sin errores de JavaScript.

No se habilitan W < 20 ni H < 30 porque el acoplamiento de `C`, `E` y `R1` con alturas pequeñas no está cerrado. El material sigue fijado a 0,5 mm.

## Verificación

`validar.py` y `validacion.json` comprueban:

- JSON válido y 687 campos numéricos idénticos a la respuesta base.
- SVG con 13 caras y 12 pliegues; 0 aberturas.
- Longitud de pliegue 674,338675 mm frente a 674,34 declarada.
- Vista previa rasterizada e inspeccionada.
- Motor compilado: 81 capturas, 19 holdouts y error 1,5 × 10⁻¹² mm (informe en `validacion-parametrica.json`).

No se validó armado físico, tolerancias, sangría de producción ni exportaciones AI/DXF/PDF. En la interfaz se comprobó la generación y el ajuste al pliego, no la descarga AI/DXF. La equivalencia digital no acredita aptitud de fabricación.

## Evidencia

- Respuesta base: `base/knife-00.json`, SHA-256 `905f5ddb8a4ce3e9889fbbdfefddfb5a5a3eb45e25995124c7f4d80edb6fcbf5`.
- Capturas: `parametrico/` con manifiesto de 101 archivos y SHA-256 por archivo.
- Icono oficial: `modeCate.image` (`https://yun.baoxiaohe.com/render/20220127/17279050001.jpg`), SHA-256 `5a19a605408e2da478820ecd98e6927d1378852e263015a02ef479c794f33bb1`, 1920 × 1920.
- Capturas realizadas con Playwright el 2026-11-09; no hay bundle REA para este modelo.
