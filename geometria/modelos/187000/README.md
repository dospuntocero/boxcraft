# Troquel 187000 · Caja almohada (pillow box)

Fuente: https://www.pacdora.com/es/dielines-detail/custom-pillow-box-dieline-187000

Modelo **187000**, «Custom pillow box dieline» / «Caja almohada», categoría **Caja Poligonal**. La página entrega como configuración inicial **118 × 70 × 25 mm** de manufactura, cartón blanco 350 g de **0,5 mm** (material 103). La imagen oficial del troquel se descargó del CDN y se conserva en `troquel-oficial.png` (905 × 1000 px): incluye 5 mm de sangría por lado, por eso su extensión es 153,5 × 165 mm frente al corte de 143 × 155 mm.

## Medidas, modos y edición

- Ejes de manufactura: **L = 118 mm** (longitud), **W = 70 mm** (anchura), **H = 25 mm** (altura).
- El editor muestra «Dimensiones de manufactura». Los modos **Interior** y **Exterior** están deshabilitados: no se capturaron conversiones verificadas para este modelo.
- El pliego indicado por el usuario es **330 × 480 mm**. El corte inicial mide **143,000 × 155,000 mm**; con 3 mm de sangría el editor calcula **6 cajas por pliego** (2 columnas × 3 filas, rotado 90°). La ficha original de Pacdora mostraba 4 con 5 mm de sangría.
- El modelo **es editable** mediante el motor local `pillow187000` (ver abajo), dentro de estos límites:
  - **L:** 20 – 323,33 mm.
  - **W:** 20 – 231 mm.
  - **H:** 6,67 – 200 mm, siempre **H < W** (el máximo efectivo depende de W).
  - El corte debe caber en **330 × 480 mm** (`L + H ≤ 330`, `2W + 18 ≤ 480`). El editor admite rotación del plano.

## Medidas mínimas observadas

La página no publica una tabla de mínimos. Se probó la interfaz real y se registró el valor **efectivo** que queda tras el ajuste automático:

| Entrada | Resultado efectivo | Observación |
|---|---|---|
| 30 × 30 × 15 mm | **30 × 30 × 10 mm** | Aceptado; la altura se ajusta a 10 mm y aparece «Las medidas que defina podrían causar errores de impresión». |
| 10 × 10 × 5 mm | **20 × 20 × 6,67 mm** | Los tres valores se elevan; misma advertencia. |
| 118 × 70 × 5 mm | **118 × 70 × 25 mm** | La altura de 5 mm se rechaza y vuelve al valor inicial. |

Conclusión acotada: el mínimo **efectivo** más pequeño observado es **20 × 20 × 6,67 mm**, y por debajo de **30 × 30 × 10 mm** la propia página advierte riesgo de impresión. No es un mínimo independiente por eje: la altura está acoplada a las demás medidas y 5 mm de altura se rechaza en 118 × 70. El catálogo usa `minimumDims = 20 × 20 × 6,67 mm` como cota informativa y `printMinimumDims = 30 × 30 × 10 mm` como mínimo recomendado de impresión.

## Motor paramétrico `pillow187000`

El motor reconstruye el corte, las siete caras y los pliegues a partir de **L, W y H**. Se basa en la construcción geométrica observada en el SVG azul de recorte, no en escalado uniforme:

| Elemento | Regla |
|---|---|
| Origen lateral | `x0 = H/2` |
| Altura de pestaña superior | `y0 = W >= 100 ? 18 : 15` |
| Radio de los arcos principales | `R = (W² + H²) / (4H)` |
| Radio de la muesca de cierre | `rt = clamp(round(((L+H)/25)·2)/2, 6, 7.5)` |
| Semiancho de la muesca | `d = R − √(R² − rt²)` |
| Corte total | `totalX = L + H`, `totalY = 2W + y0` |
| Pestaña superior | borde entre `x0 ± i`, con `i = −a + √(R² − (W/2 − y0)²)` y `a = R − H/2` |

La muesca de cierre se calcula como un semicírculo de radio `rt` sobre la línea `x = x0 + L + H/2 − d` (derecha) y su simétrica izquierda. Los arcos de transición son el mismo arco `R` del cuerpo, por lo que el corte y los pliegues quedan alineados.

### Validación del motor

Se capturaron **7 configuraciones** del editor de Pacdora y se compararon comando por comando (M/L/A) contra el motor:

