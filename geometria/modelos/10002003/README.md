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

Reemplaza SVG y JSON, manteniendo las medidas iniciales; no modifica la vista PNG. No ofrece redimensionamiento ni controles avanzados: no se capturaron variaciones paramétricas.

## Verificación y límites

Se comprobaron XML válido, conteos y correspondencia de todos los campos geométricos incluidos con la respuesta original. La suma de pliegues calculada es 1270.0040064205623 mm frente a 1270 mm declarados. Se rasterizó e inspeccionó la salida local, incluyendo ambas aberturas de colgado y los cierres insertables; no se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Sangría y anotaciones sizeArrowData quedan fuera. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción ni archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA: ev_418dd2411d60f065f42d0416564f26e7f24c8424b3a209c929e9d5f15451e97e. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
