# Análisis de Pacdora: cajas de almacenamiento

Fecha: 13 de octubre de 2026. Inspección con REA y Chrome en sesión nueva sin autenticación. Categoría: https://www.pacdora.com/es/dielines/storage-box-dielines

## Hallazgos observados

- La categoría anuncia 44 modelos. El árbol de accesibilidad de la captura contiene 15 fichas de productos; esto no demuestra que los 44 estén renderizados a la vez.
- Incluye navegación por uso/modelo, categorías con contadores, buscador, tarjetas enlazadas a fichas y contenido explicativo con FAQ.
- Hay estructuras distintas: FEFCO 0201, 0202, 0203 y 0200; cajas con seis compartimentos, deslizantes, rígidas, con tapa y asas.
- La página mezcla HTML orientado a SEO (canonical, hreflang, JSON-LD y metadatos) con recursos de Vue y consultas a una API v2. Los nombres de los módulos no permiten identificar por sí solos toda la implementación.
- La petición de catálogo observada es GET /api/v2/models?pageSize=60&current=1&dielineNameKey=storage-box-dielines&mockup=false&offset=0&complexType=0. También se consultan /models/ctree y /seo/info?id=180.

## Generador inspeccionado

Ficha: https://www.pacdora.com/es/dielines-detail/custom-dimensions-cartons-0201-dieline-200010

- Abre directamente el generador de plantillas. La interfaz expone longitud, anchura, altura, selector mm/in, material y espesor; además distingue dimensiones de manufactura, internas y externas.
- En esta sesión las unidades iniciales fueron pulgadas y el material Onda B. Los valores de manufactura mostrados fueron 17.0866 × 8.4252 × 10.9449 in, aproximadamente 434 × 214 × 278 mm. El grosor mostrado fue 0.1181 in, aproximadamente 3 mm. No se generaliza este valor inicial a otras sesiones.
- La interfaz anuncia AI, PDF, DXF y maqueta 3D; contiene controles de sangría, recorte y pliegue, compartir y diseño en línea.
- Peticiones observadas: GET /models/details?nameKey=custom-dimensions-cartons-0201-dieline-200010; /materials/science?pageSize=1000&scienceType=1; /models/preview?id=3; /project/knife?id=3&bleed=5&export_type=model; /modes/category/cal?cate_id=2&width=214&height=278&length=434.
- También hay consultas a permisos, planes y comprobación Pro. Su presencia no determina qué exportación exige pago.

## Interpretación

La experiencia se divide en catálogo de descubrimiento y generador paramétrico. Las llamadas de cálculo y troquel sugieren participación del servidor; esta captura no establece dónde ocurre toda la generación geométrica ni el plegado 3D. La distinción entre medidas internas, externas y de manufactura indica que reproducir la interfaz no basta: hace falta conocer las compensaciones por material y espesor.

Para una implementación propia, las piezas principales serían catálogo de familias, esquema de parámetros y límites por modelo, geometría de corte y pliegue, compensación de material, vista del plano, previsualización 3D y exportadores vectoriales. Esta es una propuesta de arquitectura, no código fuente recuperado de Pacdora.

## Evidencia y límites

- Categoría, DOM, accesibilidad y red: ev_ee5a28cbdb2ae7ac302682e6cde12231fd4d8031d8fa14068a5787de5ed97544.
- Generador FEFCO 0201, DOM, accesibilidad y red: ev_9d761dcb48852f2945c58238cd15c6fb302d95212ae0fead04916c8c4c2f29dc.
- Evidencia controlada de ejecución, no recuperación del código fuente original. Los identificadores corresponden a la sesión de REA.
- En la primera pasada no se cambiaron parámetros ni se solicitó exportación. La verificación adicional siguiente amplía esa cobertura. No se capturaron cuerpos de respuesta; los endpoints prueban solicitudes, no su contenido ni sus algoritmos. No se verificaron todas las familias, las condiciones de pago ni el comportamiento en móvil.

## Verificación adicional: edición y descarga

Se cambió la longitud de 17.0866 a 20 pulgadas y se confirmó el campo al quitarle el foco. El generador presentó un estado temporal con campos deshabilitados y después actualizó el plano y las medidas:

| Medida | Antes (in) | Después (in) |
| --- | --- | --- |
| Longitud de manufactura | 17.0866 | 20 |
| Longitud interna | 16.9291 | 19.8425 |
| Longitud externa | 17.1654 | 20.0787 |

