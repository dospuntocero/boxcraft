# Troquel 12109002 · Caja para pastel con asas

Fuente: https://www.pacdora.com/es/dielines-detail/cake-box-dieline-12109002

Medidas iniciales de manufactura: **236 × 170 × 180 mm**, material **Onda E de 1.5 mm**. Familia recibida: TrapezoidalFoldingAngleHandleTrayBox. Plano de **824 × 1018 mm**, con **19 caras, 26 pliegues, 46 comandos de corte exterior y 4 aberturas interiores** para asas y cierre.

## Archivos y uso

- troquel-generado.svg: caras coloreadas, cortes rojos, pliegues azules discontinuos y aberturas separadas.
- troquel-generado.json: geometría y procedencia.
- vista-previa.png: render del SVG revisado visualmente.
- generar.py: reproduce SVG y JSON sin red ni dependencias externas.
- base/knife-00.json y base/manifest.json: respuesta original y manifiesto de REA.
- validacion.json: verificaciones de la salida.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/12109002/generar.py
```

Reemplaza SVG y JSON, conservando las medidas iniciales; no actualiza la vista PNG. No ofrece redimensionamiento ni controles avanzados: no se capturaron variaciones paramétricas.

## Verificación y límites

Se verificaron XML válido, 19 caras, 26 líneas de pliegue y 4 trazados de abertura. Los campos geométricos incluidos coinciden con la respuesta capturada. La suma de pliegues calculada es 4563.102295402743 mm frente a 4563.1 mm declarados. Se rasterizó e inspeccionó la salida: asas, ranuras laterales, pestañas y pliegues diagonales visibles. No se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Sangría y anotaciones sizeArrowData quedan fuera. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción o archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA: ev_f15d9188197a7f8329e36bc85cb9c878bfb0c34f341a627343031a2b300da5b6. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
