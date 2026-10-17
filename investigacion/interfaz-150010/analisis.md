# Análisis del generador de plantillas Pacdora 150010

Fecha: 14 de octubre de 2026. Inspección con REA: navegador Chromium, ventana de 1440 × 1000, interfaz en español. Se inspeccionaron capturas, árbol de accesibilidad, DOM y solicitudes de red. No se modificó el editor local.

## Alcance y acceso

La URL solicitada, con `id=70847603`, presentó el diálogo «Iniciar sesión en Pacdora» en la sesión aislada de REA. Por ello, los resultados siguientes corresponden a la **plantilla pública 150010**, abierta sin ese identificador. No se comprobaron las medidas ni el contenido del proyecto 70847603.

## Organización de la interfaz

El patrón principal es un lienzo permanente y un panel lateral que cambia de contenido. Cambiar entre Modelos y Básico conserva el troquel, la vista 3D y las acciones de exportación en su lugar.

| Zona | Comportamiento observado | Aplicación a nuestro generador |
|---|---|---|
| Cabecera | Nombre del generador, menú, estado de guardado, diseño en línea, compartir y descargar | Mantener visibles el modelo activo y la descarga |
| Navegación izquierda | Rail de iconos: Modelos, Básico, Anticipado y Más | Usar Modelos y Medidas como accesos principales |
| Panel contextual | Contenedor blanco de aproximadamente 320 px, incluyendo un rail de 80 px | Alternar biblioteca y formulario sin abandonar el editor |
| Lienzo central | Troquel, cotas, leyenda y resumen de dimensiones sobre fondo gris | Reservar la mayor superficie al plano |
| Columna derecha | Vista 3D con deslizador de apertura; formatos y explicación de descarga | Separar vista del producto y exportación |
| Barra inferior | Selección, mano, acercar/alejar, colores y visibilidad de anotaciones | Controles persistentes para navegar por el plano |

Capturas: [Básico](basic_ready.png), [Modelos](models_loaded.png), [Más](more_open.png), [Anticipado](advanced_open.png).

## Biblioteca de modelos

La biblioteca tiene pestañas Biblioteca y Proyectos, búsqueda y selección de categoría. La categoría observada fue Cajas Plegables. Las tarjetas forman dos columnas y muestran **la caja montada**, con pequeñas muestras de material debajo. El listado puede desplazarse dentro del panel. Se observó la acción «Sustituir» en los elementos; no se ejecutó una sustitución.

La consecuencia para nuestra interfaz es concreta: la miniatura del producto montado ayuda a escoger la estructura; el plano desplegado sirve para editarla después. Conviene incluir nombre y código para diferenciar variantes parecidas.

## Editor Básico

La plantilla pública abrió con estos valores:

| Parámetro | Valor observado |
|---|---|
| Longitud × anchura × altura | 315 × 202 × 62 mm |
| Material | Onda E |
| Espesor | 1,5 mm; rango mostrado 1,1–2 mm |
| Dimensiones de manufactura | 315 × 202 × 62 mm |
| Dimensiones internas | 300 × 200 × 60 mm |
| Dimensiones externas | 316 × 204,5 × 63 mm |

El selector mm/in sí se comprobó: 315 pasó a 12,4016; 202 a 7,9528; 62 a 2,4409; y 1,5 a 0,0591. Al volver a mm se recuperaron los valores iniciales.

El desplegable de materiales mostró Cartulina blanca, Cartulina kraft, Papel arte y Cartón corrugado. No se seleccionó otro material ni se verificó su compensación geométrica.

Existen botones para dimensiones de manufactura, internas y externas. Al pulsar internas cambió la clase activa del control y apareció un estado de carga; los campos siguieron en 315/202/62 durante la captura. **La conversión entre modos quedó sin verificar.** No es suficiente para deducir sus fórmulas a partir de esta sesión.

## Plano y herramientas