La anchura, altura y espesor permanecieron en los valores iniciales. La petición de cálculo pasó de length=434 a length=508, equivalente a 20 pulgadas en milímetros. Para estas dos muestras, la longitud interna es aproximadamente 4 mm menor que la de manufactura y la externa 2 mm mayor. Esto describe el modelo y material probados; no establece una fórmula universal.

Durante la interacción se observaron POST y PUT /api/v2/projects, consultas /projects/info y /project/knife con export_type=project, y /modes/category/info?project_id=…&type=project. Por tanto, editar puede crear y actualizar un proyecto en el servidor incluso en esta sesión sin autenticación; no es una operación puramente local. No se inspeccionaron los cuerpos ni se confirmó la persistencia posterior a la sesión.

Al pulsar «Descargar la plantilla de corte» apareció el diálogo de inicio de sesión con Google, Facebook o correo electrónico. La descarga quedó condicionada a autenticación en esta prueba. No se inició sesión, no se descargó un archivo y no se determinó si después exige pago.

También se observó la carga de /scripts/wasm/knife2gltf/1.1.8/knife2gltf.min.wasm. Su nombre sugiere conversión del troquel a glTF en el cliente; la carga del recurso no demuestra por sí sola su ejecución ni su algoritmo.

Evidencia de la prueba completa: ev_02ce3efdb55845f13649814802c778e459c1fe20ddca61f9bfbe75bfcf8444e2. Todas sus acciones finalizaron. El estado final confirma las nuevas dimensiones y el diálogo de autenticación.

Pendientes delimitados: archivo exportado y precisión geométrica, comportamiento autenticado y precios, variación de grosor/material, otras familias y móvil.

## Geometría recibida y conversión 3D

La tercera pasada capturó cuerpos de respuesta, conservados en evidencia-geometria.json. Se extrajeron copias legibles de las respuestas en geometria/knife.json, geometria/preview.json y geometria/cal.json, además del bundle JavaScript servido al navegador. Son artefactos recibidos del sitio, no una implementación propia.

La respuesta /project/knife contiene geometría concreta en layer.traditional: 13 caras, comandos de trazado (M, L, A y Z), líneas de corte, pliegues identificados por nombre, sangrías, transformaciones y animación. Las caras incluyen posición, anchura, altura y su contorno. Esto confirma que el servidor entrega una representación geométrica del troquel, más allá de sus parámetros.

La respuesta /modes/category/cal inspeccionada devuelve restricciones de espesor y metadatos de capas: minThickness=0.2 y maxThickness=9 para esta consulta. No incluye los contornos del plano. Por tanto, observar esa llamada al editar no bastaba para atribuirle la generación geométrica. El material Onda B tiene sus propios límites de 2.5 a 3 mm en /project/knife; son restricciones distintas de las de categoría.

Los datos originales distinguen size={L:430,W:210,H:270,D:3}, knifeSize={L:434,W:214,H:278} y outSize={L:436,W:216,H:282}. También incluyen campos getKnifeSizeAdd y getOutSizeAdd. Los valores coinciden con las medidas de interfaz de la primera prueba; el significado algebraico completo de sus coeficientes no está demostrado.

En el bundle pacdora-3d-CYhaKcyC1P.js se observó una función que inicializa uno de dos wrappers de WebAssembly, obtiene _generateGLTFData, serializa el argumento a JSON cuando hace falta, reserva memoria opcional para bytes y convierte el resultado mediante UTF8ToString. Esto es evidencia estática de una ruta de conversión local, no una traza de ejecución de esa función. El recurso WebAssembly 1.1.8 fue solicitado durante la carga del generador. Su implementación interna no se decompiló.

Conclusión actual: la arquitectura observada es híbrida. El servidor proporciona geometría y configuración del troquel; el JavaScript del cliente contiene una ruta hacia un generador glTF en WebAssembly. Quedan sin verificar la ejecución exacta de esa ruta, todas las transformaciones posteriores y los exportadores AI/PDF/DXF.

Evidencia: ev_77d8bd80d9fa88c43120d6cc5bd429c12c5968d9da9a0622cb273808367c498c. La respuesta MCP excedió el límite de transporte y se recuperó mediante exportación del registro completo, sin repetir la captura. Las conclusiones anteriores proceden de las respuestas concretas y fragmentos del bundle examinados; no implican cobertura de todo el JavaScript.

## Vista local de la captura

