# Troquel 150010 · Caja mailer con tapa abatible

El usuario confirmó usar las medidas iniciales de la plantilla pública: **315 × 202 × 62 mm de manufactura**, cartón corrugado **Onda E de 1.5 mm**. La familia recibida del servidor es Aircraft. El plano ocupa **576 × 590 mm** y contiene 19 caras, 22 pliegues, 89 comandos de corte exterior y 4 ranuras interiores.

Fuente pública: https://www.pacdora.com/es/dielines-detail/custom-dimensions-flip-top-boxes-mailer-dieline-150010

El enlace originalmente entregado incluía id=70845997. Ese proyecto solicita inicio de sesión en la sesión de REA; sus medidas y ajustes no se recuperaron. El usuario eligió expresamente la plantilla pública, por lo que los archivos siguientes no pretenden reproducir el proyecto privado.

## Archivos

- troquel-base-publica.svg: SVG con caras coloreadas, corte rojo y pliegues azules discontinuos. Incluye las 4 ranuras como trazados independientes.
- troquel-base-publica.json: geometría y procedencia de la plantilla pública.
- vista-previa.png: vista rasterizada del SVG para inspección.
- generar.py: reproduce los archivos SVG y JSON sin conexión ni dependencias externas.
- base-publica/knife-00.json: respuesta geométrica original.
- base-publica/manifest.json: etapas, URL y hash de la respuesta capturada.
- muestras/manifest.json: intento de acceso al proyecto, con el diálogo de autenticación observado y sin respuestas geométricas del proyecto.
- validacion.json: conteos y comprobación de la geometría de salida.

Desde /Users/fran/Herd/pacdora:

```sh
python3 geometria/modelos/150010/generar.py
```

Esta ejecución reemplaza el SVG y JSON de salida, conserva las medidas iniciales y no modifica la vista PNG. No ofrece redimensionamiento paramétrico: no se capturaron variaciones de L/W/H para este modelo. No se exponen parámetros avanzados.

## Verificación

Se comprobó XML válido, las 19 caras, 22 líneas de plegado y 4 trazados de ranura. Los campos geométricos incluidos coinciden con la respuesta original. Se renderizó el SVG mediante Sharp y se inspeccionó la imagen resultante: contornos, pestañas y ranuras visibles. Esa revisión verifica la salida local, no su equivalencia visual con una captura del editor original.

El renderizador común se amplió para incluir `holes`, porque estas ranuras no forman parte del contorno exterior `cuts`. Los arcos se interpretan como SVG A con los campos recibidos. La sangría y anotaciones sizeArrowData quedan fuera. Los colores son de inspección; no se verificaron tolerancias, armado físico ni archivos de fabricación. No está validado para fabricación.

## Evidencia REA

- Proyecto que solicita autenticación: ev_60173e6f93fcf44ac89b537f646726d3a916885ea7ddb4c0f9e5281392b954ec.
- Plantilla pública y geometría: ev_d08c5f2a484622e0e1879ed095969a4b8e9aca75e8d3199b8ca638fc1ba95afe.

Ambas capturas se completaron. Sus resultados excedieron el límite de transporte MCP y se recuperaron mediante exportación de evidencia, sin repetir las capturas para recuperar el mismo resultado.
