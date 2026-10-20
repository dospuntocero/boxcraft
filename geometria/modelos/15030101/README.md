# 15030101 — Caja para tarta con ventana

Adquisición actualizada el 17 de octubre de 2026. Fuente: [Pacdora](https://www.pacdora.com/es/dielines-detail/cake-box-dieline-15030101), modelo interno 11492, familia `MutualLockingCardboardAircraftBoxWithWindow`.

![Icono original](icono.png)

## Resultado y alcance

La caja está incorporada en `editor-troqueles/dist/`, destino del enlace `dist` de la raíz. Incluye icono original local, selección de **12 materiales y 18 combinaciones de material/espesor** con geometría capturada para **150 × 150 × 50 mm**. La aplicación conserva estas medidas fijas. Se comprobó en Chrome la selección y descarga real de las 18 combinaciones, y se conservaron los SVG en `exportaciones/`.

El generador CLI permite además ocho configuraciones dimensionales exactas del material original, todas listadas en `configuraciones.json`. Hay **26 configuraciones exactas** en total. No se interpolan dimensiones ni espesores: el ajuste dimensional afín no superó el contraste independiente y permanece deshabilitado.

## Ficha base

| Propiedad | Valor |
|---|---|
| Manufactura L × W × H | 150 × 150 × 50 mm |
| Interior | 146,4 × 148,9 × 49,4 mm |
| Exterior | 150,4 × 150,4 × 50,4 mm |
| Material original | Cartón blanco 350g, ID 103 |
| Espesor original | 0,5 mm |
| Plano desplegado base | 359,6 × 448,5 mm |
| Geometría base | 15 caras, 18 pliegues, 129 comandos de corte, 1 ventana interior |

La respuesta de límites para estas medidas declara espesor 0,2–0,5 mm. Los tres materiales personalizados se capturaron en 0,2 / 0,35 / 0,5 mm. El paso de edición no se estableció. La familia declara límites dimensionales de 20–2000 mm por eje: son metadatos de la fuente y no un rango habilitado del generador local. No se estableció un pliego físico máximo.

En estas medidas, Pacdora deshabilita cartón blanco 400g (0,55 mm), kraft 120g (0,14 mm) y todas las alternativas corrugadas. La matriz completa está en [MATERIALES.md](MATERIALES.md). La incompatibilidad observada no se generaliza a otras medidas.

## Archivos y reproducción

- `base/`: geometría original, identidad, catálogo general, límites y manifiesto con hashes.
- `troquel-generado.svg`, `troquel-generado.json`, `vista-previa.png`: reproducción e inspección de la base. El SVG de inspección conserva caras, corte, arcos, pliegues y ventana; excluye sangría y cotas.
- `icono.png`: miniatura original indicada por el campo `image` del modelo; `referencia-pacdora.png`: plano de referencia indicado por `knife`.
- `parametricas/`, `independiente/`: muestras de dimensiones; `materiales/`, `personalizados/`: muestras por material/espesor. Sus manifiestos enlazan hashes, configuración efectiva y evidencia REA.
- `configuraciones.json`: registro de 26 configuraciones exactas y su procedencia.
- `validacion.json`: verificaciones estructurales de la base; `validacion-parametrizacion.json`: ajuste dimensional rechazado; `verificacion-interfaz.json`: comprobación de las 18 descargas reales.
- `exportaciones/`: SVG descargados desde el editor. Incluyen las capas activas y el sangrado local de 3 mm, diferente del sangrado de 5 mm solicitado al capturar Pacdora.
- `editor-materiales.png`: captura de la interfaz con kraft personalizado de 0,35 mm.

Desde la raíz del proyecto:

```sh
python3 geometria/modelos/15030101/preparar-configuraciones.py
python3 geometria/modelos/15030101/generar.py
python3 editor-troqueles/incorporar-modelos-adquiridos.py
```

Generar una combinación exacta en otro directorio:

```sh
python3 geometria/modelos/15030101/generar.py --material-id 7 --thickness 0.35 --output-dir /tmp/caja-kraft
python3 geometria/modelos/15030101/generar.py --length 155 --width 155 --height 55 --output-dir /tmp/caja-155
```

El generador rechaza combinaciones sin captura exacta. Sin `--output-dir`, reemplaza el SVG, JSON y validación de salida en esta carpeta. La integración siempre utiliza la base y añade únicamente perfiles con 150 × 150 × 50 mm; sus procesos de preparación reaplican el alta. La aplicación vigente está en `editor-troqueles/`.

![Troquel local](vista-previa.png)

## Dimensiones, compensaciones y parámetros

Se investigó cada eje por separado y se contrastó un ajuste afín contra combinaciones independientes. Se compararon 1.389 campos numéricos por muestra con tolerancia de 0,000001. El máximo error fue 7 unidades en el conjunto numérico, que incluye coordenadas y metadatos; no se interpreta como tolerancia física de fabricación. El registro enumera las diferencias. Se habilita un **motor afín L/W/H experimental** para la topología grande. El ajuste usa seis muestras y tiene un error máximo de **3,88 mm** en `totalX`; la base se reproduce exactamente. Los límites son L/W ≥ 100 mm y H ≥ 30 mm, porque por debajo cambia la topología (113 cortes/16 pliegues frente a 129/18). El intento anterior se retiró por errores de hasta 30 mm; este es un ajuste nuevo, separado y marcado como experimental. Las muestras y la decisión anterior quedan en `correccion/manifest.json`.

La captura adicional confirmó 155 × 155 × 55 mm con respuesta geométrica completa y dimensiones interiores 151,4 × 153,9 × 54,4 mm; exteriores 155,4 × 155,4 × 55,4 mm. Resuelve la solicitud pendiente de la primera prueba.

Cada perfil habilitado conserva sus propias compensaciones de interior/exterior y geometría. El espesor efectivo se toma de la capa; el espesor del objeto `science` puede ser el valor predeterminado del material personalizado. Se verifica la identidad del material y el espesor configurado de la respuesta. No se asume compatibilidad por compartir espesor.

Para este modelo, la respuesta trae `openParamsStatus=0` y `openParams=[]`. La sección «Más» observada ofrece servicios de diseño, no controles geométricos avanzados. No hay parámetros avanzados editables observados que se hayan reproducido.

## Verificación y evidencia

Se verificaron hashes, JSON/XML válidos, números finitos, extensión positiva y conservación exacta de las geometrías habilitadas respecto de las respuestas originales. Se comparó visualmente el troquel local con la imagen original: coinciden contorno, ventana redondeada, pestañas y distribución de pliegues; los colores de inspección son distintos. Esta inspección no sustituye una comparación métrica ni una prueba física.

Las **62 pruebas del editor** pasaron. Incluyen contraste de cada nuevo perfil contra su respuesta original y hash, conversiones interior/exterior y rechazo de medidas/espesores no capturados. En Chrome se seleccionaron las **18 combinaciones** y se descargaron sus SVG, sin errores de página. Se comprobó el XML de los archivos descargados. El script reproducible es `scripts/verificar-15030101.cjs`, con el editor servido en `http://127.0.0.1:8765/`.

Referencias REA:

| Investigación | Evidencia |
|---|---|
| Identidad en catálogo | `ev_08498ad750037811b9ce3f1df9364c88edd6730613017a0a57281de3acfd6ebc` |
| Geometría base | `ev_89ba7b7dfd2c598f54c4d2f5658241fffcecfaef8870723ea2044b409341aae2` |
| Primeras variaciones dimensionales | `ev_44cda8270657702f72a0085860e251ed8c058492bca976ff675ebcd529971e56` |
| Inventario corrugados deshabilitados | `ev_bec757e1032bd313dd177d2022a6e5e17742e1fd8239e847b018ea018941132c` |
| Inventario blanca/kraft/estucado | `ev_8bb887655d02174e192d06e5b416612d3dda8a910a7eac54eb4475e71487b280` |
| Selecciones de material | `ev_836fc89dab2fefb6bd594a26b532e8c1a834ac033c170197c1eff5f667909204` |
| Espesores personalizados | `ev_bc1ed27f966ebe5de8d6601bf2c865152ab7f39a67839296d8bc5c45a0b09885` |
| Combinación dimensional independiente y sección Más | `ev_a24378d16af31f4c9b109d696bcb112bb5a641337fb51fa46095009d65508bd1` |

Las capturas de primeras variaciones, selecciones de material y espesores personalizados reportaron `cleanup_incomplete`. Sus acciones se completaron y se conservaron respuestas geométricas completas con hashes; no acreditan cierre correcto de esas sesiones. La captura independiente final sí terminó con `terminated-owned-process`. Los bundles exportados en `evidencias/modelos/15030101/` conservan las limitaciones originales y evitan repetir capturas por errores de transporte MCP. No se observaron respuestas HTTP de error durante las dos capturas nuevas de materiales.

Quedan fuera del alcance validado la topología pequeña, espesores no muestreados, otras medidas para materiales alternativos, armado físico y tolerancias de fabricación. El motor afín grande está publicado como experimental.