Se generaron geometria/vista-troquel.html y geometria/troquel-capturado.svg con el script reproducible geometria/generar-vista.py. La vista permite ocultar caras, nombres, cortes y pliegues; conserva las coordenadas recibidas y no recalcula el modelo. Incluye una tabla de las 6 etapas y 12 rotaciones de plegado. Todas las referencias de rotación corresponden a pliegues presentes en la captura.

Verificación realizada: SVG válido como XML, 13 contornos de cara y 12 líneas de pliegue, concordantes con el JSON original. Los arcos se interpretaron mediante el comando SVG A y los campos originales; falta contrastar visualmente esta interpretación con el editor. No se representó la sangría porque su alineación respecto del corte exige verificar las transformaciones. No es un plano validado para fabricación.

La revisión visual en el navegador integrado quedó bloqueada por su política de URLs, que no admite file://. No se intentó sortear esa restricción. Los archivos están disponibles localmente; no se verificó su apariencia ni el funcionamiento de los controles en un navegador.

## Ruta estática del motor 3D

Se amplió el rastreo en geometria/ruta-conversion-3d.md, con ubicaciones en el bundle. El flujo selecciona y valida una capa, prepara los campos geométricos, elige conversor según la familia, llama al wrapper WebAssembly, revisa el resultado y aplica materiales a las mallas de exterior, interior y cantos. CurveBox y SoftPacking tienen ramas separadas del conversor genérico utilizado por la rama compatible con Carton.

Se extrajo de la captura el WebAssembly original y se leyó su tabla de exportaciones sin ejecutarlo. El inventario geometria/wasm-inventory.json confirma generateGLTFData (función 1494), memoria, malloc y utilidades de runtime. No se decompiló el algoritmo interno. Esta revisión describe relaciones estáticas; no convierte las llamadas inferidas en ejecución observada.

## Coherencia interna y parámetros avanzados

El script geometria/validar-captura.py ejecuta 8 comprobaciones y guarda su resultado en geometria/validacion-captura.json. Todas pasaron: nombres únicos; grafo conectado de 13 caras y 12 pliegues (interpretando los nombres como pares de caras); referencias del contorno a pliegues; referencias de animación; suma de longitudes de pliegue con tolerancia de 0.01 mm; extremos de corte dentro de 1340 × 494 mm; parámetros dentro de sus límites; y espesor compatible con el material. El grafo así interpretado es un árbol.

La captura contiene 6 parámetros adicionales. Sus etiquetas proceden del servidor y su efecto geométrico no fue probado variándolos:

| Código | Descripción recibida | Valor | Rango | Unidad |
| --- | --- | --- | --- | --- |
| OF | High and Low | 2 | 0–3 | longitud |
| R | Chamfering | 3 | 1.5–6 | longitud |
| G | Length of paste | 45 | 10–212 | longitud |
| GT | Paste corner | 15 | 0–45 | ángulo |
| F | 摇盖长度 | 108 | 15–214 | longitud |
| F1 | Side shaking cover | 110 | 10–110 | longitud |

Esto amplía el esquema necesario para reconstruir el modelo: además de largo, ancho, alto y espesor, el servidor entrega parámetros de pestaña de pegado, esquinas y solapas. Las correspondencias por descripción son orientativas; todavía no se recuperaron sus fórmulas.

La validación no demuestra que el troquel arme correctamente ni que sea apto para fabricación. No comprueba intersecciones, tolerancias de producción, extremos interiores de arcos, longitud total de corte o colisiones durante el plegado.

## Experimentos paramétricos y primer generador local

Se variaron por separado L=508 mm, W=254 mm y H=304.8 mm respecto de 434 × 214 × 278 mm, restaurando la base entre cambios. Se capturó además espesor 2.54 mm: conserva las dimensiones de manufactura, cambia las medidas internas/externas y reduce R de 3 a 2.5. No se dedujo una fórmula general de compensación de espesor con solo dos muestras.

Con el espesor fijo en 3 mm se construyó un modelo afín por campo geométrico. Se comprobó contra una combinación independiente: 457.2 × 228.6 × 279.4 mm. Se compararon 822 campos numéricos: caras, cortes, pliegues y los demás campos salvo sangría coinciden dentro de 0.000001 unidades; 6 coordenadas de sangría difieren menos de 0.0001 mm. No se ajustaron coeficientes con la muestra de comprobación.

El generador geometria/modelo-parametrico.py produce troquel-generado.svg y troquel-generado.json sin consultar Pacdora. Admite únicamente el rango delimitado por las muestras y conserva material/espesor y parámetros avanzados fijos. Es una reconstrucción empírica limitada, no recuperación del algoritmo original ni garantía de exactitud en todo ese rango. Uso, fórmulas resumidas y procedencia en geometria/README-modelo.md.