| L × W × H (mm) | Corte (mm) | Uso |
|---|---|---|
| 118 × 70 × 25 | 143 × 155 | Base exacta |
| 160 × 70 × 25 | 185 × 155 | Variación de L |
| 118 × 100 × 25 | 143 × 218 | Variación de W |
| 118 × 70 × 30 | 148 × 155 | Variación de H |
| 150 × 90 × 40 | 190 × 195 | Combinación |
| 118 × 95 × 25 | 143 × 205 | Frontera de W |
| 118 × 118 × 25 | 143 × 254 | W ≥ 100 y pestaña de 18 mm |

Resultados: error máximo del **corte 0,00007 mm** y de las **caras 0,00003 mm**. La prueba reproducible está en `editor-troqueles/tests/parametric-187000.test.cjs` y usa `muestras.json`.

En el editor local se comprobó el cambio **160 × 70 × 25 → corte 185 × 155 mm**, con 7 caras y 6 pliegues; la cota de altura desapareció del lienzo porque no es una medida de panel, y se edita en el panel «Dimensions».

### Estado

El motor es **experimental**: reproduce digitalmente las siete muestras, pero no se verificó con una muestra física ni contra una exportación DXF/PDF de Pacdora. La regla de `y0` (15/18 mm) y la de `rt` (pasos de 0,5 mm) son las partes con menor cobertura; cualquier combinación fuera de las siete muestras debe comprobarse antes de fabricar.

## Geometría del modelo base

La geometría base se extrajo del SVG azul de recorte que el editor de Pacdora dibuja en el DOM para 118 × 70 × 25 mm. No es el JSON `knife` del servidor (la API `project/knife?id=9351` responde `code: 401` sin sesión).

- **7 caras**: `H`, `HL`, `HT`, `HB`, `F`, `FT`, `FB`.
- **6 pliegues**: dos líneas horizontales (y = 15 y y = 85) y cuatro arcos de plegado en los laterales.
- **0 orificios**.
- Contorno de corte: **143,000 × 155,000 mm**; coordenadas originales x ∈ [0, 143], y ∈ [0, 155]. La imagen oficial añade 5 mm de sangría por lado: 153,5 × 165 mm.
- La pestaña superior mide 15 mm (18 mm para W ≥ 100). No hay faldón inferior de producto: el tramo de 10 mm de la imagen oficial es sangría.

## Pliego y límites máximos

Con el corte `totalX = L + H` y `totalY = 2W + y0`:

- **L + H ≤ 330 mm** (ancho del pliego).
- **W ≤ 231 mm** (2W + 18 ≤ 480).
- **H ≤ 200 mm** y **H < W** por geometría.
- Ejemplos: H = 25 → L ≤ 305; H = 40 → L ≤ 290; H = 60 → L ≤ 270; H = 80 → L ≤ 250.

Son cotas geométricas; no incluyen separaciones, márgenes de máquina ni nesting. El editor rechaza cualquier corte que no quepa en 330 × 480, incluso girado, y muestra el número de cajas por pliego con 3 mm de sangría.

## Archivos

- `troquel-generado.svg`: plano vectorial del modelo base, con caras blancas, corte azul y pliegues rojos discontinuos. Escala real en mm.
- `troquel-generado.json`: geometría base, extensión, conteos, motor, procedencia y límites.
- `vista-previa.png`: rasterización local del SVG base (577 × 622 px), revisada visualmente.
- `editor-187000.png`: captura del editor local con el modelo editable.
- `editor-187000-90mm.png`: comprobación de que 90 × 70 × 25 genera un corte de 115 × 155 mm.
- `troquel-oficial.png`: imagen oficial del troquel descargada de Pacdora (905 × 1000 px).
- `icono-3d.png`: render 3D oficial del modelo (1600 × 1216 px), usado como miniatura del catálogo.
- `base/geometria-dom.json`: paths de corte, caras y pliegues extraídos del DOM, con dimensiones y material.
- `muestras.json`: siete cortes y caras de referencia para la prueba del motor.
- `generar.py`: reproduce el SVG/JSON base sin red.
- `integrar.py`: da de alta el modelo, la miniatura y la capacidad de material en el editor.
- `validacion.json`: comprobaciones, hashes y límites.

El motor vive en `editor-troqueles/dist/engines.js` (`buildPillow187000`). `editor-troqueles/dist/bleed.js` usa `bleedFromCuts` para calcular la sangría desde el contorno de corte, y `editor-troqueles/dist/app.js` admite pliegues con `d`.

Desde `/Users/fran/Herd/pacdora`:

```sh
python3 geometria/modelos/187000/generar.py
python3 geometria/modelos/187000/integrar.py
node editor-troqueles/tests/parametric-187000.test.cjs
```

