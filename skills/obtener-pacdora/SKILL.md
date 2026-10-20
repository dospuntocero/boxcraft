---
name: obtener-pacdora
description: Adquirir una caja de Pacdora por código mediante REA, documentar geometría, materiales y dimensiones, obtener su icono e integrarla localmente. Activar con «obtener CODIGO» en este proyecto.
---

# Obtener una caja de Pacdora

Interpreta `obtener CODIGO` como la instrucción completa siguiente. Conserva todos los dígitos del código. Acepta opciones en lenguaje natural, por ejemplo `obtener 15030101, 200 × 120 × 80 mm, cartulina de 0,5 mm, pliego 1000 × 700 mm`. Este ejemplo no ordena adquirirlo al leer la skill.

## Prompt de ejecución

Obtén el modelo indicado de Pacdora y completa la investigación REA, reconstrucción geométrica local, ficha técnica, icono y alta en el editor de este proyecto. Usa la skill REA disponible. Trabaja hasta dejar los archivos y la integración verificables; una propuesta o captura aislada no completa el pedido.

### Identidad y preparación

Revisa `geometria/modelos/`, `investigacion/materiales/`, `editor-troqueles/` y las aplicaciones existentes. Determina la aplicación fuente vigente antes de editar; utiliza `editor-troqueles/` como única aplicación vigente. Reutiliza evidencia completa del mismo modelo y configuración, sin sobrescribir originales.

Localiza y verifica la página real por código, título y familia. No inventes el slug de la URL. Selecciona la sesión del usuario si existe mediante las herramientas admitidas. Usa los esquemas reales de REA. Si la evidencia excede el transporte, utiliza vistas o exportación del registro sin repetir una captura completada.

### Dimensiones, materiales y parámetros

Sin opciones, conserva como base los valores iniciales de Pacdora. Prioriza la configuración solicitada si la hay. Registra, por configuración:

- Medidas solicitadas y efectivas, unidades, significado de los ejes y modo interior/exterior/manufactura. Usa mm como unidad canónica. No introduzcas una altura ficticia en modelos de dos ejes.
- Material: ID, nombre, familia, espesor efectivo, opciones disponibles y límites/pasos observados para este modelo.
- Parámetros avanzados accesibles, valores originales, cambios automáticos, compensaciones internas/externas, radios, pestañas, ranuras y cierres presentes en las respuestas.
- Extensión real del troquel, pliego y orientación admitida. No heredes límites de otras cajas como universales.

Enumera los materiales/espesores ofrecidos por este modelo y captura sus combinaciones discretas accesibles. Para intervalos continuos, registra rango y paso y toma muestras representativas y límites: no declares agotado el intervalo. Lleva una matriz de casos completos, rechazados, bloqueados y pendientes.

Verifica la selección efectiva después de cada cambio y espera la respuesta correspondiente. Pacdora puede cambiar el material al cambiar medidas. El campo `science` puede conservar el material inicial: contrasta el control visible con `layer.traditional.science_id` y `layer.traditional.thickness` cuando existan. Una selección solicitada no demuestra que la geometría corresponda a ella.

### Evidencia y reconstrucción

Conserva solicitudes y respuestas originales, fecha, URL, referencias REA y configuración solicitada/efectiva. Captura corte exterior, aberturas interiores, pliegues, caras, curvas/arcos y metadatos. Registra sangría y cotas si existen y explica qué capas se reproducen.

Para reconstruir dimensiones variables, varía un eje por vez y valida después combinaciones independientes no usadas para ajustar reglas. Repite por material/espesor cuando cambie el comportamiento. No sustituyas compensaciones por escalado uniforme. Si cambia la topología, distingue los casos o limita el motor a configuraciones exactas.

Genera un motor local reproducible que funcione sin consultar Pacdora al abrir o descargar el resultado. Habilita únicamente ejes, materiales y rangos sustentados por evidencia. Separa reglas comprobadas, aproximaciones experimentales y desconocidos. No habilites silenciosamente un ajuste que falle la comparación. Conserva las geometrías exactas útiles aunque no pueda reconstruirse un motor paramétrico completo.

### Documento e icono

Obtén la miniatura/icono del recurso que realmente usa Pacdora y guárdalo localmente con URL, tipo y SHA-256. Verifica que corresponde al código y que el editor no dependa de cargarlo remotamente. Si el original no es accesible, genera una miniatura desde la geometría local e identifícala como generada. No simules un icono original mediante IA.

El documento predeterminado es `geometria/modelos/CODIGO/README.md`: identidad y fuentes; medidas/modos; materiales y espesores; matriz de cobertura; parámetros; extensión y pliego; reglas; archivos; reproducción; validaciones y límites. Incluye vista del troquel e icono. Si el usuario pide DOCX o PDF, produce además ese formato usando su skill y verifica el renderizado.

### Entregables y alta local

Sigue los esquemas reales del proyecto. Conserva en `geometria/modelos/CODIGO/`:

- `README.md`, `base/` con respuesta original y manifiesto, y muestras adicionales por configuración.
- `troquel-generado.svg`, `troquel-generado.json`, `vista-previa.png` y generador reproducible.
- Icono local y `validacion.json`.
- Manifiesto de procedencia: código, URL, fecha, configuraciones solicitadas/efectivas, unidades, rutas, hashes, referencias REA y estado de captura. Puede formar parte del manifiesto base.

Integra modelo, icono y configuraciones comprobadas en el catálogo local y sus procesos de preparación de datos. Comprueba selección, medidas, materiales, capas, previsualización y exportación. No habilites combinaciones sin geometría. Si el usuario pide solo investigación/documentación, omite el alta. Publicación, despliegue y subida de cambios quedan fuera del alias.

### Validación y cierre

Comprueba JSON/XML válidos, valores finitos, extensión positiva y correspondencia geométrica con las respuestas originales, incluyendo arcos, pliegues y aberturas. Compara muestras independientes campo a campo y documenta tolerancia y error máximo; conteos iguales no prueban equivalencia. Rasteriza e inspecciona el SVG y compara visualmente con la referencia accesible. Verifica ajuste al pliego cuando sus límites estén establecidos.

Ejecuta las pruebas existentes pertinentes y comprueba el archivo exportado, no solo el botón. Declara las verificaciones que no pudieron realizarse. La equivalencia digital no acredita armado físico ni aptitud de fabricación.

Ante autenticación, pago, HTTP 403 o controles deshabilitados, conserva lo obtenido y registra el bloqueo sin eludir restricciones ni repetir intentos idénticos. Completa tareas independientes y enumera pendientes. `cleanup_incomplete` no acredita cierre correcto de sesión, aunque sus respuestas completas puedan servir como observaciones verificables.

Entrega enlaces al documento, SVG, vista previa e icono, ubicación del alta, pruebas y alcance efectivo de dimensiones/materiales. Declara completo solo lo producido y verificado; si faltan entregables requeridos, informa resultado parcial y motivo.
