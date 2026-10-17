# Troquel 102010 · Cierre inferior snap-lock

Fuente: https://www.pacdora.com/es/dielines-detail/custom-dimensions-tuck-end-boxes-auto-bottome-snap-lock-dieline-102010

Por indicación del usuario se conservan las medidas iniciales de manufactura: **120.6 × 60.6 × 161.1 mm**, cartón blanco 350 g de **0.5 mm**. La familia recibida del servidor es PairBuckle. El plano ocupa 377.9 × 282.25 mm y contiene 13 caras, 12 pliegues y 80 comandos de corte.

## Archivos

- troquel-generado.svg: plano local con caras coloreadas, cortes rojos y pliegues azules discontinuos.
- troquel-generado.json: geometría local con medidas y procedencia.
- generar.py: reproduce el plano sin conexión ni dependencias externas.
- reglas-altura.json y validacion-generador.json: regla empírica de altura y su comprobación.
- muestras/: respuestas originales y manifiesto de las etapas de captura.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/102010/generar.py
```

La ejecución reemplaza el SVG y JSON de salida. El valor predeterminado mantiene exactamente las medidas iniciales. Largo y ancho quedan fijos. No se exponen controles avanzados.

Se conserva una opción experimental `--height`, entre 161.1 y 190.5 mm. Su regla se dedujo de dos respuestas con L=139.7 y W=76.2, y se comprobó en otra pareja L=129.54 y W=68.58, al pasar de H=190.5 a H=177.8: los 857 campos numéricos comparados coincidieron dentro de 0.000001 unidades. Los datos de comprobación no se usaron para ajustar la regla. Su aplicación a alturas distintas de la inicial con L=120.6 y W=60.6 es una transferencia empírica, no una segunda comprobación directa del servidor.

## Cambio de estructura del fondo

No se aplicó un único ajuste lineal a largo y ancho. Con L=139.7, W=60.6 y H=161.1 el servidor entregó 92 comandos de corte y S1=1, frente a los 80 comandos y S1=0 de la base. Con W=76.2 volvió a 80 comandos. El cambio es estructural y no equivale a escalar las coordenadas. Las muestras completas quedan disponibles para un análisis futuro si se necesitan otras medidas.

## Verificación y límites

La geometría de salida predeterminada coincide con la capa original en todos los campos incluidos. Se verificó XML del SVG, medidas de salida, conteos de caras/pliegues y la comprobación independiente de altura. Se excluyeron sangría y anotaciones sizeArrowData tanto de la salida como de la comparación de altura. Los arcos se representan mediante comandos SVG A con los campos recibidos; no se contrastó visualmente su interpretación con el editor.

Los colores sirven para inspección. No se verificó una muestra física, plegado real, tolerancias de producción ni exportación AI/DXF/PDF. No está validado para fabricación.

## Evidencia

- Inspección inicial: ev_c6ea1b036de1ac294d9e3583195505c1ec266575314f7ee931adc64f29436088.
- Geometría inicial tras recuperación: ev_d1a199a17596b35f91edc2663082fe51f7e8dee1d3e8ea30e3b1605d3502ea79.
- Muestras y comprobación de altura: ev_0a7239223cabad80da05402c2a2ce706c070f982ebc2bf7269b14408127c2ff2.

Las primeras capturas de variaciones agotaron el límite MCP de 300 s. Se diagnosticó y cerró con autorización un navegador temporal de REA que había quedado abierto. Después se recuperaron las capturas. La captura final de muestras reportó cleanup_incomplete; se exportó su observación parcial, con todas las acciones registradas completadas y las respuestas usadas presentes. No se presenta su ciclo de vida como completo. La geometría y los campos comparados proceden de las respuestas conservadas, no de los intentos sin resultado.