La leyenda distingue sangría en verde, recorte en azul y pliegue en rojo discontinuo. El plano incluye cotas internas azules y dimensiones totales exteriores. El resumen superior presenta las tres clases de dimensiones simultáneamente.

El menú de visibilidad ofrece dimensiones generales, dimensiones básicas, línea de corte e información de anotación. El control de color abrió una edición de Recorte con valor hexadecimal `#2028b0`. Se comprobó que los menús abren; no se alteraron sus valores.

La vista 3D muestra la caja montada y un deslizador de apertura. No se probó su animación ni la sincronización con nuevas medidas. La presencia de cotas en el plano tampoco demuestra por sí sola que se puedan editar directamente.

## Exportación y funciones secundarias

Se mostraron opciones AI, PDF, DXF y maqueta 3D. No se descargaron archivos ni se comprobó su disponibilidad en una cuenta determinada.

Anticipado presenta numerosos parámetros técnicos y una invitación a actualizar al plan Negocios. Al abrirlo aparecen muchas cotas adicionales sobre el plano. Para el alcance solicitado anteriormente, puede omitirse esta sección.

Más reúne servicios como diseño en línea, impresión, herramientas de IA e integración con Illustrator. Es una sección secundaria respecto a seleccionar modelo, ajustar medidas y obtener el troquel.

## Arquitectura inferida

El DOM y las solicitudes sugieren una aplicación con estado compartido entre biblioteca, parámetros y lienzo. Se observaron peticiones de detalles de modelo, categorías, materiales y geometría mediante rutas como `models/details`, `models/ctree`, `material_effect` y `project/knife`. Sus nombres y parámetros son evidencia de comunicación, no una especificación completa de las fórmulas.

Durante la secuencia de biblioteca apareció un `POST /api/v2/projects`, seguido de consultas a un identificador nuevo. Esto no corresponde al proyecto solicitado y no demuestra persistencia duradera. La atribución exacta de la petición a una acción concreta no queda establecida por el orden de recepción de eventos.

## Prioridad para nuestro generador

1. Biblioteca con miniaturas de cajas montadas, nombre y código; selección que carga los parámetros del modelo.
2. Panel Medidas con longitud, anchura, altura, unidades, material y espesor, sujeto a los parámetros realmente soportados por cada generador.
3. Lienzo que se actualiza con las medidas y conserva zoom y desplazamiento; cotas claras y controles de visibilidad.
4. Exportación vinculada al estado actual. Incorporar otros formatos cuando exista un exportador verificado para ellos.

Las compensaciones de material, los modos interno/externo y el plegado 3D requieren implementación y validación por estructura. Esta inspección no permite derivarlos únicamente de la apariencia de los controles.

## Evidencia reproducible

| Archivo | Evidencia REA | Cobertura |
|---|---|---|
| [Proyecto](proyecto-evidencia.json) | `ev_6e1034e685c578f4c8bf2484e16f6cbb0edc8714066eba7913b9c5e318932172` | URL exacta; autenticación requerida |
| [Básico](basico-evidencia.json) | `ev_ab4d82b6083ec032ea60501004c9482747bbad429dc016bfbca7b360696ac6e5` | Estado público inicial y captura |
| [Paneles](paneles-evidencia.json) | `ev_11786905427e6c43b26c80a8d25f558ef541acd27ae098d1634876915997112c` | Biblioteca, mm/in, Más y Anticipado |
| [Controles](controles-evidencia.json) | `ev_43446cea86be031c95fa044f36ecc7ad0c352bb8a5e81b7ea33a5f23dc7f432f` | Materiales, modo interno, visibilidad y color |

Limitaciones: las capturas son de escritorio; no se evaluó adaptación móvil. El DOM conserva paneles ocultos, por lo que la visibilidad se contrastó con las imágenes. Algunas solicitudes seguían pendientes al cerrar las capturas; no se obtuvieron cuerpos de respuesta ni se validaron fórmulas, descarga o guardado.
