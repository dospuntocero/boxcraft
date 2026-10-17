# Troquel 112310 · Caja con asa y fondo encajable

Fuente: https://www.pacdora.com/es/dielines-detail/custom-dimensions-tuck-end-box-variations-auto-bottome-snap-lock-boxes-dieline-112310

Se conservan las medidas iniciales de manufactura: **302 × 152 × 182 mm**, material **Onda E de 1.5 mm**. Familia recibida: BuckleSuitcaseForward. El plano ocupa **952 × 439 mm**, con **16 caras, 15 pliegues, 72 comandos de corte exterior y 3 aberturas interiores**.

## Archivos y uso

- troquel-generado.svg: caras coloreadas, cortes rojos, pliegues azules discontinuos y aberturas representadas como trazados separados.
- troquel-generado.json: geometría y procedencia.
- vista-previa.png: render del SVG inspeccionado visualmente.
- generar.py: reproduce SVG y JSON sin red ni dependencias externas.
- base/knife-00.json y base/manifest.json: respuesta original y manifiesto de REA.
- validacion.json: verificaciones de salida.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/112310/generar.py
```

Reemplaza SVG y JSON, manteniendo las medidas iniciales; no modifica la vista PNG. No ofrece redimensionamiento ni controles avanzados: no se capturaron variaciones paramétricas.

## Verificación y límites

Se comprobó XML válido, conteos y correspondencia de todos los campos geométricos incluidos con la respuesta original. La suma de pliegues calculada es 3190.7774125491183 mm, frente a 3190.78 mm declarados por el servidor. Se rasterizó e inspeccionó la salida local, incluyendo abertura de asa, ranuras y pestañas inferiores; no se comparó con una imagen del editor original.

Los arcos se interpretan como SVG A con los campos recibidos. Se excluyen sangría y anotaciones sizeArrowData. Los colores sirven para inspección; no se verificaron armado físico, tolerancias de producción ni archivos AI/DXF/PDF. No está validado para fabricación.

Evidencia REA: ev_a908ce42df7992776ec9aa9f023d02b40ed588be86d11b3e40489dbabec3274f. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
