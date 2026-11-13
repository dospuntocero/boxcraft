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

- `A = ceil((W − 1)/2) + (L >= 100 ? 8 : 7)`.
- `AR` cambia con el régimen de L: si L < 100, `W < 31 ? 1 : W < 35 ? 5 : W < 43 ? 6 : 7`; si L ≥ 100, `W < 31 ? 1 : W < 33 ? 5 : W < 41 ? 6 : 7`.
- `C = L >= 100 ? 15 : 13`; `CR = L >= 100 ? 8 : 7`.
- `G = L + W >= 125,25 ? 16 : 13`; `L1 = L − 1`. La frontera se localizó con sondas decimales: 125,2 → 13 y 125,25 → 16.
- `NX = NY = W < 31 ? 2 : 3`.

Se capturaron **78 configuraciones** (L 70–120, W 30–48, H 70–150 mm): 49 originales y 29 nuevas (8 con H 70–75 y 21 con L 70–99). Las 29 nuevas se reservaron como holdouts. El error máximo fue **0,000000000014 mm**; la topología se mantiene en 16 caras, 15 pliegues, 94 cortes y 2 aberturas. El informe está en `reglas-parametricas.json` y `validacion-parametrica.json`.

La altura y la longitud mínimas bajan a 70 mm (la longitud estaba en 80 mm). Se añadieron 21 capturas con L 70–99 para fijar el régimen; en el proceso se corrigieron `A` (`ceil((W − 1)/2)`, que ajusta los anchos decimales) y `AR` (umbrales 35/43 mm cuando L < 100). Las cuatro solapas interiores (`FRT`, `FLT`, `FRB`, `FLB`) miden hasta 28 mm y se pliegan esa profundidad desde cada abertura; con H = 70 mm quedan al menos 14 mm de holgura (2 × 28 = 56 mm), de modo que el cierre cabe sin chocar. Las capturas nuevas incluyen H = 70, 71 y 75 mm, y L = 70, 71, 75 y 99 mm.

## Verificación y límites

Se comprobaron XML válido, conteos y correspondencia de todos los campos geométricos incluidos con la respuesta original. La suma de pliegues calculada es 1270.0040064205623 mm frente a 1270 mm declarados. Se rasterizó e inspeccionó la salida local, incluyendo ambas aberturas de colgado y los cierres insertables; no se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Sangría y anotaciones sizeArrowData quedan fuera. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción ni archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA: ev_418dd2411d60f065f42d0416564f26e7f24c8424b3a209c929e9d5f15451e97e. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
