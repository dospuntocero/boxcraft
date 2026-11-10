# Troquel 10001006 · Caja con solapas insertables

Fuente: https://www.pacdora.com/es/dielines-detail/tuck-end-software-box-dieline-10001006

Medidas iniciales de manufactura: **40 × 40 × 130 mm**, cartón blanco 350 g de **0.5 mm**. Familia recibida: Pair. Plano de **172.5 × 231 mm**, con **13 caras, 12 pliegues y 76 comandos de corte exterior**, sin aberturas interiores.

## Archivos y uso

- troquel-generado.svg: caras coloreadas, cortes rojos y pliegues azules discontinuos.
- troquel-generado.json: geometría y procedencia.
- vista-previa.png: render del SVG inspeccionado visualmente.
- generar.py: reproduce SVG y JSON sin conexión ni dependencias externas.
- base/knife-00.json y base/manifest.json: respuesta original y manifiesto de REA.
- validacion.json: comprobaciones de salida.
- compilar-reglas.py: deriva los parámetros internos y ajusta las reglas desde `parametrico/`.
- parametrico/: capturas históricas y `extension/` con 273 muestras de las ampliaciones.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/10001006/generar.py
```

Reemplaza SVG y JSON. El editor usa un motor `compiled` que adapta L/W/H con reglas sobre los parámetros internos `A, AR, C, CR, E, S, G, NX, NY`, separadas en tres regímenes de anchura; no modifica la vista PNG.

## Motor verificado

El editor aplica reglas compiladas en los parámetros internos que devuelve Pacdora, con tres regímenes según la anchura:

- `W <= 20`: ATT = 0, AX = 2,5, NX = NY = 2.
- `20 < W < 30`: ATT = 13, AX = 2,5, NX = NY = 2.
- `W >= 30`: ATT = 13, AX = 3,5, NX = NY = 3.

Parámetros derivados de L/W:

- `A = min(floor(L/2), floor((ceil(W) + C + 0,5)/2 + 0,5))`.
- `AR = W <= 30 ? 1 : L < 40 ? floor((W+2)/8)+1 : L < 60 ? floor((W+3)/8)+1 : L < 100 ? floor((W+13)/8) : floor((W+14)/8)`.
- `C = 10/11/13/15` y `CR = 5/6/7/8` para `L < 40`, `L < 60`, `L < 100` y `L >= 100`.
- `E = 8` si `L >= 65`; si no, `6` para `W > 30`, `4`/`5`/`6` según `L < 40`, `L < 45` o el resto.
- `S = L >= 65 ? 6 : 4`.
- `G = L + W >= 125,25 ? 16 : min(13, W − 1,5)`.
- `NX = NY = W <= 30 ? 2 : 3`.

Se capturaron **321 respuestas** (314 dentro del rango validado) y se reservaron **79 holdouts**. El error máximo fue **0,0000000000026 mm**; topología constante de 13 caras, 12 pliegues y 76 cortes. El motor reproduce **L 30–100, W 10,6–60 y H 80–180 mm**, incluidas muestras con decimales en los bordes y anchuras estrechas como **74 × 14 × 124 mm** (plano 188 × 177 mm). Informe en `reglas-parametricas.json` y `validacion-parametrica.json`; `compilar-reglas.py` reconstruye ambos desde `parametrico/`.

Los bordes no obvios se sondearon con decimales: `W = 10,6`, `14`, `20,5`, `29,5` y `30,5`; `L = 64,5` y `99,5`; y `L + W = 125,25`. `G` cambia en 125,25 (no en 126), se reduce a `W − 1,5` cuando `W < 15` y `AR` cambia de fórmula en L = 40, 60 y 100.

## Verificación y límites

Se comprobó, con el motor en Node, que las 314 muestras únicas dentro del rango (378 archivos con duplicados históricos) reproducen los 725 campos numéricos de la capa `traditional` (error máximo 1,9 × 10⁻¹²). También se comprobaron XML válido, conteos y correspondencia con la respuesta original. La suma de pliegues calculada es 810.4040064205623 mm frente a 810.4 mm declarados. Se rasterizó e inspeccionó la salida local, incluyendo pestaña de pegado, solapas laterales y cierres insertables; no se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Sangría y anotaciones sizeArrowData quedan fuera. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción ni archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA original: ev_4c9d52a11d7a7bccb98fcd7cc22344a35016e616b6af52eb7fab1d14df6ace8a. Las capturas de la ampliación se hicieron con Playwright el 2026-10-28 y se conservan en `parametrico/extension/` con manifiesto y SHA-256. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