`integrar.py` copia `187000.svg` y `model-previews/187000.png`, actualiza `modelos.json` y `capacidades-materiales.json`, y escribe `validacion.json`.

## Procedencia de las imágenes

- Troquel oficial: `https://cdn.pacdora.com/model/6d6d4d46-c6be-4ef3-8b2c-1b350e8ca24c.png` · SHA-256 `fa588b53333b68593bf5e8f39dc9c4f0610ba150e45a8ec6e83966e2f26a6ffa`.
- Render 3D: `https://cdn.pacdora.com/render/1752215243723/12540291.png` · SHA-256 `07b93b988ec125c53950be1c07bc7f4dac57739cdee6f9c455bc65264f4b5c40`.
- Ninguna de las dos requiere autenticación. La descarga del archivo vectorial (AI/PDF/DXF) sí exige iniciar sesión; no se eludió esa restricción.

## Validación y límites

- XML del SVG válido; JSON válido; extensión positiva.
- Corte, caras y pliegues del modelo base comparados con el SVG de Pacdora; el contorno coincide con la imagen oficial al considerar su sangría de 5 mm.
- Motor validado contra 7 muestras: corte 0,00007 mm, caras 0,00003 mm.
- Editor local: 187000 editable, corte 143 × 155 mm, 7 caras, 6 pliegues, 0 aberturas; cambios a 160 × 70 × 25 (185 × 155 mm), 90 × 70 × 25 (115 × 155 mm) y H = 40 (158 × 155 mm) verificados.
- Pliego: 143 × 155 ≤ 330 × 480; 6 cajas por pliego con 3 mm de sangría y rotación.
- No se comparó contra una exportación DXF/PDF de Pacdora ni contra una muestra física. No se verificaron offsets internos/externos, sangría oficial, capas de impresión ni parámetros avanzados.
- La equivalencia digital no acredita armado físico ni aptitud de fabricación.

## Evidencia REA

- Página y geometría base: `ev_73771f17be96543b91985400c8f8a0ea185b779c7b1718c50df19a2a7b62f099`.
- Variación 150 × 90 × 40: `ev_b7dfb9d69864d7dfb09eb62a730fd7383932aad52219bf19e45cef89a842049a`.
- Variación L = 160: `ev_75444ecb274977fc80301d9f223eb08ef608842b64cb585918abae7d07539b36`.
- Variación W = 100: `ev_b01014a87287bb74eb74040a95f3a45f0b1289f156b2e2dac43cd03348032c78`.
- Variación H = 30: `ev_a17998c5f2150f9ef24dc18d11bbeedd9d944eabaa4bc4b1f5bbac6049f2164b`.
- W = 95: `ev_94b5cc880a1f761d5152117b4a0eaae2aa80eacc78fae74cb8d639f380c43f75`.
- W = 118 (pestaña de 18 mm): `ev_51bfc35be8205161fcf30e5c7305b2d9514f33306d9aff1ae80e414da735b6c4`.
- Mínimo 30 × 30 × 15: `ev_c49872181fc6f5b0d481cd296a30f80eba29925ecb021aefe7db762fa8879002`.
- Mínimo 10 × 10 × 5: `ev_4f33ca9d5103fe45b6649168794a2f60a09fc3ef5d012c6d6166091d8db4257d`.
- H = 5 rechazado: `ev_b9c3a3fddcf813092254ab6bddb15a627826145dd2bd913975d1e818be0c595b`.
- Descarga bloqueada por inicio de sesión: `ev_af74ae399a73a565cb2738641e2f8e1b7bd7210e7e687ca3f8f5b9a71378bb4b`.
- Edición 160 × 70 × 25 en el editor: `ev_1cffc89bf22f2d06b5ce9e43fed76fb40f7817d76fbc55db9d1ed21fc696b237`.
- Edición 90 × 70 × 25 (corte 115 × 155): `ev_7c206ac683d9cf047bf39061520a58c34190af40a2054d7c6fb81a2786a83a8f`.
- Edición H = 40 mm (corte 158 × 155, 4 por pliego): `ev_544b9107c3a61bb9a71726d7c637f05fd4fbed2e71cee3697cc78522dab9afc6`.
- Panel de dimensiones con el motor: `ev_29f91a232f637d29e9b33eea18646659a47ca341cfac2507b5f1869822026e45`.
- Render final del catálogo tras retirar la barra superior y el control de caras: `ev_6462b1265fb2d5083bba4b23929892f9c3671602f9669becc951d9e30515d594`.