La pestaña avanzada muestra «Actualiza para desbloquear parámetros avanzados» y «Actualizar a Negocios». Sus valores se observaron, pero sus cambios manuales quedaron pendientes por esa restricción; no se eludió.

Las capturas de experimentos y comprobación terminaron con cleanup_incomplete y se recuperaron mediante exportación. Todas las acciones registradas completaron y las respuestas geométricas utilizadas están presentes. Esa cobertura parcial permite comparar los datos conservados, pero no acredita limpieza completa del proceso. IDs: ev_70c78216d8ca163ef7f939d0aed16da00ebc22365fb62afe71f36c34f435b46a y ev_e71c55c541c5bd0970f35ad5e7d9e8acfe58b97439dd0975c40c6f3260455e65. Pestaña avanzada: ev_f5a6bc57aa5f99256bd933eac5f9a8ebfa1cfaf1ca8187ee3166b635309300bf.

## Segundo modelo: caja para loción corporal 10001029

Se analizó la ficha indicada por el usuario y se construyó geometria/modelos/10001029/generar.py. El modelo pertenece a la familia Pair, con 13 caras, 76 comandos de corte y 12 pliegues. La configuración capturada es 60 × 45 × 120 mm y cartón blanco 350 g de 0.5 mm.

Este troquel cambia automáticamente cierres y solapas al variar las medidas básicas. El primer ajuste solo con L,W,H no bastaba; se añadieron muestras para separar esos valores internos sin modificar controles avanzados. El generador final usa únicamente los tres parámetros básicos y conserva material/espesor. Se comprobó contra tres estados independientes del entrenamiento, con 784 campos numéricos coincidentes por estado dentro de 0.000001 unidades. La sangría y anotaciones no se generan ni se incluyeron en esa comparación.

El intervalo admitido es L=68.58–76.2, W=45–63.5, H=120–152.4 mm. Se conserva el troquel-base.svg de 60 × 45 × 120 como representación de la captura original. Uso, resultados, fórmulas inferidas y evidencias están documentados en geometria/modelos/10001029/README.md. No está validado para fabricación ni se verificó exhaustivamente el intervalo.

## Tercer modelo: 102010, cierre inferior snap-lock

Se generó geometria/modelos/102010/troquel-generado.svg con las medidas iniciales solicitadas por el usuario: 120.6 × 60.6 × 161.1 mm de manufactura, cartón blanco 350 g de 0.5 mm. La geometría corresponde a la familia PairBuckle: 13 caras, 12 pliegues y 80 comandos de corte, en un plano de 377.9 × 282.25 mm. La salida predeterminada conserva los campos geométricos originales incluidos.

Las muestras mostraron un cambio de estructura del fondo: al aumentar L a 139.7 con W=60.6, el número de comandos de corte pasó a 92; al aumentar W a 76.2 regresó a 80. Por eso no se publicó un generador lineal general de L/W. El usuario confirmó continuar con las medidas originales, que se mantienen fijas en la salida.

Se añadió un motor afín L/W/H experimental ajustado con seis capturas de la topología de 80 cortes; el error máximo fue 1,82 mm y la base se reproduce exactamente. L, W y H son editables, con L ≤ 2W: por encima el fondo cambia a 92 cortes y se rechaza. No se validó una muestra física. Sangría y anotaciones quedan fuera. Uso y limitaciones en geometria/modelos/102010/README.md. No se validó fabricación ni equivalencia visual de los arcos con el editor.

## Cuarto modelo: 150010, caja mailer con tapa abatible

El enlace incluía el proyecto 70845997, que solicitó autenticación y no entregó su geometría. El usuario confirmó usar las medidas iniciales de la plantilla pública: 315 × 202 × 62 mm de manufactura, Onda E de 1.5 mm.

Se generó geometria/modelos/150010/troquel-base-publica.svg: 19 caras, 22 pliegues, 89 comandos de corte exterior y 4 ranuras interiores, sobre un plano de 576 × 590 mm. El renderizador común ahora incluye los trazados holes, necesarios para representar esas ranuras. Se verificó XML, conteos y correspondencia de la geometría incluida con la captura; se rasterizó e inspeccionó la vista local.

