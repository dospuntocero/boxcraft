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

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/10001006/generar.py
```

Reemplaza SVG y JSON, manteniendo las medidas iniciales; no modifica la vista PNG. No ofrece redimensionamiento ni controles avanzados: no se capturaron variaciones paramétricas.

## Verificación y límites

Se comprobaron XML válido, conteos y correspondencia de todos los campos geométricos incluidos con la respuesta original. La suma de pliegues calculada es 810.4040064205623 mm frente a 810.4 mm declarados. Se rasterizó e inspeccionó la salida local, incluyendo pestaña de pegado, solapas laterales y cierres insertables; no se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Sangría y anotaciones sizeArrowData quedan fuera. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción ni archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA: ev_4c9d52a11d7a7bccb98fcd7cc22344a35016e616b6af52eb7fab1d14df6ace8a. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
