# Troquel 112047 · Techo con cordón y fondo encajable

Fuente: https://www.pacdora.com/es/dielines-detail/roofing-cord-buckle-bottom-box-dieline-112047

Se conservan las medidas iniciales de manufactura: **70 × 50 × 60 mm**, cartón blanco 350 g de **0.5 mm**. La familia recibida es RoofWiringAndBottomBox. El plano ocupa **252.5 × 152.5 mm**, con **19 caras, 18 pliegues, 72 comandos de corte exterior y 4 orificios circulares superiores**. Los orificios tienen radio de 2 mm en los datos recibidos.

## Archivos y uso

- troquel-generado.svg: plano con caras coloreadas, corte rojo, pliegue azul discontinuo y cuatro orificios como cortes independientes.
- troquel-generado.json: geometría y procedencia.
- vista-previa.png: imagen rasterizada del SVG, revisada visualmente.
- generar.py: reproduce SVG y JSON con Python estándar, sin red.
- base/knife-00.json y base/manifest.json: respuesta original, etapas y hash capturados por REA.
- validacion.json: comprobaciones de la salida.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/112047/generar.py
```

Reemplaza SVG y JSON de salida, manteniendo las medidas iniciales. No modifica la vista PNG. No ofrece redimensionamiento ni controles avanzados: no se capturaron variaciones paramétricas de este modelo.

## Verificación

Se comprobó XML válido, conteos de caras/pliegues/orificios y correspondencia de todos los campos geométricos incluidos con la respuesta original. La longitud de pliegues calculada es 1010.7692338711901 mm, frente a 1010.77 mm declarados por el servidor. Se rasterizó e inspeccionó la salida: cuatro orificios visibles, pliegues de techo, pestaña lateral y cierre inferior. No se comparó con una captura visual del editor original.

La sangría y las anotaciones sizeArrowData se excluyen. Los arcos se interpretan como SVG A con los campos originales. Los colores sirven para inspección; no se verificaron armado físico ni tolerancias de producción. No está validado para fabricación.

Evidencia REA: ev_4f668f2c1bdecad06f7412545afea068086c1ad9e77e5d01e76afba6a6b770c0. La captura se completó; excedió el límite de transporte MCP y se recuperó mediante exportación del registro sin repetir la captura.
