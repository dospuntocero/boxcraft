# Troquel 10002003 · Caja con doble pestaña de colgado

Fuente: https://www.pacdora.com/es/dielines-detail/custom-dimensions-hook-boxes-double-hook-dieline-10002003-10002003

Medidas iniciales de manufactura: **100 × 40 × 120 mm**, cartón blanco 350 g de **0.5 mm**. Familia recibida: PairWithHook. Plano de **295.5 × 263.75 mm**, con **16 caras, 15 pliegues, 94 comandos de corte exterior y 2 aberturas de colgado**.

## Archivos y uso

- troquel-generado.svg: caras coloreadas, cortes rojos, pliegues azules discontinuos y aberturas como trazados independientes.
- troquel-generado.json: geometría y procedencia.
- vista-previa.png: render del SVG inspeccionado visualmente.
- generar.py: reproduce SVG y JSON sin red ni dependencias externas.
- base/knife-00.json y base/manifest.json: respuesta original y manifiesto de REA.
- validacion.json: comprobaciones de salida.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/10002003/generar.py
```

Reemplaza SVG y JSON. El editor usa un motor `compiled` que adapta L/W/H con reglas sobre los parámetros internos `A, AR, C, CR, G, L1, NX, NY`; no modifica la vista PNG.

## Motor verificado

El editor aplica reglas compiladas en los parámetros internos que devuelve Pacdora:

- `A = floor(W/2) + (L >= 100 ? 8 : 7)`.
- `AR = W < 31 ? 1 : W < 33 ? 5 : W < 41 ? 6 : 7`.
- `C = L >= 100 ? 15 : 13`; `CR = L >= 100 ? 8 : 7`.
- `G = L + W >= 129 ? 16 : 13`; `L1 = L − 1`.
- `NX = NY = W < 31 ? 2 : 3`.

Se capturaron **49 configuraciones** (L 80–120, W 30–48, H 80–150 mm) y se reservaron 12 como holdouts. El error máximo fue **0,000000000003 mm**; la topología se mantiene en 16 caras, 15 pliegues, 94 cortes y 2 aberturas. El informe está en `reglas-parametricas.json` y `validacion-parametrica.json`.

## Verificación y límites

Se comprobaron XML válido, conteos y correspondencia de todos los campos geométricos incluidos con la respuesta original. La suma de pliegues calculada es 1270.0040064205623 mm frente a 1270 mm declarados. Se rasterizó e inspeccionó la salida local, incluyendo ambas aberturas de colgado y los cierres insertables; no se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Sangría y anotaciones sizeArrowData quedan fuera. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción ni archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA: ev_418dd2411d60f065f42d0416564f26e7f24c8424b3a209c929e9d5f15451e97e. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