No se reconstruyó el proyecto privado ni se ajustó un motor de redimensionamiento para este modelo. La salida conserva las medidas públicas iniciales elegidas por el usuario. Sangría y anotaciones quedan fuera; no se validó fabricación. Procedencia y uso en geometria/modelos/150010/README.md.

## Quinto modelo: 112047, techo con cordón y fondo encajable

Se generó geometria/modelos/112047/troquel-generado.svg con las medidas iniciales: 70 × 50 × 60 mm, cartón blanco 350 g de 0.5 mm. La familia RoofWiringAndBottomBox contiene 19 caras, 18 pliegues, 72 comandos de corte exterior y 4 orificios superiores de radio 2 mm. El plano ocupa 252.5 × 152.5 mm.

Se conservaron los campos geométricos incluidos de la captura, se comprobaron XML y conteos, y se rasterizó e inspeccionó la salida local. La suma de pliegues coincide con la longitud declarada dentro del redondeo a centésimas. No se realizaron variaciones paramétricas; se entrega la configuración inicial fija, sin sangría ni anotaciones. Uso y evidencia en geometria/modelos/112047/README.md. No validado para fabricación.

## Sexto modelo: 12109002, caja para pastel con asas

Se generó geometria/modelos/12109002/troquel-generado.svg con las medidas iniciales 236 × 170 × 180 mm, Onda E de 1.5 mm. La familia TrapezoidalFoldingAngleHandleTrayBox contiene 19 caras, 26 pliegues, 46 comandos de corte exterior y 4 aberturas. El plano ocupa 824 × 1018 mm.

Se conservaron los campos geométricos incluidos, se comprobaron XML y conteos, y la longitud de pliegues coincide con el valor declarado dentro del redondeo a centésimas. Se rasterizó e inspeccionó la salida local, incluyendo asas y ranuras laterales. Se entrega la configuración inicial fija, sin sangría, anotaciones ni redimensionamiento. Uso y evidencia en geometria/modelos/12109002/README.md. No validado para fabricación.

## Séptimo modelo: 112310, caja con asa y fondo encajable

Se generó geometria/modelos/112310/troquel-generado.svg con las medidas iniciales 302 × 152 × 182 mm, Onda E de 1.5 mm. La familia BuckleSuitcaseForward contiene 16 caras, 15 pliegues, 72 comandos de corte exterior y 3 aberturas. El plano ocupa 952 × 439 mm.

Se verificaron XML, conteos y conservación de los campos geométricos incluidos. La suma de pliegues coincide con el valor declarado dentro del redondeo a centésimas. Se rasterizó e inspeccionó la salida local. Se entrega la configuración inicial fija, sin sangría, anotaciones ni redimensionamiento. Uso y evidencia en geometria/modelos/112310/README.md. No validado para fabricación.

## Octavo modelo: 10001006, caja con solapas insertables

Se generó geometria/modelos/10001006/troquel-generado.svg con las medidas iniciales 40 × 40 × 130 mm, cartón blanco 350 g de 0.5 mm. La familia Pair contiene 13 caras, 12 pliegues y 76 comandos de corte exterior, sin aberturas interiores. El plano ocupa 172.5 × 231 mm.

Se comprobaron XML, conteos y conservación de los campos geométricos incluidos. La suma de pliegues coincide con el valor declarado dentro del redondeo a centésimas. Se rasterizó e inspeccionó la salida local. Configuración inicial fija, sin sangría, anotaciones ni redimensionamiento. Uso y evidencia en geometria/modelos/10001006/README.md. No validado para fabricación.

## Noveno modelo: 10002003, caja con doble pestaña de colgado

Se generó geometria/modelos/10002003/troquel-generado.svg con las medidas iniciales 100 × 40 × 120 mm, cartón blanco 350 g de 0.5 mm. La familia PairWithHook contiene 16 caras, 15 pliegues, 94 comandos de corte exterior y 2 aberturas de colgado. El plano ocupa 295.5 × 263.75 mm.

Se comprobaron XML, conteos y conservación de los campos geométricos incluidos. La suma de pliegues coincide con el valor declarado dentro del redondeo a centésimas. Se rasterizó e inspeccionó la salida local. Configuración inicial fija, sin sangría, anotaciones ni redimensionamiento. Uso y evidencia en geometria/modelos/10002003/README.md. No validado para fabricación.

## Décimo modelo: 180370, envase para papas fritas

Se generó geometria/modelos/180370/troquel-generado.svg con las medidas iniciales 120 × 80 × 160 mm, cartón blanco 250 g de 0.35 mm. La familia ChipBox contiene 10 caras, 9 pliegues y 26 comandos de corte exterior, sin aberturas interiores. El plano ocupa 314.301396 × 453 mm.

