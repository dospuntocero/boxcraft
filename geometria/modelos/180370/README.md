# Troquel 180370 · Envase para papas fritas

Fuente: https://www.pacdora.com/es/dielines-detail/french-fries-box-dieline-180370

Medidas iniciales de manufactura: **120 × 80 × 160 mm**, cartón blanco 250 g de **0.35 mm**. Familia recibida: ChipBox. Plano de **314.301396 × 453 mm**, con **10 caras, 9 pliegues y 26 comandos de corte exterior**, sin aberturas interiores.

## Archivos y uso

- troquel-generado.svg: caras coloreadas, cortes rojos y pliegues azules discontinuos.
- troquel-generado.json: geometría y procedencia.
- vista-previa.png: render del SVG inspeccionado visualmente.
- generar.py: reproduce SVG y JSON sin conexión ni dependencias externas.
- base/knife-00.json y base/manifest.json: respuesta original y manifiesto de REA.
- validacion.json: comprobaciones de salida.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/180370/generar.py
```

Reemplaza SVG y JSON, manteniendo las medidas iniciales; no modifica la vista PNG. No ofrece redimensionamiento ni controles avanzados: no se capturaron variaciones paramétricas.

## Verificación y límites

Se comprobaron XML válido, conteos y correspondencia de todos los campos geométricos incluidos con la respuesta original. La suma de pliegues calculada es 1326.0558990037791 mm frente a 1326.06 mm declarados. Se rasterizó e inspeccionó la salida local, con contornos curvos, paredes inclinadas y pestañas laterales; no se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Sangría y anotaciones sizeArrowData quedan fuera. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción ni archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA: ev_122d9d496f87d479cdc26e2cd7caaeb42656bbc63e440199f52f8ae5a71e0ae5. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
