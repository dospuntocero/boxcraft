# Troquel 180320 · Caja para sándwich con ventana

Fuente: https://www.pacdora.com/es/dielines-detail/sandwich-box-with-window-dieline-180320

Medidas iniciales de manufactura expuestas por la interfaz: **120 × 75 mm**, cartón blanco 350 g de **0.5 mm**. Este modelo tiene dos controles dimensionales; H=0 es un valor auxiliar de la API, no una altura física de cero. Familia recibida: WindowLockSandwichBox.

El plano ocupa **289.4533188057741 × 289.37794000823277 mm**, con **12 caras, 13 pliegues, 63 comandos de corte exterior y una ventana interior**.

## Archivos y uso

- troquel-generado.svg: caras coloreadas, corte rojo, pliegues azules discontinuos y ventana como corte independiente.
- troquel-generado.json: geometría y procedencia, con L/W como medidas expuestas.
- vista-previa.png: render del SVG inspeccionado visualmente.
- generar.py: reproduce SVG y JSON sin conexión ni dependencias externas.
- base/knife-00.json y base/manifest.json: respuesta original y manifiesto de REA.
- validacion.json: comprobaciones de salida.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/180320/generar.py
```

Reemplaza SVG y JSON, manteniendo las medidas iniciales; no modifica la vista PNG. No ofrece redimensionamiento ni controles avanzados: no se capturaron variaciones paramétricas.

## Verificación y límites

Se comprobaron XML válido, conteos y correspondencia de todos los campos geométricos incluidos con la respuesta original. La suma de pliegues calculada es 1033.7041481883562 mm frente a 1033.7 mm declarados. Se rasterizó e inspeccionó la salida local, incluyendo la ventana, pliegues diagonales y pestañas; no se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Sangría y anotaciones sizeArrowData quedan fuera. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción, colocación de película en la ventana ni archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA: ev_9e09f689ace42c23508869c90acd37b28df78921975b0730b2b74f72a35d73b1. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