Se comprobaron XML, conteos y conservación de los campos geométricos incluidos. La suma de pliegues coincide con el valor declarado dentro del redondeo a centésimas. Se rasterizó e inspeccionó la salida local, incluyendo los contornos curvos. Configuración inicial fija, sin sangría, anotaciones ni redimensionamiento. Uso y evidencia en geometria/modelos/180370/README.md. No validado para fabricación.

## Undécimo modelo: 180320, caja para sándwich con ventana

Se generó geometria/modelos/180320/troquel-generado.svg con las dos medidas iniciales expuestas: 120 × 75 mm, cartón blanco 350 g de 0.5 mm. H=0 es un campo auxiliar de la API; no se presenta como altura física. La familia WindowLockSandwichBox contiene 12 caras, 13 pliegues, 63 comandos de corte exterior y una ventana. El plano ocupa aproximadamente 289.4533 × 289.3779 mm.

Se comprobaron XML, conteos y conservación de los campos geométricos incluidos. La suma de pliegues coincide con el valor declarado dentro del redondeo a centésimas. Se rasterizó e inspeccionó la salida local. Configuración inicial fija, sin sangría, anotaciones ni redimensionamiento. Uso y evidencia en geometria/modelos/180320/README.md. No validado para fabricación.

## Duodécimo modelo: 187000, caja almohada (pillow box)

La ficha `custom-pillow-box-dieline-187000` expone 118 × 70 × 25 mm de manufactura, cartón blanco 350 g de 0,5 mm. La geometría se obtuvo del SVG que el editor dibuja en el DOM para esa configuración: 7 caras, 6 pliegues, sin orificios, con un corte de 143 × 155 mm (la imagen oficial, con 5 mm de sangría por lado, mide 153,5 × 165 mm). La API `project/knife?id=9351` respondió `code: 401`; la descarga vectorial exige inicio de sesión. Se descargaron la imagen oficial del troquel (905 × 1000) y el render 3D (1600 × 1216), ambos públicos en el CDN.

Se probó la interfaz para acotar los mínimos: 30 × 30 × 15 se convirtió en 30 × 30 × 10; 10 × 10 × 5 se elevó a 20 × 20 × 6,67; 118 × 70 × 5 volvió a 118 × 70 × 25. El mínimo efectivo observado es 20 × 20 × 6,67 mm, con advertencia de impresión por debajo de 30 × 30 × 10 mm; la altura está acoplada a las demás medidas. Con el pliego de 330 × 480 mm, el corte de 143 × 155 mm cabe y el editor calcula 6 cajas por pliego (2 × 3, giradas, con sangría de 3 mm); como cota geométrica del corte, W ≤ 231 mm y L + H ≤ 330 mm.

El modelo se dio de alta con el motor local `pillow187000`, que reconstruye corte, caras y pliegues a partir de L/W/H con `x0 = H/2`, `y0 = 15/18`, `R = (W²+H²)/(4H)` y `totalX = L+H`, `totalY = 2W+y0`. Se validó contra 7 capturas del editor (error máximo 0,00007 mm en corte y 0,00003 mm en caras) y quedó editable entre 20–323,33 mm de L, 20–231 mm de W y 6,67–200 mm de H, con H < W y pliego de 330 × 480 mm. Es experimental: no se verificó una exportación DXF/PDF ni una muestra física, y no se inventaron offsets internos/externos. Uso, archivos, procedencia y evidencias en geometria/modelos/187000/README.md.

## Decimotercer modelo: 188060, caja hexagonal

La ficha `custom-dimensions-polygonal-boxes-hexagonal-dieline-188060` expone **100,6 × 40,6 × 181,6 mm** de manufactura (interior 100 × 40 × 180; exterior 145,2 × 41 × 222,6), cartón blanco de 0,5 mm. La geometría se conservó de la respuesta `project/knife`: **19 caras, 26 pliegues y 28 cortes**, con un plano de **336,7 × 262,8 mm**. Se dio de alta con un motor de paneles L/W/H experimental: `totalX = 135,5 + 2L`, `totalY = 2W + H`, radios fijos. La base es exacta y L=110 se validó contra el SVG renderizado (error máximo 0,7 mm); W/H son analíticos y no tienen muestra independiente. La miniatura es el mockup oficial de Pacdora. Uso y límites en geometria/modelos/188060/README.md.
